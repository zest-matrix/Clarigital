#!/usr/bin/env python3
"""cx_expand_02.py — Session 92. Second content-remediation batch, eleven pages.

Target is the S91 decision: 600+ content words of the part that was missing,
not 800. Two <h2> sections each, written as the practical and failure layer
the originals skipped. Typed sources only where a real primary source exists;
two pages get none and the reason is the same as batch one (SOP D2).

No invented figures. Where a number would have carried a point, the mechanism
is described instead.
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
from guide_builder import sources_block

FTC = ('official', 'FTC Endorsement Guides',
       'the disclosure obligations attaching to affiliate and endorsement relationships in the United States',
       'ftc.gov')
ASCI = ('official', 'ASCI Guidelines for Influencer Advertising in Digital Media',
        'the disclosure obligations for affiliate and influencer content aimed at Indian audiences',
        'ascionline.in')
GSC = ('official', 'Google Search Central documentation',
       'canonicalisation, duplicate handling, and how Google selects a canonical URL',
       'developers.google.com')
IAB = ('official', 'IAB Tech Lab content taxonomy and specifications',
       'the standard content categories contextual systems classify against',
       'iabtechlab.com')
AMZ = ('official', 'Amazon Seller Central and Flipkart Seller Hub documentation',
       'listing requirements, image specifications and the fee structures described here',
       'sellercentral.amazon.in')
GMC = ('official', 'Google Merchant Center product data specification',
       'the image requirements a product feed must satisfy to remain eligible',
       'support.google.com')
EMAIL = ('official', 'CAN-SPAM Rule and the GDPR consent and transparency provisions',
         'the consent, identification and unsubscribe obligations that apply to automated commercial email',
         'ftc.gov')
SNAP = ('official', 'Snap for Business documentation',
        'Public Profile eligibility, Spotlight distribution and Lens publishing described here',
        'forbusiness.snapchat.com')

S = lambda t, c: (t, c)

PAGES = {

'codex/ecommerce/ecommerce-marketplace-strategy': dict(sources=[AMZ], sections=[
 S('The Unit Economics Nobody Models Before Listing', '''
<p>Marketplace margin is not the platform commission. It is the commission plus everything the
platform charges around it, and sellers routinely discover the difference after their first quarter.</p>
<p>The costs that actually compound: <strong>the referral or commission fee</strong> on the sale;
<strong>fulfilment fees</strong> if you use the platform's logistics, charged by weight band, so a
product that sits just over a band boundary costs materially more than one just under;
<strong>storage fees</strong> that escalate for slow-moving stock; <strong>return shipping</strong>,
which on a generous-returns marketplace is a volume cost rather than an exception;
<strong>advertising</strong>, which stops being optional once a category is competitive; and
<strong>payment settlement timing</strong>, which is a working-capital cost rather than a fee.</p>
<p>Model the product-level contribution after all of them <strong>before</strong> you list, and model
it at your expected return rate rather than at zero. A product with healthy gross margin and a high
return rate can be loss-making at volume, and the marketplace dashboard will not tell you — it reports
revenue, not contribution.</p>
'''),
 S('Owning the Customer When the Platform Does Not Let You', '''
<p>The structural trade of marketplace selling is that the platform owns the customer relationship.
You get demand you could not have bought; you do not get the email address, the repeat purchase, or
the ability to speak to the buyer directly.</p>
<p>What actually works within the rules is narrower than most advice suggests. <strong>Packaging
inserts</strong> that offer genuine value — a registration for a warranty, a guide to using the
product — can move a buyer onto your own channel, provided they do not solicit a review or disparage
the platform. <strong>Brand registration programmes</strong> give you control of the listing content
and some analytics. <strong>Building a brand people search for by name</strong> is the slowest route
and the only durable one, because branded demand follows you across channels.</p>
<p>What does not work: asking for reviews in exchange for anything, contacting buyers outside the
platform's messaging system, or including your own storefront URL where the platform forbids it.
These get accounts suspended, and a suspension on a channel carrying most of your revenue is an
existential event rather than a setback. <strong>Treat marketplace dependence as concentration risk
and measure it</strong> — the share of revenue from one platform is a number your business should
know and most do not.</p>
''')]),

'codex/affiliate-marketing/email-affiliate-marketing': dict(sources=[FTC, ASCI, EMAIL], sections=[
 S('Deliverability Is the Constraint, Not Creativity', '''
<p>Affiliate content stresses email deliverability in ways ordinary marketing does not, and a sender
who ignores this discovers it as a sudden and unexplained collapse in open rates.</p>
<p>Three mechanisms do the damage. <strong>Affiliate link domains carry reputation</strong> —
redirect and tracking domains shared across many senders inherit the behaviour of the worst of them,
and a link shortener with a poor history can affect your placement regardless of your own conduct.
<strong>Promotional density</strong> shifts your mail into the promotions tab or the spam folder:
a list conditioned to expect useful content will tolerate commercial mail and will not tolerate only
commercial mail. And <strong>engagement decay</strong> compounds, because mailbox providers weight
recent recipient behaviour heavily and an unengaged segment drags the whole domain.</p>
<p>Practical mitigations: use your own tracking domain where the programme allows it, authenticate
properly so your mail is attributable to you, and <strong>segment aggressively by engagement</strong>
— mailing an unresponsive segment to hit a revenue number costs you the responsive one.</p>
'''),
 S('Disclosure in a Medium With No Hover State', '''
<p>Email removes the affordances other channels rely on for disclosure. There is no hover preview of
a destination, no platform-native paid-partnership label, and no consistent rendering across clients.
The obligation does not relax to compensate.</p>
<p>What that means in practice:</p>
<ul>
<li><strong>Disclose near the top and near the link</strong>, not only in a footer. A reader who acts
on the first recommendation never reaches the footer.</li>
<li><strong>Make it legible as text</strong>. A disclosure in an image fails for anyone with images
blocked by default, which is a large share of recipients.</li>
<li><strong>It applies to the forwarded copy too.</strong> Email is forwarded and archived; a
disclosure that depends on the original context does not survive.</li>
<li><strong>The commercial relationship also engages email law separately</strong> — consent,
accurate sender identification and a working unsubscribe are obligations regardless of the affiliate
question, and affiliate revenue makes a message commercial for those purposes.</li>
</ul>
<p>The simplest defensible pattern is a short plain-text line immediately above the first
recommendation, in the same typeface as the body copy, saying plainly that the links earn a
commission.</p>
''')]),

'codex/affiliate-marketing/saas-affiliate-marketing': dict(sources=[FTC, ASCI], sections=[
 S('Churn Makes the Commission Model the Hard Part', '''
<p>SaaS affiliate programmes fail on commission design more often than on recruitment, because a
subscription can be refunded, downgraded or churned after the commission is paid.</p>
<p>Three structures, each with a failure mode worth understanding before choosing.
<strong>Recurring commission</strong> — a share of revenue for as long as the customer pays —
aligns the affiliate with retention and is the most attractive to serious partners. It is also the
hardest to forecast and the most expensive at scale, and it creates a liability that outlives the
relationship.</p>
<p><strong>One-time commission</strong> is simple and predictable and gives the affiliate no reason to
care whether the customer sticks, which shows up as poor-fit referrals.
<strong>Hybrid</strong> — a larger first payment plus a smaller recurring share — is the common
compromise and usually the right one.</p>
<p>Whichever you choose, <strong>a clawback window is not optional</strong>. Define the period, make
it visible in the terms, and set it against your actual observed refund and early-churn curve rather
than a round number. An affiliate who discovers a clawback they were not told about does not stay.</p>
'''),
 S('Free Trials Break the Attribution You Think You Have', '''
<p>The SaaS funnel inserts a delay and a decision between the click and the money, and standard
affiliate tracking was not designed for it.</p>
<p>A user clicks an affiliate link, starts a free trial, uses the product for two weeks across
several devices, and converts from a billing email on a different browser. <strong>Last-click
attribution will credit nobody</strong>, and the affiliate will tell you their referrals are not
being tracked. They are usually right.</p>
<p>The fix is to <strong>attribute at trial start rather than at payment</strong>, stamp the referral
onto the account record at signup, and carry it through to conversion server-side. That removes the
dependence on a cookie surviving a fortnight and a device change. It also means you are paying on
conversion but attributing on signup, which is the correct separation.</p>
<p>Two further details that cause disputes. <strong>Self-serve upgrades months later</strong> — decide
explicitly whether an affiliate is credited when a customer they referred on a free plan upgrades a
year on, and write it down. And <strong>sales-assisted deals</strong>: if a referred trial becomes an
enterprise contract closed by your sales team, the affiliate terms should already say what happens,
because settling it afterwards satisfies nobody.</p>
''')]),

'codex/ecommerce/ecommerce-international': dict(sources=[], sections=[
 S('Landed Cost Is the Whole Proposition', '''
<p>Cross-border e-commerce fails at checkout more than it fails at acquisition, and the cause is
almost always the same: the customer sees one price on the product page and a materially different
one at the end.</p>
<p><strong>Landed cost</strong> is the item price plus shipping plus duty plus import tax plus any
broker or handling fee. Presenting anything less than that as the price is a promise you will break.</p>
<p>Two models, and the choice is strategic rather than operational.
<strong>Delivered duty paid</strong> means you calculate and collect everything at checkout and the
parcel arrives with nothing to pay. It is more work, it requires accurate duty classification, and it
converts far better because the customer's experience matches the promise.
<strong>Delivered at place</strong> means the carrier collects duty on delivery. It is simpler for
you and it produces refused parcels, support contacts and negative reviews from customers who feel
ambushed — and a refused international parcel costs you twice.</p>
<p>If you cannot do the first properly, <strong>say clearly on the product page that duty is payable
on delivery</strong>. A disclosed surprise is not a surprise.</p>
'''),
 S('Why the Second Market Is Harder Than the First', '''
<p>Most international programmes are planned as a sequence of identical launches and are not. The
second market costs more than the first in ways the plan rarely captures.</p>
<p><strong>Operations stop being a project and become a process.</strong> One extra market is a
launch; three is a function — returns processing in each region, local customer contact in the right
hours, and stock allocation decisions nobody owned before.</p>
<p><strong>Every market adds a maintenance obligation, not just a setup cost.</strong> Prices,
shipping tables, tax rules and content all need upkeep, and they need it whether or not the market is
performing.</p>
<p><strong>Payment mix differs more than people expect</strong>, and a market where your preferred
method has low penetration will underperform for reasons that look like demand and are not. Check
which methods dominate locally before concluding the product does not sell there.</p>
<p>The practical rule is the same one that governs localisation: <strong>fewer markets, properly
served, beat more markets thinly served.</strong> Pick the second market because the evidence points
at it, not because it was next on a list.</p>
''')]),

'codex/ecommerce/ecommerce-email-automation': dict(sources=[EMAIL], sections=[
 S('Sequencing Flows So They Do Not Collide', '''
<p>Each flow works in isolation and the trouble starts when a customer qualifies for several at once.
A buyer who abandons a cart, then purchases, then browses again can receive an abandonment reminder,
a purchase confirmation, a review request and a browse-abandonment message inside a day.</p>
<p>The fix is a <strong>priority order and a global frequency cap</strong> applied above the
individual flows, not inside them.</p>
<p>A workable priority, highest first: <strong>transactional</strong> messages always send — order
confirmations and shipping updates are expected and exempt from suppression.
<strong>Post-purchase</strong> outranks acquisition, because a message about something already bought
is more relevant than one about something not yet bought. <strong>Abandonment</strong> flows should
<em>exit immediately on purchase</em>, which sounds obvious and is the most common defect in a live
setup. <strong>Win-back and broadcast</strong> come last and should be suppressed for anyone active
in another flow.</p>
<p>Test the collision cases deliberately: abandon then buy, buy then abandon, buy twice. Each should
produce a sequence a person would recognise as sensible.</p>
'''),
 S('Consent, Identification and the Unsubscribe That Has to Work', '''
<p>Automation multiplies whatever your consent practice is. A flawed list-building method sends one
bad message manually and thousands automatically.</p>
<p>Three obligations carry across jurisdictions even where the detail differs.
<strong>Consent</strong> has to be given for marketing specifically — a checkout that collects an
email to deliver an order has not obtained marketing consent by implication, and a pre-ticked box is
not consent in regimes that require it to be freely given.
<strong>Identification</strong> means the message says clearly who is sending it, with a genuine
postal contact.
<strong>Unsubscribe</strong> must work, must be easy, and must take effect promptly across every flow
— not only the one the recipient was reading.</p>
<p>That last point is the one automation breaks. An unsubscribe honoured by the broadcast tool but not
by the transactional-adjacent flows produces exactly the complaint that damages a sending domain.
<strong>Test the unsubscribe from inside each automated flow</strong>, not from a newsletter, and
confirm the suppression propagates everywhere before the flow goes live.</p>
''')]),

'codex/ecommerce/ecommerce-product-photography': dict(sources=[GMC, AMZ], sections=[
 S('Specification Before Aesthetics', '''
<p>Product imagery is judged twice: by a human and by a feed validator, and the second one rejects
silently. A listing disapproved on image grounds does not fail loudly — it simply stops appearing.</p>
<p>The constraints that most often cause rejection are mechanical rather than artistic.
<strong>Minimum dimensions</strong>, which differ between marketplace listings and shopping feeds.
<strong>Background requirements</strong> — the main image is usually required to be on plain white
with the product filling most of the frame.
<strong>Prohibited overlays</strong>: promotional text, watermarks, borders, logos and calls to
action are disallowed on primary images almost everywhere, and are the single most common cause of
disapproval.
<strong>Accurate representation</strong> — the image must show what is actually sold, so a picture
showing accessories not included in the box is a compliance problem rather than a marketing choice.</p>
<p><strong>Build the specification into the shoot brief</strong>, not into a retouching pass
afterwards. Re-shooting because the framing left too little product in frame is expensive; cropping
to fix it usually is not possible at the required resolution.</p>
'''),
 S('The Shot List That Actually Sells', '''
<p>Beyond the compliant primary image, the secondary images do the persuading, and the useful ones
answer the questions that otherwise become returns or support contacts.</p>
<ul>
<li><strong>Scale.</strong> The product next to something with a known size. Ambiguous scale is one of
the most common causes of a wrong-expectation return.</li>
<li><strong>Detail.</strong> Material, texture, finish, stitching — close enough to answer
&ldquo;what is this actually made of&rdquo;.</li>
<li><strong>In use.</strong> Context that shows the product doing its job, which also communicates
size implicitly.</li>
<li><strong>What is in the box.</strong> Every component laid out. This single image removes a
recurring class of complaint.</li>
<li><strong>Dimensions.</strong> A clean diagram with measurements, where relevant.</li>
</ul>
<p>On <strong>AI-generated and AI-edited imagery</strong>, the rule follows from accurate
representation rather than from any prohibition on the technique: <strong>background replacement and
cleanup are ordinarily fine; altering the product itself is not.</strong> An image that makes the
product look different from the item shipped creates returns, reviews and a disclosure problem, and
the fact that a model rather than a retoucher produced it changes nothing.</p>
''')]),

'codex/programmatic/contextual-targeting-programmatic': dict(sources=[IAB], sections=[
 S('Where Contextual Classification Still Fails', '''
<p>Modern contextual analysis reads the page rather than matching keywords, which fixed most of the
crude failures. The ones that remain are worth knowing because they are the ones that reach a brand
safety report.</p>
<p><strong>Irony, quotation and reporting.</strong> An article quoting something offensive in order to
criticise it classifies on the quoted words. Systems have improved and this remains the hardest case.</p>
<p><strong>Timing.</strong> Classification happens after content is published and crawled. On a page
that updates rapidly — a live blog, a comment-heavy article — the classification can describe the
page as it was rather than as it is.</p>
<p><strong>Thin and dynamic pages.</strong> A listing page assembled at request time may carry too
little stable text to classify confidently, and a system that returns low confidence is usually
treated as a pass by default.</p>
<p><strong>Language and locale.</strong> Classification quality is uneven across languages, and a
taxonomy built for one market applies awkwardly to another. For Indian inventory in particular,
check how a vendor handles multilingual and transliterated content before buying at scale.</p>
'''),
 S('Buying It Without Fooling Yourself About Reach', '''
<p>Contextual is frequently sold as a like-for-like replacement for audience targeting. It is not,
and the difference shows up as a reach shortfall three weeks into a campaign.</p>
<p>An audience segment follows a person across every page they visit. A contextual segment exists
only where matching content exists — so <strong>the addressable inventory is bounded by publishing
volume on your topic</strong>, not by the number of people interested in it. A narrow, brand-safe
contextual segment on a niche subject can be too small to spend against, and will silently
under-deliver rather than fail.</p>
<p>Three things to establish before committing budget. <strong>Forecast the segment</strong> in the
platform against your actual exclusions, not a generic estimate. <strong>Ask how the taxonomy maps
to standard categories</strong>, because vendor-specific categories are difficult to compare and
impossible to port. And <strong>ask what happens on low confidence</strong> — whether the impression
is included or excluded by default, which quietly determines both your reach and your risk.</p>
<p>Used well, contextual is a complement: it reaches people in a relevant moment regardless of what is
known about them, which is exactly where audience targeting is weakest.</p>
''')]),

'codex/social-media/social-commerce': dict(sources=[], sections=[
 S('The Operational Load Nobody Budgets For', '''
<p>Social commerce is usually approved as a marketing initiative and lands as an operations one. The
storefront is the easy part; what follows it is not.</p>
<p><strong>Catalogue synchronisation</strong> has to be continuous. A product that sells out on your
site and stays live on a social storefront produces an order you cannot fill, and platforms penalise
cancellation rates.</p>
<p><strong>Comments and direct messages become a sales channel with an expectation of speed.</strong>
A question on a shoppable post at nine in the evening is a purchase intent with a short half-life, and
it does not route to your helpdesk unless somebody builds that.</p>
<p><strong>Returns arrive through a different door.</strong> The platform's buyer protection terms may
differ from your own policy, and where they do, theirs generally governs the transaction.</p>
<p>The honest test before launching: <strong>who owns the inbox, and what is the response target after
hours?</strong> If there is no answer, the storefront will generate demand you visibly fail to serve,
which is worse than not being there.</p>
'''),
 S('What to Measure, Given the Platform Reports Generously', '''
<p>Platform-reported social commerce performance is measured by the party selling the advertising, and
the standard metrics flatter it in predictable ways.</p>
<p>Two adjustments make the numbers usable. <strong>Compare view-through and click-through conversions
separately</strong> rather than accepting a blended figure, because view-through credit on a platform
with enormous reach will attribute purchases that were happening anyway.
<strong>Watch your own total revenue, not just the attributed portion</strong> — if platform-attributed
sales rise while total sales do not, the channel is reallocating credit rather than creating demand.</p>
<p>The measurement that actually settles the question is the same one that settles it for connected
TV: <strong>a holdout</strong>. Turn the channel off in a matched region or audience for a defined
period and observe total revenue. It is unpopular, it costs real sales, and it is the only method that
answers the question without asking the seller to mark their own work.</p>
<p>For a channel small enough that a holdout is impractical, be honest that the number is directional
and do not let it justify a budget shift it cannot support.</p>
''')]),

'codex/seo/technical/duplicate-content-canonicalisation': dict(sources=[GSC], sections=[
 S('When Google Ignores Your Canonical, and Why', '''
<p>A canonical tag is a <strong>hint, not a directive</strong>. Google selects a canonical itself and
will override yours. Understanding the override conditions saves a great deal of wasted diagnosis.</p>
<p>The common reasons a declared canonical is disregarded: <strong>the target differs substantially in
content</strong>, so the pages are not duplicates and the declaration is simply wrong;
<strong>conflicting signals</strong>, where internal links, the sitemap and hreflang point somewhere
else than the tag does; <strong>the canonical target is non-indexable</strong>, whether noindexed,
blocked in robots.txt or returning an error; <strong>canonical chains</strong>, where A points to B
which points to C; and <strong>a relative URL that resolves wrongly</strong> on some templates.</p>
<p>The diagnostic that answers it directly is the URL inspection tool, which reports the
<strong>user-declared</strong> canonical and the <strong>Google-selected</strong> one side by side.
When they differ, the problem is a signal conflict somewhere else on the site, and changing the tag
again will not fix it.</p>
'''),
 S('Choosing the Right Instrument for the Problem', '''
<p>Canonical tags are the default answer to duplication and frequently the wrong one. Each instrument
does something different and they are not interchangeable.</p>
<table>
<tr><th>Situation</th><th>Instrument</th></tr>
<tr><td>Two URLs, genuinely the same page</td><td><strong>Canonical</strong> to the preferred one</td></tr>
<tr><td>A page permanently moved</td><td><strong>301 redirect</strong>, not a canonical</td></tr>
<tr><td>Faceted or filtered variants with no search value</td><td><strong>noindex</strong>, or block the parameter</td></tr>
<tr><td>Paginated sequences</td><td><strong>Self-referencing canonicals</strong> on each page</td></tr>
<tr><td>Same content for different regions or languages</td><td><strong>hreflang</strong> plus self-referencing canonicals</td></tr>
<tr><td>Syndicated to a third party</td><td>Ask for a <strong>canonical back to you</strong>, or accept the risk</td></tr>
</table>
<p>Two errors are worth naming because they are frequent and expensive.
<strong>Canonicalising paginated pages to page one</strong> removes deeper items from consideration
entirely. And <strong>combining noindex with a canonical</strong> on the same URL sends contradictory
instructions — one says do not index this, the other says consolidate its signals into another page —
and the outcome is unpredictable. Choose one.</p>
''')]),

'codex/social-media/snapchat-marketing': dict(sources=[SNAP], sections=[
 S('Creating for a Camera-First Audience', '''
<p>Content that performs elsewhere generally underperforms on Snapchat, because the platform's
conventions were set by private messaging rather than by broadcast.</p>
<p>Three differences shape production. <strong>Vertical, full-screen, sound-on is the baseline</strong>
rather than an option, and repurposed landscape content reads as imported.
<strong>Production polish is not an advantage.</strong> Content that looks made rather than captured
is treated as advertising by an audience that came for something else, and a phone-shot clip often
outperforms a studio one.
<strong>The first second decides everything</strong>, with no title, thumbnail or caption doing that
work in advance.</p>
<p>Practically: shoot in the app or in a way indistinguishable from it, cut hard and early, put the
substance before any branding, and caption for the meaningful share of viewing that happens without
sound despite the sound-on default.</p>
'''),
 S('Whether It Is Worth Your Time', '''
<p>The honest assessment for most brands is that organic Snapchat is a poor use of scarce content
capacity, and it is worth being specific about when that is wrong.</p>
<p><strong>It is worth it when</strong> your audience genuinely skews to the platform's younger
demographic and you can verify that from your own data rather than from a general statistic; when you
can produce in the native idiom without a separate production cycle; or when AR is a real product fit
— a try-on for eyewear, cosmetics or furniture is a functional tool rather than a campaign, and it is
the platform's genuine differentiator.</p>
<p><strong>It is not worth it when</strong> the plan is to cross-post existing vertical video, which
performs poorly and costs the appearance of effort; when the goal is link traffic, which the platform
constrains heavily for organic accounts; or when nobody owns it, because organic performance here
decays faster than on platforms with a searchable back catalogue.</p>
<p>Set the expectation before starting: <strong>this is a presence and a creative-capability
investment, not an acquisition channel</strong>. Judged as the latter it will disappoint, and the
disappointment will be correct.</p>
''')]),

'codex/business-strategy/international-marketing': dict(sources=[], sections=[
 S('Sequencing Markets Rather Than Ranking Them', '''
<p>Market selection frameworks produce a ranked list, and a ranked list is not a plan. The second
market should be chosen for what it teaches and what it shares with the first, not only for its
score.</p>
<p>Three practical criteria that ranking models tend to miss.
<strong>Operational adjacency</strong>: a market sharing a language, a legal framework, a payment
infrastructure or a distribution partner with one you already serve costs a fraction of an isolated
one, even at a lower score.
<strong>Learning value</strong>: an early market that tests the riskiest assumption in your thesis is
worth more than a safe one that confirms what you know.
<strong>Reversibility</strong>: some entries are cheap to exit and some create obligations —
employees, leases, regulatory registrations, distributor contracts with termination terms — that
outlast the decision to leave.</p>
<p>Sequence for <strong>compounding capability</strong>. Three adjacent markets served properly build
an operating model; three unrelated ones build three separate problems.</p>
'''),
 S('The Signals That Tell You to Stop', '''
<p>International programmes are much easier to start than to end, and the usual failure is not a bad
market but a market nobody was willing to close. Decide the exit criteria at entry, when you are still
objective.</p>
<p>Signals worth writing into the plan in advance:</p>
<ul>
<li><strong>Cost of acquisition not improving with scale.</strong> In a working market it falls as
brand and learning accumulate. Flat CAC after a full cycle usually means the proposition is not
landing rather than that the spend is too low.</li>
<li><strong>Retention below your home benchmark by a wide margin.</strong> Acquisition problems are
fixable; retention gaps usually mean the product or the promise does not fit the market.</li>
<li><strong>Management attention out of proportion to revenue.</strong> The most expensive cost of a
marginal market is senior time, and it never appears in the P&amp;L for that market.</li>
<li><strong>Every gain requiring bespoke work.</strong> If nothing transfers to or from other markets,
you have a separate business rather than an expansion.</li>
</ul>
<p><strong>A decision to withdraw made against criteria set in advance is a good decision.</strong>
One made in the eighteenth month against a feeling is the same outcome reached more expensively.</p>
''')]),
}

ANCHOR = '</div>\n    <aside class="guide-sidebar">'
# The .srcs rules live in _build/codex_style.txt for future builds, but these
# pages were generated before it carried them. A page that gains a sources
# block must gain the CSS in the same write, or it ships an unstyled element —
# the I7 failure shape ("elements needing styling to exist").
_TPL = io.open('_build/codex_style.txt', encoding='utf-8').read()
SRCS_CSS = '\n' + _TPL[_TPL.index('.srcs{'):_TPL.index('.srcs a{word-break:break-word}') + len('.srcs a{word-break:break-word}')]
assert '.srcs{' in SRCS_CSS and '</style>' not in SRCS_CSS, 'bad CSS extraction'
SRCS_CSS_MARK = '.srcs{'
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
    if cfg['sources'] and SRCS_CSS_MARK not in out:
        assert out.count('</style>') == 1, f + ': %d style blocks' % out.count('</style>')
        before = len(out)
        out = out.replace('</style>', SRCS_CSS + '\n</style>', 1)
        assert len(out) == before + len(SRCS_CSS) + 1, f + ': css delta wrong'
    if cfg['sources']:
        assert SRCS_CSS_MARK in out, f + ': sources block with no .srcs CSS'
    io.open(f, 'w', encoding='utf-8').write(out)
    done += 1
    print('  ✅ %-54s +%d words %s' % (path.replace('codex/', ''),
          len(re.sub(r'<[^>]+>', ' ', add).split()),
          '+%d sources' % len(cfg['sources']) if cfg['sources'] else '(no sources: methodological)'))
print('\n%d pages expanded' % done)
