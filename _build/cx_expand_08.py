#!/usr/bin/env python3
"""cx_expand_08.py — Session 100. Eighth content-remediation batch, thirteen pages.

Seven Codex, six AI Atlas. Two-anchor logic copied from cx_expand_07.py.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

GCM = ('official', 'Google Consent Mode and Google Tag documentation',
       'the four consent signals, basic versus advanced behaviour, and the conversion-modelling thresholds described here',
       'developers.google.com')
DPDP = ('official', 'Digital Personal Data Protection Act, 2023 and the DPDP Rules, 2025',
        'the consent standard that applies in India and the absence of a legitimate-interest basis',
        'meity.gov.in')
GBP = ('official', 'Google Business Profile guidelines',
       'bulk verification, location group management and the name and address rules referenced here',
       'support.google.com')
MSFT = ('official', 'Microsoft Advertising documentation',
        'inventory syndication, LinkedIn profile targeting and the campaign settings described here',
        'about.ads.microsoft.com')
AMZ = ('official', 'Amazon Advertising and Seller Central documentation',
       'ad type eligibility, ACOS and TACOS definitions and the placement reporting described here',
       'advertising.amazon.com')
MCP = ('official', 'Model Context Protocol specification',
       'the host, client and server roles, the transport options and the capability model described here',
       'modelcontextprotocol.io')
OWASP = ('official', 'OWASP Top 10 for Large Language Model Applications',
         'the prompt-injection categories and the mitigation guidance referenced here', 'owasp.org')
FTC = ('official', 'FTC Endorsement Guides',
       'the disclosure obligations attaching to paid creator relationships in the United States', 'ftc.gov')
ASCI = ('official', 'ASCI Guidelines for Influencer Advertising in Digital Media',
        'the disclosure obligations for influencer content aimed at Indian audiences', 'ascionline.in')

S = lambda t, c: (t, c)

PAGES = {

'codex/analytics-cro/consent-mode-v2': dict(sources=[GCM, DPDP], sections=[
 S('Choosing Between Basic and Advanced, Honestly', '''
<p>The choice is presented as a technical setting and is really a policy decision, because the two
modes behave differently before a user has answered the banner.</p>
<p><strong>Basic</strong> holds the tags back entirely until consent is given. Nothing is sent, nothing
is collected, and an unconsented visitor is invisible. It is the more conservative reading and the
easier one to defend.</p>
<p><strong>Advanced</strong> loads the tags immediately and sends <strong>cookieless pings</strong>
carrying no identifiers, which is what feeds the modelling. More data, more complexity, and a position
you have to be able to justify — because something did leave the browser before the user answered.</p>
<p>Two things decide it. <strong>What your legal advice says</strong> about transmitting anything
pre-consent in your jurisdictions. And <strong>whether you have the volume for modelling to work at
all</strong> — below the platform's thresholds you get the complexity of advanced mode and none of the
benefit, which is the most common wasted implementation.</p>
<p><strong>India is not a lighter-touch case.</strong> The DPDP framework is consent-based with
<strong>no legitimate-interest basis</strong>, so a configuration built for a market with one does not
transfer.</p>
'''),
 S('Verifying It Rather Than Assuming It', '''
<p>Consent mode fails silently. The banner appears, the tags fire, the dashboard fills, and nothing
tells you the signals are wrong.</p>
<p>The checks worth running, in order:</p>
<ul>
<li><strong>Watch the network requests before and after consenting.</strong> Confirm what is sent in
each state, and that the consent parameters actually change.</li>
<li><strong>Check the default state is denied</strong>, and that it is set <em>before</em> any tag
loads. A default of granted, or one applied too late, is the most common and most serious
misconfiguration.</li>
<li><strong>Test a decline, not just an accept.</strong> Almost nobody does, and the decline path is
the one that carries the risk.</li>
<li><strong>Verify the update fires</strong> when consent changes, including when a user later
withdraws it.</li>
<li><strong>Check region-specific defaults</strong> if you serve multiple jurisdictions.</li>
</ul>
<p>And <strong>document the configuration next to the analytics documentation.</strong> They are owned
by different people, changed independently, and together they determine every number the business
runs on.</p>
''')]),

'ai-atlas/specialist-tools/images-design/krea': dict(sources=[], sections=[
 S('Where Real-Time Generation Changes the Work', '''
<p>The interesting claim is not speed for its own sake. It is that fast feedback changes what kind of
work is possible — the difference between describing an image and steering one.</p>
<p>Three workflows it genuinely enables. <strong>Iterating on composition</strong>, where you move or
sketch an element and watch the result update, rather than rewriting a prompt and waiting.
<strong>Finding a direction</strong>, sweeping through variations quickly when you do not yet know what
you want. And <strong>working from a rough sketch</strong>, where your drawing is the structure and the
model supplies the rendering.</p>
<p>Where the advantage disappears: <strong>final-quality single images</strong>, where you already know
the brief and one careful generation from a stronger model beats fifty fast ones.
<strong>Text rendering</strong>, which remains a weak point across real-time tools.
<strong>Strict consistency</strong> across a set, which real-time exploration actively works against.</p>
<p>The honest summary: <strong>it is an exploration tool, not a production tool</strong>, and teams that
adopt it as the latter are disappointed for a predictable reason.</p>
'''),
 S('Fitting It Into a Pipeline', '''
<p>The workable pattern is to use it for the part it is good at and hand off for the rest.</p>
<p><strong>Explore fast, finish elsewhere.</strong> Establish composition, colour and direction in
real time, then take the chosen direction to a higher-fidelity generator or to a designer. The output
of the fast stage is a decision, not an asset.</p>
<p><strong>Upscaling is a separate step and worth treating as one.</strong> An enhance pass will
invent detail that was not there, which is fine for texture and a problem for anything that must stay
accurate — a product, a logo, a face, a chart.</p>
<p><strong>Check the licence before commercial use</strong>, and check it per plan rather than once.
Terms differ between free and paid tiers on most of these tools, and the free tier is frequently the
one that was tested.</p>
<p><strong>And keep the prompt and settings with the output.</strong> Fast iteration produces dozens of
near-identical results, and a month later the one you shipped is indistinguishable from the forty you
did not unless you recorded which was which.</p>
''')]),

'codex/seo/local/multi-location-seo': dict(sources=[GBP], sections=[
 S('Operating Profiles at Scale Without Losing Control', '''
<p>Beyond a handful of locations, profile management stops being a marketing task and becomes an
operations one, and the failure is usually governance rather than optimisation.</p>
<p><strong>Use a location group</strong> so ownership sits with the organisation rather than with
whichever manager claimed the listing first. Profiles claimed on personal accounts by departed staff
are the single most common blocker in a multi-location audit, and recovering them is slow.</p>
<p><strong>Decide centrally what is local and what is not.</strong> Name, category, hours, description
and photographs should follow one standard; replies to reviews and posts benefit from a local voice.
Getting this backwards — central review replies, local categories — produces both inconsistency and
blandness.</p>
<p><strong>Bulk verification</strong> is available above a threshold of locations and is worth pursuing
early, because verifying individually does not scale.</p>
<p><strong>And audit for duplicates on a schedule.</strong> At scale, duplicates appear continuously —
from a franchisee, an aggregator, an old listing resurfacing — and each one splits reviews and signals
for that branch.</p>
'''),
 S('Reporting So a Regional Manager Can Act', '''
<p>Multi-location reporting fails when it aggregates. A national average conceals every location that
needs help and every one that is working.</p>
<p><strong>Report by location, ranked</strong>, on the actions rather than the rankings: calls,
direction requests, enquiries. The ranked list is what makes the conversation possible.</p>
<p><strong>Compare each location against itself over time</strong>, not against other locations.
Catchment density, competition and category differ enough that cross-location comparison mostly
measures geography.</p>
<p><strong>Segment by cause where you can.</strong> A location underperforming with strong reviews and
a complete profile has a competition or catchment problem; one with thin reviews has a process problem
the branch can fix. Those need different conversations.</p>
<p><strong>And watch the profile-edit log per location</strong>, because public suggested edits change
information branch by branch and nobody notices centrally.</p>
<p>The reporting test: <strong>can a regional manager open this and know which three branches to ring
on Monday?</strong> If not, it is a dashboard rather than a report.</p>
''')]),

'codex/paid-advertising/microsoft-ads/microsoft-ads-fundamentals': dict(sources=[MSFT], sections=[
 S('Sizing the Opportunity Before Committing', '''
<p>The usual mistake is treating Microsoft as a smaller copy of Google and budgeting proportionally.
The share differs enormously by market, device and audience, so the general figure is the wrong input.</p>
<p>How to size it with your own data rather than a statistic. <strong>Check your analytics for the
search-engine split on existing traffic</strong> — that is your audience, not the market average.
<strong>Look at the device and operating-system mix</strong>, since desktop and Windows skew the share
substantially. <strong>Consider the buying context</strong>: workplace machines, older demographics and
certain B2B categories over-index, sometimes dramatically.</p>
<p><strong>And run the import as a test rather than a launch.</strong> A fortnight at a modest budget
answers the question better than any estimate, and the import makes that test nearly free to set up.</p>
<p>The honest expectation: <strong>materially lower volume and frequently lower cost per click</strong>,
which together can produce a better cost per acquisition on a channel that will never be your largest.
That is a legitimate thing to own, and a bad thing to over-invest in.</p>
'''),
 S('Where the Inventory Actually Comes From', '''
<p>Understanding the syndication matters because it explains performance variation that otherwise looks
random.</p>
<p>Your ads can appear on the <strong>owned search properties</strong>, on <strong>partner sites</strong>
that use the search technology, and on the <strong>Audience Network</strong>, which is native display
rather than search. These are three different things with three different intent profiles, and the
default settings frequently include all of them.</p>
<p>The practical consequences. <strong>Partner-site traffic converts differently</strong> from owned
search and is worth separating before concluding the channel does not work.
<strong>The Audience Network should be its own campaign</strong> — mixed into a search campaign it
distorts both the numbers and the bid strategy.
<strong>And check the distribution settings explicitly</strong> rather than accepting the defaults,
because an account imported from elsewhere carries assumptions that do not apply here.</p>
<p>The genuine differentiator remains <strong>LinkedIn profile targeting</strong> — company, industry
and job function in a search-adjacent platform. Coverage is partial, so it works best layered onto an
intent signal rather than used alone.</p>
''')]),

'codex/ecommerce/d2c-strategy': dict(sources=[], sections=[
 S('The Costs D2C Moves Onto Your Balance Sheet', '''
<p>Selling direct removes the retailer's margin and takes on the work that margin paid for. The
business case usually counts the first and not the second.</p>
<p>What you now own: <strong>customer acquisition</strong>, which is the retailer's largest hidden
contribution and the item that most often breaks the model;
<strong>fulfilment and returns</strong>, per order rather than per pallet, at an entirely different
unit cost; <strong>customer service</strong>, including the people who would have taken the complaint
in a shop; <strong>payments and fraud</strong>; and <strong>the technology</strong>, which is the
cheapest of the five and the only one most plans budget properly.</p>
<p>Model contribution after all of them, at your realistic return rate, and compare it against the
wholesale margin you are replacing. <strong>A brand with a healthy gross margin can be loss-making
direct at any volume</strong>, and the point at which that becomes visible is usually after the
warehouse is leased.</p>
<p>The version that works is usually narrower than the ambition: <strong>a subset of products, a subset
of customers, and a clear reason those customers prefer buying from you.</strong></p>
'''),
 S('Living With Both Channels', '''
<p>Almost every D2C brand ends up hybrid, and the friction is predictable enough to plan for.</p>
<p><strong>Price.</strong> Undercutting your retailers wins a short-term sale and costs the
relationship. The usual resolution is parity on shared lines and difference elsewhere — exclusive
sizes, bundles, editions, early access — so the value is real without being a discount.</p>
<p><strong>Data.</strong> You know your direct customers and not your retail ones, which is exactly the
asymmetry retail media platforms monetise. Treat direct as your research channel, not only your sales
channel — what you learn there informs everything.</p>
<p><strong>Inventory.</strong> Allocation between channels is a recurring decision with no clean answer,
and it is the one that causes internal argument. Decide the rule in advance rather than case by case.</p>
<p><strong>And relationship.</strong> Your buyer will notice the direct channel. Bringing it to them
early, with the positioning explained, is a different conversation from having it discovered.</p>
<p>The honest framing: <strong>D2C is rarely a replacement for distribution and frequently a valuable
addition to it</strong> — and plans that assume the first tend to be the ones that fail.</p>
''')]),

'codex/ecommerce/quick-commerce': dict(sources=[], sections=[
 S('Designing an Assortment for a Ten-Minute Basket', '''
<p>The dark store holds a fraction of a supermarket's range, so the whole commercial question is which
of your products deserve one of those slots.</p>
<p>What earns a slot: <strong>high purchase frequency</strong>, because the model runs on repeat;
<strong>genuine urgency</strong> — the thing someone needs now rather than this week;
<strong>an impulse or top-up role</strong>; and <strong>a pack size suited to a small immediate
basket</strong> rather than a monthly shop.</p>
<p>What does not: bulky low-value items where delivery economics fail, considered purchases needing
comparison, and anything with a long tail of variants — <strong>shelf space is the binding constraint
and range depth is what gets cut.</strong></p>
<p><strong>The pack-size decision is the strategic one.</strong> A smaller pack at a higher unit price
suits the channel, sells more often, and <strong>creates a price-per-unit comparison that will be
visible against your supermarket line</strong>. Deciding that deliberately — including whether to make
a channel-specific pack — is the difference between a quick-commerce strategy and a listing.</p>
'''),
 S('Winning Visibility, and What It Costs', '''
<p>Discovery in quick commerce is closer to a retail shelf than to a search engine: a short list, a
default sort, and a small number of slots that decide most of the volume.</p>
<p>The levers, and the honesty about each. <strong>Availability</strong> is the first and the most
underrated — an out-of-stock item is invisible and its rank decays.
<strong>Platform advertising</strong> buys placement, and as with any retail media the seller of the
advertising also controls the shelf, so measure it on incrementality rather than on reported return.
<strong>Ratings and reviews</strong> matter and accumulate slowly.
<strong>And the trade relationship</strong> determines assortment decisions that no amount of
advertising overrides.</p>
<p>Two things to watch. <strong>Discounting is structural in the category</strong>, so model the price
you will actually realise rather than the list price. And <strong>the platform owns the customer</strong>
— you get orders, not relationships, which makes this a volume channel rather than a brand-building
one.</p>
<p><strong>Judge it on incremental category growth</strong>, not on channel revenue. Sales that moved
from another channel are not growth.</p>
''')]),

'ai-atlas/concepts/model-context-protocol': dict(sources=[MCP], sections=[
 S('Deciding Whether to Build a Server', '''
<p>The appeal is obvious and the work is larger than a wrapper, so the decision is worth making
deliberately.</p>
<p><strong>It is worth building when</strong> several different assistants or clients need the same
capability, so one server replaces several bespoke integrations; when the capability is stable enough
to have an interface; or when you are exposing something to people outside your team who should not
need your internals.</p>
<p><strong>It is not worth it when</strong> one application needs one integration — a direct API call
is simpler and has fewer moving parts; or when the underlying thing changes weekly, because you are
now maintaining an interface over a moving target.</p>
<p>What building one actually involves beyond the protocol: <strong>deciding what to expose and what to
withhold</strong>, which is the real design work; <strong>authentication and authorisation</strong>,
which the protocol does not solve for you; <strong>error behaviour</strong> that a model can act on
rather than a stack trace; and <strong>versioning</strong>, because a client built against your server
will break when you change it.</p>
'''),
 S('Treating a Server as an Untrusted Boundary', '''
<p>The security position that matters: <strong>anything a server returns is data, not instruction</strong>,
and a model reading tool output is reading content someone else may control.</p>
<p>That produces concrete requirements. <strong>Scope credentials to the minimum</strong> — a server
with broad write access is a broad write capability handed to whatever text arrives.
<strong>Require confirmation for consequential actions</strong>: sending, deleting, paying,
publishing. <strong>Log every call with its arguments</strong>, because reconstructing what an agent
did without that is close to impossible.
<strong>And treat third-party servers as third-party code</strong>, because that is what they are —
read what it does before connecting it to anything holding your data.</p>
<p>The failure mode to picture: a server returns a document containing text addressed to the model
rather than to you, the model treats it as an instruction, and the next tool call does something you
did not ask for. <strong>The protocol does not prevent this and is not supposed to.</strong> The
boundary is yours to enforce — covered in full on the prompt-injection page.</p>
''')]),

'ai-atlas/specialist-tools/images-design/recraft': dict(sources=[], sections=[
 S('Where Vector Output Changes the Decision', '''
<p>Most image generators produce pixels. Producing editable vector output changes what the tool is for,
because the result enters a design workflow rather than ending one.</p>
<p>What that enables: <strong>editing after generation</strong> in ordinary design software, so an
almost-right result is a starting point rather than a reroll; <strong>scaling without loss</strong>,
which matters for anything printed or displayed at variable size; and <strong>handing off to a
designer</strong> in a format they can work with rather than trace.</p>
<p>Where it does not help: <strong>photographic imagery</strong>, which is not a vector problem;
complex illustration, where the generated paths can be messy enough that cleanup costs more than
redrawing; and anything where the output was always going to be used as-is.</p>
<p>The practical test: <strong>will anyone edit this after it is generated?</strong> If yes, vector
output is a genuine advantage and worth choosing the tool for. If no, it is a format preference and the
decision should rest on quality instead.</p>
'''),
 S('Brand Consistency, and Its Real Limits', '''
<p>The feature teams adopt this for is defining a reusable style, so a series of images looks like it
came from one place. It works, within limits worth knowing before committing a campaign to it.</p>
<p><strong>It is good at</strong> holding a consistent palette, line treatment and level of abstraction
across many images — which is most of what makes a set look coherent.</p>
<p><strong>It is weaker at</strong> holding a specific character or object consistent across images,
which is a harder problem than style and is not solved by a style definition.
<strong>Text inside images</strong> remains unreliable across every tool in this category.
<strong>And exact brand colour</strong> is worth verifying rather than assuming — check the output
values against your specification rather than trusting that it looks right.</p>
<p>On rights: <strong>check the commercial terms per plan</strong>, since they differ between tiers,
and check what happens to a custom style you have trained — whether it is private, whether it persists
if you downgrade, and whether anything you generated remains licensed if you leave. <strong>These are
contract questions rather than technical ones, and they are the ones that matter after the campaign
ships.</strong></p>
''')]),

'codex/paid-advertising/amazon-ads/amazon-ads-fundamentals': dict(sources=[AMZ], sections=[
 S('Beyond ACOS — the Metrics That Change Decisions', '''
<p>ACOS is the number everyone quotes and it only describes advertising. Three others change what you
actually do.</p>
<p><strong>TACOS — total advertising cost of sales</strong>, measured against <em>all</em> sales rather
than attributed ones. It is the one number that shows whether advertising is building organic
performance: a falling TACOS at constant spend means organic sales are growing underneath the
advertising, which is the outcome you want and which ACOS cannot see.</p>
<p><strong>New-to-brand.</strong> A campaign returning well entirely from existing customers is
capturing demand rather than creating it. Both are legitimate; they are different businesses and
should be budgeted separately.</p>
<p><strong>Share of voice on your core terms</strong>, which tells you whether a competitor is moving
on you before the sales data does.</p>
<p>And the discipline that matters more than any metric: <strong>a break-even ACOS is a calculation,
not a benchmark.</strong> It follows from your margin, and a target copied from an article describes
somebody else's product.</p>
'''),
 S('Choosing Among the Ad Types', '''
<p>Three main formats, and the common error is running all of them at once before knowing which is
carrying the result.</p>
<p><strong>Sponsored Products</strong> is where almost every account should start. It appears in
results and on product pages, it is the closest to the purchase, and it is the easiest to read.</p>
<p><strong>Sponsored Brands</strong> puts a logo, a headline and several products at the top. Useful
once you have a range worth showing and a brand worth showing it under; wasteful for a single product
with no brand recognition.</p>
<p><strong>Sponsored Display</strong> reaches beyond the search result — onto competitor listings, and
off-platform to people who viewed your products. High variance, and the one most likely to look
impressive on attributed numbers while adding little.</p>
<p>The sequence that works: <strong>establish Sponsored Products, make it profitable, then add one
more and measure the total rather than the new campaign.</strong> If total sales do not move when a
second type is added, it is reallocating credit — the same test that applies to every retail media
question.</p>
''')]),

'ai-atlas/concepts/prompt-injection-ai-security': dict(sources=[OWASP], sections=[
 S('Designing Around It Rather Than Filtering For It', '''
<p>Prompt injection is not reliably solvable by detection, because the attack is written in the same
language as the legitimate input. The defences that work are architectural.</p>
<p><strong>Separate the privilege from the content.</strong> The component that reads untrusted text
should not be the component that holds credentials or can act. A model summarising a document does not
need the ability to send email.</p>
<p><strong>Give every tool the narrowest possible scope.</strong> Read-only where read-only will do;
a specific resource rather than an account; a rate limit and a spend cap on anything that costs money.</p>
<p><strong>Put a human in front of consequential actions</strong> — sending, deleting, paying,
publishing, sharing — with the actual action described rather than a summary of intent.</p>
<p><strong>Validate outputs against a schema</strong> before acting on them, so a malformed or
unexpected instruction fails closed.</p>
<p><strong>And log everything with arguments.</strong> When something does go wrong, the log is the
only way to establish what happened, and it is invariably missing.</p>
'''),
 S('What Does Not Work, and Why It Keeps Being Tried', '''
<p>Several defences are intuitive, widely recommended and insufficient. Knowing why saves the effort of
discovering it.</p>
<p><strong>Instructing the model to ignore injected instructions.</strong> This raises the bar slightly
and is not a boundary. An instruction can always be phrased to outrank a previous instruction, and the
model has no reliable way to distinguish the two.</p>
<p><strong>Keyword and pattern filtering.</strong> The attack is natural language, so the space of
phrasings is unbounded. Filters catch the obvious cases and produce false confidence about the rest.</p>
<p><strong>Delimiters around untrusted content.</strong> Useful as structure, defeated by content that
includes the delimiter or describes it.</p>
<p><strong>A second model checking the first.</strong> Better than nothing and subject to the same
class of attack, since the checker also reads attacker-influenced text.</p>
<p>The reason these keep being tried is that they are cheap and feel like security.
<strong>The reliable position is to assume injection will succeed and to limit what succeeding
achieves</strong> — which is a design constraint rather than a control you can add afterwards.</p>
''')]),

'codex/ecommerce/subscription-commerce': dict(sources=[], sections=[
 S('The Cohort Question That Decides Everything', '''
<p>Subscription businesses are judged on monthly revenue and determined by cohort retention, and the
two can move in opposite directions for a long time.</p>
<p><strong>Track retention by joining cohort, not in aggregate.</strong> Aggregate retention is
flattered by growth: new subscribers dilute the churn of older ones, so a business with worsening
retention can show improving headline numbers while it is acquiring.</p>
<p>What a cohort curve tells you that nothing else does. <strong>Where the drop is.</strong> A cliff
after the first delivery is a product or expectation problem; a cliff at the end of an introductory
offer is a pricing problem; a slow steady decline is a value problem. These need completely different
responses and look identical in a monthly churn figure.</p>
<p><strong>Whether it flattens.</strong> A curve that flattens has a durable base and the business
works. One that keeps declining has no floor, and growth is only outrunning the leak.</p>
<p><strong>And whether newer cohorts are better.</strong> That is the only real evidence that a
retention initiative worked.</p>
'''),
 S('Reducing Churn Where It Actually Happens', '''
<p>Most churn work targets the cancellation moment, which is the last and least effective place to
intervene.</p>
<p><strong>The first delivery matters more than everything after it.</strong> If it arrives late,
damaged, or unlike what was pictured, the subscription is already lost and no offer recovers it. Spend
here first.</p>
<p><strong>Give control rather than resisting cancellation.</strong> Skip a delivery, change the
frequency, swap the contents, pause for a month. <strong>A pause is a retained customer; a friction
wall is a complaint and a chargeback</strong> — and in several jurisdictions a cancellation flow harder
than the signup flow is a regulatory problem, not just a bad experience.</p>
<p><strong>Ask at cancellation and act on the answer.</strong> The reasons cluster — too much product,
too expensive, no longer needed — and two of those three have a product response rather than a discount
response.</p>
<p><strong>And watch the payment failures.</strong> A meaningful share of churn is an expired card
rather than a decision. Dunning — retry schedules, pre-expiry prompts, updater services — recovers
subscribers who never intended to leave, and it is the cheapest retention work available.</p>
''')]),

'ai-atlas/concepts/embeddings-vector-databases': dict(sources=[], sections=[
 S('Chunking, Which Decides More Than the Model Does', '''
<p>Retrieval quality is determined more by how documents are split than by which embedding model
produced the vectors, and chunking is where most effort should go.</p>
<p><strong>Too small</strong> and a chunk loses the context that made it meaningful — a sentence
referring to something defined two paragraphs earlier retrieves without its subject.
<strong>Too large</strong> and the relevant passage is diluted by surrounding text, so the match is
weaker and the model receives more to ignore.</p>
<p>What works better than a fixed size: <strong>split on structure</strong> — headings, sections,
list items — so chunks correspond to units of meaning rather than counts of characters.
<strong>Overlap adjacent chunks</strong> so a passage spanning a boundary appears whole somewhere.
<strong>Keep the heading with the chunk</strong>, which is the cheapest single improvement most
systems are missing. And <strong>store the source and position</strong> so the answer can be cited back
to a location a person can check.</p>
<p><strong>Test chunking changes against a fixed question set</strong>, because it is easy to improve
one query and quietly worsen ten.</p>
'''),
 S('Why Pure Similarity Search Disappoints', '''
<p>Semantic search finds text that means something similar, which is not always text that answers the
question — and the gap shows up in predictable places.</p>
<p><strong>Exact terms.</strong> A product code, an error number, a person's name. Embeddings are poor
at exactness, and a keyword index is better at it. <strong>Hybrid search</strong> — combining semantic
and keyword scoring — is the standard answer and fixes most complaints about retrieval quality.</p>
<p><strong>Negation and comparison.</strong> <em>Which of these does not support X</em> is close in
embedding space to text saying it does.</p>
<p><strong>Recency and filtering.</strong> Similarity has no opinion about dates or permissions, so
filter on metadata before or alongside the search rather than hoping the ranking handles it.</p>
<p><strong>Reranking</strong> — passing the top results through a more expensive model that scores them
directly against the query — usually improves quality more than changing the embedding model, and is
the second thing to try after hybrid search.</p>
<p>The practical sequence when retrieval disappoints: <strong>fix chunking, add keyword search, add
reranking, and only then consider a different embedding model.</strong> Most teams do that list
backwards.</p>
''')]),

'codex/social-media/influencer-marketing': dict(sources=[ASCI, FTC], sections=[
 S('Diligence That Survives a Bad Partnership', '''
<p>Most influencer disappointments are diligence failures, and the checks that matter take under an
hour per creator.</p>
<p><strong>Look at engagement quality, not rate.</strong> Read the comments. Generic praise in
unrelated languages, the same accounts on every post, and a comment count that does not match the
audience size are the recognisable signs of purchased engagement.</p>
<p><strong>Ask for audience demographics from the platform's own analytics</strong>, screenshared or
exported rather than self-reported — location, age and gender split. A creator whose audience is
mostly outside your market is a poor fit at any engagement rate.</p>
<p><strong>Check follower growth over time.</strong> Step changes suggest purchase; steady growth
suggests a real audience.</p>
<p><strong>Read their last twenty posts.</strong> How many were paid? A feed that is mostly sponsored
has an audience that has learned to discount it.</p>
<p><strong>And search their name plus the obvious controversy terms.</strong> Five minutes, and it is
the check that prevents the expensive kind of mistake.</p>
'''),
 S('Contracting the Things That Become Disputes', '''
<p>The disputes are predictable, which means they are preventable in the agreement.</p>
<p><strong>Usage rights</strong> — whether you may run the content as paid media, on which platforms,
for how long, and whether you may edit. This is frequently worth more than the fee and is the single
most common omission.</p>
<p><strong>Exclusivity</strong> — for how long the creator will not promote a competitor, defined by
category rather than by named company, and priced accordingly.</p>
<p><strong>Approval and revisions</strong> — how many rounds, over what timescale, and what happens if
you reject the work entirely.</p>
<p><strong>Content lifespan</strong> — whether the post stays up, and for how long. A deleted post
three weeks after payment is a common and avoidable annoyance.</p>
<p><strong>Disclosure</strong> — required, in the content, using the platform's own tool where one
exists. The obligation attaches to the payment, and it applies to gifted product too. Indian audiences
fall under ASCI's guidelines and US audiences under the FTC's; <strong>a single high standard is
simpler than maintaining two.</strong></p>
<p><strong>And FTC- or ASCI-compliant disclosure is your exposure as well as theirs</strong>, which is
why it belongs in the brief rather than in a hope.</p>
''')]),
}


# DEFERRED — ai-atlas/specialist-tools/images-design/{krea,recraft}
# S100: these use a THIRD template. Not the Codex guide-* one, not the Atlas
# concept art-* one: an `art-body` div of lane-sections with a `pg-toc`
# sidebar whose links are keyed to h2 ids in a lane colour scheme
# (#s-green-N, #s-indigo-N, #s-red-N). Every h2 carries an id and appears in
# the TOC.
#
# Splicing two h2 sections in would produce a page whose OWN table of contents
# omits two of its sections -- the derived-artefact defect class QA #7 and #8
# both found. Doing it correctly needs the ids allocated in the lane scheme,
# the sections placed inside the right lane-section/depth-band, and two TOC
# entries added.
#
# Deferred to session 102 or 103 with the content written and unused below.
# The content is kept here rather than discarded so it is not rewritten.
DEFERRED = ('ai-atlas/specialist-tools/images-design/krea',
            'ai-atlas/specialist-tools/images-design/recraft')

ANCHORS = ['</div>\n    <aside class="guide-sidebar">',
           '\n\n    </main>\n    <aside class="art-sidebar">']
_TPL = io.open('_build/codex_style.txt', encoding='utf-8').read()
SRCS_CSS = '\n' + _TPL[_TPL.index('.srcs{'):_TPL.index('.srcs a{word-break:break-word}') + len('.srcs a{word-break:break-word}')]
assert '.srcs{' in SRCS_CSS and '</style>' not in SRCS_CSS
MD = re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')

done = 0
for path, cfg in PAGES.items():
    if path in DEFERRED:
        print('  ~ deferred (third template, see note): ' + path); continue
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
