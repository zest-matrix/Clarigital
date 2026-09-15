#!/usr/bin/env python3
# Session 71 — PRODUCT GUIDE 03: BNPL checkout
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product, start to finish. The
<a href="/fintech-ai/credit-underwriting/">Credit module</a> explains why underwriting is hard. The
<a href="/fintech-ai/credit-underwriting/build-sheet/">build sheet</a> lists the tools. This page
tells you which eight steps there are and how to connect them.</p>
''' + warn("<strong>Start with this, because it invalidates most BNPL designs people arrive with.</strong> The product you are probably imagining &mdash; a credit line, loaded into a wallet, spent at checkout &mdash; <strong>is not permitted in India</strong>. A 2022 RBI circular stopped prepaid instruments being loaded from credit lines, and the digital lending rules stopped money passing through platform accounts. Firms that had built that model pivoted or shut down. <strong>What is permitted is a fresh loan, sanctioned for each transaction, disbursed directly.</strong> Everything on this page follows from that.")

g_what = '''
<p>BNPL at checkout means: a customer buys something, a lender pays the merchant now, and the
customer repays the lender later in instalments.</p>
<p>In India that is <strong>digital lending</strong>. Not a payment method, not a wallet feature
&mdash; lending, governed by the <strong>RBI Digital Lending Directions, 2025</strong> (issued
8 May 2025), which consolidated the 2022 guidelines, the default loss guarantee framework and the
digital-channel outsourcing rules into one rulebook.</p>
<p><strong>Before you write any code, settle which of two things you are:</strong></p>
<table>
<tr><th>You are&hellip;</th><th>Which means</th></tr>
<tr><td><strong>The lender</strong></td><td>An NBFC. Registration with RBI, minimum Net Owned Fund <strong>&#8377;2 crore</strong>. Your balance sheet, your risk, your licence.</td></tr>
<tr><td><strong>An LSP</strong> &mdash; Lending Service Provider</td><td>You build the experience; a regulated entity lends. <strong>The RE remains accountable for everything you do</strong>, which shapes what they will let you ship.</td></tr>
</table>
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not a payment product.</strong> Calling it &ldquo;pay later&rdquo; does not move it out of
lending regulation.</li>
<li><strong>Not a credit line.</strong> Each purchase is a separate sanction.</li>
<li><strong>Not yours to hold.</strong> Money moves between the borrower's bank account and the
regulated entity. It does not pass through you.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Decide what you are</strong></td><td>NBFC or LSP. This is an architecture decision, not a legal footnote.</td></tr>
<tr><td>2</td><td><strong>Show the offer</strong></td><td>At checkout, in milliseconds, without promising anything you cannot deliver.</td></tr>
<tr><td>3</td><td><strong>The Key Fact Statement</strong></td><td>Before sanction. Every fee, one APR, legally binding.</td></tr>
<tr><td>4</td><td><strong>Sanction the loan</strong></td><td>A fresh loan, for this purchase, now.</td></tr>
<tr><td>5</td><td><strong>Move the money</strong></td><td>Directly. Never through your account.</td></tr>
<tr><td>6</td><td><strong>The cooling-off window</strong></td><td>They can walk away paying principal and proportionate APR only.</td></tr>
<tr><td>7</td><td><strong>Repayment</strong></td><td>And what happens the first time it fails.</td></tr>
<tr><td>8</td><td><strong>Collections</strong></td><td>Regulated speech, with a criminal-law floor underneath it.</td></tr>
</table>
''' + note("Steps 1, 3 and 6 are the ones product teams treat as paperwork. They are the three that decide whether the thing you built is legal. Step 8 is the one that decides whether you stay in business after your first bad cohort.")

code_offer = code('Python — step 2, the checkout offer, and what you must not promise', r'''# You have roughly 300ms at checkout. You also have a rule: do not show an
# offer you cannot honour. A declined customer at the payment screen is a lost
# sale AND a complaint, and "pre-approved" is a word with consequences.

def checkout_offer(customer, cart, limits):
    # 1. HARD GATES first. Cheap, deterministic, no model involved.
    if customer["age"] < 18:                    return decline("underage")
    if not customer["kyc_complete"]:            return decline("kyc_required")
    if cart["amount_paise"] > limits["max_ticket_paise"]:
        return decline("above_max_ticket")
    if customer["active_loans"] >= limits["max_concurrent"]:
        return decline("concurrent_limit")
    if customer["dpd"] > 0:                     return decline("existing_arrears")

    # 2. Only now, the risk decision -- INSIDE what the gates permit.
    score = risk_model(customer, cart)
    if score < limits["min_score"]:             return decline("risk")

    # 3. Language matters. "Eligible to apply" is a fact you can support.
    #    "Pre-approved" implies a sanction you have not made yet.
    return {
        "show": True,
        "wording": "Eligible to apply",          # NOT "pre-approved"
        "tenures": [t for t in limits["tenures"] if cart["amount_paise"] >= t["min_paise"]],
        "indicative_apr": indicative_apr(score),  # INDICATIVE. The KFS is binding.
        "quote_id": new_quote_id(),               # everything downstream ties to this
        "expires_at": now() + minutes(15),
    }

def decline(reason):
    # A decline at checkout is a product event, not an error. Never show the
    # reason to the customer at this point -- but always store it.
    return {"show": False, "reason": reason}

# WHAT TO CHECK
# [ ] hard gates run BEFORE the model. They are cheap, they are auditable, and
#     they keep the model out of decisions that were never its to make
# [ ] the word on the button is a compliance decision. "Pre-approved" before a
#     sanction is a promise. Get the wording signed off, not chosen by design
# [ ] indicative APR is labelled indicative EVERYWHERE, including in analytics.
#     The KFS number is the binding one and they can differ
# [ ] quote_id threads through KFS, sanction, disbursal and repayment. When
#     something goes wrong at step 7 you will reconstruct from this
# [ ] decline reasons are STORED even though they are not shown. The
#     distribution is your best early signal that a gate is mis-set
# [ ] the offer expires. An indicative rate from three hours ago is not an offer
# [ ] latency budget is real: at 300ms, a model that takes 400ms is a decline
''')

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Decide what you are</h3>
<p>Almost every other decision follows from this one, so make it first and write it down.</p>
<table>
<tr><th>Route</th><th>What you need</th><th>Trade</th></tr>
<tr><td><strong>Become an NBFC</strong></td><td>RBI registration, <strong>&#8377;2 crore</strong> Net Owned Fund, capital adequacy, your own reporting.</td><td>Full control. Months of process and a permanent compliance function.</td></tr>
<tr><td><strong>Be an LSP for a regulated entity</strong></td><td>A partnership agreement, and the RE's approval of your flows.</td><td>Fast to start. <strong>The RE is accountable for what you build</strong>, so they will constrain it &mdash; and they are right to.</td></tr>
<tr><td><strong>Merchant-funded, no credit</strong></td><td>Nothing. The merchant discounts instead of lending.</td><td>Not BNPL. Worth naming because it is sometimes the honest answer to what the business actually wants.</td></tr>
</table>
''' + warn("<strong>The default loss guarantee is where LSP deals get interesting, and it has moved.</strong> A DLG between an RE and an LSP is capped at <strong>5% of the outstanding portfolio</strong>, must be backed by <strong>cash deposit, bank guarantee or lien-marked fixed deposit</strong> &mdash; <strong>a corporate guarantee is not eligible</strong> &mdash; and needs a board-approved policy at the RE plus explicit disclosure to the borrower that no service depends on it. In <strong>February 2026</strong> the RBI allowed NBFCs to recognise DLG when computing Expected Credit Loss again, provided the DLG is <em>integral to the loan structure</em> rather than bolted on, with ECL recomputed whenever it is used or invoked. If your commercial model rests on a DLG, that change is the difference between the deal working and not.") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; Show the offer</h3>
''' + code_offer + '''
<p><strong>The gotcha nobody documents:</strong> the word on the button. &ldquo;Pre-approved&rdquo;
reads as a decision already made, and a customer who is then declined has been told two different
things by the same company. <strong>&ldquo;Eligible to apply&rdquo; is a statement you can support at
every stage.</strong> It converts slightly worse and it removes a whole class of complaint. Treat the
wording as a compliance artefact, get it signed off, and do not let it be A/B tested into something
stronger.</p>
'''

code_kfs = code('Python — step 3, the Key Fact Statement', r'''from decimal import Decimal, ROUND_HALF_UP

# The KFS is shown BEFORE sanction and it is the single source of truth. If an
# interface says 10% and the KFS says 14% APR, the KFS is what binds. EVERY fee
# goes in it -- processing, platform, insurance premium, anything.

def build_kfs(quote, loan, fees, tenure):
    P = Decimal(loan["principal_paise"])
    total_fees = sum(Decimal(f["paise"]) for f in fees)

    # APR must include the fees. A rate quoted on principal alone while fees are
    # charged separately is the oldest trick in consumer credit and it is
    # exactly what the KFS exists to stop.
    apr = compute_apr(principal=P, fees=total_fees,
                      instalments=tenure["instalments"],
                      frequency=tenure["frequency"])

    return {
        "quote_id": quote["quote_id"],
        "lender_name": loan["regulated_entity"],   # the RE, not your brand
        "lsp_name": loan.get("lsp"),               # named separately if there is one
        "principal": P,
        "fees": [{"name": f["name"], "amount": f["paise"]} for f in fees],
        "total_fees": total_fees,
        "apr_percent": apr.quantize(Decimal("0.01"), ROUND_HALF_UP),
        "instalments": tenure["instalments"],
        "instalment_amount": instalment_amount(P, total_fees, apr, tenure),
        "total_repayable": P + total_fees + interest_total(P, apr, tenure),
        "cooling_off_days": loan["cooling_off_days"],
        "cooling_off_terms": "Exit by paying principal plus proportionate APR. "
                             "No prepayment penalty.",
        "grievance_officer": loan["grievance_contact"],
        "recovery_agent_policy_url": loan["recovery_policy_url"],
        "issued_at": now_ist(),
    }

# WHAT TO CHECK
# [ ] the KFS is rendered and ACKNOWLEDGED before sanction, not alongside it.
#     Order matters and it is checkable from your own logs
# [ ] APR includes every fee. If a fee exists anywhere in the journey and is not
#     in the KFS, the KFS is wrong
# [ ] the REGULATED ENTITY is named as the lender. A borrower who thinks your
#     brand lent them the money cannot exercise their rights against the RE
# [ ] store the exact rendered KFS, not the inputs. "What did they see" is the
#     question, and re-rendering from today's fee table will not answer it
# [ ] a changed credit limit or changed terms needs a FRESH KFS
# [ ] integer paise. Never floats. Rounding on an APR is a regulatory number
# [ ] the grievance route and the recovery-agent policy are on the document,
#     not one click away
''')

i_step34 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; The Key Fact Statement</h3>
<p><strong>What it does:</strong> tells the customer, before they are committed, exactly what this
will cost.</p>
''' + code_kfs + '''
<p><strong>The gotcha nobody documents:</strong> store the rendered document, not the inputs. Teams
store the loan parameters and plan to regenerate the KFS if anyone asks. Six months later the fee
schedule has changed, the template has changed, and the regenerated document is not what the customer
saw. <strong>The question is always &ldquo;what did they see&rdquo;, and only the artefact answers
it.</strong> It is a few kilobytes. Keep it.</p>

<h3 id="s-indigo-s4">Step 4 &mdash; Sanction the loan</h3>
<p><strong>A fresh loan, for this purchase.</strong> Not a draw on a line, because a line loaded into
a prepaid instrument is the model that was stopped in 2022.</p>
<p>Practically this means your sanction path runs inside the checkout, at checkout latency, for every
single transaction &mdash; which is the main engineering difference between BNPL and ordinary
lending. Budget for it: idempotency on the sanction call, a clear timeout policy, and a defined
answer to <em>&ldquo;the sanction timed out and we do not know if it happened&rdquo;</em>. That is the
same unknown-state problem as payouts in
<a href="/fintech-ai/payments-reconciliation/build-sheet/">Build Sheet 05</a>, and the same rule
applies: a timeout is not a failure, it is a question you must go and ask.</p>
'''

code_flow = code('Python — step 5, the money, and the account you must not have', r'''# THE RULE: disbursal and repayment flow between the BORROWER'S BANK ACCOUNT
# and the REGULATED ENTITY. Not through the LSP. Not through a platform account.
# Not through any intermediary "pool" account. There is no clever structure.

def disburse(sanction, merchant, re_client):
    # The lender pays the merchant. You instruct; you do not hold.
    instruction = {
        "from": "REGULATED_ENTITY_ACCOUNT",      # the RE's own account
        "to": merchant["settlement_account"],
        "amount_paise": sanction["principal_paise"],
        "reference": sanction["loan_id"],
        "idempotency_key": f"disb:{sanction['loan_id']}",   # intent, not attempt
    }
    assert instruction["from"] != "PLATFORM_ACCOUNT", \
        "money must not pass through the platform"
    return re_client.disburse(instruction)

def collect(loan, instalment, re_client):
    # Repayment goes borrower -> RE. An e-mandate on the borrower's account,
    # presented by the RE. Again: you instruct, you do not receive.
    return re_client.present_mandate({
        "mandate_id": loan["mandate_id"],
        "amount_paise": instalment["amount_paise"],
        "due_date": instalment["due_date"],
        "idempotency_key": f"coll:{loan['loan_id']}:{instalment['seq']}",
    })

# WHAT TO CHECK
# [ ] there is NO account in your architecture that briefly holds borrower money.
#     If one exists "for reconciliation convenience", that is the finding
# [ ] idempotency keys derive from the loan and instalment, never from a uuid4
#     per attempt. Paying a merchant twice is recoverable; collecting twice from
#     a borrower is a complaint and a refund and a trust problem
# [ ] a timeout on disbursal is UNKNOWN, not failed. Query by your own reference
# [ ] the merchant settlement account is verified before the first disbursal,
#     not after the first misdirected payment
# [ ] mandate failures are a FIRST-CLASS path with their own state machine, not
#     an exception. They are routine, not exceptional
# [ ] reconcile disbursals against sanctions daily. A disbursal with no sanction
#     is the most serious break available here
''')

i_step56 = '''
<h3 id="s-indigo-s5">Step 5 &mdash; Move the money</h3>
''' + code_flow + '''
<p><strong>The gotcha nobody documents:</strong> the pool account. Almost every payments architecture
has one, because it makes reconciliation easier. In digital lending it is the thing that is
specifically not allowed, and it is usually introduced by an engineer solving a genuine problem
without knowing it is a regulated boundary. <strong>Put the constraint in code, as an assertion, on
day one.</strong> It costs one line and it stops a design decision that is very expensive to
unwind.</p>

<h3 id="s-indigo-s6">Step 6 &mdash; The cooling-off window</h3>
<p><strong>What it does:</strong> lets the borrower exit, paying <strong>principal plus proportionate
APR only</strong>, with <strong>no prepayment penalty</strong>.</p>
<p>Three things teams get wrong:</p>
<ul>
<li><strong>They make it hard to find.</strong> If exiting requires calling support, the window
exists on paper only.</li>
<li><strong>They charge the processing fee anyway.</strong> Proportionate APR means proportionate.
A fee retained on exit is the fee the window was meant to protect against.</li>
<li><strong>They forget the merchant side.</strong> If the customer exits the loan but the goods have
shipped, somebody has to reconcile that &mdash; and it should be decided before launch, not during
the first case.</li>
</ul>
'''

code_coll = code('Python — steps 7 and 8, repayment failure and the line you must not cross', r'''from datetime import time, datetime, timedelta, timezone
IST = timezone(timedelta(hours=5, minutes=30))

# A failed instalment is routine. How you behave in the next 48 hours is where
# BNPL firms get into regulatory trouble.

def on_mandate_failure(loan, instalment, reason):
    # 1. Distinguish CANNOT PAY from DID NOT PAY. They need opposite responses
    #    and the same dashboard treats them identically.
    if reason in ("insufficient_funds",):
        path = "retry_with_notice"       # tell them BEFORE re-presenting
    elif reason in ("mandate_revoked", "account_closed"):
        path = "contact_required"
    else:
        path = "technical_retry"         # our problem, not theirs

    return {"path": path, "notify_before_retry": True,
            "retry_not_before": datetime.now(IST) + timedelta(days=1)}

# Contact rules are HARD GATES, not guidance. Same shape as Build Sheet 06.
WINDOW = (time(8, 0), time(19, 0))

def may_contact(account, channel, now=None):
    now = now or datetime.now(IST)
    t = now.timetz().replace(tzinfo=None)
    if not (WINDOW[0] <= t <= WINDOW[1]):
        return {"allow": False, "why": "outside_0800_1900_IST"}   # DIGITAL TOO
    if account.grievance_open:
        return {"allow": False, "why": "recovery_suspended_grievance_pending"}
    if account.hardship_flag:
        return {"allow": False, "why": "hardship", "action": "human_review"}
    if account.contacts_today(channel) >= account.cap(channel):
        return {"allow": False, "why": "frequency_cap"}
    return {"allow": True, "must_record": channel == "voice"}

# WHAT TO CHECK
# [ ] the window covers SMS, WhatsApp and push, not just calls. The scheduler is
#     where this is usually missing, because the dialler is the obvious place
# [ ] NEVER access contacts, call logs or media files. Prohibited outright.
#     Camera, microphone and location need explicit consent and nothing else
# [ ] no social shaming, ever. Contacting anyone other than the borrower about
#     the debt is where this stops being a compliance matter
# [ ] outsourcing collections does not outsource liability. Audit the agency's
#     logs; an assurance is not evidence
# [ ] a hardship flag raised anywhere -- including in support -- pauses
#     collections. Different vendors and different databases is the usual cause
#     of a technically compliant message that is indefensible in substance
# [ ] all digital lending data stored EXCLUSIVELY IN INDIA
''')

i_step78 = '''
<h3 id="s-indigo-s7">Steps 7 and 8 &mdash; Repayment, and collections</h3>
''' + code_coll + '''
<p><strong>The gotcha nobody documents:</strong> the phone permissions. A lending app may request
camera, microphone and location with explicit consent. <strong>Contacts, call logs and media files
are prohibited outright</strong> &mdash; no consent makes them acceptable. This is not a privacy
nicety; it is the specific abuse the rule was written to end, and an app that requests contacts is
making a statement about itself that a supervisor will read exactly as intended.</p>
'''

i_cost = registry("BNPL checkout &mdash; what it costs", [
 ("Becoming an NBFC", "direct",
  "<strong>&#8377;2 crore</strong> minimum Net Owned Fund, plus the registration process, plus a "
  "permanent compliance function. Months, not weeks."),
 ("LSP route", "direct",
  "No licence cost. The price is <strong>commercial</strong> &mdash; the RE's share, and the "
  "<strong>DLG you post: capped at 5% of the outstanding portfolio</strong>, in cash, bank guarantee "
  "or lien-marked FD. <strong>That capital is tied up</strong>, and a corporate guarantee will not "
  "substitute for it."),
 ("Underwriting data", "direct",
  "Bureau pulls, alternative data, Account Aggregator fetches. Per-call, and it runs on every "
  "checkout rather than every application &mdash; the volume is much higher than ordinary lending."),
 ("Payments", "direct",
  "Disbursal to the merchant and e-mandate presentation for collection. See "
  "<a href=\"/fintech-ai/payments-reconciliation/build-sheet/\">Build Sheet 05</a>."),
 ("Collections", "direct",
  "<strong>The line that decides whether the book is profitable.</strong> People, tooling, and "
  "recording. Regulated conduct means it cannot be optimised the way an ordinary contact centre can."),
 ("Credit loss", "direct",
  "<strong>Not a cost line, the cost line.</strong> Every other number on this page is small next to "
  "what you lose on the loans that do not repay, and it is the one number a vendor cannot quote you."),
], "September 2026") + warn("<strong>Model the unit economics on a COHORT, not a transaction.</strong> A BNPL transaction looks profitable on day one and is only actually profitable once that cohort has finished repaying. Firms that grew on transaction-level margin and discovered cohort-level losses twelve months later are the single most common failure pattern in this product category, in every market it has existed in.")

a_builds = '''
<h3 id="s-amber-week">The honest starting version</h3>
<p><strong>Build:</strong> LSP partnership with one regulated entity &rarr; hard gates plus a simple
scorecard &rarr; a properly rendered and stored KFS &rarr; sanction per transaction &rarr; disbursal
and collection through the RE &rarr; a cooling-off exit that a customer can find without calling
anyone &rarr; collections by hand, inside the contact window, with everything logged.</p>
<p><strong>You get:</strong> a compliant product you can learn from.</p>
<p><strong>It breaks when:</strong> volume outruns manual collections &mdash; which happens sooner
than you expect, because arrears arrive all at once.</p>

<h3 id="s-amber-proper">The proper version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; two REs so one partner's risk appetite does
not cap your product &rarr; a real underwriting stack with challenger models &rarr; cohort-level
unit economics reported weekly &rarr; a collections platform with the contact window enforced
<em>in code</em> &rarr; a hardship flag shared between support and collections &rarr; the DLG modelled
as tied-up capital rather than a marketing cost.</p>
<p><strong>Trade:</strong> you own the risk model and the collections conduct. Both are things you
cannot outsource the consequences of.</p>

<h3 id="s-amber-big">The version that owns the balance sheet</h3>
<p><strong>Build:</strong> your own NBFC, your own capital, your own reporting, plus everything
above.</p>
<p><strong>It breaks when:</strong> you do it before you have a year of repayment data. The licence is
the easy part; knowing what your book actually does is not.</p>
''' + note("If you take one thing from this page: <strong>settle step 1 before you design step 2.</strong> NBFC or LSP changes the money flow, the KFS wording, who the borrower's rights run against, and who signs off on your button text. Teams that design the checkout first and pick the structure later rebuild the checkout.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>The model is a credit line</strong></td><td>It is the intuitive design and it is the one that was stopped.</td><td>Fresh sanction per transaction.</td></tr>
<tr><td><strong>Money passes through a platform account</strong></td><td>An engineer added a pool account to make reconciliation easier.</td><td>Assert against it in code on day one.</td></tr>
<tr><td><strong>The KFS cannot be reproduced</strong></td><td>Inputs were stored, not the document.</td><td>Store the rendered artefact.</td></tr>
<tr><td><strong>&ldquo;Pre-approved&rdquo; then declined</strong></td><td>Marketing wording on a pre-sanction screen.</td><td>&ldquo;Eligible to apply&rdquo;, signed off, not A/B tested.</td></tr>
<tr><td><strong>Cooling-off exists but nobody uses it</strong></td><td>It requires calling support.</td><td>Put it in the app, one tap, no fee retained.</td></tr>
<tr><td><strong>An SMS goes out at 22:00</strong></td><td>The window was built on the dialler, not the scheduler.</td><td>Gate every channel, at send time, in IST.</td></tr>
<tr><td><strong>The app asks for contacts</strong></td><td>Copied from an older lending app.</td><td>Prohibited outright. Remove the permission.</td></tr>
<tr><td><strong>Profitable per transaction, loss-making per cohort</strong></td><td>Margin measured at sale, losses arrive later.</td><td>Cohort reporting from week one.</td></tr>
</table>
'''

SRC=[('official','RBI Digital Lending Directions, 2025 (8 May 2025)','the consolidated framework replacing the 2022 guidelines, the default loss guarantee framework and digital-channel outsourcing rules.','https://www.rbi.org.in'),
 ('official','RBI Master Direction on Prepaid Payment Instruments','the 2022 restriction that PPIs may not be loaded from credit lines — the rule that ended the original BNPL model.','https://www.rbi.org.in'),
 ('official','RBI — Default Loss Guarantee framework','the 5% cap, the eligible forms of cover, the exclusion of corporate guarantees, and the February 2026 change allowing DLG in ECL for NBFCs where it is integral to the loan structure.','https://www.rbi.org.in'),
 ('official','RBI — NBFC registration','the ₹2 crore minimum Net Owned Fund for new applications.','https://www.rbi.org.in'),
 ('official','DPDP Act, 2023','consent, purpose limitation, India-only storage and the penalty ceiling.','https://www.meity.gov.in'),
 ('industry','Digital lending compliance reporting','the KFS contents, cooling-off mechanics and permission restrictions as summarised by practitioners. Verify against the Directions before relying on any specific figure.','')]
_src=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_src,_re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'+(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. The DLG treatment changed in February 2026; the date is part of the claim.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/credit-underwriting/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 02</div><h3>Credit &amp; Underwriting</h3><p>The scorecard behind step 2, and the hybrid architecture that keeps the model inside the rules.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>Disbursal, e-mandates, and the timeout-is-not-a-failure rule step 4 depends on.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 06</div><h3>Customer Operations</h3><p>Collections as regulated speech, with the contact guard written out in full.</p></a>
<a href="/fintech-ai/products/video-kyc/" class="mod-card"><div class="mod-num">GUIDE 02</div><h3>Video KYC</h3><p>How the customer at step 2 got verified in the first place.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Digital lending is a licensed activity and the conduct rules carry consequences well beyond a fine. Nothing here is legal advice. Have your structure, your KFS, your money flow and your collections process reviewed by qualified counsel before a real borrower sees a checkout button.")

lanes={'green':[("How to use this page",g_read),("What BNPL actually is in India",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — what you are, and the offer",i_step12),("Steps 3 and 4 — the KFS and the sanction",i_step34),
           ("Steps 5 and 6 — the money and the exit",i_step56),("Steps 7 and 8 — repayment and collections",i_step78),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="BNPL Checkout: How to Build It"
META=("Build a BNPL checkout product step by step: the eight stages, your options at each one, how to "
      "connect them, and what RBI permits.")
LEAD=("A step-by-step guide to building a BNPL checkout product in India. Eight stages, the options at "
      "each one, exactly how each step connects to the next, real costs, and what breaks. Written for "
      "someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/bnpl-checkout",title=TITLE,meta=META,lead=LEAD,label="Product Guide 03",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/bnpl-checkout/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: _io.open(f,'w',encoding='utf-8').write(h.replace('</style>',CSSRC+'\n</style>',1))
