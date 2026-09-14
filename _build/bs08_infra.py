#!/usr/bin/env python3
# Session 57 — Build Sheet 08: Infrastructure
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

V = VERIFIED

# ---------------------------------------------------------------- GREEN

g_read = f'''
<p>The <a href="/fintech-ai/infrastructure/">Infrastructure module</a> explains why your licence
decides your architecture. This page is the parts list: what to run where, what each option costs per
unit, and the three builds.</p>
{warn(f"Prices carry a <strong>Verified {V}</strong> stamp. Model pricing is the fastest-moving number anywhere in this section &mdash; one provider cut a model by 80% in a single day during 2026 and another cancelled a scheduled increase. Treat every figure as an anchor for shape, not a quote.")}
<p>Fintech infrastructure is three planes that fail differently and should be decided separately.</p>
<table>
<tr><th>Plane</th><th>What it holds</th><th>What happens when it breaks</th></tr>
<tr><td><strong>Ledger</strong></td><td>Balances. The authoritative record of who has what.</td><td>You stop. There is no degraded mode for a ledger that is wrong.</td></tr>
<tr><td><strong>Operational</strong></td><td>Events, queues, workflows, the things that move money between systems.</td><td>Things queue up. Painful, recoverable, usually invisible to the customer for a while.</td></tr>
<tr><td><strong>AI serving</strong></td><td>Models, features, retrieval, inference.</td><td><strong>You fall back to rules and carry on.</strong> If you cannot, you designed it wrong.</td></tr>
</table>
{note("That third row is the whole design brief for AI infrastructure in a regulated firm. <strong>Every AI component must have a defined behaviour when it is unavailable</strong>, and that behaviour must be acceptable rather than merely survivable. A fraud model that is down means every transaction goes to the rules engine, not that payments stop. Build the fallback first and the model second. Teams that do it the other way round discover their fallback on the day they need it.")}
'''

g_rev = f'''
<p>The module's phrase is <em>optimise for reversibility first</em>. Here is what that means as an
engineering rule, because it is the single decision that determines how much the next five years
cost.</p>
<p>Almost every infrastructure choice in a fintech is made once, under time pressure, on incomplete
information. You will be wrong about some of them. The question is not how to be right &mdash; it is
how much a wrong answer costs to undo.</p>
<table>
<tr><th>Decision</th><th>Cost to reverse</th><th>So decide it&hellip;</th></tr>
<tr><td>Which model you call</td><td>Hours, if you put an adapter in front</td><td>Quickly. Change it often.</td></tr>
<tr><td>Which cloud region you run in</td><td>Weeks</td><td>Carefully, once.</td></tr>
<tr><td>Which observability vendor</td><td>Weeks, if you emit OpenTelemetry</td><td>Quickly. Months if you did not.</td></tr>
<tr><td>Which core banking platform</td><td><strong>Years</strong></td><td>Slowly. This is the one to get right.</td></tr>
<tr><td>Your data model for the ledger</td><td><strong>Effectively never</strong></td><td>Slowly, and write it down.</td></tr>
</table>
<p>The practical consequence is that <strong>the cheap reversals should be behind interfaces and the
expensive ones should be boring</strong>. An adapter in front of your model provider costs a day and
buys you the ability to switch when a price moves 80%. An adapter in front of your core banking
platform is a fantasy &mdash; nobody has ever successfully abstracted a core.</p>
'''

g_res = f'''
<p>Before any tooling decision, settle where data is allowed to be. In India this is not a
preference.</p>
<p>The RBI's payment data storage direction requires the <strong>full end-to-end transaction
details</strong> for payment systems to be stored <strong>only in India</strong>. Data may be
processed abroad, but it must be brought back and the foreign copy deleted within the specified
window. The DPDP Act adds consent, purpose limitation and breach notification on top, for personal
data generally.</p>
{warn("<strong>The line teams get wrong is what counts as &ldquo;processing abroad&rdquo;.</strong> Sending a transaction narration to a model API hosted outside India is a cross-border transfer of payment data. It does not stop being one because it is a single string, because it is transient, or because the provider says they do not train on it. If your prompt contains payment data, your prompt is in scope. <strong>Decide this per field, in code, before the call</strong> &mdash; not in a policy document that the inference path never reads.")}
<p>This has an architectural consequence that surprises people: <strong>the cheapest model is often
not available to you</strong> for the workloads that matter most. That is not a reason to give up on
cost. It is a reason to design a router that knows which data may leave and which may not, and to
keep an in-country path for the second category.</p>
'''

# ---------------------------------------------------------------- INDIGO

i_mat_serve = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>Frontier APIs</strong></td><td>Best quality, highest cost, hosted outside India unless the provider offers a region you can use.</td><td>provider pricing pages</td></tr>
<tr><td><strong>Mid-tier APIs</strong></td><td>The production default for most work. The most contested price point in the market.</td><td>provider pricing pages</td></tr>
<tr><td><strong>Budget and open-weight APIs</strong></td><td>An order of magnitude cheaper. Correct for classification, extraction, routing and first-pass drafting.</td><td>provider pricing pages</td></tr>
<tr><td><strong>vLLM / TGI / llama.cpp</strong> <span class="pill p-oss">oss</span></td><td>Self-hosted serving. vLLM is the default for throughput; llama.cpp for small models on modest hardware.</td><td>docs.vllm.ai</td></tr>
<tr><td><strong>Indian GPU clouds</strong></td><td>E2E, Cyfuture, AceCloud, Jarvis Labs, Yotta, Tata. INR billing, India-resident data centres, DPDP documentation.</td><td>e2enetworks.com</td></tr>
<tr><td><strong>IndiaAI Mission compute</strong></td><td>Government-subsidised GPU capacity. <strong>The cheapest legitimate GPU in India, and it is not on any commercial price list.</strong></td><td>indiaai.gov.in</td></tr>
<tr><td><strong>pgvector / Qdrant</strong> <span class="pill p-oss">oss</span></td><td>Vector search. pgvector inside the Postgres you already run is right for most teams.</td><td>github.com/pgvector/pgvector</td></tr>
<tr><td><strong>OpenTelemetry</strong> <span class="pill p-oss">oss</span></td><td>Vendor-neutral traces, metrics and logs. The thing that makes your observability decision reversible.</td><td>opentelemetry.io</td></tr>
<tr><td><strong>Langfuse / Phoenix</strong> <span class="pill p-oss">oss</span></td><td>LLM-specific tracing: prompt, retrieved context, output, cost, latency, per call.</td><td>langfuse.com</td></tr>
</table>
{note("<strong>The IndiaAI Mission line deserves a second look.</strong> A &#8377;10,300 crore government programme had empanelled more than 38,000 GPUs by mid-2026, with subsidised compute in the region of <strong>&#8377;67&ndash;92 per GPU-hour</strong> for eligible teams &mdash; roughly a third of the cheapest commercial Indian rate and around a tenth of a hyperscaler's Mumbai price. Eligibility and allocation are their own process with their own timelines, so it is not a drop-in answer. But a team that never checks is leaving the largest single cost lever on the table.")}
'''

code_blend = code('Python — the only two numbers that decide API versus self-host', r'''# NUMBER 1: your BLENDED rate. Comparing "input price" across providers is the
# single most common costing error. Output is routinely 5-6x input, so the
# ranking flips depending on your own input:output ratio.

def blended(in_price, out_price, in_tokens, out_tokens):
    """$ per 1M tokens at YOUR mix, not at the vendor's headline."""
    total = in_tokens + out_tokens
    return (in_price * in_tokens + out_price * out_tokens) / total

# A summarisation workload: long input, short output (90/10).
print(blended(2.00, 10.00, 90, 10))     # mid-tier  -> $2.80
print(blended(0.14,  0.28, 90, 10))     # budget    -> $0.154
# A generation workload: short input, long output (20/80). Same models.
print(blended(2.00, 10.00, 20, 80))     # mid-tier  -> $8.40   <- 3x the above
print(blended(0.14,  0.28, 20, 80))     # budget    -> $0.252

# NUMBER 2: the self-host CROSSOVER. Below it, the API wins on cost and on
# every operational dimension. Above it, self-hosting starts to pay.

def crossover(cluster_inr_per_hour, tokens_per_sec, api_usd_per_1m, usd_inr=88.0):
    """Monthly token volume at which self-hosting becomes cheaper."""
    self_inr_per_1m = cluster_inr_per_hour / (tokens_per_sec * 3600 / 1_000_000)
    api_inr_per_1m  = api_usd_per_1m * usd_inr
    if self_inr_per_1m >= api_inr_per_1m:
        return None                      # self-hosting never wins at this rate
    return {"self_inr_per_1m": round(self_inr_per_1m, 2),
            "api_inr_per_1m":  round(api_inr_per_1m, 2),
            "saving_per_1m":   round(api_inr_per_1m - self_inr_per_1m, 2)}

# One L40S at an Indian provider, serving a small open model.
print(crossover(cluster_inr_per_hour=61, tokens_per_sec=900, api_usd_per_1m=0.20))

# WHAT TO CHECK
# [ ] compute the blended rate on YOUR OWN traffic sample, not on an assumed
#     ratio. Pull a week of real prompts and count the tokens
# [ ] tokens_per_sec must come from a benchmark on YOUR model at YOUR batch
#     size and sequence length. Vendor throughput figures are peak, not typical
# [ ] the GPU is billed 24x7; your traffic is not. Divide by REAL utilisation.
#     A cluster busy 15% of the day costs ~6.7x its headline per token
# [ ] add to the self-host side: an engineer, monitoring, model upgrades,
#     capacity headroom for spikes, and a second node so a reboot is not an
#     outage. None of it is on the GPU price list
# [ ] add to the API side: egress, and the retry traffic from rate limits
# [ ] re-run this quarterly. An 80% price cut on one side moves the crossover
#     by 5x, and that has happened
''')

i_serve = f'''
<h3 id="s-indigo-tier">The market has three price tiers, and they are an order of magnitude apart</h3>
<p>As of September 2026 the shape is stable even though individual numbers are not. Budget and
open-weight models sit near <strong>$0.03&ndash;$0.45 per million input tokens</strong>. The
production tier clusters hard at <strong>$2 input</strong> &mdash; several major models landed on
exactly that figure, which is not a coincidence but the most contested price point in the market.
Frontier models run <strong>$4&ndash;$10 input</strong> and up to <strong>$50 output</strong>.</p>
{code_blend}
<p><strong>The gotcha nobody documents:</strong> benchmark parity is not price parity, and the gap is
enormous. On one widely-cited coding benchmark, five models score within <strong>0.4 percentage
points of each other</strong> &mdash; and their output prices run from <strong>$1.20 to $12 per
million tokens</strong>. A tenfold spread for a rounding error in capability. Higher up, the
best-scoring model costs roughly <strong>42 times</strong> the cheapest in that band.</p>
<p>Which means the only question worth asking is whether <em>your</em> tasks live in the gap. Build
an evaluation set of a hundred real examples from your own product, run the tiers against it, and
look at where they actually differ. For classification, extraction, routing and first-pass drafting
the answer is usually that they do not, and you should be on the cheap tier. For work where a weak
answer creates cleanup downstream, pay.</p>

<h3 id="s-indigo-self">Self-hosting in India</h3>
<p>The economics are genuinely different here, and better than most teams assume.</p>
<p>Indian GPU providers run roughly <strong>60&ndash;70% below hyperscaler Mumbai pricing</strong>.
An H100 lists around <strong>&#8377;219&ndash;362 per hour</strong> domestically against
<strong>&#8377;600&ndash;740</strong> on a hyperscaler's India-facing infrastructure. Reserved
pricing brings the effective rate toward <strong>&#8377;130&ndash;150</strong>. Spot capacity runs
as low as <strong>&#8377;70&ndash;88</strong> for interruptible work.</p>
{warn("<strong>Do not buy an H100 to run inference.</strong> It is a training card. For serving, an <strong>L40S at roughly &#8377;61&ndash;102/hour</strong> or an <strong>L4 at around &#8377;49</strong> delivers production throughput at a fraction of the cost, and the H100 premium only earns its place on models above roughly 70B parameters or where you genuinely need ultra-low latency at high concurrency. Specifying H100s for an inference workload is the most common and most expensive mis-sizing in this section.")}
<p>Buying outright is almost never right for an AI-serving workload: an H100 lands at
<strong>&#8377;27&ndash;34 lakh per unit</strong> with import duties, a server at
<strong>&#8377;2&ndash;5 crore</strong>, weeks to procure and months to deploy, against the same
compute available in sixty seconds on an hourly rate.</p>
<p>Two India-specific mechanics worth knowing: GPU cloud spend abroad sits under the Liberalised
Remittance Scheme and generally needs no RBI approval below <strong>$250,000 a year</strong>, and
IGST on foreign cloud services applies via reverse charge but is <strong>claimable as input
credit</strong> &mdash; so the headline dollar figure overstates the real cost to an Indian
business.</p>
'''

code_route = code('Python — a residency-aware model router', r'''from enum import Enum

class Residency(Enum):
    INDIA_ONLY = "india_only"     # RBI payment data. Cannot leave. Full stop.
    PERSONAL   = "personal"       # DPDP. May leave with consent + safeguards.
    OPEN       = "open"           # Product docs, policy text, public content.

# The classification is per FIELD, not per request. One request routinely
# carries fields in all three categories, and the strictest one wins.
FIELD_CLASS = {
    "txn_narration":   Residency.INDIA_ONLY,
    "beneficiary_vpa": Residency.INDIA_ONLY,
    "card_last4":      Residency.INDIA_ONLY,
    "customer_name":   Residency.PERSONAL,
    "customer_email":  Residency.PERSONAL,
    "policy_text":     Residency.OPEN,
    "product_faq":     Residency.OPEN,
}

ROUTES = {
    Residency.INDIA_ONLY: {"model": "self-hosted-in-mumbai", "egress": False},
    Residency.PERSONAL:   {"model": "vendor-with-india-region", "egress": False},
    Residency.OPEN:       {"model": "cheapest-global-api", "egress": True},
}

def route(payload: dict):
    present = [FIELD_CLASS[k] for k in payload if k in FIELD_CLASS]
    unknown = [k for k in payload if k not in FIELD_CLASS]
    if unknown:
        # An unclassified field is treated as the STRICTEST class, never the
        # loosest. New fields appear constantly and the default must be safe.
        present.append(Residency.INDIA_ONLY)
    strictest = (Residency.INDIA_ONLY if Residency.INDIA_ONLY in present
                 else Residency.PERSONAL if Residency.PERSONAL in present
                 else Residency.OPEN)
    r = dict(ROUTES[strictest])
    r.update({"residency": strictest.value, "unclassified_fields": unknown})
    return r

# WHAT TO CHECK
# [ ] the default for an UNKNOWN field is the strictest class. A field added by
#     a product team next sprint must not silently start crossing a border
# [ ] unclassified_fields is logged and alerted on. It is a backlog, not noise
# [ ] redaction happens BEFORE the call, not by asking the model to ignore
#     things. A prompt instruction is not a residency control
# [ ] the route taken is recorded with each inference, alongside the model and
#     version. "Which model saw this customer's data" must be answerable
# [ ] the in-country path is LOAD TESTED. It is the one you cannot fail over
#     away from, so it needs the headroom
# [ ] "transient" and "not used for training" do not change the analysis. If
#     payment data left India, it left India
# [ ] embeddings derived from restricted data inherit the restriction. A vector
#     is not anonymisation
''')

i_data = f'''
<h3 id="s-indigo-route">Residency as code</h3>
<p>Residency is usually written as a policy and enforced nowhere. The version that survives an
inspection is a function on the inference path.</p>
{code_route}
<p><strong>The gotcha nobody documents:</strong> embeddings. Teams treat a vector as a safe derived
artefact because it is not human-readable, and store it wherever is convenient. It is not
anonymisation &mdash; embedding inversion is a real and demonstrated technique, and the vector is
derived from the restricted data. If the source field was India-only, the embedding is too, and so is
the vector store holding it. This catches teams who carefully route their inference and then ship
their whole index to a hosted vector database in another region.</p>

<h3 id="s-indigo-vector">Vector storage: use the database you already have</h3>
<p>For almost every fintech workload, <code>pgvector</code> inside your existing Postgres is the
right answer, and the reasons are mostly not about performance.</p>
<ul>
<li><strong>One fewer system to place, secure and localise.</strong> Under a residency regime that is
a real saving, not an aesthetic one.</li>
<li><strong>Transactional consistency with the rows the vectors describe.</strong> A separate vector
store drifts from its source and nobody notices until retrieval starts returning deleted records.</li>
<li><strong>Your existing backup, access control and audit already cover it.</strong></li>
</ul>
<p>Move to a dedicated store when you have a specific measured reason: index size beyond what your
database can hold comfortably, or filtering requirements it cannot express. Not because a benchmark
on a public dataset showed a latency difference that is invisible next to your model's own response
time.</p>
'''

code_obs = code('Python — per-call accounting, because the bill arrives monthly', r'''import time, json

# The AI cost failure mode is not a big number. It is a number nobody saw
# growing. Record cost per call, at the call, with the thing that caused it.

def traced_call(client, model, messages, *, purpose, customer_id, route_info,
                prices):                       # prices: {"in": usd/1M, "out": usd/1M}
    t0 = time.perf_counter()
    resp = client.create(model=model, messages=messages)
    ms = (time.perf_counter() - t0) * 1000

    u = resp.usage
    cost = (u.input_tokens * prices["in"] + u.output_tokens * prices["out"]) / 1_000_000

    emit({
        "ts": time.time(),
        "purpose": purpose,              # "fraud_explain", "kyc_extract", ...
        "model": model,
        "model_version": resp.model,     # the RESOLVED version, not the alias
        "residency": route_info["residency"],
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
        "cached_tokens": getattr(u, "cached_input_tokens", 0),
        "usd": round(cost, 6),
        "latency_ms": round(ms, 1),
        "customer_id": customer_id,      # for per-customer unit economics
    })
    return resp

# WHAT TO CHECK
# [ ] "purpose" is mandatory and comes from a fixed enum. Cost per FEATURE is
#     the number that lets you kill an expensive feature nobody uses. Cost per
#     model tells you nothing actionable
# [ ] log the RESOLVED model version, not the alias you requested. A provider
#     moving an alias to a new version changes your quality and your bill with
#     no deploy on your side, and this field is how you find out
# [ ] track cached_tokens separately. Prompt caching can be a 10x+ discount on
#     repeated context and it is invisible unless you measure it
# [ ] alert on daily spend RATE, not monthly total. A monthly budget alert
#     fires on the 28th, which is 27 days late
# [ ] cost per customer, so unit economics are a fact rather than an estimate
# [ ] emit through OpenTelemetry, not a vendor SDK. The observability vendor is
#     a reversible decision only if you never coupled to them
# [ ] sample traces, but NEVER sample the cost counter. Sampled cost is wrong
''')

i_obs = f'''
<p>Everything above is a choice you make once. This is the part you live with.</p>
{code_obs}
<p><strong>The gotcha nobody documents:</strong> log the <em>resolved</em> model version, not the
alias you asked for. Calling a provider's stable alias is convenient and it means the model
underneath can change without a deploy on your side &mdash; different quality, different token
consumption, different bill. Teams investigate a quality regression for a week before someone thinks
to check whether the model changed. One field in your log makes that a five-minute question.</p>
{note("The observability decision is the clearest example of the reversibility rule on this page. Emit <strong>OpenTelemetry</strong> and your vendor is a configuration change. Emit a vendor's proprietary SDK from a thousand call sites and you have made a months-long migration out of a decision that should cost an afternoon. The instrumentation is the asset; the dashboard is a commodity.")}
'''

# ---------------------------------------------------------------- COST

cost_rows = [
 ("Model API &mdash; budget / open-weight", "direct",
  "&asymp; <strong>$0.03&ndash;$0.45 per 1M input</strong>, output roughly 2&ndash;4&times; that. "
  "The correct tier for classification, extraction, routing and first-pass drafting. An order of "
  "magnitude below the production tier."),
 ("Model API &mdash; production tier", "direct",
  "<strong>&asymp; $2 per 1M input</strong> is where several major models have converged &mdash; the "
  "most contested price point in the market. Output typically <strong>$10&ndash;$12</strong>. "
  "<strong>Compute your blended rate</strong>; an output-heavy workload can cost 3&times; an "
  "input-heavy one on the same model."),
 ("Model API &mdash; frontier", "direct",
  "<strong>$4&ndash;$10 input</strong>, <strong>$20&ndash;$50 output</strong> per 1M. Justified "
  "where a weak answer creates cleanup downstream, and rarely elsewhere."),
 ("GPU &mdash; Indian providers", "direct",
  "<strong>H100 &#8377;219&ndash;362/hr</strong> on demand; reserved brings the effective rate to "
  "<strong>&#8377;130&ndash;150</strong>; spot from <strong>&#8377;70&ndash;88</strong>. "
  "<strong>Roughly 60&ndash;70% below hyperscaler Mumbai pricing.</strong>"),
 ("GPU &mdash; hyperscaler Mumbai", "direct",
  "<strong>H100 &asymp; &#8377;600&ndash;740/hr</strong>. Worth it when the workload is glued to "
  "that cloud's other services and cross-cloud egress would eat the difference. Not otherwise."),
 ("GPU &mdash; the right card for inference", "direct",
  "<strong>L40S &#8377;61&ndash;102/hr</strong>, <strong>L4 &asymp; &#8377;49/hr</strong>, "
  "<strong>A30 &asymp; &#8377;126/hr</strong>. <strong>Do not serve inference on H100s</strong> "
  "unless the model is 70B+ or latency at high concurrency genuinely demands it."),
 ("GPU &mdash; IndiaAI Mission", "direct",
  "<strong>&asymp; &#8377;67&ndash;92 per GPU-hour</strong> subsidised, with 38,000+ GPUs empanelled "
  "by mid-2026 under a &#8377;10,300 crore programme. <strong>Roughly a third of the cheapest "
  "commercial Indian rate.</strong> Eligibility and allocation are their own process, but a team "
  "that never checks is leaving the largest cost lever untouched."),
 ("GPU &mdash; buying outright", "direct",
  "<strong>&#8377;27&ndash;34 lakh per H100</strong> including import duties; a full server "
  "<strong>&#8377;2&ndash;5 crore</strong>. Weeks to procure, months to deploy, years to depreciate. "
  "Almost never right for AI serving."),
 ("Fintech cloud, all in (India)", "direct",
  "Reported ranges: transaction infrastructure with redundancy <strong>&#8377;1&ndash;3 lakh/month</strong> "
  "for a small fintech, <strong>&#8377;10&ndash;30 lakh</strong> established. Fraud and risk model "
  "serving <strong>&#8377;50,000&ndash;3,00,000/month</strong>. Warehousing and analytics "
  "<strong>&#8377;80,000&ndash;5,00,000</strong>. DR and backup <strong>&#8377;30,000&ndash;1,50,000</strong>."),
 ("Data and observability stack", "oss",
  "<strong>Free.</strong> Postgres, pgvector, Kafka or Redpanda, Debezium, DuckDB, ClickHouse, "
  "OpenTelemetry, Langfuse. The cost is operations, and it is smaller than the licence you avoided."),
 ("The thing nobody budgets", "direct",
  "<strong>Egress, and retry traffic.</strong> Cross-cloud and cross-region data transfer is a real "
  "line on an inference bill, and rate-limit retries multiply request volume precisely when you are "
  "busiest. Both are invisible in a cost model built from unit prices."),
]

i_cost = f'''
{registry("Infrastructure &mdash; cost per unit", cost_rows, V)}
{warn("<strong>Divide every GPU rate by your real utilisation before comparing it to an API.</strong> The card bills 24 hours a day and your traffic does not. A cluster genuinely busy 15% of the time costs about <strong>6.7&times; its headline rate</strong> per token served. This single correction reverses most self-host business cases at small and mid volume, and it is almost never in the spreadsheet that justified the decision.")}
<p>Two more corrections worth making before anyone signs anything. Add an engineer, monitoring, model
upgrades and a second node to the self-hosted side &mdash; a single-node deployment means a reboot is
an outage. And re-run the comparison quarterly, because an 80% price cut on the API side moves the
crossover point by a factor of five, and that has already happened once this year.</p>
'''

# ---------------------------------------------------------------- AMBER

a_combos = f'''
<table>
<tr><th>Combination</th><th>Works because</th></tr>
<tr><td>Adapter in front of every model provider</td><td>Turns a months-long migration into a config change, on the decision most likely to need reversing.</td></tr>
<tr><td>Residency router &rarr; tiered models</td><td>Restricted data goes in-country; open data goes to the cheapest capable tier. You get compliance and cost, not one or the other.</td></tr>
<tr><td>pgvector inside the existing Postgres</td><td>One fewer system to localise, secure and back up, and the vectors stay consistent with the rows they describe.</td></tr>
<tr><td>OpenTelemetry everywhere</td><td>The observability vendor becomes reversible. The instrumentation is the asset.</td></tr>
<tr><td>Deterministic fallback behind every model</td><td>The AI plane can fail without the product failing. This is the design brief, not a nice-to-have.</td></tr>
<tr><td>Cost tagged by <em>purpose</em>, not by model</td><td>Lets you kill an expensive feature nobody uses. Cost per model is not actionable.</td></tr>
<tr><td>Indian GPU provider + spot for batch</td><td>60&ndash;70% below hyperscaler rates, with interruptible work at a fifth of that again.</td></tr>
</table>
<h3 id="s-amber-conflict">Combinations that conflict</h3>
<ul>
<li><strong>Payment data in a prompt to an offshore API.</strong> A cross-border transfer, regardless of transience or training assurances.</li>
<li><strong>Embeddings of restricted data in a hosted vector store abroad.</strong> A vector is not anonymisation and inherits the restriction of its source.</li>
<li><strong>H100s for inference serving.</strong> A training card doing a serving job, at three to five times the right price.</li>
<li><strong>Self-hosting at low utilisation.</strong> The GPU bills continuously; your traffic does not.</li>
<li><strong>A vendor observability SDK at a thousand call sites.</strong> An afternoon's decision turned into a quarter's migration.</li>
<li><strong>Trying to abstract the core banking platform.</strong> Nobody has done it. Choose slowly instead.</li>
<li><strong>Calling a model alias and not logging the resolved version.</strong> Your quality and your bill can change with no deploy on your side.</li>
<li><strong>Monthly budget alerts.</strong> They fire on the 28th, which is 27 days late. Alert on daily rate.</li>
</ul>
'''

a_builds = f'''
<h3 id="s-amber-exp">Strong and expensive</h3>
<p><strong>Build:</strong> commercial core banking platform &rarr; hyperscaler in an Indian region for
the operational plane &rarr; reserved GPU capacity with a domestic provider for in-country inference
&rarr; frontier API for open-data workloads &rarr; commercial observability on top of OpenTelemetry
&rarr; a platform team.</p>
<p><strong>Use when:</strong> you hold a licence with supervisory expectations, transaction volume is
large, and an outage is a regulatory conversation rather than a bad afternoon.</p>
<p><strong>Cost shape:</strong> core platform licence dominates everything else, by an order of
magnitude.</p>
<p><strong>Trade:</strong> the expensive decisions are also the slow ones. A threshold change can take
a release cycle, and the core you picked is the core you have for years.</p>

<h3 id="s-amber-def">Strong and reasonable &mdash; the default</h3>
<p><strong>Build:</strong> Postgres as the ledger, modelled carefully and append-only &rarr; a BaaS or
sponsor-bank relationship for the licence layer &rarr; Kafka or Redpanda for the operational plane
&rarr; <strong>an adapter in front of every model provider</strong> &rarr; a residency router with
an in-country path for restricted data and the cheap tier for everything else &rarr; pgvector in the
same Postgres &rarr; OpenTelemetry and Langfuse &rarr; deterministic fallbacks behind every model.</p>
<p><strong>Use when:</strong> you have engineers and you want to be able to change your mind about
the things that are cheap to change.</p>
<p><strong>Cost shape:</strong> model API spend on the cheap tier is small; the operational plane is
modest; the ledger is Postgres. The dominant cost is the team.</p>
<p><strong>Trade:</strong> you own the ledger correctness properties. That is the right trade, because
they are also the thing you can never outsource responsibility for.</p>
{note("Why the adapter is in the default build rather than the expensive one. Model pricing moved by 80% in a single day during 2026, and a scheduled increase on another model was cancelled weeks before it was due. An abstraction layer over a model API costs about a day to write and is the highest-return piece of code on this page. Nobody regrets it; plenty of teams regret its absence when a price moves and they cannot act for a quarter.")}

<h3 id="s-amber-lean">Strong and lean</h3>
<p><strong>Build:</strong> one Postgres &rarr; one budget-tier model API behind an adapter &rarr; a
single residency rule that keeps payment data out of prompts entirely &rarr; pgvector &rarr;
structured logs with cost per call &rarr; rules-only fallback.</p>
<p><strong>Use when:</strong> pre-launch or early, and every hour on infrastructure is an hour not on
the product.</p>
<p><strong>Cost shape:</strong> tens of dollars a month for inference, plus a small database.</p>
<p><strong>Trade:</strong> no redundancy and manual scaling. Acceptable. <strong>What is not
acceptable at any size is the ledger shortcut</strong> &mdash; floats for money, mutable rows, a
single timestamp. Those cost nothing on day one and are effectively unfixable once a year of data
sits on top of them.</p>
{warn("Whichever grade you pick, write the <strong>architecture decision record</strong> as you go and keep it short: what we chose, what we rejected, why, and what would make us revisit. Six months later nobody remembers the constraint that made an odd choice sensible, and the record is the difference between a considered decision and an inherited mystery. It is also the first artefact a supervisor asks for.")}
'''

a_next = f'''
<p>One number to watch that is not on any dashboard by default: <strong>the share of AI calls that
fell back to rules</strong>, and the trend. Zero means the fallback has never been exercised and you
do not know whether it works. A rising line means something upstream is degrading and nobody has
noticed. It is the single most informative metric about the AI plane, and almost nobody plots it.</p>
<h3 id="s-amber-next">What this feeds</h3>
<div class="mod-grid">
<a href="/fintech-ai/governance/" class="mod-card"><div class="mod-num">MODULE 09</div><h3>Governance</h3><p>Model change control, the evidence pack, and who signed off on the threshold. The next build sheet.</p></a>
<a href="/fintech-ai/customer-operations/build-sheet/" class="mod-card"><div class="mod-num">SHEET 06</div><h3>Customer Operations</h3><p>Where the model tiers get chosen in anger, and where per-resolution cost meets per-token cost.</p></a>
<a href="/fintech-ai/payments-reconciliation/build-sheet/" class="mod-card"><div class="mod-num">SHEET 05</div><h3>Payments &amp; Reconciliation</h3><p>The ledger correctness properties, and why the two clocks belong in the data model.</p></a>
<a href="/fintech-ai/regulation-india/" class="mod-card"><div class="mod-num">REFERENCE</div><h3>India regulation</h3><p>Payment data localisation and the DPDP Act, in more detail than this page allows.</p></a>
</div>
{warn("Everything on this page is illustrative. Data localisation, outsourcing and cloud adoption by regulated entities carry specific obligations under RBI direction, and getting residency wrong is a supervisory matter rather than a technical one. Nothing here is legal advice. Have your data-flow map and your cloud arrangements reviewed by qualified counsel before production traffic touches them.")}
'''

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to read this build sheet", g_read),
   ("Optimise for reversibility first", g_rev),
   ("Where your data is allowed to be", g_res),
 ],
 'indigo': [
   ("Raw materials — serving, compute and data", i_mat_serve),
   ("How to use each one — model serving", i_serve),
   ("How to use each one — residency and vectors", i_data),
   ("How to use each one — observability and cost", i_obs),
   ("Cost per unit", i_cost),
 ],
 'amber': [
   ("Best combinations", a_combos),
   ("Three recommended builds", a_builds),
   ("What next", a_next),
 ],
}

TITLE = "Infrastructure Build Sheet"
META  = ("Every serving, compute and data component for fintech AI: how to use each one, what it "
         "costs per unit, and three recommended builds.")
LEAD  = ("Every serving, compute, storage and observability component a fintech AI stack needs. What "
         "each one is for, the first working call, the gotcha nobody documents, real costs in INR and "
         "USD, and three recommended builds.")

print(f"title len: {len(TITLE + ' | Clarigital')}")
print(f"meta len : {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/infrastructure/build-sheet",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Build Sheet 08",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI"),
            ("/fintech-ai/infrastructure/", "Infrastructure")],
  lanes  = lanes,
)
