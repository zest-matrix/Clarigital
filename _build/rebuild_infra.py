import os,re,glob,json,datetime
BASE="https://www.clarigital.com"
# Session 47: '2026-05-22' was hardcoded into sitemap lastmod, the llms-full
# header and manifest.last_updated, so every rebuild after May shipped a stale
# date on all 850 pages. Derived from the clock now.
TODAY=datetime.date.today().isoformat()
allh=glob.glob('**/*.html',recursive=True)
# Session 77: a noindex page (404.html) must not be advertised in the sitemap.
allh = [f for f in allh
        if not re.search(r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex',
                         open(f, errors='ignore').read())]
# NOTE: match the META TAG, not the string. A guide ABOUT indexation
# contains the word noindex in its body text.
entries=[]
for f in allh:
    if f.endswith('index.html'):
        d=os.path.dirname(f); u=BASE+'/'+(d+'/' if d else '')
    else:
        if os.path.exists(f[:-5]+'/index.html'): continue
        u=BASE+'/'+f[:-5]+'/'
    entries.append((u,f))
entries=sorted(set(entries))
rows=[]
for u,f in entries:
    d=u.replace(BASE+'/','').strip('/').count('/')
    pri='1.0' if u==BASE+'/' else ('0.9' if d==0 else '0.8' if d==1 else '0.7')
    rows.append(f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{pri}</priority>\n  </url>')
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(rows)+'\n</urlset>\n')
valid={u.replace(BASE,'') for u,_ in entries}
idx=[e for e in json.load(open('search-index.json')) if e['u'] in valid]
have={e['u'] for e in idx}; new=0
for u,f in entries:
    p=u.replace(BASE,'')
    if p in have: continue
    h=open(f,errors='ignore').read()
    t=re.search(r'<title>([^<]*)</title>',h); d=re.search(r'name="description" content="([^"]*)"',h)
    if not t: continue
    title=re.sub(r'\s*[—|]\s*(Clarigital.*|Digital Codex.*)$','',t.group(1)).strip()
    parts=p.strip('/').split('/')
    cat=parts[1].replace('-',' ').title() if len(parts)>1 else (parts[0].title() or 'Home')
    idx.append({"t":title,"u":p,"d":(d.group(1) if d else '')[:160],"c":cat}); new+=1
json.dump(idx,open('search-index.json','w'),separators=(',',':'))
lines=["# Clarigital.com — Full Content Index for LLMs",f"# Generated: {TODAY}",f"# Total pages: {len(entries)}",""]
for u,f in entries:
    h=open(f,errors='ignore').read()
    t=re.search(r'<title>([^<]*)</title>',h); d=re.search(r'name="description" content="([^"]*)"',h)
    if t: lines.append(f"{t.group(1).strip()} | {u} | {(d.group(1) if d else '').strip()}")
open('llms-full.txt','w').write('\n'.join(lines)+'\n')
mf=json.load(open('manifest.json'))
mf.update({'total_pages':len(allh),'last_updated':TODAY})
# Session 67: codex_guides counted every index.html under codex/, which
# includes 31 section HUBS and 2 utility pages. That over-counted guides by
# 33 and the wrong number was published on the hub and in all-guides.
def _leaf_pages(prefix):
    import os as _o
    allp=glob.glob(prefix+'**/index.html',recursive=True)
    dirs={_o.path.dirname(x) for x in allp}
    leaves=[x for x in allp if not any(d!=_o.path.dirname(x) and d.startswith(_o.path.dirname(x)+'/') for d in dirs)]
    return [x for x in leaves if _o.path.dirname(x) not in {'codex/all-guides','codex/glossary'}]
for k,p in [('codex_guides','codex/'),('ai_atlas','ai-atlas/'),('ai_kids','ai-kids/'),('courses','courses/')]:
    mf['sections'][k]=len(_leaf_pages(p)) if k=='codex_guides' else len([1 for u,f in entries if f.startswith(p)])
json.dump(mf,open('manifest.json','w'),indent=2)
print(f"✅ sitemap {len(rows)} | search-index {len(idx)} (+{new}) | llms-full {len(lines)-4} | codex {mf['sections']['codex_guides']}")
