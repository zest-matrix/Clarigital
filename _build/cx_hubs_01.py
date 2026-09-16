#!/usr/bin/env python3
"""cx_hubs_01.py — Session 102. The 19 thin hubs.

WHAT THIS IS NOT
It is not a word-count exercise. These pages are hubs and short is correct for
them (SOP C9). QA #8 found that 19 of the 45 route correctly and **explain
nothing**: `codex/analytics-cro` lists 24 children in 130 words. The fix is one
or two orienting paragraphs -- what this area covers, who it is for, where to
start -- not another 600 words. None of these will or should cross 800.

RULE 4 CHECK, DONE BEFORE WRITING
`gen_counts.py` writes the `<p>NN guides ...</p>` lead on the Codex section
hubs, matching `(<p>)\\d{1,4}(\\s+guides\\b)` with count=1. Inserting AFTER that
paragraph is safe; inserting before it would capture the wrong <p> and corrupt
every count on the site. Every insertion here goes after.

THREE SHAPES
  A  Codex section hubs   -- insert after the derived count paragraph
  B  Codex sub-hubs       -- the guide-* template, same anchor as batches 1-9
  C  AI Atlas hubs        -- inconsistent with each other; anchor resolved per
                             page and asserted, never assumed
"""
import io, os, re, sys
sys.path.insert(0, '/tmp')

P = lambda *ps: ''.join('<p>%s</p>\n' % x for x in ps)

HUBS = {
'codex/history': P(
 'History is here because most digital marketing advice is a snapshot presented as a principle. '
 'Knowing <strong>why</strong> a rule exists tells you when it stops applying — and rules in this '
 'field stop applying regularly.',
 '<strong>Start with the history of digital marketing</strong> for the overall shape, then take the '
 'discipline closest to your work. The algorithm and privacy histories are the two that most often '
 'explain a constraint somebody is currently arguing with.'),

'codex/tools-resources': P(
 'These are the tools worth learning properly rather than the tools with the best marketing. Every '
 'one here is either free or has a free tier that does real work, and each guide covers what the '
 'tool actually tells you rather than every menu it has.',
 '<strong>If you are starting from nothing</strong>, Search Console first — it is free, it is your '
 'own data, and it answers more questions than any paid alternative.'),

'ai-atlas/specialist-tools/data-analysis': P(
 'Data analysis is where AI tools are most useful and most dangerous at once: they will produce a '
 'confident chart from a misread column without any sign that anything went wrong.',
 '<strong>The guides here assume you will check the output</strong>, and cover how — verifying the '
 'row count, the date range and the join before trusting any figure. A tool that saves an hour of '
 'work and produces one wrong number has not saved anything.'),

'codex/content-marketing': P(
 'Content marketing fails at distribution far more often than at production. Most of these guides '
 'are about what happens to a piece after it exists — where it goes, how it is found, and how long '
 'it keeps working.',
 '<strong>Start with strategy</strong> if you are deciding what to make, or with distribution if '
 'you are already making things nobody reads. The measurement guide is the one to reach for before '
 'a budget conversation.'),

'codex/analytics-cro': P(
 'Analytics answers what happened; CRO decides what to change. They are separate skills and this '
 'section covers both, because a measurement setup nobody acts on and a test programme with '
 'untrustworthy data fail the same way.',
 '<strong>Start with the fundamentals and the GA4 setup</strong> if the numbers are not yet '
 'trusted — everything downstream depends on that. If the data is sound, go to experimentation.',
 'A theme runs through the section: <strong>a metric with no decision attached is a number you will '
 'report for two years and never act on.</strong>'),

'codex/sem/google-ads/youtube': P(
 'YouTube sits inside Google Ads but behaves like a different channel: the creative carries far more '
 'of the result than the targeting does, and the measurement question is closer to television than '
 'to search.',
 '<strong>Read the fundamentals before the advanced guide.</strong> Most YouTube campaigns that '
 'underperform are creative problems being diagnosed as targeting problems.'),

'codex/affiliate-marketing': P(
 'Affiliate marketing is the one channel where you pay after the result, which makes it look risk-free '
 'and makes the risk move elsewhere — into attribution, partner quality and compliance.',
 '<strong>Start with the fundamentals</strong>, then the guide matching your model: content, coupon, '
 'influencer, B2B or SaaS. They behave differently enough that general advice is unusually unreliable '
 'here.',
 'The compliance guides are not optional reading. <strong>Disclosure obligations attach to the '
 'relationship, not to the link type</strong>, and they are yours as much as your partners&rsquo;.'),

'codex/email-marketing': P(
 'Email is the only channel you own, which is why it survives every platform change — and why its '
 'failures are self-inflicted rather than algorithmic.',
 '<strong>If your open rates have fallen, start with deliverability</strong> rather than subject '
 'lines. Most email problems presented as creative problems are sending-reputation problems.',
 'The automation and design guides assume you will test the decline path and the unsubscribe, which '
 'almost nobody does and which is where the damage concentrates.'),

'codex/case-studies': P(
 'Case studies are useful for mechanisms and dangerous for tactics. What transferred from these '
 'companies was rarely the specific campaign — it was a structural decision about product, pricing or '
 'distribution that the marketing then expressed.',
 '<strong>Read them for the constraint each company was under</strong>, not for the thing they did. '
 'Copying a tactic from a business with different economics is how a case study becomes an expensive '
 'quarter.'),

'codex/sem/google-ads/advanced': P(
 'Advanced here means structural rather than obscure: account architecture, measurement quality and '
 'systematic testing. Very little of it is a setting you have not found yet.',
 '<strong>Before anything in this section, make sure conversion tracking is correct.</strong> An '
 'account optimising toward a mismeasured conversion will spend the budget efficiently on the wrong '
 'outcome, and no advanced technique recovers that.'),

'codex/learn': P(
 'Two tracks, built for different starting points. <strong>Beginner</strong> assumes no background '
 'and builds the vocabulary and the mental model. <strong>Advanced</strong> assumes you work in this '
 'and want the parts that are structural rather than tactical.',
 'Neither is a certification and neither asks for an email address. If you are unsure which to take, '
 'open the first guide of each — the difference in assumed knowledge is obvious within a paragraph.'),

'codex/sem': P(
 'Search advertising is the most measurable channel and therefore the easiest to optimise in the '
 'wrong direction. Most of this section is about making sure the number you are optimising toward is '
 'the one that matters.',
 '<strong>Start with the Google Ads fundamentals</strong>, then the campaign type you actually run. '
 'The measurement and advanced guides are where accounts stop plateauing.'),

'codex/programmatic': P(
 'Programmatic is an auction, a supply chain and a measurement problem wearing one name. The supply '
 'chain is where most of the waste is, and it is the part buyers look at last.',
 '<strong>Start with real-time bidding</strong> for the mechanics, then supply-path and measurement. '
 'The brand safety and viewability guides matter more than their position in most media plans '
 'suggests.',
 'A theme across the section: <strong>the cheapest, best-performing inventory in your report is where '
 'to look first for a problem</strong>, not where to scale.'),

'ai-atlas/for-you': P(
 'These guides are organised by who you are rather than by what the tool does, because the useful '
 'question is not <em>what can this do</em> but <em>what should I use it for on a Tuesday</em>.',
 'Each one covers a small number of things worth doing, the tools that actually help, and — the part '
 'usually left out — <strong>what to be careful about</strong>, including what not to put into a '
 'chatbot and how to check an answer before acting on it.'),

'codex/ecommerce': P(
 'E-commerce marketing has a constraint the rest of digital marketing does not: <strong>the unit '
 'economics decide whether a channel is viable at all</strong>, and a tactic that works beautifully '
 'at one margin is loss-making at another.',
 '<strong>Start with the fundamentals and the SEO guide</strong>, then the channel you are actually '
 'investing in. The returns and international guides are the two most often skipped and most often '
 'expensive.'),

'codex/paid-advertising': P(
 'Paid advertising across every major platform, organised by where you are spending. The platforms '
 'differ enormously in mechanics and barely at all in the questions worth asking: what is the '
 'incremental return, what is the real supply chain, and what would make you stop.',
 '<strong>Start with media buying fundamentals</strong> if you are new to buying, or go straight to '
 'your platform if you are not. The Meta and Google sections are the deepest; the smaller platforms '
 'are covered honestly, including where they are not worth your time.'),

'ai-atlas/use-cases': P(
 'Organised by the task rather than by the tool, because the tool you should use changes far faster '
 'than the task does.',
 'Each guide covers the handful of approaches worth knowing, which tool currently does the job well, '
 'and <strong>how to tell when the output is wrong</strong> — which is the part that determines '
 'whether any of it saves time.'),

'codex/social-media': P(
 'Organic social has the worst ratio of effort to measurable return of any channel here, and it is '
 'still worth doing for reasons that do not appear in a dashboard. These guides try to be honest '
 'about both halves of that.',
 '<strong>Start with choosing platforms</strong> before anything else — most social media problems '
 'are the consequence of being on one platform too many.',
 'The crisis and community management guides are the ones to read before you need them rather than '
 'during.'),

'codex/paid-advertising/tiktok-ads': P(
 'TikTok distributes on interest rather than on a social graph, which makes creative the binding '
 'constraint and creative supply the thing most accounts run out of first.',
 '<strong>Start with the fundamentals</strong>, then creative best practices — in that order, because '
 'a well-structured account with imported creative fails in a way that is hard to diagnose.'),
}


def resolve(h, f):
    """Return (index, label) for where to insert. Anchor per page, asserted."""
    # A. Codex section hub -- after the derived count paragraph
    m = re.search(r'<p>\d{1,4}\s+guides\b[^<]*</p>', h)
    if m:
        return m.end(), 'after-count'
    # B. the guide-* template
    a = '</div>\n    <aside class="guide-sidebar">'
    if h.count(a) == 1:
        return h.find(a), 'guide-sidebar'
    # C. Atlas hubs -- after the hero section closes
    m = re.search(r'<section class="page-hero">.*?</section>', h, re.S)
    if m:
        return m.end(), 'after-hero'
    # C2. no page-hero: after the art-meta block that follows the hero lead
    m = re.search(r'<div class="art-meta">.*?</div>', h, re.S)
    if m:
        return m.end(), 'after-art-meta'
    raise AssertionError('%s: no anchor resolved' % f)


MD = re.compile(r'\*\*[^*\n]{2,60}\*\*|(?<![\w*|])\*[^*\n|]{2,60}\*(?![\w*|])')
WRAP = '<section><div class="wrap" style="padding-top:0;padding-bottom:1.2rem"><div style="max-width:70ch">%s</div></div></section>\n'

done = 0
for path, body in HUBS.items():
    f = path + '/index.html'
    assert os.path.exists(f), 'missing ' + f
    src = io.open(f, encoding='utf-8').read()
    # S102: the first version searched the WHOLE page text, which includes the
    # JSON-LD block. codex/paid-advertising was skipped because its schema
    # description (written in QA #7) begins with the same words as the new
    # paragraph. Search the VISIBLE body only.
    key = re.sub(r'<[^>]+>', '', body.split('</p>')[0])[:40]
    visible = re.sub(r'<script.*?</script>|<style.*?</style>', '', src, flags=re.S)
    if key and key in re.sub(r'<[^>]+>', '', visible):
        print('  = already done: ' + path); continue
    assert not MD.findall(re.sub(r'<[^>]+>', ' ', body)), '%s: markdown' % f
    i, label = resolve(src, f)
    add = WRAP % body
    out = src[:i] + add + src[i:]
    assert len(out) == len(src) + len(add)
    for t in ('<div', '</div>', '<section', '</section>', '<p>', '</p>'):
        assert out.count(t) == src.count(t) + add.count(t), '%s: %s moved' % (f, t)
    assert len(re.findall(r'<h1[\s>]', out)) == 1
    assert len(re.findall(r'<h2[\s>]', out)) == len(re.findall(r'<h2[\s>]', src)), 'h2 added to a hub'
    assert out.count('</html>') == 1 and out.count('</body>') == 1
    io.open(f, 'w', encoding='utf-8').write(out)
    done += 1
    print('  ✅ %-44s [%-16s] +%d words' % (path[:44], label,
          len(re.sub(r'<[^>]+>', ' ', body).split())))
print('\n%d hubs given orienting copy' % done)
