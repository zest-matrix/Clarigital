#!/usr/bin/env python3
# Session 47 — Build Sheet 04: AML & Compliance
# /fintech-ai/aml-compliance/build-sheet/
import sys
sys.path.insert(0, '/tmp')
exec(open('/tmp/fintech_builder.py').read())

V = VERIFIED   # 'September 2026'

# ---------------------------------------------------------------- GREEN

g_read = f'''
<p>The <a href="/fintech-ai/aml-compliance/">AML and Compliance module</a> explains how screening
and monitoring work. This page is the parts list and the assembly instructions: every list, every
engine, what each one costs, and what breaks.</p>
<p>Vendor and government links are here so you can verify what we say. Everything you need to
build is on this page.</p>
{warn(f"Pricing and list mechanics carry a <strong>Verified {V}</strong> stamp and sit in marked blocks. Screening vendors are mostly sales-led and change their packaging often. Treat the tiers here as budgeting anchors and as a way to recognise when a quote is out of shape.")}
<p>One thing to settle before anything else. AML is not one system. It is four, and they fail in
different ways, get bought from different vendors and are examined separately.</p>
<table>
<tr><th>Job</th><th>What it does</th><th>Can you skip it?</th></tr>
<tr><td><strong>Sanctions screening</strong></td><td>Name-matches customers and payment parties against designated lists.</td><td>No. It is strict liability in most regimes and non-discretionary in India.</td></tr>
<tr><td><strong>PEP and adverse media</strong></td><td>Flags political exposure and negative news for enhanced due diligence.</td><td>Risk-based, but a PEP hit is often how a missed sanctions match gets caught.</td></tr>
<tr><td><strong>Transaction monitoring</strong></td><td>Watches behaviour over time for laundering typologies.</td><td>No, if you are a reporting entity. It is what produces your STRs.</td></tr>
<tr><td><strong>Regulatory reporting</strong></td><td>Files CTR, STR and the rest on the regulator's portal, to deadline.</td><td>No. Late filing is itself the violation, counted per day.</td></tr>
</table>
<p>Buying one and assuming you have the others is the most expensive mistake on this page. A
screening API does not monitor transactions. A monitoring platform does not file your reports.</p>
'''

g_lists = f'''
<p>Most teams screen against every list they can find and assume more is safer. It is worth being
precise about which lists carry legal force where, because the answer changes what you must do
when one hits.</p>
<table>
<tr><th>List</th><th>Legal force for an Indian reporting entity</th></tr>
<tr><td><strong>UNSC consolidated lists</strong> (1267, 1988, 1718 and successors)</td><td><strong>Binding.</strong> Implemented through Section 51A of the UAPA, 1967 and circulated by MEA &rarr; regulators &rarr; you.</td></tr>
<tr><td><strong>UAPA Schedules 1 and 4</strong></td><td><strong>Binding.</strong> India's own domestic designations of banned organisations and individuals, maintained by the Ministry of Home Affairs. Separate from the UN lists.</td></tr>
<tr><td><strong>WMD Act 2005, Section 12A list</strong></td><td><strong>Binding.</strong> Proliferation financing. Procedure set by the Ministry of Finance Order of 30 January 2023.</td></tr>
<tr><td>OFAC SDN and Consolidated</td><td>Not binding under Indian law. Binds you through correspondent banking, USD clearing and counterparty contract.</td></tr>
<tr><td>EU Consolidated, UK OFSI Consolidated</td><td>Same. Contractual and correspondent exposure, not Indian statute.</td></tr>
</table>
{note("This is not an argument for screening less. Screen OFAC, EU and UK too &mdash; your sponsor bank and your correspondents will require it, and USD exposure is nearly universal. The point is that the <em>consequence</em> of a hit differs. A UNSC or UAPA match triggers a statutory process with clocks on it. An OFAC match triggers a commercial and correspondent-risk process. Systems that treat every list identically get the Indian process wrong, because the Indian process is not yours to run.")}
<p>That last sentence is the structural fact for this module. <strong>In India the freeze is a legal
order issued by the Ministry of Home Affairs, not a decision your product makes.</strong> Your
obligation is to detect, report inside 24 hours, restrict when the match is beyond doubt, and then
act on the order when it arrives. Build for that shape, with an unfreeze path, and you will be
right. Build a big red "freeze account" button and you will be wrong in both directions.</p>
'''

g_case = f'''
<p>On 10 November 2025 the UK's Office of Financial Sanctions Implementation fined Bank of Scotland
&pound;160,000. The penalty notice was published on 26 January 2026 and it is worth reading in full,
because it is the clearest public account of how a correctly configured screening system fails.</p>
<p>A British citizen, designated by the UK on 31 December 2020, opened an account at Halifax on
6 February 2023 using a UK passport. The name on the passport differed from the OFSI Consolidated
List entry by a changed character and an added character in the forename, a missing middle name,
and a changed character in the surname. OFSI notes these are common Russian-to-English
transliteration equivalents. No sanctions alert fired, at opening or at any point afterwards.</p>
<p>OFSI identified two causes, and said resolving <strong>either one</strong> would likely have
prevented the breach: the screening system could not reconcile the character changes, and the
sanctions list had not been enhanced, by a commercial provider or by the bank itself. The bank
<em>had</em> enhanced its PEP list commercially &mdash; and the PEP screen alerted on the same name
variation the next day.</p>
{warn("The part most summaries leave out is the more useful part. A PEP review began on 20 February. A manual adverse media check correctly identified the customer as a designated person. Through human error the reviewer recorded them as delisted from both the UK and EU lists, when only the EU listing had gone. There was no explicit instruction to escalate a potential sanctions connection to a sanctions team. The account stayed open four more days &mdash; and <strong>&pound;75,000 of the &pound;76,000 credited to it arrived in that window</strong>, after a human being had already found the right answer.")}
<p>Two lessons, in order of how much they will cost you. Enrich your sanctions list to at least the
standard you enrich your PEP list, because the difference between those two programmes is the
finding. And treat every path that can discover a designation &mdash; PEP review, adverse media,
complaint handling, an analyst's hunch &mdash; as a sanctions escalation route with a named
destination. The detection system is only half the control.</p>
<p>For completeness: the breach value was &pound;77,383.39 across 24 payments, the statutory maximum
was &pound;1,000,000, the pre-discount penalty was &pound;320,000, and a full 50% voluntary
disclosure discount brought it to &pound;160,000. There were eight aggravating factors, not one.
The list-enrichment decision was the headline, not the whole case.</p>
'''

# ---------------------------------------------------------------- INDIGO

i_mat_data = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>OFAC Sanctions List Service (SLS)</strong></td><td>Official US Treasury distribution of the SDN and Consolidated lists. Free, no key. A file service, not a screening API.</td><td>ofac.treasury.gov/sanctions-list-service</td></tr>
<tr><td><strong>UN Security Council consolidated list</strong></td><td>The 1267/1988 and related designations, published as XML. The list India implements.</td><td>un.org/securitycouncil/sanctions</td></tr>
<tr><td><strong>EU Consolidated Financial Sanctions List</strong></td><td>EU restrictive measures, free XML/CSV download.</td><td>data.europa.eu</td></tr>
<tr><td><strong>UK OFSI Consolidated List</strong></td><td>UK designations. The list in the Bank of Scotland case.</td><td>gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets</td></tr>
<tr><td><strong>MHA UAPA Schedules + nodal officers</strong></td><td>India's domestic terrorist designations, and the list of officers you must contact on a match.</td><td>mha.gov.in</td></tr>
<tr><td><strong>OpenSanctions</strong></td><td>Aggregated open dataset of sanctions, PEPs and related entities, plus a hosted match API and a self-hostable server (<code>yente</code>).</td><td>opensanctions.org</td></tr>
<tr><td><strong>Dow Jones R&amp;C / LSEG World-Check / Moody's Grid</strong></td><td>Commercial enriched lists: aliases, transliteration variants, DOB ranges, relationships. This layer is what the Bank of Scotland case turned on.</td><td>vendor sales &mdash; no public rate card</td></tr>
</table>
{note("Coverage claims are the least useful vendor metric here. Every provider covers OFAC, UN, EU and UK, because those are free and public. What you are actually buying from a commercial provider is <strong>alias density and identifier enrichment on the same entities</strong> &mdash; how many spellings of one name it knows. Ask for that, on your own risk population, in a trial.")}
'''

i_mat_eng = f'''
<table>
<tr><th>Material</th><th>What it does</th><th>Verify at</th></tr>
<tr><td><strong>ComplyAdvantage</strong></td><td>Screening and monitoring API with proprietary risk data. Published entry tier, which is rare in this market.</td><td>complyadvantage.com</td></tr>
<tr><td><strong>sanctions.io / AMLWatcher / MemberCheck / Sanction Scanner</strong></td><td>API-first screening services. Faster to integrate than enterprise suites, priced on published calculators or entity tiers.</td><td>sanctions.io</td></tr>
<tr><td><strong>NICE Actimize / Oracle FCCM / SAS AML</strong></td><td>Bank-scale suites: screening, monitoring, case management, model governance. Enterprise licensing.</td><td>niceactimize.com</td></tr>
<tr><td><strong>Napier AI / Silent Eight / Facctum</strong></td><td>Screening and alert adjudication focused on false-positive reduction and explainable scenario governance.</td><td>napier.ai</td></tr>
<tr><td><strong>TrackWizz / Signzy / IDfy / Clari5</strong></td><td>Indian providers. TrackWizz and Clari5 in particular ship the UAPA/FIU workflow rather than making you build it.</td><td>trackwizz.com</td></tr>
<tr><td><strong>Marble</strong> <span class="pill p-oss">oss</span></td><td>Real-time rule engine and case manager for monitoring and screening. Elastic Licence V2 &mdash; read the section below before you plan on it.</td><td>github.com/checkmarble/marble</td></tr>
<tr><td><strong>Tazama</strong> <span class="pill p-oss">oss</span></td><td>Linux Foundation project for real-time monitoring on ISO 20022 messages. Built for payment-switch scale.</td><td>github.com/tazama-lf</td></tr>
<tr><td><strong>Jube</strong> <span class="pill p-oss">oss</span></td><td>Real-time monitoring with ML scoring and case management. AGPLv3.</td><td>jube.io</td></tr>
<tr><td><strong>yente</strong> <span class="pill p-oss">oss</span></td><td>OpenSanctions' own match server. Free software; the data needs a licence.</td><td>github.com/opensanctions/yente</td></tr>
<tr><td><strong>RapidFuzz / jellyfish / Double Metaphone</strong> <span class="pill p-oss">oss</span></td><td>String distance and phonetic algorithms. Double Metaphone handles transliteration best of the classic options.</td><td>github.com/rapidfuzz</td></tr>
</table>
'''

code_ofac = code('Python — OFAC SLS ingest, the four-file join', r'''import csv, io, requests

BASE = "https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports"

# SLS rejects requests with no User-Agent. This is not in the docs; you get a 403
# with no body and it looks like an outage.
H = {"User-Agent": "yourcompany-aml-ingest/1.0 (compliance@yourcompany.com)"}

def grab(name):
    r = requests.get(f"{BASE}/{name}", headers=H, timeout=120)
    r.raise_for_status()
    return list(csv.reader(io.StringIO(r.text)))

# THE FOUR FILES. SDN.CSV alone is primary names only.
sdn      = grab("SDN.CSV")           # ent_num, name, type, programme, ... remarks
alt      = grab("ALT.CSV")           # ent_num -> aliases  <- transliteration variants live HERE
add      = grab("ADD.CSV")           # ent_num -> addresses
comments = grab("SDN_COMMENTS.CSV")  # remarks past the 1000-char cap: passport + tax IDs

NULL = "-0-"                          # OFAC's null sentinel, not an empty string

names = {}                            # ent_num -> {primary, aliases[]}
for row in sdn:
    names[row[0]] = {"primary": row[1], "aliases": []}
for row in alt:
    if row[0] in names:
        names[row[0]]["aliases"].append(row[3])

# WHAT TO CHECK before you screen a single customer against this
# [ ] alias count > 0 for a meaningful share of entries. If every entry has zero
#     aliases you have loaded SDN.CSV only and you are screening primary names.
#     That is structurally the Bank of Scotland failure.
# [ ] "-0-" normalised to empty everywhere. It is a literal string in the file.
# [ ] SDN_COMMENTS joined. Passport and national ID numbers routinely spill past
#     the 1000-char remarks cap and land in this file. Those identifiers are what
#     let you clear a false positive.
# [ ] row counts logged per file per run, with an alert on a drop of >5%. A
#     truncated download produces a smaller list and zero errors.
# [ ] list version hash stored WITH every screening decision. "Which list did you
#     screen against on that date" is the first question an examiner asks.
# [ ] filenames discovered from GET /sanctions-lists, not hardcoded. OFAC changes
#     them without notice.
# [ ] a scheduled job, not a deploy-time job. SLS has no webhooks and no SLA.
''')

i_free = f'''
<p>The official feeds are free, authoritative and the only acceptable source for the lists
themselves. Scraping a sanctions website instead of taking the published feed breaches terms and
fails audit expectations. What they do not give you is any matching logic at all.</p>
<h3 id="s-indigo-ofac">OFAC Sanctions List Service</h3>
<p>Free, no authentication, no published rate limits, and not a screening API. It delivers files.
Parsing, normalising, indexing, matching and staying current are all yours.</p>
{code_ofac}
<p><strong>The gotcha nobody documents:</strong> the legacy flat-file series is four files, not one.
<code>SDN.CSV</code> holds primary names. The aliases &mdash; every transliteration variant, every
a.k.a. &mdash; are in <code>ALT.CSV</code>, joined on <code>ent_num</code>. OFAC's own tutorial warns
that downloading one file means missing large amounts of list data, and it is the single most common
DIY ingestion error. If you would rather not maintain the join, take the Advanced XML instead: it
carries aliases, multiple identifiers and original-script names in one document.</p>
<p>Useful SLS endpoints beyond the file downloads: <code>/sanctions-lists</code> and
<code>/sanctions-programs</code> return the available names as JSON, <code>/changes/latest</code>
gives a delta rather than a full refresh, <code>/changes/history/{{year}}/{{month}}/{{day}}</code>
backfills a missed day, and <code>/alive</code> is a health check worth monitoring.</p>
'''

code_os = code('Python — OpenSanctions /match, first working call', r'''import requests

API = "https://api.opensanctions.org/match/default"

# Send the whole entity, never just a name string. DOB, nationality and any
# identifier are what let the scorer separate two people with one name.
payload = {"queries": {
    "q1": {"schema": "Person", "properties": {
        "name":        ["Rajesh Kumar Sharma"],
        "birthDate":   ["1979-04-11"],
        "nationality": ["in"],
    }},
}}

r = requests.post(API, json=payload,
                  headers={"Authorization": "ApiKey YOUR_KEY"},
                  params={"algorithm": "best"}, timeout=30)
r.raise_for_status()

for res in r.json()["responses"]["q1"]["results"]:
    print(res["score"], res["match"], res["caption"], res["datasets"])

# WHAT TO CHECK
# [ ] "score" is a similarity, "match" is a boolean the API derives from its own
#     threshold. Decide your own threshold; do not inherit theirs silently.
# [ ] datasets[] tells you WHICH list hit. A UNSC hit and an OFAC hit are
#     different legal events in India. Branch on it.
# [ ] absent DOB on the LIST side must not reduce the score. Sanctions entries
#     routinely have no DOB. Treating absence as disconfirmation discards real
#     matches. Verify this against a known thin entry before you go live.
# [ ] billing: /match counts LOGICAL QUERIES, not HTTP requests. Batching 10
#     entities into one call costs 10 queries. Only HTTP 200 is billed.
# [ ] store the full response body, the algorithm name and the dataset version
#     against the decision. The response IS your audit evidence.
# [ ] re-screen on list change, not only at onboarding. A customer clean on
#     Monday can be designated on Tuesday.
''')

i_enriched = f'''
<h3 id="s-indigo-os">OpenSanctions, hosted and self-hosted</h3>
<p>The most useful starting point in the market, and the one with the licensing trap.</p>
{code_os}
{warn("<strong>The licence is the thing to get right.</strong> The dataset is published under CC BY-NC 4.0 &mdash; free for non-commercial use. A fintech screening its own customers is commercial use. You need a licence: an internal licence (priced differently for financial services and everyone else) or a reseller licence if the data reaches your customers. The <code>yente</code> server software is genuinely free and open source; the <em>data</em> is what you are licensing. Teams read \"open source\" on the repo, build on it for a quarter, and discover the commercial terms during a diligence review. This is the same shape as the Surya licensing trap in the identity module.")}
<p>On hosted versus self-hosted: the hosted API is metered at roughly &euro;0.10 per successful call
with volume pricing above about 20,000 calls a month. Self-hosting <code>yente</code> converts that
into a flat data-licence cost and is the ceiling on what OpenSanctions can cost you. But the licence
is the price of the house, not the cost of living in it &mdash; <code>yente</code> needs an
Elasticsearch or OpenSearch cluster, memory, fast storage and somebody to upgrade it. Budget the
operations, not just the licence.</p>

<h3 id="s-indigo-comm">Commercial enriched lists</h3>
<p>Dow Jones, LSEG World-Check and Moody's Grid are quote-only, enterprise-sales, no sandbox. You
will not price them from a web page. What you are buying is alias density, identifier enrichment,
relationship data and a defensible answer to the OFSI question: did you enhance your list using
commercially available information, or not?</p>
<p>Two things to insist on in a trial. First, run <em>your own</em> customer file against it, not
their demo set &mdash; a provider strong on Russian and Iranian transliteration may be thin on
Indian and Gulf name forms, which is where your volume is. Second, ask for the same entity in both
the free UN feed and their enriched record, side by side. The delta is the product. If the delta is
small for your population, the free feed plus good matching is a legitimate answer, and you should
document that you tested it.</p>

<h3 id="s-indigo-llm">Where an LLM belongs in the cascade</h3>
<p>The evidence is strong and specific. Federal Reserve research (Allen and Hatfield, FEDS 2025-092)
compared four families of large language models against standard fuzzy algorithms on sanctions name
and address matching. Across realistic thresholds the models cut false positives by about 92% and
raised detection by about 11% against the best fuzzy baseline.</p>
<p>The same paper contains the number that decides your architecture: <strong>the models were on
average more than four orders of magnitude slower than the fuzzy methods.</strong> Roughly ten
thousand times. The authors' own recommendation is a cascade &mdash; exact and fuzzy matching handle
the easy cases, and only genuinely uncertain cases escalate to a model. Their cascade ran about twice
as fast as the pure LLM system with comparable accuracy.</p>
{note("The paper also splits by process, which is the practical guidance. High-velocity payment screening cannot afford model latency in the path and needs the tiered approach. Slower processes &mdash; customer due diligence at account opening, lending decisions &mdash; can lean on models much more heavily. Our position is unchanged on the audit point: <strong>keep alert generation deterministic.</strong> A deterministic layer raises the alert, so you can always answer \"why did this fire\" with a rule and a threshold. The model works on alerts that already exist &mdash; triage, adverse media summarisation, rationale drafting. That keeps the speed and the false-positive gain without making the alert itself non-reproducible.")}
'''

code_tm = code('SQL — structuring detection, the first rule worth writing', r'''-- Structuring: breaking cash or transfers into pieces that each sit below a
-- reporting threshold. In India the threshold that matters is the CTR one:
-- cash above Rs 10 lakh AGGREGATED OVER A CALENDAR MONTH, including
-- transactions that appear connected.

WITH monthly AS (
  SELECT customer_id,
         date_trunc('month', txn_at AT TIME ZONE 'Asia/Kolkata') AS month,
         SUM(amount_paise)                       AS total_paise,
         COUNT(*)                                AS txn_count,
         MAX(amount_paise)                       AS largest_paise,
         COUNT(*) FILTER (WHERE amount_paise BETWEEN 800000*100 AND 1000000*100)
                                                 AS near_threshold_count
  FROM transactions
  WHERE channel = 'CASH'
    AND txn_at >= now() - interval '3 months'
  GROUP BY 1, 2
)
SELECT customer_id, month, total_paise/100 AS total_rupees, txn_count,
       near_threshold_count,
       CASE
         WHEN total_paise > 1000000*100 THEN 'CTR_REPORTABLE'
         WHEN total_paise > 900000*100 AND largest_paise < 1000000*100
              THEN 'STRUCTURING_SUSPECTED'   -- just under, never once over
         WHEN near_threshold_count >= 3 THEN 'REPEATED_NEAR_THRESHOLD'
       END AS disposition
FROM monthly
WHERE total_paise > 900000*100 OR near_threshold_count >= 3
ORDER BY total_paise DESC;

-- WHAT TO CHECK
-- [ ] money in integer paise, never floats. A rounding error either side of a
--     statutory threshold is a filing error.
-- [ ] the month boundary is IST. Aggregating in UTC shifts roughly five and a
--     half hours of transactions into the wrong reporting month, every month.
-- [ ] CTR is an aggregate over the calendar month, not a per-transaction test.
--     Teams write "amount > 10 lakh" and under-report for years without any
--     error surfacing.
-- [ ] "connected transactions" across related accounts are included. One
--     customer, several accounts, same beneficial owner.
-- [ ] CTR_REPORTABLE is a FILING duty, not suspicion. Do not route it to the
--     STR queue. They are different reports with different deadlines.
-- [ ] the rule version and thresholds are stored with each alert, so the
--     question "what was this tuned to in March" has an answer.
-- [ ] back-test on twelve months of history before enabling. A new scenario
--     that fires on 4% of your base is a hiring plan, not an alert.
''')

i_monitor = f'''
<p>Screening asks "is this person on a list". Monitoring asks "does this behaviour look like
laundering". They share a queue and almost nothing else. Monitoring is what actually produces your
STRs, and it is the layer teams under-build because a screening API feels like it covered AML.</p>
<h3 id="s-indigo-scen">Start with named scenarios, not a score</h3>
<p>The fastest defensible start is four or five written typologies, each with a name, a rationale and
a threshold you can point at. Structuring, rapid pass-through, dormant-then-active, round-tripping
between related parties, and activity inconsistent with the declared profile will cover most of what
a small book produces. A model can come later; a model cannot be explained to an examiner in a
sentence, and a named scenario can.</p>
{code_tm}
<p><strong>The gotcha nobody documents:</strong> the calendar-month aggregation in the CTR rule.
CTR is not a per-transaction threshold. It is cash above &#8377;10 lakh <em>summed across the
month</em>, including connected transactions. A rule written as a single-transaction test will run
cleanly for years, throw no errors, and silently under-file the entire time &mdash; and under PMLA
each missed filing is a separate failure.</p>

<h3 id="s-indigo-tmtools">Choosing the engine</h3>
<table>
<tr><th>Option</th><th>Shape</th><th>Licence</th></tr>
<tr><td><strong>Marble</strong></td><td>Rule builder, real-time and batch decisioning, case manager. Go backend, Postgres + Redis + Elasticsearch. Closest open-source thing to a commercial product.</td><td><strong>Elastic Licence V2.</strong> Read it first.</td></tr>
<tr><td><strong>Tazama</strong></td><td>Linux Foundation project, ISO 20022 message oriented, designed for national payment switch volumes.</td><td>Apache-2.0</td></tr>
<tr><td><strong>Jube</strong></td><td>Real-time monitoring with supervised and unsupervised ML scoring, workflow case management.</td><td><strong>AGPLv3.</strong> Network copyleft.</td></tr>
<tr><td><strong>Your own rules on your own warehouse</strong></td><td>SQL scenarios on a scheduler, alerts into a table, a simple review UI.</td><td>Yours</td></tr>
<tr><td><strong>Commercial</strong></td><td>ComplyAdvantage, Napier AI, Facctum, Unit21 at the modern end; Actimize, Oracle, SAS at bank scale.</td><td>Licensed</td></tr>
</table>
{warn("Two licence traps worth naming before you prototype. <strong>Marble is Elastic Licence V2</strong>, which prohibits providing the software to third parties as a hosted or managed service &mdash; if you are a BaaS provider, a PSP or a platform offering monitoring to your own clients, that is the prohibited case exactly, not a grey area. <strong>Jube is AGPLv3</strong>, so offering it over a network triggers the source-disclosure obligation for your modifications. Both are fine for monitoring your own book. Neither is fine inside a product you sell. This is the same shape as the Surya licensing trap in the identity module, and it is found during diligence far more often than during evaluation.")}
<p>One deployment detail on Marble that is easy to miss: the open-source build runs against the
Firebase auth emulator locally, but production requires a real Firebase auth app. That is an external
dependency with its own data-residency question, arriving in the middle of an otherwise self-hosted
stack. Check it against your localisation position before you commit.</p>
'''

code_india = code('Python — the India designated-list workflow, with its clocks', r'''from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))

# In India the freeze is an ORDER from MHA. Your system detects, reports and
# restricts. It does not freeze on its own authority.
BINDING = {"UNSC", "UAPA_SCHEDULE_1", "UAPA_SCHEDULE_4", "WMD_12A"}

def on_designated_hit(hit, customer):
    now = datetime.now(IST)
    ev = {
        "customer_id":   customer["id"],
        "list":          hit["list"],
        "list_version":  hit["list_version"],
        "matched_on":    hit["matched_fields"],
        "score":         hit["score"],
        "detected_at":   now.isoformat(),
        # The 24-hour clock starts at identification, not at review completion.
        "report_due_at": (now + timedelta(hours=24)).isoformat(),
        "recipients": [
            "Joint Secretary (IS-I), Ministry of Home Affairs",
            f"UAPA Nodal Officer, {customer['state']}",   # state where the account is held
            "UAPA Nodal Officer, RBI",
            "FIU-IND",
        ],
        # Beyond doubt => prevent transactions now, under intimation.
        # Possible match => restrict pending verification, do not close.
        "action": "PREVENT_TRANSACTIONS" if hit["beyond_doubt"] else "RESTRICT_PENDING",
        "str_required": True,          # file the STR as well; it is a separate duty
        "customer_visible": False,     # tipping off is an offence
    }
    if hit["list"] not in BINDING:
        # OFAC / EU / UK: real exposure, different process. Correspondent and
        # contractual risk, not the UAPA statutory route.
        ev["recipients"] = ["Internal sanctions committee", "Sponsor bank"]
        ev["action"] = "REVIEW"
    return ev

# WHAT TO CHECK
# [ ] detected_at is the moment of identification by ANY route -- automated
#     screen, PEP review, adverse media, an analyst noticing. All of them start
#     the same clock. This was the Bank of Scotland gap.
# [ ] the state/UT nodal officer is derived from where the ACCOUNT is held, not
#     from the customer's correspondence address.
# [ ] an unfreeze path exists and is tested. If MHA cannot pass an unfreezing
#     order within fifteen working days it must inform the applicant -- so the
#     customer will be asking you for status while you have nothing to tell them.
# [ ] delisting requests from customers are forwarded to Joint Secretary (CTCR),
#     MHA. Not to RBI, not to your sponsor bank, not answered by support.
# [ ] no field in this record is ever rendered in a customer-facing surface, an
#     email template, a support console, or an app notification.
# [ ] DELISTINGS are processed too. A stale list wrongly freezes a cleared
#     person, which is its own regulatory and conduct problem.
''')

i_india = f'''
<p>This is the part of AML that no international vendor ships correctly out of the box, and the part
examiners in India look at first.</p>
<h3 id="s-indigo-uapa">Section 51A: the mechanics</h3>
<p>The procedure sits in the UAPA Order dated 2 February 2021, amended 22 April 2024, carried into
the RBI Master Direction on KYC. The WMD Act route is the Ministry of Finance Order of
30 January 2023. In outline:</p>
<ol>
<li>MEA updates the designated lists and pushes them to the regulators, FIU-IND and MHA. The
regulators push them to you.</li>
<li>You verify your customer base against the lists on a regular basis. Daily verification is the
expectation, not a nice-to-have.</li>
<li>On a match, <strong>within 24 hours</strong> you inform the Joint Secretary (IS-I) at MHA, the
UAPA nodal officer of the state or UT where the account is held, your regulator's UAPA nodal
officer, and FIU-IND.</li>
<li>Where the match is beyond doubt, you prevent the person from transacting, under intimation.</li>
<li>MHA causes verification through the state police or central agencies. If it confirms, a Section
51A order issues <strong>within 24 hours of that verification</strong>, without prior notice to the
customer.</li>
<li>You file an STR as well. The sanctions report does not discharge the PMLA duty.</li>
</ol>
{code_india}
<p><strong>The gotcha nobody documents:</strong> the current list of UAPA nodal officers lives on the
MHA website and changes. Teams hardcode a contact at build time and discover on the one day it
matters that the address is three officers out of date. Treat the nodal-officer list as reference
data with an owner and a refresh cadence, exactly like the sanctions list itself.</p>

<h3 id="s-indigo-fiu">FIU-IND reporting</h3>
<p>Registration and filing both run on FINGate 2.0, the successor interface to the earlier FINnet
system. Five reports:</p>
<table>
<tr><th>Report</th><th>Trigger</th><th>Deadline</th></tr>
<tr><td><strong>CTR</strong></td><td>Cash transactions above &#8377;10 lakh in a calendar month, including connected transactions.</td><td>By the 15th of the following month</td></tr>
<tr><td><strong>STR</strong></td><td>Suspicion. No monetary threshold. Includes <em>attempted</em> transactions.</td><td>Within 7 working days of forming suspicion</td></tr>
<tr><td><strong>CBWTR</strong></td><td>Cross-border wire transfers above &#8377;5 lakh.</td><td>Monthly, per the prescribed schedule</td></tr>
<tr><td><strong>CCR</strong></td><td>Counterfeit currency identified.</td><td>Per the prescribed schedule</td></tr>
<tr><td><strong>NTR</strong></td><td>Non-profit organisation receipts above the prescribed threshold.</td><td>Monthly</td></tr>
</table>
<p>Records retained five years. Principal Officer and Designated Director must be two different
people &mdash; mapping both roles to one individual is a common and entirely avoidable finding.</p>
{warn("<strong>The STR clock starts at &ldquo;forming suspicion&rdquo;, and that timestamp is a design decision.</strong> If your case management system records only the filing date, you have no defensible answer when an examiner asks when suspicion was formed. Stamp it explicitly &mdash; the moment an analyst dispositions an alert as suspicious &mdash; make it immutable, and drive the seven-working-day countdown off that field. Under PMLA, delay can be counted as a separate violation for each day late.")}
'''

# ---------------------------------------------------------------- COST

cost_rows = [
 ("Official government feeds", "direct",
  "<strong>Free.</strong> OFAC SLS, UN, EU, UK OFSI, MHA. No key, no rate limit, no SLA, no support. "
  "The cost is the ingestion pipeline: budget real engineering time for parsing, normalising, "
  "monitoring for silent truncation and handling format changes made without notice."),
 ("OpenSanctions &mdash; hosted API", "direct",
  "&asymp; <strong>&euro;0.10 per successful call</strong>, volume pricing above ~20,000 calls/month. "
  "Only HTTP 200 billed. A batch of 10 entities counts as 10 queries."),
 ("OpenSanctions &mdash; bulk data licence", "direct",
  "Quoted per use case. Internal licence for financial services, internal for other sectors, "
  "reseller if the data reaches your customers. Flat, not metered &mdash; the ceiling on your "
  "OpenSanctions spend. Add Elasticsearch and operations on top."),
 ("Screening API &mdash; entry tier", "direct",
  "&asymp; <strong>$99&ndash;$120/month</strong>. ComplyAdvantage publishes a starter plan around "
  "$99.99/month; the included entity allowance is quoted differently across sources and has changed, "
  "so <strong>confirm the allowance</strong> &mdash; that is the number that decides the price."),
 ("Screening API &mdash; mid tier", "direct",
  "&asymp; <strong>&euro;990/month</strong> for around 100 entities/month is a reported Sanction "
  "Scanner entry point. Sandbar publishes from about $500/month including OpenSanctions data. "
  "sanctions.io prices from a calculator on contract term and volume, with a 30-day trial."),
 ("Full AML platform &mdash; mid-market", "direct",
  "&asymp; <strong>$30,000&ndash;$100,000/year</strong> for screening plus monitoring plus case "
  "management."),
 ("Enterprise suites", "direct",
  "&asymp; <strong>$100,000&ndash;$800,000+/year</strong> plus implementation. NICE Actimize, Oracle "
  "FCCM, SAS. Annual licence largely independent of volume &mdash; high floor, low unit cost at scale."),
 ("Commercial enriched list data", "direct",
  "Quote-only. Dow Jones, LSEG World-Check, Moody's Grid. No public rate card, no self-serve "
  "sandbox. Expect enterprise sales and an annual commitment."),
 ("Open-source monitoring", "oss",
  "Infrastructure only &mdash; but read the licences. Marble is Elastic Licence V2, Jube is AGPLv3, "
  "Tazama is Apache-2.0. Two of those three constrain what you may do commercially."),
 ("The analyst queue", "direct",
  "<strong>Usually the largest line, and the one nobody models.</strong> A compliance analyst in "
  "India plus supervision, QA and tooling is a full salary line. At a 95% false-positive rate, "
  "alert volume is a headcount plan, not a software setting."),
]

i_cost = f'''
{registry("AML tooling &mdash; what each layer costs", cost_rows, V)}
{warn("<strong>Normalise the unit before you compare a single quote.</strong> This market prices on at least four different units and vendors rarely say which. <em>Per screen</em> (one name checked once), <em>per monitored entity</em> (unlimited re-screens of one customer), <em>per seat</em> (named analyst users), and <em>per monitoring scan</em> (each re-screen of each entity, billed separately). The last one is the trap. One vendor charges roughly $0.08 per monitoring scan on top of onboarding verification; if you re-screen daily, as sanctions screening generally requires, that is <strong>365 times the per-scan rate per customer per year</strong>, and it does not appear on the pricing page.")}
<p>Four more cost lines that turn up after signature: sandbox and QA calls billed at production
rates, minimum monthly volumes payable regardless of usage, per-list add-on fees when you need a
jurisdiction outside the bundle, and separate charges for sanctions, PEP and adverse media as three
products rather than one. Ask for all-in TCO at your projected volume, in writing, before you
sign.</p>
{note("The comparison that actually decides this is not vendor against vendor. It is <strong>tool cost plus analyst cost</strong> against the risk it retires. A cheap engine with a 98% false-positive rate is more expensive than an expensive one at 92%, once you price the queue. Make the vendor quote alert volume on your population during the trial, then multiply by your fully loaded cost per alert. That single number resolves most of these decisions.")}
'''

# ---------------------------------------------------------------- AMBER

a_combos = f'''
<table>
<tr><th>Combination</th><th>Works because</th></tr>
<tr><td>Free official feeds + commercial enriched list, both live</td><td>The official feed is the legal source of truth; the commercial layer supplies the aliases. Screen against both and you answer the OFSI question before it is asked.</td></tr>
<tr><td>Deterministic cascade raises alerts &rarr; LLM triages them</td><td>You keep reproducible alert generation and still get most of the false-positive reduction. This is the Fed paper's own recommendation.</td></tr>
<tr><td>Screening API + your own case management</td><td>You buy the data and matching, keep the workflow, the evidence trail and the STR record inside your systems.</td></tr>
<tr><td>Real-time payment screening + batch customer re-screening</td><td>Different latency budgets. Payments need milliseconds; the customer base can be re-screened overnight against the day's list delta.</td></tr>
<tr><td>One alias-enrichment standard across sanctions <em>and</em> PEP</td><td>The gap between the two programmes is the finding. Match them and it disappears.</td></tr>
<tr><td>Monitoring engine + a written typology library</td><td>Scenarios you can name, explain and tune beat a score you cannot. Examiners ask for the rationale, not the AUC.</td></tr>
</table>
<h3 id="s-amber-conflict">Combinations that conflict</h3>
<ul>
<li><strong>An LLM as the primary screen.</strong> Non-deterministic alert generation is not auditable in the sense a regulator means, and at four orders of magnitude slower it will not hold a payment latency budget either.</li>
<li><strong>Two screening vendors running in parallel, permanently.</strong> Fine as a trial. As a steady state you are paying twice and will end up trusting neither when they disagree.</li>
<li><strong>An international platform as your India sanctions workflow.</strong> Most do not implement the 24-hour nodal-officer report, the state-level routing or the CTCR delisting path. You will be building that regardless; plan for it.</li>
<li><strong>Marble, or any Elastic-Licence component, inside a product you offer as a managed service.</strong> Elastic Licence V2 explicitly prohibits providing the software to third parties as a hosted or managed service. If you are a BaaS provider or a PSP offering monitoring to your own clients, that is the prohibited case, precisely.</li>
<li><strong>Blocking a customer on a possible match.</strong> A partial match is a review trigger. Restriction pending verification is proportionate; closure is not, and a wrongly frozen customer is a conduct problem with its own regulatory exposure.</li>
<li><strong>Screening only at onboarding.</strong> Designations happen after account opening. Re-screening on list change is the control, not the extra.</li>
</ul>
'''

a_builds = f'''
<h3 id="s-amber-exp">Strong and expensive</h3>
<p><strong>Build:</strong> enterprise suite (NICE Actimize, Oracle FCCM or SAS) for screening,
monitoring and case management, plus a commercial enriched list, plus a dedicated India workflow
layer from TrackWizz or Clari5 for the UAPA and FIU mechanics.</p>
<p><strong>Use when:</strong> you are a bank or a large NBFC, you have an examination cycle, and you
need a vendor who will sit in the room with the regulator.</p>
<p><strong>Cost shape:</strong> six figures a year in licence before implementation, plus enriched
data, plus the analyst team.</p>
<p><strong>Trade:</strong> tuning goes through someone else's change process. You will wait weeks for
a threshold change you could have made in an afternoon, and you will still own the finding.</p>

<h3 id="s-amber-def">Strong and reasonable &mdash; the default</h3>
<p><strong>Build:</strong> official feeds ingested yourself as the legal source of truth &rarr; a
commercial screening API (ComplyAdvantage class) for matching and enriched data &rarr; your own case
management, evidence trail and FIU filing &rarr; an open-source or built rule engine for transaction
monitoring &rarr; an LLM triage layer on alerts that already exist &rarr; the India workflow built
in-house against the checklist above.</p>
<p><strong>Use when:</strong> you are a fintech, an NBFC or a PA with engineers, and AML is a
standing obligation rather than a one-off certification.</p>
<p><strong>Cost shape:</strong> hundreds of dollars a month for screening at moderate volume, plus
infrastructure, plus the analyst queue &mdash; which will be the largest number.</p>
<p><strong>Trade:</strong> you own the workflow and the evidence, which is the point. The case
record, the threshold rationale and the filing history are the things an examiner reads, and they
should live in your systems, not in a vendor's.</p>
{note("Why this is the default. The regulator examines <em>your</em> programme, not your vendor's product. Every enforcement pattern worth learning from &mdash; the OFSI case above, the FIU-IND orders below &mdash; turned on documentation, escalation and record-keeping rather than on detection technology. Owning that layer is the cheapest insurance available.")}

<h3 id="s-amber-lean">Strong and lean</h3>
<p><strong>Build:</strong> OpenSanctions hosted API with a proper commercial licence &rarr; a
deterministic normalise-exact-fuzzy-phonetic cascade you wrote &rarr; rules and thresholds in a
spreadsheet-backed config with sign-off &rarr; manual case handling with a written procedure &rarr;
FIU filing by hand on FINGate 2.0.</p>
<p><strong>Use when:</strong> pre-launch, or genuinely low volume, or you need a defensible programme
before you have the budget for a platform.</p>
<p><strong>Cost shape:</strong> tens to low hundreds of dollars a month plus the licence, and one
person's part-time attention.</p>
<p><strong>Trade:</strong> it does not scale past a few thousand customers, and manual filing breaks
the moment volume arrives. That is acceptable &mdash; what is not acceptable is an undocumented
programme. A small, written, signed-off setup passes an examination that a sophisticated
undocumented one fails.</p>
{warn("Whichever grade you pick, the thresholds are a documented exercise and not a default. Set the minimum acceptable recall first, as a signed-off policy decision. Then minimise alert volume within that constraint. Then record the analysis, the date, the test-set version and the approver. Threshold sensitivity analysis is a regulatory expectation, not an engineering nicety, and its absence is a finding regardless of which tools you bought.")}
'''

a_next = f'''
<p>What the numbers look like when this goes wrong in India. Section 13 of the PMLA sets the penalty
at &#8377;10,000 to &#8377;1,00,000 <strong>per failure</strong>, which reads as trivial until you
see it multiplied. FIU-IND imposed &#8377;5.49 crore on Paytm Payments Bank, &#8377;18.82 crore on
Binance, &#8377;9.27 crore on Bybit, &#8377;54 lakh on Union Bank of India, and roughly &#8377;96
lakh on PayPal for failing to register at all. The Director can also issue warnings, directions to
comply and directions to submit periodic compliance reports &mdash; and can ask MeitY to block URLs
and delist mobile applications, which for a consumer fintech is a far heavier sanction than the
fine. Registering after enforcement does not extinguish liability for the prior period.</p>
<p>The pattern across all of it: the penalties land on <em>failure to file, failure to do diligence
and failure to keep records</em>, not on failure to buy better detection software.</p>
<h3 id="s-amber-next">What this feeds</h3>
<div class="mod-grid">
<a href="/fintech-ai/identity-onboarding/" class="mod-card"><div class="mod-num">MODULE 01</div><h3>Identity &amp; Onboarding</h3><p>Screening runs on the name you captured at KYC. If the name match at onboarding was wrong, everything downstream is screening the wrong string.</p></a>
<a href="/fintech-ai/fraud-risk/" class="mod-card"><div class="mod-num">MODULE 03</div><h3>Fraud &amp; Risk</h3><p>Mule detection and AML monitoring share features and share a queue. Build the velocity and graph layer once.</p></a>
<a href="/fintech-ai/payments-reconciliation/" class="mod-card"><div class="mod-num">MODULE 05</div><h3>Payments &amp; Reconciliation</h3><p>Real-time payment screening is where the latency budget bites and where the cascade earns its place.</p></a>
<a href="/fintech-ai/governance/" class="mod-card"><div class="mod-num">MODULE 09</div><h3>Governance</h3><p>Threshold rationale, model change control and the evidence pack. The part that is actually examined.</p></a>
</div>
{warn("Everything on this page is illustrative. Sanctions screening, transaction monitoring and regulatory filing carry statutory liability, and in India the freezing procedure carries criminal-law consequences for the customer. Nothing here is legal advice. Have your programme, your thresholds and your filing workflow reviewed by qualified counsel and your compliance officer before it touches a real customer.")}
'''

# ---------------------------------------------------------------- ASSEMBLE

lanes = {
 'green': [
   ("How to read this build sheet", g_read),
   ("Which lists actually bind you", g_lists),
   ("The case that shows what failure looks like", g_case),
 ],
 'indigo': [
   ("Raw materials — sanctions and watchlist data", i_mat_data),
   ("Raw materials — engines, platforms and components", i_mat_eng),
   ("How to use each one — the official free feeds", i_free),
   ("How to use each one — enriched data and matching", i_enriched),
   ("How to use each one — transaction monitoring", i_monitor),
   ("How to use each one — the India workflow", i_india),
   ("Cost per unit", i_cost),
 ],
 'amber': [
   ("Best combinations", a_combos),
   ("Three recommended builds", a_builds),
   ("What next", a_next),
 ],
}

TITLE = "AML and Sanctions Build Sheet"
META  = ("Every sanctions list, screening engine and monitoring tool for AML: how to use each one, "
         "what it costs, and three recommended builds.")
LEAD  = ("Every list, engine and monitoring tool an AML programme needs. What each one is for, the "
         "first working call, the gotcha nobody documents, what it costs per unit, and three "
         "recommended builds at three budgets.")

print(f"title len (with suffix): {len(TITLE + ' | Clarigital')}")
print(f"meta len: {len(META)}")
assert len(TITLE + ' | Clarigital') <= 65
assert len(META) <= 165

page(
  path   = "fintech-ai/aml-compliance/build-sheet",
  title  = TITLE,
  meta   = META,
  lead   = LEAD,
  label  = "Build Sheet 04",
  crumbs = [("/", "Home"), ("/fintech-ai/", "Fintech AI"),
            ("/fintech-ai/aml-compliance/", "AML and Compliance")],
  lanes  = lanes,
)
