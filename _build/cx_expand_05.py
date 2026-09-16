#!/usr/bin/env python3
"""cx_expand_05.py — Session 96. Fifth content-remediation batch, thirteen pages.

Same contract as batches 1-4: two <h2> sections each, written as the practical
and failure layer the originals skipped; target 600+ content words; typed
sources only where a real primary source exists; no invented figures.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

ASA = ('official', 'Apple Search Ads and App Store Connect documentation',
       'campaign types, the Today tab and search-results placements, and the attribution behaviour described here',
       'searchads.apple.com')
ATT = ('official', 'Apple App Tracking Transparency policy',
       'the consent requirement that constrains attribution and audience targeting in the App Store environment',
       'developer.apple.com')
MSFT = ('official', 'Microsoft Advertising import documentation',
        'what the Google Ads import carries across, what it does not, and how scheduled sync behaves',
        'about.ads.microsoft.com')
GBP = ('official', 'Google Business Profile and Google Search Central local guidance',
       'the local pack behaviour and proximity effects that make local keyword volume data misleading',
       'support.google.com')
GSC = ('official', 'Google Search Central documentation',
       'crawl diagnostics, index coverage reporting and the rendering behaviour an audit works from',
       'developers.google.com')
GA4 = ('official', 'Google Analytics 4 documentation',
       'data retention settings, internal traffic filters, conversion configuration and consent mode behaviour',
       'support.google.com')
RDT = ('official', 'Reddit content policy and self-promotion guidance',
       'the site-wide rules and the subreddit-level discretion that governs promotional posting',
       'redditinc.com')
DIS = ('official', 'Discord and Telegram platform documentation',
       'server structure, permission models, moderation tooling and the group size limits referenced here',
       'discord.com')
FTC = ('official', 'FTC Endorsement Guides',
       'the disclosure obligations attaching to incentivised user content and reposted endorsements',
       'ftc.gov')
ASCI = ('official', 'ASCI Guidelines for Influencer Advertising in Digital Media',
        'the disclosure obligations for incentivised content aimed at Indian audiences', 'ascionline.in')
META = ('official', 'Meta Threads and Instagram documentation',
        'the account linkage, deletion behaviour and API availability described here', 'developers.facebook.com')

S = lambda t, c: (t, c)

PAGES = {

'codex/social-media/threads-marketing': dict(sources=[META], sections=[
 S('The Account Linkage, and What It Commits You To', '''
<p>A Threads account is created from an Instagram account and the two are bound together in ways that
matter before you post anything.</p>
<p><strong>The handle is inherited.</strong> You cannot choose a different name, so whatever your
Instagram handle is, that is your Threads identity. For a brand with an inconsistent handle across
networks, this decides the matter.</p>
<p><strong>Deleting has historically been entangled</strong> with the Instagram account, and the
separation has changed over time. Before a brand commits, confirm the current position rather than
assuming — an account you cannot independently retire is a different commitment from one you can.</p>
<p><strong>Your Instagram following does not transfer as followers</strong>, but it does drive the
follow suggestions that determine early reach. An established Instagram presence is the main
advantage a brand has here, and it decays if the Threads account sits dormant.</p>
<p>Practical consequence: <strong>do not open the account until someone owns it.</strong> A linked,
empty, unmaintained account is worse than none, because it is discoverable through Instagram and
signals abandonment.</p>
'''),
 S('Posting for a Conversational Feed', '''
<p>The format rewards different behaviour from Instagram, and brands importing an Instagram approach
underperform predictably.</p>
<p><strong>Replies are the mechanism, not the afterthought.</strong> Distribution follows
conversation, so a post that generates twenty replies you engage with outperforms a polished post
that generates fifty silent likes. Budget the time for replying before the time for posting.</p>
<p><strong>Text carries.</strong> Unlike Instagram, an image is optional and often unnecessary. This
lowers the production cost substantially, which is the main argument for a brand being there at all.</p>
<p><strong>Links are tolerated rather than rewarded.</strong> Treat it as a place to have the
conversation, with the link as a follow-up in a reply rather than the point of the post.</p>
<p><strong>Post more, polish less.</strong> The cadence that works is closer to several short posts a
day than to a scheduled calendar, which is a resourcing decision rather than a creative one — and the
honest reason many brands should not be here.</p>
''')]),

'codex/content-marketing/thought-leadership-content': dict(sources=[], sections=[
 S('Finding a Position You Can Actually Defend', '''
<p>The failure mode of thought leadership is agreeing with everyone. A piece nobody could disagree
with is not a position, and it is what most of the category produces.</p>
<p>The test is simple and uncomfortable: <strong>can you name a credible, informed person who would
argue the opposite?</strong> If not, you have written a description. <em>Data is important</em> is a
description. <em>Most dashboards should be deleted because they answer no decision</em> is a
position — someone sensible disagrees, and now the piece has to earn its claim.</p>
<p>Where a defensible position comes from, in order of reliability: <strong>something you have
measured</strong> that others have not; <strong>a pattern across your customers</strong> that
individual customers cannot see; <strong>a mistake you made</strong> and what it cost, which is the
most credible and least used; and <strong>a considered disagreement with received practice</strong>,
where you have to be right rather than merely contrary.</p>
<p>What does not produce one: summarising a report, restating a trend, or interviewing people who all
agree.</p>
'''),
 S('Sustaining It Past the First Three Pieces', '''
<p>Thought leadership programmes die at piece four, when the accumulated opinions run out and nobody
has built the machinery to generate more.</p>
<p><strong>Harvest rather than invent.</strong> The material already exists inside the organisation —
in sales objections, support tickets, the questions asked in every demo, the arguments the leadership
team has repeatedly. A standing practice of capturing those is worth more than a content calendar.</p>
<p><strong>Interview your own people properly.</strong> Most experts cannot write and can talk. A
recorded conversation transcribed and edited produces better material than asking them to draft
something they will not finish.</p>
<p><strong>Accept a narrow surface.</strong> A programme with one genuine area of authority and a
narrow output beats one covering everything shallowly. Readers remember a position on a subject, not
a volume of posts.</p>
<p><strong>And measure it as a slow asset.</strong> The signals are inbound conversations that cite
the work, invitations to speak, and being quoted by others — none of which appear in a monthly report.
Judging it on traffic in quarter one guarantees it gets cancelled before it works.</p>
''')]),

'codex/paid-advertising/microsoft-ads/importing-google-ads-campaigns': dict(sources=[MSFT], sections=[
 S('The Checklist for the First Week After Import', '''
<p>An import lands a working account and an inherited set of assumptions. The first week is about
separating the two.</p>
<ul>
<li><strong>Re-check every bid strategy.</strong> Automated strategies imported from an account with
far more conversion data will behave differently on thinner volume. Manual or enhanced bidding is
frequently the right starting point until the account has its own history.</li>
<li><strong>Halve the budgets, then watch.</strong> Search volume is lower, so imported budgets tend
to be wrong in the same direction across every campaign.</li>
<li><strong>Verify conversion tracking end to end</strong> with a real test conversion. The import
does not bring your tag, and an account optimising against a conversion that never fires will spend
the budget and report nothing.</li>
<li><strong>Review negative keyword lists</strong>, which import inconsistently and are the most
expensive thing to be missing.</li>
<li><strong>Check ad extensions</strong> individually rather than assuming they came across.</li>
<li><strong>Turn off the Audience Network initially</strong> so you can read search performance on its
own, then add it as a separate campaign.</li>
</ul>
'''),
 S('The Sync Trap, and How to Avoid It', '''
<p>Scheduled sync is the feature that causes the most damage, because it is helpful right up until it
is not.</p>
<p>The mechanism: a recurring import keeps the Microsoft account aligned with the Google one. The
problem is that <strong>it can overwrite the platform-specific optimisation you have been doing</strong>
— the bids you adjusted for lower volume, the negatives you added for different query patterns, the
budgets you rebalanced — and it does so silently, on a schedule, without a record anyone reads.</p>
<p>Three workable positions, in order of how much work they are:</p>
<p><strong>Sync off.</strong> Manage the account independently and accept the duplication. Correct for
any account you are actively optimising.</p>
<p><strong>Sync new items only</strong>, where the option exists — new campaigns and ads come across,
existing settings are left alone. The usual compromise.</p>
<p><strong>Full sync</strong> only where Microsoft is a low-effort mirror nobody optimises, which is a
legitimate choice if stated rather than a default nobody decided.</p>
<p><strong>Whichever you choose, write it down in the account notes</strong>, because the person who
inherits this account will not be able to tell a sync overwrite from a mistake.</p>
''')]),

'codex/paid-advertising/apple-search-ads': dict(sources=[ASA, ATT], sections=[
 S('Structuring the Account So the Data Is Usable', '''
<p>The standard structure separates what you know from what you are discovering, and accounts that
skip it cannot tell which is which.</p>
<p><strong>A brand campaign</strong> on your own app name, exact match. Defensive, cheap, and it stops
competitors owning your name. Ignore the argument that you would rank organically anyway — the ad slot
sits above the organic result.</p>
<p><strong>A competitor campaign</strong> on rival app names, if the category permits it. High intent,
higher cost, and worth testing rather than assuming.</p>
<p><strong>A category campaign</strong> on generic terms describing what the app does.</p>
<p><strong>A discovery campaign</strong> on broad match with search match enabled, whose only job is
to find terms. <strong>Mine it weekly</strong>: anything converting moves into an exact-match
campaign, anything wasting becomes a negative. Discovery is a research tool, not a performance
campaign, and judging it on cost per install misreads what it is for.</p>
<p>Without that separation, a good brand CPA hides a bad discovery CPA and the account looks healthier
than it is.</p>
'''),
 S('What the Privacy Environment Changes', '''
<p>The platform has an unusual advantage and a matching constraint, and both follow from the same
place.</p>
<p><strong>The advantage:</strong> attribution to install happens inside the App Store, so the
click-to-install measurement is direct rather than inferred. That is cleaner than most mobile
advertising.</p>
<p><strong>The constraint:</strong> everything <em>after</em> the install depends on what the user
consented to. Without tracking permission, connecting an install to later in-app behaviour is limited,
so <strong>optimising toward a post-install value event is harder here than the install numbers
suggest</strong>.</p>
<p>Practical consequences. <strong>Measure cost per install and separately measure cohort
behaviour</strong> from your own in-app analytics, rather than expecting one system to join them.
<strong>Expect slower, coarser signal</strong> on anything downstream, which rewards fewer and larger
campaigns over many small fast ones. And <strong>treat the consent prompt as part of the funnel</strong>
— when and how you ask materially affects the share who agree, and therefore how much of your
measurement works at all.</p>
''')]),

'codex/social-media/social-media-community-management': dict(sources=[], sections=[
 S('Escalation Paths, Written Before You Need Them', '''
<p>Community management is mostly routine and occasionally not, and the occasional case is decided by
whether a path existed before it arrived.</p>
<p>A workable tiering. <strong>Tier one</strong> — ordinary questions, praise, minor complaints. The
community manager answers, no approval, published response times.
<strong>Tier two</strong> — a substantiated product problem, a refund dispute, a complaint gaining
traction. Acknowledge publicly within the hour, move to a private channel, flag internally.
<strong>Tier three</strong> — safety, legal exposure, a named executive, a claim that could become a
story. **Stop responding and escalate**, because an off-the-cuff reply becomes the quote.</p>
<p>Three details that decide whether the tiering works. <strong>Name who is reachable out of
hours</strong>, because tier three does not respect a shift pattern. <strong>Pre-approve holding
language</strong> so acknowledging does not require a decision. And <strong>give the community
manager explicit authority to act at tier one</strong> — a queue where everything needs approval
produces slow, corporate, ignored responses.</p>
'''),
 S('Moderation That Does Not Become Censorship', '''
<p>The hardest judgement is the line between moderating and silencing, and getting it wrong in either
direction is expensive.</p>
<p>The workable principle: <strong>moderate behaviour, not opinion.</strong> Abuse, spam, illegal
content, personal information and harassment come down regardless of the view they express. Criticism
of your product, however blunt, stays up.</p>
<p><strong>Deleting legitimate criticism is the single most reliable way to escalate it.</strong> The
screenshot outlives the comment, and the deletion becomes the story rather than the complaint.</p>
<p><strong>Publish the moderation policy</strong> and apply it visibly and consistently. Inconsistent
enforcement is read as bias, correctly.</p>
<p><strong>Hiding is not always better than deleting.</strong> On platforms where hiding leaves the
comment visible to its author, they will discover it, and a concealed hide reads worse than an honest
removal with a reason.</p>
<p>And keep a record of what was removed and why. <strong>A moderation log is boring until the moment
someone accuses you of silencing them</strong>, at which point it is the only thing that settles it.</p>
''')]),

'codex/seo/local/local-keyword-research': dict(sources=[GBP], sections=[
 S('Building the Term List From Real Sources', '''
<p>Local keyword tools report thin and unreliable volumes, so the list has to come from elsewhere.
Four sources, in order of usefulness:</p>
<p><strong>Your own search query data.</strong> Search Console and any paid search account show what
people actually typed to reach you, with local variants you would not have guessed.</p>
<p><strong>Your own inbound calls and enquiries.</strong> What customers say on the phone is what they
type. Ask the people answering to note recurring phrasings for a fortnight.</p>
<p><strong>Autocomplete and related searches</strong>, checked from the target area rather than from
your office, because suggestions are location-influenced.</p>
<p><strong>Competitor pages that rank</strong>, read for the terms they use rather than run through a
tool.</p>
<p>Then add the variants tools systematically miss: <strong>neighbourhood and landmark names</strong>
that locals use and maps do not, <strong>colloquial and transliterated spellings</strong>, and
<strong>the "near me" family</strong>, which reports as one term and behaves as hundreds depending on
where the searcher stands.</p>
'''),
 S('Why Rank Tracking Misleads Locally', '''
<p>A local rank is not a property of a page. It is a property of a page, a query and <em>a
location</em>, and the third one is usually missing from the report.</p>
<p>Two searchers a few kilometres apart see materially different local results for the same query.
So <strong>a rank report showing position three is meaningless unless it states where it was
measured from</strong>, and a tool defaulting to a city centre will flatter a business located there
and punish one in the suburbs.</p>
<p>What to do instead: <strong>track from several points across your service area</strong>, using a
tool that supports geographic grid tracking, and read the shape rather than the number. The useful
output is a map of where you are visible and where you are not.</p>
<p><strong>And treat proximity as a constraint you cannot optimise away.</strong> A business will not
rank in the local pack far from its address no matter how good its optimisation, which is why
multi-location businesses need pages and profiles per location rather than one page working harder.</p>
<p>The honest metric for local is <strong>calls, direction requests and enquiries by area</strong>,
not average position.</p>
''')]),

'codex/social-media/reddit-marketing': dict(sources=[RDT], sections=[
 S('Doing It Without Being Removed', '''
<p>Reddit's rules are two-layered and the second layer is the one that catches brands. Site-wide policy
sets a floor; <strong>each subreddit sets its own rules and moderators enforce them at
discretion</strong>, so behaviour acceptable in one community is a ban in another.</p>
<p>What reliably works:</p>
<ul>
<li><strong>Participate before posting anything of your own.</strong> An account whose entire history
is promotion is removed on sight, and the history is public.</li>
<li><strong>Read the sidebar and the pinned rules</strong>, which say plainly whether self-promotion is
permitted and under what ratio.</li>
<li><strong>Message the moderators first</strong> where you are unsure. They generally answer, and
permission asked for is permission you can point at.</li>
<li><strong>Disclose your affiliation in the comment itself</strong>, not in a profile nobody opens.
Reddit punishes concealment far more than promotion.</li>
<li><strong>Answer questions in your area of expertise</strong> without linking. This is the whole
strategy, and it works slowly.</li>
</ul>
<p>What gets you removed: posting the same link across subreddits, vote manipulation, sockpuppet
accounts, and a helpful-sounding comment that is an advert. All three are detected, and the last one
by humans.</p>
'''),
 S('Why Reddit Threads Rank, and What That Means for You', '''
<p>Reddit threads appear prominently in search results for a category of query where people
explicitly want human opinion rather than a brand page — *best X for Y*, *is X worth it*,
*X vs Y reddit*.</p>
<p>Two consequences follow, and they point in opposite directions.</p>
<p><strong>The opportunity:</strong> a genuine, well-received answer in a thread that ranks reaches
people at a decision point for years, in a context where they trust the source precisely because it is
not you. That is worth more than a blog post on the same query.</p>
<p><strong>The risk:</strong> those threads exist about your brand whether you participate or not, and
a two-year-old complaint can be the first thing a searcher reads. <strong>Monitoring is the minimum
engagement</strong> — knowing what ranks for your brand name plus *reddit* is a five-minute check that
most brands never do.</p>
<p>Responding to old negative threads is delicate: a defensive reply revives a dead thread and puts it
back in front of people. <strong>Reply where there is a factual error you can correct, or where the
problem is fixed and saying so helps.</strong> Otherwise leave it and fix the underlying cause.</p>
''')]),

'codex/social-media/user-generated-content': dict(sources=[FTC, ASCI], sections=[
 S('Permission Is Not a Comment Saying Yes', '''
<p>Reposting someone's content without clear permission is the most common legal mistake in social
marketing, and *"we credited them"* is not a defence — <strong>the copyright sits with the creator
regardless of attribution.</strong></p>
<p>What adequate permission looks like, in increasing order of strength:</p>
<p><strong>A reply to a direct request</strong> stating what you want to do with it — which platforms,
whether paid media is included, and for how long. A comment saying *"sure!"* on a vague request covers
very little.</p>
<p><strong>A documented rights request</strong> through a UGC platform that records the grant, which is
worth the cost once volume is material.</p>
<p><strong>A campaign entry mechanism</strong> where the terms of entry grant the licence, stated
plainly rather than buried — this is the cleanest route for anything you plan to use in advertising.</p>
<p>Two things people miss. <strong>A hashtag is not a licence</strong>, whatever the campaign page
implies. And <strong>organic permission does not cover paid use</strong>: running someone's post as an
advert is a different grant and needs to be asked for specifically.</p>
'''),
 S('When Incentives Turn UGC Into Advertising', '''
<p>The moment you give something in exchange for content, the content becomes an endorsement with a
disclosure obligation — and the threshold is lower than most teams assume.</p>
<p><strong>Anything of value counts</strong>: a free product, a discount, a competition entry, a
repost to a large audience, early access. There is no minimum below which it stops being material.</p>
<p><strong>The disclosure has to be in the content</strong>, visible where the claim is, not in your
campaign terms.</p>
<p><strong>And it survives your repost.</strong> If you republish an incentivised post on your own
channel, the disclosure must still be evident to the new audience — a caption you rewrite is a caption
you are responsible for.</p>
<p>The practical arrangement: <strong>put the disclosure requirement in the brief and check compliance
before reposting</strong>, rather than discovering afterwards that a piece of content you amplified was
paid and unlabelled. Indian audiences fall under ASCI's guidelines, US audiences under the FTC's; the
detail differs and the principle does not, so one high standard is simpler to run than two.</p>
''')]),

'codex/social-media/discord-telegram-communities': dict(sources=[DIS], sections=[
 S('Deciding Whether You Need One At All', '''
<p>A branded community is a permanent operational commitment, and most organisations that start one
should not have. Four questions settle it honestly.</p>
<p><strong>Do members have a reason to talk to each other, not just to you?</strong> If every
conversation routes through the brand, you have a support channel with extra steps, and a support
channel is cheaper to run properly.</p>
<p><strong>Is there a moderator with allocated hours?</strong> Not a volunteer, not a marketer's
twenty percent. An unmoderated server fills with spam and becomes a liability visible to everyone you
invited.</p>
<p><strong>Can you sustain it in the quiet months?</strong> Communities have troughs, and a server
where the last message is from six weeks ago actively signals decline.</p>
<p><strong>What happens if it fails?</strong> Closing a community that people invested in costs more
goodwill than never opening one.</p>
<p>If the honest answers are shaky, <strong>a newsletter and a well-run support channel deliver most
of the value at a fraction of the risk.</strong></p>
'''),
 S('Structure and Safety, Which Are the Same Problem', '''
<p>Both platforms allow far more structure than new communities use, and under-structuring is what
makes moderation impossible later.</p>
<p><strong>Fewer channels than you think.</strong> A new server with twenty channels looks empty in
all twenty. Start with three or four and split one when it is genuinely busy.</p>
<p><strong>A gated entry step</strong> — rules acknowledgement, a verification role — removes most
drive-by spam before it arrives, at the cost of some friction. Worth it.</p>
<p><strong>Permissions set deliberately.</strong> Who can post links, mention everyone, create
invites, attach files. The defaults are permissive and the first abuse will use whichever one you left
open.</p>
<p><strong>Written rules, visible, enforced consistently</strong>, with a record of actions taken.</p>
<p>And the obligation that is easy to miss: <strong>if minors may be present, that changes what you
are responsible for.</strong> Age-gate where the platform allows it, be clear about who the space is
for, and ensure reporting routes reach a human quickly. A brand-run space is a space you are answerable
for, in a way that a comment section on someone else's platform is not.</p>
''')]),

'codex/seo/technical/technical-seo-audit': dict(sources=[GSC], sections=[
 S('Writing the Audit So It Gets Implemented', '''
<p>Most technical audits fail after delivery, not during. A hundred-item document arrives, nobody can
start, and it is still open a year later.</p>
<p>What changes that:</p>
<p><strong>Order by impact against effort, not by category.</strong> A section headed
<em>Crawlability</em> is organised for the auditor. A list headed <em>Do these four things first</em>
is organised for the person implementing.</p>
<p><strong>State the business consequence, not the violation.</strong> <em>"No canonical on paginated
URLs"</em> is a finding. <em>"Product pages beyond page one are not being indexed, so roughly a third
of the catalogue cannot be found in search"</em> is a reason to schedule work.</p>
<p><strong>Name the owner and the system for each item.</strong> Developer, CMS, server configuration,
DNS. An audit that does not say who can fix a thing goes to whoever commissioned it and stops.</p>
<p><strong>Separate the one-offs from the standing rules.</strong> Some items are fixes; others are
things the next template must not do again. Only the second kind prevents recurrence.</p>
<p><strong>And cap the first round at ten items.</strong> Ten done beats a hundred documented.</p>
'''),
 S('Verifying That a Fix Actually Landed', '''
<p>The step almost always skipped: confirming that what was deployed matches what was asked for.</p>
<p><strong>Re-crawl the affected URLs specifically</strong>, not the whole site, and check the exact
attribute you asked to change. Fixes are frequently applied to a template that covers fewer pages than
you assumed.</p>
<p><strong>Check the rendered HTML, not the source</strong>, where the change is JavaScript-dependent.
A tag present in the source and absent after rendering has not landed.</p>
<p><strong>Watch index coverage over the following weeks</strong> rather than the day after. Crawling
and reprocessing take time, and declaring a fix failed after 48 hours is the most common false
negative in technical SEO.</p>
<p><strong>Keep a log of what changed and when.</strong> When rankings move two months later, the only
way to connect cause and effect is a dated record — and the alternative is an argument nobody can
settle.</p>
<p>Re-audit cadence: <strong>a full pass annually, a focused pass after any migration, template change
or platform upgrade</strong>, and a standing crawl monthly to catch drift. The monthly crawl is what
finds the problem before it is a project.</p>
''')]),

'codex/analytics-cro/analytics-audit-checklist': dict(sources=[GA4], sections=[
 S('The Checks That Find the Most Damage', '''
<p>Some analytics faults distort everything downstream and are invisible in a dashboard. These are the
ones worth checking first.</p>
<ul>
<li><strong>Duplicate tags.</strong> The same tag firing twice halves bounce and doubles pageviews.
Check the network requests on a few pages rather than trusting the container.</li>
<li><strong>Internal traffic not excluded.</strong> Your own team, your agency, your office. On a
low-traffic site this is a large share of everything.</li>
<li><strong>Self-referrals.</strong> Your own domain appearing as a traffic source means session
continuity is breaking, usually across a subdomain or a payment redirect — which also means
conversions are being credited to the wrong source.</li>
<li><strong>Data retention set to the minimum</strong>, silently limiting historical analysis. Check
it; the default is not what most people want.</li>
<li><strong>Conversions counting the wrong event</strong>, or counting one event multiple times per
session.</li>
<li><strong>Filters applied to the only data view</strong>, with no unfiltered copy. Filtered data is
not recoverable.</li>
</ul>
'''),
 S('Consent, and Why the Numbers Moved', '''
<p>The most common analytics mystery — *traffic dropped and nothing changed* — is usually consent, and
it is worth checking before investigating anything else.</p>
<p><strong>Confirm what happens before a user consents.</strong> Whether tags fire, in what mode, and
whether that behaviour changed when the banner was last updated. A consent tool updated by a
compliance team frequently moves analytics numbers, and nobody connects the two.</p>
<p><strong>Understand what modelled data is.</strong> Where consent mode is active, some of what you
see is estimated rather than observed, and the modelled share varies by region and by traffic volume.
That is not wrong, but <strong>it means a year-on-year comparison spanning a consent change is
comparing two different things.</strong></p>
<p><strong>Check region-specific behaviour</strong> if you have European or other regulated traffic,
where the default should be more restrictive.</p>
<p>And <strong>document the consent configuration alongside the analytics configuration.</strong> They
are usually owned by different people, changed independently, and together they determine every number
the business runs on — which is precisely why nobody notices when one moves.</p>
''')]),

'codex/content-marketing/content-roi-measurement': dict(sources=[], sections=[
 S('Building a Number Finance Will Accept', '''
<p>Content ROI arguments fail because the content team produces a number the finance team cannot
audit. The fix is to make the assumptions explicit rather than the number impressive.</p>
<p><strong>State the cost fully.</strong> Not just freelance fees — the internal time at a loaded
rate, design, tooling, and promotion. A content programme costed at its invoice total understates
itself by a multiple, and an understated cost makes the ROI unbelievable rather than better.</p>
<p><strong>Pick one attribution model and declare it.</strong> Last-click understates content
systematically; first-click overstates it. Whichever you choose, <strong>report the same way every
time</strong> and show what the number would be under the other model. Presenting the flattering model
without saying so is what destroys credibility the first time someone checks.</p>
<p><strong>Value the outcome conservatively.</strong> If a piece generated leads, use your actual
historical close rate and actual average value, not a target.</p>
<p>A defensible modest number survives scrutiny. An impressive one that collapses under a question
costs the programme its budget.</p>
'''),
 S('Compounding, and the Reporting Period Problem', '''
<p>Content's defining economic property is that it keeps working, and standard reporting periods are
structurally unable to see it.</p>
<p>A piece published in month one may deliver most of its value in months six to thirty-six. Judged in
a quarterly review it looks like a cost; judged over its life it may be the best-performing asset the
team produced. <strong>Monthly reporting on a compounding asset systematically recommends cancelling
it.</strong></p>
<p>Three practical responses.</p>
<p><strong>Report by publication cohort, not by calendar month.</strong> Group everything published in
a quarter and track that cohort's cumulative performance forward. This makes compounding visible and
is the single most useful change.</p>
<p><strong>Separate new from existing.</strong> Traffic and leads from pieces older than a year are
the return on past investment; conflating them with this month's output makes both unreadable.</p>
<p><strong>Track the decay curve</strong> so you know when a piece needs updating rather than
replacing — refreshing a decaying performer is usually the highest-return work available and nobody
schedules it.</p>
<p>And be explicit that <strong>some content is a depreciating asset</strong>: news commentary and
campaign pages do not compound, and should not be defended as though they do.</p>
''')]),

'codex/social-media/choosing-social-media-platforms': dict(sources=[], sections=[
 S('Costing a Platform Before You Commit', '''
<p>Platform choice is made as a reach decision and paid for as an operations decision. Cost it
properly first.</p>
<p>The recurring commitments a platform creates, all of which outlast the enthusiasm: <strong>content
production in that platform's native format</strong> — the expensive item, because repurposing reads
as repurposing; <strong>community management</strong>, since an account that does not reply is worse
than no account; <strong>monitoring</strong>, because complaints arrive whether or not you are
listening; and <strong>the platform-specific learning</strong> that takes months and leaves with the
person who has it.</p>
<p>The useful test: <strong>can you sustain this in your busiest month, with one person on
leave?</strong> A cadence that only works when everything is calm is not a cadence.</p>
<p>And run the counterfactual honestly — <strong>what would the same hours produce on the platform you
are already on?</strong> Deepening an existing channel usually beats adding a shallow one, and it is
the comparison nobody makes because adding feels like progress.</p>
'''),
 S('Reviewing and Leaving', '''
<p>Platform decisions are made once and never revisited, so organisations accumulate accounts nobody
chose to keep.</p>
<p><strong>Set review criteria at the start</strong>, while you are objective: what result by when
would justify continuing, and what would mean stopping. Written down, these survive the sunk cost that
will otherwise decide it.</p>
<p><strong>Review twice a year</strong> against those criteria, not against how the platform feels.</p>
<p><strong>Leaving is a legitimate outcome and needs doing properly.</strong> Post a note saying where
the audience can find you, update every link and profile that points there, and — importantly —
<strong>do not delete the account</strong>. A dormant verified account you control is a defence against
someone else taking the handle.</p>
<p>The signals that a platform has run its course: <strong>engagement falling while effort is
constant</strong>, the audience there being one you do not sell to, the format demanding production you
cannot sustain, or nobody able to name what the channel is for. <strong>Any one of those is enough to
review. Two is enough to stop.</strong></p>
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
    print('  ✅ %-52s +%d words, %d sources' % (path.replace('codex/', ''),
          len(re.sub(r'<[^>]+>', ' ', add).split()), len(cfg['sources'])))
print('\n%d pages expanded' % done)
