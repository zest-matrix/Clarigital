import os as _os
# Session 48: these templates were read from /tmp only and were never bundled,
# so this builder could not run in a fresh session. Now resolved from _build/
# first, with a /tmp fallback for backward compatibility.
_BD=_os.path.dirname(_os.path.abspath(__file__))
def _tpl(n):
    for c in (_os.path.join(_BD,n),'/tmp/'+n):
        if _os.path.exists(c): return open(c,encoding='utf-8').read()
    raise FileNotFoundError(n+' — expected in _build/ or /tmp')
import os,re,json
import os as _os
# Session 62: this was hardcoded to a folder named after the project's first day.
# Renaming the folder per version broke every builder. The documented workflow is
# "cp _build/*.py /tmp/ && cd <site> && python3 /tmp/x.py", so cwd IS the site root.
SITE = _os.environ.get("CLARIGITAL_SITE") or _os.getcwd()
ASTYLE=_tpl('atlas_style.txt')
ANAV=_tpl('atlas_nav.txt')
AFOOT=_tpl('atlas_footer.txt')
GA4='<script async src="https://www.googletagmanager.com/gtag/js?id=G-7DFK94MRK7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-7DFK94MRK7\');</script>'
AICON='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNyIgZmlsbD0iIzI1NjNFQiIvPjx0ZXh0IHg9IjE2IiB5PSIyMiIgZm9udC1mYW1pbHk9InN5c3RlbS11aSIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9IjgwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2ZmZiI+Q0w8L3RleHQ+PC9zdmc+">'
ABUILT=[]

def asafe(path):
    p=f"{SITE}/{path}/index.html"
    if not os.path.exists(p): return True
    h=open(p,errors='ignore').read()
    stub='<title>Redirecting' in h or os.path.getsize(p)<3000
    assert stub, f"⛔ REAL CONTENT at /{path}/ ({os.path.getsize(p)}b)"
    return True

def A(path,title,meta,lead,label,sections,related):
    """Build an AI Atlas concept page (dark theme)."""
    assert len(meta)<=165, f"META {len(meta)}: {path}"
    asafe(path)
    url=f"https://www.clarigital.com/{path}/"
    body=''.join(f'<h2>{t}</h2>\n{c}\n' for t,c in sections)
    rel=''.join(f'<a href="{u}" class="sidebar-link">{t}</a>' for u,t in related)
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":meta,
        "url":url,"author":{"@type":"Organization","name":"Clarigital"},
        "publisher":{"@type":"Organization","name":"Clarigital"},"dateModified":"2026-05-22"})
    bc=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":"https://www.clarigital.com/"},
        {"@type":"ListItem","position":2,"name":"AI Atlas","item":"https://www.clarigital.com/ai-atlas/"},
        {"@type":"ListItem","position":3,"name":title,"item":url}]})
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} | Clarigital AI Atlas</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{title}">
<meta property="og:description" content="{meta}"><meta property="og:url" content="{url}">
<meta property="og:site_name" content="Clarigital">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{meta}">
{AICON}
{GA4}
<script type="application/ld+json">{ld}</script>
<script type="application/ld+json">{bc}</script>
{ASTYLE}
</head>
<body>
{ANAV}
<div class="page-hero">
  <div class="wrap">
    <nav class="breadcrumb"><a href="/">Home</a><span class="sep">&rsaquo;</span><a href="/ai-atlas/">AI Atlas</a><span class="sep">&rsaquo;</span><span>{title}</span></nav>
    <div class="label-tag">{label}</div>
    <h1>{title}</h1>
    <p class="hero-lead">{lead}</p>
    <div class="art-meta"><span class="meta-tag mt-indigo">{label}</span><span class="meta-tag"><time datetime="2026-05-22">Last verified: May 2026</time></span></div>
  </div>
</div>
<div class="wrap">
  <div class="art-layout">
    <main style="min-width:0">
{body}
    </main>
    <aside class="art-sidebar">
      <div class="sidebar-card">
        <h4 class="sidebar-heading" style="font-size:.78rem;font-weight:700;color:rgba(241,245,249,.6);text-transform:uppercase;letter-spacing:.07em;margin-bottom:10px">Related</h4>
        {rel}
      </div>
    </aside>
  </div>
</div>
{AFOOT}'''
    os.makedirs(f"{SITE}/{path}",exist_ok=True)
    open(f"{SITE}/{path}/index.html",'w').write(html)
    ABUILT.append(path)
    return path
