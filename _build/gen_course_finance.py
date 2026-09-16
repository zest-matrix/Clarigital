#!/usr/bin/env python3
"""gen_course_finance.py — Session 105. Point the finance course at the guides.

THE DEFECT
`courses/ai-finance/` has 15 lessons across three tracks. All 15 point at the
nine modules, the two playbook pages and the regulation pages -- and **none at
the 13 product guides**. The course was built before they existed and nothing
re-pointed it. Same derived-artefact class QA #7 and QA #8 both found, in a
place neither looked.

WHAT THIS DOES, AND WHAT IT DELIBERATELY DOES NOT
It does NOT restructure the 15 lessons. They are a coherent progression --
orientation and regulation, then the five core modules, then the remaining
modules and the playbook -- and rewriting them would break the progress bars,
the quiz ids and the completion state people have stored locally.

It ADDS a closing section after the advanced track: "Then build one", listing
every product guide, **derived from the filesystem** and ordered by the
`Product Guide NN` label each page carries, exactly as gen_fintech_hub.py does.
So a fourteenth guide appears here automatically.

WHAT THIS DOES NOT COVER
  - Only this course. The other 67 syllabi were not audited for the same
    problem, and at least some of them may point at pages that have moved.
  - It appends; it does not verify that the 15 existing lessons still resolve.
    linkcheck covers that separately.

Run from the site root: python3 /tmp/gen_course_finance.py
"""
import glob, io, os, re

PAGE = 'courses/ai-finance/index.html'
ANCHOR = '\n  </div>\n\n  </main>\n'
MARK = '<!-- gen_course_finance -->'

guides = []
for p in sorted(glob.glob('fintech-ai/products/*/index.html')):
    h = io.open(p, encoding='utf-8').read()
    lab = re.search(r'<div class="label-tag">Product Guide (\d+)</div>', h)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    assert h1, 'no <h1> in ' + p
    title = re.sub(r':\s*How to Build It\s*$', '', re.sub(r'<[^>]+>', '', h1.group(1)).strip())
    guides.append((int(lab.group(1)) if lab else 999, p.split('/')[2], title))
guides.sort()
assert guides, 'no product guides found'
print('derived: %d product guides' % len(guides))

WORDS = {13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen'}
word = WORDS.get(len(guides), str(len(guides)))

cards = ''.join(
    '<div class="lesson"><div class="lesson-body">'
    '<div class="lesson-num">Product guide %02d</div>'
    '<div class="lesson-title">%s</div>'
    '<div class="lesson-desc"><a href="/fintech-ai/products/%s/">Read the guide &rarr;</a></div>'
    '</div></div>' % (num, title, slug)
    for num, slug, title in guides)

block = (MARK +
         # Use only classes this page already styles. S105: the first version
         # invented .track-section and .track-head, which had no CSS rule --
         # the I7 failure shape, self-inflicted. .track-panel was rejected too:
         # it is a JS-controlled tab panel and this block must always be visible.
         '<div style="margin-top:28px">'
         # NOT .depth-band: rendercheck asserts one depth-band per track-panel
         # (courses) or per lane-section (lane pages). A fourth one on a
         # three-track course is a real inconsistency and the standing check
         # caught it. S105: my second self-inflicted defect this session.
         '<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">'
         '<span class="depth-badge" style="color:var(--indigo)">Next</span>'
         '<span class="depth-note">The course explains the capabilities. '
         'These walk one product end to end.</span></div>'
         '<h2>Then build one</h2>'
         '<p style="font-size:.86rem;line-height:1.65;margin:0 0 14px">'
         'Every guide takes a single product through eight steps: the options at each one, '
         'what goes in and what comes out, what it costs, and what breaks. '
         '<strong>' + word.capitalize() + ' products, four regulators.</strong> '
         'Start with the one closest to what you are actually building.</p>'
         '<div class="lessons-list">' + cards + '</div>'
         '</div>\n' + MARK)

src = io.open(PAGE, encoding='utf-8').read()

# replace an existing generated block, or insert a new one
if MARK in src:
    a = src.find(MARK)
    b = src.rfind(MARK) + len(MARK)
    assert b > a, 'malformed existing block'
    out = src[:a] + block + src[b:]
else:
    n = src.count(ANCHOR)
    assert n == 1, 'anchor appears %d times' % n
    i = src.find(ANCHOR)
    out = src[:i] + '\n' + block + src[i:]

# ---- verify before writing ----------------------------------------------
assert out.count('<div') == out.count('</div>'), 'div balance broken'
assert len(re.findall(r'<h1[\s>]', out)) == 1, 'h1 count moved'
assert out.count('</html>') == 1 and out.count('</body>') == 1, 'document truncated'
assert out.count('id="a-quiz"') == 1 and out.count('toggleLesson') == src.count('toggleLesson'), \
    'quiz or lesson handlers disturbed'
for _, slug, _ in guides:
    href = '/fintech-ai/products/' + slug + '/'
    assert href in out, 'guide missing: ' + href
    assert os.path.exists('fintech-ai/products/' + slug + '/index.html'), 'dead card ' + href
if out == src:
    print('  = course already current')
else:
    io.open(PAGE, 'w', encoding='utf-8').write(out)
    print('  ✅ %s updated (%d -> %d bytes)' % (PAGE, len(src), len(out)))
