#!/usr/bin/env python3
# Session 73 — PRODUCT GUIDE 05: Recurring payments (e-mandates)
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one capability, start to finish: charging a customer
repeatedly, automatically, with their permission. Subscriptions, SIPs, insurance premiums, loan
instalments.</p>
<p>It feeds every product that bills more than once.</p>
''' + warn("<strong>The rules changed on 21 April 2026 and most published guidance is out of date.</strong> The RBI's <strong>Digital Payments &mdash; E-mandate Framework, 2026</strong> (Circular RBI/DPSS/2026-27/396) <strong>consolidated eight earlier circulars into one rulebook</strong>, effective immediately. If you are reading an integration guide that cites the 2019 or 2021 circulars as current, it is describing a framework that no longer exists.")

g_what = '''
<p>An e-mandate is a standing permission: the customer authenticates <strong>once</strong>, and you
may then debit them repeatedly within agreed limits, without asking again each time.</p>
<p>The 2026 framework covers <strong>credit cards, debit cards, prepaid instruments and UPI</strong>,
for <strong>domestic and cross-border</strong> recurring transactions. Three rails, one rulebook.</p>
<table>
<tr><th>Rail</th><th>What it is</th><th>Best for</th></tr>
<tr><td><strong>Card e-mandate</strong></td><td>Standing instruction against a card.</td><td>Subscriptions, international customers, higher ticket sizes.</td></tr>
<tr><td><strong>UPI AutoPay</strong></td><td>Mandate against a UPI ID, approved in the customer's UPI app.</td><td>Consumer India. Highest reach, lowest friction to register.</td></tr>
<tr><td><strong>eNACH</strong></td><td>Standing instruction registered directly against a bank account.</td><td>Loan EMIs, larger amounts, customers without cards.</td></tr>
</table>
''' + note("<strong>UPI AutoPay runs under the same framework as card mandates.</strong> The pre-debit notification requirement and the AFA thresholds apply identically. The payment instrument changes; the compliance obligation does not. That matters when you build &mdash; one set of rules, three integrations, and it is tempting to build three different rule implementations by accident.") + '''
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not a stored card.</strong> A saved card you charge is not a mandate, and charging one
recurringly without a registered mandate is the thing this framework exists to stop.</li>
<li><strong>Not permanent.</strong> Every mandate has a validity period the customer can change.</li>
<li><strong>Not retryable like a normal decline.</strong> See step 6 &mdash; this is the part teams
get most wrong.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Pick the rail</strong></td><td>Card, UPI AutoPay, or eNACH. Often more than one.</td></tr>
<tr><td>2</td><td><strong>Register the mandate</strong></td><td>One authentication, up front. Get this right or nothing else runs.</td></tr>
<tr><td>3</td><td><strong>Store what you may debit</strong></td><td>Amount, cap, frequency, validity. This is your permission, in a row.</td></tr>
<tr><td>4</td><td><strong>Notify, 24 hours before</strong></td><td>Mandatory. Amount, date, merchant name.</td></tr>
<tr><td>5</td><td><strong>Present the debit</strong></td><td>With or without AFA, depending on amount and category.</td></tr>
<tr><td>6</td><td><strong>When it fails</strong></td><td>Diagnose the mode. Do not send everyone the same email.</td></tr>
<tr><td>7</td><td><strong>Confirm, after</strong></td><td>Post-debit notification, with the grievance route on it.</td></tr>
<tr><td>8</td><td><strong>Modify, pause, revoke, reissue</strong></td><td>The customer is in control, and cards get replaced.</td></tr>
</table>
''' + note("Steps 4, 6 and 7 are where the money is. Registration is a one-off engineering problem; <strong>collection is an operational one you will run forever</strong>, and the difference between a good and a bad implementation of step 6 is worth more than everything else on this page combined.")

code_limits = code('Python — steps 3 and 5, the limits, and the exception everyone gets wrong', r'''from decimal import Decimal

# AFA (Additional Factor of Authentication -- usually OTP or UPI PIN) is
# ALWAYS required for: registration, modification, withdrawal, the FIRST
# transaction, a customer opt-out, and any debit above the threshold.
#
# After registration, recurring debits run without AFA UP TO A LIMIT.

GENERAL_LIMIT = Decimal("15000")      # per recurring transaction

# The higher limit applies to EXACTLY THREE CATEGORIES. This is the most
# misreported rule in the whole framework.
ENHANCED_LIMIT = Decimal("100000")
ENHANCED_CATEGORIES = {
    "INSURANCE_PREMIUM",
    "MUTUAL_FUND_SIP",
    "CREDIT_CARD_BILL",
}
# NOT INCLUDED: loan EMIs. Not personal loans, not BNPL instalments, not auto
# loans. An EMI above Rs 15,000 needs AFA on every single debit, and a lending
# product built on the assumption of Rs 1 lakh headroom will fail at collection
# for exactly the customers whose instalments matter most.

def needs_afa(mandate, amount: Decimal, is_first: bool) -> dict:
    if is_first:
        return {"afa": True, "why": "first_transaction"}
    limit = (ENHANCED_LIMIT if mandate["category"] in ENHANCED_CATEGORIES
             else GENERAL_LIMIT)
    if amount > limit:
        return {"afa": True, "why": "above_threshold", "limit": limit}
    if amount > mandate["max_amount"]:
        # The CUSTOMER's own cap, set at registration for variable amounts.
        # Separate from the regulatory limit and often lower.
        return {"afa": False, "blocked": True, "why": "exceeds_customer_cap"}
    return {"afa": False}

# WHAT TO CHECK
# [ ] ENHANCED_CATEGORIES is a closed set in code, not a config someone can
#     widen. Adding "LOAN_EMI" to it is a one-line compliance breach
# [ ] the customer's own cap is enforced separately from the regulatory limit,
#     and a debit exceeding it is BLOCKED, not escalated to AFA
# [ ] amounts in Decimal or integer paise. Never float
# [ ] "first transaction" means first under THIS mandate, not first ever for
#     this customer. A re-registered mandate has a new first transaction
# [ ] validity period is stored and enforced. A debit after expiry is
#     unauthorised, and customer liability rules then apply to you
# [ ] issuers may NOT charge the customer for the e-mandate facility. If a fee
#     appears anywhere in your flow, it is yours to absorb, not theirs
''')

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Pick the rail</h3>
<p>Most products end up on two. Cards for reach and international, UPI AutoPay for Indian consumer
volume, eNACH for larger recurring amounts and customers without cards.</p>
<p><strong>The useful design decision:</strong> build the rails behind one internal mandate model, so
your business logic never branches on rail. The framework treats them identically; your code should
too. Teams that build three separate implementations end up with three slightly different
interpretations of the same rule, and the differences surface as compliance gaps rather than bugs.</p>

<h3 id="s-indigo-s2">Step 2 &mdash; Register the mandate</h3>
<p><strong>One AFA, up front.</strong> A 3DS flow on cards, a UPI PIN in the customer's UPI app, or
the bank's flow for eNACH.</p>
<p>Two things worth building properly at registration, because retrofitting them is painful:</p>
<ul>
<li><strong>Capture the customer's preferred notification channel.</strong> They choose SMS or email,
and you owe them a notification before every debit. Ask once, at registration.</li>
<li><strong>Set the variable-amount cap explicitly.</strong> If the amount can change, the customer
sets an upper limit. Make that a deliberate field in your flow rather than a default you chose.</li>
</ul>

<h3 id="s-indigo-s3">Steps 3 and 5 &mdash; What you may debit</h3>
''' + code_limits + '''
''' + warn("<strong>The &#8377;1 lakh exception covers insurance premiums, mutual fund subscriptions and credit card bills. It does NOT cover EMIs.</strong> This is the single most misreported line in the framework, and it is repeated confidently in a lot of published guidance. <strong>A loan instalment above &#8377;15,000 requires AFA on every debit.</strong> If you are building lending collections on the assumption of &#8377;1 lakh of headroom, your collection rate will fall off a cliff at exactly the ticket sizes that matter most to the book.")

code_notify = code('Python — step 4, the notification that is a hard gate', r'''from datetime import datetime, timedelta, timezone
IST = timezone(timedelta(hours=5, minutes=30))

# 24 hours before EVERY debit. Not a courtesy -- a condition of debiting.
# It must carry the amount, the debit date and the merchant name, and it goes
# on the channel the customer chose at registration.

NOTIFY_LEAD = timedelta(hours=24)
# The only carve-out: auto-replenishment of FASTag and NCMC balances.
EXEMPT = {"FASTAG_REPLENISH", "NCMC_REPLENISH"}

def schedule_pre_debit(mandate, instalment):
    if mandate["category"] in EXEMPT:
        return {"required": False}
    send_at = instalment["debit_at"] - NOTIFY_LEAD
    return {
        "required": True,
        "send_at": send_at,
        "channel": mandate["notify_channel"],        # chosen at registration
        "content": {
            "amount": instalment["amount"],
            "debit_date": instalment["debit_at"].astimezone(IST).date().isoformat(),
            "merchant_name": mandate["merchant_display_name"],
            "opt_out_url": opt_out_link(mandate, instalment),   # AFA-protected
        },
    }

def may_debit(instalment) -> dict:
    # The gate. A debit whose notification did not go out 24h earlier is not
    # a debit you are entitled to present.
    n = instalment.get("pre_debit_notification")
    if instalment["category"] in EXEMPT:
        return {"allow": True}
    if not n or n["status"] != "delivered":
        return {"allow": False, "why": "pre_debit_notification_not_delivered"}
    if instalment["debit_at"] - n["delivered_at"] < NOTIFY_LEAD:
        return {"allow": False, "why": "notification_too_late"}
    if instalment.get("customer_opted_out"):
        return {"allow": False, "why": "opted_out_for_this_debit"}
    return {"allow": True}

# WHAT TO CHECK
# [ ] may_debit() runs at PRESENTATION time, not at scheduling time. A
#     notification that failed to deliver overnight must stop the debit
# [ ] "delivered", not "sent". A queued SMS is not a notification
# [ ] the opt-out link is AFA-protected and works for a SINGLE debit as well as
#     the whole mandate. Both are required and teams usually build only the second
# [ ] the merchant name in the notification is the name the customer RECOGNISES,
#     not your legal entity. Unrecognised names drive chargebacks and complaints
# [ ] a moved debit date needs a fresh 24-hour notification. Rescheduling does
#     not inherit the old one
# [ ] notification delivery is logged per instalment. In a dispute this is the
#     evidence that you were entitled to debit at all
''')

i_step4 = '''
<h3 id="s-indigo-s4">Step 4 &mdash; Notify, 24 hours before</h3>
''' + code_notify + '''
<p><strong>The gotcha nobody documents:</strong> the notification is a <em>gate</em>, not a message.
Teams build it as a fire-and-forget alert on the scheduler and never wire the result back into the
debit decision. If the SMS bounced, the number changed, or the queue backed up overnight, the debit
should not go out &mdash; and in a dispute the delivery log is what proves you were entitled to
present it. <strong>Check delivery at presentation time, not at scheduling time.</strong></p>
'''

code_fail = code('Python — step 6, the part that decides your recovery rate', r'''# A mandate failure is NOT a retryable soft decline. Retrying it is pointless:
# the mandate itself is the problem, and only the customer can fix it.
#
# THREE FAILURE MODES, THREE DIFFERENT CUSTOMER ACTIONS. Sending the same
# "update your payment method" email to all three routes people to the wrong
# action and collapses recovery.

RECOVERY = {
    "mandate_missing_or_cancelled": {
        "customer_action": "re-register the mandate",
        "how": {"CARD": "3DS authentication", "UPI": "approve in your UPI app",
                "ENACH": "re-authorise with your bank"},
        "retryable_without_customer": False,
    },
    "above_threshold": {
        "customer_action": "approve this one payment",
        "how": {"CARD": "OTP for this transaction", "UPI": "UPI PIN for this transaction",
                "ENACH": "authorise this debit"},
        "retryable_without_customer": False,
        "note": "the mandate is fine; this single amount needs AFA",
    },
    "pre_debit_notification_failed": {
        "customer_action": "confirm in your banking app before the next attempt",
        "retryable_without_customer": False,
    },
    "insufficient_funds": {
        "customer_action": "add funds",
        "retryable_without_customer": True,        # the ONLY genuinely retryable one
        "retry_after_days": 3,
    },
}

def recovery_plan(failure, mandate):
    plan = RECOVERY.get(failure["code"])
    if not plan:
        return {"path": "human_review", "code": failure["code"]}
    msg = plan["customer_action"]
    how = plan.get("how", {}).get(mandate["rail"])
    return {"tell_customer": f"{msg}" + (f" — {how}" if how else ""),
            "auto_retry": plan["retryable_without_customer"],
            # If card re-registration goes unanswered, offer UPI AutoPay. It is
            # a lower-friction registration and recovers subscribers that a
            # second 3DS attempt will not.
            "fallback_rail": "UPI" if mandate["rail"] == "CARD" else None}

# WHAT TO CHECK
# [ ] mandate failures are a DISTINCT failure class in your dunning logic, not
#     lumped in with card declines. They behave nothing alike
# [ ] the message names the specific action. "Update your payment method" is
#     wrong for two of the three modes
# [ ] auto-retry ONLY on insufficient funds, and with notice before re-presenting
# [ ] offer UPI AutoPay as a fallback when card re-registration goes unanswered.
#     Different friction, different success rate, same framework
# [ ] measure recovery rate PER FAILURE MODE. A blended number hides that one of
#     the three is broken
# [ ] a failure never silently stops the subscription. It starts a defined
#     sequence with an end state
''')

i_step678 = '''
<h3 id="s-indigo-s6">Step 6 &mdash; When it fails</h3>
''' + code_fail + '''
<p><strong>The gotcha nobody documents, and the most expensive one on this page:</strong> a mandate
failure is not a soft decline. Ordinary card declines are retryable &mdash; the issuer might approve
tomorrow. A mandate failure means the <em>permission</em> is broken, and no number of retries will
fix it. Only the customer can, and <strong>the action they must take is different in each of the
three modes</strong>. Most billing systems send one generic email to all of them, which routes people
to the wrong action and quietly destroys the recovery rate. Splitting that one message into three is
probably the highest-return change available in this entire product area.</p>

<h3 id="s-indigo-s7">Step 7 &mdash; Confirm, after</h3>
<p>A post-debit notification after <strong>every</strong> automated collection, carrying the
grievance redressal route. The framework is explicit that the grievance mechanism must be
<em>disclosed in the notification</em> and must actually work for recurring-transaction disputes
&mdash; not a generic support link.</p>
<p>The RBI's customer-liability rules for unauthorised transactions apply here too. A debit the
customer did not authorise is not a billing dispute; it is an unauthorised transaction with clocks
attached.</p>

<h3 id="s-indigo-s8">Step 8 &mdash; Modify, pause, revoke, reissue</h3>
<table>
<tr><th>Event</th><th>What must be possible</th></tr>
<tr><td><strong>Modify</strong></td><td>Amount cap or validity period, by the customer, with AFA.</td></tr>
<tr><td><strong>Pause</strong></td><td>Without cancelling. Build it; customers who cannot pause, cancel.</td></tr>
<tr><td><strong>Revoke</strong></td><td>At any point, with AFA. Immediate effect on the next debit.</td></tr>
<tr><td><strong>Opt out of one debit</strong></td><td>A single skipped payment, not the whole mandate. Frequently missed.</td></tr>
<tr><td><strong>Card reissued</strong></td><td>Issuers may map existing card e-mandates to the reissued card &mdash; which removes the old problem of every mandate silently lapsing when a card expired.</td></tr>
</table>
''' + note("<strong>Card reissue mapping is quietly one of the most valuable changes in the 2026 framework.</strong> Mandate churn on card expiry used to be a large, invisible source of involuntary subscriber loss &mdash; the customer never chose to leave, the card simply expired. Ask your acquirer whether they support the mapping, because it is the difference between losing a cohort every three years and not.")

i_cost = registry("Recurring payments &mdash; what it costs", [
 ("The facility, to the customer", "direct",
  "<strong>Nothing. Issuers are prohibited from charging customers</strong> for using an e-mandate. "
  "If a fee exists in your flow, you absorb it."),
 ("Per transaction", "direct",
  "Ordinary payment processing, per successful debit. See "
  "<a href=\"/fintech-ai/payments-reconciliation/build-sheet/\">Build Sheet 05</a> for the rails and "
  "their rates."),
 ("Mandate registration", "direct",
  "Sometimes a separate small fee per registered mandate, sometimes bundled. Worth asking, because "
  "a high-churn product registers far more mandates than a stable one."),
 ("Notifications", "direct",
  "<strong>Two per debit cycle, minimum</strong> &mdash; one 24 hours before, one after. On SMS at "
  "scale this is a real line, and it is proportional to your billing frequency rather than your "
  "revenue."),
 ("Failure handling", "direct",
  "<strong>The line that decides the economics.</strong> Recovery is customer-action-dependent in "
  "three of four failure modes, so it costs communication and time rather than compute. Getting it "
  "right is worth more than any per-transaction saving."),
 ("Building three rails", "direct",
  "Card, UPI AutoPay and eNACH are three integrations under one rulebook. <strong>Budget three "
  "integrations and one rule engine</strong> &mdash; not three of each."),
], "September 2026") + warn("<strong>Model involuntary churn, not just failed debits.</strong> A failed instalment that is never recovered is a lost customer who did not choose to leave. Measure <em>recovery rate per failure mode</em> and <em>involuntary churn</em> separately from voluntary cancellation &mdash; most billing dashboards collapse all three into &ldquo;churn&rdquo; and hide the one you can actually fix.")

a_builds = '''
<h3 id="s-amber-week">The starting version</h3>
<p><strong>Build:</strong> one rail, usually UPI AutoPay &rarr; registration with AFA &rarr; a mandate
row storing category, cap, frequency and validity &rarr; a 24-hour notification job with delivery
checked at presentation &rarr; post-debit confirmation with the grievance route &rarr; three distinct
failure messages.</p>
<p><strong>It breaks when:</strong> customers arrive without UPI, or ticket sizes cross
&#8377;15,000 in a category without the exception.</p>

<h3 id="s-amber-proper">The proper version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; <strong>two or three rails behind one
internal mandate model</strong> &rarr; the enhanced-category list as a closed set in code &rarr; the
customer cap enforced separately from the regulatory limit &rarr; single-debit opt-out as well as
full revocation &rarr; pause without cancel &rarr; card-reissue mapping confirmed with your acquirer
&rarr; recovery rate measured <em>per failure mode</em> &rarr; UPI AutoPay offered as a fallback when
card re-registration goes unanswered.</p>
<p><strong>Trade:</strong> the rule engine is the asset. Three rails is three integrations; three
interpretations of the rules is a compliance gap waiting to be found.</p>

<h3 id="s-amber-big">The version at scale</h3>
<p><strong>Build:</strong> everything above, plus &mdash; intelligent retry timing on the one
genuinely retryable mode &rarr; notification channel optimisation &rarr; cohort-level involuntary
churn reporting &rarr; a dunning sequence that escalates across rails rather than repeating on one.</p>
''' + note("If you take one thing from this page: <strong>split your dunning message into three.</strong> Cancelled mandate, above-threshold, and notification failure need three different customer actions, and one generic email serves none of them. It is a week of work and it moves recovery more than any other change available here.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>EMI collections fail above &#8377;15,000</strong></td><td>The &#8377;1 lakh exception was assumed to cover loans.</td><td>It covers insurance, mutual funds and credit card bills only.</td></tr>
<tr><td><strong>Recovery rate is poor</strong></td><td>One generic dunning email for three different failure modes.</td><td>Three messages, three actions.</td></tr>
<tr><td><strong>Debits presented without notification</strong></td><td>The notification is fire-and-forget on the scheduler.</td><td>Check delivery at presentation time.</td></tr>
<tr><td><strong>Chargebacks from unrecognised names</strong></td><td>The legal entity name in the notification.</td><td>Use the name the customer recognises.</td></tr>
<tr><td><strong>Mandates lapse on card expiry</strong></td><td>Reissue mapping not enabled.</td><td>Ask the acquirer. It is supported now.</td></tr>
<tr><td><strong>Customers cancel instead of pausing</strong></td><td>There is no pause.</td><td>Build pause. Cancelling is a decision they cannot undo easily.</td></tr>
<tr><td><strong>Three rails, three rule implementations</strong></td><td>Each integration was built by itself.</td><td>One mandate model, three adapters.</td></tr>
<tr><td><strong>A debit after expiry</strong></td><td>Validity stored but not enforced.</td><td>Enforce it. It is an unauthorised transaction.</td></tr>
</table>
'''

SRC=[('official','RBI — Digital Payments – E-mandate Framework, 2026 (Circular RBI/DPSS/2026-27/396, 21 April 2026)','the consolidated rulebook replacing eight earlier circulars: AFA triggers, the ₹15,000 general limit, the ₹1 lakh enhanced limit and its three categories, the 24-hour pre-debit notification, post-debit confirmation, revocation, the prohibition on customer charges, card-reissue mapping, and acquirer responsibility for merchant compliance.','https://www.rbi.org.in'),
 ('official','RBI — customer liability in unauthorised electronic transactions','the liability framework that applies to recurring debits the customer did not authorise.','https://www.rbi.org.in'),
 ('official','NPCI — UPI AutoPay','the UPI mandate rail, registration in the customer’s UPI app, and the mandate lifecycle.','https://www.npci.org.in'),
 ('official','NPCI — NACH','the eNACH rail for bank-account standing instructions.','https://www.npci.org.in'),
 ('industry','Payment provider and billing-platform reporting','the failure-mode taxonomy and recovery guidance in step 6, and the observation that a single generic dunning message collapses recovery. Practitioner-sourced; test against your own cohort.',''),
 ('industry','Framework commentary, April–June 2026','summaries of the 2026 framework used to cross-check the limits and exemptions. Verify any specific figure against the circular before relying on it.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'+(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. This framework was rewritten in April 2026; the date is part of the claim.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/products/bnpl-checkout/" class="mod-card"><div class="mod-num">GUIDE 03</div><h3>BNPL Checkout</h3><p>Where these mandates collect the instalments — and where the EMI exception bites hardest.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>The rails underneath, settlement timing, and matching collections to the ledger.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 06</div><h3>Customer Operations</h3><p>Dunning is customer communication, and the contact window applies to it.</p></a>
<a href="/fintech-ai/products/account-aggregator/" class="mod-card"><div class="mod-num">GUIDE 04</div><h3>Account Aggregator</h3><p>How you knew they could afford the instalment before you set the mandate up.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Recurring debits move customer money on a standing permission, and presenting one you are not entitled to is an unauthorised transaction rather than a billing error. Nothing here is legal advice. Have your mandate model, notification logic and dunning sequence reviewed by qualified counsel and your payment partner before the first live debit.")

lanes={'green':[("How to use this page",g_read),("What an e-mandate actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 to 3 — rails, registration and limits",i_step12),
           ("Step 4 — the notification that is a gate",i_step4),
           ("Steps 6 to 8 — failure, confirmation and control",i_step678),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Recurring Payments: How to Build It"
META=("Build recurring e-mandate collections step by step: the eight stages, the 2026 limits, how to "
      "connect them, and the exception everyone gets wrong.")
LEAD=("A step-by-step guide to building recurring payments on e-mandates in India. Eight stages, the "
      "options at each one, exactly how each step connects to the next, real costs, and what breaks. "
      "Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/recurring-payments",title=TITLE,meta=META,lead=LEAD,label="Product Guide 05",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/recurring-payments/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: _io.open(f,'w',encoding='utf-8').write(h.replace('</style>',CSSRC+'\n</style>',1))
