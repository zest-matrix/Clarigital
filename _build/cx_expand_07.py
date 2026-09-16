#!/usr/bin/env python3
"""cx_expand_07.py — Session 98. Seventh content-remediation batch, thirteen pages.

Eight Codex and five AI Atlas. Anchor logic copied from cx_expand_06.py,
which handles both templates.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

EUAI = ('official', 'Regulation (EU) 2024/1689 (AI Act) and Regulation (EU) 2026/1744 (Digital Omnibus on AI)',
        'the risk tiers, the deferred high-risk dates, the Article 50 transparency duties, the GPAI systemic-risk threshold and the penalty ceiling. The Omnibus was adopted by Parliament on 16 June 2026, approved by Council on 29 June, published in the Official Journal on 24 July and entered into force on 27 July 2026',
        'eur-lex.europa.eu')
EUC = ('official', 'European Commission — Navigating the AI Act',
       'the Commission\'s own account of why the high-risk timeline moved and what was not deferred',
       'digital-strategy.ec.europa.eu')
GBP = ('official', 'Google Business Profile guidelines and Help documentation',
       'category behaviour, prohibited name keywords, the Q&A mechanics and suspension causes described here',
       'support.google.com')
GSC = ('official', 'Google Search Central documentation',
       'structured data eligibility, snippet controls and the AI feature guidance referenced here',
       'developers.google.com')
AMZ = ('official', 'Amazon Advertising and Seller Central documentation',
       'campaign types, match-type behaviour, product targeting and the placement reporting described here',
       'advertising.amazon.com')
IAB = ('official', 'IAB Tech Lab OpenRTB specification and seller authorisation files',
       'the bid request sequence, auction mechanics and supply-chain verification described here',
       'iabtechlab.com')

S = lambda t, c: (t, c)

PAGES = {

'codex/programmatic/real-time-bidding': dict(sources=[IAB], sections=[
 S('Where the Latency Budget Actually Goes', '''
<p>The whole auction completes in roughly the time it takes a page element to render, and that budget
is the constraint shaping every decision in the chain.</p>
<p>The exchange sets a timeout — typically in the low hundreds of milliseconds — and
<strong>a bidder that does not respond in time is simply excluded</strong>. Not penalised, not logged
as a loss you can analyse: absent. This produces a failure mode buyers routinely misdiagnose as poor
inventory or weak targeting.</p>
<p>What consumes the budget: the network round trip, which is physics and is why bidders run
infrastructure close to the exchanges; the bidder's own decisioning, including any model inference;
and any external lookup — a user data call, a frequency check, a brand-safety score.</p>
<p>The practical consequences. <strong>Every enrichment you add to the bid path costs win
rate</strong>, so the question for each is whether its lift exceeds the impressions it loses.
<strong>Timeout rate is a metric worth watching</strong> and almost nobody does; a bidder timing out on
a share of requests has a capacity problem wearing a performance costume. And
<strong>geography matters</strong> — bidding into a distant exchange means part of the budget is spent
before any decision is made.</p>
'''),
 S('Reading a Win-Rate Problem Correctly', '''
<p>Low win rate is the most common complaint and has several unrelated causes that look identical in
a dashboard.</p>
<table>
<tr><th>Symptom</th><th>Likely cause</th></tr>
<tr><td>Few bid requests reaching you at all</td><td>A supply problem, not a bidding one. Check your integrations and targeting breadth before your bids</td></tr>
<tr><td>Bidding often, winning rarely, clearing price far above your bid</td><td>Genuinely outbid. The inventory is more valuable to someone else</td></tr>
<tr><td>Bidding often, winning rarely, clearing price close to your bid</td><td>A bid-shading or pacing issue. Small increases may move a lot</td></tr>
<tr><td>Winning almost everything you bid on</td><td><strong>Usually bad news.</strong> You are probably overpaying, or the inventory nobody else wants</td></tr>
<tr><td>High timeout rate</td><td>Infrastructure. No bid adjustment fixes it</td></tr>
</table>
<p>The line worth remembering: <strong>an unusually high win rate is a finding to investigate, not a
result to celebrate.</strong> In a competitive auction, winning most of what you bid on means either
your bids are too high or you are the only buyer interested — and the second is rarely a compliment to
the inventory.</p>
''')]),

'codex/paid-advertising/amazon-ads/retail-media-networks': dict(sources=[AMZ], sections=[
 S('Separating the Advertising Decision From the Trade Decision', '''
<p>The structural problem with retail media is that the entity selling you advertising also controls
your shelf, your search ranking and your terms — so the negotiation is never purely about media
performance.</p>
<p>What that produces in practice: <strong>budget requested as a condition of something else</strong>
— a promotion, a listing, favourable placement — and an advertiser unable to tell whether the spend
performed or merely preserved the relationship.</p>
<p>The discipline that helps is separation, in three parts. <strong>Measure the media on media
terms</strong>, with the same incrementality standard you would apply to any other channel.
<strong>Account for trade spend separately</strong> from advertising spend, even when the same person
negotiates both, so neither hides in the other. And <strong>write down, before the conversation, the
performance level at which you would reduce the budget</strong> — because deciding that during a
negotiation is not deciding it.</p>
<p>None of this is adversarial. It is the only way to know whether a retail media programme is working,
and the answer matters most precisely where the relationship makes it hardest to ask.</p>
'''),
 S('Measuring It Without the Platform Marking Its Own Work', '''
<p>Retail media has a genuine measurement advantage — the platform sees the purchase — and that same
closeness is why its reported numbers need handling carefully.</p>
<p><strong>Distinguish new-to-brand from total.</strong> The most useful metric these platforms offer
is whether a buyer was new to your brand. A programme delivering strong returns entirely from existing
customers is capturing demand rather than creating it, which may still be worth doing, but is a
different business case.</p>
<p><strong>Watch total category sales, not attributed sales.</strong> If attributed sales rise while
your total sales on the platform do not, the advertising is reallocating credit.</p>
<p><strong>Treat branded-keyword returns sceptically.</strong> Advertising against your own brand name
on a retailer where you already rank produces excellent-looking numbers and frequently buys clicks you
had. Test it by pausing, which is cheap and unpopular.</p>
<p><strong>And run an off-platform check.</strong> Retail media influences search and consideration
beyond the retailer, so a purely on-platform view under-reports the good and over-reports the
attributed — in opposite directions at once.</p>
''')]),

'codex/seo/ai-search/answer-engine-optimisation': dict(sources=[GSC], sections=[
 S('Writing So a Machine Can Lift the Answer', '''
<p>The structural requirement is the same across every answer surface: <strong>the answer must be
extractable without the surrounding page.</strong> A paragraph that only makes sense after three
paragraphs of context cannot be quoted.</p>
<p>What that looks like in practice:</p>
<ul>
<li><strong>Answer in the first sentence under the heading</strong>, then elaborate. The inverted
pyramid, applied per section rather than per article.</li>
<li><strong>One question per heading</strong>, phrased as the question is actually asked.</li>
<li><strong>Self-contained paragraphs</strong> that carry their own subject — no opening
<em>"this means that"</em> pointing at something above.</li>
<li><strong>Definitions stated plainly</strong> and early, not built up to.</li>
<li><strong>Specific, checkable claims</strong> with figures and dates, because a hedged generality is
not worth extracting.</li>
</ul>
<p>The counter-intuitive part: <strong>this is also better writing for humans.</strong> The discipline
of making each section stand alone produces pages people can scan and use, which is why AEO rarely
requires a trade-off against quality — and why pages written to game it read badly to both audiences.</p>
'''),
 S('Being Honest About What It Returns', '''
<p>AEO is worth doing and is frequently oversold, and the gap is about what success looks like.</p>
<p><strong>The realistic outcome is being cited, not being visited.</strong> An answer surface that
uses your page may send no click at all. If your business model depends on pageviews, optimising to be
the source of an answer that replaces the visit is optimising against yourself — worth saying plainly
before the strategy is adopted.</p>
<p><strong>The value is real where the citation itself is the win</strong>: brand presence at the
moment of a question, credibility with a professional audience, and being the reference a buyer
already half-trusts when they eventually do click.</p>
<p><strong>Measurement is genuinely hard.</strong> Referral data from assistant surfaces is
inconsistent, so the workable signals are indirect — branded search volume, direct traffic, and
periodically asking the assistants your own questions and recording who they cite.</p>
<p><strong>And it is not a separate discipline.</strong> Almost everything that makes a page extractable
is standard structure, clarity and substance. A team being sold AEO as a new practice requiring new
tooling should ask which part is not already in their SEO brief.</p>
''')]),

'codex/seo/local/google-business-profile': dict(sources=[GBP], sections=[
 S('What Gets a Profile Suspended', '''
<p>Suspension is the risk nobody plans for and it removes your listing from the map entirely while you
appeal — which can take weeks.</p>
<p>The common causes, most frequent first:</p>
<ul>
<li><strong>Keywords in the business name.</strong> The name field must be the real-world name.
<em>"Sharma Dental — Best Dentist in Pune"</em> is the single most common violation, it is easy to
detect, and competitors report it.</li>
<li><strong>An address that is not a real, staffed location</strong> — a virtual office, a mailbox, a
co-working desk, or a residential address publicly displayed for a service business that should hide
it.</li>
<li><strong>Multiple listings for one location</strong>, or a listing per practitioner where the
guidelines permit one.</li>
<li><strong>Category not matching what the business does</strong> on the premises.</li>
<li><strong>A sudden burst of reviews</strong>, which triggers review-related suspension even where
the reviews are genuine.</li>
</ul>
<p><strong>Edit substantial fields one at a time, with a gap.</strong> Changing name, address,
category and hours together on an established profile is a recognised trigger.</p>
'''),
 S('Maintaining It as a Live Channel', '''
<p>The profile is treated as a setup task and behaves like a channel — it changes without you, and the
changes are visible to customers before they are visible to you.</p>
<p><strong>Suggested edits from the public can alter your information.</strong> Someone can propose a
different phone number or set of hours, and it can go live. Check the profile on a schedule; this is
the single most common cause of <em>&ldquo;our number is wrong on Google&rdquo;</em>.</p>
<p><strong>The Q&amp;A section is public and anyone can answer.</strong> Questions left unanswered get
answered by strangers, sometimes wrongly. <strong>Seed it deliberately</strong> with the questions you
are actually asked and answer them yourself.</p>
<p><strong>Hours matter more than they look.</strong> Special hours for holidays prevent the review
that begins <em>"drove there and it was closed"</em>, which is unanswerable after the fact.</p>
<p><strong>Photos age.</strong> Customer photos accumulate and the impression is formed by the most
recent, not the best.</p>
<p><strong>And watch the insights for direction requests and calls</strong> rather than views. Those are
the actions; views are the audience — and the only one of the two you can act on is the first.</p>
''')]),

'codex/analytics-cro/customer-data-platforms': dict(sources=[], sections=[
 S('The Question That Decides Whether You Need One', '''
<p>CDP projects fail more often than they succeed, and the failures are visible in advance from one
question: <strong>what will you do with a unified profile that you cannot do now?</strong></p>
<p>If the answer is a specific activation — suppress existing customers from acquisition campaigns,
trigger a message when behaviour across two systems combines, give support the purchase history at the
moment of a call — the project has a destination. If the answer is *"have a single view of the
customer"*, it does not, and the platform will be bought, populated, and left.</p>
<p>Three conditions that make one genuinely worth it: <strong>customer data genuinely scattered</strong>
across systems that cannot talk to each other; <strong>a marketing team that needs to build audiences
without engineering help</strong>, which is the honest core of the value proposition; and
<strong>identity resolution that actually matters</strong> to your business, meaning the same person
appears under different identifiers often enough to distort decisions.</p>
<p>Without at least two of those, a data warehouse and a scheduled export will do the same job for a
fraction of the cost and effort.</p>
'''),
 S('Identity Resolution, and the Damage It Can Do', '''
<p>Identity resolution is what a CDP is really selling, and it is where the risk sits.</p>
<p><strong>Deterministic matching</strong> — joining records that share a verified identifier such as
an email or account ID — is reliable and limited to the customers who have given you one.</p>
<p><strong>Probabilistic matching</strong> — inferring that two devices are the same person from
behaviour, network and timing — extends coverage and <strong>is wrong some of the time in both
directions</strong>. It merges two people into one profile and splits one person into two.</p>
<p>The consequences of a wrong merge are worse than most teams anticipate: <strong>one household
member sees another's recommendations</strong>, a support agent reads the wrong purchase history, and
in a regulated context you have combined two people's personal data. <strong>A subject access request
against a probabilistically merged profile is a genuinely awkward thing to answer.</strong></p>
<p>The defensible position: <strong>deterministic matching for anything a customer sees or that
affects a decision about them; probabilistic only for aggregate analysis</strong>, clearly labelled as
an estimate. And under a consent-based regime, be able to say which basis covers the joining itself —
not just the collection of each part.</p>
''')]),

'codex/paid-advertising/amazon-ads/sponsored-products': dict(sources=[AMZ], sections=[
 S('The Harvest Loop That Runs the Account', '''
<p>A working Sponsored Products account is a loop rather than a setup, and the loop is the same every
week.</p>
<ol>
<li><strong>Automatic campaigns discover terms</strong> you would not have guessed. Their job is
research, not performance, and judging them on ACOS misreads what they are for.</li>
<li><strong>Pull the search term report</strong> and find terms that converted.</li>
<li><strong>Promote those into an exact-match manual campaign</strong> where you control the bid.</li>
<li><strong>Add them as negatives in the automatic campaign</strong>, so the two stop competing for the
same query and you stop paying twice to learn the same thing.</li>
<li><strong>Negate the spenders that never convert</strong>, which is where most wasted budget goes.</li>
</ol>
<p><strong>The step almost everyone skips is four.</strong> Without it, the automatic campaign keeps
bidding on terms you have already graduated, and the account's own campaigns bid against each other —
visible as rising cost on terms whose conversion rate has not changed.</p>
<p>Run it weekly at first, then fortnightly. The discovery slows but never stops, because the
catalogue and the competition both keep moving.</p>
'''),
 S('Why the Listing Constrains the Advertising', '''
<p>Advertising on a retail platform is unusual in that <strong>the landing page is the product listing
and you cannot design it freely.</strong> Everything downstream of the click is governed by the
listing, which means ad performance is capped by things that are not the ad.</p>
<p>What actually determines whether the click converts: <strong>the main image</strong>, which must
meet the platform specification and carries most of the decision; <strong>price relative to visible
alternatives</strong>, since competitors appear on your own page; <strong>reviews and rating</strong>,
which no bid adjustment can compensate for; <strong>availability</strong>, because an out-of-stock item
should not be advertised at all and frequently is; and <strong>the fulfilment badge</strong>, which
shifts conversion more than most creative changes.</p>
<p>The practical rule: <strong>fix the listing before raising the bid.</strong> A poor listing with a
high bid buys expensive traffic that does not convert, and the reporting will describe it as a
keyword problem.</p>
<p>And <strong>check the placement report</strong>. Top-of-search usually converts better and costs
more; a placement adjustment is often a cleaner lever than a keyword-level bid change.</p>
''')]),

'ai-atlas/concepts/token-economics': dict(sources=[], sections=[
 S('Where the Bill Comes From, and Why Estimates Are Wrong', '''
<p>Cost forecasts for a language-model feature are usually wrong in the same direction, because the
estimate is built from the visible request and the bill is driven by what surrounds it.</p>
<p>The components people forget:</p>
<p><strong>The system prompt is charged on every call.</strong> A long instruction block is a fixed
cost per request, multiplied by volume. Halving it is frequently the largest single saving available
and nobody looks there.</p>
<p><strong>Conversation history is resent.</strong> Models are stateless, so a ten-turn conversation
sends the preceding nine turns again on the tenth call. Cost grows with the square of conversation
length unless you truncate or summarise.</p>
<p><strong>Retrieved context dominates.</strong> Where documents are injected, the retrieved passages
typically outweigh everything else, so retrieval precision is a cost decision as much as a quality one.</p>
<p><strong>Retries and failures are billed.</strong> A malformed response that triggers a retry costs
twice.</p>
<p><strong>And reasoning output is billed as output</strong>, so a model that deliberates at length
costs materially more than its headline price implies.</p>
'''),
 S('Reducing It Without Making the Product Worse', '''
<p>The levers, in rough order of saving against effort:</p>
<p><strong>Route by task.</strong> Most requests in most applications are not hard. Sending everything
to the most capable model is the single largest and most common overspend — classification, extraction
and formatting rarely need the top tier.</p>
<p><strong>Shorten the system prompt.</strong> Fixed cost, every call, and usually accumulated by
addition over months without anyone removing anything.</p>
<p><strong>Cache the stable prefix.</strong> Where the provider supports it, the unchanging front of a
prompt can be reused across calls at reduced cost — the highest-return change for applications with a
long fixed preamble, and it requires putting the stable part first, which is a code change rather than
a setting.</p>
<p><strong>Cap output length deliberately</strong>, and ask for the format you need rather than trimming
prose afterwards.</p>
<p><strong>Manage the conversation window</strong>: summarise old turns instead of resending them.</p>
<p><strong>And instrument before optimising.</strong> Log tokens per request by feature and by user
before changing anything, because the intuition about where the spend sits is wrong more often than it
is right — <strong>and a cost programme that starts with guesses usually optimises the wrong
call.</strong></p>
''')]),

'ai-atlas/concepts/open-vs-closed-models': dict(sources=[], sections=[
 S('Reading the Licence Before the Benchmark', '''
<p>The word <em>open</em> covers licences that differ enormously, and the differences bite after deployment
rather than during evaluation.</p>
<p>What to check, in order of how often it causes a problem:</p>
<ul>
<li><strong>Commercial use.</strong> Some weights are released for research only. This is the most
basic check and is skipped surprisingly often.</li>
<li><strong>Scale thresholds.</strong> Several licences impose additional terms above a user or
revenue threshold, so a licence that is free today is negotiable at the point you succeed.</li>
<li><strong>Acceptable-use restrictions</strong>, which limit application domains regardless of the
technical capability.</li>
<li><strong>Whether outputs may train another model</strong>, which matters if distillation is part of
your plan.</li>
<li><strong>Attribution and naming</strong> obligations in your product.</li>
<li><strong>Whether the licence is revocable</strong>, and what happens to deployments if it is.</li>
</ul>
<p><strong>Open weights is not open source.</strong> Open source has a specific meaning about freedom
to use, modify and redistribute for any purpose, and most released model weights do not meet it. Using
the terms interchangeably is how procurement approves something on the wrong basis.</p>
'''),
 S('Choosing on Constraints Rather Than Ideology', '''
<p>The choice is usually argued as a philosophy and decided by four practical constraints.</p>
<p><strong>Where the data may go.</strong> If it cannot leave your infrastructure or your jurisdiction,
that settles it before capability enters the discussion — and it is the most common genuine reason to
self-host.</p>
<p><strong>Whether the model may change underneath you.</strong> A hosted model is updated by its
provider; that is an advantage for capability and a problem for reproducibility. If you need the same
input to give the same output a year from now, you need a version you control.</p>
<p><strong>What you can operate.</strong> Self-hosting is a standing commitment — serving, capacity for
peaks, monitoring, and someone on call. Below a certain volume an API is cheaper once that is costed
honestly.</p>
<p><strong>How close to the frontier the task needs to be.</strong> For many production tasks the gap
between tiers is irrelevant; for the hardest reasoning work it is decisive.</p>
<p>The common answer in practice is <strong>both</strong>: a hosted frontier model for the hard,
low-volume path and a smaller self-hosted or cheaper model for the high-volume routine one.
<strong>Treating it as a single binary decision is what produces the wrong answer for most of the
traffic.</strong></p>
''')]),

'ai-atlas/concepts/ai-evals-benchmarks': dict(sources=[], sections=[
 S('Building an Eval Set That Is Worth Trusting', '''
<p>A private eval set on your own task is worth more than every public benchmark combined, and
building one is less work than it sounds.</p>
<p><strong>Start with fifty real examples.</strong> Drawn from actual usage, not invented, and
including the awkward ones — the ambiguous request, the badly-typed input, the case with no good
answer. A set of clean examples measures a situation you do not have.</p>
<p><strong>Include known failures deliberately.</strong> Every time something goes wrong in production,
that example joins the set. This is what makes an eval set improve over time rather than decay.</p>
<p><strong>Write the expected outcome, not the expected wording.</strong> For most tasks there are many
acceptable answers, so define what must be true of a good response rather than fixing its text.</p>
<p><strong>Keep it private and keep it out of prompts.</strong> An eval set that leaks into training
data or into a system prompt stops measuring anything.</p>
<p><strong>And version it.</strong> When the set changes, the scores are not comparable to last
month's — which is the most common way a team convinces itself a model got better.</p>
'''),
 S('What to Measure Besides Whether It Was Right', '''
<p>Accuracy is one dimension and rarely the one that determines whether a feature survives contact
with users.</p>
<p><strong>Consistency.</strong> Run the same input several times. A model that is right on average
and varies wildly is unusable in a workflow where someone expects the same answer twice.</p>
<p><strong>Failure mode.</strong> When it is wrong, is it obviously wrong or plausibly wrong? A system
that fails visibly is safer than one with a better score that fails convincingly — the same argument
that governs the choice between model sizes.</p>
<p><strong>Refusal behaviour</strong> at both ends: refusing things it should do is as damaging as
attempting things it should not.</p>
<p><strong>Latency distribution, not the average.</strong> The slow tail is what users experience as
broken.</p>
<p><strong>Cost per successful outcome</strong>, which is the only cost figure that compares options
fairly — a cheaper model needing two attempts is not cheaper.</p>
<p><strong>And drift.</strong> Re-run the set on a schedule against a hosted model, because it changes
without notifying you, and the first sign is usually a user complaint rather than a metric.</p>
''')]),

'codex/seo/ai-search/zero-click-search': dict(sources=[GSC], sections=[
 S('Measuring a Channel That Stopped Sending Clicks', '''
<p>The reporting problem is structural: impressions rise, clicks do not, and the standard metrics say
the channel is failing when it may be working differently.</p>
<p>What to change in how you read the data:</p>
<p><strong>Stop using click-through rate as a health measure on informational queries.</strong> A
falling CTR on a query whose answer is now shown in the results is expected, not a defect, and
optimising the title to recover it is usually wasted effort.</p>
<p><strong>Segment queries by type.</strong> Informational, navigational and transactional behave
completely differently under zero-click, and a blended CTR conceals that transactional performance may
be entirely unchanged.</p>
<p><strong>Watch branded search volume and direct traffic</strong> as the indirect signal that
visibility without clicks is still doing something.</p>
<p><strong>Track position and impressions on the queries that matter commercially</strong>, and accept
impressions as a partial outcome on the rest.</p>
<p><strong>And separate what you can influence from what you cannot.</strong> A query answered
completely in the results is not winnable, and a strategy that keeps spending on it is spending against
the platform rather than the competition.</p>
'''),
 S('Where the Clicks Still Are', '''
<p>Zero-click is uneven rather than universal, and the response is to move effort toward the queries
that still convert into visits.</p>
<p><strong>Queries with no short answer</strong> — comparisons, decisions with trade-offs, anything
where the useful response is a judgement rather than a fact.</p>
<p><strong>Queries needing a tool</strong>: calculators, configurators, checkers. The answer surface can
describe the calculation; it cannot do it with the user's numbers.</p>
<p><strong>Transactional intent</strong>, where the user has to arrive somewhere to complete the
action.</p>
<p><strong>Queries where currency matters</strong> and the visible answer may be stale — pricing,
availability, regulation, anything dated.</p>
<p><strong>And anything requiring trust in a source</strong>, where a professional reader wants to see
who says it before acting on it.</p>
<p>The strategic move is not to fight for clicks on answered questions. It is to <strong>shift the
content mix toward questions that cannot be answered in a box</strong>, and to accept presence without
a visit as a legitimate outcome on the rest — while being honest that a business model funded by
pageviews on informational content is under genuine pressure, and no optimisation resolves that.</p>
''')]),

'ai-atlas/concepts/running-ai-locally': dict(sources=[], sections=[
 S('What the Hardware Actually Decides', '''
<p>The constraint on running a model locally is memory before it is speed, and the arithmetic is
simple enough to do before buying anything.</p>
<p><strong>A model needs roughly its parameter count in memory, scaled by the precision of its
weights.</strong> Full precision needs about two bytes per parameter; common quantisations bring that
to roughly one byte, or a half, or less. So the same model can need several times more or less memory
depending only on how it was compressed.</p>
<p><strong>Then add the context.</strong> The working memory for the conversation grows with how much
text is in play, and a long context can require as much again as the weights.</p>
<p><strong>Unified memory changes the calculation.</strong> On machines where the processor and
graphics share one pool, the usable ceiling is much higher than a discrete graphics card of similar
price, which is why some laptops run models that desktops cannot.</p>
<p>The practical sequence: <strong>work out your memory ceiling, subtract what the operating system
needs, and that determines the size and quantisation you can run.</strong> Everything else is a
consequence of that number.</p>
'''),
 S('The Honest Trade, Stated Plainly', '''
<p>Local models are frequently recommended for the wrong reason and dismissed for the wrong reason.</p>
<p><strong>The genuine advantages:</strong> data never leaves the machine, which for confidential or
regulated material can be the entire argument; no per-token cost, so high-volume repetitive work is
effectively free once the hardware exists; it works without a connection; and the model does not change
underneath you.</p>
<p><strong>The genuine costs:</strong> a capability gap against frontier hosted models that is real
and, for hard reasoning tasks, large; slower generation on consumer hardware; setup and maintenance
that is a hobby for some people and an obstacle for most; and quantisation degrading quality in ways
that are not visible until a specific task exposes them.</p>
<p><strong>Where it clearly wins:</strong> sensitive documents, bulk repetitive processing,
experimentation without a bill, offline use, and learning how these systems behave.</p>
<p><strong>Where it clearly does not:</strong> anything needing the current frontier of capability,
anything where your time is worth more than the token cost, and any production system where somebody
other than you depends on it staying up.</p>
<p><strong>Most people who try it settle on both</strong>, and that is the correct answer rather than a
failure to commit.</p>
''')]),

'ai-atlas/concepts/ai-regulation': dict(sources=[EUAI, EUC], sections=[
 S('The Timeline Moved in 2026, and Only Part of It', '''
<p>The EU AI Act's high-risk deadline was widely expected in August 2026 and did not arrive. Anyone
working from a plan written before mid-2026 is working from the wrong dates.</p>
<p><strong>Regulation (EU) 2026/1744 — the Digital Omnibus on AI</strong> — was adopted by Parliament
on <strong>16 June 2026</strong>, approved by Council on <strong>29 June</strong>, published in the
Official Journal on <strong>24 July</strong> and entered into force on <strong>27 July 2026</strong>,
six days before the original deadline.</p>
<table>
<tr><th>Obligation</th><th>Position</th></tr>
<tr><td>Prohibited practices, AI literacy</td><td><strong>In force since 2 February 2025.</strong> Not deferred</td></tr>
<tr><td>GPAI model obligations</td><td><strong>In force since 2 August 2025.</strong> Not deferred. Models on the market before that date must comply by <strong>2 August 2027</strong></td></tr>
<tr><td><strong>Article 50 transparency</strong></td><td><strong>Applied 2 August 2026 as scheduled.</strong> Catches chatbots and synthetic content</td></tr>
<tr><td>High-risk, Annex III standalone</td><td>Deferred to <strong>2 December 2027</strong> — hiring, credit scoring, education, critical infrastructure</td></tr>
<tr><td>High-risk, Annex I embedded</td><td>Deferred to <strong>2 August 2028</strong> — medical devices, machinery, toys</td></tr>
<tr><td>National regulatory sandboxes</td><td>Deferred to <strong>2 August 2027</strong></td></tr>
</table>
<p><strong>Neither high-risk date is conditional on further decisions</strong> — the earlier mechanism
tying them to the publication of standards was dropped from the final text. Penalties reach
<strong>&euro;35 million or 7% of global turnover</strong>.</p>
'''),
 S('Working Out Which Role You Are In', '''
<p>The Act allocates obligations by role, and the same organisation can hold several. Establishing
which you are in is the first compliance task and the one most often skipped.</p>
<p><strong>Provider</strong> — you develop an AI system or model and place it on the market under your
name. The heaviest obligations.</p>
<p><strong>Deployer</strong> — you use an AI system in a professional capacity. Lighter, and not
nothing: human oversight, using it as intended, and in several cases informing the people affected.</p>
<p><strong>The trap:</strong> a deployer can <em>become</em> a provider by putting their own name on a
system, substantially modifying it, or using it for a purpose the original provider did not intend. A
company fine-tuning a model and shipping it as a feature has probably crossed that line.</p>
<p><strong>Extraterritorial reach is wide.</strong> The Act applies where the output is used in the
Union, regardless of where you are established — so an Indian company serving European users is in
scope, and a plan that treats this as a European problem is mistaken.</p>
''' + '<p><strong>Two practical notes.</strong> Free and open-source GPAI models are exempt from most '
'transparency and documentation duties but must still comply with copyright rules and publish a '
'training-data summary — and if a model crosses the <strong>systemic-risk threshold of 10<sup>25</sup> '
'FLOPs</strong>, all obligations apply regardless of licence. And <strong>high-risk documentation '
'describes design decisions being taken now</strong>: reconstructing it in 2027 from systems already '
'in production costs several times more than recording it as you go, which is the argument for not '
'treating the deferral as a reason to stop.</p>')]),

'codex/seo/local/local-seo-fundamentals': dict(sources=[GBP], sections=[
 S('A First-Ninety-Days Order of Work', '''
<p>Local SEO advice is usually a list of everything. The order matters more than the completeness,
because the first two items produce most of the movement.</p>
<p><strong>Weeks one to two — the profile.</strong> Claim and verify it. Get the primary category right,
which is the highest-leverage single setting there is. Complete every field. Add real photographs.
Nothing else you do will compensate for this being wrong.</p>
<p><strong>Weeks three to four — reviews.</strong> Build the habit of asking at the moment of
satisfaction, set up the direct link, and start responding to everything. This is the slowest-moving
and most durable factor, which is why it has to start early.</p>
<p><strong>Weeks five to eight — the website.</strong> Location and service pages with real local
content, consistent contact details, and local business structured data.</p>
<p><strong>Weeks nine to twelve — citations and links.</strong> Fix the aggregators and the
industry-specific directories. Pursue genuinely local links: suppliers, local press, sponsorships,
trade bodies.</p>
<p><strong>Then maintain.</strong> The profile changes without you, reviews accumulate, and competitors
move — which is the part treated as a project and behaving like a channel.</p>
'''),
 S('What Local SEO Cannot Do For You', '''
<p>Two limits are structural, and knowing them prevents a great deal of wasted spend.</p>
<p><strong>Proximity.</strong> You will not appear in the map pack far from your address, however well
optimised. A business with one location has a catchment, and no amount of content extends it. This is
the single most common source of disappointment, and the honest answers are a second location, paid
search for the outlying areas, or accepting the catchment.</p>
<p><strong>Category reality.</strong> A business whose category is not what people search for will not
be found by optimising the wrong category harder.</p>
<p>And the honest scoping question: <strong>local SEO is for businesses customers travel to, or that
travel to customers.</strong> A national e-commerce business without a physical presence, a fully
remote service, an online-only brand — these are not local SEO problems, and effort spent on a Business
Profile they do not qualify for is effort not spent on the thing that would work.</p>
<p>Measure it on <strong>calls, direction requests and form enquiries by area</strong>. Rankings are a
means; those are the outcome, and they are the only numbers that survive a conversation about whether
any of this paid for itself.</p>
''')]),
}

ANCHORS = ['</div>\n    <aside class="guide-sidebar">',
           '\n\n    </main>\n    <aside class="art-sidebar">']
_TPL = io.open('_build/codex_style.txt', encoding='utf-8').read()
SRCS_CSS = '\n' + _TPL[_TPL.index('.srcs{'):_TPL.index('.srcs a{word-break:break-word}') + len('.srcs a{word-break:break-word}')]
assert '.srcs{' in SRCS_CSS and '</style>' not in SRCS_CSS
MD = re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')

done = 0
for path, cfg in PAGES.items():
    f = path + '/index.html'
    assert os.path.exists(f), 'missing ' + f
    src = io.open(f, encoding='utf-8').read()
    if cfg['sections'][0][0] in src:
        print('  = already expanded: ' + path); continue
    add = ''.join('<h2>%s</h2>\n%s\n' % (t, c) for t, c in cfg['sections'])
    add += sources_block(cfg['sources'])
    stray = MD.findall(re.sub(r'<[^>]+>', ' ', add))
    assert not stray, '%s: markdown in the addition: %s' % (f, stray[:3])
    found = [a for a in ANCHORS if src.count(a) == 1]
    assert len(found) == 1, '%s: matched %d anchors' % (f, len(found))
    i = src.find(found[0])
    out = src[:i] + add + src[i:]
    assert len(out) == len(src) + len(add), 'length delta wrong'
    for tag in ('<div', '</div>', '<table', '</table>', '<ul', '</ul>', '<ol', '</ol>'):
        assert out.count(tag) == src.count(tag) + add.count(tag), '%s: %s moved' % (f, tag)
    assert len(re.findall(r'<h1[\s>]', out)) == 1
    assert out.count('</html>') == 1 and out.count('</body>') == 1
    if cfg['sources'] and '.srcs{' not in out:
        assert out.count('</style>') == 1, f + ': %d style blocks' % out.count('</style>')
        before = len(out)
        out = out.replace('</style>', SRCS_CSS + '\n</style>', 1)
        assert len(out) == before + len(SRCS_CSS) + 1
    if cfg['sources']:
        assert '.srcs{' in out, f + ': sources block with no CSS'
    io.open(f, 'w', encoding='utf-8').write(out)
    done += 1
    print('  ✅ %-50s +%d words, %d sources' % (path[:50],
          len(re.sub(r'<[^>]+>', ' ', add).split()), len(cfg['sources'])))
print('\n%d pages expanded' % done)
