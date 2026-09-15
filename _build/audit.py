import re,os,glob,json
from collections import defaultdict
exec(open('/tmp/linkcheck.py').read())
exec(open('/tmp/structcheck.py').read())
exec(open('/tmp/rendercheck.py').read())
H=glob.glob('**/*.html',recursive=True)
def rd(f): return open(f,errors='ignore').read()
bl=scan(verbose=False); st=check(verbose=False); rc=render_check(verbose=False)
nv=nav_coverage(verbose=False)
ne=nesting_errors(verbose=False)
hr=home_route(verbose=False)
oi=og_image_exists(verbose=False)
ms=missing_sources(verbose=False)
bu=bad_absolute_urls(verbose=False)
cd=count_drift(verbose=False)
sm=social_meta_consistency(verbose=False)
sl=skip_link_check(verbose=False)
hd=handler_check(verbose=False); ihd=inline_hidden_check(verbose=False)
links=set()
for f in H:
    for l in re.findall(r'href="(/[^"#?]*)"',rd(f)): links.add(l.rstrip('/')+'/')
orph=[('/'+(os.path.dirname(f)+'/' if os.path.dirname(f) else '')) for f in glob.glob('**/index.html',recursive=True)]
orph=[u for u in orph if u!='/' and u not in links]
t=defaultdict(int); d=defaultdict(int); badld=0
for f in H:
    h=rd(f)
    m=re.search(r'<title>([^<]*)</title>',h)
    if m: t[m.group(1)]+=1
    m2=re.search(r'name="description" content="([^"]*)"',h)
    if m2: d[m2.group(1)]+=1
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.DOTALL):
        try: json.loads(b)
        except Exception: badld+=1
flat=[f for f in H if not f.endswith('index.html')]
ck=[("Broken internal links",len(bl)),("HTML structure errors",len(st)),("Render/JS problems",len(rc)),("Orphan pages",len(orph)),
 ("Inline handler errors",len(hd)),("Inline-hidden content",len(ihd)),("Nav section coverage",len(nv)),("Block nesting errors",len(ne)),("No route to home",len(hr)),("og:image file missing",len(oi)),("Pages missing sources",len(ms)),("Malformed absolute URLs",len(bu)),("Published count drift",len(cd)),("Social/canonical metadata",len(sm)),("Skip link broken",len(sl)),
 ("Empty directories",sum(1 for r,ds,fs in os.walk('.') if not ds and not fs and r!='.')),
 ("Duplicate flat/dir pages",len([f for f in flat if os.path.exists(f[:-5]+'/index.html')])),
 ("Duplicate titles",sum(v for v in t.values() if v>1)),
 ("Duplicate descriptions",sum(v for v in d.values() if v>1)),
 ("Invalid JSON-LD",badld),
 ("Broken search inputs",sum(1 for f in H if 'id="navSearch"' in rd(f) and 'data-search-input' not in rd(f))),
 ("Missing meta description",sum(1 for f in H if '<html' in rd(f) and 'name="description"' not in rd(f))),
 ("Meta >165 chars",sum(1 for f in H for m in [re.search(r'name="description" content="([^"]+)"',rd(f))] if m and len(m.group(1))>165)),
 ("Titles >65 chars",sum(1 for f in H for m in [re.search(r'<title>([^<]*)</title>',rd(f))] if m and len(m.group(1))>65)),
 ("Missing GA4",sum(1 for f in H if '<html' in rd(f) and 'G-7DFK94MRK7' not in rd(f))),
 ("Missing og:image",sum(1 for f in H if 'property="og:image"' not in rd(f)))]
print("="*48)
print(f"Total HTML pages       {len(H)}")
print(f"Sitemap URLs           {open('sitemap.xml').read().count('<loc>')}")
print(f"Search index entries   {len(json.load(open('search-index.json')))}")
print("-"*48)
for l,v in ck: print(f"{l:<28}{v:>4}  {'✅' if v==0 else '❌'}")
if bl: print("\nbroken:",sorted(bl)[:8])
if st: print("\nstructure:",list(st.items())[:5])
if orph: print("\norphans:",orph[:8])
if rc: print("\nrender:",list(rc.items())[:5])
if hd: print("\nhandlers:",list(hd.items())[:6])
if ihd: print("\ninline-hidden:",list(ihd.items())[:6])
print(f"\n[metric] content pages under 800 words: {len(thin_content(verbose=False))}")
print(f"[metric] old stamps NEXT TO a decaying figure: {len(decaying_stamps(verbose=False))}")
print(f"[metric] classes used with no CSS rule: {len(orphan_classes(verbose=False))}")
print(f"[metric] pages with skipped heading levels: {len(heading_order(verbose=False))}")
