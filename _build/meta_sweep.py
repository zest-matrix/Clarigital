import os,re,glob,json,html as H
BASE="https://www.clarigital.com"
def og_for(p):
    if p.startswith('/ai-kids'): return '/og-ai-kids.png'
    if p.startswith('/ai-atlas'): return '/og-ai-atlas.png'
    if p.startswith('/courses'): return '/og-courses.png'
    if p.startswith('/codex'): return '/og-codex.png'
    return '/og-image.png'
CRUMB={'codex':'Codex','ai-atlas':'AI Atlas','ai-kids':'AI Kids','courses':'Courses','csp':'CSP','curriculum':'Curriculum'}
def pretty(s): return CRUMB.get(s, s.replace('-',' ').title())

stats={'og':0,'tw':0,'ld':0,'bc':0,'ogimg':0}
for f in sorted(glob.glob('**/*.html',recursive=True)):
    h=open(f,errors='ignore').read()
    if '<head' not in h: continue
    # canonical path
    m=re.search(r'rel="canonical" href="([^"]+)"',h)
    url=m.group(1) if m else BASE+'/'+(os.path.dirname(f)+'/' if f.endswith('index.html') else f[:-5]+'/')
    path=url.replace(BASE,'') or '/'
    t=re.search(r'<title>([^<]*)</title>',h); d=re.search(r'name="description" content="([^"]*)"',h)
    title=H.escape(re.sub(r'\s*[—|]\s*(Clarigital.*|Digital Codex.*)$','',t.group(1)).strip(),quote=True) if t else 'Clarigital'
    desc=d.group(1) if d else ''
    add=[]
    # --- Open Graph ---
    if 'property="og:title"' not in h:
        add.append(f'<meta property="og:type" content="article">')
        add.append(f'<meta property="og:title" content="{title}">')
        add.append(f'<meta property="og:description" content="{desc}">')
        add.append(f'<meta property="og:url" content="{url}">')
        add.append(f'<meta property="og:site_name" content="Clarigital">')
        stats['og']+=1
    elif 'property="og:site_name"' not in h:
        add.append('<meta property="og:site_name" content="Clarigital">')
    # --- og:image: replace data URIs / missing with real PNG ---
    img=BASE+og_for(path)
    if 'property="og:image"' not in h:
        add.append(f'<meta property="og:image" content="{img}">')
        add.append('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
        stats['ogimg']+=1
    else:
        cur=re.search(r'property="og:image" content="([^"]*)"',h)
        if cur and (cur.group(1).startswith('data:') or not cur.group(1).startswith('http')):
            h=h.replace(cur.group(0),f'property="og:image" content="{img}"')
            if 'og:image:width' not in h:
                add.append('<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">')
            stats['ogimg']+=1
    # --- Twitter ---
    if 'name="twitter:card"' not in h:
        add.append('<meta name="twitter:card" content="summary_large_image">')
        add.append(f'<meta name="twitter:title" content="{title}">')
        add.append(f'<meta name="twitter:description" content="{desc}">')
        add.append(f'<meta name="twitter:image" content="{img}">')
        stats['tw']+=1
    elif 'name="twitter:image"' not in h:
        add.append(f'<meta name="twitter:image" content="{img}">')
    # --- Article / WebPage JSON-LD ---
    if 'application/ld+json' not in h:
        typ='Course' if path.startswith('/courses/') and path.count('/')>2 else 'Article'
        obj={"@context":"https://schema.org","@type":typ,
             ("name" if typ=="Course" else "headline"):H.unescape(title),
             "description":H.unescape(desc),"url":url,
             ("provider" if typ=="Course" else "publisher"):{"@type":"Organization","name":"Clarigital","url":BASE}}
        if typ=="Course": obj["isAccessibleForFree"]=True
        else:
            obj["author"]={"@type":"Organization","name":"Clarigital"}
            obj["dateModified"]="2026-05-22"
        add.append('<script type="application/ld+json">'+json.dumps(obj)+'</script>')
        stats['ld']+=1
    # --- BreadcrumbList ---
    if 'BreadcrumbList' not in h and path!='/':
        parts=[p for p in path.strip('/').split('/') if p]
        items=[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"}]
        acc=''
        for i,p in enumerate(parts):
            acc+='/'+p
            nm=H.unescape(title) if i==len(parts)-1 else pretty(p)
            items.append({"@type":"ListItem","position":i+2,"name":nm,"item":BASE+acc+'/'})
        add.append('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items})+'</script>')
        stats['bc']+=1
    if add:
        h=h.replace('</head>','\n'+'\n'.join(add)+'\n</head>',1)
    open(f,'w').write(h)
print("Injected:",stats)
