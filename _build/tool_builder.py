import os as _os
# Session 48: these templates were read from /tmp only and were never bundled,
# so this builder could not run in a fresh session. Now resolved from _build/
# first, with a /tmp fallback for backward compatibility.
_BD=_os.path.dirname(_os.path.abspath(__file__))
def _tpl(n):
    for c in (_os.path.join(_BD,n),'/tmp/'+n):
        if _os.path.exists(c): return open(c,encoding='utf-8').read()
    raise FileNotFoundError(n+' — expected in _build/ or /tmp')
UPDATED = 'September 2026'   # Session 47b: was hardcoded 'May 2026'
import os,re,json
import os as _os
# Session 62: this was hardcoded to a folder named after the project's first day.
# Renaming the folder per version broke every builder. The documented workflow is
# "cp _build/*.py /tmp/ && cd <site> && python3 /tmp/x.py", so cwd IS the site root.
SITE = _os.environ.get("CLARIGITAL_SITE") or _os.getcwd()
TSTYLE=_tpl('tool_style.txt')
TNAV=_tpl('tool_nav.txt')
TFOOT=_tpl('tool_footer.txt')
TSCRIPT=_tpl('tool_scripts.txt')
GA4='<script async src="https://www.googletagmanager.com/gtag/js?id=G-7DFK94MRK7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-7DFK94MRK7\');</script>'
ICON='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNyIgZmlsbD0iIzI1NjNFQiIvPjx0ZXh0IHg9IjE2IiB5PSIyMiIgZm9udC1mYW1pbHk9InN5c3RlbS11aSIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9IjgwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2ZmZiI+Q0w8L3RleHQ+PC9zdmc+">'
TBUILT=[]

def tsafe(path):
    p=f"{SITE}/{path}/index.html"
    if not os.path.exists(p): return True
    h=open(p,errors='ignore').read()
    assert '<title>Redirecting' in h or os.path.getsize(p)<3000, f"⛔ REAL CONTENT at /{path}/ ({os.path.getsize(p)}b)"
    return True

def T(path,name,title,meta,lead,crumbs,tags,site_url,site_label,facts,green,indigo,red,related):
    """crumbs: list of (url,label). facts: list of (k,v). green/indigo/red: list of (h2,html)."""
    assert len(meta)<=165, f"META {len(meta)}: {path}"
    tsafe(path)
    url=f"https://www.clarigital.com/{path}/"
    cr=''.join(f'<a href="{u}">{l}</a><span class="sep">&rsaquo;</span>' for u,l in crumbs)
    tg=''.join(f'<span class="meta-tag mt-gray">{t}</span>' for t in tags)
    fx=''.join(f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border2)"><span>{k}</span><span style="color:var(--fg);font-weight:500">{v}</span></div>' for k,v in facts)
    def lane(cid,secs):
        return f'<div class="lane-section" id="lane-{cid}">'+''.join(f'<h2>{t}</h2>\n{c}\n' for t,c in secs)+'</div>'
    rel=''.join(f'<a href="{u}" class="sidebar-link">{t}</a>' for u,t in related)
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":meta,
      "url":url,"author":{"@type":"Organization","name":"Clarigital"},
      "publisher":{"@type":"Organization","name":"Clarigital"},"dateModified":"2026-05-22"})
    bc=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":
      [{"@type":"ListItem","position":i+1,"name":l,"item":"https://www.clarigital.com"+u} for i,(u,l) in enumerate(crumbs)]
      +[{"@type":"ListItem","position":len(crumbs)+1,"name":name,"item":url}]})
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
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
{TSTYLE}
</head>
<body>
{TNAV}
<section class="page-hero">
  <div class="wrap">
    <nav class="breadcrumb">{cr}<span>{name}</span></nav>
    <span class="label-tag">{tags[0] if tags else 'AI Tool'}</span>
    <h1>{name} — The Complete Guide</h1>
    <p class="hero-lead">{lead}</p>
    <div class="art-meta">{tg}<span class="meta-tag mt-gray">Updated {UPDATED}</span></div>
  <div style="margin-top:16px"><a href="{site_url}" target="_blank" rel="noopener" class="btn-official" style="display:inline-flex;align-items:center;gap:8px;background:var(--indigo);color:#fff;font-size:.85rem;font-weight:600;padding:10px 20px;border-radius:100px;text-decoration:none" onmouseover="this.style.filter='brightness(1.1)'" onmouseout="this.style.filter='none'">Visit {name} &#8599;</a><span style="font-size:.75rem;color:var(--muted);margin-left:10px">{site_label}</span></div>
</div>
</section>
<div style="background:var(--card-bg);border-bottom:1px solid rgba(99,102,241,.12)">
  <div class="wrap">
    <div class="lane-tabs" role="tablist">
      <button class="lane-tab" id="tab-green" role="tab" onclick="showLane('green')"><span class="lane-dot dot-green"></span><span class="lane-label">Simple</span></button>
      <button class="lane-tab" id="tab-indigo" role="tab" onclick="showLane('indigo')"><span class="lane-dot dot-indigo"></span><span class="lane-label">Working</span></button>
      <button class="lane-tab" id="tab-red" role="tab" onclick="showLane('red')"><span class="lane-dot dot-red"></span><span class="lane-label">Deep</span></button>
    </div>
  </div>
</div>
<div class="wrap">
<div class="art-layout">
<div class="art-body">
{lane('green',green)}
{lane('indigo',indigo)}
{lane('red',red)}
</div>
<div class="art-sidebar">
  <div class="sidebar-card">
    <h4>Quick facts</h4>
    <div style="font-size:.82rem;color:var(--muted);line-height:1.7">{fx}</div>
  </div>
  <div class="sidebar-card">
    <h4 style="color:var(--indigo);font-size:.8rem">&#128279; Official</h4>
    <a href="{site_url}" target="_blank" rel="noopener" class="sidebar-link">{site_label} &#8599;</a>
  </div>
  <div class="sidebar-card">
    <h4>Related</h4>
    {rel}
  </div>
</div>
</div>
</div>
{TFOOT}
{TSCRIPT}
</body>
</html>'''
    os.makedirs(f"{SITE}/{path}",exist_ok=True)
    open(f"{SITE}/{path}/index.html",'w').write(html)
    TBUILT.append(path)
    return path
