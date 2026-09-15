# CLARIGITAL QA SOP

**Every check, what covers it, and — most importantly — what is NOT covered.**

Written Session 76. Keep it honest: a checklist that pretends everything is covered is worse than
no checklist, because it stops people looking.

## How to read this

| Tag | Meaning |
|---|---|
| **AUTO** | A hard check in `audit.py`. Must be zero before packaging. Non-negotiable. |
| **METRIC** | Reported by `audit.py` but not gated. A number to watch, not a blocker. |
| **SCRIPTED** | A script exists but is run deliberately, not on every build. |
| **MANUAL** | A human has to look. No script can do it. |
| **GAP** | Nobody is checking this. Written down so it stops being invisible. |

**The rule that generated most of this document:** every defect found in sessions 47–76 passed every
check that existed at the time. *A check only sees what its pattern matches.* When adding one, write
down what it does **not** cover — that sentence is where the next defect is hiding.

---

## A. STRUCTURE AND MARKUP

| # | Check | Status |
|---|---|---|
| A1 | Balanced `<div>` count per page | **AUTO** — `HTML structure errors` |
| A2 | Balanced `section · main · nav · article · aside · header · footer · table · form` | **AUTO** — added S56 after 22 pages carried a stray `</header>` |
| A3 | **Nesting order**, not just counts — stack walk | **AUTO** — `Block nesting errors`. Added S55: counts balance when two errors cancel |
| A4 | Exactly one `<h1>` per page | **AUTO** — part of check #25 |
| A5 | `<head>`, `</body>`, `</html>` present exactly once | **AUTO** |
| A6 | Block elements nested inside `<p>` | **GAP** — 49 pages have an omitted `</p>`, which is legal HTML5. Only a *stray* `</p>` is an error |
| A7 | Heading level order (no h2 → h4 skips) | **GAP** — **566 pages skip a level.** Accessibility issue, never audited |
| A8 | Valid HTML against a real parser (W3C / html5lib) | **GAP** — everything here is regex and stack walks, not a parser |

## B. LINKS AND NAVIGATION

| # | Check | Status |
|---|---|---|
| B1 | Root-relative internal links resolve | **AUTO** — `linkcheck` |
| B2 | **Absolute self-links** resolve | **AUTO** — added S56 after **269 broken** ones hid behind a pattern that only matched `/...` |
| B3 | Zero orphan pages (≥1 inbound link) | **AUTO** |
| B4 | Every page links all five sections, top nav **and** drawer | **AUTO** — `Nav section coverage`. Added S53 after only **29 of 631** linked Fintech |
| B5 | Every page can reach the site root | **AUTO** — `No route to home`. Deliberately weaker than B4 so sections with their own nav are held to a floor |
| B6 | Sitemap = search index = page count | **AUTO** |
| B7 | **Findability** beyond "not orphaned" | **MANUAL** — S61b: 12 pages shipped reachable only from one footer line. *Not orphaned is much weaker than findable* |
| B8 | Outbound links still alive | **GAP** — one external link in AI Kids; nothing checks whether any external target still exists |
| B9 | 404 page | **DONE** — `404.html` built from the site shell, noindex, excluded from the sitemap |

## C. CONTENT

| # | Check | Status |
|---|---|---|
| C1 | Pages under 800 words | **METRIC** — 217. ~70 are hubs where short is *correct* |
| C2 | House style: British spelling, no em-dash asides, no "it's worth noting" | **MANUAL** |
| C3 | "What to check" lists inside code blocks | **MANUAL** |
| C4 | No stubs; unbuilt cards are non-clickable | **MANUAL** |
| C5 | **Content leaking between pages** | **AUTO** — check #25. S76: three pages carried another article's og tags *and its `<h1>`* |
| C6 | Duplicate or near-duplicate body content | **GAP** |
| C7 | Reading level appropriate to the audience (AI Kids vs build sheets) | **MANUAL** |

## D. ACCURACY AND SOURCES

| # | Check | Status |
|---|---|---|
| D1 | Every build sheet / product guide has a sources block | **AUTO** — `Pages missing sources` |
| D2 | Sources typed Official / Research / Vendor / Industry | **MANUAL** — the typing is the point; an undifferentiated list launders reporting into authority |
| D3 | Verification date stamped | **MANUAL** |
| D4 | Old stamp sitting next to a decaying figure | **METRIC** — `decaying_stamps`, 151. Replaced a metric that over-counted by flagging honest old dates on unchanged content |
| D5 | Claims re-verified against primary sources | **MANUAL** — the single most important thing on this list and the least automatable |
| D6 | Draft vs final regulation clearly marked | **MANUAL** |

## E. SEO — TECHNICAL

| # | Check | Status |
|---|---|---|
| E1 | Unique `<title>` ≤65 chars | **AUTO** |
| E2 | Unique meta description ≤165 chars | **AUTO** |
| E3 | Canonical present | **AUTO** |
| E4 | **Canonical absolute** | **AUTO** — check #25. S76: **853 pages had a relative canonical** against a house rule requiring absolute |
| E5 | `og:url` == canonical | **AUTO** — check #25. S76: **119 pointed at pre-restructure paths that no longer exist** |
| E6 | og:title / og:description / og:image present | **AUTO** |
| E7 | **og:image file actually exists** | **AUTO** — check #21. Added S60: a track shipped pointing at a non-existent file |
| E8 | Valid JSON-LD, Article + BreadcrumbList | **AUTO** |
| E9 | **Breadcrumb content sane** | **MANUAL** — S66 found crumbs literally named `"Https:"` and `"Www.Yourdigitalcodex.Com"` |
| E10 | No foreign / malformed absolute URLs | **AUTO** — check #23 |
| E11 | Published counts match the filesystem | **AUTO** — check #24. Eight stale-count incidents before it existed |
| E12 | robots.txt, sitemap.xml, llms.txt present | **SCRIPTED** |
| E13 | hreflang | **GAP** — single-language today |
| E14 | Keyword cannibalisation between pages | **GAP** |
| E15 | Internal link depth from the homepage | **GAP** |

## F. ACCESSIBILITY — the weakest area

| # | Check | Status |
|---|---|---|
| F1 | `<html lang>` present | **SCRIPTED** — currently 0 failures |
| F2 | All `<img>` have `alt` | **SCRIPTED** — currently 0 failures |
| F3 | Heading order | **METRIC** — `heading_order`. 566 → 438 → **101**. Four template causes fixed (registry h4, footer labels, `.lb-head`, `.sidebar-card`, `.gc-body`). Remainder are scattered individual cases, not a pattern |
| F4 | Skip-to-content link **and a target** | **AUTO** — check #26. Was 842 pages with none; now **876/876**. A link pointing at nothing is worse than none |
| F5 | Colour contrast ratios | **GAP** — never measured |
| F6 | Keyboard navigation and focus order | **GAP** |
| F7 | ARIA on toggles, accordions, drawers | **GAP** — partial `aria-expanded` only |
| F8 | Screen reader pass | **GAP** — MANUAL, never done |
| F9 | Gesture-free interaction (no blink/smile gates) | **MANUAL** — a documented conduct issue in the Video KYC guide |

## G. PERFORMANCE

| # | Check | Status |
|---|---|---|
| G1 | No external CSS, fonts or JS libraries | **MANUAL** — house rule |
| G2 | Page weight | **SCRIPTED** — median 41 KB; **3 pages >150 KB**, largest 434 KB (`sources/`) |
| G3 | Every code block has a copy button | **MANUAL** |
| G4 | Real Core Web Vitals | **GAP** — needs a browser |
| G5 | Image weight / format | **GAP** — only five og PNGs exist |

## H. MOBILE AND RESPONSIVE

| # | Check | Status |
|---|---|---|
| H1 | Viewport meta on every page | **SCRIPTED** — 0 failures |
| H2 | No fixed CSS widths >380px | **SCRIPTED** — 0 failures |
| H3 | Tables have an overflow rule | **SCRIPTED** |
| H4 | Flex containers set `align-items` where children vary in height | **MANUAL** — S59b: 195 pages were one nested element away from the circle-chip bug |
| H5 | **Rendered on a real phone** | **GAP** — *the highest-yield check available and I cannot do it* |

## I. JAVASCRIPT AND INTERACTIVITY

| # | Check | Status |
|---|---|---|
| I1 | Every `<script>` parses | **AUTO** |
| I2 | **Every inline `on*=` attribute parses** | **AUTO** — check #5. Added S47b after **1,560 Python booleans** in `onclick` |
| I3 | Every handler called is defined | **AUTO** — same check. Found the dead Codex search |
| I4 | Content renders without JavaScript | **AUTO** — `Inline-hidden content` |
| I5 | No `display:none` inline on togglable content | **AUTO** — inline always beats a class |
| I6 | **Interactive components actually work** | **MANUAL / DOM-stub tested** — quiz, progress bar, parent panel all *parsed* while broken |
| I7 | Classes used in markup have a CSS rule | **METRIC** — `orphan_classes`, 42. Triage: dangerous ones are elements needing styling *to exist* |
| I8 | localStorage / cookie behaviour | **GAP** |

## J. FORMS AND INPUTS

| # | Check | Status |
|---|---|---|
| J1 | Search inputs wired to a handler | **AUTO** — `Broken search inputs` |
| J2 | Labels associated with inputs | **GAP** |
| J3 | Placeholder counts derived, not hardcoded | **AUTO** via E11 — the count went stale **four times** before the numbers were removed |
| J4 | Error and empty states | **MANUAL** |

## K. ANALYTICS, LEGAL AND TRUST

| # | Check | Status |
|---|---|---|
| K1 | GA4 on every page | **AUTO** |
| K2 | Consent mode / cookie banner correctness | **GAP** |
| K3 | Privacy policy, terms, cookie policy, disclaimer exist | **SCRIPTED** |
| K4 | Disclaimers on regulated-topic pages | **MANUAL** |
| K5 | No ads, no tracking beyond GA4 | **MANUAL** |
| K6 | AI Kids: parent framing, safety link, no unsafe outbound | **SCRIPTED** — QA #4: 130/130, 130/130, one external link on the adult page |

## L. BUILD SYSTEM

| # | Check | Status |
|---|---|---|
| L1 | Every builder loads in a clean room | **SCRIPTED** — every QA. S48: four were unrunnable |
| L2 | Templates bundled in `_build/`, not `/tmp` | **SCRIPTED** — 12 were missing |
| L3 | No hardcoded dates, paths or counts | **MANUAL + E11** — four separate incidents |
| L4 | **Fix the builder in the same session as the page** | **MANUAL** — Rule 4. Broken five times, most recently by me in S61 |
| L5 | `_build/` and `/tmp` in sync | **MANUAL** |
| L6 | Version bumped, infra rebuilt, zip named for the version | **MANUAL** |

## M. SECURITY

| # | Check | Status |
|---|---|---|
| M1 | External links carry `rel="noopener"` | **SCRIPTED** |
| M2 | CSP, HSTS, X-Frame-Options | **GAP** — hosting-layer, never audited |
| M3 | `.well-known/security.txt` | **DONE** |
| M4 | No secrets in client code | **MANUAL** |

---

## HOW THIS IS ENFORCED — two loops, not one

A document nobody runs is a document. There are two enforcement points:

### Loop 1 — EVERY page, at creation (`newpage_check.py`)

```bash
python3 /tmp/newpage_check.py path/to/index.html     # one or more pages
python3 /tmp/newpage_check.py --changed              # anything newer than manifest.json
```

**33 page-level checks** drawn from sections A, B, C, D, E, F, H, I and K. Exit code 1 on any
**BLOCK**, so it can gate a build script. Levels: **BLOCK** stops the build · **WARN** needs a
reason · **INFO** is a known site-wide gap you are not expected to solve on one page.

**Run this as the last line of every build script, before the audit.** It catches at creation what
the QA would otherwise catch five sessions later — and it caught a heading-level skip that the
registry template had been emitting onto every build sheet since Session 44.

### Loop 2 — EVERY fifth session, whole site

The QA session below. Loop 1 proves a page is correct; Loop 2 proves the *site* is, and is the only
place the MANUAL and rotating SCRIPTED items get done.

### Keeping this document alive

**When any session finds a defect, add a row here in the same session** — with its status tag and,
if a new check was written, **what that check does not cover**. Every AUTO row below started as a
defect nobody was looking for.

## THE QA SESSION — every fifth session

**Build nothing.** The point is to look at the site rather than the table.

1. `audit.py` — all checks zero. Record **every metric** and compare to the previous QA.
2. `linkcheck` · all `<script>` · **all inline handlers** · all JSON-LD.
3. Clean-room builder load, all five.
4. Section rotation — one per QA: Codex → AI Atlas → Courses → AI Kids → Fintech.
   Run the **SCRIPTED** checks in sections F, G, H, K against that section.
5. Walk one full journey end to end.
6. **Ask the owner for two or three phone screenshots of the rotating section.**
7. Fix what is found. Record it even when trivial.
8. **Add anything newly discovered to this document, including what the new check does not cover.**

## THE FIVE RULES THIS DOCUMENT EXISTS TO ENFORCE

1. **A check only sees what its pattern matches.** Write down what it misses.
2. **A checker is code, and untested code is wrong until read.** Seven false alarms in ten sessions —
   `<p` matching inside `<path>`, an unmeasured count assertion, a regex needing a newline that was
   not there, a variable extractor reading a theme override.
3. **When a check and a check disagree, neither is evidence until one is read.** Prefer the standing
   check over the one you just wrote.
4. **Land a new check as a METRIC, fix the backlog, then promote it to AUTO.** A check that ships red
   is a check people learn to ignore.
5. **Never run a broad regex sweep across pages that mean different things.** S67's sweep fixed 1,071
   occurrences and silently broke one. S76's sweep touched 850 pages when three were intended and had
   to be restored from the packaged zip.
