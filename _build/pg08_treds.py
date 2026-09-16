#!/usr/bin/env python3
# Session 80 — PRODUCT GUIDE 08: Invoice discounting and TReDS
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product: turning an unpaid invoice into cash before the
buyer pays. An MSME has delivered, raised an invoice, and now waits 45 to 90 days. A financier pays
most of it today and collects from the buyer at maturity.</p>
''' + warn("<strong>The framework was rewritten three months before this page was written.</strong> The <strong>RBI (Trade Receivables Discounting System) Directions, 2026</strong> (RBI/DPSS/2026-27/406, <strong>23 June 2026</strong>) replaced the 2014 TReDS Guidelines and the 2023 scope circular &mdash; eight years of scattered instructions consolidated into one Master Direction, effective immediately. Several things that were barriers are now gone, and anything written before June 2026 describes the old regime.")

g_what = '''
<p>TReDS is an RBI-regulated marketplace. An MSME uploads an invoice raised on a large buyer, the
buyer accepts it, and <strong>banks and NBFCs bid against each other</strong> to finance it. The
seller takes the best bid and gets cash in about <strong>T+2</strong> instead of waiting out the
credit period.</p>
<p>Four roles, and you need to know which one you are before anything else:</p>
<table>
<tr><th>Role</th><th>What you do</th><th>What you need</th></tr>
<tr><td><strong>Seller</strong></td><td>MSME. Uploads the invoice, takes a bid.</td><td>MSME status. <strong>Onboarding due diligence was removed in 2026</strong>.</td></tr>
<tr><td><strong>Buyer</strong></td><td>Corporate, PSU or government department. Accepts the invoice and pays at maturity.</td><td>Onboarding, and the discipline to accept promptly.</td></tr>
<tr><td><strong>Financier</strong></td><td>Bank or NBFC. Bids, funds, collects at maturity.</td><td>A licence, and an appetite for <em>buyer</em> risk.</td></tr>
<tr><td><strong>Platform operator</strong></td><td>Runs the exchange.</td><td><strong>RBI authorisation and &#8377;25 crore net worth.</strong> Three exist today.</td></tr>
</table>
''' + note("<strong>The single most important thing to understand about this product: the financier takes exposure on the BUYER, not the seller.</strong> A small supplier with no credit history can access finance at a large buyer's risk profile, because the buyer has already accepted the invoice. That inversion is the whole point &mdash; and it is why the 2026 Directions removed seller-side due diligence at onboarding as an unnecessary barrier.") + '''
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not a loan to the MSME.</strong> Financing is <strong>without recourse</strong> &mdash;
if the buyer defaults, the financier pursues the buyer, not the seller.</li>
<li><strong>Not a receivable you can discount twice.</strong> Assignment must be registered with
CERSAI.</li>
<li><strong>Not the only route.</strong> Off-platform invoice discounting exists and is a different,
lighter regime with different risks. See step 1.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>On TReDS, or off it?</strong></td><td>The decision that determines every other one.</td></tr>
<tr><td>2</td><td><strong>Onboard</strong></td><td>And understand what 2026 removed.</td></tr>
<tr><td>3</td><td><strong>Get the invoice in</strong></td><td>Structured, validated, matched to a purchase order.</td></tr>
<tr><td>4</td><td><strong>Buyer acceptance</strong></td><td>Everything hangs on this. It is also the bottleneck.</td></tr>
<tr><td>5</td><td><strong>The auction</strong></td><td>Financiers bid. The seller picks.</td></tr>
<tr><td>6</td><td><strong>Register the assignment</strong></td><td>CERSAI. Now expressly required.</td></tr>
<tr><td>7</td><td><strong>Fund and settle</strong></td><td>T+2 to the seller, at maturity from the buyer.</td></tr>
<tr><td>8</td><td><strong>Maturity, default, re-discounting</strong></td><td>Including the new ability to sell the receivable on.</td></tr>
</table>
''' + note("Step 4 is where this product lives or dies. An invoice nobody has accepted is not financeable, and buyer acceptance is a human workflow inside somebody else's accounts payable department. Everything else on this page is easier than that.")

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; On TReDS, or off it?</h3>
<table>
<tr><th></th><th>On TReDS</th><th>Off-platform</th></tr>
<tr><td><strong>Regulation</strong></td><td>RBI-authorised platform, TReDS Directions 2026</td><td>Bilateral factoring or an NBFC product</td></tr>
<tr><td><strong>Recourse</strong></td><td><strong>Without recourse to the MSME</strong></td><td>Usually with recourse &mdash; the seller carries the risk</td></tr>
<tr><td><strong>Pricing</strong></td><td><strong>Competitive bidding</strong> pushes rates down</td><td>One financier, one price</td></tr>
<tr><td><strong>Buyer</strong></td><td>Must be onboarded and must accept</td><td>May not need to be involved at all</td></tr>
<tr><td><strong>Build cost</strong></td><td>Integrate with an existing platform</td><td>Build the whole thing</td></tr>
</table>
''' + warn("<strong>If you are considering becoming the platform: &#8377;25 crore minimum net worth</strong>, certified by a statutory auditor, aligned with other non-bank payment system operators. Existing authorised operators have until <strong>31 March 2028</strong> to comply. <strong>Three platforms currently operate in India.</strong> This is a licensed marketplace business, not a feature you add.") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; Onboarding, and what 2026 removed</h3>
<p>The single biggest practical change: <strong>mandatory due diligence on the MSME seller at
onboarding is gone.</strong></p>
<p>The reasoning is sound and worth internalising, because it shapes the whole product: the financier
is taking exposure on the <em>buyer's accepted invoice</em>, not on the seller's balance sheet. Asking
a small supplier for financials in order to access finance secured on someone else's credit was a
barrier with no risk purpose.</p>
<p><strong>What the platform must still do:</strong></p>
<ul>
<li><strong>Validate MSME status</strong> &mdash; the eligibility itself is still checked.</li>
<li><strong>Ensure funds are credited only to the seller's own account.</strong> This is the control
that replaces the removed due diligence, and it is the one to get right.</li>
</ul>
'''

code_invoice = code('Python — steps 3 and 4, the invoice and the acceptance that gates everything', r'''from datetime import date, timedelta
from decimal import Decimal

def validate_invoice(inv, po, seller, buyer):
    """An invoice nobody can match to a delivery is an invoice nobody accepts."""
    fail = []
    if not seller["msme_status_verified"]:
        fail.append("seller_not_verified_msme")      # eligibility, not diligence
    if inv["buyer_id"] != buyer["id"]:
        fail.append("buyer_mismatch")
    if po and inv["amount_paise"] > po["amount_paise"]:
        fail.append("exceeds_po_value")
    if inv["due_date"] <= date.today():
        fail.append("already_due")                    # nothing left to discount
    if inv["due_date"] > date.today() + timedelta(days=365):
        fail.append("tenor_too_long")
    if inv.get("already_assigned"):
        # CERSAI is the authoritative answer. Check it, do not assume.
        fail.append("already_assigned_elsewhere")
    return {"ok": not fail, "reasons": fail}

# STEP 4. THE BOTTLENECK. An accepted factoring unit carries the enforceability
# of a physical instrument -- which is exactly why the buyer's acceptance is
# the thing everything waits on, and why it sits inside somebody else's
# accounts payable process rather than yours.

def acceptance_state(fu, now=None):
    now = now or date.today()
    age = (now - fu["uploaded_on"]).days
    if fu["status"] == "ACCEPTED":
        return {"financeable": True, "days_to_accept": fu["accepted_in_days"]}
    if fu["status"] == "REJECTED":
        return {"financeable": False, "reason": fu["rejection_reason"],
                "action": "resolve_with_buyer_then_reupload"}
    # PENDING. This is where working capital dies quietly.
    return {"financeable": False, "pending_days": age,
            "escalate": age > fu["buyer_sla_days"],
            "action": "chase_named_AP_contact" if age > fu["buyer_sla_days"] else "wait"}

# WHAT TO CHECK
# [ ] measure TIME TO ACCEPTANCE per buyer, as a distribution. It is the single
#     most useful number in this product and almost nobody reports it. A buyer
#     with a 14-day median acceptance is not offering early payment, whatever
#     the credit terms say
# [ ] a rejected invoice needs a REASON the seller can act on. "Rejected" with
#     no reason sends an MSME back to a corporate switchboard
# [ ] check CERSAI before financing, not after. A receivable assigned twice is
#     a fraud you will discover at maturity
# [ ] match to a purchase order where one exists. PO-backed invoices get
#     accepted faster because the buyer's AP team has less to verify
# [ ] escalation goes to a NAMED contact in the buyer's AP team, agreed at
#     buyer onboarding. A generic inbox is where acceptance requests go to die
# [ ] never let a seller upload the same invoice twice under different
#     references. Deduplicate on buyer + invoice number + amount + date
''')

i_step34 = '''
<h3 id="s-indigo-s3">Steps 3 and 4 &mdash; The invoice, and the acceptance</h3>
''' + code_invoice + '''
<p><strong>The gotcha nobody documents:</strong> <strong>time to acceptance is the product metric,
and nobody measures it.</strong> Platforms report volumes financed and rates achieved. Neither tells
an MSME what they need to know, which is <em>how long does this buyer take to accept</em>. A buyer
with a 14-day median acceptance on a 45-day invoice has removed two thirds of the benefit before a
financier has seen it. Measure it per buyer, publish it to sellers, and use it in buyer onboarding
&mdash; a buyer who will not commit to an acceptance SLA is telling you something.</p>
'''

code_settle = code('Python — steps 6 to 8, assignment, settlement and what happens at maturity', r'''# STEP 6. CERSAI registration of the assignment is now EXPRESSLY REQUIRED.
# It is the public record that this receivable now belongs to the financier,
# and it is what makes double-discounting detectable rather than discoverable.

def register_assignment(fu, financier, cersai):
    rec = cersai.register(
        receivable_ref=fu["id"], assignor=fu["seller_id"],
        assignee=financier["id"], amount_paise=fu["amount_paise"],
        due_date=fu["due_date"])
    assert rec["status"] == "REGISTERED", "do not fund an unregistered assignment"
    return rec

# STEP 7. Settlement may run over ANY authorised payment system. Two legs,
# opposite directions, months apart.
def settle_legs(fu, bid):
    return {
        "to_seller": {"when": "T+2", "amount": fu["amount_paise"] - bid["discount_paise"],
                      "to": "seller_own_account_only"},   # the 2026 control
        "from_buyer": {"when": fu["due_date"], "amount": fu["amount_paise"],
                       "to": bid["financier_account"]},
    }

# STEP 8. AT MATURITY.
def at_maturity(fu, payment, guarantee=None, insurance=None):
    if payment and payment["received"]:
        return {"outcome": "settled"}
    # WITHOUT RECOURSE. The financier pursues the BUYER. The MSME seller is not
    # liable and must not be chased -- this is the protection that makes the
    # product usable by small suppliers at all.
    remedies = ["pursue_buyer"]
    if guarantee:  remedies.append("invoke_credit_guarantee")   # GoI-notified trust
    if insurance:  remedies.append("claim_insurance")           # premium NOT on the seller
    return {"outcome": "buyer_default", "remedies": remedies,
            "seller_liable": False}

# NEW IN 2026: a financier may RE-DISCOUNT -- sell a financed factoring unit to
# another financier before maturity. That frees the original financier's capital
# and is the mechanism that lets the market scale beyond one balance sheet.
def rediscount(fu, from_fin, to_fin, price_paise, cersai):
    cersai.update_assignee(fu["id"], new_assignee=to_fin["id"])
    return {"fu": fu["id"], "from": from_fin["id"], "to": to_fin["id"],
            "price_paise": price_paise, "recourse_to_seller": False}

# WHAT TO CHECK
# [ ] never fund before the CERSAI registration returns REGISTERED
# [ ] funds credit ONLY to the seller's own verified account. This is the
#     control that replaced seller due diligence -- treat it accordingly
# [ ] "without recourse" is enforced in your collections logic, not just in the
#     contract. A dunning system that contacts the seller on buyer default is
#     the single worst failure available in this product
# [ ] re-discounting updates the CERSAI assignee. A stale record makes the new
#     financier's claim harder to enforce exactly when it matters
# [ ] insurance premium is NEVER charged to the MSME seller. Expressly barred
# [ ] credit guarantee cover may come from ANY GoI-notified Credit Guarantee
#     Fund Trust -- check which your financiers actually hold, per buyer segment
''')

i_step68 = '''
<h3 id="s-indigo-s6">Steps 5 to 8 &mdash; Auction, assignment, settlement, maturity</h3>
<p>The auction itself is the simplest part: financiers bid a discount rate, the seller takes one.
Competitive bidding is why on-platform pricing beats a bilateral arrangement.</p>
''' + code_settle + '''
<p><strong>The gotcha nobody documents:</strong> &ldquo;without recourse&rdquo; has to be enforced in
the <em>collections system</em>, not just written in the contract. When a buyer defaults, a generic
dunning workflow will happily start contacting the party it has a phone number for &mdash; which is
the MSME seller. That is the exact harm the structure exists to prevent, it destroys the trust the
product depends on, and it is a code path, not a policy question. <strong>Assert it: the seller is
never a collections target on a TReDS factoring unit.</strong></p>

<h3 id="s-indigo-s2026">What the 2026 Directions changed, in one place</h3>
<table>
<tr><th>Change</th><th>Why it matters</th></tr>
<tr><td><strong>Seller due diligence removed at onboarding</strong></td><td>The barrier that kept small suppliers off the platform. Risk sits on the buyer.</td></tr>
<tr><td><strong>Re-discounting permitted</strong></td><td>A financier can sell on before maturity. The market is no longer capped by individual balance sheets.</td></tr>
<tr><td><strong>Credit guarantee from any GoI-notified fund trust</strong></td><td>Financiers can cover buyer default. Widens who will bid, and on whom.</td></tr>
<tr><td><strong>Insurance companies recognised as participants</strong></td><td>Another risk-transfer route &mdash; and the <strong>premium may not be passed to the seller</strong>.</td></tr>
<tr><td><strong>CERSAI registration expressly required</strong></td><td>Double-discounting becomes detectable rather than discoverable.</td></tr>
<tr><td><strong>Accepted units carry instrument enforceability</strong></td><td>An accepted factoring unit has the standing of a physical instrument.</td></tr>
<tr><td><strong>&#8377;25 crore operator net worth</strong></td><td>Aligned with non-bank PSOs. Existing operators have until 31 March 2028.</td></tr>
<tr><td><strong>Settlement via any authorised payment system</strong></td><td>Removes a plumbing constraint.</td></tr>
</table>
'''

i_cost = registry("Invoice discounting &mdash; what it costs", [
 ("The discount, to the seller", "direct",
  "The financier's margin, set by <strong>competitive bidding</strong> on TReDS rather than by one "
  "lender's price. This is the main reason on-platform beats bilateral for an MSME."),
 ("Platform fees", "direct",
  "Charged by the operator to participants. Modest per transaction; the three operators price "
  "differently and it is worth comparing if you have volume."),
 ("Becoming an operator", "direct",
  "<strong>&#8377;25 crore net worth</strong>, statutory-auditor certified, plus RBI authorisation. "
  "Existing operators have until <strong>31 March 2028</strong>. Reporting: annual net-worth "
  "certificates, monthly statistics, non-periodic director declarations."),
 ("Credit guarantee", "direct",
  "Available to financiers from any <strong>GoI-notified Credit Guarantee Fund Trust</strong>. Cost "
  "sits with the financier and shows up in the bid, not as a separate charge."),
 ("Insurance", "direct",
  "Permitted, and <strong>the premium may NOT be charged to the MSME seller</strong>. It is a "
  "financier-side cost, reflected in pricing."),
 ("CERSAI registration", "direct",
  "Per assignment. Small, mandatory, and cheaper than discovering a double assignment at maturity."),
 ("The real cost to the MSME", "direct",
  "<strong>Time to acceptance.</strong> An invoice sitting unaccepted for three weeks has already "
  "consumed most of the benefit, whatever discount rate it eventually attracts. <strong>This is not "
  "a fee and it is not on any rate card.</strong>"),
], "September 2026") + note("<strong>Compare the discount against the alternative, not against zero.</strong> An MSME's alternative to discounting is usually an overdraft, a supplier delay, or a missed order. A discount that looks expensive next to a bank rate can be cheap next to the cost of not taking the next order &mdash; and that is the comparison the seller is actually making.")

a_builds = '''
<h3 id="s-amber-week">Integrating with a platform</h3>
<p><strong>Build:</strong> pick one of the three operators &rarr; seller onboarding with MSME status
validation &rarr; invoice upload with PO matching and deduplication &rarr; acceptance tracking with a
named buyer contact &rarr; settlement reconciliation.</p>
<p><strong>You get:</strong> working capital access for your sellers without becoming a regulated
marketplace.</p>

<h3 id="s-amber-proper">The financier side</h3>
<p><strong>Build:</strong> buyer-risk scoring rather than seller-risk scoring &rarr; automated bidding
with per-buyer limits &rarr; CERSAI checks before funding and registration after &rarr;
<strong>collections that structurally cannot target the seller</strong> &rarr; credit guarantee and
insurance cover mapped per buyer segment &rarr; a re-discounting path to free capital.</p>
<p><strong>Trade:</strong> your credit model is about companies you have no relationship with. That
is a different modelling problem from consumer or SME lending, and the data is thinner.</p>

<h3 id="s-amber-big">Becoming a platform</h3>
<p><strong>Build:</strong> RBI authorisation, &#8377;25 crore net worth, the exchange itself, buyer
and financier networks on both sides.</p>
<p><strong>It breaks when:</strong> you underestimate that this is a <em>marketplace</em> problem.
Three operators exist and the constraint has never been technology &mdash; it is getting buyers to
onboard and accept promptly.</p>
''' + note("If you take one thing from this page: <strong>measure and publish time-to-acceptance per buyer.</strong> It is the number that determines whether the product delivers anything to an MSME, no platform reports it, and it is entirely measurable from data you already have.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Invoices sit unaccepted</strong></td><td>No named AP contact, no SLA, no escalation.</td><td>Agree an acceptance SLA at buyer onboarding; escalate to a person.</td></tr>
<tr><td><strong>The seller gets chased on buyer default</strong></td><td>Generic dunning used the contact it had.</td><td>Without recourse asserted in code, not just contract.</td></tr>
<tr><td><strong>A receivable is financed twice</strong></td><td>CERSAI checked after funding, or not at all.</td><td>Check before, register after, never fund unregistered.</td></tr>
<tr><td><strong>Insurance premium on the seller's statement</strong></td><td>Passed through as a cost.</td><td>Expressly barred. It is a financier cost.</td></tr>
<tr><td><strong>Seller onboarding still asks for financials</strong></td><td>Built against the pre-2026 rules.</td><td>Removed in 2026. Validate MSME status and the bank account instead.</td></tr>
<tr><td><strong>Funds reach a third-party account</strong></td><td>The account control was not enforced.</td><td>Seller's own verified account only — this is the control that replaced due diligence.</td></tr>
<tr><td><strong>Re-discounting leaves a stale CERSAI record</strong></td><td>Assignee never updated.</td><td>Update on every transfer.</td></tr>
<tr><td><strong>Duplicate invoice uploads</strong></td><td>No deduplication key.</td><td>Buyer + invoice number + amount + date.</td></tr>
</table>
'''

SRC=[('official','RBI (Trade Receivables Discounting System) Directions, 2026','circular RBI/DPSS/2026-27/406 dated 23 June 2026, effective immediately, replacing the 2014 TReDS Guidelines and the 2023 scope circular. Removal of seller onboarding due diligence, ₹25 crore operator net worth with a 31 March 2028 transition, credit guarantee from GoI-notified fund trusts, insurance participation with premium not chargeable to sellers, re-discounting, mandatory CERSAI registration, instrument enforceability of accepted factoring units, settlement via any authorised payment system, and the reporting obligations.','https://www.rbi.org.in'),
 ('official','CERSAI','registration of the assignment of receivables, and the check that makes double-discounting detectable.','https://www.cersai.org.in'),
 ('official','MSME registration (Udyam)','the MSME status the platform must validate at onboarding.','https://udyamregistration.gov.in'),
 ('official','Factoring Regulation Act and RBI factoring framework','the without-recourse structure underneath TReDS financing.','https://www.rbi.org.in'),
 ('industry','TReDS operator and practitioner commentary','the T+2 timeline, the 45–90 day credit periods, the three operational platforms, and the Budget 2026-27 measures (CPSE settlement, CGTMSE guarantees, GeM integration, securitisation of TReDS receivables). Verify any specific figure against the Directions.',''),
 ('industry','MSME financing analysis','the argument that seller-side due diligence was a barrier without a risk purpose, since exposure sits on the accepted buyer invoice.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'+(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. These Directions are three months old; anything written earlier describes the 2014 regime.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/products/co-lending/" class="mod-card"><div class="mod-num">GUIDE 07</div><h3>Co-Lending</h3><p>The other way a bank and an NBFC fund the same borrower — and its own 2025 rewrite.</p></a>
<a href="/fintech-ai/credit-underwriting/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 02</div><h3>Credit &amp; Underwriting</h3><p>Scoring a buyer you have no relationship with is a different modelling problem.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Two settlement legs in opposite directions, months apart, on one factoring unit.</p></a>
<a href="/fintech-ai/aml-compliance/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 04</div><h3>AML &amp; Compliance</h3><p>Trade finance is a classic laundering vector; invoice-value manipulation is the typology to know.</p></a>
</div>
''' + warn("This page is a guide, not a specification. TReDS is an RBI-authorised payment system and financing receivables carries obligations under the Directions, the factoring framework and FEMA where the buyer is overseas. Nothing here is legal advice. Have your structure, your account controls and your collections logic reviewed by qualified counsel before the first invoice is financed.")

lanes={'green':[("How to use this page",g_read),("What invoice discounting actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — the route, and onboarding",i_step12),
           ("Steps 3 and 4 — the invoice and the acceptance",i_step34),
           ("Steps 5 to 8 — auction, assignment, settlement, maturity",i_step68),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Invoice Discounting: How to Build It"
META=("Build an invoice discounting product step by step: the eight stages, the 2026 TReDS Directions, "
      "and what buyer acceptance really costs.")
LEAD=("A step-by-step guide to building invoice discounting and TReDS integration in India. Eight "
      "stages, the options at each one, exactly how each step connects to the next, real costs, and "
      "what breaks. Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/invoice-discounting",title=TITLE,meta=META,lead=LEAD,label="Product Guide 08",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/invoice-discounting/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)
