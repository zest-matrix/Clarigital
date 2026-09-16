#!/usr/bin/env python3
"""cx_expand_01.py — Session 90. First content-remediation batch.

The ten shortest pages in the WRITE bucket of _build/thin-pages.md. Each runs
260-320 words on the `guide-article` template, on a site whose flagship guides
run 2,000+.

WHAT THIS ADDS, AND WHAT IT DOES NOT
  Two further <h2> sections per page, written to be the part the original was
  missing -- almost always the practical layer: how you actually set the thing
  up, and what goes wrong. Not padding. If a page could not be genuinely
  improved it is not in this file.

  A typed sources block ONLY where real, checkable, primary sources exist.
  Four of these ten get one. The other six are methodological pages where the
  honest sources are textbooks and practice, and a weak sources list is worse
  than none -- `an undifferentiated list launders reporting into authority`
  (SOP D2). Saying so here rather than padding the block.

  NO invented figures. Where a number would have carried the point, the
  mechanism is described instead. Nothing on these pages is a statistic I
  could not source.

Splices into the guide-content div with an asserted index, verifies div and
anchor balance and the exact length delta, and re-parses nothing else.
Run from the site root: python3 /tmp/cx_expand_01.py
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

IAB = ('official', 'IAB Tech Lab specifications',
       'the OpenRTB specification and the programmatic deal-type definitions this page uses',
       'iabtechlab.com')
GAM = ('official', 'Google Ad Manager documentation',
       'line item priority, deal negotiation and the delivery forecasting behaviour described here',
       'support.google.com')
IABA = ('official', 'IAB digital audio and podcast measurement guidelines',
        'the download-versus-impression distinction and the technical basis for audio measurement',
        'iabtechlab.com')
FTC = ('official', 'FTC Endorsement Guides',
       'the disclosure obligations for affiliate and endorsement relationships in the United States',
       'ftc.gov')
ASCI = ('official', 'ASCI Guidelines for Influencer Advertising in Digital Media',
        'the disclosure obligations that apply to affiliate and influencer content aimed at Indian audiences',
        'ascionline.in')

S = lambda t, c: (t, c)

PAGES = {

'codex/programmatic/programmatic-direct': dict(sources=[IAB, GAM], sections=[
 S('Setting One Up, Step by Step', '''
<p>The deal itself is a negotiation, but the execution is a specific sequence and it is where most
first attempts stall.</p>
<p>The publisher creates the deal in their ad server and issues a <strong>deal ID</strong>. The buyer
adds that ID to a line item in their DSP. Both sides then have to agree on three things that are easy
to leave vague and expensive to get wrong: <strong>the flight dates</strong>, <strong>the impression
volume</strong>, and <strong>which creative sizes and formats are in scope</strong>.</p>
<p>On the publisher side the line item is given a <strong>priority above open-auction demand</strong>.
That priority is the whole mechanism — it is what converts a price agreement into a delivery
guarantee, because the ad server serves the guaranteed line before it lets the auction compete for
the same impression. A programmatic guaranteed deal running at the same priority as remnant inventory
is not guaranteed; it is a preferred deal with optimistic paperwork.</p>
<p>Before the flight starts, run a <strong>forecast</strong> in the publisher's ad server against the
exact targeting the deal specifies. A forecast run against looser targeting than the deal carries will
say the inventory exists when it does not.</p>
'''),
 S('What Goes Wrong', '''
<p><strong>Under-delivery.</strong> The most common failure, and usually a targeting problem rather
than an inventory problem: the deal was forecast on broad criteria and bought with narrow ones —
viewability floors, brand-safety exclusions or frequency caps applied on the buy side that the
publisher never modelled. Check the buyer's applied targeting against the forecast's, not against the
contract's.</p>
<p><strong>Discrepancy.</strong> Buyer and publisher will count differently, because they count at
different moments in the ad's life. Agree <strong>whose numbers bill</strong> before the flight, and
agree the tolerance. Discovering in week three that the two systems disagree by several per cent is a
commercial conversation nobody has time for mid-campaign.</p>
<p><strong>Creative approval.</strong> A premium publisher will review creative, and that review takes
time you have not scheduled. Submit early.</p>
<p><strong>Priority collisions.</strong> Two guaranteed deals competing for the same narrow inventory
will both under-deliver, and the ad server will not warn you — it will simply serve one and starve the
other. This is a publisher-side planning failure that shows up as a buyer-side complaint.</p>
''')]),

'codex/programmatic/programmatic-audio': dict(sources=[IABA, IAB], sections=[
 S('Creative in Audio Is a Different Discipline', '''
<p>Audio is the one programmatic channel where the creative cannot be skimmed, skipped by an ad
blocker, or seen out of the corner of an eye. It is also the one where the listener is usually doing
something else — driving, cooking, walking — and cannot click.</p>
<p>Three consequences shape production. <strong>The first five seconds carry the brand</strong>,
because there is no logo doing that work in parallel. <strong>A call to action has to survive not
being clickable</strong>, which in practice means a memorable phrase or a spoken URL rather than a
promo code nobody can write down. And <strong>host-read and announcer-read spots behave differently
enough to be treated as separate formats</strong> — a host read borrows the host's credibility and
cannot be reused across shows; an announcer read is portable and does not.</p>
<p>Dynamic ad insertion lets you vary the spot by listener and by moment, which is genuinely useful
and quietly expensive: every variant is a production cost and a QA surface. Decide how many variants
you will actually analyse before you commission them.</p>
'''),
 S('Podcast and Streaming Are Not One Channel', '''
<p>They are bought through similar pipes and they measure fundamentally differently.</p>
<p><strong>Streaming audio</strong> — music services and radio simulcast — behaves like the rest of
programmatic. The ad is served at the moment of listening, so an impression means something close to
what it means in display, and targeting can use the signals the platform holds about the listener.</p>
<p><strong>Podcasts</strong> historically counted <strong>downloads</strong>, which is not the same
thing as a listen: a file can be downloaded automatically and never played. The IAB measurement
guidelines exist precisely to constrain what may be counted, and whether a supplier is certified
against them is the single most useful question to ask before buying.</p>
<p>The practical rule: <strong>do not compare a podcast CPM against a streaming CPM without first
establishing that the denominator means the same thing.</strong> Much of the apparent price
difference between the two is a measurement difference wearing a pricing costume.</p>
''')]),

'codex/programmatic/header-bidding-explained': dict(sources=[IAB, GAM], sections=[
 S('Client-Side, Server-Side, and the Trade You Are Making', '''
<p>Header bidding comes in two architectures and the choice is a straight trade between revenue and
page speed.</p>
<p><strong>Client-side</strong> runs the auction in the visitor's browser. Every demand partner gets
a genuine look, cookie matching works because the call comes from the browser itself, and match rates
stay high. The cost is latency that scales with the number of partners, paid by the visitor. Each
additional partner adds requests to a page that is also trying to render.</p>
<p><strong>Server-side</strong> moves the auction to a server. One call leaves the browser, latency
stops scaling with partner count, and you can add demand without punishing the page. The cost is
cookie matching — the server is a third party to both the browser and the bidder, so match rates fall,
and a bidder that cannot identify the user bids lower or not at all.</p>
<p>Most publishers at scale run <strong>both</strong>: high-value partners client-side where match
rates matter, the long tail server-side where they do not. That hybrid is the standard answer, not a
compromise nobody chose.</p>
'''),
 S('What It Does Not Fix', '''
<p>Header bidding solves a sequencing problem: it lets demand sources compete simultaneously rather
than in a waterfall. It does not solve any of the following, and expecting it to is the usual source
of disappointment.</p>
<p><strong>It does not create demand.</strong> If three partners want your inventory, adding a fourth
auction mechanism does not make it four. Revenue lift comes from competition that was previously
suppressed by the waterfall, and that lift is finite.</p>
<p><strong>It does not fix inventory quality.</strong> Below-the-fold placements with poor viewability
bid poorly in a unified auction for the same reason they bid poorly in a waterfall.</p>
<p><strong>It does not reduce fees — it relocates them.</strong> Every additional intermediary in the
chain takes a margin, and a publisher who adds partners without auditing the chain can increase gross
revenue and reduce net.</p>
<p><strong>And it adds an operational burden that is permanent.</strong> Timeouts, price floors and
partner performance need ongoing attention. A configuration that was correct a year ago is a
configuration nobody has looked at.</p>
''')]),

'codex/programmatic/programmatic-tv-ctv': dict(sources=[IAB, IABA], sections=[
 S('Why CTV Frequency Is So Hard to Control', '''
<p>The complaint about connected TV is almost always the same: the same viewer sees the same ad far
too many times. The cause is structural rather than a settings error.</p>
<p>Inventory for one show reaches a buyer through several routes at once — the publisher's own app,
an aggregator, a device manufacturer's platform, a virtual MVPD. <strong>Each route is a separate
supply path with its own identifier for the same household</strong>, and a frequency cap set in one
DSP can only count the impressions it can see.</p>
<p>There is no universal identifier doing the work a cookie once did on the web. Device
graph matching helps and is probabilistic, which means it is wrong some of the time in both
directions.</p>
<p>Practical mitigations, in order of how much they actually help: <strong>consolidate buying into
fewer DSPs</strong>, because a cap works within a platform and not across them; <strong>buy through
fewer supply paths</strong> for the same inventory; and <strong>set the cap materially lower than
your intended exposure</strong>, because the observed frequency will exceed the set frequency.</p>
'''),
 S('Measuring It Without Fooling Yourself', '''
<p>CTV has no click. Everything downstream of the impression is inference, and the quality of that
inference is the whole measurement question.</p>
<p><strong>Completion rate</strong> is the metric most often quoted and the least informative. Most
CTV inventory is non-skippable, so completion approaches total by construction. A completion rate
near total tells you the format was non-skippable, not that the ad worked.</p>
<p><strong>Incrementality</strong> is what you actually want, and geographic holdout testing is the
most robust way to get it — withhold spend in matched regions and compare. It is slow, it costs
reach, and it is the only method that answers the question directly.</p>
<p><strong>Attribution by household IP</strong> connecting an ad exposure to a later visit on another
device is useful and systematically generous. It cannot distinguish the household member who saw the
ad from the one who searched, and it credits exposure that changed nothing.</p>
<p>Use it directionally. Do not let it settle a budget argument on its own.</p>
''')]),

'codex/affiliate-marketing/b2b-affiliate-marketing': dict(sources=[FTC, ASCI], sections=[
 S('The Cookie Window Problem', '''
<p>The single structural difference between B2B and consumer affiliate marketing is time. A consumer
purchase is often decided in a session. A business purchase involves several people, a budget cycle
and a procurement process, and the gap between the first click and the closed deal is routinely
measured in months.</p>
<p>Standard affiliate cookie windows are not built for that. A thirty-day window on a four-month sales
cycle does not under-credit affiliates slightly — <strong>it excludes most of them entirely</strong>,
and the ones it does credit are the ones who happened to touch the deal last.</p>
<p>Two responses work. <strong>Extend the window</strong> to match the actual observed cycle, which
requires knowing what that cycle is rather than assuming. Or <strong>move the conversion event
earlier</strong> and pay on a qualified lead, a booked demo or a trial start instead of on closed
revenue — accepting that you are now paying for something that does not always become a customer, and
pricing accordingly.</p>
<p>The second is more common in practice because it is easier to attribute honestly, and because an
affiliate who waits four months for a commission stops promoting long before it arrives.</p>
'''),
 S('Which Partners Actually Produce Pipeline', '''
<p>B2B affiliate programmes attract three quite different partner types and they do not perform
alike.</p>
<p><strong>Review and comparison sites</strong> capture buyers already in a category and comparing
options. High intent, high conversion, and they will want placement economics rather than a pure
performance deal once you matter to them.</p>
<p><strong>Consultants and agencies</strong> who implement your category of product carry real
influence, because they are advising on the decision rather than intercepting it. They are also the
hardest to recruit through a generic programme, and usually need a direct relationship.</p>
<p><strong>Content publishers and newsletters</strong> in the professional niche reach buyers before
the comparison stage. Slower to convert, and the only one of the three that builds demand rather than
capturing it.</p>
<p>Disclosure obligations attach to all three. A recommendation made for a commission has to be
identifiable as such, and a business audience is not a carve-out — the obligation follows the
relationship, not the sophistication of the reader.</p>
''')]),

'codex/affiliate-marketing/influencer-affiliate-marketing': dict(sources=[ASCI, FTC], sections=[
 S('Structuring the Deal So Both Sides Can Live With It', '''
<p>Pure affiliate terms rarely work with an established creator, for a reason that is easy to miss:
the creator carries all the risk of a product that does not convert, on an audience they spent years
building. Pure flat fees have the opposite problem — the brand carries all of it.</p>
<p>The arrangement that survives contact with both parties is usually a <strong>base fee plus
commission</strong>. The base covers production and the opportunity cost of the slot; the commission
gives the creator a reason to make the integration good rather than perfunctory.</p>
<p>Three terms are worth getting explicit because they are the ones that turn into disputes.
<strong>Usage rights</strong>: whether you may run the creator's content as paid media, where, and
for how long — this is frequently worth more than the commission and is frequently left unsaid.
<strong>Exclusivity</strong>: for how long the creator will not promote a direct competitor, priced
accordingly. And <strong>content approval</strong>: a brand that demands line-by-line approval will
get content that sounds like a brand, which is the thing the audience is not there for.</p>
'''),
 S('Disclosure, and Why the Link Type Does Not Change It', '''
<p>The obligation attaches to the <strong>relationship</strong>, not to the mechanism. A creator paid
a commission has a material connection to disclose whether the link is a tracked affiliate link, a
discount code, a swipe-up, or a spoken mention with no link at all.</p>
<p>What follows from that in practice:</p>
<ul>
<li><strong>A discount code is a paid relationship.</strong> Codes are frequently treated as somehow
softer than links. They are not.</li>
<li><strong>The disclosure has to be where the claim is.</strong> In a video, said and shown near the
recommendation — not only in a description most viewers never open.</li>
<li><strong>It has to be understandable.</strong> Platform tags help; a string of hashtags at the end
of a caption does not.</li>
<li><strong>It survives reposting.</strong> A story clip reshared without the disclosure is still a
paid recommendation.</li>
</ul>
<p>Indian audiences fall under ASCI's influencer guidelines; US audiences under the FTC endorsement
guides. The two differ in detail and agree on the principle, so a single high standard is simpler to
run than two.</p>
''')]),

'codex/affiliate-marketing/affiliate-programme-management': dict(sources=[FTC, ASCI], sections=[
 S('The Small Number of Partners That Matter', '''
<p>Every mature affiliate programme has the same shape: a handful of partners produce most of the
revenue, a long tail produces almost none, and the management effort is usually distributed the wrong
way round.</p>
<p>The useful discipline is to <strong>segment the programme and manage each tier differently</strong>.
The top partners deserve direct relationships, bespoke commercial terms, advance notice of promotions
and early access to product news. Treating them identically to a partner who has produced two sales is
how you lose them to a competitor who does not.</p>
<p>The middle tier is where growth actually comes from, and it responds to attention: a conversation
about what is converting, better creative, a tailored offer. The long tail should be automated
entirely — self-service onboarding, standard terms, no manual effort — because the cost of managing it
individually exceeds what it returns.</p>
<p><strong>Review the tiers on a schedule.</strong> Partners move between them, and a tiering nobody
has revisited in a year is describing last year's programme.</p>
'''),
 S('Policing It Without Poisoning It', '''
<p>Affiliate fraud is mostly not exotic. It is a small number of recognisable behaviours, and the
programme terms are where you address them — before they happen, not after.</p>
<p><strong>Brand bidding</strong> is the most common dispute. An affiliate bidding on your brand name
in search intercepts traffic that was already yours and charges you a commission for it. Decide your
position explicitly, write it into the terms, and monitor it, because a policy nobody checks is an
invitation.</p>
<p><strong>Cookie stuffing</strong> — dropping tracking cookies without a genuine click — shows up as
an implausible click-to-conversion ratio. <strong>Coupon-site last-click capture</strong> is not fraud
at all, but it does mean a partner is being paid for a conversion that was already going to happen;
the answer is commission tiering by partner type rather than accusation.</p>
<p>And <strong>trademark misuse in ad copy</strong> is a legal exposure as much as a commercial one.</p>
<p>Enforce consistently. A programme that tolerates a rule for a large partner and enforces it against
a small one has no rule, and the partners will work that out faster than you do.</p>
''')]),

'codex/business-strategy/customer-segmentation': dict(sources=[], sections=[
 S('Building One That Survives Contact With the Business', '''
<p>A segmentation is only useful if someone can act on it, and the most common failure is a beautiful
analysis that nobody can operationalise.</p>
<p>Work backwards from the decision. <strong>Ask what will be done differently for each segment
before you build it.</strong> If the answer is nothing, or if the answer is the same for every
segment, the segmentation is a description rather than a tool. This single question kills most
proposed segmentations and saves the effort.</p>
<p>Then check three properties. <strong>Identifiable</strong>: can you tell which segment a given
customer is in, from data you actually hold, at the moment you need to know? A segment defined by
attitudes you measured in a survey cannot be applied to an inbound visitor.
<strong>Substantial</strong>: is it large enough to justify treating differently?
<strong>Stable</strong>: will membership hold long enough for the treatment to pay back?</p>
<p>A segmentation that fails identifiability is the most common and the most expensive, because it
usually fails at the end of the project rather than the beginning.</p>
'''),
 S('Why Segmentations Decay, and What To Do About It', '''
<p>Segmentations are built once and then quietly stop describing reality. Three mechanisms do most of
the damage.</p>
<p><strong>The market moves.</strong> Segments defined by behaviour around a channel, a price point or
a competitor set stop meaning what they meant when any of those change.</p>
<p><strong>Your own actions move it.</strong> This is the one people miss. If you treat a segment
differently, you change its behaviour — which changes the data the segmentation was derived from. A
successful segmentation invalidates itself, and the more effective it is the faster it does so.</p>
<p><strong>The data changes underneath it.</strong> A field is deprecated, a tracking method changes,
a consent regime removes a signal. The model keeps running and its inputs no longer mean the same
thing.</p>
<p>The practical response is not to rebuild constantly. It is to <strong>track segment sizes and
segment-level behaviour over time as a standing report</strong>, and to treat a drifting distribution
as the trigger for a rebuild. A segmentation with no monitoring attached will be wrong long before
anyone notices, and the first sign will be a campaign that mysteriously stops working.</p>
''')]),

'codex/content-marketing/content-localisation': dict(sources=[], sections=[
 S('What It Costs, and Where the Cost Actually Sits', '''
<p>Localisation budgets are usually built around translation, which is the cheapest part and getting
cheaper. The expensive parts are the ones nobody lists.</p>
<p><strong>Review by someone who knows the market</strong> is the line that matters. A translation is
correct; a market reviewer tells you that the correct translation is off-register, that the example
means nothing locally, or that the claim you make routinely at home is not made in that market. This
is a recurring cost per piece, not a one-off.</p>
<p><strong>Visual and layout rework.</strong> Text length changes substantially between languages.
Layouts built to one language's word length break in another, and the fix is design time rather than
translation time.</p>
<p><strong>Ongoing maintenance</strong> is the cost that ends most localisation programmes. Every
update to the source now has to propagate to every locale. A programme that localises a hundred pages
into four languages has not created four hundred pages — it has created a maintenance obligation on
five hundred, forever.</p>
<p>Localise less, deeper. A small number of properly maintained locales beats a large number of
decaying ones.</p>
'''),
 S('The Signals That Tell You It Is Working', '''
<p>Localisation is easy to do and hard to evaluate, because the obvious metric — traffic in the target
market — moves for reasons that have nothing to do with quality.</p>
<p>More useful signals, in rough order of reliability:</p>
<ul>
<li><strong>Engaged time on localised pages versus the source-language equivalent in the same
market.</strong> If local visitors spend longer on the English page, the localisation is worse than
nothing and is actively getting in the way.</li>
<li><strong>Conversion rate by locale, compared against itself over time</strong>, not against other
locales — markets differ for reasons localisation cannot fix.</li>
<li><strong>Search visibility for terms people in that market actually use</strong>, which is the test
of whether you localised the keyword research or only the copy. This is the most common gap: the
content is translated and the topic was chosen for a different market.</li>
<li><strong>Support contacts in-language</strong>, which rise when localisation works and reveals
demand the organisation may not be staffed for.</li>
</ul>
<p>That last one is worth anticipating. Localised marketing with unlocalised support produces a worse
customer experience than no localisation at all.</p>
''')]),

'codex/ecommerce/ecommerce-returns-management': dict(sources=[], sections=[
 S('Returns as a Data Source, Not Just a Cost', '''
<p>Most return policies are designed to minimise returns. The better ones are designed to
<strong>learn from them</strong>, because a return is the most honest feedback a customer ever gives
you and it arrives with a reason attached.</p>
<p>The prerequisite is a reason taxonomy that distinguishes causes you can act on.
<strong>Wrong size</strong> is a sizing-guidance problem. <strong>Not as described</strong> is a
listing problem, and it is the one that predicts a review problem.
<strong>Damaged</strong> is packaging or carrier. <strong>Changed mind</strong> is often a targeting
problem — the wrong customer was persuaded. A single "returned" flag tells you the cost and none of
the cause.</p>
<p>Analyse those reasons <strong>by product and by acquisition channel</strong>. A product with an
unusual return rate has a listing or a quality problem. <strong>A channel with an unusual return rate
has a promise problem</strong>, and that is the finding worth having: it usually means the campaign is
overselling, and the return rate is the cost of a conversion rate somebody is being congratulated
for.</p>
'''),
 S('Designing the Policy Around the Category', '''
<p>A generous returns policy raises conversion and raises returns. Which effect dominates depends on
the category, and copying another retailer's policy is how you import their economics without their
cost base.</p>
<p><strong>High-consideration, high-margin goods</strong> generally benefit from generosity: the
conversion lift on an uncertain purchase outweighs the return cost, and the customer who keeps the
item is worth a lot.</p>
<p><strong>Low-margin, high-bulk goods</strong> often cannot support free returns at all, because the
reverse logistics cost approaches the item's margin. The honest answer here is usually to fix the
reason for returns rather than to subsidise them.</p>
<p><strong>Fashion</strong> is its own problem, because bracketing — ordering several sizes intending
to keep one — is rational customer behaviour that the policy itself created. Better size guidance,
fit data and honest imagery reduce returns more than restrictive terms do, and without the conversion
penalty.</p>
<p>Whatever you choose, <strong>state it plainly and early</strong>. A policy discovered at checkout
costs a conversion; a policy discovered after delivery costs a customer.</p>
''')]),
}

ANCHOR = '</div>\n    <aside class="guide-sidebar">'
done = 0
for path, cfg in PAGES.items():
    f = path + '/index.html'
    assert os.path.exists(f), 'missing ' + f
    src = io.open(f, encoding='utf-8').read()
    if 'id="sources"' in src or cfg['sections'][0][0] in src:
        print('  = already expanded: ' + path); continue
    add = ''.join('<h2>%s</h2>\n%s\n' % (t, c) for t, c in cfg['sections'])
    add += sources_block(cfg['sources'])
    n = src.count(ANCHOR)
    assert n == 1, '%s: anchor appears %d times' % (f, n)
    i = src.find(ANCHOR)
    out = src[:i] + add + src[i:]
    assert len(out) == len(src) + len(add), 'length delta wrong'
    assert out.count('<div') == src.count('<div') + add.count('<div'), 'div open moved'
    assert out.count('</div>') == src.count('</div>') + add.count('</div>'), 'div close moved'
    assert out.count('<a ') == src.count('<a ') + add.count('<a '), 'anchor count moved'
    assert len(re.findall(r'<h1[\s>]', out)) == 1, 'h1 count moved'
    assert out.count('</html>') == 1 and out.count('</body>') == 1, 'document truncated'
    io.open(f, 'w', encoding='utf-8').write(out)
    done += 1
    words = len(re.sub(r'<[^>]+>', ' ', add).split())
    print('  ✅ %-56s +%d words %s' % (path, words, '+sources' if cfg['sources'] else '(no sources: see docstring)'))
print('\n%d pages expanded' % done)
