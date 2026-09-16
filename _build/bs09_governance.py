#!/usr/bin/env python3
# Session 58 — Build Sheet 09: Governance (final build sheet)
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

V = VERIFIED

# ---------------------------------------------------------------- GREEN

g_read = f'''
<p>The <a href="/fintech-ai/governance/">Governance module</a> explains what model risk is and why
the scope is now enormous. This page is the parts list: the frameworks to map against, the tooling
that makes each control real, what it costs, and the three builds.</p>
{warn(f"Rules carry a <strong>Verified {V}</strong> stamp. Two of the most important things on this page are <strong>not yet final</strong> &mdash; India's model risk guidance is still a draft, and a major EU deadline shift is agreed but pending ratification. Both are flagged where they appear. Governance is the one area where building against a draft is usually correct, because the direction is clear even when the text is not.")}
<p>This is the last of the nine build sheets, and it is the one that decides whether the other eight
survive contact with a supervisor.</p>
'''

g_scope = f'''
<p>Start here, because it invalidates most existing model inventories.</p>
<p>The RBI's <strong>draft Guidance on Regulatory Principles for Model Risk Management, 2026</strong>
(Press Release 2026-2027/528, 24 June 2026) broadens "model" dramatically. It covers AI and ML
systems, scoring algorithms, <strong>rule engines</strong>, and <strong>material spreadsheets</strong>
that influence business decisions such as lending rates or customer pricing.</p>
{warn("<strong>Read that last item again.</strong> A spreadsheet that sets pricing is a model. The rules engine you built specifically <em>to avoid</em> model risk is a model. Most inventories we would expect to find in Indian fintechs list the ML models and nothing else, which means they are incomplete by design rather than by oversight. <strong>The first governance task is not building controls. It is finding what you already have.</strong>")}
<p>The draft applies to <strong>eleven categories</strong> of regulated entity: commercial banks,
small finance banks, payments banks, local area banks, regional rural banks, urban and rural
co-operative banks, NBFCs of all layers, All-India Financial Institutions, asset reconstruction
companies and credit information companies.</p>
<p>Where it sits in the lineage: a draft on model risk <em>in credit</em> (5 August 2024), then the
<strong>FREE-AI committee report</strong> (13 August 2025) with its seven sutras, 26 recommendations
and six pillars, then this. FREE-AI gave the direction; this draft is the control layer.</p>
{note("<strong>Status, precisely.</strong> The MRM guidance is a <strong>draft</strong>. Comments closed 24 July 2026 and finalisation is expected in the second half of 2026 on the RBI's usual consultation-to-final cadence. Commenters proposed a tiered transitional runway of 18, 24 and 36 months. <strong>Build the inventory now regardless.</strong> Nothing in the final text will make an accurate list of your models less useful, and the discovery exercise is the long pole.")}
'''

g_lines = f'''
<p>Three lines of defence is the structure every framework here assumes. It is worth being concrete
about what each one actually does, because the common failure is three names and one team.</p>
<table>
<tr><th>Line</th><th>Who</th><th>What they do</th><th>The failure mode</th></tr>
<tr><td><strong>First</strong></td><td>Model owners and developers</td><td>Design, build, document, run initial testing, monitor in production.</td><td>Marking their own homework and calling it validation.</td></tr>
<tr><td><strong>Second</strong></td><td>Independent validation and risk</td><td>Challenge the model. Re-derive results. Test on data the builder never saw.</td><td>Reporting to the person who owns the model's business outcome.</td></tr>
<tr><td><strong>Third</strong></td><td>Internal audit</td><td>Assess whether the framework itself works. Not the model &mdash; the process.</td><td>Auditing documentation completeness instead of control effectiveness.</td></tr>
</table>
<p>The board and its risk management committee retain ultimate accountability, and
<strong>high-risk models require explicit committee approval</strong> under the draft. That is a real
constraint on shipping: a high-risk model is not something a product team can deploy on its own
authority.</p>
{note("<strong>Independence is structural, not personal.</strong> A validator who is competent, diligent and reports to the head of the business line that owns the model is not independent, however well they do the work. If you are too small for a separate function &mdash; and most fintechs are &mdash; the honest answer is a named external validator for high-risk models and documented self-assessment for the rest. That is defensible. Calling the model owner's colleague &ldquo;the second line&rdquo; is not.")}
'''

# ---------------------------------------------------------------- INDIGO

i_mat_fw = f'''
<table>
<tr><th>Framework</th><th>What it gives you</th><th>Status for an Indian fintech</th></tr>
<tr><td><strong>RBI FREE-AI</strong></td><td>Seven sutras, 26 recommendations, six pillars. Strategic and ethical direction.</td><td>Published 13 Aug 2025. Direction-setting, not a control list.</td></tr>
<tr><td><strong>RBI Draft MRM 2026</strong></td><td>The control layer: board framework, inventory, tiering, independent validation, AI controls, vendor accountability, kill switches.</td><td><strong>Draft.</strong> Comments closed 24 Jul 2026. This is what you will be examined against.</td></tr>
<tr><td><strong>NIST AI RMF</strong> <span class="pill p-oss">oss</span></td><td>Govern / Map / Measure / Manage. Voluntary, free, well structured.</td><td>The best free scaffolding to organise work against. Use it as the backbone.</td></tr>
<tr><td><strong>ISO/IEC 42001</strong></td><td>Certifiable AI management system. Third-party verified.</td><td>Increasingly expected in enterprise procurement and by regulators as AI-specific governance distinct from 27001.</td></tr>
<tr><td><strong>ISO/IEC 27001</strong></td><td>Information security management.</td><td>The floor beneath all of it, and it cuts 42001 effort by 40&ndash;50% if you already hold it.</td></tr>
<tr><td><strong>EU AI Act</strong></td><td>Binding law with real fines. Credit scoring for natural persons is Annex III high-risk.</td><td>Relevant if you serve EU customers. See the timing warning below.</td></tr>
<tr><td><strong>Fed SR 11-7</strong></td><td>The original supervisory model risk guidance. Still the clearest articulation of validation.</td><td>Not binding on you. Worth reading anyway &mdash; most of the world's framing descends from it.</td></tr>
</table>
{warn("<strong>EU AI Act timing moved, and the shift is not yet law.</strong> On 7 May 2026 a provisional agreement under the Digital Omnibus deferred Annex III standalone high-risk obligations from <strong>2 August 2026 to 2 December 2027</strong>, and Annex I product-embedded systems from 2 August 2027 to 2 August 2028. <strong>The Omnibus is pending formal ratification, so the original date remains in force until it is adopted.</strong> Article 50 transparency duties were <em>not</em> deferred and applied from 2 August 2026. Plan against December 2027, stay ready for the earlier date, and do not let a secondary source's headline date into your project plan without checking ratification status.")}
'''

i_mat_tool = f'''
<p>Almost every control below has a free tool that makes it real. The gap between a governance
document and a governance programme is whether these are wired into CI.</p>
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>MLflow</strong> <span class="pill p-oss">oss</span></td><td>Experiment tracking and model registry. The practical starting point for an inventory that stays current instead of rotting.</td><td>mlflow.org</td></tr>
<tr><td><strong>Evidently / NannyML</strong> <span class="pill p-oss">oss</span></td><td>Drift and performance monitoring in production. NannyML estimates performance before labels arrive.</td><td>evidentlyai.com</td></tr>
<tr><td><strong>Fairlearn / AIF360</strong> <span class="pill p-oss">oss</span></td><td>Group fairness metrics and mitigation.</td><td>fairlearn.org</td></tr>
<tr><td><strong>SHAP / InterpretML</strong> <span class="pill p-oss">oss</span></td><td>Attribution, and glass-box models. InterpretML's EBMs are accurate <em>and</em> interpretable.</td><td>interpret.ml</td></tr>
<tr><td><strong>Great Expectations / Soda</strong> <span class="pill p-oss">oss</span></td><td>Data quality assertions as code. Catches the upstream breakage that degrades models silently.</td><td>greatexpectations.io</td></tr>
<tr><td><strong>Langfuse / Phoenix</strong> <span class="pill p-oss">oss</span></td><td>Tracing and evaluation for generative systems. <strong>Your LLM features are models too.</strong></td><td>langfuse.com</td></tr>
<tr><td><strong>Model Cards / Croissant</strong> <span class="pill p-oss">oss</span></td><td>Structured documentation formats. Adopting a standard beats inventing one.</td><td>modelcards.withgoogle.com</td></tr>
<tr><td><strong>Deepchecks / Giskard</strong> <span class="pill p-oss">oss</span></td><td>Test suites for models and LLM apps, runnable in CI.</td><td>giskard.ai</td></tr>
</table>
{note("Notice that the entire tooling column is open source. <strong>Governance is not a procurement problem.</strong> There is no product you can buy that makes you governed, and the commercial platforms in this space mostly package these libraries with a workflow and a dashboard. Buy that when your model count makes coordination the bottleneck &mdash; not before, and never in the belief that it substitutes for the second line.")}
'''

code_inv = code('Python — the model inventory, and the fields that prevent failures', r'''from dataclasses import dataclass, field
from datetime import date

@dataclass
class ModelRecord:
    # --- identity ---
    id: str
    name: str
    version: str
    kind: str                    # "ml" | "rules_engine" | "spreadsheet" | "llm" | "vendor"
    # A rules engine IS a model. A pricing spreadsheet IS a model. If it
    # influences a business decision, it belongs in this list.

    # --- accountability: the three fields most inventories are missing ---
    owner: str                   # a NAMED PERSON, not a team
    validator: str               # who challenged it, and is not the owner
    approver: str                # who accepted the residual risk

    # --- the field that prevents the most failures ---
    fallback: str                # what happens when this model is unavailable
    fallback_rehearsed: date     # when it was last ACTUALLY exercised
    kill_switch: str             # the concrete mechanism, not "we'd turn it off"

    # --- risk ---
    tier: str                    # "high" | "medium" | "low"
    decisions_affected: str      # what changes for a customer because of this
    population: int              # how many people it touches per month

    # --- lifecycle ---
    deployed_on: date
    last_validated: date
    next_validation_due: date
    upstream_data: list = field(default_factory=list)
    downstream_models: list = field(default_factory=list)

def inventory_gaps(records, today=None):
    today = today or date.today()
    issues = []
    for m in records:
        if m.tier == "high" and not m.approver:
            issues.append((m.id, "high_risk_without_named_approver"))
        if m.validator == m.owner:
            issues.append((m.id, "validator_is_owner"))
        if not m.fallback:
            issues.append((m.id, "no_defined_fallback"))
        if (today - m.fallback_rehearsed).days > 365:
            issues.append((m.id, "fallback_never_rehearsed_this_year"))
        if m.next_validation_due < today:
            issues.append((m.id, "validation_overdue"))
    return issues

# WHAT TO CHECK
# [ ] UNLISTED ACTIVE MODELS ARE PROHIBITED under the draft guidance. Reconcile
#     the inventory against what is actually deployed, automatically, monthly.
#     A list maintained by hand is a list that is wrong
# [ ] owner is a person. "The risk team" cannot be woken at 2am
# [ ] validator != owner, asserted in code. This is the single most common
#     finding and the easiest to prevent
# [ ] fallback_rehearsed is a DATE, not a boolean. An unrehearsed fallback is a
#     hypothesis
# [ ] upstream_data and downstream_models give you blast radius. When a feed
#     breaks you need to know every model that consumed it, in seconds
# [ ] vendor models get the SAME record. You cannot rely on a supplier's safety
#     certificate -- you remain accountable and must validate independently
# [ ] spreadsheets that set prices or rates are in scope. Go and look for them
''')

i_inv = f'''
<h3 id="s-indigo-inv">Finding what you have is most of the work</h3>
<p>The draft is explicit that <strong>unlisted active models are prohibited</strong>. That single
sentence turns the inventory from documentation into a control, and it means the reconciliation
&mdash; comparing the list against what is genuinely running &mdash; has to be automatic.</p>
{code_inv}
<p><strong>The gotcha nobody documents:</strong> <code>fallback_rehearsed</code> as a date rather
than a flag. Every model inventory has a fallback column and almost all of them contain a sentence
describing what <em>would</em> happen. A fallback that has never been exercised in production is a
hypothesis, and the day you discover it does not work is the day you needed it. Put a date in the
field, run the rehearsal on a schedule, and let the inventory go red when it ages out. This is the
governance equivalent of the fall-back-rate metric in
<a href="/fintech-ai/infrastructure/build-sheet/">Build Sheet 08</a>.</p>

<h3 id="s-indigo-tier">Tiering, and what it actually buys you</h3>
<p>Tier on <strong>materiality and complexity</strong>, and let the tier drive real differences in
process rather than a label on a spreadsheet:</p>
<table>
<tr><th>Tier</th><th>Typical</th><th>What it triggers</th></tr>
<tr><td><strong>High</strong></td><td>Credit decisions, pricing, sanctions screening, anything affecting access to a product</td><td>Explicit risk-committee approval &middot; independent validation before deployment &middot; annual revalidation &middot; documented fallback rehearsal</td></tr>
<tr><td><strong>Medium</strong></td><td>Fraud scoring with human review, collections prioritisation, marketing targeting with financial consequences</td><td>Independent review &middot; periodic revalidation &middot; monitored drift thresholds</td></tr>
<tr><td><strong>Low</strong></td><td>Internal productivity, routing, summarisation with a human in the loop</td><td>Documented self-assessment &middot; inventory entry &middot; monitoring</td></tr>
</table>
{warn("<strong>Third-party models are higher risk, not lower.</strong> The draft is direct about it: you cannot rely on a vendor's safety certificate and you must validate independently. This inverts the instinct that buying transfers risk. Practically: demand the ability to test on your own population, insist on notice of model changes, and record what happens when the vendor's model updates. A vendor model whose version you cannot pin and whose changes you cannot detect is not governable, and that should affect the buying decision rather than being discovered afterwards.")}
'''

code_kill = code('Python — the kill switch, and proving it works', r'''import time

# The draft requires human-in-the-loop controls, human override, and an
# IMMEDIATE emergency kill switch to take a malfunctioning model offline.
# "Immediate" rules out a code deploy. It has to be a runtime flag.

class ModelGate:
    def __init__(self, model_id, flags, fallback_fn, audit):
        self.model_id, self.flags = model_id, flags
        self.fallback_fn, self.audit = fallback_fn, audit

    def decide(self, features, context):
        # 1. KILL SWITCH -- checked first, every call, no caching beyond seconds
        if self.flags.is_killed(self.model_id):
            out = self.fallback_fn(features)
            self.audit.write(self.model_id, "killed", out, context)
            return out

        # 2. the model
        try:
            out = self.model.predict(features)
        except Exception as e:                      # unavailable == fall back
            out = self.fallback_fn(features)
            self.audit.write(self.model_id, f"error:{type(e).__name__}", out, context)
            return out

        # 3. ANTI-AUTOMATION-BIAS: a human override must be possible AND
        #    recorded. An override nobody can see is not oversight.
        if context.get("human_override") is not None:
            self.audit.write(self.model_id, "human_override", context["human_override"],
                             context, model_said=out)
            return context["human_override"]

        self.audit.write(self.model_id, "model", out, context)
        return out


def rehearse(gate, sample, expect_degraded_ok=True):
    """Run in production, on a schedule, on a traffic slice. A fallback you have
    never exercised is a hypothesis, not a control."""
    gate.flags.kill(gate.model_id)
    t0 = time.time()
    results = [gate.decide(f, {"rehearsal": True}) for f in sample]
    gate.flags.unkill(gate.model_id)
    return {"n": len(results), "seconds": round(time.time() - t0, 2),
            "all_returned": all(r is not None for r in results),
            "rehearsed_on": time.strftime("%Y-%m-%d")}

# WHAT TO CHECK
# [ ] the kill switch is a RUNTIME FLAG. If disabling a model needs a deploy,
#     you do not have a kill switch, you have an intention
# [ ] who may pull it is written down, and it is not only the model owner. The
#     person who most wants a model to keep running should not be the only one
#     who can stop it
# [ ] the fallback produces a decision for EVERY input, including the awkward
#     ones. A fallback that errors on 3% of traffic is a 3% outage
# [ ] rehearsal runs on real production traffic, on a schedule, and writes its
#     date back to the inventory
# [ ] HUMAN OVERRIDES ARE RECORDED WITH WHAT THE MODEL SAID. The override rate
#     and its direction is the most useful oversight metric you will have --
#     near-zero means nobody is really reviewing
# [ ] the audit record is append-only and includes the model version and the
#     threshold configuration in force at that moment
''')

i_kill = f'''
<p>The draft's AI-specific controls name four risks directly &mdash; <strong>hallucination, data
drift, operational bias and discrimination, and adversarial attack</strong> &mdash; and require
anti-automation-bias measures: human-in-the-loop, human override, and an immediate emergency kill
switch.</p>
{code_kill}
<p><strong>The gotcha nobody documents:</strong> the human override rate, and its direction. Every
governance programme records that human review exists. Almost none measures whether it is doing
anything. If reviewers override the model in under 1% of cases, you have a rubber stamp rather than
oversight, and that is worse than no human in the loop because it manufactures the appearance of
control. If they override in more than about 20%, the model is not fit for the decision it has been
given. Both numbers are actionable and neither appears on a standard dashboard.</p>

<h3 id="s-indigo-bias">Bias testing as a programme, not an event</h3>
<p>Run it before deployment, on a schedule afterwards, and on any material retrain. Three things
make the difference between a test and a programme:</p>
<ul>
<li><strong>Decide the metric first, in writing.</strong> Demographic parity, equalised odds and
predictive parity are mutually incompatible in most real datasets. Picking after you see the results
is choosing the answer you like.</li>
<li><strong>Record the disparity even when it is within tolerance.</strong> The trend matters more
than any single reading, and you cannot reconstruct a trend from tests you did not keep.</li>
<li><strong>Write down what you will do if a disparity appears</strong> before it appears. The
options &mdash; retrain, reweight, restrict the feature set, route to human review, withdraw &mdash;
are much harder to evaluate honestly while a live model is under scrutiny.</li>
</ul>
'''

# ---------------------------------------------------------------- COST

cost_rows = [
 ("NIST AI RMF", "oss",
  "<strong>Free.</strong> Govern / Map / Measure / Manage. The best available scaffolding to organise "
  "a programme against, and it costs nothing but reading time."),
 ("The entire tooling stack", "oss",
  "<strong>Free.</strong> MLflow, Evidently, NannyML, Fairlearn, AIF360, SHAP, InterpretML, Great "
  "Expectations, Langfuse, Giskard. <strong>Governance is not a procurement problem.</strong>"),
 ("ISO/IEC 42001 &mdash; audit fees", "direct",
  "Published ranges vary widely by scope. A startup with one or two AI systems: roughly "
  "<strong>$5,000&ndash;$10,000</strong> for the certification body. A 51&ndash;200 person company at "
  "single-business-unit scope: <strong>$25,000&ndash;$75,000</strong> combined Stage 1 and Stage 2 on "
  "the accredited path."),
 ("ISO/IEC 42001 &mdash; all-in year one", "direct",
  "Startup: <strong>$15,000&ndash;$40,000</strong>. Mid-size: <strong>$20,000&ndash;$60,000</strong> "
  "direct, and up to <strong>$45,000&ndash;$100,000</strong> in implementation consulting plus "
  "<strong>$25,000&ndash;$65,000</strong> of internal labour if you are starting from nothing. "
  "<strong>Holding ISO 27001 cuts effort 40&ndash;50%.</strong>"),
 ("ISO/IEC 42001 &mdash; timeline", "direct",
  "Greenfield <strong>9&ndash;14 months</strong>. With ISO 27001 in place <strong>5&ndash;9</strong>. "
  "Mature AI governance <strong>3&ndash;6</strong>. <strong>Dominated by internal audit and "
  "management review cycles, not by the external audit.</strong> Auditor scarcity is a real "
  "scheduling constraint."),
 ("Independent validation", "direct",
  "External validators for high-risk models, priced per engagement. <strong>The realistic answer for "
  "a fintech too small for a standing second line</strong>, and defensible in a way that an internal "
  "colleague of the model owner is not."),
 ("EU AI Act exposure", "direct",
  "Not a cost until it is. <strong>&euro;35M or 7%</strong> of global turnover for prohibited "
  "practices; <strong>&euro;15M or 3%</strong> for high-risk violations; <strong>&euro;7.5M or "
  "1.5%</strong> for supplying incorrect information to authorities."),
 ("The real cost", "direct",
  "<strong>People and calendar time.</strong> Independent validation, committee cycles, documentation "
  "and rehearsal. None of it is a licence fee, all of it is weeks, and it cannot be compressed by "
  "spending more."),
]

i_cost = f'''
{registry("Governance &mdash; cost per unit", cost_rows, V)}
{warn("<strong>Do not represent ISO 42001 certification as EU AI Act compliance.</strong> Presumption of conformity flows from <em>harmonised European standards</em>, and ISO 42001's harmonisation under Article 40 was underway but incomplete as of 2026. Certification is evidence of a governed process, not a regulatory passport, and saying otherwise to a customer or a notified body is its own problem. One more procurement check: <strong>confirm your certification body is accredited for ISO 42001 specifically</strong> &mdash; early certificates were issued without accreditation and carry much less weight.")}
<p>The honest framing for a small firm: certification is worth it when a customer, an investor or a
regulator is asking for third-party verification, or when you place high-risk systems on the EU
market. If none of those apply, NIST AI RMF plus a genuinely maintained inventory delivers more
governance per rupee than a certificate would.</p>
'''

# ---------------------------------------------------------------- AMBER

a_combos = f'''
<table>
<tr><th>Combination</th><th>Works because</th></tr>
<tr><td>NIST AI RMF as the backbone &rarr; RBI draft as the control list</td><td>One structures the programme, the other tells you what you will be examined on. Free plus authoritative.</td></tr>
<tr><td>MLflow registry reconciled automatically against what is deployed</td><td>Turns "unlisted models are prohibited" from a policy into a control that cannot silently fail.</td></tr>
<tr><td>Kill switch as a runtime flag + scheduled rehearsal writing back to the inventory</td><td>The control and the evidence that it works are the same mechanism.</td></tr>
<tr><td>Override rate tracked alongside model performance</td><td>The only way to tell real oversight from a rubber stamp.</td></tr>
<tr><td>Data quality assertions in CI</td><td>Most model degradation is upstream data breakage. Catch it there, not in a drift chart three weeks later.</td></tr>
<tr><td>Glass-box models where the decision is high-risk</td><td>An EBM you can read beats a black box plus an explanation of it, and it removes a whole category of validation argument.</td></tr>
<tr><td>ISO 27001 first, then 42001</td><td>Cuts 42001 effort by 40&ndash;50% and the security floor is needed anyway.</td></tr>
</table>
<h3 id="s-amber-conflict">Combinations that conflict</h3>
<ul>
<li><strong>Validator reporting to the model owner's business line.</strong> Competence does not substitute for independence.</li>
<li><strong>An inventory maintained by hand.</strong> It is wrong within a quarter, and being wrong is now a finding.</li>
<li><strong>Relying on a vendor's safety certificate.</strong> Explicitly insufficient. You remain accountable and must validate independently.</li>
<li><strong>A kill switch that needs a deploy.</strong> Not immediate, therefore not a kill switch.</li>
<li><strong>Picking the fairness metric after seeing the results.</strong> That is choosing the answer, not measuring.</li>
<li><strong>Treating LLM features as outside model risk.</strong> They are models, they influence decisions, and they are in scope.</li>
<li><strong>ISO 42001 presented as EU AI Act compliance.</strong> It is not, and the claim is its own exposure.</li>
<li><strong>Excluding rule engines and spreadsheets from the inventory.</strong> The draft includes them by name.</li>
</ul>
'''

a_builds = f'''
<h3 id="s-amber-exp">Strong and expensive</h3>
<p><strong>Build:</strong> a standing second-line model risk function &rarr; a commercial governance
platform &rarr; ISO 42001 certification &rarr; external validation for every high-risk model &rarr;
board-approved framework with a risk committee that meets on a schedule and keeps minutes.</p>
<p><strong>Use when:</strong> you are a bank or a large NBFC with an examination cycle and enough
models that coordination is the bottleneck.</p>
<p><strong>Cost shape:</strong> headcount dominates. The platform and the certificate are rounding
errors next to the people.</p>
<p><strong>Trade:</strong> process weight slows deployment. That is the intended effect, and the
complaint that governance is slowing things down is usually a sign it is working rather than a
problem to solve.</p>

<h3 id="s-amber-def">Strong and reasonable &mdash; the default</h3>
<p><strong>Build:</strong> NIST AI RMF as the structure &rarr; the RBI draft as the control checklist
&rarr; MLflow as the registry, reconciled automatically against deployments &rarr; named owner,
validator and approver on every record &rarr; tiering that drives real process differences &rarr;
external validators engaged for high-risk models only &rarr; kill switches as runtime flags, rehearsed
on a schedule &rarr; Evidently and Great Expectations in CI &rarr; Fairlearn on a written metric
chosen in advance &rarr; an append-only evidence file.</p>
<p><strong>Use when:</strong> you have engineers, you have models in production, and you would like
the examination to be uneventful.</p>
<p><strong>Cost shape:</strong> tooling free, external validation per engagement, and the real cost is
the calendar.</p>
<p><strong>Trade:</strong> you build and maintain the programme yourself. That is the right trade,
because the programme <em>is</em> your regulatory position and no vendor can hold it for you.</p>
{note("Why this is the default even for small teams. Every enforcement pattern in this section &mdash; the OFSI case in Build Sheet 04, the FIU-IND orders, the conduct findings &mdash; turned on <strong>documentation, escalation and record-keeping</strong>, not on detection technology. Governance is the cheapest insurance available and it is almost entirely free software plus discipline.")}

<h3 id="s-amber-lean">Strong and lean</h3>
<p><strong>Build:</strong> one spreadsheet that is genuinely complete &mdash; every model, rule engine
and pricing spreadsheet, with owner, fallback and tier &rarr; a written statement of what is high risk
and why &rarr; documented self-assessment for everything below it &rarr; a kill switch that works
&rarr; monitoring you actually look at.</p>
<p><strong>Use when:</strong> pre-scale, few models, no dedicated risk function.</p>
<p><strong>Cost shape:</strong> time only.</p>
<p><strong>Trade:</strong> it does not scale past a handful of models, and the spreadsheet will go
stale. Accept that and set a date to replace it. <strong>A small, complete, honest inventory beats a
sophisticated programme with gaps</strong> &mdash; examiners find the gaps, and an incomplete list is
worse than a short one because it implies a control that is not there.</p>
{warn("Whichever grade you pick, the evidence file is the deliverable. For any model, on any day, you should be able to produce: what it does &middot; who owns it &middot; what data it used &middot; who validated it and what they found &middot; who approved it &middot; what it has done in production since &middot; what happens when it fails &middot; and when that was last tested. If assembling that takes more than an afternoon, you do not have a governance programme &mdash; you have documentation about one.")}
'''

a_next = f'''
<p>That is the ninth and final build sheet. The section now has a module and a build sheet for every
stage of a fintech AI stack, from the first document a customer uploads to the committee that signs
off the model reading it.</p>
<p>One closing observation, which is the thread running through all nine. Across every enforcement
action, penalty notice and supervisory finding referenced in this section, almost none turned on the
model being insufficiently accurate. They turned on <strong>an escalation path that did not exist, a
record that was not kept, a threshold nobody had approved, or a control that had never been
tested</strong>. The engineering in these nine sheets is genuinely hard and worth doing well. It is
not what the examination is about.</p>
<h3 id="s-amber-next">The nine build sheets</h3>
<div class="mod-grid">
<a href="/fintech-ai/identity-onboarding/build-sheet/" class="mod-card"><div class="mod-num">01 &middot; 02 &middot; 03</div><h3>Identity, Credit, Fraud</h3><p>Document reading and verification, underwriting with the hybrid architecture, and fraud detection that steps up rather than blocks.</p></a>
<a href="/fintech-ai/aml-compliance/build-sheet/" class="mod-card"><div class="mod-num">04 &middot; 05</div><h3>AML and Payments</h3><p>Sanctions lists, the matching cascade, the India freeze procedure, gateway economics and settlement reconciliation.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">06 &middot; 07</div><h3>Customer Ops and Wealth</h3><p>Grounding and the refusal gate, channel economics, suitability as rules, and the SEBI perimeter.</p></a>
<a href="/fintech-ai/infrastructure/build-sheet/" class="mod-card"><div class="mod-num">08</div><h3>Infrastructure</h3><p>Model serving, residency as code, GPU economics in India, and optimising for reversibility.</p></a>
</div>
{warn("Everything on this page is illustrative. Model risk governance in a regulated entity is a board-level obligation, and the Indian guidance referenced here was a draft at the time of writing. Nothing here is legal advice. Have your framework, your tiering policy and your validation approach reviewed by qualified counsel and your risk function before they are presented as your programme.")}
'''

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to read this build sheet", g_read),
   ("What counts as a model now", g_scope),
   ("Three lines, and what each actually does", g_lines),
 ],
 'indigo': [
   ("Raw materials — frameworks to map against", i_mat_fw),
   ("Raw materials — the tooling", i_mat_tool),
   ("How to use each one — inventory and tiering", i_inv),
   ("How to use each one — kill switch, override, bias", i_kill),
   ("Cost per unit", i_cost),
 ],
 'amber': [
   ("Best combinations", a_combos),
   ("Three recommended builds", a_builds),
   ("Where this section closes", a_next),
 ],
}

TITLE = "Governance Build Sheet"
META  = ("Every framework and tool for AI model governance: how to use each one, what it costs, and "
         "three recommended builds.")
LEAD  = ("Every framework, control and tool a fintech AI governance programme needs. What each one is "
         "for, the first working call, the gotcha nobody documents, real costs, and three recommended "
         "builds at three budgets.")

print(f"title len: {len(TITLE + ' | Clarigital')}")
print(f"meta len : {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/governance/build-sheet",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Build Sheet 09",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI"),
            ("/fintech-ai/governance/", "Governance")],
  lanes  = lanes,
)
