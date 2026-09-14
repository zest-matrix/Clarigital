import re,glob,html as Hm
D={'green':('Simple','Start here','var(--green)'),
   'indigo':('Working','Build it','var(--indigo)'),
   'red':('Deep','Go deeper','var(--red)')}
CSS=("\n.art-layout{grid-template-columns:260px 1fr}"
".art-sidebar{order:-1;position:sticky;top:70px;align-self:start;max-height:calc(100vh - 90px);overflow-y:auto}"
".lane-section{display:block}"
".depth-band{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:44px 0 20px;padding-top:10px;border-top:1px solid var(--card-border,#243044)}"
".lane-section:first-of-type .depth-band{margin-top:0;border-top:none;padding-top:0}"
".depth-badge{display:inline-flex;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;padding:5px 12px;border-radius:100px;border:1px solid currentColor}"
".db-green{color:var(--green)}.db-indigo{color:var(--indigo)}.db-red{color:var(--red,#EF4444)}"
".depth-note{font-size:.78rem;color:var(--faint,#64748b)}"
".pg-toc a{display:block;font-size:.79rem;color:var(--muted);padding:5px 0 5px 11px;border-left:2px solid var(--card-border,#243044);line-height:1.45;text-decoration:none}"
".pg-toc a:hover{color:var(--fg);border-left-color:var(--indigo)}"
".pg-toc .th{font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;margin:13px 0 5px;padding-left:11px}"
".pg-toc .th:first-child{margin-top:0}"
"@media(max-width:900px){.art-layout{grid-template-columns:1fr}.art-sidebar{position:static;max-height:none;order:0}}\n")

def bal(html,start):
    d=0
    for m in re.finditer(r'<div\b|</div>',html[start:]):
        d += 1 if m.group(0)=='<div' else -1
        if d==0: return start+m.end()
    raise ValueError('unbalanced')

def go(path):
    h=open(path,errors='ignore').read()
    if 'depth-band' in h: return 'already'
    if '<div class="lane-section" id="lane-' not in h: return 'skip'
    b0=re.sub(r'<script.*?</script>','',h[h.find('<body'):],flags=re.DOTALL)
    if b0.count('<div')!=b0.count('</div>'): return 'unbalanced-input'

    # 1. remove the lane-tabs wrapper (balanced)
    m=re.search(r'<div style="background:var\(--card-bg\);border-bottom:1px solid rgba\(99,102,241,\.12\)">',h)
    if m: h=h[:m.start()]+h[bal(h,m.start()):]

    # 2. per lane: extract balanced, add ids + band
    toc=[]
    pos=0
    while True:
        m=re.search(r'<div class="lane-section" id="lane-(\w+)">',h[pos:])
        if not m: break
        s=pos+m.start(); k=m.group(1)
        e=bal(h,s)
        seg=h[s:e]
        inner=seg[m.end()-m.start():-6]      # strip the wrapper tags
        n=[0]
        def h2(x):
            sid=f"s-{k}-{n[0]}"; n[0]+=1
            toc.append((k,sid,re.sub(r'<[^>]+>','',x.group(1)).strip()))
            return f'<h2 id="{sid}">{x.group(1)}</h2>'
        inner=re.sub(r'<h2>(.*?)</h2>',h2,inner,flags=re.DOTALL)
        label,note,_=D.get(k,(k,'',''))
        band=(f'<div class="depth-band"><span class="depth-badge db-{k}">{label}</span>'
              f'<span class="depth-note">{note}</span></div>\n')
        new=f'<div class="lane-section" id="lane-{k}">{band}{inner}</div>'
        h=h[:s]+new+h[e:]
        pos=s+len(new)

    # 3. TOC card at top of sidebar
    if toc:
        out='<div class="sidebar-card"><h4>On this page</h4><div class="pg-toc">'
        last=None
        for k,sid,t in toc:
            if k!=last:
                label,_,col=D.get(k,(k,'','inherit'))
                out+=f'<div class="th" style="color:{col}">{label}</div>'; last=k
            out+=f'<a href="#{sid}">{Hm.escape(t)[:58]}</a>'
        out+='</div></div>'
        h=h.replace('<div class="art-sidebar">','<div class="art-sidebar">\n'+out,1)

    # 4. CSS + JS
    h=re.sub(r'\.lane-section\{display:none\}','',h)
    h=re.sub(r'\.lane-section\.active\{[^}]*\}','',h)
    h=h.replace('</style>',CSS+'</style>',1)
    h=re.sub(r"var tabs=document\.querySelectorAll\('\.lane-tab'\);","var tabs=[];",h)
    h=re.sub(r"var sections=document\.querySelectorAll\('\.lane-section'\);","var sections=[];",h)

    b1=re.sub(r'<script.*?</script>','',h[h.find('<body'):],flags=re.DOTALL)
    if b1.count('<div')!=b1.count('</div>'): return 'WOULD-BREAK'
    open(path,'w').write(h); return 'ok'

from collections import Counter
c=Counter()
for f in sorted(glob.glob('ai-atlas/**/index.html',recursive=True)):
    try: r=go(f)
    except Exception as e: r='ERR'; print("  ⚠",f,e)
    c[r]+=1
    if r in ('WOULD-BREAK','unbalanced-input'): print(f"  {r}: {f}")
print(dict(c))
