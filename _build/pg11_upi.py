#!/usr/bin/env python3
# Session 83 — PRODUCT GUIDE 11: UPI switch infrastructure
# First guide where the counterparty is NPCI rather than a regulator.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building on UPI: an app that pays, a checkout that collects, or the
switch underneath either. Not how UPI works for a user &mdash; how you connect to it, get certified,
stay up, and settle.</p>
<p>Ten guides on this site describe a rulebook written by a regulator. <strong>This one describes a
rulebook written by a company.</strong> NPCI is not a regulator. It is a not-for-profit umbrella
organisation operating an RBI-authorised payment system &mdash; and its circulars will constrain your
product more tightly, day to day, than most regulations do.</p>
''' + warn("<strong>UPI acquired a revenue model this week, after six years without one.</strong> The <strong>Taxation and Other Laws (Amendment) Bill, 2026</strong> amended the <strong>Payment and Settlement Systems Act, 2007</strong> to remove the bar on charging for UPI and RuPay debit, and the government notification followed on <strong>14 September 2026</strong>. It fixes one thing and leaves the rest open: <strong>no charge on UPI transactions up to &#8377;2,000, no charge on RuPay debit, and P2P stays free.</strong> Whether MDR applies only above a merchant-size threshold, at what rate, and how the income is split between the parties is with NPCI's <strong>UPI and Services Steering Committee</strong>, expected to meet this week. Rates in the <strong>0.25% to 0.4%</strong> range have been discussed. <strong>Nothing above that sentence is settled, and by the time you read this some of it will be.</strong>")

g_what = '''
<p>Four different products get called &ldquo;building on UPI&rdquo; and they have almost nothing in
common except the rails:</p>
<table>
<tr><th>What you are building</th><th>What you actually need</th><th>Effort</th></tr>
<tr><td><strong>Accepting UPI as a merchant</strong></td><td>A payment aggregator or gateway. You are a customer of this ecosystem, not a participant in it.</td><td>Days</td></tr>
<tr><td><strong>A UPI app (TPAP)</strong></td><td>A <strong>PSP bank</strong> to sponsor you, plus NPCI certification.</td><td>Months</td></tr>
<tr><td><strong>UPI inside your own app</strong></td><td>A sponsor bank&rsquo;s SDK, plus <strong>UDIR integration</strong>. See step 6.</td><td>Weeks to months</td></tr>
<tr><td><strong>The switch itself</strong></td><td>To <em>be</em> a bank, or to build the switch a bank runs.</td><td>Quarters</td></tr>
</table>
''' + note("<strong>Work out which one you are before reading further.</strong> Most teams who say &ldquo;we are building a UPI product&rdquo; mean row one, which is a commercial decision rather than an engineering project and is covered in Build Sheet 05. Rows two and four are where this page lives.") + '''
<p><strong>Who is who on the rails:</strong></p>
<table>
<tr><th>Party</th><th>Role</th></tr>
<tr><td><strong>NPCI</strong></td><td>Owns and operates UPI. Sets the rules, the liabilities, the settlement cut-offs and the dispute protocol. Approves who may participate. <strong>May audit you, directly or through a third party.</strong></td></tr>
<tr><td><strong>PSP bank</strong></td><td>A bank, connected to UPI. Holds the handle. <strong>Audits your app, owns grievance redressal, and answers for your data residency.</strong></td></tr>
<tr><td><strong>TPAP</strong></td><td>The app the customer sees. <strong>No licence, no direct line to the network.</strong> Borrows both.</td></tr>
<tr><td><strong>Issuer and beneficiary banks</strong></td><td>Where the money leaves and lands. <strong>Neither is under your control and both can fail your transaction.</strong></td></tr>
</table>
<p><strong>What this is not:</strong></p>
<ul>
<li><strong>Not a licence you can hold.</strong> Participation is approved by NPCI and sponsored by a
bank. You are always on somebody&rsquo;s paper.</li>
<li><strong>Not a feature race.</strong> The product is <strong>uptime and decline rate</strong>.
Step 8.</li>
<li><strong>Not free forever.</strong> It was, until this week.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Pick the shape</strong></td><td>Which of the four products, honestly.</td></tr>
<tr><td>2</td><td><strong>Find a bank</strong></td><td>The commercial step everyone underestimates.</td></tr>
<tr><td>3</td><td><strong>Certify with NPCI</strong></td><td>Technical and compliance. Not a formality.</td></tr>
<tr><td>4</td><td><strong>The payment path</strong></td><td>Intent, collect, QR, mandate. Four flows, one rulebook.</td></tr>
<tr><td>5</td><td><strong>The deemed state</strong></td><td><strong>Not success, not failure. The state that breaks systems.</strong></td></tr>
<tr><td>6</td><td><strong>Disputes</strong></td><td>UDIR, and a turnaround clock with a penalty on it.</td></tr>
<tr><td>7</td><td><strong>Reconcile and settle</strong></td><td>Cut-offs you do not control.</td></tr>
<tr><td>8</td><td><strong>Run it</strong></td><td>Declines, uptime, the 30% cap, and now MDR.</td></tr>
</table>
''' + note("<strong>Steps 5, 6 and 8 are where the work is</strong>, and they are the three that look like operations rather than product. A team that builds steps 1 to 4 well has built a demo that works on a good day. UPI does not have only good days.")

i_step123 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Pick the shape</h3>
<p>The question that settles it: <strong>do you need to hold the customer&rsquo;s UPI handle?</strong>
If you do, you are a TPAP and you need a PSP bank. If you only need to be paid, you need an aggregator
and this page is mostly background.</p>

<h3 id="s-indigo-s2">Step 2 &mdash; Find a bank</h3>
<p>This is a partnership negotiation, not an integration, and it is the step that decides your
timeline. The bank is taking on your risk: <strong>NPCI holds the PSP bank responsible for auditing
your app and systems, for the grievance mechanism your customers use, and for keeping all UPI
transaction data in India.</strong> A bank that signs you is accepting audit findings on your code.</p>
<p>Two routes, and the trade is the usual one:</p>
<table>
<tr><th></th><th>Direct with a PSP bank</th><th>Through an enabler</th></tr>
<tr><td><strong>You own</strong></td><td>The whole stack</td><td>The app surface</td></tr>
<tr><td><strong>Certification</strong></td><td>Yours to pass</td><td>Largely inherited</td></tr>
<tr><td><strong>Time</strong></td><td>Months</td><td>Weeks</td></tr>
<tr><td><strong>Ceiling</strong></td><td>None you did not build</td><td>Theirs</td></tr>
<tr><td><strong>Reversibility</strong></td><td>Hard &mdash; the handle suffix is theirs</td><td>Harder</td></tr>
</table>
''' + warn("<strong>The handle suffix is a switching cost disguised as a branding decision.</strong> Your customers' UPI IDs end in your PSP bank's suffix. Changing banks later means every customer re-registers a new UPI ID, which in practice means losing a meaningful share of them. <strong>Ask about the exit before you sign the entry</strong> &mdash; same rule as the payment-gateway exit path in Build Sheet 05, and for the same reason: integration takes weeks and extraction takes quarters.") + '''

<h3 id="s-indigo-s3">Step 3 &mdash; Certify with NPCI</h3>
<p>NPCI approves participation. Certification covers the technical implementation and the compliance
posture, and the specification moves &mdash; the common library, the PIN handling, the API versions and
the dispute hooks all get revised, and revisions come with dates.</p>
''' + note("<strong>Budget for re-certification as a standing cost, not a launch cost.</strong> The single most common planning error on this rail is treating NPCI certification as a gate you pass once. It is closer to a subscription: circulars land, deprecations get announced, and the compliance date is set by somebody else's calendar. <strong>A team with no capacity reserved for spec changes will spend its roadmap on them anyway.</strong>")

code_flow = code('Python — steps 4 and 5, the four flows and the state that is neither success nor failure', r'''from datetime import datetime, timedelta

# STEP 4. FOUR FLOWS, ONE RULEBOOK.
FLOWS = {
    "intent":  "customer taps, app opens, customer approves",     # best success
    "collect": "you request, customer approves later",            # worst success
    "qr":      "customer scans and pays",                         # merchant default
    "mandate": "recurring, pre-authorised",                       # see Guide 05
}

# Collect requests are the flow most abused and the flow with the worst
# conversion. Treat a high collect share as a product smell, not a feature.

# STEP 5. THE DEEMED STATE. THIS IS THE ONE.
# A UPI transaction that does not return a clean result is NOT a failure. It
# is an UNKNOWN. The debit may have happened. The credit may have happened.
# Your system knows neither, and the customer is looking at your screen.

TERMINAL = {"SUCCESS", "FAILURE"}

def on_response(txn, response):
    if response and response["result"] in TERMINAL:
        return {"state": response["result"], "final": True}
    # Deemed. Do not guess. Do not retry with a new reference.
    return {"state": "DEEMED", "final": False,
            "action": "poll_status",
            "customer_message": "We are confirming this payment",   # not "Failed"
            "never": "initiate_a_second_debit"}

def poll_plan(txn):
    """Back off. A thundering herd of status checks is how an incident
    becomes an outage -- yours and everyone else's on the same switch."""
    return [5, 15, 30, 60, 120, 300]        # seconds, then hand to reconciliation

def resolve(txn, npci_status, ledger):
    # NPCI reconciles and the outcome is guaranteed to settle one way or the
    # other. Your job is to make sure YOUR ledger ends up agreeing with it,
    # and to never have told the customer something the ledger contradicts.
    assert txn["reference"] == npci_status["reference"], "same intent, same reference"
    ledger.apply(npci_status["final_state"])
    return npci_status["final_state"]

# WHAT TO CHECK
# [ ] "deemed" is a first-class state in your schema, with its own screen,
#     its own message and its own queue. Not a null, not a failure
# [ ] a retry uses the SAME reference derived from the intent, stored BEFORE
#     the call. A fresh reference on an unknown outcome is how a customer
#     gets debited twice -- the same rule as payouts in Build Sheet 05
# [ ] status polling backs off. Fixed-interval polling during a switch
#     incident is load you are adding to an outage
# [ ] never show "Payment failed" on a deemed transaction. The money may be
#     gone, and you have just told someone it is not
# [ ] every state change is idempotent and keyed on the event id, applied in
#     the same database transaction as the ledger write
# [ ] reconcile in IST against NPCI settlement cut-offs, not against your own
#     calendar day
''')

i_step45 = '''
<h3 id="s-indigo-s4">Steps 4 and 5 &mdash; The payment path, and the deemed state</h3>
''' + code_flow + '''
<p><strong>The gotcha that produces the worst customer outcomes on this rail:</strong> <strong>a
pending UPI transaction is an unknown, not a failure, and the two demand opposite behaviour.</strong>
On a failure you retry. On an unknown you must not, because the debit may already have happened.</p>
<p>The ecosystem resolves this for you eventually &mdash; NPCI reconciles, and a failed debit is
auto-reversed under the RBI turnaround-time framework with a per-day penalty for delay. <strong>What
the framework does not do is tell your customer what is happening in the ninety seconds they are
staring at your screen.</strong> That copy is yours to write, and writing <em>&ldquo;Payment
failed&rdquo;</em> on a deemed transaction is the single most damaging string in a UPI product.</p>
'''

code_ops = code('Python — steps 6 to 8, disputes, settlement and the numbers you are actually judged on', r'''# STEP 6. DISPUTES GO THROUGH UDIR, NOT THROUGH YOUR SUPPORT INBOX.
# Unified Dispute and Issue Resolution is the ecosystem's protocol. If you
# are a partner application on a sponsor bank's SDK, integrating UDIR is a
# requirement, not an option -- your customers' eligible complaints have to
# be raised into it.

def raise_dispute(txn, reason, udir):
    case = udir.open(reference=txn["reference"], reason=reason,
                     raised_at=now_ist())
    return {"case_id": case["id"], "track_in": "UDIR",
            "your_job": "keep the customer informed while it runs"}

# STEP 7. SETTLEMENT. The cut-offs are NPCI's, not yours.
def settlement_day(txn_time_ist, cutoffs):
    """A transaction after the cut-off settles in the next cycle. Aggregating
    on a UTC day boundary moves 5.5 hours of transactions into the wrong
    settlement day, every single day."""
    return cutoffs.cycle_for(txn_time_ist)

# STEP 8. WHAT YOU ARE ACTUALLY MEASURED ON.
# Declines split two ways and only one of them is your problem -- but the
# ecosystem measures BOTH against you, and the split is the whole
# conversation with your bank and with NPCI.

def classify_decline(code_, who):
    TECHNICAL = {"switch_timeout", "psp_unavailable", "issuer_down",
                 "beneficiary_unreachable"}          # infrastructure
    BUSINESS  = {"insufficient_funds", "wrong_pin", "limit_exceeded",
                 "account_blocked"}                  # the customer or their bank
    if code_ in TECHNICAL:
        return {"type": "TD", "owner": who, "counts_against_you": True}
    if code_ in BUSINESS:
        return {"type": "BD", "owner": "customer", "counts_against_you": False}
    return {"type": "UNCLASSIFIED", "action": "map_it_before_it_ships"}

def health(window):
    return {
        "td_rate": technical_declines(window) / total(window),
        "td_by_issuer": td_split(window, "issuer"),      # not your fault, your problem
        "success_by_flow": success_split(window, "flow"),
        "deemed_rate": deemed(window) / total(window),
        "deemed_unresolved_over_1h": aging_deemed(window),
        "market_share_rolling_3m": share_rolling(window, months=3),  # the 30% cap
    }

# WHAT TO CHECK
# [ ] every decline code is MAPPED to technical or business before launch.
#     An unclassified bucket is where your real TD rate hides
# [ ] plot TD by issuer bank. You cannot fix another bank's infrastructure,
#     but you can route around it, warn the customer, and take it to your PSP
# [ ] track market share on a ROLLING THREE-MONTH basis if you are anywhere
#     near scale. That is how the cap is computed
# [ ] the deemed queue has an owner and an age, like the EDPMS queue in
#     Guide 06. Unresolved deemed transactions are a support backlog that
#     arrives all at once
# [ ] build the per-rail, per-ticket-size fee engine NOW. The threshold is
#     fixed at 2,000 rupees. The rate is not yours to choose or to schedule
''')

i_step68 = '''
<h3 id="s-indigo-s6">Steps 6 to 8 &mdash; Disputes, settlement, and running it</h3>
''' + code_ops + '''
<p><strong>THE finding, and it is the reason this page exists:</strong> <strong>your technical
decline rate is not a metric, it is the condition of your participation.</strong> UPI publishes
bank-level performance, NPCI can audit participants, and a switch that declines transactions for
infrastructure reasons is a problem the ecosystem addresses rather than tolerates. Feature roadmaps
do not survive that conversation; decline rates do.</p>
<p>And the part that makes it hard: <strong>a large share of your declines will not be your
fault.</strong> An issuer bank you have no relationship with, on infrastructure you cannot see, will
fail your customers&rsquo; payments and the customer will blame your app. You cannot fix it. You can
measure it per issuer, route around it where a second option exists, tell the customer something
truthful about why, and take the data to your PSP bank &mdash; which is the only party with standing
to escalate it. <strong>Teams that do not split declines by issuer spend years believing their own
switch is worse than it is.</strong></p>

<h3 id="s-indigo-scap">The 30% cap, still scheduled</h3>
<p>NPCI proposed in <strong>November 2020</strong> that no single third-party application provider
should process more than <strong>30% of UPI transaction volume</strong>, measured over the preceding
three months on a rolling basis, with breach met by <strong>a halt on onboarding new
customers</strong> rather than by blocking transactions. Bank-owned UPI apps are outside it.</p>
<p>The deadline has moved three times &mdash; 2022, then <strong>31 December 2024</strong>, then
<strong>31 December 2026</strong>, which is where it stands. Two apps have been well above the cap
throughout, at roughly three-quarters of monthly volume between them.</p>
''' + warn("<strong>Be careful how you use this in a business case, in either direction.</strong> The honest statement is that the cap is <strong>scheduled for 31 December 2026 and has been deferred three times</strong>. A plan that assumes it binds on that date is betting against a consistent pattern. A plan that assumes it never binds is betting that a stated rule will not be enforced. <strong>The defensible position is to build the rolling three-month share measurement and know your own number</strong>, which costs almost nothing and is the input to either outcome. Check the current position before you rely on this paragraph; it is the most likely line on this page to be out of date.")

i_cost = registry("UPI infrastructure &mdash; what it costs", [
 ("The bank relationship", "direct",
  "Commercial terms with a PSP or sponsor bank, and the step that sets your timeline. "
  "<strong>Negotiate the exit at the same time as the entry</strong> &mdash; the handle suffix makes "
  "leaving expensive in customers, not in rupees."),
 ("NPCI certification", "direct",
  "Technical and compliance certification to participate. <strong>Then treat re-certification as a "
  "standing engineering cost</strong>: specifications are revised and the compliance dates are set "
  "elsewhere."),
 ("Running the switch", "direct",
  "Infrastructure sized for peak, not average, on a rail that does <strong>24.51 billion "
  "transactions worth &#8377;29.82 lakh crore in a month</strong>. Capacity is a compliance posture "
  "here, not a cost-optimisation exercise."),
 ("The deemed queue", "indirect",
  "Support and operations cost that arrives in bursts, during exactly the incidents when everything "
  "else is also on fire. Staff it as a queue with an owner."),
 ("Revenue, from this week", "direct",
  "<strong>Zero since January 2020; the bar was removed by the 2026 amendment and notified on "
  "14 September 2026.</strong> Confirmed so far: nothing charged up to <strong>&#8377;2,000</strong>, "
  "nothing on RuPay debit, P2P free. <strong>The rate, the merchant threshold and the split between "
  "parties are with the NPCI Steering Committee.</strong> Rates of 0.25% to 0.4% have been discussed "
  "&mdash; against 1&ndash;3% on credit cards and up to 0.9% on debit."),
 ("The shape of the revenue", "indirect",
  "In 2025-26, transactions above &#8377;2,000 to merchants were about <strong>4% of UPI volume and "
  "roughly two thirds of its value</strong>. <strong>A threshold set at &#8377;2,000 therefore "
  "exempts almost every transaction and reaches most of the money</strong> &mdash; which is the "
  "design, and it is why a volume-weighted revenue model will be badly wrong."),
], "September 2026") + note("<strong>Do not write an MDR number into a pricing model.</strong> This site said that in Session 49 when the change was a proposal, and it is still the right advice with the notification published, because the rate is not notified. <strong>Do build the ability to apply a per-rail, per-ticket-size, per-merchant-category fee</strong> &mdash; that is a schema decision, it takes a sprint, and the alternative is discovering you need it in the week NPCI publishes the circular.")

a_builds = '''
<h3 id="s-amber-week">Accept UPI</h3>
<p><strong>Build:</strong> an aggregator integration, webhook signature verification over raw bytes, a
settlement-file reconciliation, and a fee engine that can price per rail and per ticket size.</p>
<p><strong>You get:</strong> UPI acceptance in days. <strong>You are a customer of this ecosystem</strong>,
and Build Sheet 05 is the page you want.</p>

<h3 id="s-amber-proper">Ship a UPI app on a sponsor bank</h3>
<p><strong>Build:</strong> sponsor bank agreement &rarr; SDK integration &rarr; <strong>UDIR</strong>
&rarr; deemed-state handling with its own screen and queue &rarr; decline mapping before launch &rarr;
data resident in India &rarr; a grievance route that reaches the PSP bank&rsquo;s mechanism.</p>
<p><strong>Trade:</strong> speed against a ceiling. You inherit the enabler&rsquo;s roadmap and their
certification, and you own the customer who is looking at a spinner.</p>

<h3 id="s-amber-big">Build the switch</h3>
<p><strong>Build:</strong> the whole transaction path, certified with NPCI, sized for peak, with
per-issuer decline telemetry, rolling three-month share measurement, an idempotent ledger keyed on
intent, and a fee engine waiting for a rate.</p>
<p><strong>It breaks when:</strong> the team optimises for the happy path. <strong>Success rate on a
good day is not the product.</strong> Behaviour during an issuer outage is, and it is the only thing
that is visible to NPCI, to your bank and to your customers simultaneously.</p>
''' + note("If you take one thing from this page: <strong>make &ldquo;deemed&rdquo; a real state in your schema today.</strong> Not a null, not a failure, not a retry. It costs a migration now and it is the difference between a bad hour and a double-debit incident with a dispute trail.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Customer debited twice</strong></td><td>An unknown outcome was retried with a fresh reference.</td><td>Reference derived from intent, stored before the call.</td></tr>
<tr><td><strong>&ldquo;Payment failed&rdquo; on a live debit</strong></td><td>Deemed mapped to failure in the UI.</td><td>Its own state, its own message, its own screen.</td></tr>
<tr><td><strong>Status polling worsens an outage</strong></td><td>Fixed-interval retries during an incident.</td><td>Exponential backoff, then hand to reconciliation.</td></tr>
<tr><td><strong>Real TD rate is invisible</strong></td><td>Unmapped decline codes in a catch-all bucket.</td><td>Map every code to technical or business before launch.</td></tr>
<tr><td><strong>Blaming your own switch for years</strong></td><td>Declines never split by issuer bank.</td><td>Plot TD per issuer. Escalate through the PSP bank.</td></tr>
<tr><td><strong>Complaints go nowhere</strong></td><td>Support inbox instead of UDIR.</td><td>Integrate UDIR. Eligible disputes are routed into it.</td></tr>
<tr><td><strong>Settlement off by a day, every day</strong></td><td>Aggregating on a UTC boundary.</td><td>IST, against NPCI cut-offs.</td></tr>
<tr><td><strong>Certification treated as a launch gate</strong></td><td>No capacity reserved for spec changes.</td><td>Standing engineering budget for re-certification.</td></tr>
<tr><td><strong>Cannot change banks</strong></td><td>Every customer&rsquo;s handle carries the suffix.</td><td>Negotiate the exit before signing the entry.</td></tr>
<tr><td><strong>No fee engine when the circular lands</strong></td><td>Six years of zero MDR encoded as an assumption.</td><td>Per-rail, per-ticket-size pricing in the schema now.</td></tr>
</table>
'''

SRC=[('official','NPCI roles and responsibilities of NPCI, PSP banks and TPAPs','the allocation published by PSP banks under NPCI requirement: NPCI owns and operates UPI, prescribes the rules, liabilities, settlement cut-offs and dispute protocol, approves participation and may audit participants directly or through a third party; the PSP bank audits the TPAP&rsquo;s app and systems, owns grievance redressal and answers for data residency; and both PSP bank and TPAP must store all UPI transaction data only in India.','https://www.npci.org.in'),
 ('official','Payment and Settlement Systems Act, 2007 and the Taxation and Other Laws (Amendment) Bill, 2026','the amendment removing the bar in section 10A, read with section 269SU of the Income-tax Act 1961, that had prevented any charge on BHIM-UPI, UPI-QR and RuPay debit payments since January 2020.','https://www.indiacode.nic.in'),
 ('official','Government notification of 14 September 2026 on MDR','the notified position that no charge applies to UPI transactions up to ₹2,000 or to RuPay debit, and that person-to-person transfers remain free. The notification does not fix the rate, the merchant threshold or the distribution of MDR income — those sit with the NPCI UPI and Services Steering Committee.','https://dfs.gov.in'),
 ('official','RBI turnaround time framework for failed transactions','the auto-reversal of failed debits with compensation payable per day of delay — the mechanism that eventually resolves a deemed transaction, and which does not help the customer in the ninety seconds they are looking at your screen.','https://www.rbi.org.in'),
 ('official','NPCI circular on the third-party application volume cap','the 30% limit on a single TPAP&rsquo;s share of UPI transaction volume proposed in November 2020, computed over the preceding three months on a rolling basis, enforced by halting new customer onboarding, with bank-owned apps outside its scope. Deadline moved from 2022 to 31 December 2024 and then to 31 December 2026.','https://www.npci.org.in'),
 ('official','NPCI dispute and decline framework','Unified Dispute and Issue Resolution as the ecosystem dispute protocol that partner applications are required to integrate, and the NPCI definitions and targets separating technical declines from business declines.','https://www.npci.org.in'),
 ('industry','UPI scale and MDR reporting, September 2026','24.51 billion transactions worth ₹29.82 lakh crore in August 2026; more than 24,000 crore transactions worth ₹314 lakh crore in 2025-26, up 30% by volume and 21% by value; transactions above ₹2,000 to merchants at about 4% of volume and roughly two thirds of value; discussed MDR rates of 0.25% to 0.4% against card MDRs of 1–3% credit and up to 0.9% debit; and the Steering Committee&rsquo;s expected meeting. Reporting, not notification — confirm every figure before use.',''),
 ('industry','UPI architecture and operations commentary','the practitioner read on sponsor-bank SDK routes, handle-suffix switching costs, deemed-transaction polling behaviour during incidents, and per-issuer decline variation. Directional.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. <strong>This page has the shortest shelf life of any on this site.</strong> The '
 'MDR notification is one day old, the rate is unnotified, and the volume cap is scheduled for 31 December '
 '2026 having been deferred three times. Verify all three before relying on them.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Aggregators, escrow, settlement files, and the economics of accepting payments.</p></a>
<a href="/fintech-ai/products/recurring-payments/" class="mod-card"><div class="mod-num">GUIDE 05</div><h3>Recurring Payments</h3><p>UPI AutoPay and the 2026 e-mandate framework, in full.</p></a>
<a href="/fintech-ai/products/cross-border-payments/" class="mod-card"><div class="mod-num">GUIDE 06</div><h3>Cross-Border Payments</h3><p>The other rail with a queue that arrives late and all at once.</p></a>
<a href="/fintech-ai/infrastructure/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 08</div><h3>Infrastructure</h3><p>Ledger correctness, the three data planes, and designing for reversibility.</p></a>
</div>
''' + warn("This page is a guide, not a specification. UPI participation is governed by NPCI circulars and procedural guidelines that are revised regularly and are authoritative over anything written here, and the MDR position changed the day before this page was published. Nothing here is legal advice. Work from the current NPCI documentation your PSP bank gives you, and confirm the MDR framework with your bank before pricing anything.")

lanes={'green':[("How to use this page",g_read),("What you are actually building",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 to 3 — shape, bank, certification",i_step123),
           ("Steps 4 and 5 — the payment path and the deemed state",i_step45),
           ("Steps 6 to 8 — disputes, settlement, running it",i_step68),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="UPI Switch Infrastructure: How to Build It"
META=("Build on UPI step by step: PSP banks and TPAP certification, the deemed state, technical "
      "declines, and what the September 2026 MDR notification changes.")
LEAD=("A step-by-step guide to building UPI infrastructure in India. Eight stages, the options at "
      "each one, exactly how each step connects to the next, real costs, and what breaks. Written "
      "for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/upi-switch",title=TITLE,meta=META,lead=LEAD,label="Product Guide 11",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/upi-switch/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m, "no <body>"
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t, "no page-hero"
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Building on the UPI '
  'rails themselves? PSP banks, NPCI certification, the deemed state, and what the September 2026 MDR '
  'notification changes: <a href="/fintech-ai/products/upi-switch/"><strong>UPI Switch Infrastructure: '
  'How to Build It &rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('payments-reconciliation', 'infrastructure'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/upi-switch' in src:
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
