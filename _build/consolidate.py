import re,glob

DEPTH={'green':('Beginner','var(--green)'),'indigo':('Intermediate','var(--indigo)'),
       'amber':('Advanced','var(--amber)')}
NOTE={'green':'Start here. No prior knowledge assumed.',
      'indigo':'Build it. Pipelines, tools and working code.',
      'amber':'Ship it. Failure modes, thresholds and evidence.'}

BAND_CSS=("\n.lane-section{display:block}"
".depth-band{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:48px 0 22px;padding-top:10px;border-top:1px solid var(--border2,#243044)}"
".lane-section:first-child .depth-band{margin-top:0;border-top:none;padding-top:0}"
".depth-badge{display:inline-flex;align-items:center;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;padding:5px 13px;border-radius:100px;border:1px solid currentColor}"
".db-green{color:var(--green,#10B981);background:rgba(16,185,129,.09)}"
".db-indigo{color:var(--indigo,#6366F1);background:rgba(99,102,241,.09)}"
".db-amber{color:var(--amber,#F59E0B);background:rgba(245,158,11,.09)}"
".depth-note{font-size:.8rem;color:var(--faint,#64748b)}"
".toc a .tdot{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:7px;vertical-align:middle}"
".toc-heading{font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;margin:15px 0 5px;padding-left:11px}\n")

def extract_balanced(html, start_idx):
    """Return (segment, end_idx) for the div opening at start_idx, matched by depth."""
    i=start_idx; depth=0
    for m in re.finditer(r'<div\b|</div>', html[start_idx:]):
        if m.group(0)=='</div>':
            depth-=1
            if depth==0:
                end=start_idx+m.end()
                return html[start_idx:end], end
        else:
            depth+=1
    raise ValueError("unbalanced")

def consolidate_fintech(path):
    h=open(path,errors='ignore').read()
    if 'depth-band' in h: return 'already'
    if '<div class="lane-section"' not in h: return 'skip'

    # --- 1. pull the three toc-groups out, balanced ---
    toc_parts=[]
    while True:
        m=re.search(r'<div class="toc-group" data-lane="(\w+)"[^>]*>',h)
        if not m: break
        k=m.group(1)
        seg,end=extract_balanced(h,m.start())
        links=re.search(r'<div class="toc">(.*)</div>\s*</div>\s*$',seg,re.DOTALL)
        toc_parts.append((k, links.group(1) if links else ''))
        h=h[:m.start()]+h[end:]

    # --- 2. remove the depth button group, balanced ---
    m=re.search(r'<div class="rail-group"><div class="rail-title">Depth</div>',h)
    if m:
        _,end=extract_balanced(h,m.start())
        h=h[:m.start()]+h[end:]

    # --- 3. build one continuous TOC ---
    if toc_parts:
        out='<div class="rail-group"><div class="rail-title">On this page</div><div class="toc">'
        for k,links in toc_parts:
            label,col=DEPTH.get(k,(k,'inherit'))
            out+=f'<div class="toc-heading" style="color:{col}">{label}</div>'
            out+=re.sub(r'(<a\b[^>]*>)',rf'\1<span class="tdot" style="background:{col}"></span>',links)
        out+='</div></div>'
        h=h.replace('<aside class="ft-rail">','<aside class="ft-rail">\n    '+out,1)

    # --- 4. depth band inside each lane section ---
    def addband(m):
        k=m.group(1); label,_=DEPTH[k]
        return (m.group(0)+f'<div class="depth-band"><span class="depth-badge db-{k}">{label}</span>'
                f'<span class="depth-note">{NOTE[k]}</span></div>\n')
    h=re.sub(r'<div class="lane-section" data-lane="(\w+)">',addband,h)

    # --- 5. CSS: always visible ---
    h=re.sub(r'(?:html\.js )?\.lane-section(?:\.active)?\{[^}]*\}','',h)
    h=h.replace('</style>',BAND_CSS+'</style>',1)

    # --- 6. JS: neutralise lane switching, keep copy + scroll-spy ---
    h=re.sub(r"var btns=document\.querySelectorAll\('\.lane-btn'\), secs=document\.querySelectorAll\('\.lane-section'\);",
             "var btns=[], secs=[];",h)
    h=re.sub(r"btns\.forEach\(function\(b\)\{b\.addEventListener\('click',function\(\)\{show\(b\.dataset\.lane\);\}\);\}\);","",h)
    h=re.sub(r"var h=\(location\.hash\|\|''\)\.replace\('#',''\);\s*show\(\['green','indigo','amber'\]\.indexOf\(h\)>-1\?h:'green'\);","",h)
    open(path,'w').write(h)
    return 'ok'

if __name__=='__main__':
    from collections import Counter
    c=Counter()
    for f in sorted(glob.glob('fintech-ai/**/index.html',recursive=True)):
        try: r=consolidate_fintech(f)
        except Exception as e: r=f'ERROR:{e}'; print("  ⚠",f,e)
        c[r]+=1
    print(dict(c))
