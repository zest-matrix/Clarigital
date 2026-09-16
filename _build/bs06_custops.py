#!/usr/bin/env python3
# Session 50 — Build Sheet 06: Customer Operations
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

V = VERIFIED

# ---------------------------------------------------------------- GREEN

g_read = f'''
<p>The <a href="/fintech-ai/customer-operations/">Customer Operations module</a> explains why an AI
agent that speaks for a regulated firm is a different problem from one that answers questions about
a t-shirt. This page is the parts list: channels, agent platforms, grounding components, what each
costs per unit, and the three builds.</p>
{warn(f"Prices carry a <strong>Verified {V}</strong> stamp and sit in marked blocks. Two of the numbers on this page change within weeks of writing &mdash; one of them on 1 October 2026 &mdash; so the dates matter more here than anywhere else in this section.")}
<p>Four jobs, bought separately, and the fourth is the one that decides whether the first three were
a good idea.</p>
<table>
<tr><th>Job</th><th>What it does</th><th>Can you skip it?</th></tr>
<tr><td><strong>Deflect</strong></td><td>Answer the question without a human. Balance, statement, how-do-I.</td><td>No, at any volume. This is what everyone buys.</td></tr>
<tr><td><strong>Assist</strong></td><td>Draft, summarise and retrieve for a human agent who stays accountable.</td><td>Underrated. Often the better first project, because the human is the control.</td></tr>
<tr><td><strong>Act</strong></td><td>Do something: raise a dispute, block a card, change an address.</td><td>Yes, and you should, for longer than feels comfortable. Actions are where liability concentrates.</td></tr>
<tr><td><strong>Escalate</strong></td><td>Hand to a human with full context, and recognise a complaint as a complaint.</td><td>No. Getting this wrong turns a support problem into a regulatory one.</td></tr>
</table>
<p>Almost every failed deployment we can find evidence for over-invested in the first and
under-invested in the fourth.</p>
'''

g_principle = f'''
<p>One tribunal decision governs the whole design. Air Canada argued that its chatbot was a separate
legal entity responsible for its own statements. The tribunal rejected that, and the question it
asked instead is the one to build against: were <strong>reasonable steps</strong> taken to ensure the
information was accurate?</p>
<p>That is a process question, and process questions have documentable answers. It is also why
<strong>a system prompt is not a control</strong>. "Never promise a refund" written in a prompt is a
suggestion to a probabilistic system. The same rule written as a validation check that blocks the
message is a control you can evidence. Regulators distinguish between the two, and so should your
architecture.</p>
<p>Two numbers then decide what you can actually build.</p>
<table>
<tr><th>Number</th><th>Reality</th></tr>
<tr><td><strong>Hallucination rate</strong></td><td>Measured at <strong>3&ndash;27%</strong> even in controlled chatbot settings. The tolerable rate in financial services is <strong>below 0.1%</strong>, because a fabricated fee, rate or account status is a regulatory incident rather than a bad customer experience.</td></tr>
<tr><td><strong>Containment</strong></td><td>Contact volume runs roughly 40% easy, 40% medium, 20% hard. Pilots reach 40&ndash;50% in 4&ndash;8 weeks, 55&ndash;65% by 8&ndash;16 weeks, and steady state at 6&ndash;9 months. <strong>Pushing past 70&ndash;75% without human review increases complaints</strong> as false resolutions compound.</td></tr>
</table>
{note("The gap between those two rows is the entire engineering problem. You cannot close a 3&ndash;27% hallucination rate to below 0.1% with a better prompt or a better model. You close it by making the system <strong>unable</strong> to state a number it did not retrieve &mdash; grounding, citation and a refusal path, enforced in code after generation. That is infrastructure, not prompt engineering, and it is the single most important sentence on this page.")}
'''

g_unit = f'''
<p>Every vendor in this category prices on a different unit, and the units are not comparable. This
is the same trap as the screening market in <a href="/fintech-ai/aml-compliance/build-sheet/">Build
Sheet 04</a>, but sharper, because here the unit definition is written by the party sending the
invoice.</p>
<table>
<tr><th>Unit</th><th>Who prices this way</th><th>What it hides</th></tr>
<tr><td><strong>Per resolution</strong></td><td>Intercom Fin, Fini, Zendesk</td><td>The vendor's definition of "resolved". This is your entire bill.</td></tr>
<tr><td><strong>Per conversation</strong></td><td>Salesforce Agentforce</td><td>You pay for failures too. At a 60% resolution rate, $2.00 per conversation is an effective <strong>$3.33 per resolution</strong>.</td></tr>
<tr><td><strong>Platform fee + usage</strong></td><td>Decagon, Ada, Sierra</td><td>A floor you pay before a single ticket, plus implementation.</td></tr>
<tr><td><strong>Per minute</strong></td><td>Voice vendors</td><td>Dead air. The vendor is paid for the time its own system spends thinking.</td></tr>
<tr><td><strong>Per message</strong></td><td>WhatsApp / Meta</td><td>Chattiness. A wordy agent costs more than a concise one, literally.</td></tr>
</table>
<p><strong>Normalise everything to cost per resolved contact before you compare a single quote.</strong>
Divide per-conversation rates by your realistic resolution rate. Divide per-minute rates by your
connect rate. Add the helpdesk seats that AI-only vendors assume you already have.</p>
{warn("<strong>Get the resolution definition in writing, as four specific questions.</strong> Does a conversation that escalated to a human still bill? Does a customer returning with the same question bill twice? Is resolution <em>confirmed by the customer</em> or <em>inferred from the chat ending</em>? What happens during an outage spike? At least one major vendor counts an <em>assumed</em> resolution when a customer simply leaves without replying &mdash; which is also, exactly, what a customer does when the answer was useless.")}
<p>Notice what that means. The vendor's billing metric and your quality metric are <em>the same
measurement</em>, and the vendor's version is biased toward billing you. The module makes the same
point from the quality side: teams count "no escalation" but never count "customer came back about
the same thing". <strong>Measure recontact yourself, on your own data, and never accept the
vendor's resolution number as a quality signal.</strong> Published resolution rates illustrate why:
one vendor cites roughly 71% across its customer base while independent reports place the figure
nearer 42&ndash;50%.</p>
'''

# ---------------------------------------------------------------- INDIGO

i_mat_chan = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>WhatsApp Business Platform</strong> <span class="pill p-indirect">indirect</span></td><td>The dominant Indian support channel. Reached through a Business Solution Provider, never directly.</td><td>developers.facebook.com/docs/whatsapp</td></tr>
<tr><td><strong>BSPs — Gupshup, AiSensy, Interakt, MyOperator, Twilio</strong></td><td>The layer between you and Meta. Template management, inbox, automation, billing.</td><td>vendor sites</td></tr>
<tr><td><strong>Exotel / Knowlarity / Plivo / Twilio</strong></td><td>Indian telephony and SIP. The dial tone under any voice agent.</td><td>exotel.com</td></tr>
<tr><td><strong>Yellow.ai / MyOperator / Ringg</strong></td><td>Indian voice agents with real multilingual coverage — Hindi, Hinglish and 9&ndash;20+ Indian languages with mid-call switching.</td><td>yellow.ai</td></tr>
<tr><td><strong>Intercom Fin</strong></td><td>Published per-outcome pricing, runs over an existing helpdesk without seats. The reference point for the category.</td><td>fin.ai/pricing</td></tr>
<tr><td><strong>Zendesk AI agents</strong></td><td>Native if you are already on Zendesk. Per automated resolution, with an overage model worth reading carefully.</td><td>zendesk.com</td></tr>
<tr><td><strong>Decagon / Sierra / Ada</strong></td><td>Enterprise agents, quote-only, no public pricing. All three need a separate helpdesk underneath for human workflows.</td><td>vendor sales</td></tr>
<tr><td><strong>Freshdesk / Zoho Desk</strong></td><td>Helpdesks with strong India presence and pricing, and data residency options that matter under DPDP.</td><td>freshworks.com</td></tr>
</table>
{note("The <strong>helpdesk dependency</strong> is the cost that pure-play AI vendors do not surface. Ada, Sierra and Decagon are agents, not helpdesks &mdash; human agent workflow still needs a platform underneath at roughly <strong>$55&ndash;$175+ per agent per month</strong>. Add that line to every quote before you compare.")}
'''

i_mat_ground = f'''
<p>The grounding layer is where the hallucination number gets closed, and almost all of it is
open source or something you already run.</p>
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>pgvector</strong> <span class="pill p-oss">oss</span></td><td>Vector search inside the Postgres you already operate. Correct answer for most teams; one fewer system to secure under DPDP.</td><td>github.com/pgvector/pgvector</td></tr>
<tr><td><strong>Qdrant / Weaviate</strong> <span class="pill p-oss">oss</span></td><td>Dedicated vector stores. Worth it at scale or when you need hybrid filtering the database cannot do.</td><td>qdrant.tech</td></tr>
<tr><td><strong>BM25 (Elasticsearch / OpenSearch)</strong> <span class="pill p-oss">oss</span></td><td>Keyword retrieval. Hybrid keyword-plus-vector beats either alone, and it is the part teams skip.</td><td>opensearch.org</td></tr>
<tr><td><strong>Ragas / DeepEval / promptfoo</strong> <span class="pill p-oss">oss</span></td><td>Evaluation harnesses: faithfulness, answer relevance, regression suites you can run in CI.</td><td>docs.ragas.io</td></tr>
<tr><td><strong>Langfuse / Phoenix</strong> <span class="pill p-oss">oss</span></td><td>Tracing every generation with its retrieved context. This <em>is</em> your audit record.</td><td>langfuse.com</td></tr>
<tr><td><strong>Presidio</strong> <span class="pill p-oss">oss</span></td><td>PII detection and redaction before text leaves your boundary for a model.</td><td>github.com/microsoft/presidio</td></tr>
<tr><td><strong>ISO 42001</strong></td><td>AI management system certification. Increasingly expected by financial regulators as governance distinct from SOC 2 or ISO 27001.</td><td>iso.org</td></tr>
</table>
'''

code_ground = code('Python — the refusal gate: a control, not a prompt', r'''import re
from decimal import Decimal

# Numbers, money, dates and account states may ONLY appear in an answer if they
# came from a retrieved source or a system call. This runs AFTER generation and
# BEFORE the message is sent. It is a control because it blocks; a prompt is not
# a control because it advises.

NUMERIC = re.compile(r'(?:₹|Rs\.?\s?|INR\s?)?\d[\d,]*(?:\.\d+)?%?')
SAFE_PHRASES = {"24 hours", "7 working days", "one", "two", "three"}  # policy text

def gate(answer: str, grounded_values: set[str], sources: list[dict]) -> dict:
    # 1. every number in the answer must be traceable to retrieved content
    found = {m.group(0).strip() for m in NUMERIC.finditer(answer)}
    ungrounded = {v for v in found
                  if v not in grounded_values and v.lower() not in SAFE_PHRASES}
    if ungrounded:
        return {"send": False, "reason": "ungrounded_numeric",
                "detail": sorted(ungrounded), "action": "escalate"}

    # 2. commitments the business has not authorised the agent to make
    FORBIDDEN = [r"\bwe (?:will|shall) refund\b", r"\bguarantee[ds]?\b",
                 r"\bapproved\b", r"\bwaive[dr]?\b", r"\bno charge\b"]
    for pat in FORBIDDEN:
        if re.search(pat, answer, re.I):
            return {"send": False, "reason": "unauthorised_commitment",
                    "detail": pat, "action": "escalate"}

    # 3. no sources retrieved => the model is answering from parameters alone
    if not sources:
        return {"send": False, "reason": "no_grounding", "action": "escalate"}

    # 4. retrieval confidence floor. Below it, refuse rather than guess.
    if max(s["score"] for s in sources) < 0.62:
        return {"send": False, "reason": "weak_retrieval", "action": "escalate"}

    return {"send": True, "sources": [s["id"] for s in sources]}

# WHAT TO CHECK
# [ ] the gate runs on the OUTPUT, after generation. A rule enforced only in the
#     prompt cannot be evidenced to a regulator and cannot be unit tested
# [ ] refusal is a FIRST-CLASS PATH, not an error. "I need to get a colleague to
#     confirm that" is a good answer. A confident wrong number is not
# [ ] every block is logged with the reason code. The distribution of reason
#     codes over time is your early warning that scope has crept
# [ ] grounded_values is built from the RETRIEVED TEXT and API responses, not
#     from the model's own output. Otherwise it grounds itself
# [ ] the confidence floor is a versioned, approved, dated setting. Changing it
#     is a control change -- same discipline as an AML threshold
# [ ] test with adversarial inputs: "so you're saying my fee is waived, right?"
#     Confirmation-seeking is how customers extract commitments
# [ ] intents that NEVER reach a generative model are routed before this runs --
#     card block, fraud report, bereavement, complaint, hardship
''')

i_ground = f'''
<h3 id="s-indigo-gate">Grounding is the product</h3>
<p>Retrieval-augmented generation is described everywhere as a way to give a model your documents.
For a regulated firm it is better understood as a way to make certain answers <em>impossible</em>.
The retrieval is half of it; the gate on the way out is the half that matters.</p>
{code_ground}
<p><strong>The gotcha nobody documents:</strong> the numbers the model gets wrong are almost never
the ones in your knowledge base. They are the ones it interpolates &mdash; a plausible processing
time, a plausible fee, a plausible interest rate that sits comfortably between two real ones. A
faithfulness score computed over your document set will not catch it, because the statement is not
contradicted by any document; it is simply unsupported by all of them. That is why the gate checks
for <em>presence in retrieved content</em> rather than <em>absence of contradiction</em>.</p>

<h3 id="s-indigo-never">The intents that must never reach a generative model</h3>
<p>Route these deterministically, before any model sees them. They are not hard to classify and the
downside of getting one wrong is not a bad review:</p>
<ul>
<li><strong>Card block, account freeze, fraud report.</strong> Time-critical, and a wrong answer is a
financial loss the customer will attribute to you.</li>
<li><strong>Bereavement and account closure on death.</strong> There is no acceptable generated
response here.</li>
<li><strong>Hardship and collections.</strong> Regulated speech. See below.</li>
<li><strong>Anything that is a complaint.</strong> The hard part is recognition &mdash; customers do
not say "I wish to lodge a complaint", they say "this is the third time". Classify for complaint
signals separately from intent, and err toward logging one.</li>
<li><strong>Vulnerability signals.</strong> Distress, confusion, mentions of illness or coercion.</li>
</ul>
'''

code_contact = code('Python — collections contact guard, RBI conduct rules as code', r'''from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

# RBI responsible business conduct directions on recovery, effective 1 July 2026.
# These are hard gates. A system prompt telling an agent "do not call at night"
# is not a control; this function is.

WINDOW_START, WINDOW_END = time(8, 0), time(19, 0)

def may_contact(account, channel: str, now=None) -> dict:
    now = now or datetime.now(IST)
    t = now.timetz().replace(tzinfo=None)

    # The window applies to DIGITAL channels too. An automated SMS, WhatsApp
    # message or push notification at 22:00 is a reportable violation, not a
    # grey area -- and automated schedulers are exactly how firms breach it.
    if not (WINDOW_START <= t <= WINDOW_END):
        return {"allow": False, "reason": "outside_0800_1900_IST", "channel": channel}

    # Recovery must be SUSPENDED on an account with an open grievance.
    if account.grievance_open:
        return {"allow": False, "reason": "grievance_pending_recovery_suspended"}

    # Field visits require prior consent. No consent, no visit.
    if channel == "field_visit" and not account.visit_consent_on_file:
        return {"allow": False, "reason": "no_prior_consent_for_visit"}

    # Persistent contact is prohibited. Cap and count, per channel, per window.
    if account.contacts_today(channel) >= account.channel_cap(channel):
        return {"allow": False, "reason": "frequency_cap"}

    # Hardship disclosed ANYWHERE -- including to the support team -- pauses
    # collections contact. This is the integration that is usually missing.
    if account.hardship_flag:
        return {"allow": False, "reason": "hardship_flagged", "action": "human_review"}

    return {"allow": True, "must_record": channel in ("voice", "field_visit"),
            "retain_until": (now + timedelta(days=183)).date().isoformat()}

# WHAT TO CHECK
# [ ] the window is evaluated in IST from the ACCOUNT's perspective, and at SEND
#     time, not at queue time. A batch queued at 18:55 that dispatches at 19:20
#     has breached
# [ ] digital channels are inside the gate. Most implementations gate calls and
#     leave the SMS scheduler outside it
# [ ] recovery calls and visits are RECORDED and retained 6 months, or until
#     related litigation concludes -- whichever is longer
# [ ] agents are IIBF-certified and identify themselves; the identification is
#     in the recording
# [ ] NO remote disabling of a financed device. This is prohibited outright
# [ ] grievance: acknowledged in 24h, resolved in 30 days, recovery suspended on
#     that account while it is pending
# [ ] the hardship flag is shared between SUPPORT and COLLECTIONS. Different
#     vendors and different databases is the usual cause of a technically
#     compliant message that is indefensible in substance
# [ ] outsourcing does not outsource the obligation -- your agency's breach is
#     yours. Audit their logs, do not accept their assurance
''')

i_collections = f'''
<p>Collections is the part of customer operations where the AI question stops being about quality and
starts being about legality. <strong>Collections speech is regulated speech.</strong></p>
<p>The RBI responsible business conduct directions on recovery took effect on 1 July 2026 and they
are specific enough to implement directly.</p>
{code_contact}
<p><strong>The gotcha nobody documents:</strong> the contact window is usually implemented on the
dialler and not on the scheduler. Voice calls get gated correctly because the dialler is the obvious
place to put the rule. The automated SMS reminder, the WhatsApp utility template and the push
notification go out through completely different systems, built by a different team, with no window
logic at all. The directions cover digital contact. A reminder at 22:00 is a violation regardless of
which service sent it.</p>
{warn("<strong>Vicarious liability is the clause that changes procurement.</strong> Outsourcing collections does not outsource the obligation. If your recovery agency breaches the window, or fails to record a call, or intimidates a customer, that is your regulatory exposure and your Internal Ombudsman's problem. Contract for log access and audit it yourself. An agency's assurance that it is compliant is not evidence that it is.")}
'''

code_wa = code('Python — WhatsApp cost accounting, and why chattiness is now a line item', r'''from datetime import datetime, timedelta

# Meta India list rates, effective 1 July 2026, per DELIVERED message,
# before your BSP's platform fee and before 18% GST.
RATE_INR = {"marketing": 0.8631, "utility": 0.1150, "authentication": 0.1150}
GST = 1.18

# From 1 October 2026 Meta charges for SERVICE messages -- replies inside the
# 24-hour customer service window -- at the utility/authentication rate. They
# have been free since November 2024. For a support-heavy business this turns
# the single biggest message category from free into a per-message cost.
SERVICE_FREE_UNTIL = datetime(2026, 10, 1)

def cost_of_conversation(messages, sent_at=None) -> dict:
    sent_at = sent_at or datetime.now()
    total, lines = 0.0, []
    for m in messages:
        cat = m["category"]
        if cat == "service":
            rate = 0.0 if sent_at < SERVICE_FREE_UNTIL else RATE_INR["utility"]
        else:
            rate = RATE_INR[cat]
        total += rate
        lines.append((cat, round(rate, 4)))
    meta_cost = total * GST
    return {"messages": len(messages), "lines": lines,
            "meta_inr_incl_gst": round(meta_cost, 2),
            "note": "BSP platform fee is additional and is the only thing that "
                    "differs between BSPs -- Meta's rate is identical for all"}

# WHAT TO CHECK
# [ ] you are comparing like with like. Quoted WhatsApp prices differ because
#     some include GST, some include BSP markup and some are Meta list. Ask
#     which of the three any number is, every time
# [ ] marketing is ~7.5x utility. A support message mis-templated as marketing
#     costs 7.5x and is also the wrong category for compliance
# [ ] from 1 Oct 2026, model your AI agent's REPLY COUNT, not just conversation
#     count. An agent that sends five short messages costs five times one that
#     sends one clear message
# [ ] Click-to-WhatsApp entry opens a 72-hour free window; ordinary inbound opens
#     24 hours. Route accordingly
# [ ] the rate is set by the RECIPIENT's country, not yours. An Indian business
#     messaging a UK number pays the UK rate, which is many times higher
# [ ] template rejection and quality-rating downgrades are real operational
#     costs. A downgraded number gets throttled, which is an outage you cannot
#     fix with engineering
''')

i_channels = f'''
<h3 id="s-indigo-wa">WhatsApp: the number that changes on 1 October 2026</h3>
<p>WhatsApp is the default support channel for Indian consumer fintech, and its cost model has just
been rewritten twice. Meta moved from conversation-based to <strong>per-message</strong> pricing
during 2025, which made every older pricing guide wrong. The second change lands in weeks.</p>
{code_wa}
{warn("<strong>The 24-hour customer service window has been free since November 2024. From 1 October 2026 Meta charges per service message at the utility rate.</strong> For a business whose WhatsApp volume is mostly customers asking questions, the category that was free becomes the category you pay for. Model it before it lands, because it creates a design incentive that did not exist before: <strong>a verbose AI agent is now measurably more expensive than a concise one</strong>, and most agents are tuned for warmth rather than brevity.")}
<p>On BSP selection there is one fact that settles most of the evaluation:
<strong>Meta's per-message rate is identical whichever BSP you use.</strong> The only things that
differ are the platform fee, the markup on Meta's rate, and the setup charge &mdash; which runs from
zero to around &#8377;25,000. Compare those three and the inbox quality. Do not let a BSP present
Meta's rate as though it were their pricing.</p>

<h3 id="s-indigo-voice">Voice, and the dead-air problem</h3>
<p>Indian support and collections are voice-heavy, and voice is where the per-unit trap bites
hardest. Headline rates run <strong>&#8377;2&ndash;&#8377;12 a minute</strong> with
<strong>&#8377;3&ndash;&#8377;6</strong> the common mid-market band. Effective cost in production is
commonly reported at <strong>two to four times</strong> the headline once you add the platform fee,
telephony markup over TRAI rates, and connect-rate losses. A &#8377;3/min quote is often
&#8377;6&ndash;&#8377;9/min in practice.</p>
<p><strong>The gotcha nobody documents:</strong> per-minute pricing pays the vendor for its own
latency. If the agent takes twenty seconds to process a response, or asks an unnecessary confirmation
question, you are billed for that. Ask every voice vendor for their
<strong>average silence-to-speech ratio across a sample of 1,000 real calls</strong>. It is a fair
question, it is measurable, and the reaction to being asked tells you most of what you need to
know.</p>
<p>Two more things to pin down before signing. A per-minute rate should bundle all four layers
&mdash; speech-to-text, the model, text-to-speech and telephony &mdash; and some vendors quote one
and bill the rest. And if pricing is per <em>attempt</em> rather than per connected call, Indian
outbound connect rates of 30&ndash;65% mean you are paying for a lot of ringing.</p>
'''

# ---------------------------------------------------------------- COST

cost_rows = [
 ("AI agent &mdash; per resolution", "direct",
  "<strong>Intercom Fin $0.99</strong> per outcome (50-outcome monthly minimum; $49/mo entry "
  "including 50; runs over an existing helpdesk, no seats required). <strong>Zendesk $2.00</strong> "
  "per automated resolution. <strong>Fini $0.89 / $0.69 / $0.49</strong> by tier. "
  "$0.50&ndash;$1.00 per resolved conversation with no platform fee is competitive for mid-market."),
 ("AI agent &mdash; per conversation", "direct",
  "<strong>Salesforce Agentforce ≈ $2.00</strong>. <strong>Divide by your resolution rate before "
  "comparing</strong> &mdash; at 60% that is an effective <strong>$3.33 per resolution</strong>."),
 ("AI agent &mdash; enterprise", "direct",
  "Quote-only. <strong>Sierra</strong>: year one commonly estimated at <strong>$200k&ndash;$350k+</strong>, "
  "annual contracts from ~$150k, implementation <strong>$50k&ndash;$200k</strong>, 3&ndash;7 month "
  "deployments. <strong>Decagon</strong>: publishes nothing; platform fee around $50k/yr, "
  "third-party contract data from ~$105k to a ~$432k median. <strong>Ada</strong> from ~$30k/yr."),
 ("Helpdesk underneath", "direct",
  "<strong>$55&ndash;$175+ per agent per month.</strong> AI-only vendors need one and rarely mention "
  "it. Add it to every quote before comparing."),
 ("WhatsApp &mdash; Meta rate (India)", "direct",
  "Per delivered message, list, effective 1 July 2026: <strong>marketing &#8377;0.8631</strong>, "
  "<strong>utility &#8377;0.1150</strong>, <strong>authentication &#8377;0.1150</strong>. "
  "<strong>+18% GST</strong> (marketing is &#8377;1.0185 with GST). Marketing is ~7.5&times; "
  "utility. Marketing rates rose ~10% during 2026; utility and authentication held."),
 ("WhatsApp &mdash; service messages", "direct",
  "<strong>Free until 1 October 2026</strong>, then charged at the utility rate. This is the line "
  "that changes support economics. Inbound opens a 24-hour window; Click-to-WhatsApp opens 72 hours."),
 ("WhatsApp &mdash; BSP fee", "direct",
  "Platform fee plus any markup, on top of Meta. Setup <strong>&#8377;0&ndash;&#8377;25,000</strong>. "
  "<strong>Meta's rate is the same through every BSP</strong> &mdash; the markup is the only variable."),
 ("Voice AI (India)", "direct",
  "Headline <strong>&#8377;2&ndash;&#8377;12/min</strong>, mid-market <strong>&#8377;3&ndash;&#8377;6</strong>. "
  "<strong>Effective 2&ndash;4&times; headline</strong> in production. Per connected call "
  "&#8377;4&ndash;&#8377;15; per successful outcome &#8377;8&ndash;&#8377;25. Enterprise scale "
  "improves it &mdash; roughly &#8377;9.94/min at 25,000 min/month falling to ~&#8377;6/min at "
  "25 lakh. Implementation can reach seven figures. +18% GST."),
 ("Human benchmark (India)", "direct",
  "Fully loaded telecaller: <strong>&#8377;30,000&ndash;45,000/mo</strong> BPO, "
  "<strong>&#8377;45,000&ndash;70,000</strong> in-house mid-tier, "
  "<strong>&#8377;70,000&ndash;1,20,000</strong> in-house senior BFSI. Roughly 80&ndash;120 dials a "
  "day, <strong>25&ndash;40 meaningful connects</strong>, 22 working days. Compute your own cost per "
  "connect before believing any deflection business case."),
 ("Grounding stack", "oss",
  "<strong>Infrastructure only.</strong> pgvector, BM25, Ragas, Langfuse, Presidio cost nothing. "
  "Model inference is the variable, and it is small next to per-resolution vendor pricing at "
  "moderate volume."),
]

i_cost = f'''
{registry("Customer operations &mdash; cost per unit", cost_rows, V)}
{warn("<strong>Watch the overage terms, not the rate.</strong> From 1 January 2026 one major vendor bills overage automatically each month for customers on non-standard contracts, with overage <em>on by default</em>, no cap and no grace period. It can be switched off &mdash; which pauses the AI agent at the limit instead, turning a billing setting into an availability decision. Another charges an AI-resolved ticket as <em>both</em> a ticket and a resolution. Read the metering clause with the same attention you give the rate.")}
<p>One more note on vendor stability rather than price: the AI support market is consolidating. A
roughly $3.6 billion acquisition of a major agent vendor was agreed in June 2026 and had not closed
at the time of writing, with pricing unchanged so far. That is not a reason to avoid anyone, but it
is a reason to ask what happens to your contract and your data on a change of control.</p>
'''

# ---------------------------------------------------------------- AMBER

a_combos = f'''
<table>
<tr><th>Combination</th><th>Works because</th></tr>
<tr><td>Deterministic intent routing &rarr; grounded generation &rarr; output gate</td><td>The dangerous intents never reach a model, and what the model does produce cannot state an unretrieved number.</td></tr>
<tr><td>Assist before deflect</td><td>A human stays accountable while you learn your own failure modes on real traffic. Cheaper to be wrong.</td></tr>
<tr><td>Hybrid retrieval: BM25 + vector</td><td>Keyword catches product names, policy codes and error codes that embeddings blur. Skipping it is the most common retrieval mistake.</td></tr>
<tr><td>Tracing + evaluation suite in CI</td><td>Every generation stored with its retrieved context is simultaneously your debugging tool and your "reasonable steps" evidence.</td></tr>
<tr><td>One hardship flag shared by support and collections</td><td>Closes the integration gap that produces compliant messages which are indefensible in substance.</td></tr>
<tr><td>Recontact rate measured alongside containment</td><td>The only honest deflection metric, and the one the vendor's billing definition is biased against.</td></tr>
</table>
<h3 id="s-amber-conflict">Combinations that conflict</h3>
<ul>
<li><strong>A system prompt as your compliance control.</strong> Not evidenceable, not testable, not a control. Put the rule in code that blocks.</li>
<li><strong>Generative answers on card block, fraud, bereavement, hardship or complaints.</strong> Route these deterministically. There is no upside.</li>
<li><strong>Chasing containment past 70&ndash;75% without human review.</strong> Complaint volume rises as false resolutions compound, and complaints are a regulated process with their own clocks.</li>
<li><strong>Accepting the vendor's resolution rate as a quality metric.</strong> It is a billing metric that happens to share a name.</li>
<li><strong>Gating the dialler but not the SMS scheduler.</strong> The recovery contact window covers digital channels.</li>
<li><strong>A verbose agent on WhatsApp after 1 October 2026.</strong> Chattiness is now billed per message.</li>
<li><strong>Collections and support on separate vendors with no shared flag.</strong> This is the failure that reaches the ombudsman.</li>
</ul>
'''

a_builds = f'''
<h3 id="s-amber-exp">Strong and expensive</h3>
<p><strong>Build:</strong> enterprise AI agent (Sierra or Decagon class) with white-glove
configuration, a full helpdesk underneath, an Indian voice platform with real multilingual coverage,
a separate collections platform, and ISO 42001 certification.</p>
<p><strong>Use when:</strong> contact volume is in the millions, you have a supervisory relationship
to defend, and vendor accountability has value independent of cost.</p>
<p><strong>Cost shape:</strong> six figures in USD annually before usage, plus implementation in the
$50k&ndash;$200k band, plus 3&ndash;7 months before it answers a live customer.</p>
<p><strong>Trade:</strong> you cannot change a refusal threshold on a Friday afternoon. Every
adjustment goes through someone else's release process, and the liability stays with you regardless
&mdash; contracts in this category have been moving exposure toward the deploying firm, not the
vendor.</p>

<h3 id="s-amber-def">Strong and reasonable &mdash; the default</h3>
<p><strong>Build:</strong> published-price AI agent (Fin class) over the helpdesk you already run
&rarr; deterministic routing that keeps the dangerous intents away from it &rarr; hybrid retrieval on
pgvector against a knowledge base you own &rarr; <strong>your own output gate</strong> &rarr; tracing
with Langfuse and an evaluation suite in CI &rarr; WhatsApp through a BSP chosen on markup &rarr;
voice only where voice is genuinely the channel.</p>
<p><strong>Use when:</strong> you have engineers, support volume is material, and you need to be able
to explain any individual answer.</p>
<p><strong>Cost shape:</strong> roughly a dollar per resolution plus per-message channel costs plus
near-zero for the grounding stack.</p>
<p><strong>Trade:</strong> you own the gate, the evaluation suite and the knowledge base quality.
That is the right trade, because those three are what a regulator asks about and none of them is
something a vendor can own on your behalf.</p>
{note("Why the gate stays in-house even when the agent is bought. The vendor's guardrails protect the vendor's reputation; yours must protect your licence. They are not the same specification, and the second one has to be inspectable by your compliance team and testable in your CI. Buying the agent and building the gate is the sensible division.")}

<h3 id="s-amber-lean">Strong and lean</h3>
<p><strong>Build:</strong> <strong>assist only</strong> &mdash; retrieval and drafting for human
agents, no autonomous customer-facing answers &rarr; a well-maintained knowledge base &rarr; WhatsApp
through a low-markup BSP with utility templates only &rarr; one shared hardship flag &rarr; a written
escalation and complaint policy.</p>
<p><strong>Use when:</strong> early, or regulated enough that an autonomous answer is not worth the
first incident.</p>
<p><strong>Cost shape:</strong> channel costs plus modest inference. No per-resolution fee at all.</p>
<p><strong>Trade:</strong> no deflection, so support cost scales with volume. Accept it. An assist
deployment that makes ten agents meaningfully faster is a real result, it carries almost none of the
regulatory exposure, and it produces the labelled data that makes a later deflection project work.</p>
{warn("Whichever grade you pick: <strong>capture CSAT at the point of resolution, not 24 hours later</strong>, and track &ldquo;wrong answer given&rdquo; as a share of escalations. If that figure passes roughly 3%, stop expanding scope and fix retrieval. Expanding coverage while accuracy degrades is the signature of over-automation, and it is visible in complaint volume months before it is visible in a dashboard.")}
'''

a_next = f'''
<p>The escalation path above you, and worth knowing before you need it: complaints acknowledged in
24 hours and resolved in 30 days, an Internal Ombudsman at larger institutions, and then
<strong>RB-IOS 2026</strong>, effective 1 July 2026, with awards up to &#8377;30 lakh for
consequential loss and &#8377;3 lakh for time, expense and harassment. Criminal intimidation under
BNS Section 351 runs in parallel for collections conduct.</p>
<p>What reaches the RBI CMS portal about you is a supervisory signal. The useful internal metric is
not complaint volume &mdash; it is the share of complaints that a customer had to escalate because
your first response missed that it was a complaint at all.</p>
<h3 id="s-amber-next">What this feeds</h3>
<div class="mod-grid">
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>"Where is my refund" is the highest-volume contact reason in Indian fintech. Reconciliation quality <em>is</em> support volume.</p></a>
<a href="/fintech-ai/identity-onboarding/" class="mod-card"><div class="mod-num">MODULE 01</div><h3>Identity &amp; Onboarding</h3><p>Failed KYC is the second-highest contact driver, and the hardest to answer without disclosing why.</p></a>
<a href="/fintech-ai/fraud-risk/" class="mod-card"><div class="mod-num">MODULE 03</div><h3>Fraud &amp; Risk</h3><p>False declines arrive as angry contacts. Step-up rather than block is a support decision as much as a risk one.</p></a>
<a href="/fintech-ai/governance/" class="mod-card"><div class="mod-num">MODULE 09</div><h3>Governance</h3><p>ISO 42001, model change control, and the evidence pack that makes "reasonable steps" a documented answer.</p></a>
</div>
{warn("Everything on this page is illustrative. Customer communications from a regulated firm carry conduct obligations, and collections speech is regulated speech with criminal exposure attached. Nothing here is legal advice. Have your escalation policy, your refusal thresholds and your collections contact logic reviewed by qualified counsel and your compliance officer before a real customer sees them.")}
'''

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to read this build sheet", g_read),
   ("The principle, and the two numbers", g_principle),
   ("The unit is the trap", g_unit),
 ],
 'indigo': [
   ("Raw materials — channels and agent platforms", i_mat_chan),
   ("Raw materials — grounding and evaluation", i_mat_ground),
   ("How to use each one — grounding and the gate", i_ground),
   ("How to use each one — channels and their economics", i_channels),
   ("How to use each one — collections", i_collections),
   ("Cost per unit", i_cost),
 ],
 'amber': [
   ("Best combinations", a_combos),
   ("Three recommended builds", a_builds),
   ("What next", a_next),
 ],
}

TITLE = "Customer Operations Build Sheet"
META  = ("Every channel, AI agent and grounding tool for support: how to use each one, what it costs "
         "per resolution, and three recommended builds.")
LEAD  = ("Every channel, agent platform and grounding component a support stack needs. What each one "
         "is for, the first working call, the gotcha nobody documents, real cost per unit, and three "
         "recommended builds at three budgets.")

print(f"title len: {len(TITLE + ' | Clarigital')}")
print(f"meta len : {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/customer-operations/build-sheet",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Build Sheet 06",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI"),
            ("/fintech-ai/customer-operations/", "Customer Operations")],
  lanes  = lanes,
)
