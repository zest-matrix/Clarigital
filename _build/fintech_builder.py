import os,re,json,html as Hm
import os as _os
# Session 62: this was hardcoded to a folder named after the project's first day.
# Renaming the folder per version broke every builder. The documented workflow is
# "cp _build/*.py /tmp/ && cd <site> && python3 /tmp/x.py", so cwd IS the site root.
SITE = _os.environ.get("CLARIGITAL_SITE") or _os.getcwd()
BASE="https://www.clarigital.com"
GA4='<script async src="https://www.googletagmanager.com/gtag/js?id=G-7DFK94MRK7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-7DFK94MRK7\');</script>'
ICON='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNyIgZmlsbD0iIzEwQjk4MSIvPjx0ZXh0IHg9IjE2IiB5PSIyMiIgZm9udC1mYW1pbHk9InN5c3RlbS11aSIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9IjgwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2ZmZiI+Q0w8L3RleHQ+PC9zdmc+">'
FBUILT=[]

# Session 47: these were hardcoded to 'May 2026' / '2026-05-22' in three places,
# so every page built after May 2026 shipped a stale verification stamp and a
# stale dateModified. Set them once per session; page() reads them.
VERIFIED = 'September 2026'      # human-readable stamp in hero + registry blocks
DATEMOD  = '2026-09-15'          # JSON-LD dateModified, ISO

STYLE='''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--bg:#0F172A;--bg2:#111827;--card:#151C2C;--border:#1E293B;--border2:#243044;
--fg:#F1F5F9;--muted:#94A3B8;--faint:#64748B;--green:#10B981;--teal:#14B8A6;--teal-dim:rgba(20,184,166,.09);--indigo:#6366F1;--amber:#F59E0B;--red:#EF4444;--blue:#2563EB}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--fg);line-height:1.75;font-size:16px;-webkit-font-smoothing:antialiased}
a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1240px;margin:0 auto;padding:0 24px}
/* nav */
.site-nav{background:rgba(15,23,42,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:200}
.nav-in{max-width:1240px;margin:0 auto;padding:0 24px;height:58px;display:flex;align-items:center;gap:20px}
.nav-logo{display:flex;align-items:center;gap:9px;font-weight:700;color:var(--fg);font-size:1rem}
.logo-mark{width:30px;height:30px;border-radius:8px;background:var(--green);display:flex;align-items:center;justify-content:center;font-size:.72rem;font-weight:800;color:#fff}
.nav-links{display:flex;gap:2px;margin-left:auto;flex-wrap:wrap}
.nav-links a{font-size:.82rem;color:var(--muted);padding:6px 11px;border-radius:7px}
.nav-links a:hover,.nav-links a.active{background:var(--border);color:var(--fg);text-decoration:none}
/* hero */
.page-hero{padding:44px 0 28px;border-bottom:1px solid var(--border);background:linear-gradient(180deg,rgba(20,184,166,.08),transparent)}
.breadcrumb{font-size:.78rem;color:var(--faint);margin-bottom:14px}
.breadcrumb a{color:var(--faint)}.breadcrumb .sep{margin:0 7px;opacity:.5}
.label-tag{display:inline-block;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--green);background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.28);padding:4px 12px;border-radius:100px;margin-bottom:14px}
h1{font-size:clamp(1.8rem,3.6vw,2.5rem);font-weight:800;letter-spacing:-.025em;line-height:1.18;margin-bottom:14px}
.hero-lead{font-size:1.05rem;color:var(--muted);max-width:760px;line-height:1.75}
.art-meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:16px}
.meta-tag{font-size:.72rem;color:var(--muted);background:var(--bg2);border:1px solid var(--border2);padding:4px 11px;border-radius:100px}
/* LAYOUT: sticky left rail */
.ft-layout{display:grid;grid-template-columns:236px minmax(0,1fr);gap:40px;padding:32px 0 72px;align-items:start}
.ft-rail{position:sticky;top:76px;max-height:calc(100vh - 96px);overflow-y:auto;padding-right:6px}
.rail-group{margin-bottom:22px}
.rail-title{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--faint);margin-bottom:9px}
.lane-btn{display:flex;align-items:center;gap:9px;width:100%;background:none;border:1px solid var(--border2);color:var(--muted);font-family:inherit;font-size:.84rem;font-weight:600;text-align:left;padding:9px 12px;border-radius:9px;cursor:pointer;margin-bottom:7px;transition:all .15s}
.lane-btn:hover{border-color:var(--faint);color:var(--fg)}
.lane-btn.active{background:var(--card);color:var(--fg);border-color:currentColor}
.lane-btn.active.lb-green{border-color:var(--green);color:var(--green)}
.lane-btn.active.lb-indigo{border-color:var(--indigo);color:var(--indigo)}
.lane-btn.active.lb-amber{border-color:var(--amber);color:var(--amber)}
.lane-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-green{background:var(--green)}.dot-indigo{background:var(--indigo)}.dot-amber{background:var(--amber)}
.toc a{display:block;font-size:.79rem;color:var(--muted);padding:5px 0 5px 11px;border-left:2px solid var(--border2);line-height:1.5}
.toc a:hover{color:var(--fg);border-left-color:var(--teal);text-decoration:none}
.toc a.sub{padding-left:22px;font-size:.75rem;color:var(--faint)}
/* content */
.ft-body h2{font-size:1.45rem;font-weight:700;letter-spacing:-.02em;margin:36px 0 14px;scroll-margin-top:78px}
.ft-body h2:first-child{margin-top:0}
.ft-body h3{font-size:1.08rem;font-weight:600;margin:26px 0 10px;color:var(--fg);scroll-margin-top:78px}
.ft-body p{margin-bottom:15px;color:#CBD5E1}
.ft-body ul,.ft-body ol{margin:0 0 16px 22px;color:#CBD5E1}
.ft-body li{margin-bottom:8px}
.ft-body strong{color:var(--fg);font-weight:600}
.ft-body code{background:var(--bg2);border:1px solid var(--border2);border-radius:5px;padding:1px 6px;font-size:.87em;font-family:ui-monospace,Menlo,monospace;color:#A5B4FC}
.lane-section{display:block}.depth-band{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:48px 0 22px;padding-top:10px;border-top:1px solid var(--border2)}.lane-section:first-child .depth-band{margin-top:0;border-top:none;padding-top:0}.depth-badge{display:inline-flex;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;padding:5px 13px;border-radius:100px;border:1px solid currentColor}.db-green{color:var(--green);background:rgba(16,185,129,.09)}.db-indigo{color:var(--indigo);background:rgba(99,102,241,.09)}.db-amber{color:var(--amber);background:rgba(245,158,11,.09)}.depth-note{font-size:.8rem;color:var(--faint)}.toc a .tdot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:7px;vertical-align:middle}.toc-heading{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;margin:15px 0 5px;padding-left:11px}
@keyframes fi{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
/* code block + copy */
.cb{position:relative;margin:0 0 20px}
.cb-head{display:flex;align-items:center;justify-content:space-between;background:var(--bg2);border:1px solid var(--border2);border-bottom:none;border-radius:10px 10px 0 0;padding:8px 13px}
.cb-lang{font-size:.7rem;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:var(--faint)}
.cb-copy{background:var(--border);border:1px solid var(--border2);color:var(--muted);font-family:inherit;font-size:.72rem;font-weight:600;padding:4px 11px;border-radius:6px;cursor:pointer;transition:all .15s}
.cb-copy:hover{background:var(--border2);color:var(--fg)}
.cb-copy.done{background:rgba(16,185,129,.15);border-color:var(--green);color:var(--green)}
.cb pre{background:#0B1220;border:1px solid var(--border2);border-radius:0 0 10px 10px;padding:15px 16px;overflow-x:auto;margin:0}
.cb pre code{background:none;border:none;padding:0;color:#CBD5E1;font-size:.84rem;line-height:1.7}
/* callouts */
.note{border-left:3px solid var(--teal);background:var(--teal-dim);border-radius:0 9px 9px 0;padding:14px 17px;margin:0 0 20px}
.warn{border-left:3px solid var(--amber);background:rgba(245,158,11,.07);border-radius:0 9px 9px 0;padding:14px 17px;margin:0 0 20px}
.note p:last-child,.warn p:last-child{margin-bottom:0}
.note-lbl{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.07em;color:var(--teal);margin-bottom:5px;display:block}
.warn .note-lbl{color:var(--amber)}
/* tables */
.ft-body table{width:100%;border-collapse:collapse;margin:0 0 22px;font-size:.88rem}
.ft-body th{background:var(--bg2);text-align:left;padding:10px 13px;font-weight:600;color:var(--fg);border:1px solid var(--border2);font-size:.8rem}
.ft-body td{padding:10px 13px;border:1px solid var(--border2);color:#CBD5E1;vertical-align:top}
/* registry */
.reg{background:var(--card);border:1px solid var(--border2);border-radius:12px;padding:18px 20px;margin:0 0 22px}
.reg-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.reg-head h3{font-size:.95rem;font-weight:700;color:var(--fg)}
.reg-date{font-size:.7rem;color:var(--faint);background:var(--bg2);border:1px solid var(--border2);padding:3px 10px;border-radius:100px;white-space:nowrap}
.reg-row{display:grid;grid-template-columns:170px 1fr;gap:14px;padding:9px 0;border-bottom:1px solid var(--border2);font-size:.86rem}
.reg-row:last-child{border-bottom:none}
.reg-row .n{font-weight:600;color:var(--fg)}
.reg-row .d{color:var(--muted)}
.pill{display:inline-block;font-size:.66rem;font-weight:600;padding:2px 8px;border-radius:100px;margin-left:6px}
.p-direct{background:rgba(16,185,129,.15);color:var(--green)}
.p-indirect{background:rgba(99,102,241,.15);color:#A5B4FC}
.p-oss{background:rgba(245,158,11,.15);color:var(--amber)}
/* module cards */
.mod-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin:0 0 26px}
.mod-card{display:block;background:var(--card);border:1px solid var(--border2);border-radius:12px;padding:18px;transition:border-color .18s,transform .18s}
.mod-card:hover{border-color:var(--green);transform:translateY(-2px);text-decoration:none}
.mod-num{font-size:.68rem;font-weight:700;color:var(--green);letter-spacing:.08em;margin-bottom:7px}
.mod-card h3{font-size:1rem;font-weight:600;color:var(--fg);margin-bottom:6px}
.mod-card p{font-size:.84rem;color:var(--muted);line-height:1.6;margin:0}
.site-footer{border-top:1px solid var(--border);padding:26px 0;text-align:center;color:var(--faint);font-size:.82rem;margin-top:40px}
@media(max-width:900px){
 .ft-layout{grid-template-columns:1fr;gap:20px}
 .ft-rail{position:static;max-height:none;border-bottom:1px solid var(--border);padding-bottom:16px}
 .toc{display:none}
 .lane-btn{display:inline-flex;width:auto;margin-right:7px}
 .reg-row{grid-template-columns:1fr;gap:3px}
}

/* ---- Fintech AI section identity (Session 62) ---- */
.ft-tag{display:inline-flex;align-items:center;gap:6px;font-size:.63rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--teal);background:var(--teal-dim);border:1px solid rgba(20,184,166,.28);padding:4px 11px;border-radius:100px;margin-bottom:13px}
.ft-tag::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--teal)}
.mod-card{position:relative;transition:border-color .18s,transform .18s,background .18s}
.mod-card::before{content:"";position:absolute;left:0;top:16px;bottom:16px;width:2px;border-radius:0 2px 2px 0;background:var(--teal);opacity:0;transition:opacity .18s}
.mod-card:hover::before{opacity:1}
.mod-card:hover{border-color:rgba(20,184,166,.45);transform:translateY(-1px)}
.mod-num{color:var(--teal)}
.ft-stats{display:flex;flex-wrap:wrap;border:1px solid var(--border);border-radius:12px;overflow:hidden;margin:24px 0 8px}
.ft-stat{flex:1;min-width:124px;padding:15px 17px;border-right:1px solid var(--border)}
.ft-stat:last-child{border-right:0}
.ft-stat-n{font-size:1.3rem;font-weight:700;color:var(--teal);line-height:1;letter-spacing:-.02em}
.ft-stat-l{font-size:.68rem;color:var(--faint);margin-top:5px;text-transform:uppercase;letter-spacing:.07em}
.sheet-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(206px,1fr));gap:10px;margin:14px 0 4px}
.sheet-card{display:block;padding:13px 15px;background:var(--card);border:1px solid var(--border);border-left:2px solid var(--teal);border-radius:0 10px 10px 0;text-decoration:none;transition:border-color .18s,background .18s}
.sheet-card:hover{background:var(--bg2);border-color:rgba(20,184,166,.5);border-left-color:var(--teal)}
.sheet-n{font-size:.62rem;font-weight:700;letter-spacing:.08em;color:var(--teal);text-transform:uppercase}
.sheet-t{font-size:.85rem;font-weight:600;color:var(--fg);margin-top:3px;line-height:1.35}
h2{scroll-margin-top:70px}
.ft-body h2::after{content:"";display:block;width:26px;height:2px;background:var(--teal);border-radius:2px;margin-top:9px;opacity:.75}
@media(max-width:640px){.ft-stat{min-width:50%;border-bottom:1px solid var(--border)}.sheet-grid{grid-template-columns:1fr}}

.srcs{margin-top:10px;border-top:1px solid var(--border);padding-top:16px}
.srcs ol{list-style:none;counter-reset:s;padding:0;margin:0}
.srcs li{counter-increment:s;position:relative;padding:9px 0 9px 30px;border-bottom:1px solid var(--border);font-size:.82rem;line-height:1.6;color:var(--muted)}
.srcs li:last-child{border-bottom:0}
.srcs li::before{content:counter(s);position:absolute;left:0;top:10px;font-size:.68rem;font-weight:700;color:var(--faint);font-variant-numeric:tabular-nums}
.src-k{display:inline-block;font-size:.6rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;border-radius:100px;margin-right:7px;vertical-align:1px}
.src-official{background:rgba(20,184,166,.12);color:var(--teal);border:1px solid rgba(20,184,166,.3)}
.src-research{background:rgba(99,102,241,.12);color:var(--indigo);border:1px solid rgba(99,102,241,.3)}
.src-vendor{background:rgba(245,158,11,.12);color:var(--amber);border:1px solid rgba(245,158,11,.3)}
.src-industry{background:rgba(148,163,184,.1);color:var(--muted);border:1px solid var(--border2)}
.srcs strong{color:var(--fg);font-weight:600}
.srcs a{word-break:break-word}
</style>'''

SCRIPT='''<script>
(function(){
  var btns=document.querySelectorAll('.lane-btn'), secs=document.querySelectorAll('.lane-section');
  function show(l){
    btns.forEach(function(b){b.classList.toggle('active',b.dataset.lane===l);});
    secs.forEach(function(s){s.classList.toggle('active',s.dataset.lane===l);});
    document.querySelectorAll('.toc-group').forEach(function(g){g.style.display=g.dataset.lane===l?'block':'none';});
    try{history.replaceState(null,'','#'+l);}catch(e){}
  }
  window.showLane=show;
  btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.lane);});});
  var h=(location.hash||'').replace('#','');
  show(['green','indigo','amber'].indexOf(h)>-1?h:'green');

  document.querySelectorAll('.cb-copy').forEach(function(btn){
    btn.addEventListener('click',function(){
      var pre=btn.closest('.cb').querySelector('pre code');
      var txt=pre?pre.innerText:'';
      function ok(){btn.textContent='Copied';btn.classList.add('done');setTimeout(function(){btn.textContent='Copy';btn.classList.remove('done');},1800);}
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(ok).catch(function(){fb(txt,ok);});}
      else{fb(txt,ok);}
    });
  });
  function fb(t,cb){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity=0;document.body.appendChild(a);a.select();try{document.execCommand('copy');cb();}catch(e){}document.body.removeChild(a);}

  var links=document.querySelectorAll('.toc a[href^="#s-"]');
  var obs=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      links.forEach(function(a){a.style.color='';a.style.borderLeftColor='';});
      var a=document.querySelector('.toc a[href="#'+e.target.id+'"]');
      if(a){a.style.color='var(--fg)';a.style.borderLeftColor='var(--green)';}
    });
  },{rootMargin:'-78px 0px -70% 0px'});
  document.querySelectorAll('.ft-body h2[id],.ft-body h3[id]').forEach(function(h){obs.observe(h);});
})();
</script>'''

def NAV(active=''):
    L=[('/codex/','Codex'),('/ai-atlas/','AI Atlas'),('/fintech-ai/','Fintech AI'),('/ai-kids/','AI Kids'),('/courses/','Courses'),('/about/','About')]
    return ('<nav class="site-nav"><div class="nav-in"><a href="/" class="nav-logo"><div class="logo-mark">CL</div><span>Clarigital</span></a>'
      '<div class="nav-links">'+''.join(f'<a href="{u}"{" class=\"active\"" if u==active else ""}>{n}</a>' for u,n in L)+'</div></div></nav>')

def code(lang,body):
    esc=Hm.escape(body)
    return (f'<div class="cb"><div class="cb-head"><span class="cb-lang">{lang}</span>'
      f'<button class="cb-copy" type="button">Copy</button></div>'
      f'<pre><code>{esc}</code></pre></div>')

def prompt(body):
    return code('Prompt — paste into any AI',body)

def registry(title,rows,verified=None):
    verified = verified or VERIFIED
    out=''.join(f'<div class="reg-row"><div class="n">{n}<span class="pill p-{k}">{k}</span></div><div class="d">{d}</div></div>' for n,k,d in rows)
    return (f'<div class="reg"><div class="reg-head"><h3>{title}</h3>'
      f'<span class="reg-date">Verified {verified}</span></div>{out}</div>')

def note(t,lbl='Note'): return f'<div class="note"><span class="note-lbl">{lbl}</span><p>{t}</p></div>'
def warn(t,lbl='Watch out'): return f'<div class="warn"><span class="note-lbl">{lbl}</span><p>{t}</p></div>'

def page(path,title,meta,lead,label,crumbs,lanes,extra_head='',og='/og-fintech.png'):
    """lanes = {'green':[(heading, html), ...], 'indigo':[...], 'amber':[...]}"""
    assert len(meta)<=165, f"META {len(meta)}: {path}"
    p=f"{SITE}/{path}/index.html"
    if os.path.exists(p):
        h=open(p,errors='ignore').read()
        assert '<title>Redirecting' in h or os.path.getsize(p)<3000, f"⛔ REAL CONTENT at /{path}/"
    url=f"{BASE}/{path}/"
    LANES=[('green','Beginner','Start here. No prior knowledge assumed.','var(--green)'),
           ('indigo','Intermediate','Build it. Pipelines, tools and working code.','var(--indigo)'),
           ('amber','Advanced','Ship it. Failure modes, thresholds and evidence.','var(--amber)')]
    railbtns=''
    body=''; tl=''
    for k,n,note,col in LANES:
        secs=lanes.get(k,[])
        if not secs: continue
        band=(f'<div class="depth-band"><span class="depth-badge db-{k}">{n}</span>'
              f'<span class="depth-note">{note}</span></div>\n')
        inner=band
        tl+=f'<div class="toc-heading" style="color:{col}">{n}</div>'
        for i,(hd,html) in enumerate(secs):
            sid=f"s-{k}-{i}"
            inner+=f'<h2 id="{sid}">{hd}</h2>\n{html}\n'
            tl+=f'<a href="#{sid}"><span class="tdot" style="background:{col}"></span>{hd}</a>'
            for m in re.finditer(r'<h3 id="([^"]+)">([^<]+)</h3>',html):
                tl+=f'<a class="sub" href="#{m.group(1)}">{m.group(2)}</a>'
        body+=f'<div class="lane-section" data-lane="{k}">{inner}</div>'
    toc=f'<div class="rail-group"><div class="rail-title">On this page</div><div class="toc">{tl}</div></div>'
    cr=''.join(f'<a href="{u}">{l}</a><span class="sep">&rsaquo;</span>' for u,l in crumbs)
    ld=json.dumps({"@context":"https://schema.org","@type":"Article","headline":title,"description":meta,"url":url,
      "author":{"@type":"Organization","name":"Clarigital"},"publisher":{"@type":"Organization","name":"Clarigital","url":BASE},
      "dateModified":DATEMOD})
    items=[{"@type":"ListItem","position":i+1,"name":l,"item":BASE+u} for i,(u,l) in enumerate(crumbs)]
    items.append({"@type":"ListItem","position":len(crumbs)+1,"name":title,"item":url})
    bc=json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>document.documentElement.classList.add("js");</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title} | Clarigital</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{Hm.escape(title)}">
<meta property="og:description" content="{meta}"><meta property="og:url" content="{url}">
<meta property="og:site_name" content="Clarigital">
<meta property="og:image" content="{BASE}{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{Hm.escape(title)}">
<meta name="twitter:description" content="{meta}"><meta name="twitter:image" content="{BASE}{og}">
{ICON}
{GA4}
<script type="application/ld+json">{ld}</script>
<script type="application/ld+json">{bc}</script>
{extra_head}
{STYLE}
</head>
<body>
{NAV('/fintech-ai/')}
<div class="page-hero"><div class="wrap">
  <nav class="breadcrumb">{cr}<span>{title}</span></nav>
  <div class="label-tag">{label}</div>
  <div class="ft-tag">Fintech AI</div><h1>{title}</h1>
  <p class="hero-lead">{lead}</p>
  <div class="art-meta"><span class="meta-tag">Verified {VERIFIED}</span><span class="meta-tag">Free &middot; No signup</span><span class="meta-tag">Official sources only</span></div>
</div></div>
<div class="wrap"><div class="ft-layout">
  <aside class="ft-rail">
    {toc}
  </aside>
  <main class="ft-body">{body}</main>
</div></div>
<footer class="site-footer"><div class="wrap"><p>Part of <a href="/">Clarigital.com</a> &middot; Free &middot; Official sources &middot; No paywalls</p></div></footer>
{SCRIPT}
</body>
</html>'''
    os.makedirs(f"{SITE}/{path}",exist_ok=True)
    open(p,'w').write(html)
    FBUILT.append(path)
    print(f"  ✅ /{path}/")
