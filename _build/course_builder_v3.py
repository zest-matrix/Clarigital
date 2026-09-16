import os,re,json
import os as _os
# Session 62: this was hardcoded to a folder named after the project's first day.
# Renaming the folder per version broke every builder. The documented workflow is
# "cp _build/*.py /tmp/ && cd <site> && python3 /tmp/x.py", so cwd IS the site root.
SITE = _os.environ.get("CLARIGITAL_SITE") or _os.getcwd()
import os as _os
# Session 47b: these were read from /tmp only, so they did not exist in a fresh
# session and the builder was unrunnable. Now bundled in _build/ with a fallback.
_BD=_os.path.dirname(_os.path.abspath(__file__))
def _tpl(n):
    for c in (_os.path.join(_BD,n), '/tmp/'+n):
        if _os.path.exists(c): return open(c,encoding='utf-8').read()
    raise FileNotFoundError(n+' — expected in _build/ or /tmp')
CSTYLE=_tpl('c_style.txt')
CSCRIPT=_tpl('c_script.txt')
CNAV=_tpl('c_nav.txt')
GA4='<script async src="https://www.googletagmanager.com/gtag/js?id=G-7DFK94MRK7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-7DFK94MRK7\');</script>'
ICON='<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMiAzMiI+PHJlY3Qgd2lkdGg9IjMyIiBoZWlnaHQ9IjMyIiByeD0iNyIgZmlsbD0iIzI1NjNFQiIvPjx0ZXh0IHg9IjE2IiB5PSIyMiIgZm9udC1mYW1pbHk9InN5c3RlbS11aSIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9IjgwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2ZmZiIgbGV0dGVyLXNwYWNpbmc9Ii0uNSI+Q0w8L3RleHQ+PC9zdmc+">'
CBUILT=[]

def vurl(u):
    """HARD FAIL if a lesson URL does not resolve. This is the Session 19-22 bug guard."""
    b=u.rstrip('/')
    ok=(os.path.isfile(SITE+b+'/index.html') or os.path.isfile(SITE+b+'.html') or os.path.isfile(SITE+u))
    assert ok, f"⛔ LESSON URL DOES NOT EXIST: {u}"
    return u

def Q(q,a,b,c,d,correct): return (q,[a,b,c,d],correct)

def _lesson(pfx,n,t,desc,mins,url):
    vurl(url)
    lid=f"{pfx}-l{n}"
    return (f'<div class="lesson" id="{lid}"><button class="lesson-check" onclick="toggleLesson(\'{lid}\')" aria-label="Mark complete">'
      f'<svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M2 6l3 3 5-5" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
      f'<div class="lesson-body"><div class="lesson-num">Lesson {n}</div><div class="lesson-title">{t}</div>'
      f'<div class="lesson-desc">{desc}</div><div class="lesson-footer"><span class="lesson-time">~{mins} min</span>'
      f'<a href="{url}" class="lesson-link">Read the guide &rarr;</a></div></div></div>')

def _quiz(tid,qs):
    out=''
    for q,opts,cor in qs:
        btns=''.join(f'<button class="quiz-opt" onclick="checkAnswer(this,{str(j==cor).lower()})">{o}</button>' for j,o in enumerate(opts))
        out+=f'<div class="quiz-q"><p class="qtext">{q}</p><div class="quiz-opts">{btns}</div><div class="quiz-feedback"></div></div>'
    return (f'<div class="quiz-section"><button class="quiz-toggle" onclick="toggleQuiz(\'{tid}-quiz\')">'
      f'<h2>Test your understanding</h2><span class="qt-arrow">&#9660;</span></button>'
      f'<div class="quiz-body" id="{tid}-quiz">{out}</div></div>')

def build(slug,title,subtitle,outcomes,bl,il,al,bq,iq,aq):
    p=f"courses/{slug}"
    q=f"{SITE}/{p}/index.html"
    if os.path.exists(q):
        h=open(q,errors='ignore').read()
        assert '<title>Redirecting' in h or os.path.getsize(q)<3000, f"⛔ REAL COURSE at /{p}/"
    assert len(subtitle)<=250
    total=len(bl)+len(il)+len(al)
    out=''.join(f'<div class="outcome"><span class="outcome-check">&#10003;</span><span>{o}</span></div>' for o in outcomes)
    B=''.join(_lesson('b',i+1,*l) for i,l in enumerate(bl))
    I=''.join(_lesson('i',i+1,*l) for i,l in enumerate(il))
    A=''.join(_lesson('a',i+1,*l) for i,l in enumerate(al))
    meta=f"Free {title} course — Beginner to Advanced. {subtitle}"[:160]
    url=f"https://www.clarigital.com/courses/{slug}/"
    ld=json.dumps({"@context":"https://schema.org","@type":"Course","name":f"Learn {title}",
      "description":meta,"url":url,"provider":{"@type":"Organization","name":"Clarigital","url":"https://www.clarigital.com"},
      "isAccessibleForFree":True})
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<script>document.documentElement.classList.add("js");</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Learn {title} — Free Course | Clarigital</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="Learn {title} — Free Course">
<meta property="og:description" content="{meta}"><meta property="og:url" content="{url}">
<meta property="og:site_name" content="Clarigital">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Learn {title} — Free Course">
<meta name="twitter:description" content="{meta}">
<meta property="og:image" content="https://www.clarigital.com/og-courses.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:image" content="https://www.clarigital.com/og-courses.png">
{ICON}
{GA4}
<script type="application/ld+json">{ld}</script>
{CSTYLE}
</head>
<body>
{CNAV}
<div class="course-hero"><div class="wrap">
  <nav class="breadcrumb"><a href="/courses/">Courses</a><span class="sep">&rsaquo;</span><span>Learn {title}</span></nav>
  <h1>Learn {title}</h1>
  <p class="hero-sub">{subtitle}</p>
  <div class="hero-outcomes">{out}</div>
  <div class="hero-meta"><span class="hm-item"><span class="hm-dot"></span>Free forever</span><span class="hm-item"><span class="hm-dot"></span>No signup required</span><span class="hm-item"><span class="hm-dot"></span>Progress saved locally</span><span class="hm-item"><span class="hm-dot"></span>{total} lessons</span></div>
</div></div>
<div class="wrap">
  <div class="track-info"><p>Three tracks &mdash; pick your level. Progress is saved automatically in your browser.</p></div>
  <div class="track-tabs">
    <button class="track-tab active" id="tab-beginner" onclick="showTrack('beginner')"><span class="track-dot" style="background:var(--green)"></span>Beginner</button>
    <button class="track-tab" id="tab-intermediate" onclick="showTrack('intermediate')"><span class="track-dot" style="background:var(--indigo)"></span>Intermediate</button>
    <button class="track-tab" id="tab-advanced" onclick="showTrack('advanced')"><span class="track-dot" style="background:var(--amber)"></span>Advanced</button>
  </div>
  <div class="track-panel active" id="track-beginner">
    <div class="track-progress"><div class="tp-bar"><div class="tp-fill" id="prog-b" style="width:0%"></div></div><span class="tp-label" id="prog-b-label">0 of {len(bl)} complete</span></div>
    <div class="lessons-list">{B}</div>{_quiz('b',bq)}
  </div>
  <div class="track-panel" id="track-intermediate">
    <div class="track-progress"><div class="tp-bar"><div class="tp-fill" id="prog-i" style="width:0%"></div></div><span class="tp-label" id="prog-i-label">0 of {len(il)} complete</span></div>
    <div class="lessons-list">{I}</div>{_quiz('i',iq)}
  </div>
  <div class="track-panel" id="track-advanced">
    <div class="track-progress"><div class="tp-bar"><div class="tp-fill" id="prog-a" style="width:0%"></div></div><span class="tp-label" id="prog-a-label">0 of {len(al)} complete</span></div>
    <div class="lessons-list">{A}</div>{_quiz('a',aq)}
  </div>
</div>
<footer style="padding:32px 20px;text-align:center;color:var(--faint);font-size:.8rem;border-top:1px solid var(--border);margin-top:60px">
  <p>Part of <a href="/" style="color:var(--blue)">Clarigital.com</a> &middot; Free &middot; Official sources &middot; No ads</p>
</footer>
{CSCRIPT}
</body>
</html>'''
    os.makedirs(f"{SITE}/{p}",exist_ok=True)
    open(q,'w').write(html)
    CBUILT.append(slug)
    print(f"  ✅ {title} ({total} lessons, all URLs verified)")
