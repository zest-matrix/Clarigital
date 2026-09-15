#!/usr/bin/env python3
# Session 75 — PRODUCT GUIDE 06: Cross-border payments
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one capability: moving money across India's border, legally,
for goods or services. Receiving from overseas customers, paying overseas suppliers, or both.</p>
<p>It is the capability behind every Indian SaaS company, exporter, freelancer platform and
marketplace that touches a foreign currency.</p>
''' + warn("<strong>The framework changed completely and the old one is still widely described as current.</strong> The <strong>OPGSP</strong> regime &mdash; imports capped at <strong>$2,000</strong>, exports at <strong>$10,000</strong> per transaction, and <strong>services excluded entirely</strong> &mdash; was withdrawn by the RBI circular of <strong>31 October 2023</strong>. It was replaced by <strong>PA-CB</strong>, then consolidated into the <strong>Master Direction on Regulation of Payment Aggregators of 15 September 2025</strong>. Anything describing OPGSP limits as live is describing a regime that no longer exists.")

g_what = '''
<p>Cross-border payments in India sit on three legal layers at once, and you cannot ignore any of
them:</p>
<table>
<tr><th>Layer</th><th>What it governs</th></tr>
<tr><td><strong>FEMA, 1999</strong></td><td>Whether the money may cross the border at all, and for what purpose.</td></tr>
<tr><td><strong>RBI payment regulation</strong></td><td>Who is allowed to move it &mdash; AD banks, and now authorised PA-CBs.</td></tr>
<tr><td><strong>PMLA / FIU-IND</strong></td><td>Reporting obligations. A Delhi High Court ruling in July 2023 confirmed these operators are reporting entities.</td></tr>
</table>
<p><strong>The three PA-CB categories, by direction of flow:</strong></p>
<table>
<tr><th>Category</th><th>Direction</th><th>Who needs it</th></tr>
<tr><td><strong>Export</strong></td><td>Money coming <em>in</em> from overseas buyers</td><td>SaaS, IT services, freelancers, exporters.</td></tr>
<tr><td><strong>Import</strong></td><td>Money going <em>out</em> to overseas sellers</td><td>Businesses buying foreign goods, software or services.</td></tr>
<tr><td><strong>Both</strong></td><td>Two-way</td><td>Marketplaces, and anyone who both earns and spends abroad.</td></tr>
</table>
''' + note("<strong>Match the category to your flow before you sign anything.</strong> A provider authorised for export-only cannot process your outbound supplier payments, and you will find that out at the moment you need to pay someone. If you do both, you need a provider covering both &mdash; or two providers.") + '''
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not a wire transfer with an API.</strong> The documentation obligations are the product.</li>
<li><strong>Not unlimited.</strong> See step 5.</li>
<li><strong>Not something you can route around.</strong> Using unauthorised channels is a FEMA
violation, with penalties running to criminal prosecution for wilful breaches.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Which direction?</strong></td><td>In, out, or both. It decides everything after.</td></tr>
<tr><td>2</td><td><strong>Pick your route</strong></td><td>AD bank, a PA-CB provider, or become one.</td></tr>
<tr><td>3</td><td><strong>Verify the authorisation</strong></td><td>Final, not in-principle. And the right category.</td></tr>
<tr><td>4</td><td><strong>Onboard the merchant</strong></td><td>KYC, plus the FEMA purpose of the money.</td></tr>
<tr><td>5</td><td><strong>Move it &mdash; inside the cap</strong></td><td>&#8377;25 lakh per unit, and the word &ldquo;unit&rdquo; is doing work.</td></tr>
<tr><td>6</td><td><strong>Document it</strong></td><td>Purpose code, FIRA, EDPMS or IDPMS. This is what makes it legal, not just successful.</td></tr>
<tr><td>7</td><td><strong>The FX</strong></td><td>Where the real cost lives, and where it is hidden.</td></tr>
<tr><td>8</td><td><strong>Reconcile and report</strong></td><td>Including the FIU-IND obligation that surprises people.</td></tr>
</table>
''' + note("Step 6 is the one that separates a working integration from a compliant one. A payment can settle perfectly and still leave you with an open entry in a monitoring system that someone has to close, months later, without the paperwork.")

code_cap = code('Python — step 5, the cap, and the word doing all the work', r'''from decimal import Decimal

# Per-unit cap on goods and services processed through a PA-CB.
PER_UNIT_CAP = Decimal("2500000")      # Rs 25 lakh
EDD_THRESHOLD = Decimal("250000")      # Rs 2.5 lakh -> enhanced due diligence

# NOTE THE WORD. The OPGSP limit it replaced was PER TRANSACTION. This one is
# PER UNIT of goods or services, and how a "unit" is measured is genuinely
# ambiguous -- the RBI has not defined it precisely and practitioners have been
# asking since the 2023 circular.
#
# Practical consequence: a Rs 35 lakh consulting engagement is NOT solved by
# splitting it into two payments. If it is one unit of service, it is one unit.
# Structuring invoices to duck the cap is the thing that looks like structuring.

def check_transaction(txn) -> dict:
    flags = []
    if txn["value_inr"] > PER_UNIT_CAP:
        flags.append({
            "block": True, "why": "exceeds_per_unit_cap",
            "action": "route via an AD bank directly, not by splitting the invoice",
        })
    if txn["value_inr"] > EDD_THRESHOLD:
        flags.append({"block": False, "why": "enhanced_due_diligence_required",
                      "action": "EDD on the counterparty before processing"})
    if not txn.get("purpose_code"):
        flags.append({"block": True, "why": "no_purpose_code",
                      "action": "a payment without a FEMA purpose is not a payment you can make"})
    if txn["direction"] not in txn["provider_categories"]:
        flags.append({"block": True, "why": "provider_not_authorised_for_direction",
                      "action": "export-only cannot process imports"})
    return {"allow": not any(f["block"] for f in flags), "flags": flags}

# WHAT TO CHECK
# [ ] above the cap, the answer is a DIFFERENT ROUTE, not a smaller invoice.
#     An AD bank can handle what a PA-CB cannot. Splitting to fit is the
#     pattern every AML system is built to notice
# [ ] "unit" is ambiguous. Write down YOUR interpretation, get it agreed with
#     your provider and your bank IN WRITING, and apply it consistently. An
#     inconsistent interpretation is worse than a conservative one
# [ ] EDD above Rs 2.5 lakh is on the COUNTERPARTY, and it takes time. Build it
#     into the flow, not as a blocking surprise at payment
# [ ] the purpose code is chosen from the RBI list at the point of the payment,
#     not guessed later by finance from the narration
# [ ] provider category is checked in code against the direction. It is a
#     one-line check and it prevents a whole class of failed payment
''')

i_step123 = '''
<h3 id="s-indigo-s1">Steps 1 and 2 &mdash; Direction, then route</h3>
<table>
<tr><th>Route</th><th>What it means</th><th>When it fits</th></tr>
<tr><td><strong>AD Category-I bank directly</strong></td><td>Your bank handles the remittance and the documentation.</td><td>Low volume, large tickets, or anything above the PA-CB cap.</td></tr>
<tr><td><strong>An authorised PA-CB</strong></td><td>A provider handles collection, conversion and paperwork.</td><td>Most businesses. Better rates, better developer experience, and the documentation largely handled.</td></tr>
<tr><td><strong>Become a PA-CB</strong></td><td><strong>&#8377;15 crore net worth at application, rising to &#8377;25 crore</strong>, plus authorisation, FIU-IND registration and FEMA obligations.</td><td>Cross-border payments <em>are</em> your product.</td></tr>
</table>

<h3 id="s-indigo-s3">Step 3 &mdash; Verify the authorisation</h3>
''' + warn("<strong>The procurement trap: &ldquo;in-principle approval&rdquo; is not authorisation.</strong> Several well-known names have held in-principle PA-CB approval for extended periods while their final authorisation remained pending. In-principle means the RBI is minded to approve, subject to conditions. It does not mean the entity may yet process your cross-border payments. <strong>Ask two questions and get written answers: is the authorisation final, and which category does it cover?</strong> &ldquo;We are RBI regulated&rdquo; answers neither.") + '''
<p>The same check applies to the accounts underneath. A PA-CB maintains separate collection accounts
with an AD Category-I bank &mdash; <strong>one for imports, one for exports</strong> &mdash; and they
must not be commingled, with each other or with the provider's own money. That separation is what
keeps your export documentation intact, so your purpose codes and reconciliation continue to work.
It is worth asking a provider to describe their account structure; a vague answer is informative.</p>
'''

code_docs = code('Python — step 6, the documentation that makes it legal', r'''# A payment that settles is not the same as a payment that is compliant. The
# money arriving is the easy part; closing the regulatory entry is the work.

PURPOSE_CODES = {          # illustrative -- use the current RBI list
    "P0802": "software consultancy / implementation",
    "P0807": "business and management consultancy",
    "P1006": "advertising and market research",
    "P0103": "export of goods",
}

def remittance_record(txn, merchant):
    rec = {
        "direction": txn["direction"],               # INWARD | OUTWARD
        "purpose_code": txn["purpose_code"],          # chosen at payment time
        "amount_fcy": txn["amount_fcy"],
        "currency": txn["currency"],
        "amount_inr": txn["amount_inr"],
        "fx_rate_applied": txn["fx_rate"],
        "value_date": txn["value_date"],
        "counterparty": txn["counterparty"],
        "invoice_ref": txn["invoice_ref"],
        "contract_ref": txn.get("contract_ref"),
    }
    if txn["direction"] == "INWARD":
        # Export of services or goods. The AD bank reports into EDPMS, and the
        # entry stays OPEN until it is matched and closed. An unclosed entry is
        # a compliance item with your name on it, months later.
        rec["fira_required"] = True                  # Foreign Inward Remittance Advice
        rec["edpms_entry"] = "expected"
        rec["close_by"] = txn["value_date"] + realisation_window(merchant)
    else:
        # Import. Reported into IDPMS, and the entry closes against evidence
        # that you actually received what you paid for.
        rec["idpms_entry"] = "expected"
        rec["evidence_required"] = ["bill_of_entry" if txn["is_goods"]
                                    else "service_completion_evidence"]
    return rec

# WHAT TO CHECK
# [ ] FIRA is requested and STORED per inward remittance. It is the evidence
#     the money is export proceeds and not something else, and clients,
#     auditors and the tax authority all ask for it eventually
# [ ] EDPMS / IDPMS entries are TRACKED TO CLOSURE, not assumed closed. An open
#     entry is the single most common cross-border compliance debt, and it
#     surfaces as a bank refusing your next transaction
# [ ] the purpose code is picked at payment time from the current RBI list.
#     Reverse-engineering it from a bank narration months later is guesswork
# [ ] store the FX RATE APPLIED, not just the INR amount. Without it you cannot
#     audit the spread in step 7
# [ ] invoice and contract references are captured with the payment, because
#     closing an EDPMS entry needs the documents, not the payment record
# [ ] outward payments need evidence you received the thing. A bill of entry
#     for goods; something defensible for services
''')

i_step456 = '''
<h3 id="s-indigo-s4">Step 4 &mdash; Onboard the merchant</h3>
<p>Standard KYC under the Master Direction, plus one thing domestic onboarding does not have:
<strong>the FEMA purpose</strong>. You are not just establishing who they are, you are establishing
what the money is <em>for</em>, because that determines whether it may cross the border at all.</p>
<p>Ongoing due diligence applies, and enhanced due diligence kicks in above
<strong>&#8377;2.5 lakh per unit</strong>. That is low enough that for most B2B exporters it is the
normal case rather than the exception &mdash; build it into the flow rather than treating it as an
escalation.</p>

<h3 id="s-indigo-s5">Step 5 &mdash; Move it, inside the cap</h3>
''' + code_cap + '''
<p><strong>The gotcha nobody documents:</strong> the cap is <strong>per unit</strong>, not per
transaction &mdash; a deliberate change from the OPGSP regime it replaced, and the RBI has not
defined precisely what a &ldquo;unit&rdquo; is. For a physical good it is intuitive. For a
&#8377;35 lakh consulting engagement it is not, and <strong>splitting the invoice is exactly the
behaviour an AML system is designed to flag</strong>. The correct answer above the cap is a different
route &mdash; an AD bank &mdash; not a smaller invoice. Write down your interpretation of
&ldquo;unit&rdquo;, agree it with your provider and your bank in writing, and apply it the same way
every time.</p>

<h3 id="s-indigo-s6">Step 6 &mdash; Document it</h3>
''' + code_docs + '''
<p><strong>The gotcha nobody documents:</strong> <strong>EDPMS and IDPMS entries stay open until
somebody closes them.</strong> The payment succeeds, the money is in the account, everyone moves on
&mdash; and an entry sits in a monitoring system waiting for documentation. It surfaces months later
as a bank declining your next transaction until the backlog is cleared. <strong>Track entries to
closure as a first-class part of the product</strong>, not as something finance will sort out at year
end, because by then the invoices are hard to find and the people who raised them have moved on.</p>
'''

i_step78 = '''
<h3 id="s-indigo-s7">Step 7 &mdash; The FX</h3>
<p><strong>This is where the money goes, and it is almost never on the pricing page.</strong></p>
<p>A provider quoting &ldquo;1% fee&rdquo; may be applying an exchange rate two or three percent away
from the interbank rate. The fee is visible and the spread is not, and the spread is usually the
larger number. <a href="/fintech-ai/payments-reconciliation/build-sheet/">Build Sheet 05</a> records
that all-in cross-border costs are frequently reported in the <strong>5&ndash;7%</strong> range
against a <strong>3%</strong> headline, and the difference is almost entirely FX.</p>
<table>
<tr><th>Ask this</th><th>Why</th></tr>
<tr><td><strong>&ldquo;What is your markup over the interbank mid-rate?&rdquo;</strong></td><td>The only question that gets a comparable number. &ldquo;Competitive rates&rdquo; is not an answer.</td></tr>
<tr><td><strong>&ldquo;Show me the rate you applied on my last ten transactions, against the mid at that timestamp.&rdquo;</strong></td><td>Turns a claim into arithmetic. Store the applied rate per transaction and you can compute this yourself.</td></tr>
<tr><td><strong>&ldquo;Who else takes a cut before it lands?&rdquo;</strong></td><td>Correspondent bank charges, beneficiary bank charges, and lifting fees are real and often undisclosed.</td></tr>
</table>
''' + warn("<strong>Store the FX rate applied, per transaction, from day one.</strong> Without it you cannot audit your provider, cannot compare two providers honestly, and cannot answer a merchant asking why they received less than they expected. It is one column, and adding it later means the historical comparison you actually want is impossible.") + '''

<h3 id="s-indigo-s8">Step 8 &mdash; Reconcile and report</h3>
<p>Three obligations that arrive together and are usually owned by nobody:</p>
<ul>
<li><strong>Reconciliation.</strong> Foreign currency in, INR out, at a rate, on a date, with fees
deducted somewhere. See <a href="/fintech-ai/payments-reconciliation/build-sheet/">Build Sheet 05</a>
&mdash; the control-total discipline applies identically, with an FX leg added.</li>
<li><strong>EDPMS / IDPMS closure</strong>, tracked as a queue with an owner and an age.</li>
<li><strong>FIU-IND.</strong> Cross-border payment operators are reporting entities under the PMLA.
Registration and reporting obligations follow, and
<a href="/fintech-ai/aml-compliance/build-sheet/">Build Sheet 04</a> covers the mechanics.</li>
</ul>
'''

i_cost = registry("Cross-border payments &mdash; what it costs", [
 ("Headline provider fee", "direct",
  "Commonly quoted around <strong>1&ndash;3%</strong>. <strong>This is the visible part and usually "
  "the smaller one.</strong>"),
 ("FX spread", "direct",
  "<strong>Where the money actually goes.</strong> Markup over the interbank mid-rate, rarely "
  "disclosed as a number. All-in cross-border cost is frequently reported at "
  "<strong>5&ndash;7%</strong> against a 3% headline."),
 ("Correspondent and beneficiary bank charges", "direct",
  "Deducted in transit by banks you never chose. Ask who takes a cut before the money lands &mdash; "
  "the answer is often more than one party."),
 ("Becoming a PA-CB", "direct",
  "<strong>&#8377;15 crore net worth at application, rising to &#8377;25 crore.</strong> Plus "
  "authorisation, FIU-IND registration, separate import and export collection accounts with an "
  "AD Category-I bank, and FEMA reporting. A licensed business, not a feature."),
 ("Enhanced due diligence", "direct",
  "Required above <strong>&#8377;2.5 lakh per unit</strong> &mdash; low enough that for most B2B "
  "exporters it is the normal case. Analyst time, not licence cost."),
 ("EDPMS / IDPMS closure", "direct",
  "<strong>The cost nobody budgets.</strong> Someone must chase documents and close entries. Left "
  "alone it accumulates until a bank stops processing your transactions, and then it is urgent."),
], "September 2026") + note("<strong>Compute your effective all-in rate yourself, per transaction:</strong> <em>(amount the counterparty sent &minus; amount that reached the account) &divide; amount sent</em>. Compare it to the interbank mid at that timestamp. That single number makes every provider comparable and it is the one nobody will quote you.")

a_builds = '''
<h3 id="s-amber-week">The starting version</h3>
<p><strong>Build:</strong> one authorised PA-CB provider matching your direction &rarr; purpose code
captured at payment time &rarr; FIRA requested and stored per inward remittance &rarr; FX rate stored
per transaction &rarr; a spreadsheet tracking EDPMS entries to closure.</p>
<p><strong>It breaks when:</strong> a transaction exceeds the per-unit cap, or you start paying
outward and your provider is export-only.</p>

<h3 id="s-amber-proper">The proper version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; an AD bank relationship for above-cap
transactions &rarr; provider category checked in code against direction &rarr; EDD built into the
flow above &#8377;2.5 lakh &rarr; a written, agreed interpretation of &ldquo;unit&rdquo; &rarr; an
EDPMS/IDPMS closure queue with an owner and an age report &rarr; effective all-in rate computed per
transaction and reviewed monthly.</p>
<p><strong>Trade:</strong> the documentation machinery is real work that produces nothing visible
until the day it is needed, and then it is the only thing that matters.</p>

<h3 id="s-amber-big">Becoming the PA-CB</h3>
<p><strong>Build:</strong> authorisation, &#8377;25 crore net worth, separate collection accounts,
FEMA and FIU-IND reporting, merchant due diligence at scale.</p>
<p><strong>Use when:</strong> cross-border payments are the product. Not to save on FX.</p>
''' + note("If you take one thing from this page: <strong>store the FX rate applied on every single transaction, starting with the first one.</strong> It is one column. Without it you cannot audit your provider, compare alternatives honestly, or explain a shortfall to a merchant &mdash; and it cannot be reconstructed later.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Provider cannot process your payment</strong></td><td>Export-only authorisation, outbound payment.</td><td>Check category against direction, in code.</td></tr>
<tr><td><strong>&ldquo;RBI regulated&rdquo; turns out to be in-principle</strong></td><td>Nobody asked whether authorisation was final.</td><td>Two written questions: final, and which category.</td></tr>
<tr><td><strong>An invoice is split to fit the cap</strong></td><td>It seemed like the obvious workaround.</td><td>Route above-cap transactions through an AD bank.</td></tr>
<tr><td><strong>The bank stops processing</strong></td><td>A backlog of open EDPMS entries.</td><td>Track closure as a queue from the first transaction.</td></tr>
<tr><td><strong>The merchant received less than expected</strong></td><td>Spread plus correspondent charges, neither visible.</td><td>Store the applied rate; compute all-in cost per transaction.</td></tr>
<tr><td><strong>Purpose code guessed at year end</strong></td><td>Not captured at payment time.</td><td>Pick it from the current RBI list, at payment.</td></tr>
<tr><td><strong>No FIRA when a client asks</strong></td><td>Never requested.</td><td>Request and store per inward remittance.</td></tr>
<tr><td><strong>EDD blocks a payment unexpectedly</strong></td><td>Treated as an escalation, not a step.</td><td>Above &#8377;2.5 lakh it is the normal path.</td></tr>
</table>
'''

SRC=[('official','RBI Master Direction on Regulation of Payment Aggregators (15 September 2025)','the consolidated framework including PA-CB: the three categories, net worth, the separate import and export collection accounts with AD Category-I banks, and the prohibition on commingling.','https://www.rbi.org.in'),
 ('official','RBI circular on Regulation of PA-CBs (31 October 2023)','the creation of the PA-CB framework, the withdrawal of OPGSP, the ₹25 lakh per-unit cap and the ₹2.5 lakh enhanced due diligence threshold.','https://www.rbi.org.in'),
 ('official','Foreign Exchange Management Act, 1999 and RBI purpose codes','whether money may cross the border and under which purpose, plus the EDPMS and IDPMS monitoring systems.','https://www.rbi.org.in'),
 ('official','FIU-IND','the reporting-entity obligation that attaches to cross-border payment operators under the PMLA.','https://fiuindia.gov.in'),
 ('industry','PA-CB practitioner commentary','the OPGSP limits it replaced ($2,000 imports, $10,000 exports, services excluded), the ambiguity in the word "unit", and the in-principle-versus-final authorisation distinction. Practitioner-sourced; verify current authorisation status directly with the provider.',''),
 ('industry','Cross-border cost reporting','the 5–7% all-in figure against a ~3% headline, and the composition of correspondent and beneficiary charges. Compute your own effective rate rather than relying on any published range.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'+(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. Authorisation status changes; verify with the provider before routing money.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Control totals, the FX leg, and the PA Directions that govern the accounts underneath.</p></a>
<a href="/fintech-ai/aml-compliance/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 04</div><h3>AML &amp; Compliance</h3><p>FIU-IND registration and reporting, and why splitting an invoice looks like structuring.</p></a>
<a href="/fintech-ai/products/recurring-payments/" class="mod-card"><div class="mod-num">GUIDE 05</div><h3>Recurring Payments</h3><p>The 2026 e-mandate framework covers cross-border recurring transactions too.</p></a>
<a href="/fintech-ai/regulation-india/" class="mod-card"><div class="mod-num">REFERENCE</div><h3>India regulation</h3><p>FEMA, the PA Directions and the PMLA obligations in one place.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Cross-border payments are governed by FEMA, and using an unauthorised channel is a statutory violation rather than a commercial mistake. Nothing here is legal advice. Have your route, your purpose-code mapping and your documentation process reviewed by qualified counsel and your AD bank before the first transaction.")

lanes={'green':[("How to use this page",g_read),("What cross-border payments actually are",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 to 3 — direction, route and authorisation",i_step123),
           ("Steps 4 to 6 — onboarding, the cap and the paperwork",i_step456),
           ("Steps 7 and 8 — FX, reconciliation and reporting",i_step78),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Cross-Border Payments: How to Build It"
META=("Build cross-border payments step by step: the eight stages, the PA-CB rules, how to connect "
      "them, and where the FX cost actually hides.")
LEAD=("A step-by-step guide to building cross-border payments from India. Eight stages, the options at "
      "each one, exactly how each step connects to the next, real costs, and what breaks. Written for "
      "someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/cross-border-payments",title=TITLE,meta=META,lead=LEAD,label="Product Guide 06",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/cross-border-payments/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: _io.open(f,'w',encoding='utf-8').write(h.replace('</style>',CSSRC+'\n</style>',1))
