#!/usr/bin/env python3
# Session 72 — PRODUCT GUIDE 04: Account Aggregator
import sys, re as _re, io as _io; sys.path.insert(0,'/tmp')
exec(open('/tmp/fintech_builder.py').read())

g_read = '''
<p>This page walks you through building one product, start to finish. This one is a
<em>capability</em> rather than a customer-facing product: it is how you get a customer's financial
data, with their permission, from institutions that are not you.</p>
<p>It feeds almost everything else &mdash; underwriting, wealth advice, personal finance, income
verification.</p>
''' + warn("<strong>The budget warning first, because it is the single most useful thing on this page.</strong> A lender planning a one-directional &ldquo;pull bank statements for underwriting&rdquo; integration is actually scoping <strong>two modules</strong>. Since an RBI circular of October 2023, a regulated entity joining as a data <em>consumer</em> must also join as a data <em>provider</em> if it holds financial information. You will build the side that fetches, <strong>and the side that serves your own loan data to competitors who ask with valid consent</strong>. Budgets built on the first module alone are <strong>wrong by roughly half</strong>.")

g_what = '''
<p>Account Aggregator is India's consented financial data rail. Three roles:</p>
<table>
<tr><th>Role</th><th>Who</th><th>What they do</th></tr>
<tr><td><strong>FIP</strong></td><td>Banks, NBFCs, insurers, depositories, GSTN, NPS record-keepers, CCIL</td><td><strong>Holds</strong> the customer's data.</td></tr>
<tr><td><strong>AA</strong></td><td>An RBI-licensed NBFC</td><td><strong>Moves</strong> the data. Cannot read it.</td></tr>
<tr><td><strong>FIU</strong></td><td>You</td><td><strong>Consumes</strong> the data for a stated purpose.</td></tr>
</table>
<p>The design principle that makes the whole thing work: <strong>the AA is a data-blind pipe</strong>.
Data is encrypted end to end between FIP and FIU, and the AA does not hold the decryption key. It
brokers consent; it never sees the money.</p>
''' + note("This matters when you evaluate AAs. Because they are data-blind, <strong>they cannot differentiate on the data</strong> &mdash; every AA delivers the same bytes. They differentiate on <strong>consent success rate, FIP coverage and uptime</strong>, and those are the only three things worth measuring in a trial.") + '''
<p><strong>The scale, as of 31 December 2025:</strong> around <strong>2.61 billion</strong> accounts
enabled for sharing, <strong>252.9 million</strong> users with linked accounts, <strong>126</strong>
institutions live as both FIP and FIU, and another <strong>50</strong> as FIP only. This is not a
pilot.</p>
<p><strong>What it is not:</strong></p>
<ul>
<li><strong>Not screen scraping.</strong> No credentials, ever. If your flow asks for a net-banking
password, you have built the thing AA exists to replace.</li>
<li><strong>Not a data purchase.</strong> You get what the customer consented to, for as long as they
consented, for the purpose you named.</li>
<li><strong>Not open to everyone.</strong> See step 1.</li>
</ul>
'''

g_map = '''
<table>
<tr><th>#</th><th>Step</th><th>In plain words</th></tr>
<tr><td>1</td><td><strong>Can you even be an FIU?</strong></td><td>You must be regulated by RBI, SEBI, IRDAI or PFRDA. Most startups cannot.</td></tr>
<tr><td>2</td><td><strong>Scope both modules</strong></td><td>Fetching and serving. This is the half everyone forgets.</td></tr>
<tr><td>3</td><td><strong>Pick your AA, or several</strong></td><td>Coverage and consent success rate, not price.</td></tr>
<tr><td>4</td><td><strong>Write the consent request</strong></td><td>Purpose, scope, duration, frequency. This is a legal document in JSON.</td></tr>
<tr><td>5</td><td><strong>Hand over to the AA</strong></td><td>The customer consents in the AA's app, not yours. Design for the handoff.</td></tr>
<tr><td>6</td><td><strong>Fetch and decrypt</strong></td><td>The part that is genuinely just engineering.</td></tr>
<tr><td>7</td><td><strong>Use it &mdash; only for what you said</strong></td><td>Purpose limitation is not a suggestion.</td></tr>
<tr><td>8</td><td><strong>Revocation and expiry</strong></td><td>What you delete, and when, and how you prove it.</td></tr>
</table>
''' + note("Steps 1, 2 and 8 are where the money and the risk are. Steps 4 to 6 are a solved commodity on the happy path &mdash; the ReBIT specification is published, the calls are named, and a competent team gets a fetch working in a fortnight.")

code_consent = code('Python — step 4, the consent artefact, which is a legal document in JSON', r'''from datetime import datetime, timedelta, timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Everything you are allowed to do with this data is decided HERE, before the
# customer sees anything. Over-ask and they decline. Under-ask and you go back
# for a second consent, which they will also decline.

def build_consent_request(customer, use_case):
    now = datetime.now(IST)
    return {
        # WHY. Must be a permitted purpose code, and it binds you at step 7.
        "Purpose": {
            "code": use_case["purpose_code"],       # e.g. "101" wealth, "103" lending
            "text": use_case["purpose_text"],       # shown to the customer, in plain words
            "refUri": use_case["policy_url"],
        },
        # WHAT. Narrow it. "All accounts, all history" reads as a fishing trip.
        "fiTypes": use_case["fi_types"],            # ["DEPOSIT"] not everything
        "consentTypes": ["TRANSACTIONS", "PROFILE", "SUMMARY"],

        # HOW FAR BACK. Ask for what your model uses, not what it might use.
        "FIDataRange": {
            "from": (now - timedelta(days=use_case["lookback_days"])).isoformat(),
            "to":   now.isoformat(),
        },
        # HOW LONG, and HOW OFTEN. A one-off underwriting pull is ONE fetch.
        # A monitoring use case is recurring -- and needs saying out loud.
        "consentStart": now.isoformat(),
        "consentExpiry": (now + timedelta(days=use_case["consent_days"])).isoformat(),
        "fetchType": use_case["fetch_type"],        # "ONETIME" | "PERIODIC"
        "Frequency": use_case.get("frequency"),     # only if PERIODIC
        "DataLife":  {"unit": "MONTH", "value": use_case["retain_months"]},
        "DataFilter": use_case.get("filters", []),

        "customerId": customer["aa_handle"],        # name@aa, not your user id
    }

# WHAT TO CHECK
# [ ] ONETIME vs PERIODIC is a product decision, not a default. A periodic
#     consent for a one-off underwriting decision is over-collection and it is
#     the first thing a reviewer will ask about
# [ ] DataLife is how long you may KEEP it, separate from how long the consent
#     runs. Two different clocks, two different obligations
# [ ] lookback_days matches what your model actually consumes. Asking 24 months
#     to use 6 is over-collection you cannot justify
# [ ] purpose_text is written for a human, not copied from the code table. The
#     customer reads this in the AA app and decides there
# [ ] store the SIGNED ARTEFACT you received, not your request. The artefact is
#     the permission; your request was a proposal
# [ ] one consent per purpose. Bundling lending and marketing into one request
#     is how a whole ecosystem loses consent success rate
''')

i_step12 = '''
<h3 id="s-indigo-s1">Step 1 &mdash; Can you even be an FIU?</h3>
<p><strong>You must be registered with and regulated by RBI, SEBI, IRDAI or PFRDA.</strong> A fintech
with no NBFC licence, no lending licence and no adviser registration cannot be an FIU. There is no
partial route.</p>
<table>
<tr><th>Route</th><th>What it means</th></tr>
<tr><td><strong>Get regulated</strong></td><td>NBFC, investment adviser, insurer, whatever fits the business. Months, and a permanent compliance function.</td></tr>
<tr><td><strong>Partner with a regulated entity</strong></td><td>They are the FIU; you build the product layer. Fast, and the data-use decisions are theirs.</td></tr>
<tr><td><strong>Become an AA yourself</strong></td><td>An RBI-licensed NBFC-AA: <strong>&#8377;2 crore Net Owned Fund</strong> before the certificate, no storage or caching of financial data, tested DR and business continuity, three board committees, periodic IS audits.</td></tr>
</table>
''' + warn("If you are considering the third row: the commonly cited reasons applications stall are <strong>incomplete technical documentation, not reaching the &#8377;2 crore Net Owned Fund before the certificate is issued, a poor consent-revocation interface, and skipped IS audits or DR drills</strong>. Three of those four are engineering problems that arrive disguised as paperwork.") + '''

<h3 id="s-indigo-s2">Step 2 &mdash; Scope both modules</h3>
<p><strong>What it does:</strong> the part of the project that doubles the estimate.</p>
<p>Since October 2023, a regulated entity joining as an FIU <strong>must also join as an FIP</strong>
if it holds financial information. The rule exists to stop free-riding: you cannot take from the
ecosystem without contributing to it.</p>
<table>
<tr><th>Module</th><th>What it does</th><th>Usually estimated?</th></tr>
<tr><td><strong>FIU side</strong></td><td>Request consent, fetch, decrypt, use.</td><td>Yes. This is what people mean by &ldquo;AA integration&rdquo;.</td></tr>
<tr><td><strong>FIP side</strong></td><td>Receive consent artefacts, <strong>validate their signatures</strong>, and serve <em>your</em> data to whoever asks with valid consent &mdash; including competitors.</td><td><strong>No.</strong> And it has harder availability requirements, because now you are the dependency.</td></tr>
</table>
<p>The FIP side is the more demanding build. As an FIU, a slow response is your problem. As an FIP,
<strong>a slow response is someone else's customer failing to get a loan</strong>, and your uptime
becomes an ecosystem metric.</p>
'''

i_step34 = '''
<h3 id="s-indigo-s3">Step 3 &mdash; Pick your AA</h3>
<p>Because every AA is data-blind, they all deliver identical bytes. There are exactly three things
worth measuring, and none of them is the per-fetch price.</p>
<table>
<tr><th>Measure</th><th>Why it decides the product</th></tr>
<tr><td><strong>FIP coverage</strong></td><td>Which banks your actual customers use. A 95% coverage figure is meaningless if the missing 5% is where your segment banks.</td></tr>
<tr><td><strong>Consent success rate</strong></td><td>The share of started journeys that end in delivered data. <strong>This is the number.</strong> It moves conversion more than anything you control.</td></tr>
<tr><td><strong>Uptime, and FIP-level uptime</strong></td><td>An AA that is up while a major FIP is down is still a failed fetch for your customer. Ask for the breakdown, not the headline.</td></tr>
</table>
''' + note("Use more than one AA. They cost little to run in parallel, coverage differs, and consent success rate differs by AA <em>and</em> by FIP. Routing a customer to the AA with the best success rate for <em>their</em> bank is a real conversion gain and it is invisible if you only integrated one.") + '''

<h3 id="s-indigo-s4">Step 4 &mdash; Write the consent request</h3>
''' + code_consent + '''
<p><strong>The gotcha nobody documents:</strong> two clocks. <code>consentExpiry</code> is how long
your permission to <em>fetch</em> lasts. <code>DataLife</code> is how long you may <em>keep</em> what
you already fetched. Teams set one and assume it governs both, then either delete data they were
entitled to retain, or &mdash; much worse &mdash; retain data whose life expired months ago.
<strong>Model them as two independent timers from the start</strong>, because retrofitting a
retention clock onto a warehouse is genuinely painful.</p>
'''

code_fetch = code('Python — steps 5 and 6, the handoff and the fetch', r'''# STEP 5. The customer leaves your app, consents inside the AA's app, and comes
# back. That redirect is where most drop-off happens, and it is the part you can
# actually influence.

def start_consent_journey(consent_request, aa_client, session):
    art = aa_client.create_consent(consent_request)     # returns consentHandle
    return {
        "redirect_url": art["redirectUrl"],
        "consent_handle": art["consentHandle"],
        # Save EVERYTHING you will need when they come back. They may return on
        # a different device, an hour later, or not at all.
        "resume_token": persist_session(session, art["consentHandle"]),
        # Tell them what is about to happen. An unexplained redirect to an
        # unfamiliar brand is the single biggest cause of abandonment here.
        "explain": "You'll approve this with your Account Aggregator, then come "
                   "straight back. We never see your banking password.",
    }

# STEP 6. Poll for the artefact, then fetch, then decrypt.
def fetch_when_ready(consent_handle, aa_client, keys):
    status = aa_client.consent_status(consent_handle)
    if status["status"] == "PENDING":
        return {"state": "waiting"}                     # customer still deciding
    if status["status"] in ("REJECTED", "EXPIRED"):
        return {"state": "no_consent", "reason": status["status"]}

    artefact = aa_client.get_consent(status["consentId"])
    verify_signature(artefact)                          # NOT optional
    store_artefact(artefact)                            # the permission itself

    sess = aa_client.create_fi_request(artefact, keys["public"])
    data = aa_client.fetch_fi(sess["sessionId"])        # encrypted payload
    return {"state": "ready",
            "records": [decrypt(d, keys["private"]) for d in data["FI"]]}

# WHAT TO CHECK
# [ ] VERIFY THE ARTEFACT SIGNATURE. It is the only thing proving the customer
#     actually consented. Skipping it because "it came from the AA" removes the
#     entire security property of the framework
# [ ] the redirect explains itself BEFORE it happens, and names the AA. An
#     unexplained jump to an unknown brand is the main drop-off cause
# [ ] resume works on a different device and after a delay. Consent journeys are
#     abandoned and resumed hours later far more often than teams assume
# [ ] PENDING is normal and can last minutes. Poll with backoff; never block a
#     user-facing request on it
# [ ] private keys live in a KMS or HSM, never in application config. You are
#     holding the only thing standing between an encrypted payload and a breach
# [ ] a failed fetch is reported to the customer in plain words, with a retry.
#     "Something went wrong" after they just approved data sharing reads as a
#     betrayal of the trust they extended thirty seconds ago
# [ ] log every step with the consent handle. Disputes are reconstructed from it
''')

i_step56 = '''
<h3 id="s-indigo-s5">Steps 5 and 6 &mdash; The handoff and the fetch</h3>
''' + code_fetch + '''
<p><strong>The gotcha nobody documents:</strong> the redirect is the product. Everything else on this
page is compliance and engineering; the moment a customer leaves your app for an unfamiliar
third-party brand is where the conversion actually happens or does not. <strong>Explain what is about
to occur, name the AA, and say explicitly that you never see their banking password</strong> &mdash;
because a meaningful share of people assume you will, and abandon for exactly that reason.</p>
'''

i_step78 = '''
<h3 id="s-indigo-s7">Step 7 &mdash; Use it, only for what you said</h3>
<p><strong>Purpose limitation is enforceable.</strong> You named a purpose in the consent, the
customer approved <em>that</em>, and using the data for something else is a breach of the consent and
a DPDP problem at the same time.</p>
<p>Three rules that keep this simple:</p>
<ul>
<li><strong>Tag every record with the consent id it arrived under.</strong> Then &ldquo;may we use
this for X&rdquo; is a query, not a meeting.</li>
<li><strong>A new purpose needs a new consent.</strong> Not a wider one next time &mdash; a separate
one, for the new thing.</li>
<li><strong>Derived data inherits the purpose.</strong> A score computed from AA data is AA data. This
is the same rule as embeddings inheriting residency in
<a href="/fintech-ai/infrastructure/build-sheet/">Build Sheet 08</a>, and it is missed for the same
reason: the derived artefact does not look like the source.</li>
</ul>

<h3 id="s-indigo-s8">Step 8 &mdash; Revocation and expiry</h3>
<p><strong>The customer can revoke at any time.</strong> Your system must handle that arriving
without warning, for a customer mid-journey, on a Sunday.</p>
<table>
<tr><th>Event</th><th>What must happen</th></tr>
<tr><td><strong>Revoked</strong></td><td>Stop fetching immediately. Existing data is governed by <code>DataLife</code>, not deleted on the spot &mdash; but no new fetches, ever, under that consent.</td></tr>
<tr><td><strong>Consent expired</strong></td><td>Same. Fetching on an expired consent is the clearest possible breach.</td></tr>
<tr><td><strong>DataLife expired</strong></td><td><strong>Delete.</strong> Including from backups, derived tables and any model training set it reached.</td></tr>
</table>
''' + warn("<strong>&ldquo;Delete&rdquo; is the hardest word on this page.</strong> Financial data fetched for underwriting typically lands in a warehouse, a feature store, a model training set and a backup within its first hour. A retention clock that only deletes the primary record has deleted almost nothing. <strong>Decide, before your first fetch, where AA data is allowed to go</strong> &mdash; and keep that list short, because every destination is a place you will have to delete from later and prove that you did.")

i_cost = registry("Account Aggregator &mdash; what it costs", [
 ("Being an FIU", "direct",
  "The licence you already hold, or a partnership. <strong>The regulatory status is the entry "
  "cost</strong>, not the integration."),
 ("Per fetch", "direct",
  "AAs charge per successful data fetch, commercially negotiated and modest at volume. "
  "<strong>Not the number that decides anything</strong> &mdash; consent success rate moves your "
  "economics far more than per-fetch price."),
 ("The FIU module", "direct",
  "Consent, fetch, decrypt, store. Weeks for a competent team. ReBIT specifications are published "
  "and the calls are named, so the happy path is a solved commodity."),
 ("The FIP module", "direct",
  "<strong>The half that is missed.</strong> Receive and validate artefacts, serve your own data on "
  "demand, with availability that matters to other firms' customers. <strong>Budget roughly the same "
  "again as the FIU side</strong>, plus ongoing uptime obligations."),
 ("Becoming an AA", "direct",
  "<strong>&#8377;2 crore Net Owned Fund</strong> before the certificate, three board committees, "
  "periodic IS audits, tested DR, and a no-storage architecture. A licensed business, not a feature."),
 ("Certification and membership", "direct",
  "Certification by a Sahamati-empanelled auditor, plus ecosystem membership fees by category. "
  "Small next to the build, and a gating item on timelines."),
 ("Retention and deletion", "direct",
  "<strong>Quietly the expensive one.</strong> Every destination AA data reaches is somewhere you "
  "must later delete from and evidence the deletion. This is engineering time, not licence cost."),
], "September 2026") + note("<strong>The number to optimise is consent success rate, and almost nobody instruments it.</strong> Measure it per AA, per FIP and per step of the journey &mdash; started, redirected, approved, delivered. A 10-point improvement there is worth more than any price negotiation you will have, and it is entirely within your control at the redirect.")

a_builds = '''
<h3 id="s-amber-week">The starting version</h3>
<p><strong>Build:</strong> partner with a regulated entity as FIU &rarr; one AA &rarr; a single
narrow consent for one purpose &rarr; a clearly explained redirect &rarr; fetch, decrypt, store with
the consent id attached &rarr; a manual revocation process.</p>
<p><strong>It breaks when:</strong> you need a bank the AA does not cover, or a second purpose.</p>

<h3 id="s-amber-proper">The proper version</h3>
<p><strong>Build:</strong> everything above, plus &mdash; <strong>two or three AAs with routing by FIP
coverage and success rate</strong> &rarr; both modules, FIU and FIP, scoped from day one &rarr;
consent and DataLife as separate enforced timers &rarr; every record tagged with its consent id
&rarr; a written list of permitted destinations for AA data &rarr; automated deletion covering
warehouse, features and backups &rarr; consent success rate instrumented per AA, per FIP, per step.</p>
<p><strong>Trade:</strong> the deletion machinery is real work for a benefit nobody sees until it is
needed. Build it early anyway, because it is far harder to add once data has spread.</p>

<h3 id="s-amber-big">Becoming the AA</h3>
<p><strong>Build:</strong> an RBI-licensed NBFC-AA. A different business with a different balance
sheet, board committees and audit regime.</p>
<p><strong>Use when:</strong> consent management <em>is</em> your product. Not because you want better
terms on fetches.</p>
''' + note("If you take one thing from this page: <strong>scope the FIP module in your first estimate.</strong> It is the half that is forgotten, it is the harder half, and discovering it mid-project is how an eight-week integration becomes a quarter.")

a_breaks = '''
<table>
<tr><th>What goes wrong</th><th>Why</th><th>Fix</th></tr>
<tr><td><strong>The estimate is half the work</strong></td><td>Only the FIU module was scoped.</td><td>FIP module from day one.</td></tr>
<tr><td><strong>Consent success rate is poor</strong></td><td>The redirect is unexplained.</td><td>Say what happens next and name the AA before you send them.</td></tr>
<tr><td><strong>Signature never verified</strong></td><td>&ldquo;It came from the AA, so it is fine.&rdquo;</td><td>Verify. It is the whole security property.</td></tr>
<tr><td><strong>Data retained past DataLife</strong></td><td>Only consent expiry was modelled.</td><td>Two independent clocks.</td></tr>
<tr><td><strong>Deletion misses the warehouse</strong></td><td>The retention job deletes the primary record only.</td><td>A written destination list, enforced.</td></tr>
<tr><td><strong>A score outlives its consent</strong></td><td>Derived data was not treated as AA data.</td><td>Derived inherits purpose and retention.</td></tr>
<tr><td><strong>Coverage gap for your segment</strong></td><td>A headline coverage number was accepted.</td><td>Test with your own customers' banks.</td></tr>
<tr><td><strong>One consent bundles several purposes</strong></td><td>It seemed efficient.</td><td>One consent per purpose.</td></tr>
</table>
'''

SRC=[('official','RBI Master Direction — NBFC-Account Aggregator (2 September 2016, as amended)','the AA licence, the data-blind architecture, the no-storage requirement and the ₹2 crore Net Owned Fund. Amended to add GSTN (2022), NPS record-keepers (2023) and CCIL (2024) as FIPs.','https://www.rbi.org.in'),
 ('official','RBI circular, October 2023','the bilateral mandate — a regulated entity joining as an FIU must also join as an FIP if it holds financial information.','https://www.rbi.org.in'),
 ('official','ReBIT technical specifications','the consent artefact structure, the API sequence and the encryption scheme every party implements.','https://api.rebit.org.in'),
 ('official','Sahamati','ecosystem participant lists, the live metrics quoted here, certification and membership categories. RBI recognised Sahamati as the AA self-regulatory organisation on 5 June 2026.','https://sahamati.org.in'),
 ('official','DPDP Act, 2023','consent, purpose limitation and erasure obligations that sit alongside the AA framework rather than replacing it.','https://www.meity.gov.in'),
 ('industry','Ecosystem scale figures (31 December 2025)','2.61 billion accounts enabled, 252.9 million users with linked accounts, 126 institutions as both FIP and FIU, 50 FIP-only. Published ecosystem metrics; check the current dashboard before quoting.','')]
_s=open('fintech-ai/governance/build-sheet/index.html',encoding='utf-8').read()
CSSRC=_re.search(r'\n\.srcs\{.*?\.srcs a\{word-break:break-word\}',_s,_re.S).group(0)
lis=''.join(f'<li><span class="src-k src-{k}">{k}</span><strong>{n}</strong> &mdash; {w}'+(f' <a href="{u}" target="_blank" rel="noopener">{u.split("//")[-1].split("/")[0]}</a>' if u else '')+'</li>' for k,n,w,u in SRC)
a_src=('<h2 id="sources">Sources</h2><p>Every figure, rule and date on this page, and where to check it. '
 'Entries are typed so you can see which are primary-sourced and which are industry reporting.</p>'
 f'<div class="srcs"><ol>{lis}</ol><p style="font-size:.75rem;color:var(--faint);margin-top:12px">'
 'Checked September 2026. Ecosystem figures move monthly; the date is part of the claim.</p></div>')

a_next='''
<div class="mod-grid">
<a href="/fintech-ai/credit-underwriting/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 02</div><h3>Credit &amp; Underwriting</h3><p>What you do with the bank statements once they arrive, and the hybrid architecture around the model.</p></a>
<a href="/fintech-ai/products/bnpl-checkout/" class="mod-card"><div class="mod-num">GUIDE 03</div><h3>BNPL Checkout</h3><p>Where an AA fetch runs at checkout latency, on every transaction rather than every application.</p></a>
<a href="/fintech-ai/wealth-advisory/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 07</div><h3>Wealth &amp; Advisory</h3><p>AA as the route to a real fact find, rather than a self-reported one.</p></a>
<a href="/fintech-ai/infrastructure/build-sheet/" class="mod-card"><div class="mod-num">BUILD SHEET 08</div><h3>Infrastructure</h3><p>Residency, key management, and why derived data inherits the restrictions of its source.</p></a>
</div>
''' + warn("This page is a guide, not a specification. The Account Aggregator framework is RBI-regulated and consented financial data carries obligations under both the framework and the DPDP Act. Nothing here is legal advice. Have your consent wording, retention design and deletion process reviewed by qualified counsel before your first real fetch.")

lanes={'green':[("How to use this page",g_read),("What Account Aggregator actually is",g_what),("The whole journey, in one table",g_map)],
 'indigo':[("Steps 1 and 2 — eligibility, and the module everyone forgets",i_step12),
           ("Steps 3 and 4 — choosing an AA and writing the consent",i_step34),
           ("Steps 5 and 6 — the handoff and the fetch",i_step56),
           ("Steps 7 and 8 — purpose, revocation and deletion",i_step78),
           ("What it costs",i_cost)],
 'amber':[("Three versions you could build",a_builds),("What goes wrong",a_breaks),("Where to go next",a_next+a_src)]}

TITLE="Account Aggregator: How to Build It"
META=("Build an Account Aggregator integration step by step: the eight stages, your options at each "
      "one, how to connect them, and the module everyone forgets.")
LEAD=("A step-by-step guide to building an Account Aggregator integration. Eight stages, the options "
      "at each one, exactly how each step connects to the next, real costs, and what breaks. Written "
      "for someone who has not built this before.")
print("title",len(TITLE+' | Clarigital'),"meta",len(META))
assert len(TITLE+' | Clarigital')<=65 and len(META)<=165
page(path="fintech-ai/products/account-aggregator",title=TITLE,meta=META,lead=LEAD,label="Product Guide 04",
     crumbs=[("/","Home"),("/fintech-ai/","Fintech AI")],lanes=lanes)
f='fintech-ai/products/account-aggregator/index.html'
h=_io.open(f,encoding='utf-8').read()
if '.srcs{' not in h: _io.open(f,'w',encoding='utf-8').write(h.replace('</style>',CSSRC+'\n</style>',1))
