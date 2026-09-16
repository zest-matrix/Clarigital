#!/usr/bin/env python3
"""cx_expand_04.py — Session 95. Fourth content-remediation batch, thirteen pages.

Same contract as batches 1-3: two <h2> sections each, written as the practical
and failure layer the originals skipped; target 600+ content words; typed
sources only where a real primary source exists; no invented figures.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

GA4 = ('official', 'Google Analytics 4 documentation',
       'the UTM parameter handling, session definition and engaged-session criteria described here',
       'support.google.com')
GSC = ('official', 'Google Search Central documentation',
       'mobile-first indexing, HTTPS as a ranking signal, migration guidance and hacked-site recovery',
       'developers.google.com')
GBP = ('official', 'Google Business Profile guidelines',
       'the name, address and phone requirements that citation consistency is measured against',
       'support.google.com')
MDN = ('official', 'MDN Web Docs on HTTP security headers',
       'the behaviour of HSTS, Content-Security-Policy, X-Content-Type-Options and Referrer-Policy',
       'developer.mozilla.org')
TT = ('official', 'TikTok Ads Manager creative documentation',
      'the format specifications, sound requirements and Spark Ads mechanics described here',
      'ads.tiktok.com')
GADS = ('official', 'Google Ads Help documentation',
        'Display Network targeting types, placement controls and the reporting behaviour described here',
        'support.google.com')
IAB = ('official', 'IAB Tech Lab specifications and the seller authorisation files',
       'the supply-path and seller-verification mechanics referenced here', 'iabtechlab.com')
BSKY = ('official', 'Bluesky and AT Protocol documentation',
        'custom feed mechanics, handle verification via domain, and account portability', 'docs.bsky.app')

S = lambda t, c: (t, c)

PAGES = {

'codex/analytics-cro/utm-parameters-campaign-tracking': dict(sources=[GA4], sections=[
 S('Governing Tags Across a Team', '''
<p>UTM tagging fails at the organisational level rather than the technical one. The parameters are
trivial; getting four people in two agencies to write them identically is not.</p>
<p><strong>A spreadsheet is not governance.</strong> What works is a single builder — a form that
constructs the URL from controlled dropdowns rather than free text — so the values cannot drift. Free
text guarantees <code>facebook</code>, <code>Facebook</code>, <code>fb</code> and <code>FB</code> in
the same report.</p>
<p>Three rules worth enforcing in the builder itself. <strong>Lowercase everything</strong>, because
the parameters are case-sensitive and analytics will treat variants as separate sources.
<strong>No spaces</strong>, which become <code>%20</code> and look like different values.
<strong>Never tag internal links</strong> — a UTM on a link between two pages of your own site starts
a new session and re-attributes an existing visitor to the campaign, inflating it and destroying the
original source.</p>
<p>That last one is the most damaging and the most common. If your own navigation carries UTMs,
every report downstream of it is wrong in a way that looks like success.</p>
'''),
 S('What the Tags Cannot Tell You', '''
<p>UTMs record what the link said, not what happened. Several gaps follow from that and each one
misleads in a predictable direction.</p>
<p><strong>They are trivially editable.</strong> A user can change the parameters, and bots do. Traffic
arriving with malformed or nonsensical campaign values is usually spam rather than a tagging error.</p>
<p><strong>They are lost on redirect chains</strong> if any hop drops the query string, which turns a
tagged visit into direct traffic.</p>
<p><strong>They cannot see dark social.</strong> A link shared in a private message or a group chat
arrives untagged regardless of what you built, which is a large share of what gets recorded as direct.</p>
<p><strong>They describe the click, not the journey.</strong> UTMs feed last-click attribution by
default, so a campaign that introduced a customer and a campaign that closed them look identical, and
only one gets credit.</p>
<p>The practical consequence: <strong>use UTMs to answer "which link did they arrive on", not "what
caused the sale".</strong> The second question needs a holdout or a model, and treating tag data as
though it answers it is how channels get defunded for work they actually did.</p>
''')]),

'codex/social-media/bluesky-marketing': dict(sources=[BSKY], sections=[
 S('Verification by Domain, and Why It Matters More Here', '''
<p>Bluesky lets an account set its handle to a domain it controls, so a brand can appear as
<code>@yourcompany.com</code> rather than a username. This is done by publishing a DNS record or
serving a file at a well-known path on the site.</p>
<p>It is worth doing early for a reason specific to the platform: <strong>there is no blue tick to
apply for.</strong> Domain control is the verification mechanism, and it is self-serve. An account
that has not done it is indistinguishable from an impersonator, and impersonation is easy on an open
network where anyone can register any username.</p>
<p>Two practical notes. <strong>Changing the handle does not break the account</strong> — followers
and posts persist, because identity is held separately from the handle. And <strong>a subdomain
works</strong>, so a team account can be <code>@news.yourcompany.com</code> without touching the
apex record.</p>
<p>Do this before posting anything, not after the first impersonation report.</p>
'''),
 S('Building for Feeds Rather Than an Algorithm', '''
<p>The platform's defining feature for marketers is that <strong>the feed is not one algorithm you
optimise against.</strong> Users subscribe to custom feeds, many of them community-built and
topic-specific, each with its own inclusion rules.</p>
<p>That changes the work. Instead of guessing at ranking signals, you <strong>find the feeds your
audience actually reads and understand what puts a post into them</strong> — usually a keyword, a
hashtag, or membership of a curated list. Getting into three relevant topic feeds is worth more than
any amount of general optimisation.</p>
<p>It also changes the risk. <strong>Feeds are built and maintained by individuals</strong>, so one
can change its rules or disappear without notice, and distribution built on a single feed is fragile
in a way that distribution on a platform algorithm is not.</p>
<p>The honest scale assessment: this is a smaller audience than the established networks, skewed to
technology, media and academia. <strong>Judge it on the quality of the conversation and on reaching a
specific professional community, not on reach.</strong> Treated as a volume channel it will
disappoint; treated as a place to be present where a particular audience talks, it is cheap.</p>
''')]),

'codex/seo/technical/https-security': dict(sources=[GSC, MDN], sections=[
 S('The Migration Checklist, in Order', '''
<p>An HTTPS migration loses rankings when steps are done out of sequence, not when they are skipped.
The order matters more than the completeness.</p>
<ol>
<li><strong>Install and test the certificate</strong> on staging. Confirm the full chain serves, not
just the leaf — an incomplete chain validates in some browsers and fails in others.</li>
<li><strong>Fix mixed content first.</strong> Every image, script, stylesheet and iframe must load
over HTTPS. A single insecure asset breaks the padlock on the whole page.</li>
<li><strong>Update internal links and canonicals</strong> to the HTTPS versions. Relying on redirects
for your own links leaves every internal hop going through a redirect.</li>
<li><strong>301 redirect HTTP to HTTPS</strong>, page for page. Never to the homepage.</li>
<li><strong>Add the HTTPS property in Search Console</strong> — it is a separate property, and
forgetting it means your data appears to stop.</li>
<li><strong>Submit the updated sitemap</strong> with HTTPS URLs.</li>
<li><strong>Only then enable HSTS.</strong> It is deliberately hard to reverse; enabling it before
everything above is verified turns a mistake into a long one.</li>
</ol>
'''),
 S('Headers Worth Setting, and What Each Actually Prevents', '''
<p>Security headers are cheap to add and easy to add wrongly. Each one prevents a specific thing, and
knowing which is the difference between configuration and cargo cult.</p>
<table>
<tr><th>Header</th><th>What it prevents</th><th>Caution</th></tr>
<tr><td><strong>HSTS</strong></td><td>Downgrade to HTTP after the first visit</td><td>Hard to undo. Start with a short max-age, raise it once stable</td></tr>
<tr><td><strong>Content-Security-Policy</strong></td><td>Injected scripts executing</td><td>The one most likely to break your site. Deploy report-only first</td></tr>
<tr><td><strong>X-Content-Type-Options</strong></td><td>Browsers guessing a file's type and executing it</td><td>Safe. Set it and forget it</td></tr>
<tr><td><strong>Referrer-Policy</strong></td><td>Leaking full URLs to third parties</td><td>Too strict and you lose referrer data in your own analytics</td></tr>
<tr><td><strong>X-Frame-Options</strong></td><td>Your pages being framed for clickjacking</td><td>Breaks legitimate embedding if you have any</td></tr>
</table>
<p><strong>Content-Security-Policy is worth the effort and is not a one-line addition.</strong> Run it
in report-only mode for a fortnight, collect what it would have blocked, and only then enforce.
Enforcing first is how a site loses its own analytics, its fonts, or its checkout.</p>
''')]),

'codex/seo/local/local-citations': dict(sources=[GBP], sections=[
 S('Fixing Citations in the Right Order', '''
<p>Citation cleanup is mostly wasted effort because it is done in the wrong order. The volume is
enormous and the value is concentrated in a handful of sources.</p>
<p><strong>Start with the data aggregators and the primary profile.</strong> Many smaller directories
pull from a small number of upstream sources, so correcting a listing on a site that is downstream of
a wrong aggregator record means it will revert. Fixing upstream propagates; fixing downstream does
not.</p>
<p><strong>Then the industry-specific directories</strong> that matter in your sector — a restaurant's
reservation platforms, a clinic's health directories. These carry real traffic as well as signal.</p>
<p><strong>Then the general directories</strong>, by size.</p>
<p><strong>And stop.</strong> The long tail of scraped directories is effectively infinite and
chasing it has no measurable return. A service promising to fix hundreds of citations is selling
volume, not results.</p>
<p>The one situation that justifies a thorough sweep is <strong>a genuine change</strong> — a move, a
rebrand, a new number — where stale records actively mislead customers rather than merely being
inconsistent.</p>
'''),
 S('What Actually Counts as an Inconsistency', '''
<p>Not every difference matters, and treating them all as equal is how citation work becomes
busywork.</p>
<p><strong>Materially different, worth fixing:</strong> a different phone number, a wrong or outdated
address, a closed location still listed as open, a different business name entirely, or a competitor's
number on your listing — which happens and is not always accidental.</p>
<p><strong>Cosmetically different, largely harmless:</strong> <em>Street</em> versus <em>St</em>,
<em>Suite 4</em> versus <em>#4</em>, presence or absence of <em>Pvt Ltd</em>, and formatting of the
phone number. These are normalised by the systems reading them.</p>
<p><strong>The genuinely damaging case is duplicates</strong> — two or three listings for the same
location with different details. Duplicates split reviews and signals between records and are worse
than a single inconsistent listing. Merging them is the highest-value citation work there is, and
almost nobody starts there.</p>
<p>Audit for duplicates first, material errors second, and leave the abbreviations alone.</p>
''')]),

'codex/seo/technical/mobile-seo': dict(sources=[GSC], sections=[
 S('What Mobile-First Indexing Actually Penalises', '''
<p>Mobile-first indexing means the mobile rendering of your page is the one that counts. The failures
it produces are rarely about layout — they are about content that exists on desktop and does not
exist on mobile.</p>
<p><strong>Content hidden behind interactions is fine; content omitted is not.</strong> Text inside an
accordion or a tab is indexed normally as long as it is present in the markup. Text removed from the
mobile template, or loaded only when a user taps, may not be.</p>
<p>The specific things to check, in order of how often they bite:</p>
<ul>
<li><strong>Structured data present on both.</strong> Frequently rendered on desktop only.</li>
<li><strong>Meta titles and descriptions identical</strong> across both renderings.</li>
<li><strong>Images with the same alt text</strong>, and not lazy-loaded in a way that leaves them
absent from the rendered HTML.</li>
<li><strong>Internal links intact.</strong> A cut-down mobile navigation removes the internal linking
that pages deeper in the site depend on — the most damaging item on this list and the least visible.</li>
</ul>
'''),
 S('Diagnosing It Without Guessing', '''
<p>The gap between what you see on your phone and what a crawler sees is where mobile SEO problems
live, and your phone is not a reliable instrument.</p>
<p><strong>Use the URL inspection tool's rendered HTML</strong>, not a browser. It shows what was
actually received and executed, which is the only version that matters.</p>
<p><strong>Compare the rendered mobile HTML against the desktop HTML</strong> as text. Diff them. A
word-count gap between the two is the single most useful mobile SEO diagnostic and takes a minute.</p>
<p><strong>Check the crawl stats for the mobile user agent specifically.</strong> If mobile crawling
is a small fraction of desktop, something is discouraging it.</p>
<p><strong>Test on a throttled connection</strong>, not on office wifi. Mobile page speed problems are
invisible at high bandwidth, and the resources that fail are usually the ones that load last.</p>
<p>One thing that does <em>not</em> need checking any more: whether to build a separate mobile site.
The answer is no, and a responsive single URL removes an entire category of the problems above.</p>
''')]),

'codex/business-strategy/brand-voice-tone': dict(sources=[], sections=[
 S('Making a Voice Guide People Can Use', '''
<p>Most voice guides are unusable because they describe a personality rather than a decision. Three
adjectives tell a writer nothing at the moment they are choosing between two sentences.</p>
<p>What works is <strong>paired examples</strong>. For each principle, show a sentence that follows it
and a sentence that does not, drawn from your own material rather than invented. A writer reading
<em>"we say 'you can cancel any time', not 'cancellation is available to subscribers'"</em> learns
more than from the word <em>approachable</em>.</p>
<p>Then add the parts guides usually omit. <strong>A words-we-use-and-avoid list</strong>, with
reasons — not a style ban, but the terms your audience does not use.
<strong>Decisions about mechanics</strong>: contractions, the Oxford comma, sentence case in headings,
how you write numbers. These are where inconsistency is most visible and least debatable.
<strong>And how the voice bends</strong> for an error message, a legal notice, a rejection.</p>
<p>A guide that cannot resolve an argument between two writers is decoration.</p>
'''),
 S('Voice When the Copy Is Generated', '''
<p>Generated copy defaults to a recognisable register — fluent, symmetrical, slightly elevated, fond
of tricolons and of the "not X, but Y" construction. It is competent and it is nobody's voice, and a
brand that adopts it wholesale sounds like every other brand doing the same.</p>
<p>Three practical responses.</p>
<p><strong>Give the model examples, not adjectives.</strong> The same paired samples that make a voice
guide usable for a person make it usable as a prompt. Adjectives produce an average; examples produce
something closer to yours.</p>
<p><strong>Name the patterns to avoid explicitly</strong>, because they are strong defaults and will
return unless excluded by name.</p>
<p><strong>Edit for specificity rather than for style.</strong> The most reliable tell in generated
copy is not the phrasing, it is the absence of anything only your organisation could say — a real
number, a real customer, a real constraint. Adding one concrete detail does more than rewriting three
sentences.</p>
<p>And keep a human decision at the end. <strong>Voice is a position about who you are talking to</strong>,
and that is not a drafting task.</p>
''')]),

'codex/paid-advertising/tiktok-ads/tiktok-creative-best-practices': dict(sources=[TT], sections=[
 S('Testing Creative at the Rate the Platform Consumes It', '''
<p>The binding constraint on TikTok is creative supply. Assets fatigue faster than on any comparable
platform, so a process that produces one polished video a month cannot feed it.</p>
<p><strong>Build a testing structure that isolates the variable.</strong> Same audience, same budget,
several distinct creative concepts — not variations of one concept, which tests nothing useful.
Distinct means a different hook, a different format, a different narrator.</p>
<p><strong>Judge early on hold rate, not on conversions.</strong> The share of viewers still watching
at two and six seconds tells you within hours whether a hook works, long before conversion data is
readable. A creative that loses most viewers in two seconds will not be rescued by the landing page.</p>
<p><strong>Retire on a schedule, not on a threshold.</strong> Waiting for performance to collapse
means running weak creative through the decline. Plan the replacement while the current asset is
still working.</p>
<p><strong>And produce in batches.</strong> A shoot that yields eight usable variants costs little
more than one that yields two, and the constraint is volume.</p>
'''),
 S('Using Creators Without the Usual Mistakes', '''
<p>Creator-made content generally outperforms brand-made content on the platform, and most brands
undermine the advantage in the same three ways.</p>
<p><strong>Over-directing.</strong> A creator handed a script produces an advert in their own voice,
which is the worst of both. Brief the message and the constraints; leave the execution alone.</p>
<p><strong>Not securing usage rights.</strong> Running a creator's organic post as paid media requires
permission, and negotiating it after the post performs costs far more than agreeing it upfront. Settle
the term, the platforms and whether you may edit, before the shoot.</p>
<p><strong>Treating it as a one-off.</strong> The creators who work best are the ones who understand
the product, and that takes more than one video. A small roster producing regularly beats a large
roster producing once.</p>
<p>On disclosure: a paid relationship must be evident to the viewer, and the platform's own
paid-partnership tool is the clearest way to do it. <strong>The obligation follows the payment, not
the format</strong> — a gifted product is a material connection too.</p>
''')]),

'codex/business-strategy/market-research': dict(sources=[], sections=[
 S('The Questions That Produce Useless Answers', '''
<p>Most bad research is bad at the question level, and no amount of sample size repairs it.</p>
<p><strong>Do not ask people to predict their own behaviour.</strong> <em>"Would you buy this at
₹500?"</em> reliably overstates intent, because agreeing is free. Ask what they did last time
instead — what they actually bought, what they actually paid, when.</p>
<p><strong>Do not ask them to explain their preferences.</strong> People construct plausible reasons
after the fact, fluently and sincerely, and those reasons are not the cause.</p>
<p><strong>Do not ask two things in one question.</strong> <em>"Was the service fast and
friendly?"</em> cannot be answered by someone who found it fast and rude.</p>
<p><strong>Do not put the answer in the question.</strong> <em>"How much did you enjoy…"</em> has
already assumed enjoyment.</p>
<p>The reliable pattern is <strong>past behaviour, specific and recent</strong>. It is less exciting
than asking about the future and it is the only part of a survey that predicts anything.</p>
'''),
 S('Knowing When You Have Enough', '''
<p>Two different questions get confused: how many people do I need, and how many conversations do I
need. They have different answers.</p>
<p><strong>For qualitative work, the test is saturation</strong> — you stop when new interviews stop
producing new themes. For a reasonably homogeneous group that usually arrives sooner than people
expect; for a varied one, later. The number is an outcome, not an input, and running interviews to hit
a target after saturation is spending money to confirm what you know.</p>
<p><strong>For quantitative work, the size depends on the decision</strong>, not on a rule of thumb.
Detecting a large difference needs far fewer responses than detecting a small one, so the useful
question is how small a difference would change what you do. If a five-point gap would not alter the
decision, you do not need to be able to detect it.</p>
<p><strong>And representativeness beats volume.</strong> Two thousand responses from a self-selected
list describe that list. Two hundred from a properly drawn sample describe the market. A large
unrepresentative sample is more dangerous than a small one, because the numbers look authoritative.</p>
''')]),

'codex/paid-advertising/display-advertising': dict(sources=[GADS, IAB], sections=[
 S('Making Display Accountable', '''
<p>Display carries a reputation for being unaccountable, and most of that is a measurement choice
rather than a property of the channel.</p>
<p><strong>Separate view-through from click-through conversions in every report.</strong> Blended,
they overstate the channel; separated, both numbers are usable. This single change alters most display
debates.</p>
<p><strong>Set a view-through window you can defend.</strong> The defaults are generous, and a long
window on a high-reach channel credits purchases that would have happened regardless.</p>
<p><strong>Exclude your own converters and recent visitors</strong> from prospecting campaigns, or
prospecting quietly becomes remarketing with a prospecting label and excellent-looking numbers.</p>
<p><strong>Run a holdout for anything substantial.</strong> A matched-region test is the only method
that answers whether display created demand rather than observed it.</p>
<p>Done that way, display is a legitimate upper-funnel channel with honest numbers. Done the default
way, it produces impressive reports that fall apart the first time anyone tests them.</p>
'''),
 S('Placement Hygiene as a Standing Task', '''
<p>The largest source of wasted display spend is inventory nobody chose. Automatic placement
expansion will find cheap impressions, and cheap impressions are cheap for reasons.</p>
<p>A routine that works, run monthly rather than at launch:</p>
<ul>
<li><strong>Sort the placement report by spend</strong> and exclude anything that has spent
meaningfully with no conversions and no engagement.</li>
<li><strong>Exclude app inventory unless you deliberately want it.</strong> A large share of accidental
display spend is mobile games, where the click is usually a mis-tap.</li>
<li><strong>Check content categories</strong>, not just individual sites — the blunt category
exclusions catch what a site-by-site list never will.</li>
<li><strong>Look at the distribution, not the average.</strong> A handful of placements consuming most
of the budget is normal; the question is whether they are the ones you would have picked.</li>
</ul>
<p>And treat a placement that performs implausibly well as something to investigate rather than to
scale. <strong>The cheapest, best-performing inventory in the report is where to look first for
invalid traffic.</strong></p>
''')]),

'codex/analytics-cro/data-clean-rooms': dict(sources=[], sections=[
 S('What Makes One Work in Practice', '''
<p>Clean rooms fail on the unglamorous parts, not on the privacy technology.</p>
<p><strong>Match rate decides everything.</strong> If only a minority of your customers can be matched
to the partner's data, the analysis describes that minority — which is systematically the more
digitally engaged, more frequently logged-in part of your base. A clean room with a low match rate
does not produce a weaker answer; it produces a confidently wrong one about a skewed group.
<strong>Ask for the match rate before the contract, not after the first analysis.</strong></p>
<p><strong>Your own data has to be ready.</strong> Identifiers normalised, hashed in the agreed way,
deduplicated, and reflecting a consistent definition of a customer. Most of the effort in a clean-room
project is this, before anything joins.</p>
<p><strong>Somebody has to be able to write the query.</strong> The interfaces are SQL-shaped and
constrained by aggregation thresholds, so a team with no analyst will buy access and not use it.</p>
'''),
 S('The Limits That Decide Whether It Is Worth It', '''
<p>The constraints that make a clean room private also make it awkward, and they are what determine
whether one earns its cost.</p>
<p><strong>Aggregation thresholds mean small segments return nothing.</strong> Queries below a minimum
audience size are suppressed, so the narrow, high-value analyses people most want are often exactly
the ones that cannot be run.</p>
<p><strong>You cannot export the joined data.</strong> Outputs are aggregates. Anything you want to
use downstream has to be expressible as an aggregate.</p>
<p><strong>Each partner is a separate room.</strong> Cross-platform measurement — the reason most
people want one — usually means several rooms with incompatible outputs, which is the problem you
started with in a more expensive form.</p>
<p><strong>And the costs are ongoing</strong>: the licence, the engineering to keep data flowing, and
the analyst time to use it.</p>
<p>The honest test: <strong>name the specific decision the clean room will settle, and what you will
do differently depending on the answer.</strong> If that is vague, the project will produce interesting
charts and no decisions — the same test that governs a segmentation or a dashboard.</p>
''')]),

'codex/paid-advertising/media-buying-fundamentals': dict(sources=[IAB], sections=[
 S('Reading What You Are Actually Paying For', '''
<p>The headline rate is rarely the cost. What sits between the rate and the outcome is the part worth
reading.</p>
<p><strong>Ask what share of your budget reaches the publisher.</strong> Between you and the inventory
there may be an agency, a DSP, an exchange and an SSP, each taking a margin. The difference between
gross and working media is frequently large and rarely volunteered.</p>
<p><strong>Establish whose numbers bill.</strong> Buyer and publisher count differently; agree the
system of record and the acceptable discrepancy before the flight rather than during it.</p>
<p><strong>Read the make-good terms.</strong> What happens on under-delivery, on invalid traffic, on a
brand-safety incident — and whether the remedy is a refund or more of the same inventory.</p>
<p><strong>Check the cancellation window.</strong> A campaign you cannot pause is a fixed cost, and on
a direct buy that window can be long.</p>
<p>None of this is adversarial. It is the difference between buying a rate and buying an outcome.</p>
'''),
 S('Frequency, Waste, and the Number Nobody Sets', '''
<p>Reach and frequency are planned and then not managed, and the gap between the plan and the
delivery is where most media waste lives.</p>
<p><strong>Frequency caps only work within a platform.</strong> Three campaigns each capped at three
impressions can deliver nine to the same person, and none of the three reports a problem. If you buy
one audience across several platforms, <strong>the effective cap is the sum</strong>, and the only
controls are consolidating buying or setting each cap materially lower.</p>
<p><strong>Distribution matters more than average frequency.</strong> An average of four can mean
everyone saw it four times, or that most saw it once and a few saw it twenty. Those are different
campaigns with the same number. Ask for the frequency distribution, not the mean.</p>
<p><strong>Diminishing returns arrive earlier than plans assume</strong>, and past a point additional
exposure produces irritation rather than recall — a cost that does not appear in any report.</p>
<p>The practical discipline: <strong>decide the frequency you intend before buying, measure the
distribution you got, and treat a long tail as budget to reallocate</strong> rather than as reach.</p>
''')]),

'codex/social-media/social-listening': dict(sources=[], sections=[
 S('Building Queries That Do Not Drown You', '''
<p>A listening setup fails in one of two directions: it returns everything, so nobody reads it, or it
returns nothing, so it seems unnecessary. Both are query problems.</p>
<p><strong>Start from the question, not the brand name.</strong> <em>Are people complaining about
delivery times?</em> produces a usable query. <em>Monitor our brand</em> produces a firehose.</p>
<p><strong>Handle ambiguity deliberately.</strong> A brand name that is also a common word needs
context terms and exclusions, and building those is most of the setup work. Test the query and read
the first hundred results before trusting it — the noise is obvious on inspection and invisible in a
volume chart.</p>
<p><strong>Account for how people actually write.</strong> Misspellings, abbreviations, transliteration
and local-language variants. In Indian markets in particular, a query in English alone will miss a
large share of what is being said.</p>
<p><strong>And separate the streams.</strong> Complaints, competitor mentions, feature requests and
general chatter want different routing and different response times. One combined feed gets ignored
as a single undifferentiated volume.</p>
'''),
 S('The Blind Spots Every Tool Shares', '''
<p>Listening tools see public posts on platforms that permit access, which is a smaller slice of the
conversation than dashboards imply.</p>
<p><strong>Private and semi-private spaces are invisible</strong> — messaging groups, closed
communities, direct messages. For many Indian consumer categories this is where most word of mouth
actually happens, which means the tool is measuring the visible minority.</p>
<p><strong>Platform access changes without notice</strong>, and historical coverage varies by
platform, so a trend line can move because access changed rather than because sentiment did.</p>
<p><strong>Automated sentiment is weakest exactly where it matters</strong>: sarcasm, code-switching
between languages, and category-specific terms where a normally negative word is neutral. Spot-check
it against a sample you read yourself before quoting a sentiment percentage to anyone.</p>
<p>Used honestly, listening is an <strong>early-warning and qualitative-insight tool</strong> — it
tells you what is being said and in what terms. <strong>Treated as a measurement system</strong>,
producing sentiment scores and share-of-voice percentages presented to two decimal places, it gives
false precision about a biased sample.</p>
''')]),

'codex/analytics-cro/bounce-rate-engagement-rate': dict(sources=[GA4], sections=[
 S('Why the Old Metric Misled So Consistently', '''
<p>Bounce rate was defined as a session with a single interaction, and that definition broke in a
specific and predictable way: <strong>it could not distinguish a satisfied visitor from a
disappointed one.</strong></p>
<p>Someone who searched for your opening hours, found them, and left had an entirely successful
visit and was recorded identically to someone who arrived, saw the wrong thing, and left in two
seconds.</p>
<p>Worse, it was <strong>trivially manipulable</strong>. Firing any additional event — a scroll
tracker, a timer — ended the bounce, so a site could improve the metric by changing its tracking and
nothing else. Comparisons between sites, or between a site before and after a tracking change, were
meaningless.</p>
<p>The replacement inverts it and adds time and depth: a session counts as engaged if it lasts beyond
a threshold, or has multiple page views, or includes a conversion. <strong>It is a better metric
because it has more than one way to succeed</strong>, not because the threshold is well chosen.</p>
'''),
 S('Using It Without Being Misled Again', '''
<p>The new metric is an improvement and it is still a proxy. Three habits keep it honest.</p>
<p><strong>Never compare it across page types.</strong> A reference page answering one question and a
category page that exists to send people onward should have very different engagement rates, and the
reference page being lower is correct rather than a problem.</p>
<p><strong>Compare a page against itself over time.</strong> A drop after a change is a signal; a
number in isolation is not. This is the only comparison the metric reliably supports.</p>
<p><strong>Check the engagement threshold before interpreting anything.</strong> It is configurable,
so the same content can produce different engagement rates in two properties. If someone changed it,
your trend line moved for a reason unrelated to your content.</p>
<p>And be specific about what would count as a problem: <strong>a page with high entries, low
engagement and no onward path</strong> is worth investigating. A low engagement rate on a page that
answers the question and offers nothing further is the page working. <strong>The metric measures
behaviour, not satisfaction, and the two diverge most on exactly the pages that serve people best.</strong></p>
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
    print('  ✅ %-50s +%d words, %d sources' % (path.replace('codex/', ''),
          len(re.sub(r'<[^>]+>', ' ', add).split()), len(cfg['sources'])))
print('\n%d pages expanded' % done)
