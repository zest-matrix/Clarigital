#!/usr/bin/env python3
"""rescope.py — Session 87. Classify the thin-content backlog.

The `thin_content` metric has read 217 across six QA sessions. The MASTER has
carried an estimate that "~70 are hubs where short is CORRECT" since Session
59 and that estimate has never been tested. Sessions 88 onward depend on it.

This script does not invent its own definition. It imports the STANDING one
from rendercheck.thin_content so the population cannot drift from the metric
the audit reports — the alternative is two numbers that disagree, which this
project has been caught by ten times.

BUCKETS
  HUB      routes DOWNWARD to pages in its own directory. Short is correct.
  SYLLABUS routes OUTWARD to lessons that live elsewhere. Short is correct.
           Added S88 after 48 course syllabi were counted as a content backlog
           by a hub test that only looked down the tree.
  NEARLY   a real content page sitting just under the line — the cheapest
           pages to move, and where a little work removes a lot of metric.
  WRITE    a genuine leaf page with too little content. The real backlog.
  CUT      a page that should not exist: no unique content, or duplicated
           elsewhere. Needs a human decision, never an automatic delete.

WHAT THIS DOES NOT COVER
  - **A HUB can still be too thin to be useful.** `kids >= 1` answers "is this
    page's job routing", not "is this page adequate". `codex/sem/google-ads/
    youtube/` routes to two children on 171 words of real prose — correctly a
    hub, and arguably still too short. This classification does not separate
    "short is correct" from "short and thin", and a later pass should.
  - It cannot tell whether a WRITE page is worth writing. That is an editorial
    judgement and this script only sizes the queue.
  - CUT is a NOMINATION, not a verdict. Nothing here deletes anything.
  - `thin_content` excludes ai-kids/ by design (activity pages, short on
    purpose) and any page shallower than two directories deep. Those pages are
    outside this exercise entirely, correctly or not.
  - Word counts include nav and footer because the standing metric does. That
    was measured rather than assumed and comes to ~35 words, so the threshold
    is not materially inflated.

Run from the site root: python3 /tmp/rescope.py
Writes _build/thin-pages.md — the per-page list, committed to the repo.
"""
import io, os, re, sys, glob, collections

sys.path.insert(0, '/tmp')
sys.path.insert(0, os.path.join(os.getcwd(), '_build'))
import rendercheck

THIN = rendercheck.thin_content(verbose=False)          # the standing definition
print('population from the standing metric: %d pages' % len(THIN))

ALL_INDEX = set(glob.glob('**/index.html', recursive=True))
DIRS = {os.path.dirname(p) for p in ALL_INDEX}


CHROME_PAT = r'<nav\b.*?</nav>|<footer\b.*?</footer>|<div class="topbar".*?</div>'


def chrome_words(h):
    """Words contributed by nav, footer and topbar. Measured rather than
    assumed: it comes out at ~35 words, so the 800-word threshold is NOT
    materially inflated by furniture. The 217 is a real content measurement."""
    return sum(len(re.sub(r'<[^>]+>', ' ', m).split())
               for m in re.findall(CHROME_PAT, h, re.S))


def syllabus_links(h):
    """Lesson entries in a course syllabus whose target actually exists.

    A syllabus routes outward: its lessons are guides elsewhere on the site.
    Counting only RESOLVING targets means a syllabus pointing at nothing would
    not qualify as routing, which is the behaviour we want."""
    n = 0
    for u in re.findall(r'href="(/[^"#?]+/)"[^>]*>\s*Read the guide', h):
        if os.path.exists(u.strip('/') + '/index.html'):
            n += 1
    return n


def core_outlinks(h, d):
    """Out-links EXCLUDING the site chrome.

    S87: the first version counted every link on the page. The nav and footer
    contribute 21 links to EVERY page on this site, so a threshold of 12 was
    met by the menu alone and 206 of 217 pages came back as hubs. A classifier
    that reads the site's own navigation as evidence of being a hub will call
    every page a hub."""
    core = re.sub(CHROME_PAT, '', h, flags=re.S)
    return len({u for u in re.findall(r'href="(/[^"#?]+/)"', core)
                if not d.startswith(u.strip('/')) and u.strip('/') != d})


def body_words(h):
    b = h[h.find('<body'):]
    b = re.sub(r'<script.*?</script>|<style.*?</style>', '', b, flags=re.S)
    return len(re.sub(r'<[^>]+>', ' ', b).split())


rows = []
for w, f in THIN:
    h = io.open(f, encoding='utf-8', errors='ignore').read()
    d = os.path.dirname(f)
    kids = sum(1 for o in DIRS if o != d and o.startswith(d + '/'))
    ch = chrome_words(h)
    content = w - ch
    outs = core_outlinks(h, d)
    section = f.split('/')[0]

    # A page whose own directory contains other pages exists to route to them.
    # That is a structural fact about the tree, not an inference from links.
    if kids >= 1:
        bucket = 'HUB'
    # S88: a page can route OUTWARD instead of downward. A course syllabus owns
    # no child directories -- its lessons live under /codex/ -- so the tree test
    # misses it entirely and 48 syllabi were counted as a content backlog.
    # Keyed on the template rather than on a link count, because AI Atlas tool
    # guides reach 14-15 out-links from a related-tools sidebar and are genuine
    # content pages. Structure separates them; arithmetic does not.
    elif syllabus_links(h) >= 5:
        bucket = 'SYLLABUS'
    elif content < 120:
        bucket = 'CUT'
    elif content >= 600:
        bucket = 'NEARLY'
    else:
        bucket = 'WRITE'
    rows.append(dict(f=f, total=w, chrome=ch, content=content, kids=kids,
                     outs=outs, section=section, bucket=bucket))

by = collections.Counter(r['bucket'] for r in rows)
sec = collections.Counter((r['section'], r['bucket']) for r in rows)

print()
print('%-8s %5s   %s' % ('BUCKET', 'PAGES', 'meaning'))
for b, meaning in [('HUB', 'routing downward to child pages — short is correct'),
                   ('SYLLABUS', 'routing outward to lessons elsewhere — short is correct'),
                   ('NEARLY', 'a real page just under the line — cheapest to close'),
                   ('WRITE', 'the real backlog'),
                   ('CUT', 'nominated for a human decision')]:
    print('%-8s %5d   %s' % (b, by[b], meaning))
print('%-8s %5d' % ('TOTAL', len(rows)))

print()
print('by section:')
sections = sorted({r['section'] for r in rows})
print('  %-22s %5s %5s %6s %5s %4s' % ('section', 'HUB', 'SYLL', 'NEARLY', 'WRITE', 'CUT'))
for s in sections:
    print('  %-22s %5d %5d %6d %5d %4d' % (s, sec[(s, 'HUB')], sec[(s, 'SYLLABUS')],
                                             sec[(s, 'NEARLY')], sec[(s, 'WRITE')], sec[(s, 'CUT')]))

med_chrome = sorted(r['chrome'] for r in rows)[len(rows) // 2]
print()
print('median chrome words per thin page: %d' % med_chrome)
print('pages whose CONTENT clears 800 once chrome is removed: %d'
      % sum(1 for r in rows if r['content'] >= 800))

# ---- the committed artefact --------------------------------------------
out = ['# Thin-page classification — Session 87', '',
       'Generated by `_build/rescope.py` from the standing `thin_content` metric.',
       '**Do not hand-edit.** Re-run the script; the classification is derived.', '',
       '| Bucket | Pages | Meaning |', '|---|---|---|',
       '| HUB | %d | Routes downward to child pages. Short is correct. |' % by['HUB'],
       '| SYLLABUS | %d | Routes outward to lessons elsewhere. Short is correct. |' % by['SYLLABUS'],
       '| NEARLY | %d | A real page just under the line. Cheapest to close. |' % by['NEARLY'],
       '| WRITE | %d | **The real backlog.** |' % by['WRITE'],
       '| CUT | %d | Nominated for a human decision. Nothing is deleted by this script. |' % by['CUT'],
       '| **Total** | **%d** | |' % len(rows), '']
for b in ('WRITE', 'CUT', 'NEARLY', 'SYLLABUS', 'HUB'):
    sel = sorted((r for r in rows if r['bucket'] == b), key=lambda r: r['content'])
    out += ['', '## %s — %d pages' % (b, len(sel)), '',
            '| Page | Content words | Chrome | Child dirs | Out-links |', '|---|---|---|---|---|']
    out += ['| `%s` | %d | %d | %d | %d |' % (r['f'], r['content'], r['chrome'], r['kids'], r['outs'])
            for r in sel]
io.open('_build/thin-pages.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print()
print('✅ _build/thin-pages.md written — %d rows' % len(rows))
