#!/usr/bin/env python3
"""Session 68 — derive every per-section guide count from the filesystem.

Every section hub but two carried a wrong number, and `case-studies` read 331
because the Session 67 regex sweep replaced a legitimate SECTION count with the
GLOBAL one. That is the argument against broad regex sweeps in one line.
"""
import glob, io, os, re

EX = {'codex/all-guides', 'codex/glossary'}

def leaf_counts(prefix):
    allp = glob.glob(prefix + '**/index.html', recursive=True)
    dirs = {os.path.dirname(p) for p in allp}
    out = {}
    for p in allp:
        d = os.path.dirname(p)
        if any(o != d and o.startswith(d + '/') for o in dirs) or d in EX:
            continue
        parts = d.split('/')
        if len(parts) >= 2:
            out[parts[1]] = out.get(parts[1], 0) + 1
    return out

SEC = leaf_counts('codex/')
ATLAS = sum(leaf_counts('ai-atlas/').values()) + len(
    [p for p in glob.glob('ai-atlas/*/index.html')
     if not any(o != os.path.dirname(p) and o.startswith(os.path.dirname(p)+'/')
                for o in {os.path.dirname(x) for x in glob.glob('ai-atlas/**/index.html', recursive=True)})])
ATLAS = len([p for p in glob.glob('ai-atlas/**/index.html', recursive=True)
             if not any(o != os.path.dirname(p) and o.startswith(os.path.dirname(p)+'/')
                        for o in {os.path.dirname(x) for x in glob.glob('ai-atlas/**/index.html', recursive=True)})])
TOTAL = sum(SEC.values())

changed = {}

# 1. section hub lead paragraphs:  <p>NN guides ...
for d, n in SEC.items():
    f = f'codex/{d}/index.html'
    if not os.path.exists(f):
        continue
    h = io.open(f, encoding='utf-8').read()
    h2, k = re.subn(r'(<p>)\d{1,4}(\s+guides\b)', lambda m: m.group(1) + str(n) + m.group(2), h, count=1)
    if k and h2 != h:                     # S84: subn counts MATCHES, not CHANGES
        io.open(f, 'w', encoding='utf-8').write(h2)
        changed[f] = changed.get(f, 0) + k

# 2. codex hub discipline cards:  href="/codex/<sec>/" ... <div class="ac">NN guides</div>
f = 'codex/index.html'; h = io.open(f, encoding='utf-8').read()
def card(m):
    sec = m.group(1)
    n = SEC.get(sec)
    return m.group(0) if n is None else re.sub(r'(<div class="ac">)\d{1,4}(\s*guides)', rf'\g<1>{n}\g<2>', m.group(0))
h2, k = re.subn(r'<a href="/codex/([a-z0-9-]+)/"[^>]*>.*?<div class="ac">\d{1,4}\s*guides</div>\s*</a>',
                card, h, flags=re.S)
if k and h2 != h: io.open(f, 'w', encoding='utf-8').write(h2); changed[f] = k

# 3. homepage chips:  SEO &middot; NN guides
f = 'index.html'; h = io.open(f, encoding='utf-8').read(); o = h
for d, n in SEC.items():
    h = re.sub(r'(/codex/' + re.escape(d) + r'/"[^>]*>[^<]*?[·&middot;\s]+)\d{1,4}(\s+guides)',
               lambda m: m.group(1) + str(n) + m.group(2), h)
h = re.sub(r'(SEO\s*(?:·|&middot;)\s*)\d{1,4}(\s+guides)', rf'\g<1>{SEC.get("seo",0)}\g<2>', h)
if h != o: io.open(f, 'w', encoding='utf-8').write(h); changed[f] = changed.get(f, 0) + 1

# 4. the AI Atlas count quoted in the student programme
f = 'csp/orientation-2.html'
if os.path.exists(f):
    h = io.open(f, encoding='utf-8').read()
    h2, k = re.subn(r'\b\d{1,4}(\s+guides on AI tools)', lambda m: str(ATLAS) + m.group(1), h)
    if k and h2 != h: io.open(f, 'w', encoding='utf-8').write(h2); changed[f] = k

print(f"codex sections: {len(SEC)}  total guides: {TOTAL}  ai-atlas pages: {ATLAS}")
if not changed:
    print("  = all published counts already correct, nothing rewritten")
for f, k in sorted(changed.items()):
    print(f"  ✅ {f}: {k} count(s) CORRECTED")
