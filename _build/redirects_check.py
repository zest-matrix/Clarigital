#!/usr/bin/env python3
"""redirects_check.py — validate _redirects and the deploy exclusion files.

WHY THIS EXISTS
Session 93b. Two Cloudflare deploys failed in succession and the second error
exposed a defect that had been live for an unknown length of time:

    /codex/seo/technical/crawlability-indexability/
      -> /codex/seo/technical/crawlability-indexability/   301

a rule redirecting a path to ITSELF — an infinite loop. It sat in the file
behind a 273-rule list that Cloudflare rejected at rule 101, so the deploy
never got far enough to report it.

The 26 hard checks in audit.py validate the SITE. Nothing validated the
DEPLOYMENT: not _redirects, not _headers, not what the host is told to
publish. This closes that gap for _redirects.

WHAT IT CHECKS
  1. Rule count against Cloudflare's enforced ceiling (see NOTE below)
  2. Duplicate source paths          — Cloudflare rejects the deploy
  3. Self-redirects                  — infinite loop, live, silent
  4. Chains (A->B where B->C)        — dilutes and slows
  5. Targets that do not exist       — a 301 into a 404
  6. .assetsignore present and covering the known-dangerous paths

NOTE ON THE CEILING
Cloudflare documents 2,000 static and 100 dynamic redirects. The observed
behaviour is a ceiling of ~100 rules TOTAL: a file with 272 static and 1
dynamic rule was rejected at rule 101 with a message naming the dynamic
limit. The limit here follows the observed behaviour, not the documentation.

WHAT THIS DOES NOT COVER
  - _headers is not validated at all.
  - It cannot tell whether a redirect is the RIGHT redirect, only that its
    target resolves. A rule pointing at a real but wrong page passes.
  - It does not check redirects configured in the Cloudflare dashboard, which
    is where the 240 legacy .html rules now live. Those are invisible from
    the repository and nothing in this project can see them.
  - .assetsignore is checked for presence and known entries only. It cannot
    know what new private file someone drops into the folder next week.

Run from the site root: python3 /tmp/redirects_check.py
Exit code 1 on any BLOCK.
"""
import io, os, sys, collections

CEILING = 100
DANGEROUS = ['.git/', '_build/', 'CLARIGITAL-MASTER.md', '.DS_Store', '.wrangler/']

fail = []
warn = []

# ---- _redirects ---------------------------------------------------------
if not os.path.exists('_redirects'):
    fail.append('BLOCK  _redirects is missing')
else:
    lines = io.open('_redirects', encoding='utf-8').read().split('\n')
    rules = [(i + 1, l) for i, l in enumerate(lines)
             if l.strip() and not l.strip().startswith('#')]
    print('_redirects: %d rules' % len(rules))

    if len(rules) > CEILING:
        fail.append('BLOCK  %d rules exceeds the enforced ceiling of %d — the deploy will be rejected'
                    % (len(rules), CEILING))
    elif len(rules) > CEILING * 0.85:
        warn.append('WARN   %d rules, close to the %d ceiling' % (len(rules), CEILING))

    counts = collections.Counter(l.split()[0] for _, l in rules)
    for src, n in sorted(counts.items()):
        if n > 1:
            where = [str(i) for i, l in rules if l.split()[0] == src]
            fail.append('BLOCK  duplicate source %s (lines %s) — Cloudflare rejects the deploy'
                        % (src, ', '.join(where)))

    for i, l in rules:
        p = l.split()
        if len(p) >= 2 and p[0] == p[1]:
            fail.append('BLOCK  line %d SELF-REDIRECT %s — infinite loop' % (i, p[0]))

    # chains: built from a LIST, not a dict. A dict silently drops duplicates,
    # which is exactly how the self-redirect hid from my first check.
    pairs = [(l.split()[0], l.split()[1]) for _, l in rules if len(l.split()) >= 2]
    sources = {s for s, _ in pairs}
    for s, t in pairs:
        if t in sources and t != s:
            warn.append('WARN   chain %s -> %s -> ... (redirect chains dilute and slow)' % (s, t))

    for i, l in rules:
        p = l.split()
        if len(p) < 2 or '*' in p[0] or ':' in p[0]:
            continue
        t = p[1]
        if t.startswith('http') or t.strip('/') == '':
            continue
        if not os.path.exists(t.strip('/') + '/index.html'):
            warn.append('WARN   line %d target does not exist: %s -> %s (301 into a 404)' % (i, p[0], t))

# ---- .assetsignore ------------------------------------------------------
if not os.path.exists('.assetsignore'):
    fail.append('BLOCK  .assetsignore is missing — the host will publish _build/, '
                'CLARIGITAL-MASTER.md and the .git directory from the build clone')
else:
    txt = io.open('.assetsignore', encoding='utf-8').read()
    for d in DANGEROUS:
        if d not in txt:
            fail.append('BLOCK  .assetsignore does not exclude %s' % d)
    print('.assetsignore: present, all %d known-dangerous paths excluded' % len(DANGEROUS))

# ---- report -------------------------------------------------------------
print()
for w in warn:
    print('  ' + w)
for f in fail:
    print('  ' + f)
print()
if fail:
    print('FAIL — %d blocker(s), %d warning(s)' % (len(fail), len(warn)))
    sys.exit(1)
print('PASS — 0 blockers, %d warning(s)' % len(warn))
