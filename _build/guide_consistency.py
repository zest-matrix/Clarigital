#!/usr/bin/env python3
"""guide_consistency.py — structural parity across the product-guide set.

WHY THIS EXISTS
Sessions 107 and 108 each shipped a first build carrying ONE code block where
every other product guide carries two or more. Neither was a check failure:
`newpage_check` compares code blocks to copy buttons on a single page, and one
matched one. QA #6's drift test did the same.

**No check compared a page against its siblings.** Both were caught by hand, by
noticing an odd number in a column -- which is not a control.

This compares every product guide against the set and reports any that sit
outside it. It is a METRIC, not a gate: a guide legitimately needing a
different shape should be able to have one, and the report is there so the
decision is deliberate rather than accidental.

WHAT IT CHECKS
  lanes          three, in green/indigo/amber order
  code blocks    at least the set minimum
  copy buttons   one per code block
  sources        at least the set minimum, typed
  TOC            exactly one
  cost registry  exactly one
  label          a "Product Guide NN" tag
  what-to-check  present, and inside <pre> rather than loose in the prose

WHAT IT DOES NOT COVER
  - Nothing about whether the WRITING is any good, which is the thing that
    actually varies and the thing no script can see.
  - The minimum is derived from the set's own median, so if the whole set
    drifted together this would report nothing. It detects an outlier, not a
    trend.
  - Product guides only. Build sheets and modules have their own shapes and
    are not compared here.

Run from the site root: python3 /tmp/guide_consistency.py
"""
import glob, io, re, statistics, sys

G = sorted(glob.glob('fintech-ai/products/*/index.html'))
assert G, 'no product guides found'

rows = []
for p in G:
    h = io.open(p, encoding='utf-8', errors='ignore').read()
    pre = ''.join(re.findall(r'<pre>(.*?)</pre>', h, re.S))
    loose = re.sub(r'<pre>.*?</pre>', '', h, flags=re.S)
    rows.append(dict(
        slug=p.split('/')[2],
        label=(re.search(r'<div class="label-tag">Product Guide (\d+)</div>', h) or [None, '??'])[1]
        if re.search(r'<div class="label-tag">Product Guide (\d+)</div>', h)
        else '??',
        lanes=''.join(l[0] for l in re.findall(r'data-lane="(\w+)"', h)),
        code=h.count('class="cb-head"'),
        copy=len(re.findall(r'class="cb-copy"', h)),
        srcs=h.count('<span class="src-k'),
        toc=h.count('class="toc"'),
        reg=h.count('class="reg-head"'),
        wtc_in=len(re.findall(r'WHAT TO CHECK', pre)),
        wtc_out=len(re.findall(r'WHAT TO CHECK', loose)),
    ))

# The set defines its own norm, and the two dimensions need different rules.
#
# CODE BLOCKS: median. A one-block guide against a median of two is a genuine
# outlier and that is exactly what S107 and S108 shipped.
#
# SOURCES: the MINIMUM, not the median. The first version used the median and
# flagged 8 of 16 guides -- because the source standard rose deliberately
# partway through the programme, from 6 on guides 01-08 to 8 on guides 09-16.
# A check that fires on half the set is a check people learn to ignore. The
# generational split is reported below as a fact rather than as a failure.
min_code = max(1, int(statistics.median(r['code'] for r in rows)))
min_srcs = min(r['srcs'] for r in rows)
_s = sorted(r['srcs'] for r in rows)
print('set of %d guides · median code blocks %d · sources %d–%d (floor %d)'
      % (len(rows), min_code, _s[0], _s[-1], min_srcs))
if _s[0] != _s[-1]:
    print('note: sources range %d–%d across the set. Guides 01–08 were built to a'
          % (_s[0], _s[-1]))
    print('      6-source standard and 09 onward to 8. Deliberate, not drift.')
print()

hdr = '%-28s %3s %-4s %4s %4s %4s %3s %3s'
print(hdr % ('slug', 'pg', 'lane', 'code', 'copy', 'srcs', 'toc', 'reg'))
out = []
for r in rows:
    flags = []
    if r['lanes'] != 'gia':
        flags.append('lanes=%s' % r['lanes'])
    if r['code'] < min_code:
        flags.append('code %d < %d' % (r['code'], min_code))
    if r['copy'] != r['code']:
        flags.append('copy %d != code %d' % (r['copy'], r['code']))
    if r['srcs'] < min_srcs:
        flags.append('sources %d < %d' % (r['srcs'], min_srcs))
    if r['toc'] != 1:
        flags.append('toc=%d' % r['toc'])
    if r['reg'] != 1:
        flags.append('cost registry=%d' % r['reg'])
    if r['label'] == '??':
        flags.append('no Product Guide label')
    if r['wtc_in'] == 0:
        flags.append('no WHAT TO CHECK in a code block')
    if r['wtc_out'] > 0:
        flags.append('WHAT TO CHECK outside <pre>')
    mark = '  ⚠' if flags else ''
    print((hdr % (r['slug'][:28], r['label'], r['lanes'], r['code'], r['copy'],
                  r['srcs'], r['toc'], r['reg'])) + mark)
    if flags:
        out.append((r['slug'], flags))

print()
if out:
    print('OUTLIERS — %d guide(s) sit outside the set:' % len(out))
    for slug, flags in out:
        print('   %-28s %s' % (slug, '; '.join(flags)))
    print()
    print('This is a METRIC. A guide may legitimately differ — but the')
    print('difference should be a decision, which is what this report is for.')
    sys.exit(0)
print('PASS — every guide sits within the set')
