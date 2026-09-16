#!/usr/bin/env python3
"""cx_expand_03.py — Session 93. Third content-remediation batch, twelve pages.

Same contract as batches one and two: two <h2> sections each, written as the
practical and failure layer the originals skipped; target 600+ content words;
typed sources only where a real primary source exists; no invented figures.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

MSFT = ('official', 'Microsoft Advertising documentation',
        'Audience Network placement behaviour, LinkedIn profile targeting and the campaign settings described here',
        'about.ads.microsoft.com')
XADS = ('official', 'X Ads Help Center',
        'the campaign objectives, ad formats and targeting options described here', 'business.x.com')
MRC = ('official', 'Media Rating Council viewability standards and IAB/MRC measurement guidelines',
       'the viewability thresholds and the invalid-traffic definitions this page relies on', 'mediaratingcouncil.org')
TAG = ('official', 'TAG (Trustworthy Accountability Group) certification programmes',
       'the supply-chain certification referenced for invalid traffic and brand safety', 'tagtoday.net')
GSC = ('official', 'Google Search Central documentation',
       'crawl budget, faceted navigation handling and the internal linking guidance referenced here',
       'developers.google.com')
SNAPA = ('official', 'Snapchat Ads Manager documentation',
         'objectives, formats, Lens publishing and the creative specifications described here', 'businesshelp.snapchat.com')
LOOK = ('official', 'Looker Studio help documentation',
        'connector behaviour, data blending limits and extract/refresh mechanics described here', 'support.google.com')
FTC = ('official', 'FTC Endorsement Guides',
       'the disclosure obligations attaching to affiliate relationships in the United States', 'ftc.gov')
ASCI = ('official', 'ASCI Guidelines for Influencer Advertising in Digital Media',
        'the disclosure obligations for affiliate content aimed at Indian audiences', 'ascionline.in')
MMP = ('official', 'Apple App Store and Google Play policy documentation on advertising identifiers',
       'the ATT consent requirement and the advertising ID behaviour that mobile attribution now works within',
       'developer.apple.com')

S = lambda t, c: (t, c)

PAGES = {

'codex/paid-advertising/microsoft-ads/microsoft-audience-network': dict(sources=[MSFT], sections=[
 S('Controlling Placement Quality', '''
<p>The Audience Network's recurring complaint is placement quality: the ads appear somewhere the
advertiser did not expect and performance data becomes hard to read. The controls exist and most
accounts never touch them.</p>
<p><strong>Website exclusions</strong> are the first lever. Run the placement report after the first
fortnight, sort by spend, and exclude anything that has spent meaningfully without converting. This is
maintenance, not a one-off, because the inventory pool changes.</p>
<p><strong>Separate the campaign from search.</strong> Audience Network can be enabled inside a search
campaign, which mixes two very different intent profiles into one set of numbers and one bid strategy.
Running it as its own campaign costs nothing and makes both readable.</p>
<p><strong>Bid adjustments by placement</strong> let you retain the network at a lower price rather
than switching it off entirely, which is usually the better trade for a channel that works at the
right CPC and not at the wrong one.</p>
<p>Judge it on <strong>incremental</strong> conversions rather than last-click. This is upper-funnel
inventory and last-click attribution will systematically undervalue it — the same way it undervalues
display everywhere.</p>
'''),
 S('The LinkedIn Signal, and Its Limits', '''
<p>The genuine differentiator is profile targeting derived from LinkedIn — company, industry and job
function — available in a self-serve search-adjacent platform rather than only inside LinkedIn's own
ad products. For B2B that is a real advantage and it is why the network is worth testing at all.</p>
<p>Three limits to plan around. <strong>Coverage is partial</strong>: the signal is available for the
share of users who can be matched, so a campaign restricted to profile targeting addresses a fraction
of the network's reach and will under-deliver against a naive forecast.
<strong>Company targeting is not account-based marketing</strong> — it is a broad firmographic filter,
not a named-account list with the precision that implies.
<strong>Job function is coarse</strong>, and mapping it onto your actual buying committee takes work
that a category label hides.</p>
<p>The practical approach is to <strong>layer profile targeting onto an intent signal</strong> —
remarketing, or a customer match list — rather than relying on it alone. Used as the sole targeting
input it behaves like broad display with a professional gloss. Used as a qualifier on people who have
already shown interest, it does something the other networks cannot.</p>
''')]),

'codex/paid-advertising/x-ads': dict(sources=[XADS], sections=[
 S('Building the Campaign So the Data Is Readable', '''
<p>X campaigns fail diagnosis more often than they fail outright, because the structure mixes signals
that should be separated.</p>
<p><strong>Split by targeting type, not by creative.</strong> Keyword, follower-lookalike, interest
and retargeting behave so differently on cost and intent that combining them into one ad group
produces an average that describes none of them. Separate them and the losing method is obvious in
days rather than weeks.</p>
<p><strong>Set a conversion window you can defend.</strong> The platform's default attribution is
generous, and a long post-view window on a high-reach platform will credit purchases that were
happening anyway. Shorten it, then compare against your own analytics rather than accepting the
platform's figure.</p>
<p><strong>Give creative a real rotation.</strong> Fatigue arrives quickly on a feed with high
refresh, and performance decay is frequently read as audience exhaustion when it is creative
exhaustion. Change the creative before concluding the audience is spent.</p>
'''),
 S('Brand Safety as an Operational Position', '''
<p>Advertiser caution about X is about adjacency — what appears next to the ad in a live, fast-moving
feed — and it is not a question you settle once.</p>
<p>What is actually available: <strong>keyword and conversation exclusions</strong>, which work on
text you can anticipate and not on what you cannot; <strong>inventory filter settings</strong> that
trade reach against conservatism; <strong>account block lists</strong>, useful and endless; and
<strong>third-party verification</strong>, which reports after the fact rather than preventing.</p>
<p>What none of them solves is that adjacency on a real-time feed is probabilistic. <strong>The
honest position is a documented risk tolerance rather than an assurance</strong> — decide in advance
what an acceptable rate of poor adjacency looks like, who reviews it, and what triggers a pause.</p>
<p>Two practical consequences. <strong>Write the escalation path before you launch</strong>, because
the moment you need it is the moment there is no time to design it. And <strong>keep spend
proportionate to the reputational exposure</strong>: a channel where the tail risk is a screenshot is
a channel to size deliberately rather than to scale by performance alone.</p>
''')]),

'codex/paid-advertising/video-advertising': dict(sources=[MRC], sections=[
 S('Making One Asset Work Across Placements', '''
<p>Producing a bespoke cut per placement is the correct answer and rarely the affordable one. The
workable compromise is to shoot with the constraints in mind so one production yields several usable
cuts.</p>
<p><strong>Frame for the crop.</strong> Shoot 16:9 with the action and any on-screen text inside a 9:16
safe area, and a vertical cut becomes a crop rather than a reshoot. Getting this wrong is the single
most common reason a campaign has no vertical asset.</p>
<p><strong>Structure for the skip.</strong> Build the opening so the message survives being cut at
five or six seconds, which means brand and proposition early, not a slow build to a reveal.</p>
<p><strong>Design for sound-off.</strong> Burned-in captions, not a subtitle track, because many
placements ignore the track. If the video only makes sense with audio, a large share of the
impressions are wasted.</p>
<p><strong>Produce the short cut deliberately</strong> rather than trimming the long one. A six-second
asset edited from a thirty-second narrative is almost always a fragment of an argument rather than an
argument.</p>
'''),
 S('What the Standard Metrics Do Not Tell You', '''
<p>Video reporting is dense and most of it describes the placement rather than the advertising.</p>
<p><strong>Completion rate</strong> is largely a property of skippability. A high rate on
non-skippable inventory is arithmetic, not performance, and comparing completion across skippable and
non-skippable placements compares two different things.</p>
<p><strong>Viewability thresholds are minimums, not goals.</strong> The standard for video is a defined
portion of pixels in view for a defined duration — a low bar deliberately, so that it can be measured
consistently. An impression that clears it has not necessarily been watched.</p>
<p><strong>View-through conversions</strong> are the most generous number in the report and the one
most often used to justify budget. Segment them from click-through conversions and look at them
separately.</p>
<p>The measures worth building a decision on are <strong>audible-and-visible-on-complete</strong>
where the platform offers it, <strong>brand lift</strong> where the budget supports a study, and
<strong>a geographic holdout</strong> for anything substantial. All three are harder than reading the
dashboard, which is why the dashboard remains popular.</p>
''')]),

'codex/seo/technical/site-architecture': dict(sources=[GSC], sections=[
 S('Diagnosing an Architecture You Inherited', '''
<p>Most architecture work is done on a site that already exists, and the useful first step is
measurement rather than redesign.</p>
<p><strong>Crawl the site and plot click depth from the homepage.</strong> Anything beyond three or
four clicks is a candidate for promotion. The distribution matters more than any single page: a long
tail at depth six usually means a category layer is missing.</p>
<p><strong>Compare the crawl against the sitemap and against your analytics.</strong> Three sets
worth looking at: URLs in the crawl but not the sitemap, URLs in the sitemap but not reachable by
crawling, and URLs receiving traffic that appear in neither. Each set is a different defect.</p>
<p><strong>Look at log files if you can get them.</strong> They show what search engines actually
requested rather than what you think is important, and the gap between the two is usually the finding.</p>
<p><strong>Count internal links per page.</strong> Pages with one inbound internal link are relying
entirely on the sitemap, which is a weak signal and a fragile one.</p>
'''),
 S('Changing It Without Losing What Works', '''
<p>Restructuring is the highest-risk routine SEO work because the downside is immediate and the
upside is gradual.</p>
<p>The sequence that limits the damage: <strong>map every current URL to its destination before
touching anything</strong>, including the ones you intend to retire, and decide for each whether it
redirects, stays, or returns a gone status. A redirect map built after launch is built from server
errors.</p>
<p><strong>Redirect to the closest equivalent, not to the homepage.</strong> Bulk redirects to the
root are treated as soft errors and discard the signal you were trying to preserve.</p>
<p><strong>Update internal links to point at final destinations</strong> rather than relying on the
redirects. Chains dilute, slow crawling and accumulate.</p>
<p><strong>Keep the old sitemap available for a period</strong> so the redirects are discovered
promptly, then retire it.</p>
<p><strong>Expect a dip.</strong> Recovery on a well-executed migration typically takes weeks, and the
most common mistake is reversing course inside that window on the basis of a fortnight's data —
turning one disruption into two.</p>
''')]),

'codex/ecommerce/ecommerce-seo': dict(sources=[GSC], sections=[
 S('Products That Come and Go', '''
<p>The problem unique to e-commerce SEO is that the catalogue changes underneath the site. Products
sell out, get discontinued, come back seasonally, and get replaced by a successor — and each case
needs a different answer.</p>
<table>
<tr><th>Situation</th><th>Do this</th></tr>
<tr><td>Temporarily out of stock</td><td><strong>Keep the page live</strong>, say so plainly, offer alternatives and a back-in-stock notification. Never remove it</td></tr>
<tr><td>Permanently discontinued, direct successor</td><td><strong>301</strong> to the successor</td></tr>
<tr><td>Permanently discontinued, no successor</td><td><strong>Keep it</strong> if it has links or traffic, with alternatives on the page; otherwise return <strong>410</strong></td></tr>
<tr><td>Seasonal</td><td><strong>Keep the URL permanently</strong> and change the content. Rebuilding an equity-carrying page every year discards it</td></tr>
<tr><td>Variant sold out, product live</td><td>Nothing — handle it in the page, not in the URL</td></tr>
</table>
<p>The rule behind the table: <strong>a URL that has accumulated links and history is an asset, and
deleting it spends that asset to save a database row.</strong> The default should be to keep and
repurpose.</p>
'''),
 S('Facets: Deciding What Deserves to Exist', '''
<p>Faceted navigation generates near-unlimited URLs and is the largest crawl-budget problem most
catalogues have. The answer is not to block everything — some facet combinations are exactly what
people search for.</p>
<p>Decide per facet, deliberately, and write the decision down:</p>
<ul>
<li><strong>Indexable</strong> — facets with genuine search demand and enough inventory to make a
useful page. Often brand, category and sometimes colour or size. Give them clean URLs, unique titles
and real copy.</li>
<li><strong>Crawlable, not indexable</strong> — useful for users, no search demand. Let them be
reached, keep them out of the index.</li>
<li><strong>Neither</strong> — sort orders, view toggles, session parameters, and multi-facet
combinations. These should not generate crawlable links at all.</li>
</ul>
<p>Two practical rules. <strong>Cap the number of facets that can combine into an indexable URL</strong>
— two is usually the limit beyond which the pages are thin and near-duplicate. And
<strong>check that an indexable facet page has enough products to be worth landing on</strong>: a
facet page with three items is a poor result, and serving many of them is how a catalogue acquires a
quality problem it cannot see.</p>
''')]),

'codex/paid-advertising/snapchat-ads': dict(sources=[SNAPA], sections=[
 S('What to Test First, and With What Budget', '''
<p>The most common way a Snapchat test fails is that it was never given the conditions to succeed:
too little budget, too many audiences, and creative borrowed from another platform.</p>
<p>A defensible first test. <strong>One objective</strong>, chosen for what you actually need to learn.
<strong>Two or three audiences at most</strong>, each with enough budget to exit the learning phase —
splitting a small budget across six audiences produces six inconclusive results.
<strong>Native creative</strong>, shot vertically and sound-on, not a repurposed asset.
<strong>A run long enough to clear the learning period</strong> and then produce readable data, which
is usually a fortnight rather than a few days.</p>
<p>Instrument it properly before launching: the pixel or SDK firing correctly, the conversion events
you care about defined, and — where available — a server-side connection, because the browser-side
signal on mobile is the weakest part of the measurement chain.</p>
'''),
 S('Lenses: the Differentiator and Its Real Cost', '''
<p>AR Lenses are the platform's genuine differentiator, and the reason they under-deliver for most
advertisers is a budgeting error rather than a creative one.</p>
<p>A Lens has <strong>three costs, and most plans carry one</strong>. The <strong>media</strong> to
distribute it. The <strong>production</strong> — a designer or studio working in the Lens toolset,
which is a specialist skill and a real timeline. And the <strong>concept</strong>, which is the part
that decides whether it works: a Lens people want to use for its own sake, rather than an advert
wearing a filter.</p>
<p>The ones that perform tend to do something functional — a try-on that answers a real question about
fit, colour or scale — or something genuinely playful that people want to send to a friend.
<strong>Sharing is the whole mechanism</strong>: an unshared Lens is expensive display advertising.</p>
<p>So the metric to judge it on is not impressions but <strong>shares and play time</strong>. And the
decision to make before commissioning one is whether you have a concept that survives the question
*why would anyone send this to a friend* — because if the answer is thin, the media budget is better
spent on formats that do not depend on it.</p>
''')]),

'codex/programmatic/programmatic-measurement-viewability': dict(sources=[MRC, TAG], sections=[
 S('Why Vendor Numbers Disagree, and Which to Trust', '''
<p>Two verification vendors measuring the same campaign will report different viewability, and the
discrepancy is a measurement artefact rather than a fault.</p>
<p>The causes are mundane and worth knowing. <strong>Tag placement differs</strong> — a measurement
wrapper placed at a different point in the ad's load sees a different set of impressions.
<strong>Measurability rates differ</strong>, because some environments block measurement entirely and
each vendor handles unmeasured impressions differently in the denominator.
<strong>Filtering differs</strong>, since each vendor removes invalid traffic on its own rules before
reporting.</p>
<p>The practical answer is not to find the correct vendor. It is to <strong>designate one as the
system of record for billing</strong>, write that into the contract, and use the others directionally.
A campaign measured by three vendors with no designated source of truth will spend more time
reconciling than optimising.</p>
<p>And always read <strong>measurability alongside viewability</strong>. A 70% viewability rate on 50%
measured inventory is a much weaker claim than the headline suggests, and reporting that omits the
measurability figure is omitting the part that qualifies it.</p>
'''),
 S('Invalid Traffic Beyond the Obvious', '''
<p>Invalid traffic splits into a category everyone filters and a category most buyers never see.</p>
<p><strong>General invalid traffic</strong> is the routine layer — known data-centre ranges, declared
crawlers, obvious non-human patterns. It is filtered as a matter of course and is largely a solved
problem.</p>
<p><strong>Sophisticated invalid traffic</strong> is the one that matters: hijacked residential
devices, ads stacked invisibly on top of one another, pixel-stuffed frames, falsified app identifiers
and domain spoofing. It is detected statistically and after the fact, which means some of it is paid
for before it is found.</p>
<p>What actually reduces exposure, in order of effect: <strong>buy through fewer, shorter supply
paths</strong>, since most spoofing enters through resold inventory; <strong>check the seller
authorisation files</strong> for the domains you buy and treat unauthorised sellers as a reason to
exclude; <strong>prefer certified counterparties</strong> in the supply chain; and <strong>make
make-goods contractual</strong> rather than relying on goodwill after the fact.</p>
<p>Treat a suspiciously cheap, high-performing placement as a finding to investigate rather than a
result to scale. <strong>The inventory that looks too good is the inventory to audit first.</strong></p>
''')]),

'codex/affiliate-marketing/affiliate-fraud-prevention': dict(sources=[FTC], sections=[
 S('The Signals That Actually Surface Fraud', '''
<p>Affiliate fraud is usually visible in the data well before anyone looks, and the useful signals are
ratios rather than volumes.</p>
<ul>
<li><strong>Click-to-conversion ratio far outside the programme norm.</strong> Very high suggests
cookie stuffing; very low with heavy click volume suggests click fraud on a cost-per-click
arrangement.</li>
<li><strong>Time from click to conversion clustered near zero.</strong> Genuine buyers take time to
decide; a cluster of near-instant conversions suggests the click was manufactured after the purchase
decision.</li>
<li><strong>Conversions concentrated in narrow windows</strong> or at implausible hours for the
claimed audience.</li>
<li><strong>Traffic sources that do not match the stated model.</strong> A content affiliate sending
overwhelmingly direct or untagged traffic is worth a conversation.</li>
<li><strong>Refund and chargeback rate materially above programme average</strong>, which often
indicates incentivised or misrepresented conversions.</li>
</ul>
<p>Review these <strong>as a scheduled report</strong>, not in response to a suspicion. Fraud found by
accident is found late, and the commission has usually been paid.</p>
'''),
 S('Terms That Prevent Rather Than Punish', '''
<p>Most affiliate disputes are avoidable, and the avoidance happens in the programme terms before
anyone joins.</p>
<p>The clauses worth having, stated plainly rather than buried: <strong>a payment hold period</strong>
long enough to cover your refund curve; <strong>an explicit brand-bidding position</strong>, whichever
way you decide it; <strong>permitted and prohibited traffic sources</strong> named specifically —
incentivised traffic, toolbars and extensions, and paid social under your brand name are the common
gaps; <strong>a defined clawback right</strong> with the window and the trigger written down; and
<strong>a right to audit</strong> a partner's traffic on reasonable notice.</p>
<p>Two principles about enforcement matter more than the clauses. <strong>Apply them
consistently</strong> — a rule waived for a large partner and enforced against a small one is not a
rule, and partners compare notes. And <strong>investigate before accusing</strong>: a pattern that
looks like fraud is sometimes a tracking defect on your side, and a wrongly accused good partner does
not come back.</p>
<p>Disclosure obligations sit alongside all of this. A partner misrepresenting a paid relationship
creates an exposure that is yours as much as theirs.</p>
''')]),

'codex/affiliate-marketing/coupon-deal-affiliate': dict(sources=[FTC, ASCI], sections=[
 S('Testing Whether Coupon Partners Add Anything', '''
<p>The argument about coupon affiliates is an incrementality argument, and it is testable rather than
a matter of opinion.</p>
<p><strong>The cleanest test is a holdout.</strong> Suspend coupon partners for a defined period and
watch total revenue, not attributed revenue. If total holds while attributed coupon revenue
disappears, the partners were intercepting demand you already had. If total falls, they were bringing
something.</p>
<p><strong>A softer test</strong> is to look at new versus returning customers by partner. A coupon
partner delivering mostly new customers is doing acquisition; one delivering mostly returning
customers at the final step is being paid for a conversion that was already happening.</p>
<p><strong>The signal you can read without a test</strong> is the checkout behaviour: a visible
promo-code field prompts a search for a code, and the resulting commission is created by your own
interface rather than by the partner. Hiding or collapsing the field is a one-line change that
frequently moves the number.</p>
<p>Whatever the outcome, decide it on your own data. <strong>The category performs very differently by
market, margin and brand strength</strong>, and general advice about coupon affiliates is unusually
unreliable.</p>
'''),
 S('Structuring the Relationship Once You Know', '''
<p>If the test says the partners add something, the answer is rarely a flat rate for everyone.</p>
<p><strong>Commission tiering by partner type</strong> is the standard instrument: a lower rate for
last-click coupon conversions than for content partners who introduce the customer. This is not a
punishment; it prices the different work honestly, and good partners understand it.</p>
<p><strong>New-customer bonuses</strong> pay more for genuine acquisition and less for a discount
applied to a returning buyer, which aligns payment with the thing you actually want.</p>
<p><strong>Exclusive codes</strong> are worth more than public ones, because they are trackable,
attributable to one partner and controllable in value — and they stop your discount leaking onto
aggregators you never approved.</p>
<p><strong>Code hygiene is a real operational task.</strong> Expired codes circulating on aggregator
sites produce failed checkouts and support contacts, and the customer blames you rather than the site.
Audit what is live against what should be, periodically.</p>
<p>And the disclosure obligation applies here as everywhere: a page recommending a retailer for a
commission is a paid recommendation, whether the mechanism is a link or a code.</p>
''')]),

'codex/social-media/employee-advocacy': dict(sources=[FTC, ASCI], sections=[
 S('The Disclosure Question Nobody Asks First', '''
<p>Employee advocacy programmes are usually designed as a distribution problem and land as a
disclosure one.</p>
<p>The principle is the same as for any endorsement: <strong>a material connection between the
endorser and the brand has to be apparent to the reader.</strong> Employment is a material connection,
and an employee posting favourably about their employer's product to an audience that does not know
where they work is exactly the case the rules address.</p>
<p>What this means practically. <strong>Employment should be evident</strong> — in the profile, or in
the post where the profile does not make it obvious. <strong>Incentives make it stricter</strong>: if
posting earns a reward, a bonus, a prize draw or a leaderboard place, that is a paid endorsement and
needs clearer disclosure than employment alone. And <strong>a policy has to say what people may not
do</strong> — inventing results, disparaging competitors, sharing unreleased information or
pre-announcement financials.</p>
<p>Write it before the launch, in plain language, with examples. A policy written after an incident is
written about the incident.</p>
'''),
 S('Why Mandates Fail and What Replaces Them', '''
<p>The programmes that fail share a design: content is queued centrally, employees are asked to share
it, and participation is measured. The output is identical posts from many accounts, which the
platforms suppress and colleagues ignore.</p>
<p>The mechanism is straightforward. <strong>Advocacy works because it is personal</strong> — a
recommendation from someone you know reads differently from a corporate post. Centrally written
copy distributed verbatim removes exactly the property that made it work, and readers detect it
immediately.</p>
<p>What works instead: <strong>supply raw material rather than finished posts</strong> — a fact, a
customer outcome, an image, a link — and let people write their own words.
<strong>Make participation genuinely voluntary</strong>, because a compelled endorsement is a
disclosure problem and an authenticity problem at once.
<strong>Recognise contribution rather than volume</strong>, since leaderboards produce posting rather
than advocacy. And <strong>train a small group properly</strong> rather than enrolling everyone:
fifteen people who post well outperform three hundred who post once.</p>
<p>Measure it by <strong>engagement and downstream action on employee posts</strong>, not by
participation rate. Participation rate is the metric that rewards the failure mode.</p>
''')]),

'codex/analytics-cro/looker-studio-google-data-studio': dict(sources=[LOOK], sections=[
 S('Why Dashboards Get Slow, and the Fixes That Work', '''
<p>Looker Studio reports degrade predictably as they grow, and the causes are structural rather than
incidental.</p>
<p><strong>Live connectors query on every load.</strong> A report with eight charts against a live
source issues queries each time someone opens it, and against a large dataset or a rate-limited API
that is the whole problem.</p>
<p><strong>Blends are computed at query time</strong> and are the single most expensive element in
most slow reports. A report with several blends across large sources will be slow regardless of what
else you do.</p>
<p><strong>Calculated fields run per row, per query</strong>, and complex nested logic multiplies
across every chart using it.</p>
<p>What actually helps, in order: <strong>use extracts</strong> for data that does not need to be live,
which converts a repeated query into a scheduled one; <strong>pre-aggregate upstream</strong> in the
warehouse or a scheduled table so the report reads a small, purpose-built dataset;
<strong>move calculated fields upstream</strong> into that table; and <strong>split large reports into
pages</strong>, since only the visible page executes.</p>
<p>Ask first whether the data genuinely needs to be live. Most dashboards presented as real-time are
read once a day.</p>
'''),
 S('Dashboards People Actually Open', '''
<p>The common failure is not technical. It is a report that answers no particular question, so nobody
returns to it after the launch email.</p>
<p><strong>Start from the decision.</strong> Ask what the reader will do differently depending on what
the dashboard says. If there is no answer, the report is a data display and it will be abandoned —
the same test that governs a segmentation.</p>
<p><strong>One question per page</strong>, with the answer in the top left where the eye lands first.
A page that requires interpretation before it communicates has failed.</p>
<p><strong>Include the comparison in the chart.</strong> A number without a benchmark, a target or a
prior period is not information. This single habit removes most of the follow-up questions a dashboard
generates.</p>
<p><strong>Date the data and name the owner</strong> on the report itself. Reports outlive the people
who build them, and an undated dashboard silently showing stale data is worse than no dashboard —
which is the same failure this site records for stale published counts, in a different medium.</p>
<p>And <strong>retire reports deliberately.</strong> A workspace with forty dashboards has perhaps six
that are trusted, and the other thirty-four make those six harder to find.</p>
''')]),

'codex/paid-advertising/mobile-advertising': dict(sources=[MMP], sections=[
 S('Attribution After the Identifier Changes', '''
<p>Mobile attribution was built on a stable per-device advertising identifier. That assumption no
longer holds, and the practical consequences are larger than the policy summaries suggest.</p>
<p>On iOS, access to the identifier requires user permission through the app tracking prompt, and
consent rates are well below universal. On Android the identifier can be reset or withheld. So a
material share of installs cannot be deterministically matched to a click.</p>
<p>What replaces it is <strong>aggregated, delayed and privacy-constrained</strong>: postback
frameworks that report conversions in coarse buckets after a delay, with thresholds below which
nothing is reported at all. The operational consequences are what matter —
<strong>small campaigns can fall below reporting thresholds and appear to produce nothing</strong>;
<strong>optimisation windows lengthen</strong>, so fast iteration on creative becomes unreliable; and
<strong>post-install event data is limited</strong>, which weakens the value-based bidding that mobile
campaigns depend on.</p>
<p>Plan for fewer, larger, longer campaigns rather than many small fast ones. The measurement
environment now rewards that shape.</p>
'''),
 S('Mobile Fraud, and What Actually Reduces It', '''
<p>App install advertising carries a distinctive fraud problem because the payable event — an install
— is cheap to fabricate.</p>
<p>The recognisable forms. <strong>Click injection</strong>, where an app on the device detects an
install beginning and fires a click moments before completion to claim attribution.
<strong>Click flooding</strong>, sending enormous volumes of clicks so that some organic installs
attribute by chance. <strong>Install farms</strong>, real devices installing at scale.
<strong>SDK spoofing</strong>, fabricating the install signal without an install happening at all.</p>
<p>The signals that expose them are distributional. <strong>Click-to-install time</strong> clustered
near zero indicates injection; a very long flat tail indicates flooding.
<strong>Conversion rate far above the network norm</strong> is a finding, not a success.
<strong>Post-install engagement near zero</strong> is the clearest signal of all — fraudulent installs
do not open the app twice.</p>
<p>What reduces exposure: <strong>pay on a post-install event</strong> rather than the install itself,
which removes most of the economic incentive at a stroke; <strong>use a measurement partner's
fraud filtering</strong> and understand what it does and does not catch;
<strong>agree rejection terms in the insertion order</strong> before spending; and
<strong>cap and monitor by sub-publisher</strong>, since fraud concentrates in a small number of
sources that a network-level view averages away.</p>
''')]),
}

ANCHOR = '</div>\n    <aside class="guide-sidebar">'
_TPL = io.open('_build/codex_style.txt', encoding='utf-8').read()
SRCS_CSS = '\n' + _TPL[_TPL.index('.srcs{'):_TPL.index('.srcs a{word-break:break-word}') + len('.srcs a{word-break:break-word}')]
assert '.srcs{' in SRCS_CSS and '</style>' not in SRCS_CSS

done = 0
for path, cfg in PAGES.items():
    f = path + '/index.html'
    assert os.path.exists(f), 'missing ' + f
    src = io.open(f, encoding='utf-8').read()
    if cfg['sections'][0][0] in src:
        print('  = already expanded: ' + path); continue
    add = ''.join('<h2>%s</h2>\n%s\n' % (t, c) for t, c in cfg['sections'])
    add += sources_block(cfg['sources'])
    n = src.count(ANCHOR)
    assert n == 1, '%s: anchor appears %d times' % (f, n)
    i = src.find(ANCHOR)
    out = src[:i] + add + src[i:]
    assert len(out) == len(src) + len(add), 'length delta wrong'
    assert out.count('<div') == src.count('<div') + add.count('<div')
    assert out.count('</div>') == src.count('</div>') + add.count('</div>')
    assert out.count('<table') == src.count('<table') + add.count('<table')
    assert out.count('</table>') == src.count('</table>') + add.count('</table>')
    assert len(re.findall(r'<h1[\s>]', out)) == 1
    assert out.count('</html>') == 1 and out.count('</body>') == 1
    if cfg['sources'] and '.srcs{' not in out:
        assert out.count('</style>') == 1, f + ': %d style blocks' % out.count('</style>')
        before = len(out)
        out = out.replace('</style>', SRCS_CSS + '\n</style>', 1)
        assert len(out) == before + len(SRCS_CSS) + 1, f + ': css delta wrong'
    if cfg['sources']:
        assert '.srcs{' in out, f + ': sources block with no CSS'
    io.open(f, 'w', encoding='utf-8').write(out)
    done += 1
    print('  ✅ %-52s +%d words, %d sources' % (path.replace('codex/', ''),
          len(re.sub(r'<[^>]+>', ' ', add).split()), len(cfg['sources'])))
print('\n%d pages expanded' % done)
