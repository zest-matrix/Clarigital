import re,glob

RAIL_CSS = """
/* --- sticky left rail (migrated from top tabs) --- */
.crs-layout{display:grid;grid-template-columns:232px minmax(0,1fr);gap:38px;align-items:start;margin-top:32px}
.crs-rail{position:sticky;top:72px;max-height:calc(100vh - 92px);overflow-y:auto;padding-right:4px}
.crs-rail-title{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.09em;color:var(--faint,#94a3b8);margin-bottom:10px}
.track-tabs{display:flex;flex-direction:column;gap:7px;border-bottom:none;margin-top:0}
.track-tab{display:flex;align-items:center;gap:9px;width:100%;background:none;border:1px solid var(--border);border-bottom:1px solid var(--border);border-radius:9px;padding:10px 12px;font-size:.84rem;font-weight:600;color:var(--muted);cursor:pointer;font-family:var(--font);text-align:left;transition:all .16s;white-space:normal;line-height:1.35}
.track-tab:hover{border-color:var(--muted);color:var(--text,#f1f5f9)}
.track-tab.active{background:rgba(255,255,255,.04);color:var(--text,#f1f5f9);border-color:currentColor}
.crs-main{min-width:0}
.track-panel{display:block;padding:0 0 32px}
html.js .track-panel{display:none}
html.js .track-panel.active{display:block}
@media(max-width:900px){
 .crs-layout{grid-template-columns:1fr;gap:16px}
 .crs-rail{position:static;max-height:none;padding-bottom:6px}
 .track-tabs{flex-direction:row;flex-wrap:wrap}
 .track-tab{width:auto}
}
"""

def migrate(path):
    h=open(path,errors='ignore').read(); o=h
    if 'crs-layout' in h: return "already"

    # 0. malformed onclick attribute: onclick="showTrack('x')")>
    h=re.sub(r"(onclick=\"showTrack\('[a-z]+'\)\")\)>", r"\1>", h)

    # 1. strip the old track CSS rules, then append the rail CSS
    h=re.sub(r'\.track-tabs\{[^}]*\}','',h)
    h=re.sub(r'\.track-tab\{[^}]*\}','',h)
    h=re.sub(r'\.track-tab:hover[^{]*\{[^}]*\}','',h)
    h=re.sub(r'\.track-tab\.active\{[^}]*\}','',h)
    h=re.sub(r'\.track-panel\{[^}]*\}','',h)
    h=re.sub(r'(?:html\.js )?\.track-panel\.active\{[^}]*\}','',h)
    h=h.replace('</style>',RAIL_CSS+'</style>',1)

    # 2. wrap tabs + panels in the two-column layout
    start=h.find('<div class="track-tabs">')
    if start<0: return "no-tabs"
    endmark=h.rfind('</div>\n<footer')
    if endmark<0: endmark=h.rfind('</div>\n\n<footer')
    if endmark<0: return "no-footer-boundary"

    seg=h[start:endmark]
    if seg.count('<div')-seg.count('</div>')!=0:
        return f"unbalanced:{seg.count('<div')}/{seg.count('</div>')}"

    tabs_end=seg.find('</div>',seg.find('<div class="track-tabs">'))
    # find the real close of the tabs container (it has nested buttons/spans, no divs)
    tabs=seg[:tabs_end+6]
    panels=seg[tabs_end+6:]

    new=('<div class="crs-layout">\n'
         '  <aside class="crs-rail">\n'
         '    <div class="crs-rail-title">Your level</div>\n'
         f'{tabs}\n'
         '  </aside>\n'
         '  <main class="crs-main">\n'
         f'{panels}\n'
         '  </main>\n'
         '</div>\n')
    h=h[:start]+new+h[endmark:]

    # 3. progressive enhancement flag
    if 'classList.add("js")' not in h:
        h=h.replace('<head>','<head>\n<script>document.documentElement.classList.add("js");</script>',1)

    if h!=o:
        open(path,'w').write(h); return "ok"
    return "nochange"

if __name__=="__main__":
    from collections import Counter
    res=Counter()
    for f in sorted(glob.glob('courses/*/index.html')):
        r=migrate(f); res[r]+=1
        if r not in ("ok","already"): print(f"  ⚠ {f}: {r}")
    print(dict(res))
