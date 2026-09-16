#!/usr/bin/env python3
# Session 85 — PRODUCT GUIDE 12: Robo-advisory
# SEBI. Depth on the IA framework stays in Build Sheet 07 and is LINKED.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product: software that tells someone what to invest in,
and then either helps them do it or deliberately does not. Goal in, portfolio out, rebalanced over
time.</p>
<p>The regulator here is <strong>SEBI</strong>, not RBI, and the single most important thing to
understand arrives before any code: <strong>the product most teams have in mind cannot be built by
one entity.</strong></p>
''' + warn("<strong>Advice and execution were structurally separated, and it was deliberate.</strong> A registered investment adviser advises and <strong>may not execute</strong>. An <strong>Execution Only Platform</strong> executes direct mutual fund plans and <strong>may not advise</strong>. The free-advice-plus-one-tap-buy product that several Indian platforms offered before 2023 is not one regulated activity that got harder &mdash; it is <strong>two regulated activities that may not sit in the same entity</strong>. Everything else on this page follows from that sentence.")

g_what = '''
<p>Before anything else, work out which of these you are. The answer determines your registration,
your revenue model, your liability and roughly 80% of your architecture:</p>
<table>
<tr><th>You are</th><th>You may</th><th>You may NOT</th><th>You are paid by</th></tr>
<tr><td><strong>Investment Adviser (IA)</strong></td><td>Recommend, plan, review</td><td><strong>Execute</strong></td><td><strong>The client.</strong> Fee-only, capped</td></tr>
<tr><td><strong>Research Analyst (RA)</strong></td><td>Publish research, model portfolios</td><td>Give personalised advice</td><td>Subscription</td></tr>
<tr><td><strong>Execution Only Platform (EOP)</strong></td><td>Transact <strong>direct plans</strong></td><td><strong>Advise</strong>, or touch regular plans</td><td>AMCs or investors, by category</td></tr>
<tr><td><strong>Distributor</strong></td><td>Sell <strong>regular</strong> plans</td><td>Advise</td><td><strong>Commission from the manufacturer</strong></td></tr>
<tr><td><strong>None of these</strong></td><td>Publish general education</td><td><strong>Anything a reasonable person reads as a recommendation</strong></td><td>Nobody, safely</td></tr>
</table>
''' + note("<strong>&ldquo;Robo-advisory&rdquo; is not a registration category.</strong> There is no robo licence, no lighter-touch digital regime, and no threshold below which an algorithm counts as a calculator. SEBI regulates the <em>activity</em>, and a program that recommends securities to a specific person on the basis of their circumstances is giving investment advice regardless of whether a human read it first.") + '''
<p><strong>What this is not:</strong></p>
<ul>
<li><strong>Not a way to avoid the fee cap.</strong> Advisory fees for individuals and HUFs are
capped, and that ceiling is the first number in the model. Build Sheet 07 works through why.</li>
<li><strong>Not safer because the advice came from a model.</strong> <strong>Using AI increases your
responsibility; it does not share it.</strong> Step 6.</li>
<li><strong>Not education because you called it education.</strong> Step 1.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Which entity are you?</strong></td><td>And is what you are planning actually advice.</td></tr>
<tr><td>2</td><td><strong>Register</strong></td><td>IA, EOP, or both through two entities.</td></tr>
<tr><td>3</td><td><strong>Onboard</strong></td><td>KYC, agreement, fee disclosure.</td></tr>
<tr><td>4</td><td><strong>Risk profiling</strong></td><td>Capacity and tolerance are different things.</td></tr>
<tr><td>5</td><td><strong>Recommend</strong></td><td><strong>And store what you excluded.</strong></td></tr>
<tr><td>6</td><td><strong>Deliver the advice</strong></td><td>With the AI disclosure, and a human who owns it.</td></tr>
<tr><td>7</td><td><strong>Execution</strong></td><td><strong>The wall, and how the client crosses it.</strong></td></tr>
<tr><td>8</td><td><strong>Review and audit</strong></td><td>Two clocks, and a line-wise annual audit.</td></tr>
</table>
''' + note("<strong>Steps 1, 5, 7 and 8 are the skipped ones.</strong> Steps 3, 4 and 6 are the parts that look like a product and a vendor will sell you all three. The registration question, the exclusions record, the execution wall and the audit trail are what an inspection is about.")

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Is what you are building actually advice?</h3>
<p>Three screen tests, and if any answer is yes you are probably in the advisory perimeter:</p>
<ul>
<li>Does the output use anything you know about <strong>this specific user</strong>?</li>
<li>Would a reasonable user read it as a recommendation?</li>
<li>Would you be comfortable if a regulator saw it <strong>without the disclaimer</strong>?</li>
</ul>
<p>The drift is always gradual and it is always the same sequence. A calculator gains a
&ldquo;based on your answers&rdquo; label. A fund table gains a default sort. A list gains a
&ldquo;popular with people like you&rdquo; badge. <strong>No single change looks like the moment you
started giving advice, and by the end you have.</strong></p>
''' + warn("<strong>&ldquo;For educational purposes only&rdquo; is not a defence, and there is a large order saying so.</strong> SEBI's December 2025 action against an unregistered advisory operation impounded roughly <strong>&#8377;546 crore</strong> and imposed a market ban. The regulator's position is that a disclaimer does not change what an activity is &mdash; inside a course, a private group, a newsletter or a chatbot reply. <strong>If the label is doing the compliance work, there is no compliance.</strong>") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; Register, and budget properly for it</h3>
<table>
<tr><th>Item</th><th>Position</th></tr>
<tr><td><strong>Supervisory body</strong></td><td><strong>IAASB &mdash; BSE Limited</strong>, appointed 25 July 2024 for five years. Your day-to-day counterparty, not SEBI</td></tr>
<tr><td><strong>Capital</strong></td><td>The old corporate net-worth requirement was <strong>abolished in December 2024</strong> and replaced by a <strong>deposit held under lien in favour of IAASB</strong></td></tr>
<tr><td><strong>Qualification</strong></td><td>Since <strong>November 2025, a graduate of any discipline</strong> with the required NISM certification may register. The finance-degree requirement is gone</td></tr>
<tr><td><strong>Fee</strong></td><td><strong>&#8377;15,000</strong> registration, within 15 days of approval. Budget <strong>3 to 6 months</strong> for the process</td></tr>
<tr><td><strong>Corporatisation trigger</strong></td><td><strong>300 clients OR &#8377;3 crore</strong> in fees in a financial year, whichever comes first. Notify immediately, then 3 months to in-principle and 3 more to complete &mdash; onboarding continues throughout</td></tr>
<tr><td><strong>Fee ceiling</strong></td><td><strong>&#8377;1.51 lakh per client per year</strong> for individuals and HUFs, inflation-revised</td></tr>
<tr><td><strong>If you also want to execute</strong></td><td>A <strong>separate entity</strong> registered as an EOP. See step 7</td></tr>
</table>
''' + note("Depth on the IA framework &mdash; part-time IA, compliance officer eligibility, the perimeter of &ldquo;investment advice&rdquo;, the tooling and the data licensing trap &mdash; lives in <a href=\"/fintech-ai/wealth-advisory/build-sheet/\"><strong>Build Sheet 07</strong></a> and is not repeated here. <strong>This page owns the workflow and the wiring.</strong>")

code_profile = code('Python — steps 4 and 5, profiling, the binding constraint, and the exclusions nobody stores', r'''from datetime import date, timedelta

# STEP 4. TWO DIFFERENT THINGS, ROUTINELY COLLAPSED INTO ONE SCORE.
#
#   CAPACITY  = how much loss this person can absorb without the plan failing.
#               Arithmetic. Horizon, income stability, dependants, emergency
#               fund, the size of this pot relative to everything else.
#   TOLERANCE = how much loss this person can live through without selling.
#               Psychology. Measured by questionnaire, and questionnaires are
#               optimistic on a day the market is calm.
#
# A single "risk score" that blends them is unusable, because the two failure
# modes are opposite: too much capacity wastes return, too much tolerance
# produces a complaint after a drawdown.

def risk_inputs(client):
    capacity = score_capacity(client)          # 1..7
    tolerance = score_tolerance(client)        # 1..7
    required = required_for_goal(client)       # what the GOAL demands
    binding = min(capacity, tolerance)         # never 'required'
    return {
        "capacity": capacity, "tolerance": tolerance,
        "required": required, "binding": binding,
        # The asymmetry that predicts complaints. Flag it, and record that
        # the conversation happened.
        "flag_review": tolerance - capacity >= 2,
        "goal_unreachable": required > binding,
    }

def resolve_goal(inp, client):
    """If the goal needs more risk than the client can bear, the GOAL changes
    -- horizon, contribution or target -- not the portfolio. This is exactly
    the constraint an optimiser will quietly relax if you let it."""
    if not inp["goal_unreachable"]:
        return {"action": "proceed"}
    return {"action": "renegotiate_goal",
            "options": ["extend_horizon", "raise_contribution", "lower_target"],
            "not_an_option": "raise_risk_above_binding"}

# STEP 5. THE RECOMMENDATION, AND THE PART EVERYONE DROPS.
def recommend(universe, inp, policy):
    included, excluded = [], []
    for f in universe:
        why = exclusion_reason(f, inp, policy)   # ONE reason, the first that bites
        (excluded if why else included).append({"fund": f["id"], "reason": why}
                                               if why else {"fund": f["id"]})
    return {
        "as_of": date.today().isoformat(),
        "binding_constraint": inp["binding"],
        "universe_size": len(universe),
        "included": included,
        # "Why was this fund never recommended to this client?" has a correct
        # answer and it CANNOT be recomputed later, because the catalogue, the
        # policy and the client's profile will all have moved.
        "excluded": excluded,
        "policy_version": policy["version"],
        "universe_snapshot_hash": sha256_of(universe),
    }

# WHAT TO CHECK
# [ ] capacity and tolerance stored SEPARATELY, and both shown to the client
# [ ] 'required' is never a permission. If the goal needs more risk than the
#     client can bear, the goal changes
# [ ] tolerance exceeding capacity by two bands or more is flagged, the
#     conversation is had, and the fact that it was had is recorded
# [ ] store EXCLUSIONS, not just the recommendation. Cheap to write, and the
#     difference between inspection-ready and inspection-panicked
# [ ] store the universe as it stood, not a pointer to a catalogue that
#     changes weekly
# [ ] a risk profile has an expiry. So does a recommendation. They are not
#     the same clock -- see step 8
''')

i_step345 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; Onboard</h3>
<p>KYC, the advisory agreement, and the fee disclosure in writing before any advice. Nothing exotic,
and one thing worth building properly on day one: <strong>the client should be able to see the fee
they are paying as a rupee figure, not only as a percentage</strong>. Against a ceiling of
&#8377;1.51 lakh a year, the absolute number is the one that gets questioned later.</p>

<h3 id="s-indigo-s4">Steps 4 and 5 &mdash; Profiling and the recommendation</h3>
''' + code_profile + '''
<p><strong>The gotcha that separates a defensible product from a pretty one:</strong>
<strong>store the exclusions.</strong> Every robo-advisor stores what it recommended. Almost none
stores what it ruled out and why, because at build time the excluded set looks like the absence of
data rather than data.</p>
<p>It is not. <em>&ldquo;Why was this fund never recommended to this client?&rdquo;</em> has a correct
answer, it is the question an inspection asks, and it <strong>cannot be reconstructed later</strong>
&mdash; the catalogue changes weekly, the policy changes quarterly, and the client&rsquo;s profile
changes annually. A few kilobytes per recommendation buys an answer that no amount of effort
afterwards can.</p>
'''

code_wall = code('Python — steps 6 to 8, the AI disclosure, the execution wall, and two clocks', r'''# STEP 6. DELIVERY, AND THE DISCLOSURE.
# SEBI (Intermediaries) (Amendment) Regulations, 2025 -- notified 10 February
# 2025 -- inserted Regulation 16C: a regulated entity is SOLELY liable for
# the AI/ML tools it uses, whether built in-house or bought. Liability covers
# data privacy and security, the integrity of the output, and compliance with
# all applicable law. There is no vendor to point at.

def deliver(advice, client, ai_used):
    return {
        "advice_id": advice["id"],
        "delivered_at_ist": now_ist(),
        "ai_disclosure": describe_ai_use(ai_used) if ai_used else None,
        # Disclosing the EXTENT of AI use is the requirement. "We use AI" is
        # not an extent. Which step, on what inputs, reviewed by whom.
        "reviewed_by": advice["qualified_reviewer"],   # a named person
        "rationale_plain_words": advice["rationale"],
        "rendered_document": advice["pdf_bytes"],      # what they SAW
    }

# STEP 7. THE WALL.
# An investment adviser may not execute. An Execution Only Platform may not
# advise. The client crosses between them; your code must not.

EOP_CATEGORY = {
    1: {"registers_with": "AMFI", "agent_of": "AMC",      "paid_by": "AMC"},
    2: {"registers_with": "stock_exchange_EOP_segment",
        "agent_of": "investor", "paid_by": "investor",
        "base_minimum_capital_rupees": 10_00_000},
}

def handoff(advice, client, eop):
    # Direct plans only. An EOP may not touch regular plans, and an entity may
    # not be Category 1 and Category 2 at once.
    assert all(f["plan"] == "DIRECT" for f in advice["included"]), "EOP: direct plans only"
    assert eop["entity_id"] != advice["adviser_entity_id"], "advice and execution: separate entities"
    return {
        "action": "present_to_client_for_authorisation",   # never auto-execute
        "client_authorises": True,
        "route": eop["entity_id"],
        "adviser_receives_from_amc": 0,        # fee-only. No commission, ever.
    }

# STEP 8. TWO CLOCKS, AND THEY ARE NOT THE SAME CLOCK.
def clocks(client, advice):
    return {
        "profile_valid_until": client["profiled_on"] + timedelta(days=365),
        "advice_valid_until": advice["as_of"] + timedelta(days=advice["shelf_life_days"]),
        # Suitability can lapse with NOBODY transacting: the fund changed
        # mandate, or the client's circumstances did. Both need a trigger.
        "watch": ["mandate_change", "life_event", "drawdown_breach"],
    }

def monitoring_record(run):
    # Record the runs that found NOTHING. An absence of records is
    # indistinguishable from an absence of monitoring, including to you.
    return {"ran_at_ist": now_ist(), "clients_checked": run["n"],
            "exceptions": run["exceptions"], "no_exception_is_a_result": True}

# WHAT TO CHECK
# [ ] the adviser entity receives nothing from any product manufacturer. Not
#     a rebate, not a marketing fee, not a platform contribution
# [ ] no auto-execution. The client authorises, every time
# [ ] a fund changing mandate re-checks EVERY client holding it. Suitability
#     regresses without anyone transacting
# [ ] glide paths beat annual reviews -- a yearly step-down is wrong for 364
#     days and most wrong in the year before the client needs the money
# [ ] the AI disclosure names the STEP and the INPUTS, not the vendor
# [ ] the annual compliance audit is LINE-WISE against every provision, by a
#     CA, CS or CMA. Build the evidence as you go or reconstruct it in March
''')

i_step678 = '''
<h3 id="s-indigo-s6">Steps 6 to 8 &mdash; Delivery, the wall, and the two clocks</h3>
''' + code_wall + '''
<p><strong>The AI position, stated plainly because it is the opposite of what most teams
assume:</strong> <strong>using AI increases your responsibility, it does not share it.</strong>
SEBI&rsquo;s position is that responsibility for AI-assisted advice sits with the adviser
<em>irrespective of the scale and scenario of AI usage</em>, that the integrity and transparency of
the derived advice must be ensured, and that <strong>the extent of AI use must be disclosed to the
client</strong>. Since <strong>10 February 2025</strong> that has had a regulation number:
<strong>Regulation 16C</strong> makes a regulated entity solely liable for AI and ML tools it uses,
<strong>whether developed in-house or procured</strong>.</p>
''' + warn("<strong>A fuller AI framework is coming and it is not final yet.</strong> SEBI put out a consultation on responsible AI in the securities market on <strong>20 June 2025</strong>, comments closed 11 July 2025, and the Chairman has since signalled a <strong>tiered framework by purpose of AI use, with kill switches and human oversight</strong>. Principles trailed in the consultation: board-level governance with technically competent senior oversight, third-party model oversight, independent audits and periodic review, disclosure to clients where AI directly affects them &mdash; advisory is named &mdash; and <strong>testing in an environment segregated from live</strong>. <strong>Not final at the time of writing.</strong> Design to it anyway, because Regulation 16C already puts the liability on you and the tiering only decides how much evidence you have to keep.") + '''

<h3 id="s-indigo-s7">The execution wall, in detail</h3>
<p>This is the structural fact of the product, so it is worth being precise about what sits on each
side.</p>
<table>
<tr><th></th><th>Category 1 EOP</th><th>Category 2 EOP</th></tr>
<tr><td><strong>Registers with</strong></td><td><strong>AMFI</strong></td><td><strong>Stock exchange</strong>, EOP segment, as a stock broker</td></tr>
<tr><td><strong>Acts as agent of</strong></td><td>The <strong>AMCs</strong></td><td>The <strong>investor</strong></td></tr>
<tr><td><strong>Integrates with</strong></td><td>AMCs and their RTAs</td><td>The exchange platform</td></tr>
<tr><td><strong>Paid by</strong></td><td>The AMCs</td><td>The investor</td></tr>
<tr><td><strong>Deposit</strong></td><td>&mdash;</td><td><strong>&#8377;10 lakh</strong> base minimum capital, not additive if already a member in another segment</td></tr>
</table>
<p><strong>Both categories: direct plans only, and you may not be both.</strong> An EOP may not
provide services for regular plans at all, and Category 2 may not act as a transaction aggregator for
direct plans.</p>
''' + note("<strong>The commercial consequence is the one to plan around.</strong> The pre-2023 Indian model was free advice subsidised by execution or distribution revenue. The separation removed the subsidy: <strong>the adviser is fee-only against a capped fee, and the execution platform cannot advise.</strong> If your plan assumes advice is a free acquisition channel for an execution business, it is a plan for a structure that no longer exists &mdash; and that was the point of the change, not a side effect of it.")

i_cost = registry("Robo-advisory &mdash; what it costs", [
 ("IA registration", "direct",
  "<strong>&#8377;15,000</strong> within 15 days of approval, plus a <strong>deposit held under lien "
  "in favour of IAASB</strong> since the corporate net-worth requirement was abolished in December "
  "2024. Budget <strong>3 to 6 months</strong> for the process itself."),
 ("A second entity, if you want to execute", "direct",
  "An EOP registration. Category 1 through AMFI; Category 2 as a stock broker with a "
  "<strong>&#8377;10 lakh base minimum capital deposit</strong>, not additive if you are already a "
  "member in another segment. <strong>Two entities, two sets of filings, two boards.</strong>"),
 ("The fee ceiling", "indirect",
  "<strong>&#8377;1.51 lakh per client per year</strong> for individuals and HUFs is the ceiling, and "
  "the realistic retail average is a fraction of it. <strong>It decides whether you can afford human "
  "oversight per client, which decides whether you can be advisory at all.</strong> Most Indian plans "
  "fail at this line rather than at the technology &mdash; worked through in Build Sheet 07."),
 ("The calculation layer", "direct",
  "<strong>Effectively free and should be built rather than bought.</strong> There is no meaningful "
  "optimiser market at Indian retail advisory scale. What a wealthtech platform actually sells is RTA "
  "plumbing, reporting and compliance workflow &mdash; evaluate it on that."),
 ("Market data", "direct",
  "<strong>Read the redistribution licence before you show a price to a client.</strong> A broker API "
  "licence generally covers your own use; showing that data to <em>your clients</em> is "
  "redistribution. Teams find this in diligence. Detail in Build Sheet 07."),
 ("Compliance audit", "direct",
  "<strong>Annual, line-wise against every provision</strong>, by a CA, CS or CMA, with adverse "
  "findings filed to timeline. Cheap if the evidence accumulates automatically; expensive if it is "
  "reconstructed in March."),
 ("AI, as a cost rather than a saving", "indirect",
  "<strong>Regulation 16C makes you solely liable</strong> for a model you bought. Add independent "
  "review, the disclosure surface, segregated testing and the evidence trail to the subscription "
  "price before comparing it against a human."),
], "September 2026") + note("<strong>The number that decides the business is clients per adviser.</strong> Everything above is fixed cost against a capped per-client fee, so the model lives or dies on how many clients one qualified person can oversee without the oversight becoming a rubber stamp. <strong>Work that number out in week one</strong>, the same way the Video KYC guide says to work out your audit rate &mdash; it is the ceiling on the business and almost nobody computes it until they hit it.")

a_builds = '''
<h3 id="s-amber-week">Education, honestly</h3>
<p><strong>Build:</strong> calculators and explanatory content that use <strong>nothing about the
individual user</strong>, with no default sort, no personalised badge and no &ldquo;based on your
answers&rdquo;.</p>
<p><strong>You get:</strong> a legitimate audience and no advisory perimeter. <strong>Run the three
screen tests every release</strong>, because the drift is gradual and nobody intends it.</p>

<h3 id="s-amber-proper">Fee-only advisory</h3>
<p><strong>Build:</strong> IA registration &rarr; onboarding with the fee in rupees &rarr; capacity
and tolerance profiled separately &rarr; recommendations with stored exclusions &rarr; AI extent
disclosed and a named reviewer &rarr; client authorises execution elsewhere &rarr; two review clocks
&rarr; evidence accumulating for the annual audit.</p>
<p><strong>Trade:</strong> a capped fee against a defensible position. <strong>The economics are hard
and the compliance is tractable</strong>, which is the opposite of what most teams expect.</p>

<h3 id="s-amber-big">Advisory and execution, two entities</h3>
<p><strong>Build:</strong> the above, plus a separately registered EOP, with a handoff that
<strong>presents for authorisation and never auto-executes</strong>, and an adviser entity that
receives nothing from any manufacturer.</p>
<p><strong>It breaks when:</strong> the two entities share a product team and the wall becomes a
diagram rather than a control. <strong>Assert it in code</strong> &mdash; the adviser entity id and
the execution entity id are different values, and a commission field on the adviser side is
hard-coded to zero.</p>
''' + note("If you take one thing from this page: <strong>store what you excluded, and why.</strong> It costs a few kilobytes per recommendation, it is the question an inspection actually asks, and it is the one artefact here that cannot be reconstructed at any price after the fact.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>One entity doing advice and execution</strong></td><td>Built to the pre-2023 model.</td><td>Two entities. Assert the ids differ in code.</td></tr>
<tr><td><strong>Capacity and tolerance blended into one score</strong></td><td>One number is easier to display.</td><td>Store and show both. The failure modes are opposite.</td></tr>
<tr><td><strong>The optimiser relaxed the risk constraint</strong></td><td>&ldquo;Required&rdquo; treated as an input.</td><td>The goal changes, never the binding constraint.</td></tr>
<tr><td><strong>Cannot say why a fund was never recommended</strong></td><td>Exclusions were never stored.</td><td>Store them at recommendation time, with the universe snapshot.</td></tr>
<tr><td><strong>&ldquo;We use AI&rdquo; as the disclosure</strong></td><td>Treated as a label rather than an extent.</td><td>Name the step, the inputs and the reviewer.</td></tr>
<tr><td><strong>Vendor blamed for a model output</strong></td><td>Procurement felt like risk transfer.</td><td>Regulation 16C: sole liability, in-house or bought.</td></tr>
<tr><td><strong>Auto-execution on acceptance</strong></td><td>It converts better.</td><td>Client authorises. Every time.</td></tr>
<tr><td><strong>Suitability lapsed with nobody transacting</strong></td><td>A fund changed mandate.</td><td>Mandate change re-checks every client holding it.</td></tr>
<tr><td><strong>No record of monitoring that found nothing</strong></td><td>Only exceptions were logged.</td><td>Log the run. Absence of records reads as absence of monitoring.</td></tr>
<tr><td><strong>&ldquo;Educational&rdquo; content that personalises</strong></td><td>Gradual drift, no single guilty release.</td><td>Three screen tests, every release.</td></tr>
<tr><td><strong>Commission received on the adviser side</strong></td><td>A platform rebate booked as revenue.</td><td>Fee-only. Hard-code the field to zero and test it.</td></tr>
</table>
'''

SRC=[('official','SEBI (Investment Advisers) Regulations and the 2024–25 amendments','the abolition of the corporate net-worth requirement in December 2024 and its replacement with a deposit held under lien in favour of the IAASB; BSE Limited appointed as IAASB on 25 July 2024 for five years; the ₹15,000 registration fee; the 300-client or ₹3 crore corporatisation trigger; the ₹1.51 lakh per client annual fee ceiling for individuals and HUFs; the November 2025 opening of registration to graduates of any discipline holding the required NISM certification; and the annual line-wise compliance audit by a CA, CS or CMA.','https://www.sebi.gov.in'),
 ('official','SEBI (Intermediaries) (Amendment) Regulations, 2025 — Regulation 16C','notified 10 February 2025 following a November 2024 consultation and the Board&rsquo;s 208th meeting. A SEBI-regulated entity is solely liable for AI and ML tools it uses, whether developed in-house or procured, covering investor data privacy, the integrity of AI output and compliance with applicable law. Parallel amendments were made on the market infrastructure and depository side.','https://www.sebi.gov.in'),
 ('official','SEBI regulatory framework for Execution Only Platforms','circular SEBI/HO/IMD/IMD-PoD-1/P/CIR/2023/86 dated 13 June 2023, effective 1 September 2023, with the base minimum capital circular of October 2023. Category 1 registering with AMFI as agent of the AMCs; Category 2 registering as a stock broker in the exchange EOP segment as agent of the investor with a ₹10 lakh deposit that is not additive across segments; direct plans only; no regular plans; and no transaction aggregation for direct plans by Category 2.','https://www.sebi.gov.in'),
 ('official','SEBI position on advisory and execution segregation','the requirement that advisory and distribution be segregated at client level, and at group level for non-individuals, and that an individual may not provide advice and execution simultaneously — the basis for a robo-advisory platform needing a separate entity.','https://www.sebi.gov.in'),
 ('official','SEBI consultation paper on responsible AI in the securities market','released 20 June 2025 with comments closed 11 July 2025: governance by technically competent senior management, third-party model oversight, data governance, independent audits and periodic review, disclosure to clients where AI directly affects them including advisory services, testing in an environment segregated from live, and a tiered approach by purpose of AI use. STATUS: NOT FINAL at the time of writing; the Chairman has since signalled tiering with kill switches and human oversight.','https://www.sebi.gov.in'),
 ('official','SEBI enforcement on unregistered advisory','the December 2025 order impounding approximately ₹546 crore with a market ban, and the established position that a &ldquo;for educational purposes only&rdquo; label does not excuse unregistered advisory activity inside a course, a private group or a chatbot reply.','https://www.sebi.gov.in'),
 ('industry','Commentary on the effect of the EOP framework on robo-advisers','the observation that the framework ended the combined free-advice-plus-execution model, so investors no longer obtain both from one platform. Interpretation of a regulatory change, not a figure.',''),
 ('industry','Reporting on SEBI&rsquo;s forthcoming AI guidelines','the Chairman&rsquo;s June and August 2026 remarks on a tiered responsible-AI framework and on SEBI&rsquo;s own use of AI in surveillance. Speeches and reporting, not notified regulation — treat as direction.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. <strong>The responsible-AI framework is a consultation, not a regulation.</strong> '
 'Regulation 16C is in force and already places the liability on you; verify the tiering before designing to it.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/wealth-advisory/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 07</div><h3>Wealth &amp; Advisory</h3><p>The IA framework in full: tooling, data licensing, costs and three recommended builds.</p></a>
<a href="/fintech-ai/wealth-advisory/" class="mod-card"><div class="mod-num">MODULE 07</div><h3>Wealth &amp; Advisory</h3><p>Why SEBI treats AI as increasing responsibility rather than sharing it.</p></a>
<a href="/fintech-ai/governance/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 09</div><h3>Governance</h3><p>Model inventories, independent validation and kill switches — the shape SEBI is moving toward.</p></a>
<a href="/fintech-ai/products/account-aggregator/" class="mod-card"><div class="mod-num">GUIDE 04</div><h3>Account Aggregator</h3><p>Where a complete picture of a client&rsquo;s holdings comes from, with consent.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Investment advice is a registered activity, the fee ceiling and the advice/execution separation are structural rather than negotiable, and the responsible-AI framework referred to here is a consultation. Nothing here is legal advice. Have your registration route, your advisory agreement and your execution handoff reviewed by qualified counsel before advising a single client.")

lanes={'green':[("How to use this page",g_read),("What you are actually building",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — the perimeter, and registration",i_step12),
           ("Steps 3 to 5 — onboard, profile, recommend",i_step345),
           ("Steps 6 to 8 — delivery, the wall, the clocks",i_step678),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Robo-Advisory: How to Build It"
META=("Build a robo-advisory product step by step: why advice and execution cannot sit in one "
      "entity, the fee ceiling, and what Regulation 16C means for AI.")
LEAD=("A step-by-step guide to building automated investment advice in India. Eight stages, the "
      "options at each one, exactly how each step connects to the next, real costs, and what breaks. "
      "Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/robo-advisory",title=TITLE,meta=META,lead=LEAD,label="Product Guide 12",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/robo-advisory/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m, "no <body>"
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t, "no page-hero"
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Building automated advice '
  'itself? The eight steps, why advice and execution cannot sit in one entity, and what Regulation 16C '
  'means for a bought model: <a href="/fintech-ai/products/robo-advisory/"><strong>Robo-Advisory: How to '
  'Build It &rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('wealth-advisory',):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/robo-advisory' in src:
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
