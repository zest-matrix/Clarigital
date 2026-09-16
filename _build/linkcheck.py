import re,os,glob
from collections import defaultdict
def resolves(l):
    """A link resolves only if a FILE will be served."""
    l=l.split('#')[0].split('?')[0]
    if not l.startswith('/'): return True
    b=l.rstrip('/')
    if os.path.isfile('.'+b+'/index.html'): return True
    if os.path.isfile('.'+b+'.html'): return True
    if os.path.isfile('.'+l): return True
    return False
def scan(verbose=True):
    b=defaultdict(set)
    for f in glob.glob('**/*.html',recursive=True):
        # Session 56: absolute self-links (https://www.clarigital.com/...) were NEVER
        # validated -- this pattern only ever matched hrefs starting '/'. 269 were
        # broken across 129 targets while this check reported zero for months.
        _h = re.sub(r'href="https://(?:www\.)?clarigital\.com(/[^"]*)"', r'href="\1"',
                    open(f, errors='ignore').read())
        for l in re.findall(r'href="(/[^"#]*)"', _h):
            if not resolves(l) and not l.startswith(('/styles','/images','/fonts')): b[l].add(f)
    if verbose:
        print(f"Broken link targets: {len(b)}")
        for k,v in sorted(b.items(),key=lambda x:-len(x[1])): print(f"  {k}  ({len(v)} pages)")
    return b
