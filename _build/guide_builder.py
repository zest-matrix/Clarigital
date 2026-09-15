import os as _os
# Session 48: these templates were read from /tmp only and were never bundled,
# so this builder could not run in a fresh session. Now resolved from _build/
# first, with a /tmp fallback for backward compatibility.
_BD=_os.path.dirname(_os.path.abspath(__file__))
def _tpl(n):
    for c in (_os.path.join(_BD,n),'/tmp/'+n):
        if _os.path.exists(c): return open(c,encoding='utf-8').read()
    raise FileNotFoundError(n+' — expected in _build/ or /tmp')
import os, re, json
import os as _os
# Session 62: this was hardcoded to a folder named after the project's first day.
# Renaming the folder per version broke every builder. The documented workflow is
# "cp _build/*.py /tmp/ && cd <site> && python3 /tmp/x.py", so cwd IS the site root.
SITE = _os.environ.get("CLARIGITAL_SITE") or _os.getcwd()
STYLE=_tpl('codex_style.txt')
NAV=_tpl('codex_nav.txt')
GA4='<script async src="https://www.googletagmanager.com/gtag/js?id=G-7DFK94MRK7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-7DFK94MRK7\');</script>'
ICON='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNyIgZmlsbD0iI0ZGNkIzNSIvPjx0ZXh0IHg9IjE2IiB5PSIyMiIgZm9udC1mYW1pbHk9InN5c3RlbS11aSIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9IjgwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2ZmZiI+Q0w8L3RleHQ+PC9zdmc+">'

SECNAME={'seo':'SEO','analytics-cro':'Analytics & CRO','email-marketing':'Email Marketing',
'social-media':'Social Media','business-strategy':'Business Strategy','content-marketing':'Content Marketing',
'paid-advertising':'Paid Advertising','programmatic':'Programmatic','ecommerce':'E-commerce','sem':'SEM'}

def mk(path, title, meta, intro, sections, related, crumb_label, crumb_url):
    """path e.g. codex/seo/local/local-citations"""
    assert len(meta)<=165, f"META TOO LONG ({len(meta)}): {path}"
    url=f"https://www.clarigital.com/{path}/"
    body=''.join(f'<h2>{t}</h2>\n{c}\n' for t,c in sections)
    rel=''.join(f'<li><a href="{u}">{t}</a></li>' for u,t in related)
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,
        "description":meta,"url":url,"author":{"@type":"Organization","name":"Clarigital"},
        "publisher":{"@type":"Organization","name":"Clarigital"},"dateModified":"2026-05-22"})
    bc=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Codex","item":"https://www.clarigital.com/codex/"},
        {"@type":"ListItem","position":2,"name":crumb_label,"item":f"https://www.clarigital.com{crumb_url}"},
        {"@type":"ListItem","position":3,"name":title,"item":url}]})
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} — Clarigital Codex</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}"><meta property="og:url" content="{url}">
<meta property="og:site_name" content="Clarigital">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta}">
{ICON}
{GA4}
<script type="application/ld+json">{ld}</script>
<script type="application/ld+json">{bc}</script>
{STYLE}
</head>
<body>
{NAV}
<article class="guide-article">
  <div class="guide-hero"><div class="wrap">
    <nav class="breadcrumb"><a href="/codex/">Codex</a> <span class="sep">&rsaquo;</span> <a href="{crumb_url}">{crumb_label}</a> <span class="sep">&rsaquo;</span> <span>{title}</span></nav>
    <h1>{title}</h1>
    <p class="guide-intro">{intro}</p>
  </div></div>
  <div class="wrap guide-body">
    <div class="guide-content">{body}</div>
    <aside class="guide-sidebar">
      <div class="sidebar-card"><h3>Related guides</h3><ul class="sidebar-list">{rel}</ul></div>
      <div class="sidebar-card"><h3>This section</h3><a href="{crumb_url}" class="sidebar-link">{crumb_label} overview &rarr;</a></div>
    </aside>
  </div>
</article>
<footer class="site-footer"><div class="wrap"><p>Part of <a href="/">Clarigital.com</a> &middot; Free &middot; Official sources &middot; No paywalls</p></div></footer>
</body>
</html>'''
    os.makedirs(f"{SITE}/{path}", exist_ok=True)
    open(f"{SITE}/{path}/index.html",'w').write(html)
    return path

BUILT=[]
def G(*a,**k):
    BUILT.append(mk(*a,**k))

def safe_check(path):
    """Refuse to overwrite real content. Returns True if safe to write."""
    p=f"{SITE}/{path}/index.html"
    if not os.path.exists(p): return True
    h=open(p,errors='ignore').read()
    stub = '<title>Redirecting' in h or os.path.getsize(p) < 3000
    assert stub, f"⛔ REAL CONTENT at /{path}/ ({os.path.getsize(p)}b) — refusing to overwrite"
    return True

_orig_mk = mk
def mk(path,*a,**k):
    safe_check(path)
    return _orig_mk(path,*a,**k)
def G(*a,**k):
    BUILT.append(mk(*a,**k))
