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
| B7 | **Findability** beyond "not orphaned" | **MANUAL** — S61b: 12 pages shipped reachable only from one footer line. **S81: 7 of 8 product guides had no route in from the Fintech hub**, each linked only from its own module page. *Not orphaned is much weaker than findable*, and the orphan check is green at one inbound link |
| B10 | **Link TEXT matches the target page** | **METRIC** — added S89 after `codex/all-guides/` showed the **`linkedin-algorithm` title on three different guides** — residual Session 76 contamination, in a generated index nobody re-ran after the source pages were fixed. Precise form: *link text is exactly another page&rsquo;s `<h1>`, and not the target&rsquo;s* — **14 hits, 1 real**. The loose form (no shared word) returns **1,265 across 280 pages** and is useless: editorial labels legitimately differ from titles. *Does not cover:* a wrong link whose text matches nothing on the site |
| B8 | Outbound links still alive | **GAP** — one external link in AI Kids; nothing checks whether any external target still exists |
| B9 | 404 page | **DONE** — `404.html` built from the site shell, noindex, excluded from the sitemap |

## C. CONTENT

| # | Check | Status |
|---|---|---|
| C1 | Pages under 800 words | **METRIC** — 217, flat across seven QAs. Classified S87, **corrected S88** (`_build/rescope.py` → `_build/thin-pages.md`): **45 HUB · 49 SYLLABUS · 3 NEARLY · 120 WRITE · 0 CUT**. **94 pages are routing, where short is correct**; the real backlog is **123**. Chrome is ~35 words, so the threshold is not inflated by nav and footer. *Does not cover:* whether a HUB or SYLLABUS is **thin as well as short** |
| C2 | House style: British spelling, no em-dash asides, no "it's worth noting" | **MANUAL** |
| C3 | "What to check" lists inside code blocks | **MANUAL** |
| C4 | No stubs; unbuilt cards are non-clickable | **MANUAL** |
| C5 | **Content leaking between pages** | **AUTO** — check #25. S76: three pages carried another article's og tags *and its `<h1>`* |
| C10 | **Markdown syntax leaking into HTML** | **AUTO** (WARN) in `newpage_check` — added S96 after **9 instances across 5 pages** rendered as literal `**bold**` and `*italic*`. All mine, from writing emphasis in markdown habit while composing HTML in the expansion batches. Nothing had ever looked for it: it is valid HTML, balanced, and passes every structural check. *Does not cover:* underscores, backticks, or markdown link syntax. `*|MERGE|*` tags are excluded as legitimate |
| C9 | **A routing page that is thin as well as short** | **METRIC** — both halves now measured. **HUBs (S94): 19 of 45 under 200 content words** — `codex/analytics-cro` routes to 24 children on 130 words. **SYLLABUS pages (S99): 0 of 49 under 400, median 725** — they carry 15 lesson descriptions each and are substantial. So *short is correct* holds without caveat for syllabi and with a real caveat for hubs. *Does not cover:* whether a 725-word syllabus orients as well as it lists |
| C8 | **Telling a routing page from a content page** | **SCRIPTED** — `rescope.py`. S87 tested `kids>=1`, which only looks DOWN the tree; a course syllabus routes OUTWARD to `/codex/` and 49 of them were counted as a content backlog. S88 added a template-keyed `syllabus_links()`. **A link-count threshold was measured and rejected**: courses score 8–21 out-links but AI Atlas tool guides reach 14–15 from a related-tools sidebar, so arithmetic cannot separate them and structure can. *Does not cover:* any future routing page that uses neither a child directory nor the lessons-list template |
| C6 | Duplicate or near-duplicate body content | **METRIC — ALL FIVE SECTIONS MEASURED, ALL CLEAN.** Fintech max pairwise **6.4%**, Codex (333 leaf guides) **7.8%** — both entirely boilerplate — and **AI Atlas (158), Courses (69) and AI Kids (130) each returned zero pairs** sharing even four long sentences. **No substantive duplication anywhere on 883 pages.** *Does not cover:* paraphrase, reordered sentences, and shared runs under 8 words |
| C7 | Reading level appropriate to the audience (AI Kids vs build sheets) | **MANUAL** |

## D. ACCURACY AND SOURCES

| # | Check | Status |
|---|---|---|
| D1 | Every build sheet / product guide has a sources block | **AUTO** — `Pages missing sources` |
| D8 | **Codex guides have a sources block** | **GAP** — the site footer promises *"331 guides. Official sources only."* The 104 `guide-*` template pages had **no sources block at all** and the template could not emit one. S90 added `sources_block()` to `guide_builder.py` and typed sources to 7 pages. **97 still have none.** *Does not cover:* the 239 flagship pages, which carry a free-text "Sources & Further Reading" section that is not typed |
| D2 | Sources typed Official / Research / Vendor / Industry | **MANUAL** — the typing is the point; an undifferentiated list launders reporting into authority |
| D3 | Verification date stamped | **MANUAL** |
| D4 | Old stamp sitting next to a decaying figure | **METRIC** — `decaying_stamps`, 151. Replaced a metric that over-counted by flagging honest old dates on unchanged content |
| D5 | Claims re-verified against primary sources | **MANUAL** — the single most important thing on this list and the least automatable |
| D7 | **Source-link checks must exclude internal cross-references** | **MANUAL** — S84: a scan for non-https source links returned 9 hits, all of which were the deliberate Session 65 design (a module's sources block points at its build sheet's `#sources`). Correct by design, flagged by an over-broad check. *The rule: a link inside a sources block is not necessarily an external citation* |
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
| E16 | **Counts in section hub STAT STRIPS** | **SCRIPTED** — `gen_fintech_hub.py`, added S81 after the Fintech hub advertised **1 product guide against 8**, a number inserted by a one-off patch in S62 and never revisited through eight product-guide sessions. **E11 did not see it**: check #24 matches *"N guides"* prose on Codex hubs, not a `.ft-stat-n` digit in a strip. *Does not cover:* counts written into body prose on the same hubs, or stat strips in any other section |
| E17 | **Non-numeric claims about coverage going stale** | **SCRIPTED** — same script. The Fintech strip read `RBI · SEBI` while the section had begun covering IRDAI. **Every count rule on this list assumed staleness is numeric; it is not.** Now derived by naming the regulators appearing on ≥3 pages in the section. *Does not cover:* the threshold is arbitrary and it only inspects three named regulators — a fourth would have to be added by hand |
| E13 | hreflang | **GAP** — single-language today |
| E14 | Keyword cannibalisation between pages | **GAP** |
| E15 | Internal link depth from the homepage | **GAP** |

## F. ACCESSIBILITY — the weakest area

| # | Check | Status |
|---|---|---|
| F1 | `<html lang>` present | **SCRIPTED** — currently 0 failures |
| F2 | All `<img>` have `alt` | **SCRIPTED** — currently 0 failures |
| F3 | Heading order | **METRIC** — `heading_order`. 566 → 438 → 101 → **36 (S99)**. **S79 concluded the remaining 101 were "scattered individual cases, not a pattern". That was wrong.** **68 of the 101 were one line in `course_builder_v3.py`** emitting `<h3>Test your understanding</h3>` under an `<h1>` with no `<h2>` on the page — 68 of 69 course pages, identical. Fixed at the generator, the 68 pages and the `.quiz-toggle h3` CSS selector together. Remaining 36: ai-atlas 20, csp 6, codex 5, ai-kids 2, courses 1. *Does not cover:* whether those 36 are now genuinely scattered — the same claim was made at 101 and was wrong |
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
| H3 | Tables have an overflow rule | **SCRIPTED** — **S104: 1 failure found and fixed.** `ai-kids/index.html` carried a three-column comparison table inside a wrapper with `overflow:hidden` for its border radius — so on a narrow screen the table was **clipped rather than scrollable**, on the landing page of the section. Fixed with a `.compare-table-wrap{overflow-x:auto}` and a `min-width` guard so the columns stay readable. *Does not cover:* tables inside wrappers that clip by some other means, and it still cannot see the rendered result |
| H4 | Flex containers set `align-items` where children vary in height | **MANUAL** — S59b: 195 pages were one nested element away from the circle-chip bug |
| H5 | **Rendered on a real phone** | **GAP** — *the highest-yield check available and I cannot do it* |

## I. JAVASCRIPT AND INTERACTIVITY

| # | Check | Status |
|---|---|---|
| I1 | Every `<script>` parses | **AUTO** |
| I2 | **Every inline `on*=` attribute parses** | **AUTO** — check #5. Added S47b after **1,560 Python booleans** in `onclick` |
| I3 | Every handler called is defined | **AUTO** in `audit.py` — found the dead Codex search. **The `newpage_check` copy was WRONG until S94**: it matched only `function NAME(` and raised a **BLOCK** on **139 correct AI Atlas pages** that define handlers by assignment (`window.copyPrompt=function`). `audit.py` recognised both forms and stayed green, so the two checks disagreed for sessions. *A BLOCK-level false positive in the gate that runs after every build is the worst kind.* Broadened and negative-tested |
| I4 | Content renders without JavaScript | **AUTO** — `Inline-hidden content` |
| I5 | No `display:none` inline on togglable content | **AUTO** — inline always beats a class |
| I6 | **Interactive components actually work** | **MANUAL / DOM-stub tested** — quiz, progress bar, parent panel all *parsed* while broken |
| I7 | Classes used in markup have a CSS rule | **METRIC** — `orphan_classes`, 42. Triage: dangerous ones are elements needing styling *to exist*. **S90: the entire `guide-*` template is undefined** — `.guide-article`, `.guide-hero`, `.guide-body`, `.guide-content`, `.guide-sidebar`, `.guide-intro` and `.sidebar-card` have **no rule in `codex_style.txt` or on the page**, across **104 Codex guides**. Only `.wrap` is defined. The markup is semantic so the text reads, but the hero band, the two-column layout and the sidebar cards do not exist. **NOT FIXED — writing layout CSS for 104 pages blind is the risk this document exists to prevent.** Needs eyes |
| I9 | **Stylesheet variants within a section** | **MEASURED, NOT A DEFECT (S103)** — AI Atlas carries **17 distinct inline stylesheets across 158 pages**, carried as an open item since S53 on the assumption it was drift. **Diffing the variants showed most of the variation is legitimate page-specific component CSS** — `.agent-card`, `.prompt-box`, `.callout-red` — used by the pages that carry it. **Merging them would delete rules the elements need to exist**, which is the I7 failure shape performed deliberately. Genuine drift found and fixed: **3 pages** whose `.nav-logo` rule had lost `letter-spacing`, against 155 matching both bundled templates. *Does not cover:* whether every page-specific rule is still used by its page; the classifier written to test that mis-handled descendant selectors and was discarded rather than trusted |
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
| L10 | **Verify a patch compiles BEFORE writing it** | **MANUAL** — S96: a patch inserted code at the wrong indentation, **wrote the file, and only then ran `py_compile`**, leaving `newpage_check.py` broken on disk. The compile check was in the right script and in the wrong order. Correct pattern: build the candidate string, `compile()` it, write only if it passes. *Sibling of L9* |
| L9 | **A patch script that fails without failing loudly** | **MANUAL** — S87: a heredoc with a quoting error raised `SyntaxError`, wrote nothing, and the stale script then ran and printed the same numbers — reading as *"the fix made no difference"* rather than *"the fix never applied"*. Error on stderr, plausible output on stdout. **Second quiet tooling failure in four sessions.** Rule: after patching a script, assert the patch landed before trusting the run |
| L8 | **A generator that rewrites files it did not change** | **SCRIPTED** — fixed S84. `gen_counts.py` used `re.subn`, whose return value counts **matches, not changes**, then wrote unconditionally. Every run rewrote four byte-identical files and printed *"1 count(s) derived"*, so the output read as a change on a site where nothing had changed. Two harms: **the log teaches you to ignore it**, and the bumped mtimes make `newpage_check --changed` select unrelated pages. Now writes only when `h2 != h`. *Does not cover:* the other generators were not audited for the same pattern |
| L7 | **Content inserted by a one-off patch with no generator behind it** | **GAP** — added S81. Rule 4 says fix the generator, and it is silent when *there is no generator*. The Fintech hub's stat strip and its build-sheet grid were spliced in by a Session 62 patch script that was never bundled, so nothing owned those numbers and nobody could re-run them. **Both hub defects this session live in that category.** Fixed here with `gen_fintech_hub.py`; nothing checks the rest of the site for the same shape |

## N. DEPLOYMENT — added S93b, the whole section was a blind spot

The 26 hard checks validate the **site**. Until S93b **nothing validated the deployment**: not the
redirect file, not the headers file, not what the host was told to publish. Two failed deploys made
the gap visible.

| # | Check | Status |
|---|---|---|
| N1 | **`_redirects` rule count against the enforced ceiling** | **SCRIPTED** — `redirects_check.py`. Cloudflare documents 2,000 static + 100 dynamic; the **observed** ceiling is ~100 **total** — 272 static + 1 dynamic was rejected at rule 101 under a message naming the dynamic limit. *Does not cover:* whether the documented limits change back |
| N2 | **Duplicate source paths** | **SCRIPTED** — rejects the deploy. Three were present and had been for an unknown period |
| N3 | **Self-redirects** | **SCRIPTED** — `/codex/seo/technical/crawlability-indexability/` redirected **to itself**. An infinite loop, live, and invisible to every check this project had. Found only because the rule-count error was fixed first and Cloudflare then got far enough to report it |
| N4 | Redirect chains | **SCRIPTED** — warning, not a blocker |
| N5 | **Redirect targets that exist** | **SCRIPTED** — a 301 into a 404 |
| N6 | **`.assetsignore` present and covering the dangerous paths** | **SCRIPTED** — without it the host publishes `_build/`, `CLARIGITAL-MASTER.md`, `.DS_Store` and the **`.git` directory created by the build clone**. *`.git` cannot be gitignored*, so this file is the only control |
| N7 | `_headers` correctness | **GAP** — never validated |
| N8 | **Redirects configured in the host dashboard** | **GAP** — the 240 legacy `.html` rules now live in a Cloudflare Redirect Rule. **Invisible from the repository.** Nothing in this project can see or verify them |
| N9 | What is actually live vs what is in the package | **GAP** — needs a fetch. `CLARIGITAL-MASTER.md` was publicly readable and nobody knew |

## M. SECURITY

| # | Check | Status |
|---|---|---|
| M1 | External links carry `rel="noopener"` | **SCRIPTED** — **narrowed S89.** The check flagged 5 codex links; **none uses `target="_blank"`**, and `window.opener` exposure only exists with a new browsing context, so all five were correct. *A check that fires on correct behaviour is worse than no check.* Now conditional on `target="_blank"`. *Does not cover:* links opened by JavaScript |
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
2. **A checker is code, and untested code is wrong until read.** Thirteen false alarms so far.
   **S94 added two.** A `newpage_check` handler pattern that BLOCKED 139 correct pages — and then,
   worse, **a negative test that was a no-op and reported PASS**: the mutation targeted
   `copyPrompt = ` while the file contained `copyPrompt=`, so nothing changed and the green result
   proved nothing. *A test that does not modify what it claims to modify always passes.* **S93b
   is the sharpest:** a loop-detector built a `{source: target}` dict, and because the file contained
   **duplicate sources the second entry silently overwrote the first** — hiding the self-redirect from
   the very check written to find it. *The duplicates concealed themselves from the duplicate check.*
   Rebuilt to count occurrences in a list. The earlier ten —
   `<p` matching inside `<path>`, an unmeasured count assertion, a regex needing a newline that was
   not there, a variable extractor reading a theme override, a skip-link search that read only the
   first 4,000 characters, a noindex filter that matched the word in a guide's body text, and — S81
   — a **verification diff that collapsed the whole page onto one line** and so reported no change on
   a page that had changed in twenty places. *A checker that reports "nothing happened" is the
   easiest kind to believe and the hardest kind to notice.*
3. **When a check and a check disagree, neither is evidence until one is read.** Prefer the standing
   check over the one you just wrote.
4. **Land a new check as a METRIC, fix the backlog, then promote it to AUTO.** A check that ships red
   is a check people learn to ignore.
5. **Never run a broad regex sweep across pages that mean different things.** S67's sweep fixed 1,071
   occurrences and silently broke one. S76's sweep touched 850 pages when three were intended and had
   to be restored from the packaged zip.
