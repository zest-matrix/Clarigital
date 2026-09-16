#!/usr/bin/env python3
# Session 51 — Build Sheet 07: Wealth & Advisory
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

V = VERIFIED

# ---------------------------------------------------------------- GREEN

g_read = f'''
<p>The <a href="/fintech-ai/wealth-advisory/">Wealth and Advisory module</a> explains why suitability
is the obligation everything else hangs off. This page is the parts list: data sources, profiling and
optimisation components, execution rails, what each costs, and the three builds.</p>
{warn(f"Prices and rules carry a <strong>Verified {V}</strong> stamp. <strong>SEBI is the regulator for this module, not RBI</strong>, and the investment adviser framework has been amended repeatedly since December 2024. Check the current circular set before you rely on any threshold here.")}
<p>Six jobs. The first one is the one product teams want to skip, and skipping it makes everything
after it unlawful rather than merely bad.</p>
<table>
<tr><th>Job</th><th>What it does</th><th>Can you skip it?</th></tr>
<tr><td><strong>Fact find</strong></td><td>Income, obligations, dependants, horizon, existing holdings, liquidity needs.</td><td><strong>No.</strong> No fact find, no advice. Recommending without one is the defining compliance failure in this module.</td></tr>
<tr><td><strong>Risk profiling</strong></td><td>Capacity to bear loss, and tolerance for it. Two different things.</td><td>No, and conflating the two is the second defining failure.</td></tr>
<tr><td><strong>Suitability</strong></td><td>Decide what this client may hold at all.</td><td>No. This is the obligation; everything else is implementation.</td></tr>
<tr><td><strong>Allocation</strong></td><td>Choose within what suitability permits.</td><td>This is the part that looks like the product and is the least regulated.</td></tr>
<tr><td><strong>Execution</strong></td><td>Place the order or the SIP.</td><td>Yes &mdash; and if you are an adviser, you may be required to.</td></tr>
<tr><td><strong>Monitoring</strong></td><td>Watch what you already advised as markets and lives move.</td><td>No. Advice is not an event.</td></tr>
</table>
'''

g_perimeter = f'''
<p>Before any tooling decision, settle what you are. The perimeter is sharper in wealth than anywhere
else in this section, and disclaimers do not move it.</p>
<table>
<tr><th>If your product...</th><th>Then it is...</th></tr>
<tr><td>Explains how a debt fund works, generically, to everyone</td><td>Education. Outside the IA perimeter.</td></tr>
<tr><td>Tells <em>this</em> user what <em>they</em> should buy, given anything it knows about them</td><td><strong>Investment advice.</strong> Requires registration.</td></tr>
<tr><td>Shows a "recommended for you" fund list driven by a profile</td><td><strong>Investment advice</strong>, whatever the screen calls it.</td></tr>
<tr><td>Earns commission from the product it recommends</td><td>Distribution, and it cannot be advice at the same time.</td></tr>
</table>
{warn("<strong>&ldquo;For educational purposes only&rdquo; is not a defence.</strong> SEBI enforcement is explicit that a disclaimer does not excuse unregistered advisory activity &mdash; inside a course, a private group, or a chatbot reply. The December 2025 order in the Avadhut Sathe matter impounded <strong>&#8377;546 crore</strong> and imposed a market ban. Whatever your product does is what it is, regardless of the label above it.")}
<p>Two more boundaries that catch product teams:</p>
<ul>
<li><strong>IAs cannot provide trading calls.</strong> That is a specific prohibition, not a matter of
framing.</li>
<li><strong>Advice and execution are structurally segregated.</strong> Segregation at client level,
and at group level for non-individuals. An individual cannot do both simultaneously, so a
robo-advisory platform needs a separate entity &mdash; a company or an LLP. Adviser recommends,
client authorises, execution happens through brokers or AMCs. Fee-only, no commission from product
manufacturers.</li>
</ul>
<p>The finfluencer framework closes the remaining gap: registered entities may not pay, refer to, or
share data with unregistered finfluencers; educational content must not carry stock price data less
than three months old; no performance claims, no return guarantees.</p>
'''

g_ai = f'''
<p>Most regulators are still deciding what they think about AI. SEBI has decided, and its position
runs opposite to the industry's hope.</p>
{note("<strong>Using AI does not reduce your responsibility. It increases it.</strong> Responsibility for advisory and research services lies <em>solely</em> with the IA or RA, <strong>irrespective of the scale and scenario of AI usage</strong>. You must ensure data security, integrity and transparency of the advice derived, and <strong>disclose the extent of AI usage to the client</strong>. There is no arrangement in which the tool carries any of it.")}
<p>The robo-specific expectations are the closest thing to a written build specification any Indian
regulator has published for an AI product. Treat them as the acceptance criteria:</p>
<ul>
<li>The algorithm is <strong>tested for correctness and transparency</strong>, and the testing is
documented.</li>
<li>A <strong>qualified person oversees algorithm output</strong> &mdash; a named human, not a team.</li>
<li>Clients are <strong>told the advice comes from a system</strong>.</li>
<li><strong>No commission conflicts</strong> anywhere in the recommendable universe.</li>
<li>The whole thing is <strong>inspection-ready at all times</strong>, not preparable on request.</li>
</ul>
<p>Read that list as an architecture. "Tested for correctness" means the suitability logic must be
deterministic enough to have a correct answer. "Inspection-ready at all times" means the reasoning
behind every past recommendation is stored, not reconstructible. Neither is achievable if a language
model decides what a client may hold.</p>
'''

# ---------------------------------------------------------------- INDIGO

i_mat_data = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>AMFI NAV feed</strong> <span class="pill p-direct">direct</span></td><td>Daily NAV for every Indian mutual fund scheme, free, authoritative. The backbone of almost every Indian wealth product.</td><td>amfiindia.com</td></tr>
<tr><td><strong>Kite Connect</strong></td><td>Zerodha's API. Personal tier gives order placement and holdings with <strong>no market data</strong>; the paid tier adds live and historical data.</td><td>kite.trade</td></tr>
<tr><td><strong>Upstox / Angel SmartAPI / Dhan</strong></td><td>Broker APIs with data plus execution. Data scope is limited to what the broker itself licenses.</td><td>upstox.com/developer</td></tr>
<tr><td><strong>TrueData / Global Datafeeds</strong></td><td>Market data vendors: real-time streaming and historical across NSE, BSE and MCX. Exchange approvals required where applicable.</td><td>truedata.in</td></tr>
<tr><td><strong>Direct exchange feeds</strong> <span class="pill p-indirect">indirect</span></td><td>Lowest latency tick data through authorised vendors. Colocation, institutional cost, not relevant to an advisory product.</td><td>nseindia.com</td></tr>
<tr><td><strong>BSE StAR MF / NSE NMF II</strong> <span class="pill p-indirect">indirect</span></td><td>Mutual fund transaction rails. Reached through a registered intermediary.</td><td>bsestarmf.in</td></tr>
<tr><td><strong>Account Aggregator</strong> <span class="pill p-indirect">indirect</span></td><td>Consented holdings and bank data. The cleanest route to a real fact find, and consent is explicit and revocable.</td><td>sahamati.org.in</td></tr>
<tr><td><strong>CAMS / KFintech / MF Central</strong> <span class="pill p-indirect">indirect</span></td><td>RTA data. Consolidated account statements — how you discover what the client already holds.</td><td>mfcentral.com</td></tr>
</table>
{warn("<strong>The licensing trap in this section is market data redistribution.</strong> A broker API's data licence generally covers <em>you</em> using it for <em>your own</em> account. Displaying that same exchange data to your clients in a product is redistribution, and redistribution usually needs an exchange data licence or an authorised-vendor arrangement. Teams build a customer-facing product on a ₹500-a-month broker key and discover the terms during diligence. Same shape as the OpenSanctions trap in <a href=\"/fintech-ai/aml-compliance/build-sheet/\">Build Sheet 04</a> and the Elastic Licence trap in the monitoring section: <strong>the software is cheap, the licence is the product.</strong> Read the data terms before the API docs.")}
'''

i_mat_calc = f'''
<p>The calculation layer is almost entirely open source, and that is the right answer here. A
suitability engine you cannot read line by line cannot be "tested for correctness and
transparency".</p>
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>cvxpy</strong> <span class="pill p-oss">oss</span></td><td>Convex optimisation. Express allocation as constraints plus an objective, which is exactly the shape suitability requires.</td><td>cvxpy.org</td></tr>
<tr><td><strong>PyPortfolioOpt / Riskfolio-Lib</strong> <span class="pill p-oss">oss</span></td><td>Mean-variance, risk parity, hierarchical risk parity, efficient frontier. Readable implementations you can audit.</td><td>pyportfolioopt.readthedocs.io</td></tr>
<tr><td><strong>NumPy / pandas / SciPy</strong> <span class="pill p-oss">oss</span></td><td>Returns, covariance, drawdown, glide-path arithmetic. Most of what an advisory product computes.</td><td>numpy.org</td></tr>
<tr><td><strong>Great Expectations / Pandera</strong> <span class="pill p-oss">oss</span></td><td>Data validation on the NAV and price feeds. A stale or corrupt NAV silently changes advice.</td><td>pandera.readthedocs.io</td></tr>
<tr><td><strong>Postgres with temporal tables</strong> <span class="pill p-oss">oss</span></td><td>The inspection-ready record: what you advised, on what facts, under which rule version, at what time.</td><td>postgresql.org</td></tr>
<tr><td><strong>LLM (any)</strong></td><td>Explanation, document reading, fact-find conversation, drafting. <strong>Never</strong> the suitability decision.</td><td>&mdash;</td></tr>
</table>
{note("There is no meaningful commercial optimiser market to buy into at the scale most Indian advisory products operate. The maths is well understood and the libraries are mature. What you would actually be buying from a wealthtech platform is the <em>plumbing</em> &mdash; RTA integrations, StAR MF connectivity, reporting, compliance workflow &mdash; not the allocation logic. Evaluate on that basis.")}
'''

code_profile = code('Python — capacity, tolerance, and the rule that inverts most products', r'''from dataclasses import dataclass

@dataclass
class Profile:
    capacity: int      # 1-5. What the client can AFFORD to lose. Objective.
    tolerance: int     # 1-5. What the client is WILLING to lose. Subjective.
    required: int      # 1-5. What the stated goal would DEMAND. Not a permission.

def binding_risk(p: Profile) -> dict:
    # The whole module in one line. The binding constraint is the LOWER of what
    # the client can bear and what they are willing to bear. `required` never
    # raises it -- it is a property of the goal, not of the client.
    binding = min(p.capacity, p.tolerance)

    out = {"binding": binding, "capacity": p.capacity, "tolerance": p.tolerance}

    if p.required > binding:
        # THE GOAL CHANGES, NOT THE PORTFOLIO.
        # Optimising toward a stated goal is the natural engineering framing and
        # it inverts the obligation. A system that raises risk to reach a target
        # is not advising, it is rationalising.
        out["action"] = "renegotiate_goal"
        out["options"] = ["extend_horizon", "increase_contribution", "reduce_target"]
        out["forbidden"] = "increase_portfolio_risk_to_meet_target"
    else:
        out["action"] = "proceed"

    # Capacity far below tolerance is the dangerous asymmetry: a client happy to
    # take risk they cannot afford. Capacity always wins, and the gap is worth
    # recording because it predicts complaints after a drawdown.
    if p.tolerance - p.capacity >= 2:
        out["flag"] = "tolerance_exceeds_capacity"
        out["note"] = "document the conversation; expect regret risk in a fall"
    return out

# WHAT TO CHECK
# [ ] capacity is computed from FACTS -- income stability, dependants, emergency
#     fund, horizon, debt -- not from a questionnaire about feelings
# [ ] tolerance is measured with scenario questions ("your 10 lakh becomes 7
#     lakh in four months; what do you do?"), not a 1-10 slider. Stated tolerance
#     is weak evidence and collapses in a real drawdown
# [ ] `required` is stored but NEVER feeds the allocation ceiling
# [ ] no fact find on file => the function is not called at all. No advice
# [ ] the profile is versioned. When it changes, the change and its reason are
#     recorded, because the next question after a complaint is "on what basis"
# [ ] profiles expire. A three-year-old risk profile is not a current one
# [ ] the client sees their own capacity and tolerance scores and can dispute
#     them. An unexplainable score is not transparent advice
''')

i_profile = f'''
<h3 id="s-indigo-bind">The one-line rule the whole module rests on</h3>
<p>Capacity is what the client can afford to lose. Tolerance is what they are willing to lose. They
are different measurements with different evidence, and the binding constraint is the lower of the
two.</p>
{code_profile}
<p><strong>The gotcha nobody documents:</strong> the natural engineering framing is "the client wants
&#8377;2 crore in fifteen years; solve for the portfolio that gets there". That framing is the
violation. If the goal demands more risk than the client can bear, <strong>the goal changes</strong>
&mdash; longer horizon, larger contributions, smaller target &mdash; not the portfolio. Automated
advice systems get this wrong constantly, because goal-seeking is what optimisers are for and nobody
notices that the constraint has been quietly relaxed to make the objective reachable.</p>
'''

code_suit = code('Python — suitability as rules, optimisation strictly inside them', r'''import cvxpy as cp
import numpy as np

# Two layers, and the order is the point. Deterministic rules decide WHAT IS
# PERMITTED. Optimisation decides HOW TO ALLOCATE within that. A model never
# expands the permitted set -- that is what makes the system testable for
# correctness, which is a stated SEBI expectation for robo-advisory.

def permitted_universe(profile, client, catalogue):
    allowed, excluded = [], []
    for f in catalogue:
        reasons = []
        if f.risk_band > profile["binding"]:
            reasons.append("exceeds_binding_risk")
        if f.min_horizon_years > client["horizon_years"]:
            reasons.append("horizon_too_short")
        if f.lock_in_years > 0 and client["needs_liquidity_within"] < f.lock_in_years:
            reasons.append("lock_in_vs_liquidity_need")
        if f.pays_commission:
            reasons.append("commission_conflict")   # fee-only: no exceptions
        if f.category in client.get("excluded_categories", []):
            reasons.append("client_exclusion")
        (allowed if not reasons else excluded).append(
            {"fund": f.id, "reasons": reasons})
    return allowed, excluded          # BOTH are stored. Exclusions are evidence.

def allocate(allowed, mu, sigma, max_single=0.25, cap_by_band=None):
    n = len(allowed)
    w = cp.Variable(n)
    constraints = [cp.sum(w) == 1, w >= 0, w <= max_single]
    for band, cap in (cap_by_band or {}).items():
        idx = [i for i, a in enumerate(allowed) if a["band"] == band]
        if idx:
            constraints.append(cp.sum(w[idx]) <= cap)
    # Objective only ever ranks INSIDE the permitted set.
    prob = cp.Problem(cp.Maximize(mu @ w - 0.5 * cp.quad_form(w, sigma)), constraints)
    prob.solve()
    if prob.status not in ("optimal", "optimal_inaccurate"):
        return {"ok": False, "reason": "infeasible", "action": "human_review"}
    return {"ok": True, "weights": np.round(w.value, 4).tolist()}

# WHAT TO CHECK
# [ ] the EXCLUSION LIST is persisted with the recommendation. "Why was this
#     fund not recommended" is a real question and the answer must already exist
# [ ] an infeasible optimisation goes to a human. It usually means the permitted
#     set is too small for the goal -- which is information, not an error
# [ ] no code path lets the optimiser add an instrument that permitted_universe
#     excluded. Assert it in a test, not in a comment
# [ ] covariance estimated over a stated window, and the window is a versioned
#     parameter. Changing it changes advice
# [ ] the recommendable universe contains NO commission-paying products at all.
#     Fee-only is a structural property, not a filter you can switch off
# [ ] every run stores: rule version, profile version, catalogue snapshot, mu/
#     sigma inputs, solver status, output. This is "inspection-ready"
# [ ] the named qualified person who oversees output is recorded per run
''')

i_suit = f'''
<h3 id="s-indigo-rules">The hybrid, and why it is not optional here</h3>
<p>This is the same architecture as the credit module and for the same reason: a model never decides
what is permitted, only how to allocate within what is permitted.</p>
{code_suit}
<p><strong>The gotcha nobody documents:</strong> store the <em>exclusions</em>, not just the
recommendation. Every advisory product persists what it advised. Almost none persists what it
declined to advise and why. "Why did your system never recommend this fund to this client" is a
question with a correct answer, and if you have to recompute it from a catalogue that has since
changed, you cannot answer it at all. The exclusion list is small, cheap to store, and it is the
difference between inspection-ready and inspection-panicked.</p>

<h3 id="s-indigo-llm">Where the language model belongs</h3>
<p>It belongs in three places, all of them either side of the decision rather than inside it.</p>
<ul>
<li><strong>The fact find.</strong> A conversational intake that extracts structured facts is a good
use, provided the extracted facts are shown back to the client and confirmed before they are used.</li>
<li><strong>Explanation.</strong> Turning a deterministic recommendation into prose the client
understands, grounded strictly in the recommendation's own stored reasoning.</li>
<li><strong>Document reading.</strong> Parsing a consolidated account statement to discover existing
holdings.</li>
</ul>
{warn("It does not belong in the suitability decision, the risk score, or the allocation. Not because models are bad at arithmetic, but because <strong>&ldquo;tested for correctness&rdquo; requires a correct answer to exist</strong>, and because you must be able to reproduce a recommendation made two years ago from stored inputs. A model that has since been updated cannot do that. The determinism argument here is about reproducibility and inspection, not about capability.")}
'''

code_monitor = code('Python — monitoring, drift and the glide path', r'''from datetime import date

# Advice is not an event. What you recommended becomes something you are
# responsible for watching -- as markets move, and as the client's life moves.

def review(holding, profile, today=None):
    today = today or date.today()
    events = []

    # 1. ALLOCATION DRIFT. Bands, not a fixed calendar. A quarterly rebalance
    #    that fires when nothing has drifted is cost without benefit; one that
    #    waits three months while equity runs to 80% is a control that missed.
    for asset, target in holding["targets"].items():
        actual = holding["actual"][asset]
        if abs(actual - target) > holding["band"]:
            events.append({"type": "drift", "asset": asset,
                           "target": target, "actual": actual})

    # 2. GLIDE PATH. Horizon shortens every single day; the suitable allocation
    #    should move continuously with it, not in a jump at a review meeting.
    years_left = (holding["goal_date"] - today).days / 365.25
    glide_target = max(0.20, min(0.80, 0.10 + 0.045 * years_left))
    if abs(holding["targets"]["equity"] - glide_target) > 0.05:
        events.append({"type": "glide_path_due",
                       "current": holding["targets"]["equity"],
                       "should_be": round(glide_target, 3),
                       "years_left": round(years_left, 2)})

    # 3. THE PROFILE ITSELF AGES. Facts go stale faster than portfolios.
    if (today - profile["as_of"]).days > 365:
        events.append({"type": "profile_stale", "as_of": str(profile["as_of"]),
                       "action": "re_verify_before_any_new_advice"})

    # 4. SUITABILITY REGRESSION. A holding that was suitable at recommendation
    #    can stop being suitable without anyone transacting -- the fund changed
    #    mandate, or the client's capacity fell.
    for f in holding["funds"]:
        if f["current_risk_band"] > profile["binding"]:
            events.append({"type": "now_unsuitable", "fund": f["id"],
                           "was": f["risk_band_at_advice"],
                           "now": f["current_risk_band"],
                           "action": "notify_client_and_review"})
    return events

# WHAT TO CHECK
# [ ] drift uses BANDS; a calendar review is a reporting cadence, not a control
# [ ] the glide path is continuous and its formula is versioned. Clients near a
#     goal date are the ones a market fall actually hurts
# [ ] every review RUN is recorded, including the ones that found nothing. "We
#     checked and there was nothing to do" is evidence; silence is not
# [ ] a fund changing mandate or risk band triggers a re-check of every client
#     holding it, not just the next person to log in
# [ ] the client is notified when something becomes unsuitable, even if you are
#     not recommending a change -- especially then
# [ ] tax and exit-load consequences are computed BEFORE a rebalance is
#     suggested. A suitable rebalance that destroys returns after tax is not
#     suitable advice
# [ ] notifications respect the education/advice boundary. "Your equity is above
#     target" is a fact; "you should switch to X" is advice and needs the rest
#     of this pipeline behind it
''')

i_monitor = f'''
<p>The module's phrase for this is that glide paths beat periodic reviews, and the code above is
what that means in practice. A horizon shortens every day. An allocation that steps down at an
annual meeting is wrong for 364 days out of 365, and it is most wrong in the year before the client
needs the money.</p>
{code_monitor}
<p><strong>The gotcha nobody documents:</strong> record the reviews that found nothing. Advisory
products log recommendations and log transactions, and log nothing at all on the days when the
monitoring ran and everything was fine. Then a client's portfolio falls, they complain, and the
question is whether you were watching. A run record with a null result answers it. An absence of
records looks identical to an absence of monitoring, and you will be unable to tell the difference
yourself.</p>
'''

# ---------------------------------------------------------------- COST

cost_rows = [
 ("AMFI NAV feed", "oss",
  "<strong>Free.</strong> Daily NAV for every Indian scheme, published by AMFI. Authoritative and "
  "sufficient for most mutual-fund advisory products. The cost is the ingestion and validation, "
  "not the data."),
 ("Broker API &mdash; execution only", "direct",
  "<strong>Kite Connect Personal: free</strong> &mdash; order placement, positions, holdings and "
  "funds, with <strong>no live or historical market data</strong>. Bring your own data source."),
 ("Broker API &mdash; with data", "direct",
  "<strong>Kite Connect paid: &#8377;500 per month per API key</strong>, live and historical market "
  "data included at no additional cost. Per-order brokerage still applies separately."),
 ("Per-order execution cost", "direct",
  "Zerodha intraday <strong>&#8377;20 or 0.03%, whichever is lower</strong>, per executed order. "
  "Upstox ran <strong>&#8377;10 per executed order via API</strong> under a developer scheme through "
  "31 March 2026 &mdash; confirm the current schedule rather than assuming it continued."),
 ("Market data vendors", "direct",
  "TrueData, Global Datafeeds and similar: real-time streaming and historical across NSE, BSE and "
  "MCX on published plans. <strong>Exchange approvals are required where applicable</strong> &mdash; "
  "this is the licence, not the subscription."),
 ("Direct exchange feed", "indirect",
  "Lowest-latency tick data through authorised vendors, with colocation. Institutional cost "
  "structure. <strong>Not relevant to an advisory product</strong> and a sign of a mis-specified "
  "requirement if it appears in your plan."),
 ("SEBI IA registration", "direct",
  "<strong>&#8377;15,000</strong> registration fee, payable within 15 days of approval. The former "
  "<strong>&#8377;25 lakh net worth</strong> requirement for corporate IAs was replaced in December "
  "2024 by a <strong>deposit-based system</strong>, held under lien in favour of the IAASB "
  "(<strong>BSE Limited</strong>, appointed July 2024 for five years). <strong>Budget 3&ndash;6 "
  "months</strong> for the process."),
 ("Ongoing compliance", "direct",
  "Annual compliance audit by a <strong>CA, CS or CMA</strong>, reporting line-wise compliance "
  "against every provision of the IA Regulations, with adverse findings submitted within the "
  "specified timeline. A non-individual IA may appoint an <strong>independent professional</strong> "
  "(ICAI / ICSI / ICMAI) with the relevant NISM certification as compliance officer."),
 ("The fee cap &mdash; your revenue ceiling", "direct",
  "<strong>&#8377;1.51 lakh per annum per client</strong> for individuals and HUFs, revised for cost "
  "inflation and reviewed roughly every three years. Fees charged either on <strong>assets under "
  "advice</strong> or as a <strong>fixed fee</strong>. <strong>This is a hard ceiling on revenue per "
  "retail client and it should be the first number in your model.</strong>"),
 ("Corporatisation trigger", "direct",
  "An individual IA must convert to a non-individual entity on reaching <strong>300 clients</strong> "
  "or <strong>&#8377;3 crore</strong> in fee collection in a financial year, whichever comes first "
  "(raised from 150 clients). Notify SEBI immediately, then <strong>3 months</strong> for in-principle "
  "approval and <strong>3 more</strong> to complete, continuing to onboard throughout."),
 ("Calculation stack", "oss",
  "<strong>Free.</strong> cvxpy, PyPortfolioOpt, Riskfolio-Lib, NumPy, SciPy, Pandera. There is no "
  "meaningful optimiser to buy at Indian retail advisory scale &mdash; what a wealthtech platform "
  "actually sells you is RTA and StAR MF plumbing, reporting and compliance workflow."),
]

i_cost = f'''
{registry("Wealth and advisory &mdash; cost per unit", cost_rows, V)}
{warn("<strong>Model the fee cap before anything else.</strong> &#8377;1.51 lakh per client per year is the ceiling, and the realistic average retail fee is a small fraction of it. That single number decides whether your product can afford human oversight per client, which in turn decides whether it can be advisory at all or has to be execution-only. Most Indian robo-advisory business plans fail at this line, not at the technology.")}
<p>One structural note on eligibility, because it changes hiring. Since November 2025 a graduate in
<strong>any</strong> discipline may register as an IA or RA provided they hold the required NISM
certification &mdash; the finance, commerce, business or economics degree requirement is gone. The
same qualification benchmark now extends to persons associated with investment advice. The
constraint on building an advisory team has shifted from degrees to certification.</p>
'''

# ---------------------------------------------------------------- AMBER

a_combos = f'''
<table>
<tr><th>Combination</th><th>Works because</th></tr>
<tr><td>Account Aggregator fact find + deterministic suitability</td><td>Consented real holdings rather than self-reported ones, feeding rules that can be tested for correctness.</td></tr>
<tr><td>Rules decide the universe &rarr; cvxpy allocates inside it</td><td>Separates the regulated decision from the mathematical one. Only this shape is inspectable.</td></tr>
<tr><td>AMFI NAV + your own validation layer</td><td>Free, authoritative, and the validation catches the stale-NAV failure that silently changes advice.</td></tr>
<tr><td>Continuous glide path + banded drift</td><td>Two different triggers for two different causes. A calendar handles neither well.</td></tr>
<tr><td>LLM for intake and explanation, never for decision</td><td>Gets the conversational product without losing reproducibility or the correctness test.</td></tr>
<tr><td>Stored exclusions alongside stored recommendations</td><td>Answers "why not this fund" without recomputation against a catalogue that has since changed.</td></tr>
<tr><td>Temporal tables for profile, rules and catalogue</td><td>Reproducing a two-year-old recommendation needs all three as they were, not as they are.</td></tr>
</table>
<h3 id="s-amber-conflict">Combinations that conflict</h3>
<ul>
<li><strong>Advice plus commission.</strong> Structurally incompatible. Not a disclosure problem, an entity problem.</li>
<li><strong>Advice and execution in one individual.</strong> A robo platform needs a separate company or LLP.</li>
<li><strong>An LLM in the suitability path.</strong> Breaks reproducibility and the correctness test at once.</li>
<li><strong>Optimising toward the client's stated target.</strong> Silently relaxes the risk constraint to make the objective reachable. The goal changes, not the portfolio.</li>
<li><strong>&ldquo;Educational&rdquo; personalised recommendations.</strong> The disclaimer does not change what it is, and enforcement has been expensive.</li>
<li><strong>A customer-facing product on a personal broker data key.</strong> Redistribution needs a licence.</li>
<li><strong>Periodic-only review.</strong> Wrong for most of the year and most wrong close to the goal date.</li>
<li><strong>Trading calls from an IA.</strong> Specifically prohibited.</li>
</ul>
'''

a_builds = f'''
<h3 id="s-amber-exp">Strong and expensive</h3>
<p><strong>Build:</strong> registered non-individual IA with a separate execution entity, a
commercial wealthtech platform for RTA and StAR MF plumbing and reporting, licensed market data with
proper redistribution rights, a qualified oversight team, and full temporal audit infrastructure.</p>
<p><strong>Use when:</strong> you are advising on meaningful assets, clients expect statements and
reviews, and the fee per client can support a human in the loop.</p>
<p><strong>Cost shape:</strong> registration and deposit, platform licensing, data licensing, and
&mdash; dominating everything &mdash; the qualified people the regulations require.</p>
<p><strong>Trade:</strong> the economics only work at higher ticket sizes. Against a
&#8377;1.51 lakh ceiling and a realistic average far below it, this build needs either wealthy
clients or a lot of them.</p>

<h3 id="s-amber-def">Strong and reasonable &mdash; the default</h3>
<p><strong>Build:</strong> registered IA &rarr; Account Aggregator and RTA statements for the fact
find &rarr; deterministic capacity, tolerance and suitability rules you wrote and can read &rarr;
cvxpy or PyPortfolioOpt allocating strictly inside the permitted set &rarr; AMFI NAV with a
validation layer &rarr; execution through a broker or StAR MF via a separate entity &rarr; banded
drift plus a continuous glide path &rarr; temporal tables recording profile, rule version, catalogue
snapshot and exclusions on every run &rarr; an LLM for intake and explanation only.</p>
<p><strong>Use when:</strong> you have engineers and you intend to be a real adviser rather than a
distributor with a quiz.</p>
<p><strong>Cost shape:</strong> registration, near-zero for the calculation stack, modest data costs,
and the named qualified person.</p>
<p><strong>Trade:</strong> you write and maintain the suitability rules. That is the right trade
&mdash; those rules <em>are</em> your regulatory position, and a vendor cannot hold it for you.</p>
{note("Why the calculation layer is built rather than bought here, unlike the screening layer in Build Sheet 04. There, you were buying <em>data</em> you could not assemble yourself. Here the maths is public, the libraries are mature and auditable, and the regulator expects you to demonstrate correctness and transparency of the algorithm. A closed optimiser makes that harder, not easier.")}

<h3 id="s-amber-lean">Strong and lean</h3>
<p><strong>Build:</strong> stay outside the advisory perimeter deliberately &mdash; genuinely generic
education with no personalisation &rarr; calculators that compute rather than recommend &rarr;
execution-only access if you have the licence for it &rarr; no "recommended for you" anywhere in the
product.</p>
<p><strong>Use when:</strong> you are pre-registration, or advice is not the business you actually
want to be in.</p>
<p><strong>Cost shape:</strong> data and hosting.</p>
<p><strong>Trade:</strong> no personalisation at all, and that boundary needs active defence.</p>
{warn("<strong>The drift pattern is the risk in this build, and it is gradual.</strong> A calculator acquires a &ldquo;based on your answers&rdquo; label. A comparison table acquires a default sort. A generic list acquires a &ldquo;popular with people like you&rdquo; badge. No single change looks like crossing the line and the product ends up on the other side of it. Three tests worth applying to any screen: does it use anything we know about <em>this</em> user · would a reasonable user read it as a recommendation · would we be comfortable if a regulator saw it without the disclaimer. If the honest answer to the first is yes, you are advising.")}
'''

a_next = f'''
<p>Two things to settle before you write code, because both take longer than the build.</p>
<p><strong>Registration.</strong> Three to six months, realistically. Discovering it at launch is the
most common sequencing mistake in this module, and the recent amendments cut in both directions
&mdash; the qualification bar is lower and the corporatisation threshold is higher, but the
compliance audit and disclosure obligations are heavier.</p>
<p><strong>Accessibility.</strong> Obligations under the Rights of Persons with Disabilities Act
apply to regulated entities' digital platforms. It is routinely missed by product teams, it is cheap
to design in from the start, and it is expensive to retrofit into a completed advisory journey.</p>
<h3 id="s-amber-next">What this feeds</h3>
<div class="mod-grid">
<a href="/fintech-ai/credit-underwriting/build-sheet/" class="mod-card"><div class="mod-num">SHEET 02</div><h3>Credit &amp; Underwriting</h3><p>The same hybrid architecture — deterministic rules decide eligibility, the model ranks inside them.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">SHEET 06</div><h3>Customer Operations</h3><p>The education/advice boundary is enforced in support replies too. A chatbot answer can be unregistered advice.</p></a>
<a href="/fintech-ai/regulation-india/" class="mod-card"><div class="mod-num">REFERENCE</div><h3>India Regulation</h3><p>SEBI, RBI and the DPDP Act, and which of them applies to which part of your product.</p></a>
<a href="/fintech-ai/governance/" class="mod-card"><div class="mod-num">MODULE 09</div><h3>Governance</h3><p>Algorithm testing, named oversight and the inspection-ready record — the three robo expectations, as a system.</p></a>
</div>
{warn("Everything on this page is illustrative. Investment advice in India is a registered activity under SEBI regulation and unregistered advisory activity carries serious enforcement consequences. Nothing here is legal or investment advice. Have your perimeter, your suitability logic and your disclosures reviewed by qualified counsel and a compliance professional before any client sees a recommendation.")}
'''

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to read this build sheet", g_read),
   ("What you are allowed to build", g_perimeter),
   ("SEBI on AI: responsibility goes up, not down", g_ai),
 ],
 'indigo': [
   ("Raw materials — market and fund data", i_mat_data),
   ("Raw materials — profiling, optimisation, record", i_mat_calc),
   ("How to use each one — capacity and tolerance", i_profile),
   ("How to use each one — suitability and allocation", i_suit),
   ("How to use each one — monitoring what you advised", i_monitor),
   ("Cost per unit", i_cost),
 ],
 'amber': [
   ("Best combinations", a_combos),
   ("Three recommended builds", a_builds),
   ("What next", a_next),
 ],
}

TITLE = "Wealth and Advisory Build Sheet"
META  = ("Every data source, profiling and optimisation tool for advisory: how to use each one, what "
         "it costs, and three recommended builds.")
LEAD  = ("Every data source, profiling component and optimisation library an advisory product needs. "
         "What each one is for, the first working call, the gotcha nobody documents, real costs, and "
         "three recommended builds at three budgets.")

print(f"title len: {len(TITLE + ' | Clarigital')}")
print(f"meta len : {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/wealth-advisory/build-sheet",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Build Sheet 07",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI"),
            ("/fintech-ai/wealth-advisory/", "Wealth and Advisory")],
  lanes  = lanes,
)
