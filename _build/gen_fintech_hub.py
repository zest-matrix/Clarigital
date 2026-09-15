#!/usr/bin/env python3
"""gen_fintech_hub.py — derive the Fintech AI hub's counts and product-guide grid.

Session 81. Two defects made this necessary, both on /fintech-ai/:

  1. The stat strip said "1 Product guide" while eight existed. A hardcoded
     count inserted by a one-off patch in Session 62 and never revisited
     through eight product-guide sessions. Check #24 did not see it because
     that check looks for "N guides" phrasing on Codex section hubs.
  2. Seven of the eight product guides had NO route in from the hub. Each was
     linked only from its own module page. The orphan check was green because
     one inbound link is enough. SOP B7: not orphaned is much weaker than
     findable.

Everything this script writes is read from the filesystem:

  modules        directories under fintech-ai/ that carry a build sheet
  build sheets   fintech-ai/*/build-sheet/index.html
  product guides fintech-ai/products/*/index.html, ordered by the "Product
                 Guide NN" label each page carries, titled from its own <h1>
  regulators     of RBI, SEBI and IRDAI, those named on at least MIN_REG pages
                 in the section

WHAT THIS DOES NOT COVER
  - Prose counts elsewhere on the hub ("nine modules" written into a sentence
    in the body copy) are untouched. Only the stat strip, the two grid
    headings and their lead sentences are derived.
  - A future product guide that does not carry a "Product Guide NN" label will
    sort last, and one whose <h1> does not end ": How to Build It" will show
    its full <h1> on the card.
  - The regulator list is a claim about coverage, not a count. The threshold is
    arbitrary; it exists so the strip cannot silently omit a regulator the
    section has started covering, as it did with IRDAI.

Run from the site root: python3 /tmp/gen_fintech_hub.py
"""
import glob, io, os, re

HUB = 'fintech-ai/index.html'
MIN_REG = 3
REGS = ('RBI', 'SEBI', 'IRDAI')

# ---- derive ---------------------------------------------------------------
sheets = sorted(glob.glob('fintech-ai/*/build-sheet/index.html'))
modules = sorted({p.split('/')[1] for p in sheets})
guides = []
for p in sorted(glob.glob('fintech-ai/products/*/index.html')):
    h = io.open(p, encoding='utf-8').read()
    lab = re.search(r'<div class="label-tag">Product Guide (\d+)</div>', h)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    assert h1, 'no <h1> in ' + p
    title = re.sub(r':\s*How to Build It\s*$', '', h1.group(1).strip())
    guides.append((int(lab.group(1)) if lab else 999, p.split('/')[2], title))
guides.sort()

pages = glob.glob('fintech-ai/**/*.html', recursive=True)
regs = []
for r in REGS:
    n = sum(1 for p in pages
            if re.search(r'\b' + r + r'\b', io.open(p, encoding='utf-8').read()))
    if n >= MIN_REG:
        regs.append(r)

assert modules and sheets and guides and regs, 'derivation produced an empty set'
print('derived: %d modules · %d build sheets · %d product guides · %s'
      % (len(modules), len(sheets), len(guides), ' '.join(regs)))

WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
         7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve'}


def word(n):
    return WORDS.get(n, str(n))


def stat(n, label):
    return ('<div class="ft-stat"><div class="ft-stat-n">' + n +
            '</div><div class="ft-stat-l">' + label + '</div></div>')


strip = ('<div class="ft-stats">'
         + stat(str(len(modules)), 'Modules')
         + stat(str(len(sheets)), 'Build sheets')
         + stat(str(len(guides)), 'Product guide' + ('s' if len(guides) != 1 else ''))
         + stat(' &middot; '.join(regs), 'India first')
         + stat('0', 'Ads')
         + '</div>')

cards = ''.join(
    '<a href="/fintech-ai/products/' + slug + '/" class="sheet-card">'
    '<div class="sheet-n">Product guide %02d</div>'
    '<div class="sheet-t">%s</div></a>' % (num, title)
    for num, slug, title in guides)

pg_block = (
    '<h2>The ' + word(len(guides)) + ' product guides</h2>'
    '<p>A module explains how a capability works and a build sheet lists what to buy for it. '
    'A product guide walks <em>one product</em> from end to end: every step, your options at each '
    'one, what goes in, what comes out, how to connect it to the next step, and what breaks.</p>'
    '<div class="sheet-grid">' + cards + '</div>')

# ---- write, with every index asserted (Rule 5) ----------------------------
src = io.open(HUB, encoding='utf-8').read()
out = src

m = re.search(r'<div class="ft-stats">.*?</div></div></div>', out, re.S)
assert m, 'stat strip not found on ' + HUB
out = out[:m.start()] + strip + out[m.end():]

m = re.search(r'<h2>The \w+ build sheets</h2>', out)
assert m, 'build-sheet heading not found'
out = out[:m.start()] + '<h2>The ' + word(len(sheets)) + ' build sheets</h2>' + out[m.end():]

m = re.search(r'<p style="[^"]*">Building a specific product.*?</p>', out, re.S)
if m:
    out = out[:m.start()] + pg_block + out[m.end():]
else:
    m = re.search(r'<h2>The \w+ product guides</h2>.*?</div>(?=\s*<h2)', out, re.S)
    assert m, 'neither the old product-guide line nor a previous generated block was found'
    out = out[:m.start()] + pg_block + out[m.end():]

# ---- verify before saving -------------------------------------------------
assert out.count('<div') == out.count('</div>'), 'div balance broken'
assert len(re.findall(r'<h1[\s>]', out)) == 1, 'h1 count changed'
assert out.count('</html>') == 1 and out.count('</body>') == 1, 'document truncated'
for _, slug, _ in guides:
    href = '/fintech-ai/products/' + slug + '/'
    assert href in out, 'guide missing from hub: ' + href
    assert os.path.exists('fintech-ai/products/' + slug + '/index.html'), 'dead card ' + href
assert '>1</div><div class="ft-stat-l">Product guide<' not in out, 'stale count survived'

if out == src:
    print('  = hub already current')
else:
    io.open(HUB, 'w', encoding='utf-8').write(out)
    print('  ✅ ' + HUB + ' regenerated (%d bytes -> %d)' % (len(src), len(out)))
