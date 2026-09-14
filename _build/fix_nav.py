#!/usr/bin/env python3
"""Session 53 — unify site navigation.

Five nav generations were live at once. Only 29 of 631 pages linked Fintech AI,
and 362 Codex pages had NO cross-section links at all — from a Codex guide you
could not reach AI Atlas, Fintech AI, AI Kids or Courses, on desktop or mobile.

This inserts any missing section links into the top nav and the mobile drawer.
It never removes an existing link, so section-local navigation survives.
Verified before every write.
"""
import glob, re, io

SECTIONS = [
    ("/codex/",      "Codex"),
    ("/ai-atlas/",   "AI Atlas"),
    ("/fintech-ai/", "Fintech AI"),
    ("/ai-kids/",    "AI Kids"),
    ("/courses/",    "Courses"),
]

stats = {k: 0 for k in ("nav_ul", "nav_div", "drawer", "written", "skipped", "no_nav")}
added = {href: 0 for href, _ in SECTIONS}
problems = []


def missing_in(block):
    return [(h, n) for h, n in SECTIONS if f'href="{h}"' not in block]


for f in sorted(glob.glob('**/*.html', recursive=True)):
    h = io.open(f, encoding='utf-8', errors='ignore').read()
    orig = h

    nm = re.search(r'<nav class="site-nav".*?</nav>', h, re.S)
    if not nm:
        stats['no_nav'] += 1
        continue
    nav = nm.group(0)

    # ---- 1. top nav -----------------------------------------------------
    miss = missing_in(nav)
    if miss:
        if '<ul class="nav-links">' in nav:
            ins = ''.join(f'<li><a href="{hr}">{n}</a></li>' for hr, n in miss)
            new_nav = nav.replace('<ul class="nav-links">',
                                  '<ul class="nav-links">' + ins, 1)
            stats['nav_ul'] += 1
        elif '<div class="nav-links">' in nav:
            ins = ''.join(f'<a href="{hr}">{n}</a>' for hr, n in miss)
            new_nav = nav.replace('<div class="nav-links">',
                                  '<div class="nav-links">\n      ' + ins, 1)
            stats['nav_div'] += 1
        else:
            problems.append(f"{f}: unknown nav-links shape")
            new_nav = nav
        if new_nav != nav:
            h = h.replace(nav, new_nav, 1)
            for hr, _ in miss:
                added[hr] += 1

    # ---- 2. mobile drawer ----------------------------------------------
    dm = re.search(r'<div class="nav-drawer".*?</div></div>', h, re.S)
    if dm:
        drawer = dm.group(0)
        dmiss = missing_in(drawer)
        if dmiss:
            anchor = '<button class="nav-close" id="navClose">&#x2715;</button></div>'
            if anchor in drawer:
                ins = ''.join(f'<a href="{hr}" class="di">{n}</a>' for hr, n in dmiss)
                new_drawer = drawer.replace(anchor, anchor + '\n  ' + ins, 1)
                h = h.replace(drawer, new_drawer, 1)
                stats['drawer'] += 1
            else:
                problems.append(f"{f}: drawer close-button anchor not found")

    # ---- 3. verify BEFORE writing --------------------------------------
    if h == orig:
        stats['skipped'] += 1
        continue
    b_o = re.sub(r'<script.*?</script>', '', orig[orig.find('<body'):], flags=re.S)
    b_n = re.sub(r'<script.*?</script>', '', h[h.find('<body'):], flags=re.S)
    if b_n.count('<div') != b_n.count('</div>'):
        problems.append(f"{f}: div imbalance — NOT written"); continue
    if b_n.count('<div') != b_o.count('<div'):
        problems.append(f"{f}: div count changed — NOT written"); continue
    if b_n.count('<a ') != b_n.count('</a>'):
        problems.append(f"{f}: anchor imbalance — NOT written"); continue
    if h.count('</html>') != 1:
        problems.append(f"{f}: structure — NOT written"); continue
    for hr, _ in SECTIONS:
        if f'href="{hr}"' not in h:
            problems.append(f"{f}: {hr} still missing after fix"); break
    else:
        io.open(f, 'w', encoding='utf-8').write(h)
        stats['written'] += 1

print(f"pages written        : {stats['written']}")
print(f"  top nav (ul/li)    : {stats['nav_ul']}")
print(f"  top nav (div/a)    : {stats['nav_div']}")
print(f"  mobile drawer      : {stats['drawer']}")
print(f"  already complete   : {stats['skipped']}")
print(f"  no site-nav        : {stats['no_nav']}")
print("\nlinks added by section:")
for hr, n in SECTIONS:
    print(f"  {n:<12} +{added[hr]}")
if problems:
    print(f"\nPROBLEMS ({len(problems)}):")
    for p in problems[:12]:
        print("  ", p)
