import glob,re,os
def check(verbose=True):
    bad={}
    for f in glob.glob('**/*.html',recursive=True):
        h=open(f,errors='ignore').read()
        errs=[]
        he=h.find('</head>')
        if he<0: errs.append('no </head>')
        else:
            head=h[:he]
            for tag in ['<a href','<div class','<section','<article','<h1','<h2','<h3','<p>','<button','<footer','<nav']:
                if tag in head: errs.append(f'{tag} inside <head>')
        if h.count('<head>')!=1: errs.append(f'{h.count("<head>")} <head>')
        if h.count('<body')!=1: errs.append(f'{h.count("<body")} <body>')
        if h.count('</html>')!=1: errs.append(f'{h.count("</html>")} </html>')
        if re.search(r'<a\s*\n\s*<a\s',h): errs.append('stray <a fragment')
        if h.count('<title>')!=1: errs.append(f'{h.count("<title>")} <title>')
        body=re.sub(r'<script.*?</script>','',h[h.find('<body'):],flags=re.DOTALL)
        if body.count('<div')!=body.count('</div>'):
            errs.append(f"divbal:{body.count('<div')}/{body.count('</div>')}")
        # Session 48: div was the ONLY tag ever balanced. 22 pages carried a stray
        # </header> with no opener and 3 codex pages never closed <main>/<section>.
        # Browsers ignore it; HTML parsers and LLM crawlers do not.
        for t in ('section','main','nav','article','aside','header','footer','table','form'):
            o=len(re.findall(r'<'+t+r'[\s>]',h)); c=h.count('</'+t+'>')
            if o!=c: errs.append(f"{t}bal:{o}/{c}")
        # unclosed anchors heuristic
        if abs(h.count('<a ')-h.count('</a>'))>2: errs.append(f"anchor mismatch {h.count('<a ')}/{h.count('</a>')}")
        if errs: bad[f]=errs
    if verbose:
        print(f"Pages with structural problems: {len(bad)}")
        for f,e in list(bad.items())[:25]: print(f"  {f}: {', '.join(e)}")
    return bad
