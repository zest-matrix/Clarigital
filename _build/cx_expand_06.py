#!/usr/bin/env python3
"""cx_expand_06.py — Session 97. Sixth content-remediation batch, thirteen pages.

Same contract as batches 1-5. Note: two AI Atlas pages appear in this batch,
the first non-Codex pages in the remediation programme. They use the same
guide-* template so the splice anchor is identical -- asserted per page, not
assumed.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

GA4 = ('official', 'Google Analytics 4 and Google Tag Manager server-side documentation',
       'server container behaviour, transport URLs and the consent-mode interaction described here',
       'developers.google.com')
GBP = ('official', 'Google Business Profile review policies',
       'the prohibited review-gating practices and the removal request process described here',
       'support.google.com')
PIN = ('official', 'Pinterest business documentation',
       'rich pins, board structure and the freshness signals described here', 'help.pinterest.com')
TT = ('official', 'TikTok Ads Manager documentation',
      'campaign structure, Spark Ads mechanics and the attribution settings described here',
      'ads.tiktok.com')
RDT = ('official', 'Reddit Ads documentation and content policy',
       'targeting options, comment settings on promoted posts, and the advertising policy referenced here',
       'redditinc.com')
WCAG = ('official', 'WCAG 2.2 and the email accessibility guidance derived from it',
        'contrast ratios, semantic structure and the alt-text requirements described here', 'w3.org')
DPDP = ('official', 'Digital Personal Data Protection Act, 2023 and the DPDP Rules, 2025',
        'the consent basis that server-side tagging does not remove', 'meity.gov.in')

S = lambda t, c: (t, c)

PAGES = {

'codex/analytics-cro/server-side-tagging': dict(sources=[GA4, DPDP], sections=[
 S('What Actually Breaks When You Move Server-Side', '''
<p>Server-side tagging is presented as a relocation and is closer to a rebuild. Several things that
worked client-side stop working, and discovering them after migration is the usual experience.</p>
<p><strong>Anything reading the browser stops reading the browser.</strong> Screen dimensions, the
referrer, page scroll, time on page, click targets — these exist in the browser and must be
explicitly collected and forwarded. A server container receives what you send it and nothing else.</p>
<p><strong>Third-party tags that expect a page context often cannot move at all.</strong> Chat
widgets, session recorders, heatmaps and A/B testing tools need to run in the page. Server-side is for
measurement, not for everything in your container.</p>
<p><strong>Cookie behaviour changes.</strong> Setting first-party cookies from your own domain is one
of the main reasons to do this, and it requires the server container to be on a genuine subdomain of
your site rather than a vendor domain. Getting that DNS and certificate arrangement right is most of
the setup.</p>
<p><strong>And debugging gets harder.</strong> You lose the browser network tab as the source of
truth; you now need server-container logging and the discipline to use it.</p>
'''),
 S('The Consent Question, Answered Plainly', '''
<p>The most common reason teams are sold server-side tagging is the least defensible one:
<strong>it does not remove the need for consent.</strong></p>
<p>Consent attaches to the <strong>processing of personal data</strong>, not to the mechanism that
transports it. Moving the collection point from a browser to your own server changes who makes the
request and changes nothing about whether you were permitted to collect and process the data. Under a
consent-based regime — and India's DPDP framework is one, with <strong>no legitimate-interest
basis</strong> — the obligation is identical.</p>
<p>What server-side genuinely improves: <strong>page performance</strong>, because fewer third-party
scripts execute in the browser; <strong>data control</strong>, since you decide what leaves your
server and can redact before forwarding; <strong>resilience</strong> to client-side blocking of
measurement you are entitled to collect; and <strong>first-party cookie longevity</strong>.</p>
<p>Those are real and they justify the cost on their own. <strong>If the business case rests on
collecting data you could not otherwise collect, the business case is the problem</strong>, and the
architecture will not fix it.</p>
''')]),

'codex/paid-advertising/reddit-ads': dict(sources=[RDT], sections=[
 S('Deciding What to Do About Comments', '''
<p>Reddit ads carry a comment section, which no other major platform's ad units do in the same way,
and it is the single decision that most affects outcomes.</p>
<p><strong>Comments on</strong> is the higher-variance option. A promoted post that people engage with
gains credibility no creative can buy; one they turn on becomes a public pile-on attached to your
brand name and visible to everyone the ad reaches.</p>
<p><strong>Comments off</strong> is safer and is read as defensive by an audience unusually attuned to
that. It also forfeits the one thing the platform offers that others do not.</p>
<p>The workable middle: <strong>comments on, with a human monitoring for the first hours</strong>, a
prepared first comment from the brand account that is honest about what the ad is, and a genuine
willingness to answer. A brand that shows up in its own comments and answers the hard question does
better than one that runs a polished ad and hides.</p>
<p>If you cannot staff that, <strong>turn comments off and accept the lower ceiling</strong> — which
is a legitimate decision, unlike leaving them on and unattended.</p>
'''),
 S('Targeting That Works, and the Trap in It', '''
<p>Subreddit targeting is the platform's real asset: you are reaching people by what they have chosen
to read about, which is closer to intent than most interest targeting.</p>
<p>What works: <strong>a curated list of specific subreddits</strong> you have actually read, rather
than the broad interest categories, which behave like ordinary display. Build the list by looking at
where your customers already discuss the problem, not by keyword.</p>
<p><strong>The trap is scale.</strong> A precise list of relevant communities is often too small to
spend against, and the platform will helpfully expand delivery beyond it. Check whether expansion is
enabled, because a campaign that started as precise subreddit targeting can quietly become broad
reach with the same reporting label.</p>
<p><strong>And match the creative to the community.</strong> A single ad across twelve subreddits
reads as an ad in all twelve. The platform's audience punishes generic more than most.</p>
<p>Measure on assisted and view-through separately from last click — this is a consideration channel,
and judging it purely on last-click conversions will under-report it in the same way display is
under-reported.</p>
''')]),

'codex/social-media/short-form-video-strategy': dict(sources=[], sections=[
 S('A Production System That Survives Contact With a Calendar', '''
<p>Short-form fails on supply, not on ideas. The teams that sustain it have a system rather than a
calendar.</p>
<p><strong>Batch the shoot, not the post.</strong> One session producing eight to twelve pieces costs
little more than one producing two, and the marginal cost is setup. A weekly shoot is a different
operation from a weekly post.</p>
<p><strong>Keep a running idea list</strong> fed from customer questions, support tickets and
comments, so the shoot never starts from a blank page. The blank page is what kills the cadence.</p>
<p><strong>Separate the roles.</strong> The person who is good on camera is rarely the person who
edits well or the person who knows what to make. Trying to be all three is why most programmes stop
after six weeks.</p>
<p><strong>Template the edit.</strong> Consistent captions, a consistent end frame, a consistent
opening beat — so editing is assembly rather than design.</p>
<p><strong>And build a bank before launching.</strong> Ten pieces in reserve means a bad fortnight
does not break the cadence, and cadence is most of what the platforms reward.</p>
'''),
 S('Reading Retention Instead of Views', '''
<p>Views are the least useful number on the report. Retention tells you what to change and where.</p>
<p><strong>The first-three-seconds drop</strong> is a hook problem. If most viewers leave before the
content starts, nothing later in the video matters and re-editing the middle is wasted work.</p>
<p><strong>A steady decline</strong> is normal and is about pacing. Tightening cuts and removing the
setup lifts it.</p>
<p><strong>A sharp mid-video cliff</strong> marks a specific moment — a slow explanation, a
brand mention, a change of pace. Watch that second of the video and you will usually see it.</p>
<p><strong>A flat line to the end</strong> means the video could be longer, which is the signal most
people never look for.</p>
<p><strong>Rewatches and shares outrank likes</strong> on every platform in this format, because both
indicate the content did something for the viewer rather than being merely acceptable.</p>
<p>The practical loop: <strong>change one thing per batch</strong> — the hook, the pacing, the length —
and compare retention curves rather than view counts, which are too influenced by distribution luck to
read as feedback.</p>
''')]),

'codex/seo/local/online-reviews-reputation': dict(sources=[GBP], sections=[
 S('Asking for Reviews Without Breaking the Rules', '''
<p>The line is narrower than most businesses assume, and crossing it risks the profile rather than
just the reviews.</p>
<p><strong>Permitted:</strong> asking every customer, in person, by email, by message or on a receipt.
Making it easy with a direct link or QR code. Reminding once. Training staff to ask.</p>
<p><strong>Not permitted:</strong> offering anything of value for a review — a discount, an entry, a
free item — regardless of whether you ask for a positive one.
<strong>Review gating</strong>, which means asking how satisfied someone is and routing only the happy
ones to the public review form, is explicitly prohibited and is the most common violation because it
feels reasonable.
<strong>Bulk requests</strong> in one burst, which reads as inauthentic.
And <strong>buying reviews</strong>, which is detectable and increasingly enforced.</p>
<p>The one adjustment that legitimately moves the number most: <strong>ask at the moment of
satisfaction</strong>, not weeks later in a monthly email. A request sent when the work is finished and
the customer is pleased converts several times better than the same request sent cold.</p>
'''),
 S('Responding, and What a Response Is Actually For', '''
<p>The audience for a review response is not the reviewer. It is the next prospective customer reading
the profile, who will read both the complaint and the reply and form a view of how you handle
problems.</p>
<p>That reframes the whole exercise. <strong>Write for the reader, not the writer.</strong></p>
<p>What works on a negative review: <strong>respond promptly and briefly</strong>; <strong>do not
argue the facts in public</strong> even when you are right, because a factual rebuttal reads as
defensive regardless of its accuracy; <strong>acknowledge the experience</strong> without necessarily
accepting the characterisation; <strong>offer a route off the platform</strong> with a real contact;
and <strong>never disclose anything about the customer</strong>, which in a healthcare or financial
context can be a regulatory matter as well as a bad look.</p>
<p>What to do about a genuinely fraudulent review — a competitor, a person who was never a customer,
one containing abuse: <strong>report it through the platform's process with specifics</strong>, and
expect it to fail more often than it succeeds. Meanwhile respond publicly and calmly, because the
response is what the next reader sees whether or not the review is ever removed.</p>
<p><strong>And respond to positive reviews too</strong>, briefly. A profile where only complaints get
replies tells its own story.</p>
''')]),

'codex/analytics-cro/web-analytics-fundamentals': dict(sources=[GA4], sections=[
 S('Where the Numbers Come From, and Why Two Tools Disagree', '''
<p>Two analytics tools will never agree, and knowing why prevents a great deal of wasted
reconciliation.</p>
<p><strong>Different session definitions.</strong> How long a gap ends a session, whether a new
campaign starts a new one, and what happens at midnight all differ between tools.</p>
<p><strong>Different collection points.</strong> A tag firing on page load, a tag firing after consent,
and a server log capture three different populations of the same traffic.</p>
<p><strong>Different bot filtering.</strong> Each vendor removes automated traffic on its own rules,
before you see any of it.</p>
<p><strong>Different attribution.</strong> One tool's last-click and another's data-driven model will
allocate the same conversion differently, and both are internally consistent.</p>
<p>The practical rule: <strong>pick one system of record per question and stop reconciling.</strong>
Use the ad platform's numbers for optimising the ad platform, your analytics for on-site behaviour, and
your own database for revenue. Trying to make three systems agree consumes analyst time and produces
nothing, because they are measuring different things by design.</p>
'''),
 S('A Measurement Plan That Fits on One Page', '''
<p>Most analytics implementations begin with tools and end with a dashboard nobody uses. The order
should be the reverse.</p>
<p>The one-page structure that works:</p>
<ol>
<li><strong>The business objective</strong>, in a sentence. Not <em>grow</em> — what specifically.</li>
<li><strong>The two or three questions</strong> you need answered to steer towards it.</li>
<li><strong>For each question, the metric that answers it</strong>, and the comparison that makes it
meaningful — against last period, a target, or a segment.</li>
<li><strong>For each metric, where it comes from</strong> and who owns it.</li>
<li><strong>What you will do differently</strong> depending on what it says.</li>
</ol>
<p><strong>Step five is the one that gets skipped and the one that matters.</strong> A metric with no
decision attached is a number you will report monthly for two years and never act on — the same test
that governs a segmentation, a dashboard and a clean room.</p>
<p>Write it before configuring anything. <strong>The plan determines what you need to track; the tool
does not determine what you need to know.</strong></p>
''')]),

'codex/social-media/pinterest-marketing': dict(sources=[PIN], sections=[
 S('Working With the Long Lifespan', '''
<p>Pinterest behaves unlike a feed: a pin can drive traffic for years, and the strategic consequences
are the opposite of every other social platform.</p>
<p><strong>Evergreen beats timely.</strong> Content tied to a news moment wastes the format. Content
answering a durable question compounds.</p>
<p><strong>Seasonality runs early.</strong> People plan on Pinterest, so seasonal content needs to be
live well before the season rather than during it. Publishing a festive guide in the festive week is
publishing it late.</p>
<p><strong>Old pins keep working</strong>, which means your library is an asset rather than an
archive, and auditing what still drives traffic is more valuable than producing more.</p>
<p><strong>And the destination has to survive.</strong> A pin that outlives the page it links to sends
traffic to a 404 for years. <strong>Check your top-performing pins against live URLs periodically</strong>
— this is the maintenance task nobody schedules, and on a platform with this lifespan it is the one
that matters most.</p>
'''),
 S('Whether It Is Worth Your Time', '''
<p>Pinterest rewards specific categories heavily and most others barely at all, and being honest about
which you are in saves months.</p>
<p><strong>Strong fit:</strong> anything visual and planned — home, interiors, food, fashion, beauty,
weddings, travel, craft, gardening. Also, less obviously, <strong>anything explainable as a
diagram</strong>: finance basics, health information, educational content. The second group is
underserved and competes with less.</p>
<p><strong>Weak fit:</strong> B2B software, professional services, anything where the purchase is not
visual and not planned in advance. Presence here is usually an obligation someone inherited.</p>
<p>The resourcing question is the deciding one. Pinterest needs <strong>original vertical imagery</strong>,
which is a production cost, and consistency over months before results appear. A brand that already
produces photography for other reasons is adding a distribution channel cheaply. A brand that would
have to start producing imagery is starting a new function.</p>
<p><strong>Judge it on referral traffic and its trend over six months</strong>, not on impressions.
Impressions here are abundant and mean very little.</p>
''')]),

'codex/email-marketing/email-design-templates': dict(sources=[WCAG], sections=[
 S('Testing Across Clients Without Losing a Week', '''
<p>Email rendering is inconsistent enough that testing is not optional, and thorough testing is
expensive. The compromise is a tiered approach.</p>
<p><strong>Tier one — test every send.</strong> The two or three clients that account for most of your
list. Look at your own analytics rather than industry figures; the distribution varies enormously by
audience.</p>
<p><strong>Tier two — test on template change.</strong> The next several clients, plus dark mode, plus
one narrow mobile viewport.</p>
<p><strong>Tier three — accept degradation.</strong> Old desktop clients with known limitations. Make
sure the email is readable there, not that it is beautiful.</p>
<p>Two habits that prevent most problems. <strong>Build from a template you have already
tested</strong> rather than designing fresh each time — the failures come from new structures, not new
copy. And <strong>send a real test to real accounts</strong> on the main clients, because a rendering
preview and an actual inbox differ in ways that matter, particularly around image blocking and
clipping on long emails.</p>
'''),
 S('Accessibility, Which Also Fixes Deliverability', '''
<p>Accessible email is better email for reasons that have nothing to do with compliance, and the
overlap with deliverability is large enough to be the practical argument.</p>
<p><strong>Real text, not text in images.</strong> Screen readers cannot read an image of text, image
blocking hides it, and an image-only email is a recognised spam pattern. One change solves three
problems.</p>
<p><strong>Semantic structure</strong> — actual headings rather than large bold paragraphs — so the
email can be navigated rather than only read top to bottom.</p>
<p><strong>Alt text on every image</strong>, describing function rather than appearance. This is also
what a recipient with images blocked sees, which is a large share of your list.</p>
<p><strong>Sufficient contrast</strong>, checked rather than eyeballed, and tested in dark mode where
many clients invert colours unpredictably.</p>
<p><strong>Descriptive link text.</strong> <em>Read the pricing guide</em> rather than <em>click
here</em>, which is unusable out of context and is also the pattern filters associate with bulk mail.</p>
<p><strong>And a real text-to-image ratio.</strong> Not a myth exactly, but the underlying point is
sound: an email that is one large image is worse on every axis at once.</p>
''')]),

'codex/business-strategy/brand-strategy': dict(sources=[], sections=[
 S('Making Brand Decisions That Constrain Something', '''
<p>A brand strategy that permits everything decides nothing. The test of each element is whether it
rules something out.</p>
<p><strong>Positioning</strong> that names the competitor you are chosen instead of, and the customer
you are not for. A positioning statement with no excluded customer is a description of the market.</p>
<p><strong>A single-minded proposition</strong>: the one thing you want remembered. Three things is
zero things, because nobody carries three.</p>
<p><strong>Distinctive assets</strong> — colour, shape, sound, character, format — chosen and then
used with monotonous consistency. Their value is entirely in repetition, so changing them because the
team is bored destroys the asset at exactly the point it starts working.</p>
<p><strong>And a decision about what you will not do</strong>: categories you will not enter, tones you
will not use, partnerships you will decline.</p>
<p>The practical check on any brand document: <strong>find the sentence that would cause an argument
if someone proposed the opposite.</strong> If every sentence would be agreed to by everyone, you have
written a description of being a good company.</p>
'''),
 S('Measuring Brand Without Pretending It Is Performance', '''
<p>Brand measurement fails in two directions: not measured at all, or measured with performance
metrics that cannot see it.</p>
<p>What is actually measurable, in increasing order of effort:</p>
<p><strong>Branded search volume</strong> — the cheapest proxy there is, available in your own Search
Console, and a reasonable indicator of whether more people are looking for you by name.</p>
<p><strong>Direct and organic traffic share</strong> over time, which moves slowly and in the right
direction when brand is working.</p>
<p><strong>Share of voice</strong> in your category, from listening or from a media measure.</p>
<p><strong>Prompted and unprompted awareness</strong>, which needs a survey and a consistent panel, and
is the first genuinely reliable measure.</p>
<p><strong>Price elasticity and win rate against a named competitor</strong> — the commercial outcomes
brand is supposed to produce, and the ones worth the most.</p>
<p>Two rules. <strong>Measure on a long cadence</strong> — twice a year, not monthly, because the
signal is slower than the noise. And <strong>never compare brand spend to performance spend on
last-click ROI</strong>, which is a comparison the measurement system is structurally unable to make
fairly, and the argument that defunds brand investment in most organisations.</p>
''')]),

'codex/social-media/social-media-crisis-management': dict(sources=[], sections=[
 S('The Holding Statement, Written in Advance', '''
<p>The first hour decides most of a crisis and is the hour in which nobody can write well. The answer
is to have written it already.</p>
<p>A holding statement acknowledges without conceding, and buys the time to establish facts. Its
components: <strong>that you are aware</strong>; <strong>that you are taking it seriously</strong>;
<strong>what you are doing right now</strong>; <strong>when you will say more</strong>; and
<strong>where to go for help</strong> if anyone is affected.</p>
<p>What it must not contain: <strong>speculation about cause</strong>, <strong>an assurance you cannot
yet support</strong>, <strong>blame directed anywhere</strong>, or <strong>the word "unfortunately"</strong>,
which reads as distancing.</p>
<p>Prepare a version for each of the three or four scenarios that are actually plausible for your
business — an outage, a data incident, a product safety issue, a staff conduct matter. Have them
approved by legal in advance, because <strong>the approval is the slow part, and approving a template
in calm conditions is a different exercise from approving a statement at midnight.</strong></p>
'''),
 S('Afterwards, Which Is the Part That Gets Skipped', '''
<p>The response ends and the organisation moves on, and the two most valuable activities both happen
after.</p>
<p><strong>A factual reconstruction.</strong> What happened, when each party knew, what was said and
when. Written within days, while people remember, and separately from any assignment of blame — a
timeline that people are frightened of is a timeline that does not get written honestly.</p>
<p><strong>Then the process questions.</strong> Did the escalation path work? Was the right person
reachable? Did the holding statement fit, or was it rewritten from scratch? What was the actual gap
between first signal and first response, measured rather than estimated?</p>
<p>And the one nobody asks: <strong>was this a crisis, or did we make it one?</strong> A meaningful
share of social media crises are ordinary complaints amplified by a defensive or slow response.
Distinguishing those honestly is what prevents the next one.</p>
<p><strong>Update the plan while it is uncomfortable.</strong> A review conducted three months later
produces agreement and no changes. Conducted in the week after, it produces specific, unwelcome, useful
amendments.</p>
''')]),

'ai-atlas/concepts/small-language-models': dict(sources=[], sections=[
 S('Choosing a Size by the Failure You Can Tolerate', '''
<p>Model selection is usually framed as a capability question and is better framed as a failure
question: <strong>what happens when this gets it wrong, and how often can you afford that?</strong></p>
<p>Small models fail differently from large ones. They are <strong>more likely to fail obviously</strong>
— producing something malformed, off-topic or incomplete — which is easier to catch automatically.
Large models fail <strong>more plausibly</strong>, producing fluent, confident, wrong output that
passes a superficial review.</p>
<p>That changes the calculation. For a task where <strong>a wrong answer is caught downstream</strong>
— a classification that gets validated, an extraction checked against a schema, a draft a human edits —
a small model's higher error rate may cost almost nothing, and the latency and price advantage is real.</p>
<p>For a task where <strong>a wrong answer reaches someone and is believed</strong>, the plausible
failure of a larger model is the more dangerous one, and neither size removes the need for the check.</p>
<p>The practical sequence: <strong>define the acceptable error rate first, measure both on your own
data, and choose the cheapest one that clears the bar.</strong> Almost nobody does it in that order.</p>
'''),
 S('What Running One Actually Involves', '''
<p>The appeal of a small model is usually cost or control, and both come with work that the comparison
tables omit.</p>
<p><strong>Self-hosting is an operational commitment</strong>, not a one-off saving: serving
infrastructure, capacity for peaks rather than averages, monitoring, and someone who can debug it at
two in the morning. Below a certain volume, an API is cheaper once that is costed honestly.</p>
<p><strong>The evaluation burden shifts to you.</strong> With a hosted frontier model you inherit the
vendor's testing; with a small or distilled model on your task, you own the question of whether it is
good enough, which means building an evaluation set before you deploy rather than after.</p>
<p><strong>Updates are yours to manage.</strong> A hosted model improves without your involvement — and
changes without your involvement, which cuts both ways. A self-hosted one stays exactly as it is until
you do the work, which is a genuine advantage for reproducibility and a genuine cost in capability.</p>
<p><strong>And on-device is a different discipline again</strong>: memory limits, battery, thermal
throttling, and the fact that you cannot patch a model on a device the user has not updated.</p>
<p>The honest summary: <strong>small models win on latency, unit cost and data residency, and lose on
the amount of engineering you have to supply yourself.</strong></p>
''')]),

'codex/seo/local/service-area-businesses': dict(sources=[GBP], sections=[
 S('Building Location Pages That Are Not Doorways', '''
<p>A service-area business needs pages for the areas it serves, and the standard approach — one
template with the place name substituted — is the definition of a doorway page and is treated as such.</p>
<p>What makes an area page legitimate is that <strong>it contains something true only of that
area</strong>. Sources, in rough order of how easy they are to produce honestly:</p>
<ul>
<li><strong>Actual jobs done there</strong>, described with enough specificity to be recognisable —
the most valuable and the most work.</li>
<li><strong>Reviews from customers in that area</strong>, quoted with permission.</li>
<li><strong>Area-specific practicalities</strong>: travel time, parking, access constraints, local
regulations, typical property types or conditions that affect the work.</li>
<li><strong>Local coverage detail</strong> — which neighbourhoods, which postcodes, and honestly where
you do not go.</li>
</ul>
<p><strong>The discipline: build pages only for areas where you have something to say.</strong> Four
substantial area pages outperform forty templated ones, and forty templated ones can attract a manual
action that costs the whole site.</p>
'''),
 S('Proving You Are Real Without a Shopfront', '''
<p>A hidden address removes the trust signals a storefront provides, and the compensation has to be
built deliberately.</p>
<p><strong>Show the people.</strong> Real photographs of the actual team, named, rather than stock
imagery. This is the single most effective substitute and the most commonly skipped.</p>
<p><strong>Show the work.</strong> Before-and-after photographs with locations, dated, and enough of
them to look like a business rather than a portfolio.</p>
<p><strong>Show the credentials.</strong> Registration numbers, insurance, trade body memberships,
certifications — stated plainly with numbers that can be checked.</p>
<p><strong>Be reachable in more than one way.</strong> A phone number that a person answers, in stated
hours, plus at least one alternative. A form-only contact page reads as an entity that does not want to
be contacted.</p>
<p><strong>And be honest about coverage.</strong> A page claiming to serve an entire state when you
work within one city is the fastest way to earn a one-star review from someone you declined to travel
to — and that review is permanent in a way the enquiry was not.</p>
''')]),

'codex/paid-advertising/tiktok-ads/tiktok-ads-fundamentals': dict(sources=[TT], sections=[
 S('Setting Up So the Learning Phase Completes', '''
<p>The most common cause of a failed TikTok test is a structure that prevents any ad group from
gathering enough data to optimise.</p>
<p><strong>Fewer ad groups, more budget each.</strong> Splitting a modest budget across six audiences
means none exits the learning phase, and six inconclusive results read as the platform not working.</p>
<p><strong>Do not edit during learning.</strong> Changing the budget, the bid, the audience or the
creative restarts it. The instinct to fix a slow start is exactly what prevents the recovery.</p>
<p><strong>Optimise toward an event that happens often enough.</strong> A conversion occurring a
handful of times a week cannot train a bid strategy. Optimise for a more frequent upstream event and
measure the rare one separately.</p>
<p><strong>Give it a fortnight before judging.</strong> Shorter reads are dominated by learning-phase
volatility, and the decisions made from them are usually wrong in both directions.</p>
<p>Instrument before launching: the pixel or events API firing, the events you care about defined, and
where available a server-side connection, because the browser-side signal is the weakest link.</p>
'''),
 S('Reading Attribution Honestly', '''
<p>Platform-reported performance is measured by the party selling the inventory, and on a high-reach
video platform the standard settings are generous in a specific direction.</p>
<p><strong>Separate click-through from view-through</strong> in every report. Blended, a view-through
window on a platform with this much reach credits purchases that were already happening.</p>
<p><strong>Shorten the default windows</strong> and compare against your own analytics. The gap between
platform-reported conversions and what your own system sees is the number to understand, not to
eliminate — they are measuring different things and both are internally consistent.</p>
<p><strong>Watch total revenue, not attributed revenue.</strong> If platform-attributed sales rise
while total sales do not, the channel is reallocating credit rather than creating demand.</p>
<p><strong>And run a holdout for anything material.</strong> A geographic or audience holdout over a
defined period is the only method that answers the incrementality question directly. It costs real
sales and it is the only evidence that survives a sceptical finance review.</p>
''')]),

'ai-atlas/concepts/reasoning-models': dict(sources=[], sections=[
 S('Deciding When the Extra Compute Is Worth Paying For', '''
<p>Reasoning models cost more and take longer, so the useful question is which tasks repay it.</p>
<p><strong>They repay it when the task has a verifiable answer and multiple steps.</strong>
Mathematics, code that must run, logic puzzles, planning with constraints, and analysis where an
intermediate mistake invalidates the conclusion. The extra compute is spent checking and revising, and
checking only helps when there is something to check against.</p>
<p><strong>They do not repay it on tasks with no single right answer.</strong> Drafting, summarising,
rewriting, tone work, brainstorming — here additional deliberation produces something more laboured
rather than more correct, and occasionally worse, because the model reasons its way out of a good first
instinct.</p>
<p><strong>They do not repay it on simple retrieval or classification</strong>, where you are paying a
premium for deliberation on a task that needs none.</p>
<p>The practical rule: <strong>if you cannot describe how you would check the answer, the extra compute
is unlikely to be buying you accuracy.</strong> Route by task type rather than defaulting everything to
the most capable option.</p>
'''),
 S('What the Visible Reasoning Is and Is Not', '''
<p>Many reasoning models expose a chain of intermediate steps, and it is easy to over-read.</p>
<p><strong>It is not a guaranteed causal account of how the answer was produced.</strong> It is
generated text, and a model can produce a plausible chain that does not correspond to the computation
that determined its output. Treating it as an audit trail is a mistake — particularly in a regulated
setting, where explainability means something specific and stricter.</p>
<p><strong>It is still genuinely useful</strong>, for three practical purposes: spotting where an
assumption was introduced, seeing which interpretation of an ambiguous question was taken, and finding
the step where a long calculation went wrong.</p>
<p><strong>Read it for those, and verify the answer independently.</strong></p>
<p>Two operational notes. <strong>Latency changes the product</strong>: a response taking tens of
seconds needs a different interface from one taking two, and designing for the fast case then switching
models breaks the experience. And <strong>cost scales with deliberation</strong>, so a task routed to a
reasoning model by default will be a great deal more expensive at volume than the headline token price
suggests.</p>
''')]),
}

# Two anchors: the Codex guide-* template and the AI Atlas art-* template.
# S97 assumed one and the assertion caught it before any Atlas page was written.
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
    # C10, at source: markdown must never reach the page (S96)
    stray = MD.findall(re.sub(r'<[^>]+>', ' ', add))
    assert not stray, '%s: markdown in the addition: %s' % (f, stray[:3])
    found = [a for a in ANCHORS if src.count(a) == 1]
    assert len(found) == 1, '%s: matched %d anchors (counts %s)' % (
        f, len(found), [src.count(a) for a in ANCHORS])
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
    print('  ✅ %-52s +%d words, %d sources' % (path[:52],
          len(re.sub(r'<[^>]+>', ' ', add).split()), len(cfg['sources'])))
print('\n%d pages expanded' % done)
