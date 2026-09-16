#!/usr/bin/env python3
# Session 82 — PRODUCT GUIDE 10: Alternative credit scoring
# The first product guide where the deliverable is a MODEL, not a money flow.
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product: a score that decides whether to lend to someone
a credit bureau cannot rank. A first-time borrower with no loan history. A shopkeeper whose income is
real and undocumented. A gig worker paid weekly by four different platforms.</p>
<p>Every other product guide on this site describes a flow of money. <strong>This one describes a
model</strong>, and the difference matters more than it sounds: a payment either settles or it does
not, while a score is right on average and wrong about a person.</p>
''' + warn("<strong>The product most people picture is not legal in India.</strong> The phone-data scorecard &mdash; contacts, call logs, SMS inboxes, installed apps, photo metadata &mdash; is the thing alternative credit scoring is famous for internationally. The <strong>RBI Digital Lending Directions, 2025</strong> (8 May 2025) permit camera, microphone and location with explicit consent and <strong>prohibit access to contacts, call logs and media files outright.</strong> If your reference implementation came from a market where that data is fair game, throw the feature list away before you start.")

g_what = '''
<p>Alternative credit scoring means using data that is <strong>not a repayment history</strong> to
estimate whether someone will repay. It exists because roughly the same person keeps being refused:
creditworthy, and invisible to the instrument that measures creditworthiness.</p>
<p>Four things get called &ldquo;the score&rdquo; and they are different objects with different
obligations:</p>
<table>
<tr><th>Object</th><th>What it is</th><th>Who owns the consequence</th></tr>
<tr><td><strong>Bureau score</strong></td><td>Produced by a Credit Information Company from reported repayment data.</td><td>The CIC, under the credit information framework.</td></tr>
<tr><td><strong>Your model&rsquo;s score</strong></td><td>Your estimate, from your features.</td><td><strong>You.</strong> Entirely, including where a vendor built it.</td></tr>
<tr><td><strong>A vendor score you consume</strong></td><td>Someone else&rsquo;s model, called over an API.</td><td><strong>Still you.</strong> See step 6.</td></tr>
<tr><td><strong>The decision</strong></td><td>Approve, refer or decline, at a price.</td><td>You, and it is the decision rather than the score that a borrower can contest.</td></tr>
</table>
''' + note("<strong>Keep the score and the decision separate in your head and in your code.</strong> A score is a number. A decision is an act with a reason attached, and the reason has to survive being asked for months later. Teams that collapse the two end up unable to answer <em>why was this person declined</em> without re-running a model that has since been retrained.") + '''
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not a way around the bureau.</strong> You still report to Credit Information Companies,
now on a much shorter cycle. Step 8.</li>
<li><strong>Not a licence-free product.</strong> Lending is regulated; scoring for a lender makes you
part of a regulated model. Step 6.</li>
<li><strong>Not automatically more inclusive.</strong> The honest version of that claim is in step 7,
and it is the most important paragraph on this page.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>What is the decision?</strong></td><td>And is a model the right shape for it at all.</td></tr>
<tr><td>2</td><td><strong>What may you lawfully use?</strong></td><td>Narrower than you think, and consent is the only basis.</td></tr>
<tr><td>3</td><td><strong>Pull the data</strong></td><td>Bureau, Account Aggregator, ULI, GST, your own records.</td></tr>
<tr><td>4</td><td><strong>Features, with lineage</strong></td><td>Every feature traceable to a field and a consent.</td></tr>
<tr><td>5</td><td><strong>Train and test for bias</strong></td><td>Choose the fairness metric <em>before</em> you see the result.</td></tr>
<tr><td>6</td><td><strong>Validate and register</strong></td><td>Independently. Including the vendor&rsquo;s model.</td></tr>
<tr><td>7</td><td><strong>Decide, and record the reason</strong></td><td><strong>The step that carries the obligation.</strong></td></tr>
<tr><td>8</td><td><strong>Monitor, report, retire</strong></td><td>Drift, weekly bureau reporting, and a 10-year inventory.</td></tr>
</table>
''' + note("<strong>Steps 1, 2, 7 and 8 are the ones people skip.</strong> Steps 3 to 6 are the part that looks like data science and they are the part a vendor will happily sell you. The obligations live almost entirely outside them.")

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; What is the decision, and does it need a model?</h3>
<p>Write the decision down as a sentence before anything else: <em>approve or decline an unsecured
loan of &#8377;10,000 to &#8377;50,000, to a first-time borrower, at one of three prices.</em> Then
ask whether a model beats a rule.</p>
<p>Often it does not, and the honest answer is worth having early. A handful of well-chosen rules on
verified income and existing obligations will get a small lender further than a gradient-boosted
model trained on 4,000 loans, and it has two properties the model does not: <strong>you can explain
every decision, and you can change it on a Tuesday.</strong></p>
''' + warn("<strong>A rule engine is a model too.</strong> The RBI's <strong>draft Guidance on Regulatory Principles for Model Risk Management, 2026</strong> (PR 2026-2027/528, <strong>24 June 2026</strong>, comments closed 24 July 2026 &mdash; <strong>still a draft at the time of writing</strong>) defines a model to include AI and ML systems, <strong>scoring algorithms, rule engines and material spreadsheets</strong> that influence decisions such as lending rates or customer pricing. The rules engine you wrote specifically to avoid model risk is in scope. <strong>The first governance task is not building controls, it is finding what you already have.</strong> Depth on the framework itself is in Build Sheet 09; this page covers what it means for one scoring pipeline.") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; What may you lawfully use?</h3>
<table>
<tr><th>Data</th><th>Position</th></tr>
<tr><td>Bureau report and score</td><td>Permitted, with consent. <strong>Every pull alerts the customer</strong> &mdash; see step 3</td></tr>
<tr><td>Bank statements via Account Aggregator</td><td>Permitted, with a consent artefact. <strong>Verify the signature</strong></td></tr>
<tr><td>GST returns, Udyam, land records, invoices</td><td>Permitted, with consent. Increasingly available through ULI</td></tr>
<tr><td>Your own transaction and repayment history</td><td>Permitted, for the purpose the customer agreed to</td></tr>
<tr><td>Camera, microphone, location</td><td><strong>Explicit consent required</strong>, purpose-bound</td></tr>
<tr><td><strong>Contacts, call logs, media files</strong></td><td><strong>PROHIBITED</strong></td></tr>
</table>
''' + warn("<strong>India has no &ldquo;legitimate interest&rdquo; basis. This is the single most consequential difference from a GDPR-shaped design.</strong> Under the <strong>DPDP Act</strong> and the <strong>DPDP Rules, 2025</strong> (notified <strong>13 November 2025</strong>), consent is the operative basis and it must be free, specific, informed, unconditional and unambiguous. A European team can lean on legitimate interest for credit assessment and fraud prevention; an Indian one cannot. <strong>Every field in your feature store needs a consent that names the purpose it is being used for</strong> &mdash; and a score derived from a field inherits that field's purpose, the same rule as derived AA data. Phasing: the Data Protection Board has been operational since <strong>13 November 2025</strong>, consent-manager provisions commence <strong>13 November 2026</strong>, and <strong>substantive obligations commence 13 May 2027</strong>. Penalties reach <strong>&#8377;250 crore</strong> and stack per violation.")

code_data = code('Python — steps 2 to 4, lawful fields and features that can explain where they came from', r'''from datetime import date, timedelta

# STEP 2. CLASSIFY EVERY FIELD BEFORE IT REACHES A FEATURE STORE.
# An unknown field defaults to the STRICTEST class, never the loosest -- the
# same rule as cross-border classification in Build Sheet 08. The difference
# here is that "prohibited" means prohibited, not "needs a stronger consent".

PROHIBITED = {"contacts", "call_logs", "media_files", "installed_apps_list",
              "sms_inbox"}          # Digital Lending Directions 2025

def admit(field, consents):
    if field["name"] in PROHIBITED:
        raise ValueError("prohibited source: %s" % field["name"])
    c = consents.get(field["name"])
    if c is None:
        return {"admit": False, "why": "no_consent_on_record"}
    if c["purpose"] != field["purpose"]:
        # Consent given to assess a loan does not cover marketing, collections
        # scoring, or a model you build next year.
        return {"admit": False, "why": "purpose_mismatch"}
    if c["expires_on"] < date.today():
        return {"admit": False, "why": "consent_expired"}
    return {"admit": True, "consent_id": c["id"]}

# STEP 3. TWO CLOCKS AND ONE SIDE EFFECT.
# A bureau pull is visible to the customer: CICs must alert the consumer by
# SMS or email whenever a specified user accesses their credit information
# report. "Pull everything and decide later" is not a silent design.

def pull_plan(applicant, ticket_paise):
    plan = ["own_records"]                    # free, silent, already consented
    if ticket_paise > 2_500_000:              # only then is a hard pull earned
        plan.append("bureau_full")
    else:
        plan.append("bureau_soft")
    if applicant["has_bank_consent"]:
        plan.append("aa_statements")          # verify the artefact SIGNATURE
    if applicant["is_business"]:
        plan.append("gst_returns")
    return plan

# STEP 4. LINEAGE. A feature that cannot name its field and its consent is a
# feature you cannot defend, retire or explain.

def build_feature(name, value, field, consent_id, window_days):
    return {"name": name, "value": value,
            "source_field": field,            # what it came from
            "consent_id": consent_id,         # under which permission
            "window_days": window_days,       # over what period
            "computed_on": date.today().isoformat(),
            "retire_on": (date.today() + timedelta(days=window_days)).isoformat()}

# WHAT TO CHECK
# [ ] every feature resolves to a field AND a consent id. No exceptions, no
#     "derived so it does not count" -- a score computed from a field IS that
#     field for purpose and residency
# [ ] an unrecognised field is refused, not admitted with a warning
# [ ] a soft pull and a hard pull are different products with different
#     customer-visible consequences. Decide which one each journey earns
# [ ] bureau data is processed and stored in India and not transferred out
# [ ] the AA consent artefact signature is VERIFIED, not assumed
# [ ] retention is per-feature, not one global sweep. Your warehouse, feature
#     store, training set and backups all received a copy within the hour
''')

i_step34 = '''
<h3 id="s-indigo-s3">Steps 3 and 4 &mdash; Pull the data, and keep the lineage</h3>
''' + code_data + '''
<p><strong>Where the data actually comes from.</strong> Three rails matter and only one of them is
new:</p>
<table>
<tr><th>Rail</th><th>What it gives you</th><th>Status</th></tr>
<tr><td><strong>Credit Information Companies</strong></td><td>Reported repayment history across the system.</td><td>Mature. Four bureaus.</td></tr>
<tr><td><strong>Account Aggregator</strong></td><td>Consented bank statements and other financial information.</td><td>Mature. <a href="/fintech-ai/products/account-aggregator/">Its own guide</a> &mdash; and note you may have to join as an FIP too.</td></tr>
<tr><td><strong>Unified Lending Interface</strong></td><td>One API gateway to many data providers instead of many bilateral integrations.</td><td><strong>No longer a pilot.</strong></td></tr>
</table>
''' + note("<strong>ULI is the integration argument, not the underwriting argument.</strong> Built by the Reserve Bank Innovation Hub, launched as the Public Tech Platform for Frictionless Credit on <strong>10 August 2023</strong> and rebranded ULI on <strong>26 August 2024</strong>. As at <strong>12 December 2025</strong> the RBI reported <strong>64 lenders onboarded</strong> &mdash; 41 banks and 23 NBFCs, up from 36 a year earlier &mdash; with <strong>more than 136 data services</strong> across <strong>12 loan journeys</strong>, up from around 50 services. What it removes is the many-to-many integration cost. What it does not remove is your obligation: <strong>the RBI has been explicit that consent management and grievance redress stay with the individual lender, not the platform.</strong> Plugging into ULI hands you more data and none of the accountability.")

i_step56 = '''
<h3 id="s-indigo-s5">Step 5 &mdash; Train, and test for bias before you like the answer</h3>
<p>The discipline that matters is sequencing, not technique. <strong>Choose and write down the
fairness metric before you run the test.</strong> Demographic parity, equalised odds and predictive
parity are mutually incompatible on most real data, so picking one afterwards is choosing the answer
rather than measuring it.</p>
<p>Record the disparity even when it sits inside tolerance. <strong>The trend is the signal</strong>,
and a single in-tolerance reading tells you nothing about direction.</p>
''' + warn("<strong>The proxy problem is the whole problem, and it does not announce itself.</strong> You will not put caste, religion or gender in the model. You may well put in pin code, handset price band, employer category, or the language the application was completed in &mdash; each of which carries some of that signal, and none of which looks like a protected attribute in a feature list. <strong>Test the outcome distribution, not the input list.</strong> A model with no protected attribute and a 20-point approval gap across districts is not a fair model with a coincidence.") + '''

<h3 id="s-indigo-s6">Step 6 &mdash; Validate independently, and register the model</h3>
<p>The draft MRM guidance is specific in ways that are easy to fail:</p>
<ul>
<li><strong>Tiering</strong> on materiality, complexity and autonomy, with an <strong>anti-dilution
rule</strong> so a high-materiality model cannot be tiered down because it happens to be simple.</li>
<li><strong>No model may be used unless it is in the inventory</strong>, and a decommissioned model
stays in the inventory for a minimum of <strong>ten years</strong>.</li>
<li><strong>Independent validation by the regulated entity is mandatory even where the vendor has
certified the model</strong>, with audit rights and exit arrangements written into the contract.</li>
<li><strong>Seven AI risk dimensions</strong> named: explainability, hallucinations, bias,
overfitting, spurious correlations, output variability and data risks.</li>
<li><strong>Kill switches, human oversight, disclosure to customers that AI is in use</strong>, a
human assistance option on customer-facing AI, and red-teaming.</li>
</ul>
''' + note("<strong>Independence is structural, not personal.</strong> A competent validator who reports into the model owner's business line is not independent. For a small lender the defensible answer is a <strong>named external validator for high-materiality models</strong> plus documented self-assessment below that line &mdash; which survives a question in a way that an internal colleague does not. Assert <code>validator != owner</code> in code; it is the most common finding and the easiest to prevent.")

code_decide = code('Python — steps 7 and 8, the decision with a reason, and what you watch afterwards', r'''# STEP 7. THE DECISION. THIS IS THE STEP THAT CARRIES THE OBLIGATION.
# Under the credit information framework a lender must inform the customer the
# reasons for rejection. Under the draft MRM guidance, credit underwriting is
# material decision-making and attracts a higher explainability threshold.
#
# You cannot reconstruct a reason later. Six months from now the model has
# been retrained, the thresholds have moved and the feature set has changed.
# The question is always: why did you decline THIS person on THAT day.

THREE_OUTCOMES = ("APPROVE", "REFER", "DECLINE")   # never two

def decide(applicant, score, features, model, policy):
    outcome = ("APPROVE" if score >= policy["approve_at"]
               else "REFER" if score >= policy["refer_at"]
               else "DECLINE")
    record = {
        "applicant_id": applicant["id"],
        "outcome": outcome,
        "score": score,
        "model_id": model["id"],                 # the RESOLVED version
        "model_version": model["version"],       # never the alias
        "policy_version": policy["version"],
        "thresholds": dict(policy),              # as they were TODAY
        "top_reasons": top_reasons(features, model),   # human-readable, ranked
        "features_snapshot": features,           # the blob, not a recipe
        "decided_at_ist": now_ist(),
    }
    if outcome == "DECLINE":
        # Must be sayable to the customer in plain words, and must be TRUE of
        # this decision -- not a generic list of things that usually matter.
        assert record["top_reasons"], "a decline with no stated reason is not shippable"
    return record

# A model that cannot explain itself is not banned. It is EXPENSIVE: the draft
# guidance requires enhanced validation, output verification, more frequent
# monitoring and USAGE RESTRICTIONS to compensate. Price that before choosing
# the architecture, because it is a permanent operating cost and not a one-off.

def explainability_budget(model):
    if model["explainable"]:
        return {"validation": "standard", "monitoring": "quarterly"}
    return {"validation": "enhanced", "output_verification": True,
            "monitoring": "monthly", "usage_restrictions": True}

# STEP 8. AFTER THE DECISION.
def monitor(model, window):
    return {
        "psi_by_feature": population_stability(window),     # drift
        "approval_rate_by_district": rate_by(window, "district"),
        "override_rate": rate_of_human_overrides(window),
        "decline_reasons_distribution": reasons_hist(window),
        "kill_switch": model["runtime_flag"],   # a flag, not a deploy
        "fallback_share": share_that_fell_back_to_rules(window),
    }

# WHAT TO CHECK
# [ ] three outcomes, never two. An automatic decline on a thin file is
#     usually wrong -- route to a human and let a person decline
# [ ] the stored reason is the reason for THIS decision, not a template
# [ ] log the RESOLVED model version. A vendor moving an alias changes your
#     decisions with no deploy on your side
# [ ] the kill switch is a runtime flag, and someone other than the model
#     owner can pull it
# [ ] human override rate under ~1% is a rubber stamp and worse than no human,
#     because it manufactures the appearance of oversight
# [ ] plot the share of decisions that FELL BACK to rules. Zero means the
#     fallback has never run and you do not know that it works
# [ ] reconcile and aggregate in IST. A UTC day boundary moves 5.5 hours of
#     decisions into the wrong reporting day, every day
''')

i_step78 = '''
<h3 id="s-indigo-s7">Steps 7 and 8 &mdash; Decide, record, monitor, report</h3>
''' + code_decide + '''
<p><strong>The gotcha that shapes the whole build:</strong> <strong>you must be able to say why you
said no, and the model that scores best is usually the one least able to.</strong> Those two
sentences are in tension and most teams discover it after the model is chosen.</p>
<p>Two separate instruments push the same way. The credit information framework requires a lender to
<strong>inform the customer the reasons for rejection</strong>. The draft MRM guidance places credit
underwriting in <strong>material decision-making</strong>, where a model that cannot fully explain
itself must be compensated with enhanced validation, output verification, more frequent monitoring
and <strong>usage restrictions</strong>. <strong>Explainability is therefore a constraint on model
selection, with a price attached, rather than a reporting feature you add at the end.</strong></p>

<h3 id="s-indigo-srep">Reporting back, on a clock that keeps shortening</h3>
<table>
<tr><th>Obligation</th><th>Position</th></tr>
<tr><td>Reporting frequency</td><td><strong>Fortnightly</strong> (15th and last day) from <strong>1 January 2025</strong>, within <strong>7 calendar days</strong> of the fortnight. Amended directions moving to a <strong>weekly</strong> incremental cycle &mdash; the <strong>9th, 16th, 23rd and last day</strong> &mdash; were deferred from 1 April to <strong>1 July 2026</strong></td></tr>
<tr><td>Complaint resolution</td><td><strong>30 calendar days</strong> &mdash; 21 for the lender to investigate and correct, 9 for the CIC to update</td></tr>
<tr><td>Compensation for delay</td><td><strong>&#8377;100 per calendar day</strong></td></tr>
<tr><td>Access alerts</td><td>CICs alert the consumer by SMS or email <strong>whenever a specified user accesses their report</strong></td></tr>
<tr><td>Rejection</td><td>The lender must inform the customer <strong>the reasons</strong></td></tr>
<tr><td>Residency</td><td>Credit information <strong>processed and stored in India</strong>, not transferred out</td></tr>
<tr><td>Third-party sharing</td><td>Consent-based; the recipient <strong>may not resell or re-share</strong>, and the CIC must assess it first</td></tr>
</table>
''' + note("<strong>Weekly reporting cuts both ways and the second way is the one that affects your build.</strong> Fresher data is the benefit everyone quotes. The consequence nobody designs for: <strong>the file you scored on can change between decision and disbursal.</strong> On a fortnightly cycle that window was mostly theoretical; on a weekly one it is ordinary. Decide explicitly whether a sanction is re-checked before money moves, and store the answer &mdash; because if you do not decide, the answer is no, by default, silently.")

i_cost = registry("Alternative credit scoring &mdash; what it costs", [
 ("Bureau pulls", "direct",
  "Per enquiry, negotiated by volume, and cheaper soft than hard. The cost that actually matters is "
  "not the rupee figure: <strong>every access alerts the customer</strong>, so a pull-everything "
  "design spends trust as well as money."),
 ("Account Aggregator", "direct",
  "Per fetch, plus the build. <strong>Scope it as two modules, not one</strong> &mdash; a regulated "
  "entity joining as an FIU must generally also join as an FIP. Estimates built on the FIU side alone "
  "are wrong by roughly half. Detail in the Account Aggregator guide."),
 ("ULI integration", "direct",
  "One gateway rather than many bilateral integrations. <strong>Saves integration cost, transfers no "
  "accountability</strong> &mdash; consent management and grievance redress stay with you."),
 ("A vendor score", "direct",
  "Per call, and the cheapest-looking option. <strong>Independent validation is mandatory anyway</strong>, "
  "so budget the validation alongside the subscription, and get audit rights and an exit in the contract."),
 ("Independent validation", "direct",
  "A named external validator for high-materiality models. Recurring, not one-off, and the line most "
  "often missing from a business case."),
 ("Explainability", "indirect",
  "<strong>A model that cannot explain itself costs more forever</strong> &mdash; enhanced validation, "
  "output verification, more frequent monitoring and usage restrictions. Price it at architecture "
  "choice, not at go-live."),
 ("The inventory", "direct",
  "Every model registered, no model used unless listed, and a decommissioned model retained "
  "<strong>ten years</strong>. Cheap to run from day one, expensive to reconstruct."),
 ("Getting it wrong", "indirect",
  "<strong>&#8377;100 per calendar day</strong> per unresolved credit information complaint past 30 "
  "days, DPDP penalties to <strong>&#8377;250 crore</strong> stacking per violation, and a "
  "supervisory conversation about a model you cannot explain."),
], "September 2026") + note("<strong>The cheapest useful thing on this list is the decision record.</strong> Storing the score, the resolved model version, the thresholds as they stood and the ranked reasons costs a few hundred bytes per application. It is also the only artefact that answers the question you will actually be asked, and it cannot be recreated after the fact at any price.")

a_builds = '''
<h3 id="s-amber-week">Rules, honestly</h3>
<p><strong>Build:</strong> verified income and existing obligations from Account Aggregator data
&rarr; a handful of written rules &rarr; three outcomes &rarr; every decision recorded with its
reason.</p>
<p><strong>You get:</strong> a lending product you can explain, change and defend. <strong>Register it
anyway</strong> &mdash; a rule engine is a model.</p>

<h3 id="s-amber-proper">A scorecard you can read</h3>
<p><strong>Build:</strong> logistic regression or a small gradient-boosted model on lineage-tracked
features &rarr; fairness metric chosen in writing before testing &rarr; independent validation &rarr;
inventory entry &rarr; ranked reasons on every decline &rarr; drift and approval-rate monitoring by
district.</p>
<p><strong>Trade:</strong> a point or two of discrimination against the ability to answer a question
in one sentence. <strong>On this side of the trade the regulator and the customer want the same
thing</strong>, which is unusual and worth taking.</p>

<h3 id="s-amber-big">A deep model, with the costs paid</h3>
<p><strong>Build:</strong> the above, plus enhanced validation, output verification, monthly
monitoring, documented usage restrictions, red-teaming, a runtime kill switch and a rules fallback
that is exercised rather than assumed.</p>
<p><strong>It breaks when:</strong> the lift was measured on a bake-off and the compensating controls
were not costed. <strong>Measure the lift against your own rules baseline, in production, on split
traffic</strong> &mdash; and then subtract the permanent operating cost above before deciding it won.</p>
''' + note("If you take one thing from this page: <strong>store the reason at the moment you decide.</strong> Everything else here can be retrofitted with effort. A reason that was never written down is gone, and it is the one thing a borrower, a bureau complaint and a supervisor will all ask for.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>Cannot say why someone was declined</strong></td><td>The reason was never stored; the model has since been retrained.</td><td>Ranked reasons written at decision time, with the resolved model version.</td></tr>
<tr><td><strong>Phone data in the feature list</strong></td><td>Copied from a market where it is permitted.</td><td>Contacts, call logs and media files are prohibited. Remove, do not gate.</td></tr>
<tr><td><strong>Features with no consent behind them</strong></td><td>&ldquo;Derived, so it does not count.&rdquo;</td><td>A derived value inherits the purpose of its source.</td></tr>
<tr><td><strong>Fairness metric chosen after the test</strong></td><td>Three metrics, incompatible, one flattering.</td><td>Choose and record it before running anything.</td></tr>
<tr><td><strong>Approval gap by district, no protected attribute anywhere</strong></td><td>Pin code, handset band and employer category are proxies.</td><td>Test the outcome distribution, not the input list.</td></tr>
<tr><td><strong>Vendor score trusted because the vendor validated it</strong></td><td>It looks like buying, not building.</td><td>Independent validation is required regardless. Audit rights in the contract.</td></tr>
<tr><td><strong>Model quietly changed under you</strong></td><td>An alias was logged instead of a version.</td><td>Log the resolved version. Alert on change.</td></tr>
<tr><td><strong>Bureau alerts surprise the customer</strong></td><td>Pull-everything design; every access notifies them.</td><td>Earn the hard pull. Soft first, and tell people what you are doing.</td></tr>
<tr><td><strong>File changed between sanction and disbursal</strong></td><td>Weekly reporting made a theoretical window ordinary.</td><td>Decide the re-check rule explicitly and store it.</td></tr>
<tr><td><strong>Kill switch needs a deploy</strong></td><td>Built as a config change.</td><td>A runtime flag, pullable by someone other than the model owner.</td></tr>
<tr><td><strong>Fallback share is zero</strong></td><td>Read as a good sign.</td><td>It means the fallback has never run and is untested.</td></tr>
</table>
'''

SRC=[('official','RBI draft Guidance on Regulatory Principles for Model Risk Management, 2026','PR 2026-2027/528, released 24 June 2026 for consultation with comments due 24 July 2026 — six chapters and sixty-four principles, applying to eleven categories of regulated entity including Credit Information Companies. The definition of a model covering scoring algorithms, rule engines and material spreadsheets; risk-based tiering with an anti-dilution rule; the inventory requirement and ten-year retention of decommissioned models; mandatory independent validation of third-party models; the seven AI risk dimensions; kill switches, human oversight, AI disclosure and red-teaming; and the higher explainability threshold for material decisions. STATUS: DRAFT — verify against the final text before designing to any provision.','https://www.rbi.org.in'),
 ('official','RBI Digital Lending Directions, 2025','issued 8 May 2025. Camera, microphone and location permitted with explicit consent; access to contacts, call logs and media files prohibited; data stored in India. Covered in depth on the BNPL guide rather than repeated here.','https://www.rbi.org.in'),
 ('official','RBI Master Direction on credit information reporting','the fortnightly cycle on the 15th and last day from 1 January 2025 submitted within seven calendar days; the amended incremental cycle on the 9th, 16th, 23rd and last day deferred from 1 April to 1 July 2026; the 30-calendar-day complaint framework split 21 days to the credit institution and 9 to the CIC; ₹100 per day compensation; SMS and email alerts on every access by a specified user; the duty to inform customers the reasons for rejection; India-only processing and storage; and the limits on third-party sharing.','https://www.rbi.org.in'),
 ('official','Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025','Rules notified 13 November 2025. The absence of a legitimate-interest basis and the standard that consent be free, specific, informed, unconditional and unambiguous; the three commencement phases of 13 November 2025, 13 November 2026 and 13 May 2027; and penalties reaching ₹250 crore, applied per violation.','https://www.meity.gov.in'),
 ('official','Unified Lending Interface','launched as the Public Tech Platform for Frictionless Credit on 10 August 2023 and rebranded ULI on 26 August 2024, built by the Reserve Bank Innovation Hub. The RBI reported 64 lenders — 41 banks and 23 NBFCs — more than 136 data services and 12 loan journeys as at 12 December 2025, and has been explicit that consent management and grievance redress remain with individual lenders.','https://www.rbi.org.in'),
 ('official','RBI FREE-AI Committee report','13 August 2025. The framework for responsible and ethical enablement of AI that this guidance descends from, together with the 5 August 2024 draft on model risks in credit.','https://www.rbi.org.in'),
 ('industry','Analysis of ULI and pricing-based exclusion','the argument that platform-scale data access shifts borrowers from outright exclusion to exclusion by price, without visibility into how particular inputs affect the rate offered. A criticism worth engaging with rather than a figure to build on.',''),
 ('industry','Credit reporting implementation commentary','the operational read on the weekly incremental cycle and what it asks of a lender’s reporting stack. Directional; confirm every date against the Master Direction.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join('<li><span class="src-k src-'+k+'">'+k+'</span><strong>'+n+'</strong> &mdash; '+w+(' <a href="'+u+'" target="_blank" rel="noopener">'+u.split("//")[-1].split("/")[0]+'</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 '<div class="srcs"><ol>'+lis+'</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. <strong>The Model Risk Management guidance is a DRAFT.</strong> Comments closed '
 '24 July 2026 and it had not been finalised at the time of writing. Verify status before designing to it.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/credit-underwriting/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 02</div><h3>Credit &amp; Underwriting</h3><p>Every tool for this, what each one costs, and three recommended builds.</p></a>
<a href="/fintech-ai/governance/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 09</div><h3>Governance</h3><p>The model risk framework in full — inventory, tiering, validation, kill switches.</p></a>
<a href="/fintech-ai/products/account-aggregator/" class="mod-card"><div class="mod-num">GUIDE 04</div><h3>Account Aggregator</h3><p>Where most of your alternative data comes from, and why it is two modules.</p></a>
<a href="/fintech-ai/products/bnpl-checkout/" class="mod-card"><div class="mod-num">GUIDE 03</div><h3>BNPL Checkout</h3><p>The digital lending rulebook in full, including what a platform may never touch.</p></a>
</div>
''' + warn("This page is a guide, not a specification. Lending is a regulated activity, the model risk guidance quoted here is a draft, and a scoring decision affects a real person's access to credit. Nothing here is legal advice. Have your data basis, your fairness testing and your validation arrangements reviewed by qualified counsel and an independent validator before the first live decision.")

lanes={'green':[("How to use this page",g_read),("What alternative credit scoring actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — the decision, and what you may use",i_step12),
           ("Steps 3 and 4 — the data, and the lineage",i_step34),
           ("Steps 5 and 6 — bias testing and validation",i_step56),
           ("Steps 7 and 8 — decide, record, monitor, report",i_step78),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Alternative Credit Scoring: How to Build It"
META=("Build an alternative credit scoring product step by step: what data you may lawfully use, "
      "bias testing, and why every decline needs a stored reason.")
LEAD=("A step-by-step guide to building a credit score from data that is not a repayment history, in "
      "India. Eight stages, the options at each one, exactly how each step connects to the next, real "
      "costs, and what breaks. Written for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/alternative-credit-scoring",title=TITLE,meta=META,lead=LEAD,label="Product Guide 10",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/alternative-credit-scoring/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: h=h.replace('</style>',CSSRC+'\n</style>',1)
if 'class="skip-link"' not in h:
    h=h.replace('</style>',"\n.skip-link{position:absolute;left:-9999px;top:0;z-index:999;background:#0F172A;color:#fff;padding:10px 16px;border-radius:0 0 8px 0;font-size:.85rem;font-weight:600;text-decoration:none}\n.skip-link:focus{left:0;outline:2px solid #14B8A6;outline-offset:2px}\n</style>",1)
    m=_re.search(r'<body[^>]*>',h); assert m, "no <body>"
    h=h[:m.end()]+'\n<a class="skip-link" href="#main-content">Skip to content</a>'+h[m.end():]
    t=_re.search(r'<div class="page-hero"(?![^>]*\bid=)',h); assert t, "no page-hero"
    h=h[:t.end()]+' id="main-content"'+h[t.end():]
_io.open(f,'w',encoding='utf-8').write(h)

# ---- Link from the credit module. Rule 5: match the element, assert, verify.
NOTE_BLOCK = ('<div class="note"><span class="note-lbl">Product guide</span><p>Scoring a borrower the '
  'bureau cannot rank? The eight steps, what data you may lawfully use, and why every decline needs a '
  'stored reason: <a href="/fintech-ai/products/alternative-credit-scoring/"><strong>Alternative '
  'Credit Scoring: How to Build It &rarr;</strong></a></p></div>')
ANCHOR = '<div class="note"><span class="note-lbl">Build sheet</span>'
for mod in ('credit-underwriting', 'governance'):
    p = 'fintech-ai/' + mod + '/index.html'
    src = _io.open(p, encoding='utf-8').read()
    if 'products/alternative-credit-scoring' in src:
        print('  = already linked from /' + mod + '/'); continue
    n = src.count(ANCHOR)
    assert n == 1, 'anchor appears ' + str(n) + ' times in ' + p + ' — refusing to write'
    i = src.find(ANCHOR)
    assert i != -1, 'anchor not found in ' + p
    out = src[:i] + NOTE_BLOCK + src[i:]
    assert NOTE_BLOCK.count('<div') == 1 and NOTE_BLOCK.count('</div>') == 1, 'block shape changed'
    assert out.count('<div') == src.count('<div') + 1, 'div count moved unexpectedly'
    assert out.count('</div>') == src.count('</div>') + 1, 'close-div count moved unexpectedly'
    assert len(out) == len(src) + len(NOTE_BLOCK), 'length changed by more than the block'
    _io.open(p, 'w', encoding='utf-8').write(out)
    print('  + linked from /' + mod + '/')
