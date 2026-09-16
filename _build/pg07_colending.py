#!/usr/bin/env python3
# Session 78 — PRODUCT GUIDE 07: Co-lending
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product: two regulated lenders funding the same loan to
the same borrower, at the same time. A bank brings cheap money, an NBFC brings reach and
underwriting.</p>
''' + warn("<strong>Everything written about co-lending before August 2025 describes a repealed framework.</strong> The <strong>RBI (Co-Lending Arrangements) Directions, 2025</strong> (issued 6 August 2025, refs RBI/DOR/2025-26/139 and DOR.STR.REC.44/13.07.010/2025-26) took effect <strong>1 January 2026</strong> and repealed the 2020 circular entirely. Three things changed that invalidate most existing designs: <strong>the bank can no longer reject loans after sourcing</strong>, <strong>the borrower must be charged a single blended rate</strong>, and <strong>both partners retain 10%</strong> rather than the NBFC retaining 20%.")

g_what = '''
<p>Co-lending exists because banks and NBFCs have opposite problems. A bank has cheap deposits and
weak reach into small-ticket and rural lending. An NBFC has the reach and the underwriting but funds
itself expensively. Put them on the same loan and the borrower gets a rate neither could offer
alone.</p>
<table>
<tr><th>Who may participate</th><th>Who may not</th></tr>
<tr><td>Commercial banks &middot; All-India Financial Institutions &middot; NBFCs including housing finance companies</td><td><strong>Small finance banks, regional rural banks and local area banks are excluded</strong></td></tr>
</table>
<p><strong>The 2025 Directions changed the shape of the product, not just its paperwork:</strong></p>
<table>
<tr><th>Item</th><th>2020 model</th><th>2025 Directions</th></tr>
<tr><td>Scope</td><td>Priority sector only</td><td><strong>All lending</strong></td></tr>
<tr><td>Retention</td><td>NBFC 20%</td><td><strong>Each partner 10%, both sides</strong></td></tr>
<tr><td>Bank's choice</td><td>Could reject loans after sourcing</td><td><strong>Irrevocable back-to-back commitment. Discretion abolished</strong></td></tr>
<tr><td>Pricing</td><td>Hurdle rate, each lender priced separately</td><td><strong>One blended rate to the borrower</strong></td></tr>
<tr><td>Transfer</td><td>Loosely specified</td><td><strong>Within 15 calendar days</strong></td></tr>
</table>
''' + note("<strong>The blended rate is the change with the most commercial consequence.</strong> Under the hurdle-rate model an NBFC could price the borrower above its own cost and keep the spread created by the bank's cheaper funds. A single weighted-average rate removes that margin entirely. If your co-lending business case was built on it, the business case is gone &mdash; and that is the point of the rule.") + '''
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not loan sale.</strong> Buying loans after origination is the <strong>Transfer of Loan
Exposures</strong> regime &mdash; a different rulebook with different economics.</li>
<li><strong>Not two loans.</strong> One borrower, one loan, one rate, one point of contact.</li>
<li><strong>Not outside digital lending rules.</strong> A digital co-lending arrangement is governed
by <em>both</em> these Directions <em>and</em> the Digital Lending Directions, 2025.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Find a partner, write the CLA</strong></td><td>A board-approved policy and a formal agreement. Before any code.</td></tr>
<tr><td>2</td><td><strong>Agree the commitment</strong></td><td>Irrevocable, back-to-back. The bank cannot cherry-pick later.</td></tr>
<tr><td>3</td><td><strong>Compute the blended rate</strong></td><td>Weighted average. One number to the borrower.</td></tr>
<tr><td>4</td><td><strong>The KFS</strong></td><td>Each lender's share and rate, plus the blended APR.</td></tr>
<tr><td>5</td><td><strong>Disburse and transfer</strong></td><td>Escrow, and 15 calendar days.</td></tr>
<tr><td>6</td><td><strong>Two books, one borrower</strong></td><td>Separate accounts, one common reference number.</td></tr>
<tr><td>7</td><td><strong>Service it</strong></td><td>One customer interface. Rate changes ripple.</td></tr>
<tr><td>8</td><td><strong>Classify and disclose</strong></td><td>The same borrower cannot be standard at one lender and NPA at the other.</td></tr>
</table>
''' + note("Steps 3 and 8 are the two that break integrations. Blended pricing has to recompute whenever either partner moves its rate, and unified asset classification requires two institutions with different internal norms to agree on one answer about one borrower, every day.")

code_blend = code('Python — step 3, the blended rate, recomputed whenever either side moves', r'''from decimal import Decimal, ROUND_HALF_UP

# ONE rate to the borrower: the weighted average of the partners' rates,
# weighted by their funding share. The hurdle-rate model -- where each lender
# priced separately and the originator kept the difference -- is gone.

def blended_rate(legs) -> Decimal:
    """legs = [{'re':'BANK','share':Decimal('0.80'),'rate':Decimal('9.50')}, ...]"""
    total = sum(l["share"] for l in legs)
    assert total == Decimal("1"), f"shares must sum to 1, got {total}"
    for l in legs:
        # Each partner retains a minimum 10% of EVERY individual loan.
        # 2025 Directions: applies to BOTH sides, not just the NBFC.
        assert l["share"] >= Decimal("0.10"), f"{l['re']} below the 10% floor"
    r = sum(l["share"] * l["rate"] for l in legs)
    return r.quantize(Decimal("0.01"), ROUND_HALF_UP)

def borrower_apr(legs, fees_paise, principal_paise, tenure_months) -> Decimal:
    # Any charge the borrower pays on top of blended interest goes into the APR.
    # A fee that exists anywhere in the journey and is not in the APR makes the
    # APR wrong, and the APR is the binding number.
    return apr_from(principal_paise, fees_paise, blended_rate(legs), tenure_months)

def on_partner_rate_change(loan, re_id, new_rate):
    # A rate move by EITHER partner changes what the borrower pays. Servicing
    # must recompute, reschedule and re-disclose -- this is not a back-office
    # adjustment, it is a change to the customer's contract terms.
    legs = [dict(l, rate=new_rate) if l["re"] == re_id else l for l in loan["legs"]]
    new = blended_rate(legs)
    return {"old_blended": loan["blended_rate"], "new_blended": new,
            "reschedule": new != loan["blended_rate"],
            "fresh_kfs_required": new != loan["blended_rate"],
            "notify_borrower": True}

# WHAT TO CHECK
# [ ] the 10% floor is asserted PER LOAN, not per portfolio. A portfolio at 12%
#     containing individual loans at 4% does not comply
# [ ] shares sum to exactly 1. Use Decimal; a float rounding error here is a
#     mispriced loan
# [ ] blended rate recomputes on ANY partner rate change, and triggers a fresh
#     KFS. Teams build the rate once at origination and never revisit it
# [ ] every borrower charge is in the APR, not just the interest
# [ ] store the LEGS with the loan -- share and rate per partner, at that date.
#     Recomputing from today's rates cannot reproduce a historical instalment
# [ ] the borrower sees ONE rate. Showing two lenders' rates is the model the
#     Directions replaced
''')

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; The partner and the agreement</h3>
<p>Both parties need a <strong>board-approved co-lending policy</strong>, and the arrangement needs a
<strong>formal CLA</strong> covering, at minimum:</p>
<ul>
<li>Terms and the funding split</li>
<li><strong>Borrower selection criteria</strong>, agreed up front rather than applied case by case</li>
<li>Fee structure between the partners</li>
<li>Segregation of responsibilities &mdash; sourcing, underwriting, servicing, collections</li>
<li><strong>Which lender is the customer interface</strong></li>
</ul>

<h3 id="s-indigo-s2">Step 2 &mdash; The commitment that changed the product</h3>
''' + warn("<strong>Under the 2020 model the bank could look at each sourced loan and decline it.</strong> That discretion is <strong>abolished</strong>. The partner now gives an <strong>irrevocable commitment to fund its agreed share on a back-to-back basis</strong>, and selective or post-disbursement acquisition falls under the <strong>Transfer of Loan Exposures Directions</strong> instead &mdash; a different regime entirely. <strong>The consequence is architectural: your credit policy must be agreed BEFORE origination, in the CLA, because there is no second look.</strong> Every co-lending stack built on &ldquo;source, then send to the bank for approval&rdquo; needs rebuilding as &ldquo;apply the agreed policy, then both fund automatically&rdquo;.") + '''

<h3 id="s-indigo-s3">Step 3 &mdash; The blended rate</h3>
''' + code_blend + '''
<p><strong>The gotcha nobody documents:</strong> the blended rate is not a number you compute once.
If either partner changes its rate during the loan's life &mdash; and over a multi-year tenure one of
them will &mdash; the borrower's rate changes, the schedule changes, and a fresh Key Fact Statement is
owed. Most co-lending implementations compute the blend at origination and store it as a constant.
That is a defect that only surfaces at the first repricing, by which time there are thousands of
loans carrying a stale rate.</p>
'''

code_ops = code('Python — steps 5 to 8: escrow, two books, one answer about the borrower', r'''from datetime import timedelta

TRANSFER_WINDOW = timedelta(days=15)      # calendar days, not business days

def disburse(loan, escrow, legs):
    # All transactions between the REs and the borrower route through an escrow
    # maintained for the arrangement. Neither lender's own account touches
    # borrower money directly.
    for l in legs:
        escrow.credit(source=l["re"], amount=l["share"] * loan["principal_paise"],
                      ref=loan["common_ref"])
    escrow.debit(to=loan["borrower_account"], amount=loan["principal_paise"],
                 ref=loan["common_ref"])
    return {"transfer_due_by": loan["origination_date"] + TRANSFER_WINDOW}

def book(loan, legs):
    # SEPARATE loan accounts per co-lender, joined by ONE common reference.
    # The common ref is what makes reconciliation and credit bureau reporting
    # possible; without it you have two unrelated loans to the same person.
    return [{"re": l["re"], "account_no": l["re"] + "-" + loan["common_ref"],
             "common_ref": loan["common_ref"], "share": l["share"],
             "rate": l["rate"], "outstanding": l["share"] * loan["principal_paise"]}
            for l in legs]

def classify(loan, views):
    """views = each partner's own SMA/NPA view of this borrower."""
    # UNIFIED BORROWER-LEVEL CLASSIFICATION. The same borrower cannot be
    # standard at the bank and NPA at the NBFC. The partners' internal norms
    # differ, so the CLA must say HOW the single answer is reached.
    worst = max(views.values(), key=lambda v: v["severity"])
    disagreement = len({v["stage"] for v in views.values()}) > 1
    return {"agreed_stage": worst["stage"],
            "partners_disagreed": disagreement,
            "resolution_rule": loan["cla"]["classification_rule"],
            "action": "escalate_to_cla_committee" if disagreement
                      and not loan["cla"].get("classification_rule") else "apply"}

# WHAT TO CHECK
# [ ] the transfer window is 15 CALENDAR days. A 15-business-day assumption is
#     wrong by up to five days in a month with holidays
# [ ] common_ref is generated ONCE, at origination, and used by both partners in
#     their own systems AND in credit bureau reporting
# [ ] the classification rule is written INTO the CLA, not resolved by email
#     each time. Two institutions with different SMA norms will disagree, and
#     the borrower's bureau record depends on the answer
# [ ] ONE customer interface, named in the loan agreement. If it changes during
#     the tenure the borrower is told IN ADVANCE
# [ ] escrow reconciles daily. Two funders, one disbursal, one repayment stream
#     -- see Build Sheet 05 for the control-total discipline
# [ ] DLG between the partners is capped at 5% and disclosed
''')

i_step48 = '''
<h3 id="s-indigo-s4">Step 4 &mdash; The Key Fact Statement</h3>
<p>The KFS carries more than an ordinary loan's does. It must show <strong>each lender's share and
rate</strong> as well as the single blended figure:</p>
<p style="background:var(--bg2);border:1px solid var(--border);border-radius:8px;padding:12px 14px;font-size:.86rem">
Bank &mdash; 80% @ 9.50% &nbsp;&middot;&nbsp; NBFC &mdash; 20% @ 16.00% &nbsp;&middot;&nbsp;
<strong>Blended &mdash; 10.80%</strong> &nbsp;&middot;&nbsp; APR including all charges &mdash; 11.4%</p>
<p>Everything in <a href="/fintech-ai/products/bnpl-checkout/">Product Guide 03</a> about the KFS
applies here too: it is shown before sanction, the APR includes every fee, and
<strong>you store the rendered document rather than the inputs</strong>.</p>

<h3 id="s-indigo-s5">Steps 5 to 8 &mdash; Escrow, books, servicing, classification</h3>
''' + code_ops + '''
<p><strong>The gotcha nobody documents:</strong> unified asset classification. Two institutions with
different internal SMA and NPA norms must produce <strong>one answer about one borrower</strong>,
every day, and that answer drives the borrower's credit bureau record. The Directions require the
unified view but do not resolve the methodological difference for you. <strong>If your CLA does not
state exactly how disagreement is settled, you will be settling it by email while a borrower's bureau
file is wrong.</strong> Write the rule into the agreement, implement it as code, and log every time
the partners disagreed &mdash; that log is the evidence the rule is being applied consistently.</p>

<h3 id="s-indigo-s8">Disclosure</h3>
<ul>
<li><strong>NBFCs must list their co-lending partners publicly on their website.</strong></li>
<li>Financial statements must disclose <strong>volumes, rates, fees, performance and
guarantees</strong> for co-lending arrangements.</li>
<li>Any <strong>DLG between the partners is capped at 5%</strong> and disclosed.</li>
</ul>
'''

i_cost = registry("Co-lending &mdash; what it costs and what it earns", [
 ("The retention", "direct",
  "<strong>10% of every individual loan, on both sides.</strong> That is capital tied up per loan, "
  "not per portfolio, and it is the real cost of participating."),
 ("The margin you can no longer take", "direct",
  "<strong>The blended rate removes the hurdle-rate spread.</strong> If the business case depended on "
  "pricing the borrower above your own cost while funding at the bank's, that margin is gone by "
  "design."),
 ("The DLG", "direct",
  "Capped at <strong>5%</strong>, and it is real capital posted, not a marketing term. See "
  "<a href=\"/fintech-ai/products/bnpl-checkout/\">Product Guide 03</a> for the eligible forms."),
 ("Two-system integration", "direct",
  "Separate loan accounts in two institutions joined by one reference, daily escrow reconciliation, "
  "and a blended rate that recomputes on either side's move. <strong>Budget this as an integration "
  "project, not a feature.</strong>"),
 ("The 15-day clock", "direct",
  "Operational cost of hitting a <strong>calendar-day</strong> transfer window every time, including "
  "across holidays."),
 ("What you earn", "direct",
  "Reach and volume the NBFC could not fund alone, and assets the bank could not originate alone. "
  "<strong>The economics now come from volume and cost of funds, not from pricing opacity</strong> "
  "&mdash; which is a harder but more durable business."),
], "September 2026") + note("<strong>Model the arrangement, not the loan.</strong> A co-lending book's economics depend on the funding split, both partners' costs of funds, the retention on both sides, and the DLG posted. Change any one and the whole arrangement reprices. Build that as a model you can run before you sign the CLA, because the CLA is hard to renegotiate afterwards.")

a_builds = '''
<h3 id="s-amber-week">The starting version</h3>
<p><strong>Build:</strong> one bank partner &rarr; a CLA with the credit policy agreed up front
&rarr; blended rate computed and stored with the legs &rarr; KFS showing both shares &rarr; escrow
disbursal &rarr; separate books with a common reference &rarr; manual classification reconciliation.</p>
<p><strong>It breaks when:</strong> either partner reprices, or the partners disagree on a borrower's
stage.</p>

<h3 id="s-amber-proper">The proper version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; blended rate as a <em>function</em> that
recomputes on any leg change and triggers a fresh KFS &rarr; the classification rule written into the
CLA and implemented in code, with a disagreement log &rarr; daily escrow reconciliation with control
totals &rarr; the 10% floor asserted per loan &rarr; common reference flowing into both bureau
submissions &rarr; the public partner list and statutory disclosures automated.</p>
<p><strong>Trade:</strong> you are operating inside another institution's release cycle. Their rate
change is your reschedule.</p>

<h3 id="s-amber-big">Multiple partners</h3>
<p><strong>Build:</strong> several bank partners, routed by product and geography, with an
arrangement-level economic model per partner.</p>
<p><strong>It breaks when:</strong> you build it before one arrangement has run through a full cycle
&mdash; an origination, a repricing, a delinquency and a recovery. Until then you do not know what
you are scaling.</p>
''' + note("If you take one thing from this page: <strong>the credit policy must be settled in the CLA, before origination.</strong> The bank's second look is gone. Every stack designed around &ldquo;source, then get approval&rdquo; has to become &ldquo;apply the agreed policy, then both fund automatically&rdquo; &mdash; and that is a rebuild, not a configuration change.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>The bank tries to decline a sourced loan</strong></td><td>Designed against the 2020 discretionary model.</td><td>Irrevocable back-to-back commitment. Agree policy in the CLA.</td></tr>
<tr><td><strong>Blended rate goes stale</strong></td><td>Computed once at origination and stored as a constant.</td><td>A function over the legs, recomputed on any change.</td></tr>
<tr><td><strong>Retention below 10% on some loans</strong></td><td>The floor was applied at portfolio level.</td><td>Assert per individual loan.</td></tr>
<tr><td><strong>Partners disagree on NPA stage</strong></td><td>Different internal norms, no rule in the CLA.</td><td>Write the resolution rule into the agreement; log disagreements.</td></tr>
<tr><td><strong>Two unrelated loans in the bureau</strong></td><td>No common reference number.</td><td>One ref, generated at origination, used by both.</td></tr>
<tr><td><strong>Transfer misses the window</strong></td><td>15 business days assumed.</td><td>Calendar days.</td></tr>
<tr><td><strong>Borrower sees two rates</strong></td><td>The old model surfaced in the UI.</td><td>One blended rate; shares disclosed in the KFS only.</td></tr>
<tr><td><strong>The business case evaporates</strong></td><td>It rested on the hurdle-rate spread.</td><td>It is gone by design. Rebuild on volume and cost of funds.</td></tr>
</table>
'''

SRC=[('official','RBI (Co-Lending Arrangements) Directions, 2025','issued 6 August 2025 (RBI/DOR/2025-26/139 · DOR.STR.REC.44/13.07.010/2025-26), effective 1 January 2026. The 10% retention on both sides, the irrevocable back-to-back commitment, the blended rate, the 15-calendar-day transfer, escrow routing, unified borrower-level classification, the 5% DLG cap and the disclosure obligations.','https://www.rbi.org.in'),
 ('official','RBI Co-Lending by Banks and NBFCs to Priority Sector (5 November 2020)','the repealed framework — retained here only to show what changed.','https://www.rbi.org.in'),
 ('official','RBI (Transfer of Loan Exposures) Directions','the regime that now governs selective or post-disbursement loan acquisition, which co-lending no longer permits.','https://www.rbi.org.in'),
 ('official','RBI (Digital Lending) Directions, 2025','applies in addition to the Co-Lending Directions where the arrangement is digital.','https://www.rbi.org.in'),
 ('industry','Legal and practitioner analysis of the 2025 Directions','the comparison table against the 2020 model, and the observation that the blended rate removes the hurdle-rate margin. Verify any specific figure against the Directions before relying on it.',''),
 ('industry','Core lending platform implementation notes','the KFS share-disclosure format, common loan reference numbering, and dynamic rate recalculation. Vendor-sourced.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'+(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. These Directions took effect on 1 January 2026; anything older describes a repealed framework.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/credit-underwriting/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 02</div><h3>Credit &amp; Underwriting</h3><p>The credit policy that must now be agreed in the CLA before a single loan is sourced.</p></a>
<a href="/fintech-ai/products/bnpl-checkout/" class="mod-card"><div class="mod-num">GUIDE 03</div><h3>BNPL Checkout</h3><p>The KFS discipline and the DLG rules, both of which apply here.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Escrow control totals, two funders and one repayment stream.</p></a>
<a href="/fintech-ai/governance/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 09</div><h3>Governance</h3><p>The classification rule is a model decision with a board behind it.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Co-lending is a regulated arrangement between licensed entities and the CLA is a binding contract that is difficult to renegotiate. Nothing here is legal advice. Have your agreement, your pricing model and your classification rule reviewed by qualified counsel before the first loan is sourced.")

lanes={'green':[("How to use this page",g_read),("What co-lending actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 to 3 — partner, commitment, pricing",i_step12),
           ("Steps 4 to 8 — the KFS, the money, the books",i_step48),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Co-Lending: How to Build It"
META=("Build a co-lending product step by step: the eight stages, the 2025 Directions, how to connect "
      "them, and what the blended rate changes.")
LEAD=("A step-by-step guide to building a co-lending arrangement in India. Eight stages, the options "
      "at each one, exactly how each step connects to the next, real costs, and what breaks. Written "
      "for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/co-lending",title=TITLE,meta=META,lead=LEAD,label="Product Guide 07",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/co-lending/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
# SOP F4: skip link + target, at creation
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h)
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h)
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)
