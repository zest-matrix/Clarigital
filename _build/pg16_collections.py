#!/usr/bin/env python3
# Session 108 — PRODUCT GUIDE 16: Collections and recovery. Closes Phase 1.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one thing: the system that contacts a borrower who has missed
a payment, and decides what to say, when, and how many times.</p>
<p><strong>Every other product guide on this site regulates a transaction. This one regulates a
conversation.</strong> The rules govern the hour you may call, the words you may use, who you may
mention it to, and what evidence you must keep &mdash; and they were written for a human agent at a
time when the agent is increasingly a machine.</p>
''' + warn("<strong>The rulebook was rewritten six weeks ago and it commences on 1 January 2027.</strong> After two rounds of consultation &mdash; a first draft in February 2026 and a revised draft on 20 May 2026 &mdash; the RBI notified the <strong>Reserve Bank of India (Commercial Banks &mdash; Responsible Business Conduct) Fourth Amendment Directions, 2026</strong> on <strong>6 August 2026</strong>, with parallel circulars for NBFCs. <strong>Nine circulars, one commencement date: 1 January 2027.</strong> Until then the existing instructions continue to apply unchanged. Anything you read describing the February or May drafts is describing a text that was superseded before it took effect.")

g_what = '''
<p>Collections is a sequence of decisions, and the regulated part is the contact rather than the
decision. What you are building:</p>
<table>
<tr><th>Layer</th><th>What it decides</th><th>Regulated?</th></tr>
<tr><td><strong>Prioritisation</strong></td><td>Which accounts to work, in what order</td><td>Indirectly &mdash; through the model rules</td></tr>
<tr><td><strong>Treatment</strong></td><td>Reminder, call, restructure offer, field visit</td><td>Partly</td></tr>
<tr><td><strong>Contact</strong></td><td>When, how often, by what channel, in what words</td><td><strong>Heavily, and specifically</strong></td></tr>
<tr><td><strong>Settlement</strong></td><td>What you will accept and on what terms</td><td>By your own board-approved policy</td></tr>
</table>
''' + note("<strong>The standing rules, in force today and unchanged until January.</strong> The <strong>Fair Practices Code</strong> restricts contact to <strong>8 AM to 7 PM</strong>, across every channel &mdash; call, SMS, messaging app, email and visit &mdash; and prohibits contacting relatives, employers, neighbours or colleagues to apply pressure. The recovery agents circular of <strong>12 August 2022</strong> reinforced this across regulated entities. And throughout, <strong>the lender remains liable for the conduct of anyone recovering on its behalf.</strong> Outsourcing the calling does not outsource the answerability.") + '''
<p><strong>What this is not:</strong></p>
<ul>
<li><strong>Not a dialler project.</strong> The hard part is deciding who not to call and when to
stop.</li>
<li><strong>Not a place to deploy autonomy.</strong> See step 5.</li>
<li><strong>Not device locking.</strong> That category shrank sharply in August. Step 7.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Segment by reason, not by days past due</strong></td><td>Forgot, cannot, will not. Three different problems.</td></tr>
<tr><td>2</td><td><strong>Build the contact rules as code</strong></td><td>Hours, frequency, channel, consent. Not as a policy document.</td></tr>
<tr><td>3</td><td><strong>Write what gets said</strong></td><td>And what may never be said.</td></tr>
<tr><td>4</td><td><strong>Decide the channel</strong></td><td>Self-serve first. A call is expensive in more than money.</td></tr>
<tr><td>5</td><td><strong>If a machine speaks, constrain it</strong></td><td><strong>The step with no settled rulebook.</strong></td></tr>
<tr><td>6</td><td><strong>Offer a way out</strong></td><td>Restructure, settle, pause. The point of the exercise.</td></tr>
<tr><td>7</td><td><strong>Escalate lawfully</strong></td><td>Agents, visits, devices &mdash; all newly constrained.</td></tr>
<tr><td>8</td><td><strong>Record and answer for it</strong></td><td>Recordings, complaints, the Ombudsman clock.</td></tr>
</table>
''' + note("<strong>Steps 1, 5 and 8 are the ones that get skipped.</strong> Steps 2 to 4 are what a collections platform sells you. <strong>Nobody sells you the segmentation by reason, the constraint on the machine, or the evidence trail</strong> &mdash; and those three decide whether the system recovers money or generates complaints.")

i_step123 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Segment by reason, not by days past due</h3>
<p>Almost every collections system buckets accounts by how late they are. Days past due is a
measure of <em>how long</em>, and tells you nothing about <em>why</em> &mdash; which is the only thing
that determines what works.</p>
<table>
<tr><th>Reason</th><th>What actually works</th></tr>
<tr><td><strong>Forgot</strong> &mdash; a failed mandate, an expired card, a changed account</td><td>A reminder and a one-tap fix. <strong>A call here is a cost and an irritation</strong></td></tr>
<tr><td><strong>Cannot</strong> &mdash; income shock, illness, job loss</td><td>A restructure conversation. Pressure produces nothing and costs the relationship</td></tr>
<tr><td><strong>Will not</strong> &mdash; dispute, dissatisfaction, refusal</td><td>Resolution of the dispute, or lawful escalation. Not more reminders</td></tr>
</table>
<p><strong>The first bucket is usually the largest and the cheapest to fix</strong>, and treating it
with the same intensity as the third is how collections programmes generate complaints while
recovering money they would have recovered anyway.</p>

<h3 id="s-indigo-s2">Step 2 &mdash; Contact rules belong in code</h3>
<p>A policy document saying <em>we call between 8 and 7</em> is not a control. The control is a
function that refuses to place the call.</p>
<p>What has to be enforced, not documented: the <strong>8 AM to 7 PM window across every channel</strong>,
in the borrower's local time; a frequency cap per day and per week; a rule that a promise to pay
suppresses contact until the promised date; that a registered dispute suppresses collections contact
entirely; and that <strong>nobody other than the borrower and a guarantor is contacted about the
debt.</strong></p>

<h3 id="s-indigo-s3">Step 3 &mdash; What gets said, and what may never be said</h3>
<p>Script the permitted messages, and script them narrowly. More usefully, enumerate the prohibited
ones, because that list is short, specific and the one that generates complaints:</p>
<ul>
<li><strong>Any threat</strong>, including implied &mdash; arrest, criminal proceedings, seizure
without an order, damage to a person's standing.</li>
<li><strong>Abusive, obscene or intimidating language.</strong></li>
<li><strong>Disclosing the debt to anyone else</strong>, including by leaving a message with a family
member or writing it on a visible envelope.</li>
<li><strong>Misrepresenting who you are</strong> or what authority you hold.</li>
<li><strong>Claiming legal consequences that do not exist.</strong> For an unsecured loan, no asset is
seized without a court order.</li>
</ul>
'''

code_contact = code('Python — steps 2 to 5, the rules as a gate, and constraining a machine that speaks', r'''from datetime import datetime, time, timedelta

# STEP 2. THE GATE. Nothing reaches a borrower except through this.
WINDOW = (time(8, 0), time(19, 0))      # Fair Practices Code: 8 AM to 7 PM

def may_contact(account, now_local, channel, history, flags):
    """Returns (allowed, reason). A policy document does not stop a call.
    This does."""
    if not (WINDOW[0] <= now_local.time() < WINDOW[1]):
        return False, "outside_permitted_hours"        # every channel, not just voice
    if flags["dispute_registered"]:
        return False, "dispute_open"
    if flags["promise_to_pay_until"] and now_local.date() <= flags["promise_to_pay_until"]:
        return False, "promise_to_pay_active"
    if history.contacts_today(account) >= flags["daily_cap"]:
        return False, "daily_cap_reached"
    if history.contacts_this_week(account) >= flags["weekly_cap"]:
        return False, "weekly_cap_reached"
    if flags["vulnerability_hold"]:
        return False, "vulnerability_hold"             # see step 5
    return True, "ok"

def permitted_recipients(account):
    # Nobody else. Not a relative, an employer, a neighbour or a colleague.
    return [account["borrower"]] + account.get("guarantors", [])

# STEP 5. IF A MACHINE DOES THE SPEAKING.
# There is no settled rulebook for an automated voice agent in collections.
# The conduct rules were written for a person, they apply to the lender
# regardless of who or what makes the call, and the gap is yours to fill.

AGENT_CONSTRAINTS = {
    "identifies_as_automated_up_front": True,
    "states_the_lender_by_name": True,
    "route_to_human_offered_every_turn": True,
    "may_negotiate": False,          # it presents options; it does not deal
    "may_threaten": False,           # not expressible, not merely disallowed
    "max_turns_before_human": 6,
    "recording_disclosed_before_it_starts": True,
}

# The thing an automated caller cannot do is notice.
DISTRESS_MARKERS = ("hospital", "died", "passed away", "lost my job",
                    "cannot cope", "harassing me", "legal notice")

def supervise(turn, agent_constraints):
    if any(m in turn["transcript"].lower() for m in DISTRESS_MARKERS):
        # Not a branch in the script. Leave the automation entirely.
        return {"action": "hand_to_human_now", "suppress_further_automation": True,
                "set_vulnerability_hold": True}
    if turn["index"] >= agent_constraints["max_turns_before_human"]:
        return {"action": "offer_human"}
    return {"action": "continue"}

# WHAT TO CHECK
# [ ] the gate is the ONLY path to a borrower. A campaign tool that can
#     bypass it is the whole control gone
# [ ] the hour test uses the BORROWER's local time, not your server's
# [ ] the window applies to SMS and messaging apps too. An automated message
#     at 10pm is the same violation as a call
# [ ] a promise to pay suppresses contact. Calling someone who has already
#     told you when they will pay is the most common avoidable complaint
# [ ] distress markers exit the automation rather than branch inside it
# [ ] the agent cannot express a threat. Not "is instructed not to" -- the
#     phrasing is not in its permitted output at all
# [ ] every suppression is logged with its reason. "We did not call" is
#     evidence only if it is recorded
''')

i_step45 = '''
<h3 id="s-indigo-s4">Steps 2 to 5 &mdash; The gate, and the machine that speaks</h3>
''' + code_contact + '''
<p><strong>THE finding, and it is the reason this page is different from the other fifteen:</strong>
<strong>the conduct rules describe how a person should behave, they bind the lender regardless of who
or what places the call, and nothing yet describes how an automated caller should behave. The gap is
yours to fill and it will be filled later, by somebody else, retrospectively.</strong></p>
<p>An automated dialler complies with the 8 AM to 7 PM window trivially &mdash; better than a human
team does. What it cannot do is <strong>notice</strong>. A person hearing <em>"my father is in
hospital"</em> stops. A script hears an unmatched intent and asks about the payment again, and the
second question is the one that becomes a complaint, a screenshot and an Ombudsman case.</p>
''' + warn("<strong>Design the exit, not the branch.</strong> The instinct is to add distress handling as a path inside the conversation. That is the wrong shape: a machine that responds to <em>&ldquo;I lost my job&rdquo;</em> with a scripted empathy line and then returns to collection has produced something worse than silence. <strong>Distress should end the automation entirely</strong> &mdash; hand to a human, suppress further automated contact, and set a hold. It costs conversion on a small number of calls and it is the difference between a system that is defensible and one that is not.") + '''
<p>Two further positions worth taking before anyone requires them. <strong>Say it is automated, up
front.</strong> There is no Indian rule presently compelling that disclosure in collections, and a
borrower who discovers mid-call that they have been arguing with a machine about their debt is a
complaint you created. <strong>And never let it negotiate.</strong> It may present options your policy
has already approved; it may not agree terms, because an agreement reached with a machine is an
argument about what was agreed.</p>
'''

code_resolve = code('Python — steps 6 to 8, resolution, escalation and the evidence you will be asked for', r'''from datetime import date, timedelta

# STEP 6. THE WAY OUT, OFFERED EARLY RATHER THAN CONCEDED LATE.
def resolution_options(account, policy):
    """Present what your policy already approves. Do not hold options back as
    a negotiating position -- the segment that needs them is the segment that
    does not respond to pressure."""
    opts = []
    if policy["allow_reschedule"]:
        opts.append({"type": "reschedule", "self_serve": True})
    if account["hardship_flag"] and policy["allow_pause"]:
        opts.append({"type": "pause", "months": policy["max_pause_months"],
                     "self_serve": True})
    if account["days_past_due"] > policy["settlement_after_days"]:
        opts.append({"type": "settlement", "self_serve": False})   # needs approval
    # Self-serve at 11pm converts. The same option behind a daytime phone
    # call frequently does not.
    return opts

# STEP 7. ESCALATION. EACH STEP HAS A PRECONDITION, NOT A DAY COUNT.
def may_escalate(account, step, agents, now):
    if step == "field_visit":
        # Fourth Amendment Directions, from 1 Jan 2027: notice first.
        return account["visit_notice_sent_on"] is not None and \
               now.date() >= account["visit_notice_sent_on"] + timedelta(days=1)
    if step == "assign_agency":
        # Certified, background-verified, publicly listed, borrower informed.
        a = agents.assigned(account)
        return all([a["iibf_certified"], a["background_verified"],
                    a["published_on_website"], account["borrower_informed_in_writing"]])
    if step == "restrict_device":
        # Baseline is prohibition. Only a device this loan financed.
        return account["device_was_financed_by_this_loan"] and \
               account["days_past_due"] >= policy_min_days() and \
               account["graduated_restriction_only"]
    return False

# STEP 8. THE EVIDENCE, AND THE CLOCK THAT RUNS WITHOUT YOU.
def complaint_sla(received_on):
    """RB-IOS 2026: no reply within 30 days, or an unsatisfactory one, and the
    borrower may go to the Ombudsman. Set your own clock shorter."""
    return {"internal_target": received_on + timedelta(days=14),
            "ombudsman_eligible_from": received_on + timedelta(days=30)}

def evidence_pack(account, store):
    # What a complaint is answered with. Assemble it now, not later.
    return {
        "contact_log": store.contacts(account),        # incl. SUPPRESSED, with reason
        "recordings": store.recordings(account),       # prior intimation given
        "transcripts": store.transcripts(account),
        "who_called": store.actor(account),            # human or agent, named
        "options_offered": store.offers(account),
        "notices_sent": store.notices(account),
    }

# WHAT TO CHECK
# [ ] report complaint AGE, not complaint volume. The oldest open complaint
#     predicts escalation; the count does not
# [ ] log suppressed contacts with their reason. "We did not call" is
#     evidence only if it was recorded at the time
# [ ] every escalation step checks a PRECONDITION, not a day counter
# [ ] the actor on every contact is identifiable -- which human, or which
#     automated agent and which version of it
# [ ] test retrieval of a recording from six months ago before you need one
# [ ] run the SLA clock in IST against calendar days, not working days. The
#     Ombudsman's 30 days do not pause for your weekend
''')

i_step678 = '''
<h3 id="s-indigo-s6">Step 6 &mdash; Offer a way out</h3>
<p>The purpose of collections is recovery, and the highest-recovery action for the <em>cannot pay</em>
segment is almost always a restructure rather than pressure. Build the options into the first contact
rather than holding them back as a concession: a revised schedule, a short pause, a part-payment
arrangement, a settlement where the account warrants it.</p>
<p><strong>Make them self-serve.</strong> A borrower who can restructure at eleven at night without
speaking to anyone will do it. The same borrower, asked to call during office hours to discuss it,
frequently does not.</p>
''' + code_resolve + '''

<h3 id="s-indigo-s7">Step 7 &mdash; Escalation, and what changed in August</h3>
<p>The <strong>Fourth Amendment Directions</strong> of <strong>6 August 2026</strong>, in force from
<strong>1 January 2027</strong> and issued under sections 21 and 35A of the Banking Regulation Act,
convert a scattered set of expectations into a detailed and enforceable code. What they add:</p>
<table>
<tr><th>Requirement</th><th>Detail</th></tr>
<tr><td><strong>Agent certification</strong></td><td>Background verification, and certification through <strong>IIBF</strong> or a similar institution</td></tr>
<tr><td><strong>Public disclosure</strong></td><td>An updated list of empanelled recovery agencies on the website and digital platforms</td></tr>
<tr><td><strong>Notice before a visit</strong></td><td><strong>At least one day's prior notice</strong> of any recovery-related visit</td></tr>
<tr><td><strong>Notice of change</strong></td><td>Borrowers told when an agency is assigned, changed or removed</td></tr>
<tr><td><strong>Call recording</strong></td><td>Recovery interactions recorded, <strong>with prior intimation</strong></td></tr>
<tr><td><strong>Board-approved policy</strong></td><td>Monitoring, escalation, due diligence, and compensation linked to complaints</td></tr>
<tr><td><strong>Scope</strong></td><td>Recovery agencies and agents defined; <strong>Business Correspondents handling collections are in</strong></td></tr>
</table>
''' + warn("<strong>Device locking: the baseline is now prohibition.</strong> The revised framework permits only <strong>graduated restriction of functions on a device the loan financed</strong>, after a defined period of missed payments, and creates a <strong>compensation mechanism for borrowers subjected to wrongful recovery action</strong>. Outside device finance, remote locking is not a recovery tool. <strong>If your collections roadmap contains a device-control feature, that feature has a deadline rather than a launch date</strong>, and the compensation exposure attaches to getting it wrong.") + '''

<h3 id="s-indigo-s8">Step 8 &mdash; Record it, and answer for it</h3>
<p>Two clocks matter. Internally, a complaint must be capable of being answered with what was actually
said &mdash; which means the recording, the transcript, the contact log with its suppression reasons,
and the identity of whoever or whatever made the call.</p>
<p>Externally, the <strong>Reserve Bank Integrated Ombudsman Scheme, 2026</strong>, effective
<strong>1 July 2026</strong>, sets the path: the complainant approaches the regulated entity first,
and may escalate to the Ombudsman if there is no reply within <strong>30 days</strong> or the reply is
unsatisfactory, within <strong>90 days</strong> of that period expiring.</p>
''' + note("<strong>That timeline is your real service level.</strong> A complaint that sits unanswered for thirty days becomes an Ombudsman case automatically, whatever its merits. <strong>Route collections complaints to a named owner with a shorter internal clock than thirty days</strong>, and track age rather than volume &mdash; the metric that predicts escalation is how long the oldest open complaint has been open, and almost nobody reports it.")

i_cost = registry("Collections and recovery &mdash; what it costs", [
 ("The contact gate", "direct",
  "Small to build, and the highest-value component here. <strong>Every route to a borrower must pass "
  "through it</strong>; a campaign tool that can bypass it removes the control entirely."),
 ("Self-serve resolution", "direct",
  "Restructure, pause and part-payment without a conversation. <strong>Usually the highest-return "
  "investment in the whole programme</strong>, because the largest segment simply forgot and the "
  "second largest needs terms rather than pressure."),
 ("Voice automation", "direct",
  "Per minute or per conversation, and cheap against an agent. <strong>Price the supervision "
  "alongside it</strong> &mdash; transcript monitoring, distress detection, human handover capacity "
  "&mdash; because the unsupervised version is the one that produces the complaint."),
 ("Agent certification", "direct",
  "<strong>From 1 January 2027</strong>: background verification and certification through IIBF or "
  "similar, for every agent interacting with borrowers. Recurring, and it applies to outsourced "
  "agencies as much as employees."),
 ("Recording and retention", "direct",
  "Recovery interactions recorded with prior intimation, stored, and retrievable when a complaint "
  "arrives months later. <strong>Retrievability is the requirement</strong>, not storage."),
 ("Complaint handling", "direct",
  "A named owner and an internal clock <strong>shorter than the Ombudsman's 30 days</strong>. "
  "Understaffing this converts ordinary complaints into regulatory ones."),
 ("Getting it wrong", "indirect",
  "The lender is liable for agent conduct and cannot outsource it. Penalties in the "
  "<strong>crores</strong> have been imposed for recovery-agent harassment, and the new framework adds "
  "a <strong>quantified compensation mechanism</strong> for wrongful recovery action."),
], "September 2026") + note("<strong>The number worth computing first: what share of your overdue accounts are in the &lsquo;forgot&rsquo; bucket?</strong> In most portfolios it is the majority, it is recoverable with a reminder and a working payment link, and every rupee of collections intensity spent on it is spent generating irritation for money you were going to get. <strong>That figure decides the size of everything else on this list.</strong>")

a_builds = '''
<h3 id="s-amber-week">Reminders and self-serve</h3>
<p><strong>Build:</strong> failed-mandate detection &rarr; a reminder inside permitted hours &rarr; a
one-tap payment link &rarr; self-serve restructure.</p>
<p><strong>You get:</strong> most of the recoverable balance, almost no conduct exposure, and no
recovery agents. <strong>For many lenders this is the whole product</strong>, and the reason it is not
built first is that it does not look like collections.</p>

<h3 id="s-amber-proper">Segmented treatment with human calling</h3>
<p><strong>Build:</strong> the above, plus segmentation by reason &rarr; the contact gate enforcing
hours, caps, promises and disputes &rarr; scripted treatments with a prohibited list &rarr; human
calling for the <em>cannot pay</em> segment &rarr; complaints to a named owner.</p>
<p><strong>Trade:</strong> people cost money and exercise judgement. <strong>The judgement is what you
are buying</strong>, not the throughput.</p>

<h3 id="s-amber-big">Automated voice at scale</h3>
<p><strong>Build:</strong> the above, plus an automated caller that <strong>identifies itself</strong>,
<strong>cannot express a threat</strong>, <strong>cannot negotiate</strong>, offers a human every turn,
and <strong>exits entirely on any distress marker</strong> &mdash; with transcript supervision and a
human handover capacity sized for the exits.</p>
<p><strong>It breaks when:</strong> the exit is built as a branch inside the conversation rather than
an exit from it. <strong>A machine that acknowledges a bereavement and then asks about the payment
again has produced the worst available outcome</strong>, and it will be a screenshot before it is a
metric.</p>
''' + note("If you take one thing from this page: <strong>put distress handling outside the automation, not inside it.</strong> Every other control here is a rule a machine can follow. Noticing that something has changed is the one thing it cannot do, and the whole defensibility of an automated collections system rests on how quickly it stops.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>SMS at 10pm</strong></td><td>The window was applied to voice only.</td><td>Every channel. An automated message is a contact.</td></tr>
<tr><td><strong>Call in the wrong time zone</strong></td><td>Server time, not borrower time.</td><td>Evaluate the window in the borrower's local time.</td></tr>
<tr><td><strong>Calling after a promise to pay</strong></td><td>The promise was logged, not enforced.</td><td>Suppress until the promised date.</td></tr>
<tr><td><strong>Contacting a relative</strong></td><td>Treated as a way to reach the borrower.</td><td>Borrower and guarantors only. Nobody else.</td></tr>
<tr><td><strong>Campaign tool bypasses the gate</strong></td><td>A second route to the customer existed.</td><td>One path. Everything else is the control removed.</td></tr>
<tr><td><strong>Machine keeps collecting after a bereavement</strong></td><td>Distress built as a branch.</td><td>Exit the automation. Hold further contact.</td></tr>
<tr><td><strong>Borrower discovers mid-call it is a bot</strong></td><td>Disclosure not required, so not given.</td><td>Say it up front anyway.</td></tr>
<tr><td><strong>Machine agreed terms</strong></td><td>Negotiation left open.</td><td>It presents approved options. It does not deal.</td></tr>
<tr><td><strong>Field visit with no notice</strong></td><td>Old practice.</td><td>One day's prior notice, from 1 January 2027.</td></tr>
<tr><td><strong>Device locked outside device finance</strong></td><td>It worked, so it stayed.</td><td>Baseline is prohibition, with compensation exposure.</td></tr>
<tr><td><strong>Complaint sits 30 days</strong></td><td>Tracked by volume, not age.</td><td>Internal clock shorter than the Ombudsman's. Track the oldest.</td></tr>
<tr><td><strong>Cannot say what was said</strong></td><td>Recording absent or unretrievable.</td><td>Record with prior intimation; test retrieval.</td></tr>
</table>
'''

SRC=[('official','Reserve Bank of India (Commercial Banks — Responsible Business Conduct) Fourth Amendment Directions, 2026','notified 6 August 2026 with parallel circulars for NBFCs — nine circulars sharing a commencement date of 1 January 2027, issued under sections 21 and 35A of the Banking Regulation Act, 1949. Recovery agent background verification and IIBF certification, public disclosure of empanelled agencies, at least one day&rsquo;s notice before a recovery visit, notification when an agency is assigned or changed, recording of recovery interactions with prior intimation, a board-approved recovery policy covering monitoring, escalation, due diligence and compensation, the restriction of device functionality to financed devices only after a defined period of default, and a compensation mechanism for wrongful recovery action. Existing instructions continue to apply until 1 January 2027.','https://www.rbi.org.in'),
 ('official','RBI Fair Practices Code — conduct in recovery','the restriction of borrower contact to between 8 AM and 7 PM across all channels, the prohibition on contacting relatives, employers, neighbours or colleagues to apply pressure, the prohibition on threatening or abusive conduct, and the principle that the lender remains responsible for the conduct of agents acting on its behalf.','https://www.rbi.org.in'),
 ('official','RBI circular on engagement of recovery agents, 12 August 2022','the reinforcement and extension of recovery conduct requirements across regulated entities, including in relation to digital lending applications and tele-calling.','https://www.rbi.org.in'),
 ('official','RBI draft Amendment Directions of February 2026 and the revised draft of 20 May 2026','the two consultation rounds preceding the notified text, with proposed commencement dates of 1 July 2026 and then 1 October 2026 respectively. Both were superseded by the 6 August 2026 notification. Recorded here because a great deal of published commentary still describes the drafts.','https://www.rbi.org.in'),
 ('official','Reserve Bank Integrated Ombudsman Scheme, 2026','effective 1 July 2026. The complainant approaches the regulated entity first and may escalate to the Ombudsman where there is no reply within 30 days or the reply is unsatisfactory, within 90 days of that period expiring.','https://rbi.org.in'),
 ('official','RBI Master Direction on Outsourcing of Financial Services','the framework under which a regulated entity remains accountable for functions it outsources, including collections, and must exercise due diligence and oversight over service providers.','https://www.rbi.org.in'),
 ('official','RBI Responsible Business Conduct (Second Amendment) Directions, 2026','notified 15 June 2026 and also commencing 1 January 2027, extending responsibility to DSAs, DMAs, sub-agents and third-party service provider representatives and requiring published lists of empanelled agents. Covered in full on the Embedded Insurance guide.','https://www.rbi.org.in'),
 ('industry','Reporting on recovery-agent enforcement and complaint volumes','penalties in the crores imposed for recovery-agent harassment, and reporting that loan and credit-card matters form the largest share of grievances. Directional; confirm any figure against the order before relying on it.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. <strong>The Fourth Amendment Directions are notified but not yet in force</strong> '
 '&mdash; they commence 1 January 2027, and until then the existing instructions apply. Verify against the '
 'notified text rather than against the February or May drafts, which were superseded.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/products/alternative-credit-scoring/" class="mod-card"><div class="mod-num">GUIDE 10</div><h3>Alternative Credit Scoring</h3><p>Model governance, and why a collections score is a model too.</p></a>
<a href="/fintech-ai/products/embedded-insurance/" class="mod-card"><div class="mod-num">GUIDE 09</div><h3>Embedded Insurance</h3><p>The other RBC Directions commencing the same day.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 06</div><h3>Customer Operations</h3><p>Grievance handling, contact windows and the conduct stack.</p></a>
<a href="/fintech-ai/products/bnpl-checkout/" class="mod-card"><div class="mod-num">GUIDE 03</div><h3>BNPL Checkout</h3><p>The digital lending rulebook, including what a platform may never access.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Recovery conduct is regulated in detail, the framework was notified on 6 August 2026 and commences on 1 January 2027, and automated calling sits in a gap the rules do not yet describe. Nothing here is legal advice. Have your contact rules, your scripts, your automation constraints and your outsourcing contracts reviewed by qualified counsel before a single call is placed.")

lanes={'green':[("How to use this page",g_read),("What you are actually building",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 to 3 — segment, gate, script",i_step123),
           ("Steps 2 to 5 — the gate, and the machine that speaks",i_step45),
           ("Steps 6 to 8 — resolve, escalate, answer for it",i_step678),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Collections and Recovery: How to Build It"
META=("Build a collections system step by step: the contact rules as code, constraining an automated "
      "caller, and what the August 2026 Directions change.")
LEAD=("A step-by-step guide to building loan collections and recovery in India. Eight stages, the "
      "options at each one, exactly how each step connects to the next, real costs, and what breaks. "
      "Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
MD=_re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')
for nm,lane in lanes.items():
    for t,c in lane:
        s=MD.findall(_re.sub(r'<[^>]+>',' ',c)); assert not s, 'markdown in %s: %s'%(t,s[:3])
page(path="fintech-ai/products/collections-recovery",title=TITLE,meta=META,lead=LEAD,label="Product Guide 16",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/collections-recovery/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Contacting borrowers who '
  'have missed a payment? The eight steps, the contact rules as code, and what the August 2026 Directions '
  'change from 1 January 2027: <a href="/fintech-ai/products/collections-recovery/"><strong>Collections '
  'and Recovery: How to Build It &rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('credit-underwriting', 'customer-operations'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/collections-recovery' in src:
        print('  = already linked from /' + mod + '/'); continue
    n = src.count(ANCHOR)
    assert n == 1, 'anchor appears ' + str(n) + ' times in ' + p
    i = src.find(ANCHOR); assert i != -1
    out = src[:i] + NOTE_BLOCK + src[i:]
    assert out.count('<div') == src.count('<div') + 1
    assert out.count('</div>') == src.count('</div>') + 1
    assert len(out) == len(src) + len(NOTE_BLOCK)
    _io.open(p, 'w', encoding='utf-8').write(out)
    print('  + linked from /' + mod + '/')
