#!/usr/bin/env python3
"""Session 55 — repair scrambled block nesting on 25 pages.

Session 51 tried string replacement and the verification guard correctly refused
to write. Counting cannot fix this because the errors cancel: an unclosed
<div class="chapter"> plus a spare </div> in the tail balances perfectly.

This walks the tag stream with a stack and repairs structurally:
  * close tag matches stack top          -> pop, keep
  * close tag is DEEPER in the stack     -> the elements above it were never
                                            closed. Emit their closing tags
                                            first, then this one
  * close tag is not in the stack at all -> stray. Drop it
  * anything still open at </body>       -> close it

Nothing is written unless the page reaches ZERO nesting errors, div balance
holds, and the visible text is byte-identical to before.
"""
import glob, re, io, sys, html as htmlmod

BLOCK = ('div', 'section', 'main', 'header', 'footer', 'article', 'nav', 'aside')
TAG = re.compile(r'<(/?)(' + '|'.join(BLOCK) + r')\b[^>]*?(/?)>', re.I)


def nesting_errors(body):
    stack, errs = [], []
    for m in TAG.finditer(body):
        if m.group(3):                      # self-closing, ignore
            continue
        if not m.group(1):
            stack.append(m.group(2).lower())
        elif not stack or stack[-1] != m.group(2).lower():
            errs.append(f"</{m.group(2)}> closes <{stack[-1] if stack else 'NOTHING'}>")
            if stack:
                stack.pop()
        else:
            stack.pop()
    return errs + [f"never_closed:<{t}>" for t in stack]


def visible_text(s):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return ' '.join(htmlmod.unescape(t).split())


def repair(body):
    """Return (new_body, actions)."""
    out, stack, actions, pos = [], [], [], 0
    for m in TAG.finditer(body):
        out.append(body[pos:m.start()])
        pos = m.end()
        tag = m.group(2).lower()

        if m.group(3):                                  # self-closing
            out.append(m.group(0)); continue

        if not m.group(1):                              # opening
            stack.append(tag); out.append(m.group(0)); continue

        # closing
        if stack and stack[-1] == tag:
            stack.pop(); out.append(m.group(0)); continue

        if tag in stack:
            # elements above it were never closed — close them, innermost first
            while stack and stack[-1] != tag:
                unclosed = stack.pop()
                out.append(f'</{unclosed}>')
                actions.append(f'inserted </{unclosed}>')
            if stack:
                stack.pop()
            out.append(m.group(0))
        else:
            actions.append(f'dropped stray </{tag}>')    # nothing to close

    out.append(body[pos:])
    # anything still open at the end
    while stack:
        unclosed = stack.pop()
        out.append(f'</{unclosed}>')
        actions.append(f'appended </{unclosed}> at end')
    return ''.join(out), actions


def process(path, write=False):
    h = io.open(path, encoding='utf-8', errors='ignore').read()
    bstart = h.find('<body')
    head, body = h[:bstart], h[bstart:]
    # keep scripts out of the walk, then splice them back
    scripts = []
    def stash(m):
        scripts.append(m.group(0))
        return f'@@S{len(scripts)-1}@@'
    body_ns = re.sub(r'<script.*?</script>', stash, body, flags=re.S)

    before = nesting_errors(body_ns)
    if not before:
        return None

    fixed_ns, actions = repair(body_ns)
    after = nesting_errors(fixed_ns)

    fixed = re.sub(r'@@S(\d+)@@', lambda m: scripts[int(m.group(1))], fixed_ns)
    new = head + fixed

    checks = {
        'nesting_clean': not after,
        'div_balanced':  fixed_ns.count('<div') == fixed_ns.count('</div>'),
        'text_intact':   visible_text(body) == visible_text(fixed),
        'html_once':     new.count('</html>') == 1,
    }
    ok = all(checks.values())
    if ok and write:
        io.open(path, 'w', encoding='utf-8').write(new)
    return {'path': path, 'before': len(before), 'after': len(after),
            'actions': actions, 'checks': checks, 'ok': ok, 'written': ok and write}


if __name__ == '__main__':
    write = '--write' in sys.argv
    results = []
    for f in sorted(glob.glob('**/*.html', recursive=True)):
        r = process(f, write=write)
        if r:
            results.append(r)
    good = [r for r in results if r['ok']]
    bad = [r for r in results if not r['ok']]
    print(f"pages with nesting errors : {len(results)}")
    print(f"  repairable              : {len(good)}")
    print(f"  NOT repairable          : {len(bad)}")
    print(f"  written                 : {sum(1 for r in results if r['written'])}")
    for r in results[:4]:
        print(f"\n  {r['path']}")
        print(f"    {r['before']} errors -> {r['after']}")
        print(f"    actions: {r['actions'][:4]}")
        print(f"    checks : {r['checks']}")
    for r in bad[:5]:
        print(f"\n  FAILED {r['path']}: {r['checks']}")
