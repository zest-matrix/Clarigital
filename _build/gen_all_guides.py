#!/usr/bin/env python3
"""Session 67 — regenerate /codex/all-guides/ from the filesystem.

It was hand-maintained, listed 236 of 364, and its headline count had gone stale
(218). Both failure modes disappear when the page is derived.
"""
import glob, io, os, re, html as H

def title_of(path):
    h = io.open(path, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', h, re.S)
    t = re.sub(r'<[^>]+>', '', m.group(1)) if m else ''
    t = H.unescape(t).strip()
    if not t:
        m = re.search(r'<title>(.*?)</title>', h, re.S)
        t = H.unescape(m.group(1)).split('|')[0].strip() if m else ''
    return re.sub(r'\s+', ' ', t)

# a page is a GUIDE if no deeper index.html lives beneath it
allp = sorted(glob.glob('codex/**/index.html', recursive=True))
dirs = {os.path.dirname(p) for p in allp}
guides, hubs = [], {}
for p in allp:
    d = os.path.dirname(p)
    if any(o != d and o.startswith(d + '/') for o in dirs):
        hubs[d] = title_of(p)
    else:
        guides.append(p)

EXCLUDE = {'codex/all-guides', 'codex/glossary'}
guides = [p for p in guides if os.path.dirname(p) not in EXCLUDE]

groups = {}
for p in guides:
    groups.setdefault(os.path.dirname(os.path.dirname(p)), []).append(p)

def gname(d):
    if d in hubs and hubs[d]:
        return hubs[d]
    return ' &mdash; '.join(s.replace('-', ' ').title() for s in d.split('/')[1:]) or 'The Codex'

blocks = []
for d in sorted(groups, key=lambda x: (len(x.split('/')), x)):
    items = sorted(groups[d], key=lambda p: title_of(p).lower())
    cards = ''.join(
        f'<a href="/{os.path.dirname(p)}/" class="ag-card">{H.escape(title_of(p))} '
        f'<span class="ag-arr">&#8594;</span></a>' for p in items)
    href = f'/{d}/' if os.path.exists(f'{d}/index.html') else '/codex/'
    blocks.append(f'<div class="ag-group"><h2 class="ag-h">'
                  f'<a href="{href}" style="color:var(--navy);text-decoration:none">{gname(d)}</a>'
                  f'</h2><div class="ag-grid">{cards}</div></div>')

total = len(guides)
f = 'codex/all-guides/index.html'
h = io.open(f, encoding='utf-8').read()

# replace every existing ag-group block with the regenerated set
# balance-extract every existing ag-group block; replace the whole span.
# A rfind on '</div></div>' guessed the boundary and lost a closing tag.
spans = []
for m in re.finditer(r'<div class="ag-group">', h):
    i = m.start(); d = 0; end = None
    for t in re.finditer(r'<div\b|</div>', h[i:]):
        d += 1 if t.group(0) == '<div' else -1
        if d == 0:
            end = i + t.end(); break
    assert end, 'unbalanced ag-group'
    spans.append((i, end))
assert spans, 'no ag-group blocks found'
gap = ''.join(h[spans[k][1]:spans[k+1][0]] for k in range(len(spans) - 1))
assert not gap.strip(), 'non-ag-group content inside the region'
new = h[:spans[0][0]] + ''.join(blocks) + h[spans[-1][1]:]

# every count on the page comes from the filesystem now
new = re.sub(r'\b\d{2,4}\b(?=\s*(?:Digital Marketing |Digital Codex )?[Gg]uides)', str(total), new)

b = re.sub(r'<script.*?</script>', '', new[new.find('<body'):], flags=re.S)
assert b.count('<div') == b.count('</div>'), f"div {b.count('<div')}/{b.count('</div>')}"
assert b.count('<a ') == b.count('</a>'), 'anchors'
assert new.count('</html>') == 1
linked = len(set(re.findall(r'href="(/codex/[^"]+/)" class="ag-card"', new)))
assert linked == total, f"listed {linked} of {total}"
io.open(f, 'w', encoding='utf-8').write(new)
print(f"regenerated: {total} guides in {len(blocks)} groups, all linked")
