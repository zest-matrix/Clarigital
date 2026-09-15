#!/usr/bin/env python3
# Session 86 — PRODUCT GUIDE 13: SME treasury. FINAL product guide.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product: software that tells a small business how much
money it has, how much is coming, how much is going out, and what to do about the gap. Multiple bank
accounts, unpaid invoices, a payroll date, and a surplus sitting in a current account earning
nothing.</p>
<p><strong>This is the thirteenth and last product guide, and it is the one where the other twelve
meet.</strong> Almost every boundary described across this section runs through a treasury product,
which is why it is a harder build than it looks and why it is last.</p>
''' + note("<strong>It is also the least regulated product in this set, and that is the trap rather than the relief.</strong> There is no treasury licence. There is nothing to apply for. What there is instead is <strong>four lines you must not cross</strong>, each of which is crossed by a feature a customer will ask you for and an engineer can build in a sprint. <strong>The fastest way to become regulated in this product is to be helpful.</strong>")

g_what = '''
<p>SME treasury is <strong>visibility, timing and control</strong> over money a business already has
and already owes. You are not a bank, not a lender, not a broker and not a payment company &mdash;
and the product is largely defined by staying that way.</p>
<p><strong>The four lines, and the feature request that crosses each one:</strong></p>
<table>
<tr><th>They ask for</th><th>You become</th><th>Instead</th></tr>
<tr><td>&ldquo;Hold our money so payouts are instant&rdquo;</td><td>A <strong>payment aggregator</strong>. Escrow with a scheduled commercial bank, net worth &#8377;15 crore rising to &#8377;25 crore, day-end balance equal to the amount realised</td><td><strong>Never touch the money.</strong> Initiate from their account, on their mandate</td></tr>
<tr><td>&ldquo;Tell us where to park the surplus&rdquo;</td><td>An <strong>investment adviser</strong>. Registration, a capped fee, and you may not execute</td><td>Show <strong>their own bank&rsquo;s</strong> options and the arithmetic. Recommend nothing</td></tr>
<tr><td>&ldquo;Front us the cash until the invoice clears&rdquo;</td><td>A <strong>lender</strong>. NBFC registration, the Digital Lending Directions, a KFS</td><td>Route to a regulated lender, or to <strong>TReDS</strong></td></tr>
<tr><td>&ldquo;Convert this to dollars for us&rdquo;</td><td>Inside <strong>FEMA</strong>, needing an authorised dealer</td><td>Their AD bank does the conversion. You do the <strong>tracking</strong></td></tr>
</table>
''' + warn("<strong>None of those four looks like a licensing decision at the moment it is made.</strong> Each arrives as a support ticket from a customer you like, gets scoped as a fortnight of work, and is shipped by someone who has never read a Master Direction. <strong>Put the four assertions in code on day one</strong> &mdash; a boundary you can only enforce by remembering it is not a boundary.") + '''
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not an accounting package.</strong> Accounting is what happened; treasury is what is about
to happen and what you will do about it.</li>
<li><strong>Not an ERP module.</strong> The value is <em>across</em> banks and counterparties, which is
exactly what a single-system module cannot see.</li>
<li><strong>Not a forecast.</strong> A forecast is one output. The product is the decision it
supports.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Decide what you are not</strong></td><td>The four lines, asserted in code.</td></tr>
<tr><td>2</td><td><strong>See the cash</strong></td><td>Every account, one position, one currency base.</td></tr>
<tr><td>3</td><td><strong>Receivables</strong></td><td><strong>And the IRN that makes one real.</strong></td></tr>
<tr><td>4</td><td><strong>Payables</strong></td><td>Approvals, limits, and who may release money.</td></tr>
<tr><td>5</td><td><strong>Forecast</strong></td><td>A range with a confidence, not a number.</td></tr>
<tr><td>6</td><td><strong>The surplus</strong></td><td>Show the arithmetic. Recommend nothing.</td></tr>
<tr><td>7</td><td><strong>Currency</strong></td><td>If they trade abroad, there is a queue waiting for them.</td></tr>
<tr><td>8</td><td><strong>Close the loop</strong></td><td>Reconciliation, and an audit trail of decisions.</td></tr>
</table>
''' + note("<strong>Steps 1, 3 and 8 are the skipped ones</strong>, and they are unusual company: a licensing question, a tax-compliance dependency and a reconciliation job. None of the three is what a treasury product demo is about, and all three are what makes one trustworthy.")

code_boundary = code('Python — steps 1 and 2, the four assertions and one honest cash position', r'''from datetime import date, timedelta
from decimal import Decimal

# STEP 1. THE FOUR LINES, AS CODE RATHER THAN AS A POLICY DOCUMENT.
# Each of these is a single feature away from a licence you do not hold.

def assert_boundaries(action, ctx):
    # 1. Money never rests with you. Not for an hour, not "in transit".
    assert action["settlement_account_owner"] == "customer", \
        "holding customer funds makes you a payment aggregator"
    # 2. You may show options and arithmetic. You may not rank, default-sort,
    #    badge, or personalise them. See the robo-advisory guide.
    assert not action.get("recommends_instrument"), \
        "ranking an investment for a specific customer is investment advice"
    # 3. Bridging a gap with your own balance sheet is lending.
    assert action["funding_source"] != "platform_balance_sheet", \
        "advancing funds is lending"
    # 4. Conversion belongs to an authorised dealer bank.
    assert action.get("fx_conversion_by") in (None, "customer_ad_bank"), \
        "converting currency requires an AD bank"
    return True

# STEP 2. ONE POSITION, ACROSS BANKS.
# The whole reason this product exists: a business with four accounts at three
# banks has four balances and no position.

def position(accounts, as_of=None):
    as_of = as_of or date.today()
    total = Decimal(0); stale = []
    for a in accounts:
        # A balance is only as good as its timestamp. Say so on the screen.
        age_h = (as_of - a["balance_as_of"]).days * 24
        if age_h > 24:
            stale.append({"account": a["id"], "age_hours": age_h})
        total += Decimal(a["balance_paise"])
    return {
        "as_of_ist": as_of.isoformat(),
        "total_paise": total,
        "by_account": [{"id": a["id"], "bank": a["bank"],
                        "balance_paise": a["balance_paise"],
                        "as_of": a["balance_as_of"].isoformat()} for a in accounts],
        # Never present a stale figure as current. An SME will make a payroll
        # decision on this number.
        "stale_accounts": stale,
        "confidence": "LOW" if stale else "OK",
    }

# WHAT TO CHECK
# [ ] every one of the four assertions runs on every money-adjacent action,
#     not in a design review
# [ ] a balance carries its own timestamp all the way to the screen
# [ ] "available" is not "balance" -- subtract uncleared cheques, holds, and
#     the minimum the bank requires
# [ ] one currency base, converted at a STORED rate with a timestamp, never
#     at today's rate applied to yesterday's balance
# [ ] read-only access by default. The consent to SEE money and the consent
#     to MOVE money are different permissions and should look different
# [ ] aggregate in IST against bank cut-offs, not a UTC calendar day
''')

i_step12 = '''
<h3 id="s-indigo-s1">Steps 1 and 2 &mdash; What you are not, and what the money is</h3>
''' + code_boundary + '''
<p><strong>On data:</strong> a business&rsquo;s bank data reaches you through the <strong>Account
Aggregator</strong> framework with a consent artefact, and GSTN is an information provider inside it,
so returns are available on the same rails. Two things carry over from the
<a href="/fintech-ai/products/account-aggregator/">AA guide</a> and are not repeated here:
<strong>verify the consent artefact signature</strong>, and remember that <strong>two clocks
apply</strong> &mdash; how long you may fetch is not how long you may keep.</p>
'''

i_step34 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; Receivables, and the IRN that makes one real</h3>
<p>An SME treasury product lives on the receivables ledger, and in India that ledger has a tax
dependency most treasury software treats as somebody else&rsquo;s problem.</p>
<table>
<tr><th>Rule</th><th>Position</th></tr>
<tr><td><strong>E-invoicing applies</strong></td><td>AATO above <strong>&#8377;5 crore</strong> in any financial year since 2017-18. <strong>Permanent once crossed</strong> &mdash; it keeps applying to every GSTIN under that PAN even if a later year falls below</td></tr>
<tr><td><strong>The 30-day hard stop</strong></td><td>AATO <strong>&#8377;10 crore and above</strong>, from <strong>1 April 2025</strong>: an invoice, credit note or debit note must reach the IRP <strong>within 30 days of its date</strong>. The portal refuses it afterwards</td></tr>
<tr><td><strong>What a miss costs</strong></td><td>No IRN means <strong>no valid tax invoice</strong>, which means <strong>your customer cannot claim input tax credit</strong></td></tr>
<tr><td><strong>Cancellation</strong></td><td><strong>24 hours</strong> on the IRP. After that it is a credit note, which itself must be reported</td></tr>
<tr><td><strong>Turnover is aggregate</strong></td><td>Across all GSTINs under one PAN: taxable, exempt, exports and inter-state stock transfers, excluding GST itself</td></tr>
</table>
''' + warn("<strong>This is where a treasury problem becomes a customer relationship problem, and it is the finding worth carrying off this page.</strong> A missed IRN does not hurt the business that issued the invoice first. <strong>It hurts their customer</strong>, who loses input tax credit on a purchase they have already paid for &mdash; and who will remember it at renewal. <strong>Model the IRN as a state on the receivable, not as a field on the invoice</strong>, with an age, an owner and an escalation before day 30. A receivable with no IRN is not a receivable you can chase, finance or count.") + '''
<p>The rest of receivables is ordinary and still usually done badly: ageing buckets that mean
something, a promised-payment date that is separate from the due date, and a single reference that
survives from invoice to bank credit. <strong>If the invoice cannot be matched to the credit
automatically, the whole product degrades into a spreadsheet with a login.</strong></p>

<h3 id="s-indigo-s4">Step 4 &mdash; Payables, which is really about permission</h3>
<p>The engineering here is small and the design is not. Three questions decide it: <strong>who may
approve, up to what, and who may release</strong>. In most small businesses one person does all
three, and the product&rsquo;s job is to make the separation cheap enough to adopt rather than to
enforce a policy nobody asked for.</p>
''' + note("<strong>The control that pays for itself is beneficiary verification on change, not approval limits.</strong> Invoice-redirection fraud does not defeat an approval workflow &mdash; the payment is genuinely approved, to genuinely the wrong account. <strong>Treat a change of bank details on an existing supplier as a separate event requiring separate confirmation through a channel the request did not arrive on.</strong> It is a day of work and it is the single highest-value control in this product.")

code_forecast = code('Python — steps 5 to 8, a forecast with a confidence, a surplus without advice, and the close', r'''# STEP 5. FORECAST. A NUMBER IS A LIE; A RANGE IS A FORECAST.
# The useful output is not "you will have 42 lakh on the 30th". It is "payroll
# on the 30th is covered unless these two invoices slip, and here they are".

def cash_forecast(position, receivables, payables, horizon_days=45):
    base = position["total_paise"]
    rows = []
    for d in range(horizon_days):
        day = date.today() + timedelta(days=d)
        inflow_p50 = sum(r["amount_paise"] * r["p_pay_by"](day) for r in receivables)
        outflow = sum(p["amount_paise"] for p in payables if p["due"] == day)
        base = base + inflow_p50 - outflow
        rows.append({"date": day.isoformat(), "expected_paise": base,
                     "committed_outflow_paise": outflow})
    return {"rows": rows,
            "confidence": position["confidence"],      # inherits its inputs
            "drivers": top_swing_factors(receivables), # WHICH invoices decide it
            "breach_dates": [r["date"] for r in rows if r["expected_paise"] < 0]}

# The single most useful screen in the product is not the chart. It is:
# "these three invoices decide whether the 30th works."

# STEP 6. THE SURPLUS, WITHOUT BECOMING AN ADVISER.
def surplus_options(customer, amount_paise, days_until_needed):
    opts = customer["bank"].deposit_products(amount_paise, days_until_needed)
    return {
        "amount_paise": amount_paise,
        "days_until_needed": days_until_needed,
        # Arithmetic, in a stable order, with the assumptions visible.
        "options": [{"name": o["name"], "rate_pa": o["rate_pa"],
                     "lock_in_days": o["lock_in_days"],
                     "interest_paise": simple_interest(amount_paise, o["rate_pa"],
                                                       days_until_needed),
                     "breaks_before_needed": o["lock_in_days"] > days_until_needed}
                    for o in opts],
        "sort": "stable_by_lock_in",     # NOT by return. A default sort ranks.
        "recommended": None,             # and it stays None
        "disclaimer_is_not_the_control": True,
    }

# STEP 7. CURRENCY -- if they trade abroad, there is a queue waiting for them.
def fx_exposure(invoices, base="INR"):
    open_entries = [i for i in invoices if i["edpms_idpms_status"] == "OPEN"]
    return {"by_currency": bucket(invoices, "currency"),
            # Entries stay open until somebody closes them, and resurface as a
            # bank declining the next transaction. Queue, owner, age.
            "open_regulatory_entries": len(open_entries),
            "oldest_open_days": max([i["age_days"] for i in open_entries] or [0])}

# STEP 8. CLOSE THE LOOP.
def close(period, ledger, statements):
    # FULL OUTER JOIN. A bank line matching no ledger entry is the interesting
    # case -- money that moved and nobody can explain.
    matched, only_ledger, only_bank = full_outer_match(ledger, statements)
    assert control_total(statements) == expected_total(period), "abort: file incomplete"
    return {"matched": len(matched), "unexplained_bank_lines": len(only_bank),
            "unmatched_ledger": len(only_ledger),
            "decisions_log": period["decisions"]}   # what was decided, and why

# WHAT TO CHECK
# [ ] a forecast carries the confidence of its worst input, not its best
# [ ] name the invoices that decide the outcome. That is the product
# [ ] surplus options are never ranked, sorted by return, or badged. Stable
#     order, visible assumptions, nothing recommended
# [ ] control totals BEFORE matching, and abort on mismatch -- a truncated
#     statement reconciles perfectly on the rows it contains
# [ ] full outer join, never left. The unexplained bank line is the point
# [ ] EDPMS and IDPMS entries tracked as a queue with an owner and an age
# [ ] log the DECISION, not only the transaction: what was chosen, on what
#     figures, by whom. That log is the difference between a tool and a record
''')

i_step58 = '''
<h3 id="s-indigo-s5">Steps 5 to 8 &mdash; Forecast, surplus, currency, close</h3>
''' + code_forecast + '''
<p><strong>On forecasting, briefly, because the temptation is large.</strong> This is the step where
a team reaches for a model, and for most SMEs a model is the wrong tool for an honest reason:
<strong>the outcome is usually decided by two or three specific invoices</strong>, not by a pattern
across thousands. Naming those invoices is more useful than predicting the aggregate, it is
explainable, and it survives the month the business wins an unusually large order. <strong>If you do
use a model, everything in the alternative credit scoring guide applies</strong> &mdash; including
that a rule engine is a model and that you must be able to say why.</p>
''' + warn("<strong>Step 6 is where this product most often crosses a line without noticing.</strong> Showing a customer what their own bank offers on a 30-day deposit, with the interest worked out, is arithmetic. <strong>Sorting that list by return is a recommendation.</strong> So is a &ldquo;best for you&rdquo; badge, a default selection, and a nudge that appears only when the balance is large. The <a href=\"/fintech-ai/products/robo-advisory/\">robo-advisory guide</a> sets out the three screen tests; run them on this screen every release, because this is the screen a growth team will want to optimise.") + '''

<h3 id="s-indigo-s7">Where this product touches the rest of the section</h3>
<p>Thirteen guides in, the map is worth drawing once. <strong>A treasury product is an integration of
other people&rsquo;s regulated surfaces</strong>, and each one has its own page:</p>
<table>
<tr><th>Surface</th><th>Where the detail is</th></tr>
<tr><td>Consented bank and GST data</td><td><a href="/fintech-ai/products/account-aggregator/">Account Aggregator</a></td></tr>
<tr><td>Paying suppliers, collecting from customers</td><td><a href="/fintech-ai/payments-reconciliation/build-sheet/">Build Sheet 05</a> and <a href="/fintech-ai/products/upi-switch/">UPI</a></td></tr>
<tr><td>Standing instructions and auto-debits</td><td><a href="/fintech-ai/products/recurring-payments/">Recurring Payments</a></td></tr>
<tr><td>Turning an unpaid invoice into cash</td><td><a href="/fintech-ai/products/invoice-discounting/">Invoice Discounting</a></td></tr>
<tr><td>Paying or being paid across borders</td><td><a href="/fintech-ai/products/cross-border-payments/">Cross-Border Payments</a></td></tr>
<tr><td>Anything resembling a recommendation</td><td><a href="/fintech-ai/products/robo-advisory/">Robo-Advisory</a></td></tr>
<tr><td>Anything resembling a credit decision</td><td><a href="/fintech-ai/products/alternative-credit-scoring/">Alternative Credit Scoring</a></td></tr>
</table>
'''

i_cost = registry("SME treasury &mdash; what it costs", [
 ("Registrations", "direct",
  "<strong>None, if you hold the four lines.</strong> That is the entire commercial argument for "
  "building this product rather than a lending or payments one &mdash; and it evaporates the first "
  "time money rests in your account."),
 ("Account Aggregator", "direct",
  "Per fetch, plus the build. Scope it as <strong>two modules</strong> if you are a regulated entity: "
  "joining as an FIU can also require joining as an FIP. Detail in the Account Aggregator guide."),
 ("Bank connectivity", "direct",
  "The real integration cost, and it is <strong>per bank</strong>. Coverage is the product; a treasury "
  "tool that sees three of a customer&rsquo;s four accounts is worse than a spreadsheet, because it "
  "looks complete."),
 ("E-invoicing integration", "direct",
  "IRP connectivity, or a GSP. Small against what a <strong>blocked IRN</strong> costs a customer&rsquo;s "
  "customer in lost input tax credit."),
 ("Forecast accuracy", "indirect",
  "Not a line item and the thing you are actually selling. <strong>A wrong forecast that looks "
  "confident is worse than no forecast</strong>, because an SME will schedule payroll against it."),
 ("The support cost of being right", "indirect",
  "Every stale balance, unmatched credit and open EDPMS entry becomes a conversation. "
  "<strong>Staff reconciliation as a queue with an owner</strong>, not as a month-end task."),
 ("What you are competing with", "indirect",
  "<strong>A spreadsheet and a WhatsApp group, and they are free and already working.</strong> The bar "
  "is not another treasury product. It is the incumbent process, which has no licence fee and no "
  "integration risk."),
], "September 2026") + note("<strong>The honest pricing observation for this product:</strong> an SME will pay for a decision it can act on and will not pay for a dashboard. The willingness to pay sits on <em>&ldquo;payroll on the 30th is covered unless these two invoices slip&rdquo;</em> &mdash; a sentence, not a chart &mdash; and everything on this page exists to make that sentence true and defensible.")

a_builds = '''
<h3 id="s-amber-week">Read-only visibility</h3>
<p><strong>Build:</strong> AA consent &rarr; balances across every account with timestamps &rarr;
receivables ageing with IRN state &rarr; one position, one currency base.</p>
<p><strong>You get:</strong> the thing the spreadsheet cannot do, with <strong>no regulated
surface at all</strong>. Read-only is a legitimate destination, not a stepping stone.</p>

<h3 id="s-amber-proper">Visibility plus initiation</h3>
<p><strong>Build:</strong> the above, plus approval workflow, beneficiary-change verification, payment
initiation <strong>from the customer&rsquo;s own account on their own mandate</strong>, and
reconciliation with control totals and a full outer join.</p>
<p><strong>Trade:</strong> initiation is where the four assertions start earning their place daily.
<strong>Money still never rests with you</strong> &mdash; if a feature needs it to, the feature is the
problem, not the assertion.</p>

<h3 id="s-amber-big">Treasury with financing and currency</h3>
<p><strong>Build:</strong> the above, plus routing to <strong>TReDS</strong> or a regulated lender for
the cash gap, EDPMS and IDPMS tracked as an aged queue, and surplus options shown as arithmetic in a
stable order.</p>
<p><strong>It breaks when:</strong> one of the four boundaries is crossed for a good reason. The
sequence is always the same &mdash; a customer asks, it is scoped as a fortnight, and it ships.
<strong>Make the assertion fail the build rather than fail a review.</strong></p>
''' + note("If you take one thing from this page: <strong>the four boundaries are code, not policy.</strong> Every one of them will be crossed by a feature request that is reasonable, well-intentioned and small. An assertion that fails the build is the only version of that boundary that survives contact with a roadmap.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Funds rest in a platform account</strong></td><td>&ldquo;Instant payouts&rdquo; shipped as a feature.</td><td>Assert the settlement account owner. You are not a payment aggregator.</td></tr>
<tr><td><strong>Surplus list sorted by return</strong></td><td>It is the obvious default sort.</td><td>Stable order, no ranking, nothing recommended.</td></tr>
<tr><td><strong>Stale balance shown as current</strong></td><td>The timestamp was dropped at the API layer.</td><td>Carry it to the screen. Payroll gets decided on that number.</td></tr>
<tr><td><strong>Receivable with no IRN, past day 30</strong></td><td>IRN treated as a field, not a state.</td><td>State with an age, an owner and escalation before day 30.</td></tr>
<tr><td><strong>Customer loses input tax credit</strong></td><td>A missed IRN on an invoice they already paid.</td><td>Same fix, and tell them early rather than at reconciliation.</td></tr>
<tr><td><strong>Payment approved, to the wrong account</strong></td><td>Invoice redirection defeats approval, not verification.</td><td>Beneficiary change is a separate event, confirmed out of band.</td></tr>
<tr><td><strong>Forecast confident and wrong</strong></td><td>Confidence not inherited from inputs.</td><td>A forecast carries the confidence of its worst input.</td></tr>
<tr><td><strong>Reconciled perfectly against a truncated file</strong></td><td>No control totals.</td><td>Control totals first, abort on mismatch.</td></tr>
<tr><td><strong>Unexplained bank credits never surface</strong></td><td>Left join instead of full outer.</td><td>Full outer join. The unmatched bank line is the point.</td></tr>
<tr><td><strong>EDPMS backlog discovered by a declined transaction</strong></td><td>Nobody owned the queue.</td><td>Owner and age, from the first transaction.</td></tr>
<tr><td><strong>Three of four accounts connected</strong></td><td>One bank had no integration.</td><td>Say so on screen. A partial position that looks complete is worse than none.</td></tr>
</table>
'''

SRC=[('official','GST e-invoicing under Rule 48(4), CGST Rules','the ₹5 crore aggregate annual turnover threshold applying since 1 August 2023 to any financial year from 2017-18 onwards and continuing to apply once crossed; aggregate turnover computed across all GSTINs under one PAN including taxable, exempt, export and inter-state stock transfer values and excluding GST; and the treatment of an invoice issued without a valid IRN as not issued.','https://www.cbic.gov.in'),
 ('official','GSTN advisory of 5 November 2024 on the IRP reporting window','the 30-day limit for reporting invoices, credit notes and debit notes to the Invoice Registration Portal, extended from taxpayers with AATO of ₹100 crore and above to those with ₹10 crore and above with effect from 1 April 2025, after which the portal refuses the document; and the 24-hour cancellation window on the IRP.','https://einvoice.gst.gov.in'),
 ('official','RBI (Regulation of Payment Aggregators) Directions, 2025','the escrow requirement with a scheduled commercial bank, the exclusion of own funds, the day-end balance equal to the amount realised, and the ₹15 crore to ₹25 crore net worth path — the regime a treasury product enters the moment customer funds rest in its own account. Detail in Build Sheet 05.','https://www.rbi.org.in'),
 ('official','SEBI position on the advisory perimeter','that a program recommending securities to a specific person on the basis of their circumstances is giving investment advice, and that a disclaimer does not change what an activity is — the basis for showing surplus options as arithmetic in a stable order rather than as a ranked list. Detail in the Robo-Advisory guide.','https://www.sebi.gov.in'),
 ('official','Account Aggregator framework and the NBFC-AA Master Direction','the consent-artefact mechanism through which bank and GST data reaches a treasury product, the requirement to verify the artefact signature, and the separate consent-expiry and data-life clocks. Detail in the Account Aggregator guide.','https://www.rbi.org.in'),
 ('official','FEMA and the EDPMS / IDPMS reporting framework','the requirement that currency conversion run through an authorised dealer bank, and that export and import entries remain open until documented — the queue that resurfaces as a bank declining the next transaction. Detail in the Cross-Border Payments guide.','https://www.rbi.org.in'),
 ('industry','E-invoicing implementation commentary','the operational read on threshold proposals below ₹5 crore, portal authentication changes, and the practical consequence of a blocked IRN for a recipient&rsquo;s input tax credit. Directional; confirm any threshold against the current notification before relying on it.',''),
 ('industry','SME cash-management practice','the observation that the incumbent process is a spreadsheet and a messaging group, and that willingness to pay attaches to an actionable decision rather than to a dashboard. Judgement, not a measured figure.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. GST thresholds have been lowered repeatedly and proposals below &#8377;5 crore '
 'have been discussed; confirm the current figure against the notification rather than against this page.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/products/invoice-discounting/" class="mod-card"><div class="mod-num">GUIDE 08</div><h3>Invoice Discounting</h3><p>The regulated way to turn a receivable into cash without becoming a lender.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Escrow, control totals, full outer joins and the economics of moving money.</p></a>
<a href="/fintech-ai/products/robo-advisory/" class="mod-card"><div class="mod-num">GUIDE 12</div><h3>Robo-Advisory</h3><p>The three screen tests for whether a screen has become a recommendation.</p></a>
<a href="/fintech-ai/build-playbook/" class="mod-card"><div class="mod-num">PLAYBOOK</div><h3>Build Playbook</h3><p>Licensing, stack selection and the go-live gate, in one place.</p></a>
</div>
''' + warn("This page is a guide, not a specification. A treasury product sits next to four regulated activities and the distance between it and each of them is one feature. Nothing here is legal advice. Have your fund flows, your surplus screen and your financing referrals reviewed by qualified counsel before launch, and re-review them whenever the roadmap adds something a customer asked for.")

lanes={'green':[("How to use this page",g_read),("What SME treasury actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — the four lines, and the cash position",i_step12),
           ("Steps 3 and 4 — receivables, the IRN, and payables",i_step34),
           ("Steps 5 to 8 — forecast, surplus, currency, close",i_step58),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="SME Treasury: How to Build It"
META=("Build an SME treasury product step by step: the four lines that turn it into a regulated "
      "business, the IRN that makes a receivable real, and what breaks.")
LEAD=("A step-by-step guide to building cash and treasury software for Indian small businesses. "
      "Eight stages, the options at each one, exactly how each step connects to the next, real "
      "costs, and what breaks. Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/sme-treasury",title=TITLE,meta=META,lead=LEAD,label="Product Guide 13",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/sme-treasury/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m, "no <body>"
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t, "no page-hero"
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Building cash and treasury '
  'software for small businesses? The eight steps, the four lines that turn it into a regulated business, '
  'and the IRN that makes a receivable real: <a href="/fintech-ai/products/sme-treasury/"><strong>SME '
  'Treasury: How to Build It &rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('customer-operations', 'infrastructure'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/sme-treasury' in src:
        print('  = already linked from /' + mod + '/'); continue
    n = src.count(ANCHOR)
    assert n == 1, 'anchor appears ' + str(n) + ' times in ' + p + ' — refusing to write'
    i = src.find(ANCHOR); assert i != -1, 'anchor not found in ' + p
    out = src[:i] + NOTE_BLOCK + src[i:]
    assert NOTE_BLOCK.count('<div') == 1 and NOTE_BLOCK.count('</div>') == 1, 'block shape changed'
    assert out.count('<div') == src.count('<div') + 1, 'div count moved'
    assert out.count('</div>') == src.count('</div>') + 1, 'close-div count moved'
    assert len(out) == len(src) + len(NOTE_BLOCK), 'length delta wrong'
    _io.open(p, 'w', encoding='utf-8').write(out)
    print('  + linked from /' + mod + '/')
