#!/usr/bin/env python3
"""newpage_check.py — run the page-level QA SOP against specific pages.

The SOP is checked in full every fifth session. That is too late for a page
built in session N+1. This runs every page-level item at creation.

    python3 /tmp/newpage_check.py fintech-ai/products/video-kyc/index.html
    python3 /tmp/newpage_check.py --changed      # anything newer than manifest.json

Exit code 1 if any BLOCKER fails, so it can gate a build script.
Sections refer to _build/QA-SOP.md.
"""
import sys, os, re, json, glob, html as H, subprocess

BASE = 'https://www.clarigital.com'
BLOCK, WARN, INFO = 'BLOCK', 'WARN', 'INFO'


def checks(path, h):
    """Yield (level, sop_ref, ok, detail)."""
    body = h[h.find('<body'):]
    nos = re.sub(r'<script.*?</script>', '', body, flags=re.S)

    # ---- A. STRUCTURE ----------------------------------------------------
    yield (BLOCK, 'A1 div balance', nos.count('<div') == nos.count('</div>'),
           f"{nos.count('<div')}/{nos.count('</div>')}")
    for t in ('section', 'main', 'nav', 'article', 'aside', 'header', 'footer', 'table', 'form'):
        o, c = len(re.findall(r'<' + t + r'[\s>]', h)), h.count(f'</{t}>')
        if o or c:
            yield (BLOCK, f'A2 <{t}> balance', o == c, f"{o}/{c}")

    stack, nest = [], 0
    for m in re.finditer(r'<(/?)(div|section|main|header|footer|article|nav|aside)\b[^>]*>', nos):
        if not m.group(1):
            stack.append(m.group(2))
        elif not stack or stack[-1] != m.group(2):
            nest += 1
            stack and stack.pop()
        else:
            stack.pop()
    yield (BLOCK, 'A3 nesting order', nest == 0 and not stack, f"{nest + len(stack)} errors")
    yield (BLOCK, 'A4 exactly one <h1>', len(re.findall(r'<h1[\s>]', h)) == 1,
           str(len(re.findall(r'<h1[\s>]', h))))
    yield (BLOCK, 'A5 doc structure', h.count('</html>') == 1 and h.count('</body>') == 1, '')

    levels = [int(m.group(1)) for m in re.finditer(r'<h([1-6])[\s>]', h)]
    skips = sum(1 for a, b in zip(levels, levels[1:]) if b > a + 1)
    yield (WARN, 'A7 heading order', skips == 0, f"{skips} level skips")

    # ---- B. LINKS --------------------------------------------------------
    anch = nos.count('<a ') == nos.count('</a>')
    yield (BLOCK, 'B0 anchor balance', anch, f"{nos.count('<a ')}/{nos.count('</a>')}")
    broken = [u for u in re.findall(r'href="(/[^"#?]*)"', h)
              if not os.path.exists(u.lstrip('/') or 'index.html')
              and not os.path.exists(u.strip('/') + '/index.html')
              and not os.path.exists(u.strip('/'))]
    yield (BLOCK, 'B1 internal links resolve', not broken, ', '.join(sorted(set(broken))[:3]))
    yield (BLOCK, 'B4 nav has all five sections',
           all(f'href="{s}"' in h for s in
               ('/codex/', '/ai-atlas/', '/fintech-ai/', '/ai-kids/', '/courses/'))
           or 'kids-nav' in h, '')
    yield (BLOCK, 'B5 route to home',
           bool(re.search(r'href="/"|href="https://(?:www\.)?clarigital\.com/?"', h)), '')

    # ---- E. SEO ----------------------------------------------------------
    t = re.search(r'<title>(.*?)</title>', h, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    c = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    u = re.search(r'<meta property="og:url" content="([^"]*)"', h)
    g = re.search(r'<meta property="og:title" content="([^"]*)"', h)
    yield (BLOCK, 'E1 title <=65', bool(t) and len(t.group(1)) <= 65,
           f"{len(t.group(1)) if t else 0} chars")
    yield (BLOCK, 'E2 meta <=165', bool(d) and len(d.group(1)) <= 165,
           f"{len(d.group(1)) if d else 0} chars")
    yield (BLOCK, 'E4 canonical absolute', bool(c) and c.group(1).startswith('http'),
           c.group(1) if c else 'missing')
    yield (BLOCK, 'E5 og:url == canonical',
           bool(c and u) and c.group(1).rstrip('/') == u.group(1).rstrip('/'), '')
    if t and g:
        tw = set(re.findall(r'[a-z]{4,}', H.unescape(t.group(1)).lower()))
        gw = set(re.findall(r'[a-z]{4,}', H.unescape(g.group(1)).lower()))
        yield (BLOCK, 'C5/E6 og:title not leaked', not (tw and gw and not tw & gw), '')
    ogi = re.search(r'<meta property="og:image" content="[^"]*?(/[^"/]+\.(?:png|jpg|webp))"', h)
    yield (BLOCK, 'E7 og:image file exists',
           bool(ogi) and os.path.exists(ogi.group(1).lstrip('/')),
           ogi.group(1) if ogi else 'missing')
    ld_ok = True
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            json.loads(b)
        except Exception:
            ld_ok = False
    yield (BLOCK, 'E8 JSON-LD valid', ld_ok, '')
    yield (BLOCK, 'E10 no malformed absolute URLs',
           not re.search(r'clarigital\.com/https:|digitalcodex\.com', h), '')

    # ---- F. ACCESSIBILITY ------------------------------------------------
    yield (BLOCK, 'F1 <html lang>', bool(re.search(r'<html[^>]*lang=', h)), '')
    imgs = re.findall(r'<img[^>]*>', h)
    yield (BLOCK, 'F2 img alt', all('alt=' in i for i in imgs), f"{len(imgs)} images")
    yield (BLOCK, 'F4 skip link + target',
           'class="skip-link"' in h and h.count('id="main-content"') == 1, '')

    # ---- H. MOBILE -------------------------------------------------------
    yield (BLOCK, 'H1 viewport', bool(re.search(r'name="viewport"', h)), '')
    css = ' '.join(re.findall(r'<style>(.*?)</style>', h, re.S))
    wide = [w for w in re.findall(r'(?:^|[;{])\s*(?:min-)?width:\s*(\d{3,})px', css) if int(w) > 380]
    yield (WARN, 'H2 no fixed widths >380px', not wide, ', '.join(wide[:3]))
    yield (WARN, 'H3 table overflow rule', '<table' not in h or 'overflow-x' in css, '')

    # ---- I. JAVASCRIPT ---------------------------------------------------
    js_ok = True
    for s in re.findall(r'<script>(.*?)</script>', h, re.S):
        open('/tmp/_np.js', 'w').write(s)
        if subprocess.run(['node', '--check', '/tmp/_np.js'], capture_output=True).returncode:
            js_ok = False
    yield (BLOCK, 'I1 <script> parses', js_ok, '')
    hs = re.findall(r'\bon\w+="([^"]*)"', h)
    if hs:
        open('/tmp/_np.js', 'w').write('function _w(){%s}' %
                                       '\n'.join(x.replace('&quot;', '"').replace('&amp;', '&')
                                                 .replace('&#39;', "'") for x in hs))
        ok = subprocess.run(['node', '--check', '/tmp/_np.js'], capture_output=True).returncode == 0
        yield (BLOCK, 'I2 inline handlers parse', ok, f"{len(hs)} handlers")
        defined = set(re.findall(r'function\s+(\w+)\s*\(', h))
        called = set()
        for a in hs:
            for stmt in re.split(r';', a):
                m2 = re.match(r"\s*(?:return\s+)?([A-Za-z_$][\w$]*)\s*\(", stmt)
                if m2:
                    called.add(m2.group(1))
        BUILTIN = {'alert', 'parseInt', 'parseFloat', 'String', 'Number', 'Boolean', 'Math',
                   'Date', 'JSON', 'encodeURIComponent', 'decodeURIComponent', 'setTimeout',
                   'setInterval', 'fetch', 'confirm', 'prompt', 'require', 'eval'}
        miss = sorted(called - defined - BUILTIN)
        yield (BLOCK, 'I3 handlers defined', not miss, ', '.join(miss[:3]))
    yield (BLOCK, 'I5 no inline display:none on togglable content',
           not re.search(r'class="[^"]*\b(quiz-body|track-panel|lane-section|tab-panel)\b[^"]*"'
                         r'[^>]*style="[^"]*display:\s*none', h), '')
    defined_css = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    used = set()
    for a in re.findall(r'class="([^"]+)"', re.sub(r'<style>.*?</style>', '', h, flags=re.S)):
        used.update(a.split())
    JS_ADDED = {'open', 'active', 'cur', 'js', 'show', 'hidden', 'on', 'selected',
                'done', 'visible', 'wrong', 'correct'}
    orphan = sorted(used - defined_css - JS_ADDED)
    yield (WARN, 'I7 classes have CSS', not orphan, ', '.join(orphan[:4]))

    # ---- K. ANALYTICS ----------------------------------------------------
    yield (BLOCK, 'K1 GA4 present', 'googletagmanager.com' in h or 'gtag(' in h, '')

    # ---- D. SOURCES ------------------------------------------------------
    if '/build-sheet/' in path or '/products/' in path:
        yield (BLOCK, 'D1 sources block', 'id="sources"' in h, '')


def run(paths):
    worst = 0
    for p in paths:
        h = open(p, encoding='utf-8', errors='ignore').read()
        rows = list(checks(p, h))
        fails = [r for r in rows if not r[2]]
        blockers = [r for r in fails if r[0] == BLOCK]
        mark = '✅' if not fails else ('❌' if blockers else '⚠️')
        print(f"\n{mark} {p}   ({len(rows)} checks, {len(fails)} failed)")
        for lvl, ref, ok, det in fails:
            print(f"    {lvl:5} {ref}" + (f"  — {det}" if det else ''))
        if blockers:
            worst = 1
    print(f"\n{'FAIL — blockers present' if worst else 'PASS'}")
    return worst


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--changed' in sys.argv:
        ref = os.path.getmtime('manifest.json')
        args = [f for f in glob.glob('**/*.html', recursive=True)
                if os.path.getmtime(f) >= ref - 1]
    if not args:
        print(__doc__)
        sys.exit(0)
    sys.exit(run(args))
