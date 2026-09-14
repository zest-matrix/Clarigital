import glob,re,subprocess,os
def render_check(verbose=True):
    """Content must be visible WITHOUT JavaScript. Non-JS crawlers and LLM
    fetchers do not execute scripts - content hidden behind JS is invisible
    to them. Also catches inline display:none beating a CSS .active class."""
    bad={}
    for f in glob.glob('**/index.html',recursive=True):
        h=open(f,errors='ignore').read(); iss=[]
        # courses: track panels
        if 'track-panel' in h:
            if re.search(r'track-panel" id="track-\w+" style="display:\s*none',h):
                iss.append('track_inline_hidden')
            if '<div class="track-panel active" id="track-beginner">' not in h:
                iss.append('no_default_track')
            if '.track-panel{display:block}' not in h:
                iss.append('tracks_hidden_without_js')
            nb=len(re.findall(r'<div class="depth-band">',h))
            npn=len(re.findall(r'<div class="track-panel',h))
            if nb!=npn: iss.append('depth_bands_mismatch')
            if h.count('<div class="crs-layout">')!=1:
                iss.append('rail_layout_missing')
        # lane pages: content must render without JS
        if 'lane-section' in h:
            if '.lane-section{display:block}' not in h:
                iss.append('lanes_hidden_without_js')
            nb=len(re.findall(r'<div class="depth-band">',h))
            nl=len(re.findall(r'<div class="lane-section"',h))
            if nb!=nl: iss.append('depth_bands_mismatch')
            if re.search(r'<button[^>]*lane-tab',h): iss.append('lane_tabs_remain')
        # any JS syntax error breaks every interaction on the page
        for s in re.findall(r'<script>(.*?)</script>',h,re.DOTALL):
            open('/tmp/_rc.js','w').write(s)
            if subprocess.run(['node','--check','/tmp/_rc.js'],capture_output=True).returncode:
                iss.append('js_syntax_error'); break
        if iss: bad[f]=iss
    if verbose:
        print(f"Pages with render problems: {len(bad)}")
        for f,i in list(bad.items())[:15]: print(f"  {f}: {i}")
    return bad

def thin_content(threshold=800, verbose=True):
    """Reportable metric, not a zero-target. Counts CONTENT pages (depth>=2)
    whose visible word count is below threshold."""
    thin=[]
    for f in glob.glob('**/index.html',recursive=True):
        if f.count('/')<2: continue
        if f.startswith('ai-kids/'): continue      # activity pages, short by design
        h=open(f,errors='ignore').read()
        b=h[h.find('<body'):]
        b=re.sub(r'<script.*?</script>','',b,flags=re.DOTALL)
        b=re.sub(r'<style.*?</style>','',b,flags=re.DOTALL)
        w=len(re.sub(r'<[^>]+>',' ',b).split())
        if w<threshold: thin.append((w,f))
    thin.sort()
    if verbose: print(f"Content pages under {threshold} words: {len(thin)}")
    return thin


# ─────────────────────────────────────────────────────────────────────────
# Session 47b. Three defects shipped past all 15 checks because nothing ever
# looked inside an inline event attribute:
#   * onclick="checkAnswer(this,True)"  — Python bools written into JavaScript,
#     1,560 occurrences across 65 pages. node --check only ever saw <script>.
#   * checkAnswer() was never defined ANYWHERE on the site.
#   * style="display:none" on .quiz-body beat .quiz-body.open, so the toggle
#     silently did nothing. Also a rule-6 violation.
# ─────────────────────────────────────────────────────────────────────────

ATTRS = ('onclick','onchange','onsubmit','oninput','onmouseover','onmouseout','onkeyup','onfocus','onblur')

def handler_check(verbose=True):
    """Inline event attributes must (a) parse as JavaScript and (b) call only
    functions that exist on the page."""
    bad={}
    pat = re.compile(r'\b(' + '|'.join(ATTRS) + r')="([^"]*)"')
    _batch=[]; _order=[]
    for f in glob.glob('**/*.html', recursive=True):
        h=open(f,errors='ignore').read(); iss=[]
        defined=set(re.findall(r'function\s+(\w+)\s*\(', h))
        defined |= set(re.findall(r'window\.(\w+)\s*=', h))
        defined |= set(re.findall(r'(?:var|let|const)\s+(\w+)\s*=\s*function', h))
        called=set(); bodies=[]
        for m in pat.finditer(h):
            body=m.group(2).replace('&quot;','"').replace('&amp;','&').replace('&#39;',"'")
            bodies.append(body)
            # Only TOP-LEVEL calls — the handler the attribute actually invokes.
            # Anything after a dot is a method on a built-in (document.getElementById,
            # navigator.clipboard.writeText); anything inside a string is CSS (rgba).
            for stmt in re.split(r';', body):
                m2 = re.match(r"\s*(?:return\s+)?([A-Za-z_$][\w$]*)\s*\(", stmt)
                if m2: called.add(m2.group(1))
        BUILTIN={'alert','parseInt','parseFloat','String','Number','Boolean','Math','Date',
                 'JSON','encodeURIComponent','decodeURIComponent','setTimeout','setInterval',
                 'fetch','confirm','prompt','require','eval',
                 'if','for','return','typeof'}
        missing=sorted(c for c in called if c not in defined and c not in BUILTIN)
        if missing: iss.append('undefined_handler:'+','.join(missing[:4]))
        if bodies:
            _order.append((f,bodies))
            _batch.append('function _h%d(){%s}' % (len(_order),'\n'.join(bodies)))
        if iss: bad[f]=iss
    # Session 48: this spawned `node` once per page (851 processes) and pushed the
    # whole audit past its time limit. One process for the lot; bisect only on failure.
    def _nc(src):
        open('/tmp/_hb.js','w').write(src)
        return subprocess.run(['node','--check','/tmp/_hb.js'],capture_output=True).returncode==0
    if _batch and not _nc('\n'.join(_batch)):
        for f,bodies in _order:
            if not _nc('function _x(){%s}' % '\n'.join(bodies)):
                bad.setdefault(f,[]).append('inline_js_syntax_error')
    if verbose:
        print(f"Pages with inline-handler problems: {len(bad)}")
        for f,i in list(bad.items())[:15]: print(f"  {f}: {i}")
    return bad


TOGGLABLE = ('quiz-body','track-panel','lane-section','tab-panel')

def inline_hidden_check(verbose=True):
    """Content that a JS class toggle is supposed to reveal must not carry an
    inline display:none — inline style always beats the class."""
    bad={}
    for f in glob.glob('**/*.html', recursive=True):
        h=open(f,errors='ignore').read(); iss=[]
        for cls in TOGGLABLE:
            if re.search(r'class="[^"]*\b'+cls+r'\b[^"]*"[^>]*style="[^"]*display:\s*none', h):
                iss.append(f'inline_hidden:{cls}')
        if iss: bad[f]=iss
    if verbose:
        print(f"Pages hiding togglable content inline: {len(bad)}")
        for f,i in list(bad.items())[:15]: print(f"  {f}: {i}")
    return bad


def stale_stamps(months=4, verbose=True):
    """Session 66 note: this metric OVER-COUNTS. Of 292 pre-May-2026 stamps,
    138 sit on pages with no figure that can decay -- a conceptual guide whose
    dateModified says April 2026 is CORRECT, and bumping it would be lying to
    readers and to search engines about freshness. Only the ~101 pages that
    quote prices or dated regulation are a real re-verification backlog.
    Use decaying_stamps() for the number that matters."""
    """Reportable metric. A stale date is valid HTML, valid JSON-LD and a working
    page, which is exactly why 545 pages carried a four-month-old dateModified
    without any check noticing."""
    import datetime
    today=datetime.date.today()
    cut=today-datetime.timedelta(days=months*30)
    MON={m:i+1 for i,m in enumerate(['January','February','March','April','May','June',
         'July','August','September','October','November','December'])}
    stale=[]
    for f in glob.glob('**/*.html', recursive=True):
        h=open(f,errors='ignore').read(); why=[]
        for d in re.findall(r'"dateModified":\s*"(\d{4})-(\d{2})-(\d{2})"', h):
            if datetime.date(int(d[0]),int(d[1]),int(d[2])) < cut: why.append('dateModified')
        for mo,yr in re.findall(r'(?:Verified|Updated) ([A-Z][a-z]+) (\d{4})', h):
            if mo in MON and datetime.date(int(yr),MON[mo],1) < cut: why.append('stamp')
        if why: stale.append((f,sorted(set(why))))
    if verbose: print(f"Pages with stamps older than {months} months: {len(stale)}")
    return stale


BLOCK = ('div','section','main','header','footer','article','nav','aside')

def nesting_errors(verbose=True):
    """Session 51 metric. COUNTING tags cannot detect two errors that cancel:
    an unclosed <div class="chapter"> plus a spare </div> in the tail balances
    perfectly and still produces a scrambled tree. This walks the stack instead.
    Browsers silently repair it; HTML parsers and LLM crawlers do not."""
    bad = {}
    pat = re.compile(r'<(/?)(' + '|'.join(BLOCK) + r')\b[^>]*>')
    for f in glob.glob('**/*.html', recursive=True):
        h = open(f, errors='ignore').read()
        b = re.sub(r'<script.*?</script>', '', h[h.find('<body'):], flags=re.S)
        stack, errs = [], []
        for m in pat.finditer(b):
            if not m.group(1):
                stack.append(m.group(2))
            elif not stack or stack[-1] != m.group(2):
                errs.append(f"</{m.group(2)}> closes <{stack[-1] if stack else 'NOTHING'}>")
                if stack: stack.pop()
            else:
                stack.pop()
        errs += [f"never_closed:<{t}>" for t in stack]
        if errs: bad[f] = errs
    if verbose:
        print(f"Pages with block-nesting errors: {len(bad)}")
        for f, e in list(bad.items())[:10]: print(f"  {f}: {e[:2]}")
    return bad


CANON_SECTIONS = ('/codex/', '/ai-atlas/', '/fintech-ai/', '/ai-kids/', '/courses/')

def nav_coverage(verbose=True):
    """Session 53. Five nav generations were live at once and only 29 of 631
    pages linked Fintech AI. 362 Codex pages had NO cross-section links at all —
    from a Codex guide you could not reach any other section, on any device.
    Nothing checked this, because every page's nav was internally valid."""
    bad = {}
    for f in glob.glob('**/*.html', recursive=True):
        h = open(f, errors='ignore').read()
        nm = re.search(r'<nav class="site-nav".*?</nav>', h, re.S)
        if not nm:
            continue                      # kids-nav and standalone pages opt out
        nav = nm.group(0)
        miss = [s for s in CANON_SECTIONS if f'href="{s}"' not in nav]
        dm = re.search(r'<div class="nav-drawer".*?\n</div>', h, re.S)
        if dm:
            miss += [s + '(drawer)' for s in CANON_SECTIONS
                     if f'href="{s}"' not in dm.group(0)]
        if miss:
            bad[f] = miss
    if verbose:
        print(f"Pages missing a canonical section link: {len(bad)}")
        for f, m in list(bad.items())[:10]:
            print(f"  {f}: {m[:4]}")
    return bad


HOME = re.compile(r'href="/"|href="https://(?:www\.)?clarigital\.com/?"')

def home_route(verbose=True):
    """Session 56. 224 pages sat outside the site-nav system and nothing checked
    them. 98 CSP task pages showed a Clarigital logo that was not a link at all —
    a student on a task page had no way back to the site. AI Kids deliberately
    keeps its own nav (different audience, different safety framing) but must
    still offer one route out."""
    bad = [f for f in glob.glob('**/*.html', recursive=True)
           if f != 'index.html'
           and not HOME.search(open(f, errors='ignore').read())]
    if verbose:
        print(f"Pages with no route to the site root: {len(bad)}")
        for f in bad[:10]: print("  ", f)
    return bad


# classes that JavaScript adds at runtime, so absence from markup-time CSS is fine
_JS_CLASSES = {'open','active','cur','js','show','hidden','on','selected','done',
               'visible','killed','wrong','correct'}

def orphan_classes(verbose=True):
    """Session 59 QA. Classes used in markup with NO CSS rule on the page.
    This is exactly the .quiz-opts failure of Session 47b, where the generator
    drifted away from the stylesheet and the quiz rendered unstyled.

    Most hits are harmless dead hooks left by a redesign (.guide-hero etc, where
    .art-layout does the real work). The dangerous ones are ELEMENTS THAT NEED
    STYLING TO EXIST AT ALL -- the course progress bar had four undefined
    classes and rendered as nothing on 65 pages. Triage, do not bulk-fix."""
    from collections import Counter
    orphan, where = Counter(), {}
    for f in glob.glob('**/*.html', recursive=True):
        h = open(f, errors='ignore').read()
        css = ' '.join(re.findall(r'<style>(.*?)</style>', h, re.S))
        if not css:
            continue
        defined = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
        body = re.sub(r'<style>.*?</style>', '', h, flags=re.S)
        used = set()
        for attr in re.findall(r'class="([^"]+)"', body):
            used.update(attr.split())
        for c in used - defined - _JS_CLASSES:
            if not c.startswith('lang-'):
                orphan[c] += 1
                where.setdefault(c, f)
    if verbose:
        print(f"Distinct classes with no CSS rule: {len(orphan)}")
        for c, n in orphan.most_common(12):
            print(f"  {n:>4}x .{c}  e.g. {where[c]}")
    return orphan


def og_image_exists(verbose=True):
    """Session 60. The og:image check only ever verified the TAG was present.
    A new track shipped pointing at /og-kids.png, which does not exist -- the
    file is og-ai-kids.png. Social previews would have rendered blank and every
    check was green."""
    import os
    bad = {}
    for f in glob.glob('**/*.html', recursive=True):
        h = open(f, errors='ignore').read()
        for m in re.finditer(r'<meta property="og:image" content="[^"]*?(/[^"/]+\.(?:png|jpg|jpeg|webp))"', h):
            if not os.path.exists(m.group(1).lstrip('/')):
                bad[f] = m.group(1)
    if verbose:
        print(f"Pages whose og:image file is missing: {len(bad)}")
        for f, u in list(bad.items())[:10]: print(f"  {f}: {u}")
    return bad


def missing_sources(verbose=True):
    """Session 63. Build sheets and product guides carry verifiable figures --
    prices, thresholds, statutory dates. Every one must say where it came from
    and how that source is typed (official / research / vendor / industry).
    Modules are exempt for now; they are explanatory rather than figure-heavy.
    Scope will widen in the module sources pass."""
    # Session 65: scope widened from build sheets to EVERY fintech page that
    # makes verifiable claims. The section hub is the single exemption -- it is
    # navigation, and its claims live on the pages it links to.
    EXEMPT = {'fintech-ai/index.html'}
    bad = []
    for f in glob.glob('fintech-ai/**/index.html', recursive=True):
        if f in EXEMPT:
            continue
        h = open(f, errors='ignore').read()
        if 'id="sources"' not in h:
            bad.append(f)
    if verbose:
        print(f"Build sheets / product guides with no sources block: {len(bad)}")
        for f in bad[:10]: print("  ", f)
    return bad


def bad_absolute_urls(verbose=True):
    """Session 66. A page carried `clarigital.com/https:/www.yourdigitalcodex.com/...`
    in its canonical, og:url AND breadcrumb JSON-LD -- a concatenation bug pointing at
    a domain this site no longer uses, with breadcrumb names of "Https:" and
    "Www.Yourdigitalcodex.Com". linkcheck never saw it because it only validates
    paths, not whether an absolute URL is coherent."""
    bad = {}
    for f in glob.glob('**/*.html', recursive=True):
        h = open(f, errors='ignore').read()
        hits = re.findall(r'https?://[^"\'<> ]*(?:clarigital\.com/https:|digitalcodex\.com)[^"\'<> ]*', h)
        if hits:
            bad[f] = sorted(set(hits))[:3]
    if verbose:
        print(f"Pages with malformed or foreign absolute URLs: {len(bad)}")
        for f, u in list(bad.items())[:10]: print(f"  {f}: {u}")
    return bad


def decaying_stamps(verbose=True):
    """The honest version of stale_stamps: only pages whose old verification
    stamp sits next to something that decays -- money, pricing, or a dated rule."""
    import datetime
    cut = datetime.date.today() - datetime.timedelta(days=120)
    MON = {m: i+1 for i, m in enumerate(['January','February','March','April','May','June',
           'July','August','September','October','November','December'])}
    ABB = {m[:3]: i+1 for i, m in enumerate(MON)}
    out = []
    for f in glob.glob('**/*.html', recursive=True):
        h = open(f, errors='ignore').read()
        old = False
        for mo, yr in re.findall(r'(?:Verified|Updated) ([A-Z][a-z]{2,8}) (\d{4})', h):
            n = MON.get(mo) or ABB.get(mo[:3])
            if n and datetime.date(int(yr), n, 1) < cut:
                old = True
        if old and re.search(r'(?:\$|\u20b9|&#8377;|USD|INR)\s?[\d,]+|\bper month\b|\bpricing\b', h, re.I):
            out.append(f)
    if verbose:
        print(f"Pages with an old stamp NEXT TO a decaying figure: {len(out)}")
    return out
