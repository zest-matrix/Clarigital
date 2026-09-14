# Clarigital.com — Master Project File
**Last updated: Monday 14 September 2026, 5:00 PM IST**
**Current deploy zip: `clarigital-v59.zip`**
**Live site:** https://www.clarigital.com
**Hosted on:** Cloudflare Pages (static, zero server-side functions)

---

## ⚠ FIRST THING IN ANY NEW SESSION

```bash
cd /home/claude/audit
unzip -q /mnt/user-data/uploads/clarigital-v59.zip
cd clarigital-v*/          # folder is named for the version
cp _build/*.py /tmp/          # scripts live in the zip, not in /tmp
python3 /tmp/audit.py         # confirm 23/23 at zero before changing anything
```

All build and verification scripts are bundled at `_build/` inside the zip. `_build/README.md`
lists what each one does. **They are not in /tmp in a fresh session — copy them first.**

---


## HOW TO START A NEW SESSION

1. The user will provide a zip file of the current live site
2. Unzip it: `unzip filename.zip -d site`
3. Read this entire file before writing any code
4. Work inside the unzipped folder — edit files directly
5. Rezip when done: `zip -r output.zip site-folder/ --exclude "*.DS_Store" --exclude "*.bak" --exclude "*.tmp" -q`
6. Update this MD file at the end of every session before delivering the zip
7. Always end with IST timestamp

---

## CURRENT SITE STATE (v10 — 22 May 2026, after Session 23)

| Metric | Value |
|---|---|
| Total HTML pages | **870** |
| Codex guides | **364** |
| AI Atlas pages | **158** |
| AI Kids pages | **117** |
| Courses | **69** (68 courses + hub) |
| CSP pages | **107** |
| Curriculum pages | **5** |
| Definition + policy + other | **10** |
| Sitemap URLs | **870** (1:1 with pages) |
| Search index entries | **870** |
| 301 redirect rules in `_redirects` | **272** |

**Note on the Codex count.** It reads 313, not 534. Session 23 deleted 240 duplicate flat `.html`
files that were exact twins of `/dir/index.html` pages and 301-redirected them. No unique content was
lost — the old 534 double-counted. Unique Codex guides actually rose by 33 in Session 23.

### Zero-check status (all must stay 0)

| Check | Status |
|---|---|
| Broken internal links | 0 ✅ |
| Duplicate flat/dir page pairs | 0 ✅ |
| Duplicate `<title>` tags | 0 ✅ |
| Duplicate meta descriptions | 0 ✅ |
| Broken search inputs (`id="navSearch"`) | 0 ✅ |
| Missing meta description | 0 ✅ |
| Meta description >165 chars | 0 ✅ |
| Missing GA4 tag | 0 ✅ |
| ElevenLabs nav/footer bleed | 0 ✅ |
| Stale "Search 313 guides" placeholder | 0 ✅ |
| Empty directories | 0 ✅ |
| Missing Open Graph | 0 ✅ |
| Missing Twitter card | 0 ✅ |
| Missing JSON-LD | 0 ✅ |
| Missing BreadcrumbList | 0 ✅ |
| Missing og:image | 0 ✅ |
| Inline handler errors | 0 ✅ |
| Inline-hidden content | 0 ✅ |
| Render/JS problems | 0 ✅ |
| HTML structure errors | 0 ✅ |
| Orphan pages | 0 ✅ |
| Invalid JSON-LD | 0 ✅ |
| Titles over 65 chars | 0 ✅ |
| Broken course lesson links | 0 of 1,020 ✅ |

---

### Session 66 — HOUSEKEEPING, AND A DEAD DOMAIN IN THE CANONICALS (DONE, 14 Sep 2026)

Two carried items. Investigating the first turned up something considerably worse.

#### ⚠ A DOMAIN THIS SITE NO LONGER USES, IN CANONICAL AND og:url

`codex/all-guides/` and two other pages carried:

```
https://www.clarigital.com/https:/www.yourdigitalcodex.com/all-guides/
```

A **concatenation bug** — an absolute URL pasted into a path slot — pointing at a domain the
site no longer uses. It appeared in **`rel=canonical`, `og:url` and the breadcrumb JSON-LD**, and the
breadcrumb had been generated *from the broken URL*, producing list items literally named
**`"Https:"`** and **`"Www.Yourdigitalcodex.Com"`**.

**Every check was green.** `linkcheck` validates *paths*; it had no opinion on whether an absolute
URL was coherent. A wrong canonical is one of the more damaging SEO defects available and it sat
there invisibly.

All three pages fixed; the breadcrumb rebuilt as Home → The Codex → All 364 Guides.

**My first fix broke two links** — stripping the old domain left `/seo/how-google-search-works/`
and `/all-guides/` without their `/codex/` prefix. `linkcheck` caught it in the same cycle. Repaired
with an existence assertion on every target before writing.

**CHECK #23 — &ldquo;Malformed absolute URLs&rdquo;.** Flags any absolute URL that is
self-concatenated or points at a foreign domain we used to own.

#### The fifth stale count: "All 218 Digital Marketing Guides"

The **all-guides page** — the one whose entire job is listing everything — said **218** in its
title, meta description, og, twitter card and JSON-LD, against **364** actual guides. Now correct.

Sixth occurrence of a hardcoded count going stale (313 → 253 → 218 → 220 → the search
placeholder → this). **Counts that describe the site must be derived at build time or removed.**

#### The stale-stamp metric was measuring the wrong thing

108 &rarr; investigated rather than bulk-fixed, and the split matters:

| | Count | Verdict |
|---|---|---|
| Pages stamped Apr 2026 with **no figure that can decay** | **138** | **Correct as-is.** A conceptual guide whose `dateModified` says April is honest. **Bumping it would be lying** to readers and to search engines about freshness |
| Pages stamped Apr 2026 that **quote prices or dated rules** | **~101** | A real re-verification backlog |

**`stale_stamps()` kept with a docstring warning that it over-counts; `decaying_stamps()` added and
wired into the audit in its place** — old stamp *next to* money, pricing or a dated rule.
Currently **151** across the site.

**The principle: a metric that tells you to do a dishonest thing is a broken metric.** Bumping 292
dates would have turned every one of those checks green and made the site less trustworthy.

#### Codex hub, resolved as deliberate

**129 of 364 guides are not linked from the hub** — they live under section sub-hubs, and the
orphan check is green because every one has an inbound link. The hub links `/codex/all-guides/`,
which is the correct route. That is a **curated hub, not a broken one**, and it is now recorded as
deliberate so it stops being re-raised.

*(Open: `all-guides` itself lists 236 of 364. Not fixed this session — it needs the listing
regenerated from the filesystem rather than hand-maintained, which is its own piece of work.)*

**Site: 23/23 at zero &middot; 870 pages &middot; linkcheck 0.**

---

### Session 65 — SOURCES PASS, PART 2: THE WHOLE SECTION (DONE, 14 Sep 2026)

Sources extended from the 10 build-sheet/product pages to **all 26 fintech pages** &mdash; the nine
modules, both regulatory spine pages, the four build-playbook pages, and the essay.

| | |
|---|---|
| Pages with a sources block | **26** |
| Total entries | **125** |
| Total links | **102**, all https |
| By type | **Official 90** &middot; Industry 20 &middot; Vendor 13 &middot; Research 2 |

**72% of entries are primary-sourced** &mdash; regulator, statute or standards body. That ratio is
itself worth tracking: if it falls, the section has drifted toward reporting.

#### The anti-duplication rule, applied to citations

Modules and build sheets cover the same subject, so their sources could have been copied wholesale.
Instead:

> **Modules cite the regulation. Build sheets cite the pricing.**

Each module's block ends with a line pointing at its build sheet's sources for tooling and cost
figures. Same discipline as the product-guide rule from Session 52: **one owner per fact.** A price
that appears in two source lists will eventually be checked in one and stale in the other.

#### Scope of check #22 widened

From *build sheets and product guides* to **every fintech page**, with exactly one exemption written
into the code:

```python
EXEMPT = {'fintech-ai/index.html'}   # the hub is navigation; its claims live on
                                     # the pages it links to
```

Per the Session 56 rule, the exemption is **in the check and commented**, not an undocumented gap.

#### Verification caught my own bad check

My first verification regex reported **&ldquo;0 entries, 0 links&rdquo;** while `audit.py` reported
the blocks present. Rather than trust the green audit, I rewrote the count &mdash; the regex had an
over-specific tail anchor and matched nothing. The content was fine; **the checker was wrong.**

Third time in three sessions a verification script has produced a confident wrong answer
(`<p` inside `<path>`, the `==5` count assertion, now this). **When a check and a check disagree,
neither is evidence until one is read.**

**Site: 22/22 at zero &middot; 870 pages &middot; linkcheck 0.**

---

### ★ Session 64 — QA #2: COURSES (DONE, 14 Sep 2026)

**Nothing built.** Second scheduled health check. Focus rotated to **Courses** because QA #1 changed
the progress-bar CSS and Session 47b changed the quiz CSS, and neither had ever been seen rendered.

#### Trend against QA #1

| | QA #1 (857 pages) | QA #2 (870 pages) |
|---|---|---|
| Hard checks | 20 / 20 zero | **22 / 22 zero** |
| Broken links | 0 | 0 |
| `<script>` blocks | 2,313 | **2,339** — 0 failures |
| Inline handlers | 10,677 | **10,689** — 0 failures |
| JSON-LD blocks | 1,813 | **1,839** — 0 failures |
| Clean-room builders | 5 / 5 | 5 / 5 |
| *thin pages* | 217 | 217 |
| *stale stamps* | 108 | 108 |
| *orphan classes* | 46 | 46 |

#### ⚠ THE FIND — the progress bar never moved, and my first fix was also wrong

QA #1 made the bar **visible** (it had no CSS at all). That is what exposed the next layer.

```js
var tracks = { beginner:[...], intermediate:[...], advanced:[...] };
Object.keys(tracks).forEach(function(track){
  var fill  = document.getElementById('prog-'+track+'-fill');   // prog-beginner-fill
  var label = document.getElementById('prog-'+track+'-label');  // prog-beginner-label
```

The markup ids are **`prog-b` / `prog-i` / `prog-a`** and **`prog-b-label`**. So `track` resolved to
`beginner`, both lookups returned `null`, and **neither the bar nor the label ever updated** on 65
course pages. Both guarded by `if(fill)`, so it failed in complete silence.

**My first fix was wrong.** I changed the selector to `'prog-'+track`, assuming `track` was `b`/`i`/
`a`. It is not — it is the long name. That fix resolved `prog-beginner`, which also does not
exist. **I caught it only because I went and read what `track` actually contained instead of
trusting my own diagnosis.**

**Correct fix:** a short-code map inside the loop, `{beginner:'b',intermediate:'i',advanced:'a'}`,
so both the fill and the label resolve. Applied to 65 pages; **3 gen-1 pages skipped because their
markup uses long-form ids and their original JS was already correct** — scoped by markup, not
by filename.

`_build/c_script.txt` patched (Rule 4). **Functionally tested against a DOM stub:** 2 of 5 lessons
now renders 40% with the label *&ldquo;2 of 5 lessons&rdquo;*; 1 of 5 renders 20%. **195 track
lookups across all course pages now resolve.**

#### The lesson this QA taught

**Fixing a rendering bug can expose a behavioural one.** The bar was invisible, so nobody could
observe that it also never moved. QA #1's CSS fix was necessary *and* it turned a silent defect into
a visible one — which is exactly what a QA cycle is for, and an argument for fixing visibility
bugs even when the thing behind them looks fine.

**And: verify the assumption, not just the symptom.** My wrong fix would have passed every automated
check on this site — valid JS, resolving syntax, no broken links. Only reading the actual value
of `track` found it.

#### Also checked, all clean

Courses: **68/68 quizzes** fully wired (CSS, JS, no inline hide, visible without JS) · all six
progress-bar classes defined on all 65 pages · **0** missing viewports · **0** fixed widths
above 380px · responsive rule present. Seven-hop journey across Home → Courses → AI Kids
→ Money Explorer → Fintech all resolve with nav present.

**Still cannot open a browser.** QA #2 found a real bug through structural reasoning, but the
standing request holds: **two or three pages on a phone, one section per QA.** Next rotation:
**AI Atlas**.

---

### Session 63 — THE SOURCES PASS, PART 1 (DONE, 14 Sep 2026)

*&ldquo;Even AI searches cite their sources, so why shouldn't we.&rdquo;* Applied to all **9 build
sheets + the product guide**. 47 source links, 63 entries.

#### The format, and why each decision was made

| Decision | Reason |
|---|---|
| **Foot of the page, not inline footnotes** | Inline markers wreck the reading flow of a page meant to be worked through with a terminal open |
| **Every entry is TYPED** | `Official` (teal) &middot; `Research` (indigo) &middot; `Vendor` (amber) &middot; `Industry` (grey) |
| **Each entry says WHAT IT SUPPORTS** | A bare link list is decoration. *&ldquo;This is where the &#8377;1.51 lakh fee cap comes from&rdquo;* is a source |
| **Only sources actually used** | Not a reading list. If it did not produce a number on the page, it is not there |
| **The check date is shown** | *&ldquo;Pricing and draft regulation move; the date is part of the claim&rdquo;* |

**The typing is the part that matters.** A regulator's PDF and a pricing-comparison blog are not
equivalent evidence, and presenting them in one undifferentiated list would be worse than citing
nothing &mdash; it launders industry reporting into apparent authority. A reader can now see at a
glance that the OFSI penalty figures are `Official` and the Indian voice-AI per-minute range is
`Industry`, and weight them accordingly.

**Where a claim could not be primary-sourced, the entry says so in the entry itself** rather than in
a general disclaimer &mdash; e.g. the UPI MDR range is marked *&ldquo;rates are not notified; treat
as direction, not figures&rdquo;*, and the enterprise AI-agent ranges note that none of those vendors
publishes a rate card.

**Older sheets carry an honest older date.** Build sheets 01&ndash;03 are stamped `May 2026`, not
backdated to today, because those figures were not re-verified this session.

#### CHECK #22 — "Pages missing sources"

Every build sheet and product guide must carry a sources block. Modules are **explicitly exempt for
now** &mdash; they are explanatory rather than figure-heavy &mdash; and the check's docstring says
so, per the Session 56 rule that a check must state what it does not cover. Scope widens in the
module pass.

`fintech_builder.py` now ships the `.srcs` CSS, so a regenerated page keeps the styling.

**Site: 22/22 at zero &middot; 870 pages &middot; linkcheck 0 &middot; 47 source links, all https, all typed.**

---

### Session 62 — FINTECH THEME, DONE PROPERLY (14 Sep 2026)

Making good on the Session 54 overstatement. **The real diagnosis:** the Fintech hub was built with
the **article template**, not a hub template. Structurally it was a module page — `lane-section`,
`depth-band`, `toc`, `note`, `warn`. AI Atlas's hub has `hc-*` hub cards, a `tool-grid`, `tc-*` tool
cards and a section tag. That is why one felt like a *place* and the other like a *document*.
Session 54 changed the paint. This changed the room.

#### What shipped, across all 27 fintech pages

| Element | What it does |
|---|---|
| **`.ft-tag`** | A teal section pill above every hero — a dot plus `FINTECH AI`. Present on all 27 |
| **`.mod-card`** | Teal left rail that fades in on hover, 1px lift, teal border. `.mod-num` now teal |
| **`h2::after`** | A 26px teal underline rule on every `.ft-body h2` — quiet, consistent, unmistakably the section's |
| **`.ft-stats`** | Hub stat strip: 9 modules · 9 build sheets · 1 product guide · RBI·SEBI · **0 ads** |
| **`.sheet-grid` / `.sheet-card`** | Nine build-sheet cards on the hub, teal left border, each one a route the hub previously did not offer |

**Rule 4 honoured this time:** the theme CSS *and* the `ft-tag` markup are both in
`fintech_builder.py`, so a regenerated page keeps the identity.

**Discoverability gain, not just decoration:** before this, the nine build sheets were reachable
**only from inside their own module page**. The hub listed modules and never mentioned that build
sheets existed. That is a genuine navigation fix wearing a visual-design hat.

#### ⚠ I BROKE RULE 5 AND CORRUPTED THE HUB

```python
j = h.find('The nine modules')        # asserted != -1  ✅
j = h.rfind('<h2', 0, j)              # NOT asserted    ❌  returned -1
h = h[:j] + BLOCK + h[j:]             # spliced before the LAST CHARACTER
```

The heading text's first occurrence is in the **table of contents**, which sits *before* any `<h2>`.
So `rfind` found nothing, returned `-1`, and `h[:-1] + BLOCK + h[-1:]` **truncated the document** —
the file ended `...</p>>` with `</html>` gone.

Rule 5 has been in this file since Session 30-something: *never use `str.find()` as an insertion
index without asserting `!= -1`*. I asserted the `find` and not the `rfind` on the very next line.

**Caught by `structcheck` (`0 </html>`) within one audit cycle.** Not shipped. But the checks caught
it, not me.

**Two refinements now recorded:**
1. **Every index gets a guard, including the second one on the same variable.** `rfind` is `find`.
2. **Match the ELEMENT, not the text.** `re.search(r'<h2[^>]*>\s*The nine modules\s*</h2>')` is
   unambiguous; `find('The nine modules')` hits the TOC, the meta description and the JSON-LD first.
   Same family as the `<p` matching inside `<path>` in Session 59b.

#### Still open for Fintech identity

A dedicated **section menu** (Atlas-style persistent module switcher) was not built. The TOC rail
covers within-page navigation but there is no cross-module switcher. Deferred deliberately rather
than half-done — flagged so it is not quietly forgotten a second time.

**Site: 21/21 at zero · 870 pages · linkcheck 0.**

---

### Session 61c — THE ZIP FOLDER WAS NAMED AFTER DAY ONE (14 Sep 2026)

User: *&ldquo;the main folder after the unzip shows `clarigital-14thApril` — it should show the
current version right?&rdquo;* Yes. **Every version since April unzipped to the same folder name.**

Two problems, one of them silent and dangerous:

1. The name was meaningless — it said nothing about which build you had.
2. **Unzipping v53 beside v52 collided.** Same folder name, so the second extraction either merged
   into or overwrote the first, and nothing announced it. Anyone keeping two versions to compare was
   quietly getting one.

**Folder is now named for the version: `clarigital-v54/`, matching the zip.**

#### The reason it had never been renamed — five hardcoded absolute paths

```python
SITE="/home/claude/audit/clarigital-14thApril"   # in 5 of the builders
```

Renaming the folder would have broken `atlas_builder`, `guide_builder`, `tool_builder`,
`course_builder_v3` and `fintech_builder` on the next run. **The folder name had become load-bearing
by accident.**

Now derived, not hardcoded:

```python
SITE = os.environ.get("CLARIGITAL_SITE") or os.getcwd()
```

The documented workflow is `cp _build/*.py /tmp/ && cd <site> && python3 /tmp/x.py`, so the working
directory *is* the site root. The env var is there for anyone running it differently.

`_build/README.md` and the MASTER start block no longer name the folder either — the instruction
is now `cd clarigital-v*/`.

**Verified after the rename:** 5/5 builders load in a clean room, 21/21 checks at zero, sitemap
regenerated, linkcheck 0, and **zero remaining references to the old name anywhere in the tree.**

#### The pattern, for the fourth time

Hardcoded environment assumptions that nobody notices until something moves: the **May 2026 dates**
(Session 47), the **/tmp-only templates** that made four builders unrunnable (Session 48), the
**`/wsp/` paths** left behind by a directory rename (Session 56), and now **the folder name itself**.

**When something is written down in more than one place, one of those places is going to be wrong
later.** Derive it, or the next person to move anything discovers it the hard way.

---

### Session 61b — THE KIDS TRACK WAS BUILT BUT NOT FINDABLE (14 Sep 2026)

User: *&ldquo;I can't see the fintech kids part anywhere — where do I find it?&rdquo;* They were right.
Twelve sessions shipped and effectively nobody could reach them.

| Route in | Before | After |
|---|---|---|
| Track card on the AI Kids homepage | **none** | ✅ `prog-card green`, matching Starter/Explorer/Builder |
| Body links on the kids homepage | **1**, in a footer text line | 1 card + nav |
| Links from **Fintech AI** | **0** | ✅ note on the hub |
| In the kids **nav** | 116 of 117 | **117 of 117** |

#### The placement bug

Session 60 inserted the nav link by matching `<a href="/ai-kids/parents/"...>` — but on the kids
homepage that string appears in a **footer paragraph as well as the nav**, and the footer matched
first. The result was `Safety Guide &middot; <a>Money</a><a>For Parents</a>` jammed into a sentence,
with no separator, and **nothing in the nav at all**.

**The lesson: when inserting into a named region, extract that region first and operate inside it.**
Matching a string that happens to appear in the region is not the same as matching the region. The
fix extracts `<nav class="kids-nav">...</nav>` and substitutes only within it.

**Building a thing and linking a thing are two tasks.** Every check was green because
`nav_coverage()` skips `kids-nav` by design and the orphan-page check only requires *one* inbound
link — which a single footer mention satisfied. **&ldquo;Not orphaned&rdquo; is a much weaker
property than &ldquo;findable&rdquo;.**

#### ⚠ CORRECTION — I overstated the Fintech theme in Session 54

I wrote that Fintech &ldquo;has its own identity now&rdquo;. **That was too strong.** What Session 54
actually did:

- declared `--teal:#14B8A6` and `--teal-dim`
- repointed body links, the hero wash, the TOC hover rail and `.note` callouts to it
- resolved a genuine collision where `--green` meant Fintech, Beginner lane **and** AI Kids at once

That is a **colour correction**, not a theme. The hub is still structurally the same page as before:
9,495 characters of CSS against AI Atlas's 12,319, **4 uses of `var(--teal)`** on the hub, and no
distinct hub layout, card geometry or section menu of the kind AI Atlas has.

**Outstanding for a real Fintech theme** — a genuine session's work, not a colour sweep:
hub hero treatment &middot; module card geometry &middot; a section menu &middot; build-sheet and
product-guide card styling &middot; consistent teal accenting throughout rather than four uses.

**Recorded as a correction rather than quietly re-scoped.** The claim was in the MASTER and someone
reading it would have believed the work was done.

**Site: 21/21 at zero · 870 pages · linkcheck 0.**

---

### Session 61 — MONEY EXPLORER EXTENDED TO 12 (DONE, 14 Sep 2026)

Track grown from 8 to **12 sessions**. Site 866 → **870**. The project session moved from 8 to 12 so
the finale stays the finale; **session 7 (scams) deliberately stays at 7** — early enough to revisit
several times before the track ends.

#### The four new sessions

| # | Title | The idea underneath |
|---|---|---|
| 8 | Where Does the Bank Keep It? | Fractional reserve, acted out. Take three deposits of 100, lend 200, then ask *&ldquo;what if we all want it today?&rdquo;* **The unease is the lesson — do not rush past it into reassurance** |
| 9 | Saving Up Is Hard | Ten empty boxes. Change one design element at a time and ask whether it helps. **Saving behaviour is a design choice somebody made, not willpower** |
| 10 | When the Computer Gets It Wrong | How would you notice · who do you tell · **what proof do you have**. Proof is what the session-1 ledger was for |
| 11 | Who Can See What You Bought? | Guess a person from their shopping list. **Transaction data is personal data**, and inference from ordinary records is the point |

Session 10 carries the line that matters most after session 7: *&ldquo;the computer says so&rdquo; is
never the end of the conversation — including when an adult says it.* A child who will push back
against a grown-up deferring to a machine has learned something durable.

Session 12 now requires **four** things in the child's own design, adding *a way to tell a person when
it gets something wrong* (session 10) to the ledger, identity check and reason-for-no.

#### ⚠ RULE 4 VIOLATION BY ME, CAUGHT IMMEDIATELY — fifth occurrence in this project

Session 60 found two defects in the new track (`og:image` pointing at a non-existent
`/og-kids.png`, and `.kids-out` used but undefined) and **fixed the generated pages**. The generator
was not touched. Rebuilding in this session **regenerated both defects on all 13 pages.**

Caught by the per-page verification before anything shipped, but it should not have happened —
Rule 4 has been in this file since Session 30-something and I broke it anyway.

**Both now fixed in `_build/kids_money.py` itself**: the og path, and a guard that injects
`.kids-out` into the extracted STYLE if the source page lacks it.

**The pattern to internalise: if a fix is applied to output that a script produces, the fix is
temporary by definition.** Rebuild after every generator patch and re-verify — a passing check on
files you hand-edited proves nothing about the next build.

A second self-inflicted error worth recording: my patch script asserted
`s.count('/og-kids.png')==5` when the real count was 2. The assertion failed, the patch never
applied, the rebuild silently used the old script, and the verification then reported 13 failures
that looked like new bugs. **A brittle assertion on an unverified count turns a no-op into a
confusing failure.** Count first, then assert — or do not assert on counts you have not measured.

**Site: 21/21 at zero · 870 pages · linkcheck 0.**

---

### Session 60 — AI KIDS: THE 'MONEY EXPLORER' TRACK (DONE, 14 Sep 2026)

`/ai-kids/money/` + 8 session pages. Site 857 → **866**. Ages 9–12, parent present, 25 min each.

#### Safety position, decided BEFORE any content was written

- **No real money anywhere.** No bank accounts, no card numbers, no UPI, no payment apps.
- Every example is pretend — paper, or typed into a chat.
- **Parent present is stated on every session**, not just the first.
- **Session 7 (scams) is placed before the project session** and the index says do not skip it.
- Session 3 explicitly says: photograph the *pretend* receipt, **never** a real bill or card.
- Session 6 states plainly that no real service lends money to children, so any offer of money,
  coins or credit online is a scam.

#### The eight sessions

| # | Title | The idea underneath |
|---|---|---|
| 1 | What Money Actually Is | Money is a **ledger**, not an object. Tear the paper in half to show why banks keep several copies and never rub out a line |
| 2 | How Does It Know It Is You? | Know / Have / Are. **A second category beats a longer password** |
| 3 | Teaching a Computer to Read | Child reads a receipt and scores confidence out of ten. **"I could not find it" ≠ a guess** |
| 4 | Spotting the Odd One Out | Anomaly detection, then **invent an innocent reason for each anomaly** — the cost of a false alarm |
| 5 | Is That Fair? | One rule, four different children. **Every fixed rule is unfair to someone** |
| 6 | Should a Computer Decide? | Refused with no reason vs a reason you can argue with. **Explainability as a right** |
| 7 | **Spotting a Scam** | **HURRY · SECRET · TOO GOOD · ASKING**, and one rule that covers all of them |
| 8 | Build Your Own Money Helper | Synthesis — and they write what it is **never allowed to do** |

**Session 7 is the highest-value page in the track.** The four signs generalise to scams the child
has not met yet, and the *secrecy* sign protects against considerably more than fraud. The parent
note says to revisit it repeatedly because awareness fades.

**Design choice worth keeping:** every session ends on a limit rather than a capability — what the
system should do when unsure, what it is not allowed to do, who has to explain. Same spine as the
nine build sheets, pitched at a child.

#### Three defects found while building, and one new check

1. **`og:image` pointed at `/og-kids.png`, which does not exist** — the real file is
   `og-ai-kids.png`. **The existing og:image check only verified the TAG was present, never that the
   file existed.** Social previews would have rendered blank with every check green.
   → **CHECK #21 `og_image_exists()`** added. Currently 0.
2. **`.kids-out` used but undefined** on the new pages — caught by the `orphan_classes` metric from
   QA #1, one session after it was written.
3. **An unclosed `<div class="wrap">`** on all 8 session pages, from a helper that opened a wrapper
   the caller had to close. Caught before writing by the per-page nesting walk.

#### Nav

`Money` added to the kids nav on **117/117** AI Kids pages, across **two different nav shapes** —
the second needed a different anchor. `nav_coverage()` deliberately skips `kids-nav`, so this was
manual and is worth remembering: **the kids section is outside the automated nav check by design.**

**Site: 21/21 at zero · 866 pages · linkcheck 0.**

---

### Session 59b — THE CHIP BUG WAS ONLY HALF FIXED (14 Sep 2026)

User re-sent the Session 47b screenshot and asked whether it was fixed everywhere, desktop and
mobile. **Correct instinct — it was not.**

#### What 47b actually did, and what it missed

47b fixed the **symptom**: the `btn-official` div was nested inside `.art-meta`, became the tallest
flex item, every `.meta-tag` stretched to match it, and `border-radius:100px` on a tall span turned
the chips into circles. Un-nesting it on 58 pages made the circles go away.

**It did not fix the cause.** `.art-meta` is `display:flex` with **default `align-items:stretch`**,
so *any* future element taller than a chip recreates the bug instantly.

**Audit of all 557 `.art-meta` instances across 422 pages:**

| CSS variant | Pages | Safe? |
|---|---|---|
| `align-items:center` present | 362 | ✅ |
| `display:flex;flex-wrap:wrap;gap:8px` | 168 | ❌ **vulnerable** |
| `display:flex;gap:8px;flex-wrap:wrap;margin-top:16px` | 27 | ❌ **vulnerable** |

**195 pages were one nested element away from the same bug.** All now carry `align-items:center`,
and `fintech_builder.py`, `atlas_style.txt` and `tool_style.txt` were patched so no builder can emit
the vulnerable form again (Rule 4).

**Result: 557/557 defensive, 0 pages nesting a block element inside `.art-meta`.**

#### A false positive in my own check, worth recording

My first nesting scan reported 6 Codex pages "containing `<p>`". They contain an SVG
`<path>` element — the substring `<p` matched inside `<path`. **Pattern matching on tag prefixes
without a word boundary produces confident wrong answers.** Same family of error as the
`undefined_handler` check flagging `document.getElementById` in Session 47b. Use `<(?:div|p|table)[\s>]`,
never `<p`.

#### Mobile, answered properly

Chips are `padding:3px 10px` with `border-radius:100px` and no height or aspect constraint, inside a
`flex-wrap:wrap` container with **no `@media` rule touching `.art-meta` anywhere on the site**. On a
narrow viewport they simply wrap onto more lines at their natural height. With `align-items:center`
now universal, a tall sibling on any future page can no longer stretch them on any width.

**The 47b note that mobile was "actually better, not worse" was right but incomplete** — it was
better by accident of wrapping, not by design. It is now correct by design.

---

### ★ Session 59 — QA #1: THE FIRST SCHEDULED HEALTH CHECK (DONE, 14 Sep 2026)

**Nothing was built.** First of the every-fifth-session QA cycle. 857 pages.

#### Baseline recorded — compare every future QA against this

| | QA #1 (14 Sep 2026) |
|---|---|
| Pages / sitemap / search index | **857 / 857 / 857** |
| Hard checks | **20 / 20 at zero** |
| Broken links (incl. absolute self-links) | **0** |
| `<script>` blocks parsed | **2,313** — 0 failures |
| Inline handlers parsed | **10,677** — 0 failures |
| JSON-LD blocks parsed | **1,813** — 0 failures |
| Builders loading in a clean room | **5 / 5** |
| Journey walk (home → fintech → module → sheet → product guide) | **5 / 5 hops, nav present on every page** |
| *[metric]* thin pages (<800 words) | **217** |
| *[metric]* stale stamps (>4 months) | **108** |
| *[metric]* classes with no CSS rule | **46** |

#### ⚠ THE FIND — the course progress bar rendered as NOTHING on 65 pages

`.track-progress`, `.tp-bar`, `.tp-fill`, `.tp-label` and `.lessons-list` were used in markup with
**zero CSS rules anywhere on the site**. The fill carried an inline `style="width:0%"` and the
JavaScript faithfully updated it — writing a width to an element with **no height, no background and
no track**. A progress indicator that showed nothing, on every course page, driven by working code.

Fixed on all 65, and `_build/c_style.txt` patched so the builder emits it (Rule 4). The fill is
lane-coloured: green / indigo / amber for beginner / intermediate / advanced.

**Same failure shape as the Session 47b quiz**: the generator emits class hooks, the stylesheet never
grew rules for them, and nothing compared the two. That is now a standing metric.

#### NEW METRIC — `orphan_classes()`: classes used in markup with no CSS rule

Started at **51 distinct**, now **46** after the fix. **Deliberately a metric, not a gate**, because
most hits are harmless: `.guide-hero`, `.guide-sidebar`, `.guide-content` etc. appear on 104 Codex
pages as **dead hooks from an old design** — `.art-layout{display:grid;grid-template-columns:1fr 268px}`
and a bare `aside{}` selector do the actual layout. `.clarigital-back` (258×), `.btn-official` (80×)
and `.toggle-arrow` (96×) all carry full inline styles.

**Triage rule, worth remembering:** the dangerous orphans are elements that need styling *to exist at
all* — bars, fills, tracks, overlays. A dead hook on a `<div>` that inline styles already handle is
cruft. **Do not bulk-fix this metric; read it.**

#### Also checked and healthy

- **Mobile:** viewport meta on **857/857** · **zero** fixed CSS widths above 380px · only 2 pages had
  a `<table>` with no overflow rule. The 3-column one is fine; the **5-column** page got a
  `@media(max-width:640px)` scroll guard.
- **Clean room:** all five builders load with `_build/*` alone and no `/tmp` templates.
- **Journey:** every hop resolves and every page carries a nav.

#### Honest limitation of this QA

**I cannot open a browser.** Steps 4 and 5 of the QA spec were executed as structural proxies — CSS
presence, viewport, fixed widths, overflow risk, class/rule reconciliation, link resolution. That
found a real rendering bug this time, but it is not equivalent to looking.

**The user's two screenshots in Session 47b remain the highest-yield defect-finding event in the
project.** The QA session should be paired with the user opening two or three pages on a phone and
sending back what looks wrong. Suggested rotation, one section per QA: Codex → AI Atlas → Courses →
AI Kids → Fintech.

---

### Session 58 — BUILD SHEET 09: Governance — **ALL NINE COMPLETE** (DONE, 14 Sep 2026)

`/fintech-ai/governance/build-sheet/` — 4,413 words, 2 code blocks, 1 registry. Site 856 → **857**.

**🏁 THE BUILD-SHEET SET IS DONE.** Nine modules, nine build sheets: Identity · Credit · Fraud ·
AML · Payments · Customer Ops · Wealth · Infrastructure · Governance.

#### THE SCOPE EXPLOSION — invalidates most existing inventories

RBI **draft Guidance on Regulatory Principles for Model Risk Management, 2026** (PR 2026-2027/528,
**24 June 2026**, signed Brij Raj, CGM, Dept of Regulation) broadens "model" to include AI/ML systems,
scoring algorithms, **rule engines**, and **material spreadsheets** that influence business decisions
like lending rates or customer pricing.

**A pricing spreadsheet is a model. The rules engine you built specifically to AVOID model risk is a
model.** Most Indian fintech inventories list ML models and nothing else — incomplete by design.
**The first governance task is not building controls, it is finding what you already have.**

- **11 RE categories**: commercial, small finance, payments, local area, regional rural, urban
  co-op and rural co-op banks · NBFCs all layers · AIFIs (EXIM, NABARD, NaBFID, NHB, SIDBI) · ARCs · CICs
- **Board-approved MRMF** over the full lifecycle · **Three Lines of Defence** · Board + RMCB retain
  ultimate accountability · **high-risk models need explicit RMCB approval**
- **Model inventory mandatory — UNLISTED ACTIVE MODELS ARE STRICTLY PROHIBITED**
- AI-specific controls against **hallucination, data drift, operational bias/discrimination,
  adversarial attack**
- **Anti-automation-bias**: HITL, human override, **immediate emergency kill switch**
- **Third-party: you CANNOT rely on a vendor's safety certificate.** Independent validation required.
  *Buying does not transfer risk — third-party models are HIGHER risk, not lower*
- **STATUS: DRAFT.** Comments closed 24 Jul 2026; finalisation expected H2 2026. Commenters proposed
  an 18/24/36-month tiered runway. Lineage: credit model draft 5 Aug 2024 → FREE-AI report
  13 Aug 2025 → this.

#### ⚠ EU AI ACT TIMING MOVED — and the shift is not yet law

**7 May 2026 provisional agreement (Digital Omnibus / Omnibus VII):**

| Obligation | Was | Now |
|---|---|---|
| Annex III standalone high-risk | 2 Aug 2026 | **2 Dec 2027** |
| Annex I product-embedded | 2 Aug 2027 | **2 Aug 2028** |
| **Article 50 transparency** | 2 Aug 2026 | **NOT deferred — applied** |

**The Omnibus is PENDING FORMAL RATIFICATION; the original date remains in force until adopted.**
Plan against Dec 2027, stay ready for the earlier one, and do not let a secondary source's headline
date into a project plan without checking ratification status. Unchanged: Art 5 prohibitions
2 Feb 2025, GPAI Art 51–56 from 2 Aug 2025. Fines **€35M/7%** prohibited · **€15M/3%** high-risk ·
**€7.5M/1.5%** incorrect information. Credit scoring for natural persons = Annex III high-risk.

#### ISO 42001 (Verified September 2026)

| | |
|---|---|
| Audit fees | Startup **$5k–$10k** · 51–200 staff, single BU **$25k–$75k** (Stage 1+2, accredited) |
| All-in year one | Startup **$15k–$40k** · mid-size **$20k–$60k** direct, plus **$45k–$100k** consulting and **$25k–$65k** internal labour greenfield |
| Timeline | Greenfield **9–14 months** · with ISO 27001 **5–9** · mature programme **3–6** |
| Leverage | **ISO 27001 in place cuts effort 40–50%** |

- **Timeline is dominated by internal audit and management review cycles, not the external audit.**
  Auditor scarcity is a real scheduling constraint.
- **Certification is NOT EU AI Act compliance.** Presumption of conformity flows from *harmonised
  European standards*; ISO 42001 harmonisation under Art 40 was underway but incomplete.
- **Confirm the certification body is accredited for ISO 42001 specifically** — early certificates
  were issued without accreditation.

#### Gotchas documented

1. **`fallback_rehearsed` is a DATE, not a boolean.** Every inventory has a fallback column
   describing what *would* happen. An unexercised fallback is a hypothesis. Schedule the rehearsal,
   write the date back, let the record go red when it ages out.
2. **The human override rate is the oversight metric nobody plots.** Under ~1% means a rubber stamp —
   *worse than no human in the loop, because it manufactures the appearance of control*. Over ~20%
   means the model is not fit for the decision.
3. **A kill switch that needs a deploy is not a kill switch.** "Immediate" means a runtime flag. And
   whoever most wants the model running must not be the only person who can stop it.
4. **Independence is structural, not personal.** A competent validator reporting into the model
   owner's business line is not independent. For small firms the honest answer is a **named external
   validator for high-risk models** plus documented self-assessment below — defensible in a way that
   an internal colleague is not.
5. **Choose the fairness metric in writing BEFORE testing.** Demographic parity, equalised odds and
   predictive parity are mutually incompatible on most real data; picking afterwards is choosing the
   answer. Record the disparity even when within tolerance — the trend is the signal.
6. **`validator != owner` asserted in code.** Most common finding, easiest to prevent.
7. **Governance is not a procurement problem.** The entire tooling column is open source. No product
   makes you governed, and commercial platforms mostly package these libraries with a dashboard.
8. **A small COMPLETE inventory beats a sophisticated one with gaps.** Examiners find gaps, and an
   incomplete list implies a control that is not there.

**The evidence-file test:** for any model on any day, produce what it does · who owns it · what data
· who validated and what they found · who approved · production history · failure behaviour · when
that was last tested. **If that takes more than an afternoon, you have documentation about a
programme rather than a programme.**

#### THE CLOSING OBSERVATION FOR THE WHOLE SECTION

Across every enforcement action, penalty notice and supervisory finding referenced in all nine build
sheets, **almost none turned on the model being insufficiently accurate**. They turned on an
escalation path that did not exist, a record not kept, a threshold nobody approved, or a control
never tested. The engineering is hard and worth doing well. **It is not what the examination is
about.**

---

### Session 57 — BUILD SHEET 08: Infrastructure (DONE, 14 Sep 2026)

`/fintech-ai/infrastructure/build-sheet/` — 4,725 words, 3 code blocks, 1 registry.
Linked from the module. Site 855 → **856**. **8 of 9 build sheets done.**

**Organising idea:** three planes that fail differently — ledger (you stop), operational (things
queue), **AI serving (you fall back to rules and carry on)**. That third row is the whole design
brief: every AI component needs a defined, *acceptable* behaviour when unavailable. Build the
fallback first and the model second.

#### Model API pricing, September 2026 (per 1M tokens)

| Tier | Input | Output |
|---|---|---|
| Budget / open-weight | **$0.03–$0.45** | 2–4× input |
| **Production — the war zone** | **$2** | **$10–$12** |
| Frontier | $4–$10 | **$20–$50** |

Several major models converged on **exactly $2 input** — the most contested price point in the
market. Volatility is the story: one provider cut a model **80% in a single day** (30 July 2026),
another **cancelled a scheduled increase** weeks before it was due (11 Aug 2026).

**BENCHMARK PARITY IS NOT PRICE PARITY.** Five models score within **0.4 percentage points** of each
other on a widely-cited coding benchmark while their output prices run **$1.20 to $12** — a tenfold
spread for a rounding error. The top scorer costs ~**42×** the cheapest in that band. The only
useful question is whether *your* tasks live in the gap: build a 100-example eval from your own
product and check.

**Blended rate is the costing error everyone makes.** Output is routinely 5–6× input, so the ranking
flips with your own ratio. Same two models: at 90/10 input-heavy, $2.80 vs $0.154. At 20/80
output-heavy, **$8.40 vs $0.252** — the mid-tier tripled, the budget tier barely moved.

#### India GPU economics (Verified September 2026)

| Item | Rate |
|---|---|
| H100, Indian providers | **₹219–362/hr** on demand · reserved **₹130–150** · spot **₹70–88** |
| H100, hyperscaler Mumbai | **₹600–740/hr** — Indian providers run **60–70% cheaper** |
| **Right card for inference** | **L40S ₹61–102/hr · L4 ₹49/hr · A30 ₹126/hr** |
| **IndiaAI Mission (subsidised)** | **₹67–92/GPU-hour** — 38,000+ GPUs empanelled, ₹10,300 crore programme |
| Buying outright | **₹27–34 lakh/H100** with duties; full server **₹2–5 crore** |

**DO NOT SERVE INFERENCE ON H100s.** It is a training card. L40S or L4 delivers production
throughput at a fraction of the cost; H100 only earns its place above ~70B parameters or at genuine
ultra-low-latency high-concurrency. **Most common and most expensive mis-sizing in this section.**

**The IndiaAI Mission is the largest untouched cost lever** — roughly a third of the cheapest
commercial Indian rate, a tenth of a hyperscaler's. "The cheapest legitimate GPU in India is not on
any commercial price list."

India mechanics: GPU cloud spend abroad sits under **LRS, no RBI approval below $250k/year**; IGST
via reverse charge is **claimable as input credit**, so the headline dollar figure overstates real
cost.

#### Gotchas documented

1. **Divide every GPU rate by REAL UTILISATION.** The card bills 24×7; traffic does not. A cluster
   busy 15% of the day costs **~6.7× its headline** per token. **This single correction reverses most
   self-host business cases** and is almost never in the spreadsheet that justified the decision.
2. **Embeddings inherit the residency of their source.** A vector is not anonymisation — inversion is
   demonstrated. Teams route inference carefully then ship the whole index to a hosted vector DB
   abroad.
3. **A prompt containing payment data is a cross-border transfer.** Transience and "we don't train on
   it" do not change the analysis. Classify **per field**, in code, on the inference path — and an
   **unknown field defaults to the STRICTEST class**, never the loosest.
4. **Log the RESOLVED model version, not the alias.** A provider moving an alias changes quality and
   bill with no deploy on your side. Teams debug a regression for a week before checking.
5. **Tag cost by PURPOSE, not by model.** Cost per feature lets you kill an expensive feature nobody
   uses; cost per model tells you nothing actionable.
6. **Alert on daily spend RATE.** A monthly budget alert fires on the 28th — 27 days late.
7. **Never sample the cost counter**, even when sampling traces. Sampled cost is simply wrong.
8. **Emit OpenTelemetry, not a vendor SDK.** The observability vendor is reversible only if you never
   coupled to it. Instrumentation is the asset; the dashboard is a commodity.
9. **Egress and rate-limit retries** are real and absent from every unit-price model.

**The reversibility table** — decide fast what is cheap to undo (model choice: hours behind an
adapter), slowly what is not (**core banking: years · ledger data model: effectively never**).
Nobody has successfully abstracted a core; do not try. **The model adapter is one day's work and the
highest-return code on the page** — an 80% price move happened this year and teams without one could
not act for a quarter.

**Metric nobody plots:** the share of AI calls that **fell back to rules**, and its trend. Zero means
the fallback has never been exercised and you do not know it works. Rising means something upstream
is degrading unnoticed.

---

### Session 56 — THE 224 ORPHANED PAGES, AND A WHOLE CLASS OF INVISIBLE BROKEN LINKS (DONE, 14 Sep 2026)

Started as "give the 224 non-`site-nav` pages a way out". Turned into the largest broken-link find of
the project.

#### 269 BROKEN ABSOLUTE SELF-LINKS — invisible for months

`linkcheck` matched `href="(/[^"#]*)"` — hrefs starting with `/`. **It never looked at
`href="https://www.clarigital.com/..."`.** Those are internal links written in absolute form, and
**269 of them were broken across 129 targets** while "Broken internal links: 0" reported green.

| Cause | Count | Fix |
|---|---|---|
| **`/wsp/` → `/csp/`** — the Student Program directory was renamed and links never followed | **205** | remapped, 107 pages |
| **Stale Codex paths** from a restructure (`/codex/seo/core-web-vitals/` → `/codex/seo/fundamentals/core-web-vitals/`) | **55** | remapped by unique slug match |
| **Pages that no longer exist** | **9** | repointed to nearest real ancestor section |

All absolute self-links across **837 pages** were also normalised to root-relative, so they are
visible to `linkcheck` from now on.

**`linkcheck` extended** to normalise absolute self-links before extracting. It immediately found
9 more that the remapper could not resolve — the check earning its place on the day it was written,
for the second time in four sessions.

#### The 224 pages outside the nav system

| Group | Finding | Decision |
|---|---|---|
| **117 AI Kids** | Already linked home — 117/117. The earlier count was my measuring error, not a defect | Keep `kids-nav`. A children's section should NOT carry the full adult nav — different audience, different safety framing. 3 pages needed the link added |
| **98 CSP task pages** | Topbar showed a Clarigital logo **that was not a link at all**. A student on a task page had no way back to the site | Discreet `← Clarigital` added to the topbar. No structural change |
| **9 CSP pages** | Had `nav-back`, but pointing at a deep `/wsp/` path or a relative `../index.html` that resolves to `csp/index.html`, not the root | Repointed to `/` |

#### CHECK #20 — "No route to home"

Every page must offer at least one link to the site root. Deliberately **weaker than
`nav_coverage`** and applied to **all 855 pages regardless of nav shape**, so sections with their own
navigation (AI Kids, CSP) are held to a floor without being forced into the main nav.

**Site: 20/20 at zero · 855 pages · linkcheck 0 (now including absolute self-links).**

#### The lesson, and it is the same one again

**A check only sees what its pattern matches.** `linkcheck` was correct about every link it looked at
and blind to an entire syntax. `node --check` was correct about every `<script>` and blind to
`onclick=`. Div counting was correct about totals and blind to ordering. `nav_coverage` was correct
about `site-nav` and blind to 224 pages using other navs.

**When adding a check, write down what it does NOT cover.** That sentence is where the next defect
is hiding.

---

### Session 55 — NESTING REPAIR: 25 PAGES FIXED (DONE, 14 Sep 2026)

The open finding from Session 51, closed. **Block nesting errors: 25 → 0.**

#### Why Session 51's attempt failed and this one worked

51 tried **string replacement** and the guard correctly refused to write both pages it attempted
(5→3 errors, 6→6). That was the right refusal. String replacement cannot fix this class of defect
because **the two errors cancel**: an unclosed `<div class="chapter">` plus a spare `</div>` in the
tail balances the count perfectly, so there is no unique string to target and no way to tell from
counts which of the two to change.

**The working approach is a stack walk**, in `_build/fix_nesting.py`:

| Situation | Action |
|---|---|
| close tag matches stack top | pop, keep |
| close tag is **deeper** in the stack | the elements above it were never closed → **emit their closing tags first**, then this one |
| close tag is **not in the stack at all** | stray → **drop it** |
| still open at `</body>` | close it |

Scripts are stashed behind placeholders before the walk and spliced back after, so `</div>` inside a
JS string cannot corrupt the stack.

#### The fix was tiny and identical on all 25

```
- </article>
+ </div></article>        <- close the chapter div that was never closed
...
- </div>                  <- drop the spare that was compensating for it
+
```

One insert, one drop. The whole tail of every affected document had been mis-parenting as a result:
`</article>` closed a `<div>`, then `</div>` closed the `<article>`, then `</section>` closed a
`<div>`, cascading to `</main>`.

#### Four gates, all four required before any write

`nesting_clean` (0 errors after) · `div_balanced` · **`text_intact`** — visible text byte-identical
before and after, so no content can be lost by a structural repair · `html_once`.

All 25 passed all four. A dry run was inspected as a unified diff on one page before anything was
written.

#### CHECK #19 — "Block nesting errors" promoted from metric to hard gate

It was a metric in Sessions 51–54 *because it was not yet at zero*. Now it is, so it gates. That
sequencing is the right pattern for any future check: **land it as a metric, fix the backlog, then
promote.** A check that ships red is a check people learn to ignore.

**Site now: 19/19 at zero · 855 pages · linkcheck 0 · 1,809 JSON-LD blocks clean.**

**Remaining metrics:** 217 thin pages (≈70 are hubs where short is correct) · 108 stale stamps.

---

### Session 54 — FINTECH VISUAL IDENTITY (DONE, 14 Sep 2026)

#### THE DIAGNOSIS — green meant three different things

Fintech had no section accent of its own. It used `--green` `#10B981` for body links and the hero
wash. But that same green is **also** the Beginner lane marker, **and** AI Kids' identity colour on
the homepage. One colour, three meanings, and the section read as muddy and borrowed.

Meanwhile `.note` — a general callout used in every lane — was **indigo**, which is the Intermediate
lane colour. So a note in a Beginner section was silently painted "intermediate".

#### THE FIX — one colour, one meaning

| Colour | Now means, and only means |
|---|---|
| **`--teal` `#14B8A6`** | **Fintech AI section identity** — body links, hero wash, TOC hover rail, `.note` callouts, the nav item |
| `--green` `#10B981` | **Beginner lane**, and AI Kids on the homepage. No longer overloaded |
| `--indigo` `#6366F1` | **Intermediate lane only.** Freed from `.note` |
| `--amber` `#F59E0B` | Advanced lane |

**Applied:** 6 replacements in `fintech_builder.py` (Rule 4 — patched in the same session),
150 across all 25 fintech pages, and the nav item recoloured on **626 pages** plus 4 that still had
it sharing AI Kids' green.

New vars in the fintech STYLE: `--teal:#14B8A6` and `--teal-dim:rgba(20,184,166,.09)`.

**Lane semantics verified intact** after the change — `.dot-green`, `.db-green` and `.lb-green`
untouched. The check is in the patch script, asserted before writing.

**The principle worth carrying:** a colour that carries two meanings carries neither. Before touching
any other section's palette, list what each colour currently signals and find the collisions first.

---

## THE FULL ROADMAP — 42 SESSIONS, WITH A HEALTH CHECK EVERY FIFTH

Committed. No compromise. **Every 5th session is a QA session** — nothing new is built, the whole
site is verified and whatever is broken gets fixed.

| Session | Work |
|---|---|
| ~~54~~ | ~~Fintech visual identity~~ **DONE** |
| ~~55~~ | ~~Fix the 25 nesting-error pages~~ **DONE** — check #19 now gates |
| ~~56~~ | ~~224 pages outside the nav system~~ **DONE** — plus 269 invisible broken links; check #20 |
| ~~57~~ | ~~Build Sheet 08 — Infrastructure~~ **DONE** |
| ~~58~~ | ~~Build Sheet 09 — Governance~~ **DONE — ALL NINE BUILD SHEETS COMPLETE** |
| ~~**59**~~ | ~~**★ QA #1**~~ **DONE** — found the unstyled progress bar on 65 pages |
| ~~60~~ | ~~AI Kids Money Explorer track — 8 sessions + index~~ **DONE** |
| ~~61~~ | ~~Money Explorer extended to 12 sessions~~ **DONE** |
| ~~62~~ | ~~Fintech theme~~ **DONE** — section menu still outstanding |
| ~~63~~ | ~~Sources pass part 1 — 9 build sheets + product guide~~ **DONE**, check #22 |
| ~~64~~ | ~~**★ QA #2** — Courses~~ **DONE** — found the progress bar never updated |
| ~~65~~ | ~~Sources pass part 2 — all 26 fintech pages~~ **DONE**, check #22 widened |
| ~~66~~ | ~~Housekeeping~~ **DONE** — dead domain in canonicals, check #23, metric corrected |
| 67 | Regenerate `all-guides` from the filesystem (lists 236 of 364) |
| ~~62~~ | ~~Fintech theme~~ **DONE** — section menu still outstanding |
| ~~63~~ | ~~Sources pass part 1 — 9 build sheets + product guide~~ **DONE**, check #22 |
| ~~64~~ | ~~**★ QA #2** — Courses~~ **DONE** — found the progress bar never updated |
| ~~65~~ | ~~Sources pass part 2 — all 26 fintech pages~~ **DONE**, check #22 widened |
| ~~66~~ | ~~Housekeeping~~ **DONE** — dead domain in canonicals, check #23, metric corrected |
| 67 | Regenerate `all-guides` from the filesystem (lists 236 of 364) |
| **64** | **★ QA** |
| 65 | Housekeeping — 108 stale stamps, Codex hub 220 cards vs 364 guides |
| 66–68 | Product guides 02–04 |
| **69** | **★ QA** |
| 70–73 | Product guides 05–08 |
| **74** | **★ QA** |
| 75–78 | Product guides 09–12 |
| **79** | **★ QA** |
| 80–81 | Product guides 13–14 |
| 82 | Re-scope content remediation — classify the 217 (≈70 are hubs where short is CORRECT) |
| 83 | Content remediation 1 |
| **84** | **★ QA** |
| 85–88 | Content remediation 2–5 |
| **89** | **★ QA** |
| 90–93 | Content remediation 6–9 |
| **94** | **★ QA** |
| 95–98 | Content remediation 10–13 |
| **99** | **★ QA — final** |

### ★ THE QA SESSION — what it must do

**Build nothing.** The point is to look at the site rather than the table.

1. Full audit, all 18 checks at zero, plus every metric recorded and compared to last QA
2. `linkcheck` · every `<script>` through `node --check` · every inline handler · every JSON-LD block
3. `nesting_errors()`, `nav_coverage()`, `stale_stamps()`, `thin_content()` — trend, not just count
4. **Open a real page in a browser and look at it.** Desktop and mobile width. Different sections
   each time, rotating
5. Click through one full user journey: homepage → section → module → build sheet → product guide
6. Verify one builder still runs from a clean room
7. Fix everything found. Record it in the MASTER even when the fix is trivial

**Why this cadence exists.** Six separate defects have now survived for months while every check
passed: stale dates · Python booleans in JavaScript · four unrunnable builders · scrambled block
nesting · a nav where 362 pages could not reach four of five sections · a colour meaning three
things. **Every one was valid-but-wrong.** Two user screenshots found in one minute what 15
automated checks had missed. The QA session is that, scheduled.

---

### Session 53 — NAVIGATION WAS BROKEN SITE-WIDE (14 Sep 2026)

User reported: Fintech AI missing from the mobile menu and from the homepage hub cards. Both true,
and the underlying problem was far larger than either symptom.

#### FIVE NAV GENERATIONS WERE LIVE AT ONCE

| Pages | What the nav offered |
|---|---|
| **362** | **`/codex/` only — NO cross-section links at all** |
| 183 | about · ai-atlas · codex · courses · curriculum — no fintech, no ai-kids |
| 56 | + ai-kids — still no fintech |
| 26 | + fintech ✅ |
| 2 | codex hub — fintech but `/curriculum/` not `/ai-kids/` |
| **1** | the homepage — the only correct one on the entire site |

**Only 29 of 631 pages linked Fintech AI.** And from any of the 362 Codex guides you could not reach
AI Atlas, Fintech AI, AI Kids or Courses — on desktop *or* mobile. The logo pointed at `/codex/`, not
home. The mobile drawer offered only Codex subsections. **362 pages were a walled garden**, and the
Codex is 364 of the site's 855 pages.

**Fixed: 631 of 631 pages with a site-nav now link all five sections, in the top bar and the drawer.**
Up from 29. Nothing was removed — section-local links survive alongside the new global ones.

Three nav shapes had to be handled: `<ul class="nav-links">`, `<div class="nav-links">`, and
`<ul class="nav-links" role="list">` — the third was missed by an exact-string match on the first
pass and caught by the new check, which is the check earning its place on the day it was written.
Two drawer shapes: `&#x2715;` and a literal `✕` close button.

#### NEW CHECK #18 — "Nav section coverage"

Every page with a `site-nav` must link all five canonical sections, in **both** the top bar and the
drawer. Fired at 10 immediately after the first pass; now **0**.

**Why 17 checks missed this for months:** every page's nav was *internally valid*. Valid HTML, no
broken links, no orphans — the sitemap was complete and every page was reachable *by a crawler*.
Nothing checked whether a **human** could get from one section to another. **Reachability and
navigability are different properties, and only the first was ever tested.**

#### Also fixed

- **Homepage hub card for Fintech AI — it did not exist.** Cards existed for Codex, AI Atlas and
  AI Kids only. Added in teal (`#14B8A6`), distinct from kids green / atlas indigo / codex blue.
- **`Search 360+ guides+ guides`** — a duplicated fragment in the search placeholder, on **62 pages**.
  Now "Search all guides". *This is the fifth time a hardcoded count has gone stale or malformed
  (313 → 253 → 218 → 220 → this). The numbers are out of the placeholders now.*

#### STILL OPEN — 224 pages outside the site-nav system

- **117 `kids-nav`** — AI Kids has its own nav. Probably correct for the audience, but it should at
  least reach home. Needs a decision, not a default.
- **98 with NO `<nav>` at all** — `csp/` student-program pages. Unexamined.
- **9 `<nav class="nav">`** — a fourth shape.

`nav_coverage()` deliberately skips pages without a `site-nav`, so these are invisible to it. That is
a known gap in the check, not an oversight.

---

### Session 52 — NEW PAGE TYPE: PRODUCT GUIDES (prototype, 14 Sep 2026)

`/fintech-ai/products/document-ai/` — 4,895 words, 3 code blocks, 1 registry. Site 854 → **855**.
Linked from the Identity module, under the build-sheet note.

#### THE GAP THE USER FOUND

The site is organised on ONE axis: **capability** (identity, credit, fraud, AML, payments…). Modules
explain how things work; build sheets list what to buy for a *domain*. Both answer *what do I buy for
this capability*.

They never answer **how do I ship this product**. Checked against a list of 16 real fintech products
(Document AI, Video KYC, liveness, UPI switch, soundbox, cross-border remittance, alt credit scoring,
co-lending, invoice discounting, BNPL, AA modules, transaction monitoring, eNACH/AutoPay routers,
embedded insurtech, robo-advisory, treasury/payroll SaaS): **zero existed as a page.**

The ingredients were all there — Textract, Azure Document Intelligence, PaddleOCR, Surya, 39 mentions
of OCR across the identity module. **We documented every ingredient and never wrote a recipe.**

**Why we missed it:** the module axis was set early and inherited by the build-sheet template at
Session 44 without ever being re-examined. Nobody asked whether the reader's unit of work might be a
*product* rather than a *capability*. For anyone building FOR a bank or an MNC, it always is — they
have a Video KYC product with a spec and a delivery date, not an "identity capability".

#### THE NEW PAGE TYPE — what makes it different from a build sheet

A build sheet says *here are the parts and three ways to combine them.*
A product guide says *step 3 outputs this shape, step 4 expects that shape, here is the transform,
and here is what happens when step 3 returns low confidence.*

**The wiring is the whole reason the page type exists.** Template:

1. How to use this page (and where to go instead)
2. What the product actually is — and what it is NOT
3. **The whole journey in one table** — every step, in plain words
4. Per step: what it does · **your options as a table** (option / what it is / cost / when to pick) ·
   what goes in · what comes out · **how to connect it to the next step** · what breaks
5. **A dedicated wiring section** for the hardest handoff, with both data shapes written out
6. What it costs
7. Three versions (weekend / proper / enterprise)
8. What goes wrong, ranked by frequency
9. Where to go deep — links INTO the module and build sheet

**STYLE: "dodo language" — an explicit second register.** Short sentences. Second person. Jargon
defined once on first use. Assumes the reader has not built this before. This is a *deliberate
deviation* from the dense expert voice of the modules and must be written into the house style,
or it will get quietly edited back.

**THE ANTI-DUPLICATION RULE — non-negotiable.** The product guide owns the **workflow and the
wiring**. Depth stays in the module and the build sheet and is *linked*. If a product guide
re-explains OCR, that content is now maintained twice and it WILL drift. This project has the scars:
the quiz markup drifted from its stylesheet until it died (47b), and there are 12 AI Atlas stylesheet
generations live right now.

#### Document AI — the eight-step spine

`1. Get the file · 2. Check it is usable · 3. Work out what it is · 4. Read the text ·
5. Turn words into fields · 6. Check the fields are real · 7. Accept, review or reject ·
8. Keep the evidence`

**Steps 2, 6, 7 and 8 are the ones people skip, and they are the ones that separate a demo from a
product.** Steps 3 and 4 are where the money goes; 2, 6, 7 and 8 are where the product lives.

**Findings worth carrying into other product guides:**

1. **Confidence ≠ correctness.** An OCR engine reads a smudged 8 as a 3 at 0.98. Checksums and format
   rules must run on 0.99 fields too. This is step 6 and it is the demo/product line.
2. **A joined field takes the LOWEST score of its parts, never the average.** "RAJESH" 0.99 +
   "KUMAR" 0.60 is a 0.60 name. Averaging confidence is how bad reads get through.
3. **Carry the confidence AND the bounding box all the way through.** They look like debug data at
   step 5; by step 7 they are the product (reviewers go 3–5× faster when the box is drawn on the
   image) and by step 8 they are the evidence.
4. **Boxes as 0–1 fractions, never pixels.** Pixels break on a different upload resolution.
5. **Normalise every OCR engine into ONE internal shape in a per-engine adapter.** Never let
   Textract's key names reach your database. Engine swap becomes a one-file change.
6. **`missing` must be an explicit list, not absent keys.** "We could not find the DOB" and "we never
   looked" are different facts.
7. **An LLM asked for JSON will invent a plausible DOB.** Verify every returned value appears in the
   OCR text; if not, mark it missing. Same rule as the refusal gate in Build Sheet 06 — **present in
   retrieved text, not merely plausible**.
8. **Three outcomes, never two.** Accept / review / reject. Automatic reject on a real customer's
   document is almost always wrong — route to review and let a person reject.
9. **Measure the OVERRIDE RATE.** If reviewers accept 95% of what you send them, thresholds are too
   tight and you are paying people to click yes.
10. **Every reviewer correction is training data AND a bug report.** Store before and after. Highest
    value data the system generates; most teams discard it.
11. **DigiLocker can skip steps 2–6 entirely** for supported documents — you receive the issued
    record, not a photograph. Check availability BEFORE building the pipeline.
12. **"Ask the user what the document is" beats any classifier** when there is a user to ask. Free
    and more accurate. Classifiers are for post boxes and bulk scans.

**Cost figures carried unchanged from Build Sheet 01 and stamped `Verified May 2026`** — not
re-verified this session, and the page says so. This pushed the stale-stamp metric 107 → 108, which
is correct behaviour, not a regression.

#### SCOPE WARNING

16 products at this depth is **16 sessions**, roughly doubling the remaining backlog (2 build sheets,
25 nesting-error pages, content remediation re-estimated at 12–18 sessions). Two or three of the
listed products — merchant soundboxes/POS, payroll SaaS — sit outside the current nine-module remit
and need a scope decision rather than being slotted in.

**This page is a PROTOTYPE.** Judge the format before committing to the other fifteen. Two sheets
into a nine-sheet format was a cheap place to discover a frame was wrong; the same logic applies here.

---

### Session 51 — BUILD SHEET 07: Wealth & Advisory (DONE, 14 Sep 2026)

`/fintech-ai/wealth-advisory/build-sheet/` — 4,937 words, 3 code blocks, 1 registry.
Linked from the module. Site 853 → **854**. **SEBI is the regulator here, not RBI.**

#### SEBI IA framework — amended repeatedly since Dec 2024 (Verified Sep 2026)

| Item | Current position |
|---|---|
| **Supervisory body** | **IAASB = BSE Limited**, appointed 25 July 2024 for five years |
| **Net worth** | **Abolished Dec 2024.** The old ₹25 lakh corporate net worth replaced by a **deposit-based system**, held **under lien in favour of IAASB** |
| **Registration fee** | **₹15,000**, within 15 days of approval. Budget **3–6 months** for the process |
| **Corporatisation trigger** | **300 clients OR ₹3 crore** fee collection in a FY, whichever first (raised from 150 clients). Notify immediately → **3 months** for in-principle approval → **3 more** to complete, onboarding continues throughout |
| **Qualification** | **Nov 2025: graduates of ANY discipline** may register as IA or RA with the required NISM certification. The finance/commerce/economics degree requirement is gone. Extends to "persons associated with investment advice" |
| **Fee cap** | **₹1.51 lakh p.a. per client** (individuals and HUFs), inflation-revised, reviewed ~every 3 years by the ASB. AUA mode or fixed fee |
| **Part-time IA** | New category. The other activity must not involve handling client money or advising on investment products |
| **Compliance audit** | Annual, by **CA / CS / CMA**, **line-wise** against every provision, adverse findings filed within the timeline. Non-individual IAs may appoint an independent ICAI/ICSI/ICMAI professional with NISM certification as compliance officer |
| **Scope** | "Investment advice" covers only **SEBI-regulated securities**; IAs may advise outside that perimeter with disclosure **plus a client declaration and undertaking**. "Investment products" excluded from the definition. **IAs cannot give trading calls** |
| **Model portfolios** | Now within "research services" for RAs — methodology, review frequency, benchmarking and horizon must be defined |

**SEBI on AI, verbatim in effect:** responsibility lies **solely with the IA/RA, irrespective of the
scale and scenario of AI usage**; data security, integrity and transparency of the derived advice
must be ensured; **the extent of AI use must be disclosed to the client**. Existing-client compliance
deadline was 30 April 2025. **Using AI increases responsibility, it does not share it.**

**Enforcement anchor:** the Dec 2025 Avadhut Sathe order — **₹546 crore impounded plus a market
ban**. "For educational purposes only" does not excuse unregistered advisory activity, inside a
course, a private group, or a chatbot reply.

#### Data and tooling (Verified Sep 2026)

- **AMFI NAV feed — free**, daily, every Indian scheme. Backbone of most Indian wealth products.
- **Kite Connect Personal: free** — orders, positions, holdings, funds, **NO market data**.
  **Kite Connect paid: ₹500/month per API key**, live + historical data included.
- Zerodha intraday brokerage **₹20 or 0.03%, whichever lower**, per executed order. Upstox ran
  **₹10/executed order via API** under a developer scheme **through 31 March 2026** — that date has
  passed; confirm rather than assume it continued.
- Three data tiers: **broker APIs** (data + execution, scope limited to the broker's licence) ·
  **aggregators** (TrueData, Global Datafeeds — unified REST, fundamentals, corporate actions) ·
  **direct exchange feeds** (authorised vendors, colocation — institutional, and a sign of a
  mis-specified requirement if it appears in an advisory plan).
- **Calculation layer is free and should be built, not bought:** cvxpy, PyPortfolioOpt,
  Riskfolio-Lib, NumPy, SciPy, Pandera. There is no meaningful optimiser market at Indian retail
  advisory scale — what a wealthtech platform actually sells is **RTA / StAR MF plumbing, reporting
  and compliance workflow**. Evaluate on that.

**THE LICENSING TRAP — market data redistribution.** A broker API's data licence generally covers
*you* using it for *your own* account. Showing that exchange data to *your clients* is
**redistribution**, which normally needs an exchange data licence or an authorised-vendor
arrangement. Teams build a customer-facing product on a ₹500/month key and find out in diligence.
**Third instance of the same pattern** — OpenSanctions CC BY-NC (Sheet 04), Elastic Licence V2 on
Marble (Sheet 04), and now this. *The software is cheap; the licence is the product.*

#### Gotchas documented

- **The fee cap is the first number in the model, not the last.** ₹1.51 lakh/client/year is the
  ceiling and the realistic retail average is a fraction of it. It decides whether you can afford
  human oversight per client, which decides whether you can be advisory at all. **Most Indian
  robo-advisory plans fail at this line, not at the technology.**
- **`binding = min(capacity, tolerance)`; `required` is never a permission.** If the goal demands
  more risk than the client can bear, **the goal changes** — horizon, contribution or target — not
  the portfolio. Goal-seeking is what optimisers are *for*, which is exactly why the constraint gets
  quietly relaxed and nobody notices.
- **Store the EXCLUSIONS, not just the recommendation.** "Why was this fund never recommended to
  this client" has a correct answer, and it cannot be recomputed from a catalogue that has since
  changed. Cheap to store; the difference between inspection-ready and inspection-panicked.
- **Record the monitoring runs that found nothing.** An absence of records is indistinguishable from
  an absence of monitoring — including to you.
- **Tolerance exceeding capacity by 2+ bands** is the asymmetry that predicts complaints after a
  drawdown. Flag and document the conversation.
- **Glide paths beat periodic reviews** — an annual step-down is wrong for 364 days a year and most
  wrong in the year before the client needs the money.
- **Suitability regression:** a holding can stop being suitable with nobody transacting — the fund
  changed mandate, or capacity fell. A mandate change must re-check every client holding it.
- **The drift pattern in "education-only" products is gradual:** a calculator gains a "based on your
  answers" label, a table gains a default sort, a list gains a "popular with people like you" badge.
  Three screen tests: does it use anything we know about *this* user · would a reasonable user read
  it as a recommendation · would we be comfortable if a regulator saw it without the disclaimer.

---

### ⚠ OPEN FINDING — 25 PAGES WITH SCRAMBLED BLOCK NESTING (not fixed)

Found while fixing a `<div>` I had wrongly nested inside a `<p>` in my own build script.

**Counting tags cannot detect two errors that cancel.** These pages have an unclosed
`<div class="chapter">` *and* a spare `</div>` in the tail. Div counts balance perfectly, all 17
checks pass, and the tree is still scrambled — `</article>` ends up closing a `<div>`, then
`</div>` closes the `<article>`, and the error cascades to `</main>`.

- **25 of 854 pages.** 22 share the signature `</article> closes <div>`; mostly `codex/analytics-cro/`.
- Browsers silently repair it. **HTML parsers and LLM crawlers do not**, and machine readability is
  the site's stated purpose.
- **NOT FIXED.** I attempted two pages, the verification guard refused both (5→3 errors on one, 6→6
  on the other), and nothing was written. The tail structure differs between page families, so this
  needs a proper stack-driven repair, not a string replacement — and it needs budget to verify.

**New metric wired into `audit.py`: `nesting_errors()`** — a stack walk over
`div · section · main · header · footer · article · nav · aside`. Currently reports **25**. Kept as a
metric rather than a zero-gate precisely because it is not yet fixed.

**Session 52 should do this first.** The repair is mechanical once written: walk the stack, and where
a close tag does not match the top, insert the missing close before it. Verify with `nesting_errors()`
per page before writing, and only write pages that reach zero.

**The general lesson, third time this project has learned a version of it:** a check that counts is
not a check that validates. Div balance passed on 25 broken pages for months.

---

### Session 50 — BUILD SHEET 06: Customer Operations (DONE, 14 Sep 2026)

`/fintech-ai/customer-operations/build-sheet/` — 5,218 words, 3 code blocks, 1 registry.
Linked from the top of the module. Site 852 → **853**.

**Organising idea:** the gap between a 3–27% hallucination rate and a sub-0.1% tolerance cannot be
closed with a better prompt or a better model. It closes by making the system **unable** to state a
number it did not retrieve — grounding, citation and a refusal path enforced **in code after
generation**. Infrastructure, not prompt engineering.

#### ⚠ TIME-CRITICAL — WhatsApp free service window ENDS 1 OCTOBER 2026

The single most important finding of the session, and it lands in ~2.5 weeks.

- Meta moved from **conversation-based to per-message pricing** during 2025 — every older WhatsApp
  pricing guide is wrong.
- The **24-hour customer service window has been free since November 2024**. **From 1 Oct 2026 Meta
  charges per service message at the utility/authentication rate.**
- For a support-heavy business this turns the *largest* message category from free into a per-message
  cost, and creates a design incentive that did not previously exist: **a verbose AI agent is now
  measurably more expensive than a concise one.** Most agents are tuned for warmth, not brevity.

**India rate card (Meta list, effective 1 July 2026, per delivered message, before BSP fee and GST):**

| Category | Rate |
|---|---|
| Marketing | **₹0.8631** (rose ~10% during 2026 from ₹0.7846) |
| Utility | **₹0.1150** |
| Authentication | **₹0.1150** |
| Authentication-International | ₹2.4971, tiering down to ₹1.7480 |

- **+18% GST.** A ₹0.8631 marketing message is **₹1.0185** with GST.
- **Marketing is ~7.5× utility.** A support message mis-templated as marketing costs 7.5×.
- **Meta's rate is IDENTICAL through every BSP.** The only variables are the BSP platform fee, its
  markup, and setup (₹0–₹25,000). Do not let a BSP present Meta's rate as its own pricing.
- Rate is set by the **recipient's** country, not yours. Inbound opens a 24-hour window;
  Click-to-WhatsApp opens **72 hours**.
- **Quoted WhatsApp prices differ wildly because some include GST, some include BSP markup and some
  are Meta list.** Ask which of the three, every time. (Observed in the wild: ₹0.8631, ₹0.88 and
  ₹1.09 all described as "the marketing rate".)

#### AI agent pricing — the unit is the trap again (Verified September 2026)

| Vendor | Unit | Rate |
|---|---|---|
| **Intercom Fin** | per outcome | **$0.99**, 50-outcome monthly minimum, $49/mo entry incl. 50. Runs over an existing helpdesk, **no seats required** |
| **Zendesk** | per automated resolution | **$2.00** |
| **Fini** | per resolved ticket | **$0.89 / $0.69 / $0.49** by tier |
| **Salesforce Agentforce** | per **conversation** | ≈ **$2.00** |
| **Sierra** | quote-only | year one commonly estimated **$200k–$350k+**; contracts from ~$150k; implementation **$50k–$200k**; **3–7 month** deployments |
| **Decagon** | quote-only | publishes nothing; platform fee ~$50k/yr; third-party contract data ~$105k to ~$432k median |
| **Ada** | quote-only | from ~$30k/yr |

- **Per-conversation is not per-resolution.** At a 60% resolution rate, $2.00/conversation is an
  effective **$3.33 per resolution**. Divide by your realistic rate before comparing anything.
- **Helpdesk dependency is the hidden line.** Ada, Sierra and Decagon are agents, not helpdesks —
  human workflow needs a platform underneath at **$55–$175+/agent/month**. Add it to every quote.
- Competitive benchmark: **$0.50–$1.00 per resolved conversation with no platform fee** for mid-market.

**THE finding worth carrying forward — the billing metric IS the quality metric.**
The vendor's definition of "resolution" is your entire bill, and at least one major vendor counts an
**assumed resolution** when a customer exits without replying — which is also exactly what a customer
does when the answer was useless. **Get four answers in writing:** does an escalated conversation
still bill · does a customer returning with the same question bill twice · is resolution *confirmed
by the customer* or *inferred from the chat ending* · what happens during an outage spike.
This lines up exactly with the module's quality finding (teams count "no escalation" but never count
"customer recontacted"). **Measure recontact yourself. Never accept the vendor's resolution number as
a quality signal.** One vendor cites ~71% average resolution; independent reports place it at 42–50%.

**Metering clauses to read as carefully as the rate:** from **1 January 2026** one major vendor bills
overage automatically each month on non-standard contracts — **overage ON by default, no cap, no
grace period**; switching it off *pauses the AI agent at the limit* instead, turning a billing setting
into an availability decision. Another charges an AI-resolved ticket as **both a ticket and a
resolution**. Market is consolidating — a ~**$3.6bn** acquisition of a major agent vendor was agreed
June 2026, not closed at time of writing, pricing unchanged so far. Ask what happens to your contract
and data on change of control.

#### Voice AI in India (Verified September 2026)

- Headline **₹2–₹12/min**; **₹3–₹6** is the common mid-market band.
- **Effective cost is 2–4× headline** in production once platform fees, telephony markup over TRAI
  rates and connect-rate losses are added. A ₹3/min quote is typically ₹6–₹9/min live.
- Per connected call **₹4–₹15**; per successful outcome **₹8–₹25**.
- Scale helps unusually hard: ~₹9.94/min at 25,000 min/month → ~₹6.02/min at 25 lakh. Implementation
  can reach seven figures. +18% GST.
- **Four cost layers — STT + LLM + TTS + telephony.** Some vendors quote one and bill the rest.
  Confirm the rate bundles all four.
- **Per-minute pricing pays the vendor for its own latency.** Dead air is billed. **Ask for the
  average silence-to-speech ratio across a sample of 1,000 real calls.** The reaction to the question
  tells you most of what you need.
- Per **attempt** rather than per connected call is a trap: Indian outbound connect rates run 30–65%.
- Language mix drives cost: English-only < Hinglish code-switch < Tamil < Malayalam.
- **Human benchmark:** fully loaded telecaller ₹30,000–45,000/mo (BPO), ₹45,000–70,000 (in-house
  mid), ₹70,000–1,20,000 (in-house senior BFSI); 80–120 dials/day, **25–40 meaningful connects**,
  22 working days. Compute your own cost per connect before believing any deflection business case.

#### Gotchas documented

- **A system prompt is not a control.** "Never promise a refund" in a prompt is a suggestion to a
  probabilistic system; the same rule as a validation check that blocks the send is evidenceable and
  unit-testable. Regulators distinguish between them.
- **The numbers a model gets wrong are not the ones in your knowledge base** — they are the ones it
  *interpolates*: a plausible processing time, a plausible fee between two real ones. A faithfulness
  score over your documents will not catch it, because nothing contradicts it. **Gate on PRESENCE IN
  RETRIEVED CONTENT, not absence of contradiction.**
- **Refusal must be a first-class path**, not an error branch.
- **The collections contact window is usually implemented on the dialler and not on the scheduler.**
  Voice gets gated; the automated SMS, WhatsApp utility template and push notification go through
  different systems with no window logic. The directions cover **digital** contact — 22:00 is a
  violation regardless of which service sent it.
- Evaluate the window **at send time in IST, not at queue time**. A batch queued 18:55 dispatching
  19:20 has breached.
- **Vicarious liability:** outsourcing collections does not outsource the obligation. Contract for
  agency log access and audit it; an assurance of compliance is not evidence of compliance.
- **Hybrid retrieval (BM25 + vector)** — keyword catches product names, policy codes and error codes
  that embeddings blur. Skipping BM25 is the most common retrieval mistake.

**Position the page takes:** buy the agent, **build the gate**. Vendor guardrails protect the
vendor's reputation; yours must protect your licence — different specifications, and the second must
be inspectable by compliance and testable in CI. The lean build is **assist-only** (no autonomous
customer-facing answers), stated as a legitimate destination rather than a stepping stone: it carries
almost none of the exposure and produces the labelled data a later deflection project needs.

---

### BUILDER NOTE — an f-string trap that has now cost two sessions

`note()` and `warn()` are called from inside f-strings. **A backslash cannot appear inside an
f-string expression**, so `warn("... \\"quoted\\" ...")` is a **SyntaxError** — the build script
refuses to parse, and the failure looks like a content problem rather than a syntax one. It cost a
session in 47 and again in 50.

**Use HTML entities for quotes in anything passed to `note()`, `warn()` or `registry()`:**
`&ldquo;` `&rdquo;` `&lsquo;` `&rsquo;`. Documented in `_build/README.md`.

---

### Session 49 — BUILD SHEET 05: Payments & Reconciliation (DONE, 13 Sep 2026)

`/fintech-ai/payments-reconciliation/build-sheet/` — 5,454 words, 3 code blocks, 1 registry.
Linked from the top of the module. Site 851 → **852**.

**The organising idea:** in every other build sheet cost is a line item. Here it is a percentage of
revenue forever, so the page leads on economics rather than on tooling.

#### THE BIG ONE — UPI MDR IS COMING BACK

The **Taxation and Other Laws (Amendment) Bill, 2026**, passed by the Lok Sabha in August 2026,
amends the **Payment and Settlement Systems Act, 2007** to let the government notify categories of
digital transactions that may carry charges. Zero MDR on UPI and RuPay debit has held since
January 2020.

| | |
|---|---|
| Consumers | No charge. All P2P stays free. Stated by the Finance Ministry. |
| Reported rate under discussion | **0.25%–0.4%** |
| Scope | **Large merchants only** (turnover thresholds around ₹1–1.5 crore reported), on tickets **above ₹2,000** |
| Coverage | Would leave roughly **95% of UPI transactions** untouched |
| Status | **Enabling provision only. Rates and categories NOT notified.** |

**Do not write a number into a pricing model.** Do build the ability to apply a per-rail,
per-ticket-size fee. The page says it plainly: *if your margin only works at 0% UPI MDR, your margin
is a policy position rather than a business model.*

Context captured: UPI runs ~88% of India's digital payments, past **24 billion transactions and
~₹30 lakh crore a month**. NPCI's 30% third-party market-share cap is now scheduled for
**December 2026**; PhonePe and Google Pay together hold ~80%.

#### RBI (Regulation of Payment Aggregators) Directions, 2025 — notified 15 Sep 2025

Repealed and replaced the 2020 PA-PG Guidelines, the 2021 clarifications and the separate PA-CB
circular. Effective immediately on notification.

- **Three categories: PA-O** (online) · **PA-P** (physical/proximity) · **PA-CB** (cross-border).
  **PA-P is newly regulated** — PA-P-only entities had to apply by **31 Dec 2025** or wind down by
  **28 Feb 2026**.
- **Net worth ₹15 crore at application → ₹25 crore**, maintained on an ongoing basis.
- **Escrow** with a Scheduled Commercial Bank. Own funds excluded. **Day-end balance must equal the
  amount realised.** Pre-funding permitted for domestic PAs only, and pre-funded amounts cannot be
  withdrawn.
- **PA-CB:** separate **InCA** (inward) and **OCA** (outward), never commingled · per-transaction cap
  **₹25 lakh** · no direct forex dealing except through an authorised dealer · no interest on
  international balances.
- **Settlement liberalised** from a fixed regulatory timeline to the PA–merchant agreement, provided
  it is fair, equitable and transparently disclosed. *(Sources differ on whether a T+1 outer limit
  survives — verify against the Master Direction before designing around it.)*
- **Card data: only issuers and networks may store it.** Everyone else tokenises or deletes.
- Monthly transaction statistics to RBI; quarterly auditor's certificate on escrow. FIU-IND
  registration required — ties to Build Sheet 04.
- **⚠ Deadline: 15 September 2026** — merchants onboarded up to 31 Dec 2025 must be brought into line
  with the new CDD requirements. No leeway for merchants onboarded from 1 Jan 2026. Acquiring banks
  now need their own policy for merchants acquired by non-bank PAs.

#### Pricing captured (Verified September 2026)

| Item | Figure |
|---|---|
| Domestic cards / netbanking / wallets | ≈ **2%** (Razorpay class); **1.75–1.95%** commonly cited for Cashfree |
| High-volume domestic cards | sometimes a **flat ≈ ₹9/transaction** instead of a percentage — much cheaper on large tickets |
| Premium (Amex, Diners, EMI, international) | ≈ **3%**; chargeback protection ≈ **+1%** |
| Legacy gateways | **1.6–1.8%** headline + setup **₹5,000–50,000** + AMC **₹2,400–9,999/yr** |
| **GST** | **18% on the fee, not the transaction.** A 2% fee is **2.36%** all-in. Never in the headline |
| Cross-border receipt | ≈3% headline, **5–7% all-in** with FX spread and partner bank fees |
| Instant settlement | paid add-on — **price it as a loan**: 0.1% to get money one day early ≈ **36% annualised** |

**The ranking argument, stated in the page:** do NOT rank on TDR. On ₹1 crore monthly volume the
1.75%-vs-2% spread is ~₹30,000/month. Vendor-claimed success rates differ by 10+ points, which is
**₹10 lakh of orders**. Rank on success rate measured on *your own* split traffic, settlement timing
and what early access costs, **reconciliation data quality**, and failure behaviour (webhook
reliability, replay tooling, and the documented Indian pattern of sudden account freezes).

**Compute cost per successful order, not per transaction:** `(fee × 1.18) ÷ success rate`, per rail,
on your own mix. Reorders most shortlists. No vendor will compute it for you.

#### Gotchas documented

- **Zero MDR never meant zero cost.** MDR is the acquiring charge; your PA's platform fee is a
  separate commercial term. Published cards commonly show UPI at 0% and contracts sometimes still
  carry a fee. Get the rail-by-rail rate in writing.
- **Webhook signature must be verified over RAW BYTES.** `get_json()` reorders keys and changes
  whitespace, the digest never matches, and teams "fix" it by skipping verification.
- **Webhooks are at-least-once and out-of-order.** `payment.failed` can arrive *after*
  `payment.captured`. Order by the event's own timestamp, never by arrival. Store the event id and
  check it **in the same transaction** as the state change.
- **A signed webhook proves origin, not correctness.** Verify the amount against your own order.
- **A webhook is a notification; the settlement file is the fact.** Webhook → `captured`,
  settlement file → `settled`. **Collapsing these two states causes a large share of all breaks.**
- **Fees are deducted per-transaction by some PSPs and as one aggregate debit by others** — and it
  varies by plan within a single PSP. Per-transaction means every match is net-of-fees; aggregate
  means transactions match exactly and one large debit belongs to no order. **Building for one and
  receiving the other is a full rewrite of the matching layer.** Ask for a sample file first.
- **A timeout is not a failure, it is an unknown.** Retrying a timed-out payout with a *fresh*
  idempotency key is how platforms pay the same person twice. Derive the key from the **intent**,
  store it **before** the call, and resolve unknowns by querying on *your* reference.
- **Refunds are not negative payments.** Own lifecycle, own settlement timing, own failure mode
  (money left escrow, never reached the customer). Own table, own idempotency key, own queue.
- **Control totals before matching, and ABORT on mismatch.** A truncated file reconciles at a
  perfect rate on the rows present.
- **FULL OUTER JOIN, not LEFT.** A settlement row in no ledger is the interesting case — money you
  were paid and cannot explain.
- **Reconcile in IST.** Settlement files cut on IST business days; UTC aggregation moves 5.5 hours
  into the wrong settlement day, every day.
- **Ask about the exit path before signing.** Integration takes a day; extracting card tokens,
  mandates and subscription state takes a quarter, and that is why merchants accept bad renewals.

**Position the page takes:** DuckDB plus an append-only ledger gets most teams further than they
expect — settlement reconciliation is a join, and until millions of transactions a day it runs in
seconds against CSVs on disk. Buying an enterprise close suite for a single-PSP book is three to six
months of implementation to automate a query you could write today.

**The second gateway is in the DEFAULT build, not the expensive one** — not mainly for redundancy,
but because running 5% of traffic elsewhere is the only honest success-rate comparison available and
the only leverage at renewal.

---

### SESSION 48 — BUILD INFRASTRUCTURE REPAIR (13 Sep 2026)

**Build Sheet 05 was not started.** Chasing the one loose end left by 47b turned it into a much
larger problem, and fixing it was worth more than a rushed page. Sheet 05 moves to Session 49.

#### FOUR OF FIVE PAGE BUILDERS COULD NOT RUN AT ALL

47b found `course_builder_v3.py` reading two templates from `/tmp`. The real number is **twelve
templates across four builders**, none of them ever bundled:

| Builder | Missing templates |
|---|---|
| `atlas_builder.py` | `atlas_style.txt`, `atlas_nav.txt`, `atlas_footer.txt` |
| `tool_builder.py` | `tool_style.txt`, `tool_nav.txt`, `tool_footer.txt`, `tool_scripts.txt` |
| `guide_builder.py` | `codex_style.txt`, `codex_nav.txt` |
| `course_builder_v3.py` | `c_style.txt`, `c_script.txt`, `c_nav.txt` |

Only `fintech_builder.py` was self-contained. **This is the root cause of the 47b quiz failure** —
the generator and the stylesheet drifted apart because nobody could load them together.

All twelve reconstructed from live pages and bundled in `_build/`. Every builder now resolves
`_build/` → `/tmp` → raise. **Verified in a clean room** (`_build/*` copied to an empty directory,
no `/tmp` templates present): all five builders load.

**Reconstruction was verified, not assumed.** Each template was extracted from 6+ pages of its type
and required byte-identical agreement. Seven passed. **Five did not, and hold the dominant variant
only:** `atlas_style.txt` (**12 live variants**, dominant 52/155), `atlas_footer.txt` (19 variants,
22/155), `c_nav.txt` (3, 52/64), `tool_scripts.txt` (3, 15/23). Documented in `_build/README.md`.
**Regenerating an AI Atlas page will restyle it to the majority template — diff before accepting.**

**Twelve stylesheet generations inside one section is its own finding.** Not fixed this session;
it needs a deliberate consolidation like Session 43, not a silent normalisation.

#### BUG 5 — 28 pages with unbalanced block tags

Found because the template extraction refused to agree. `structcheck` had **only ever balanced
`<div>`**.

- **22 AI Atlas tool pages: a stray `</header>` with no opening `<header>`.** The nav sat outside the
  header landmark on those pages and inside it on the other 16.
- **3 Codex pages never closed `<main>` or `<section>`** (`linkedin-ads`, `pinterest-ads`,
  `whatsapp-marketing`).

All 28 fixed. Browsers silently repair this, which is exactly why it survived — but the site's stated
purpose is to be readable by non-JS crawlers and LLM fetchers, and those parse the markup as written.

**`structcheck` now balances** `section · main · nav · article · aside · header · footer · table ·
form` alongside `div`. Site-wide: **zero unbalanced block tags.**

Fixing the header bug also made `tool_nav.txt` uniform (2 variants → 1), which is how the extraction
check confirmed the fix rather than just asserting it.

**State:** 851 pages · 17/17 at zero · all block tags balanced · 5/5 builders runnable.

---

### SESSION 47b — FOUR LIVE BUGS FOUND FROM TWO SCREENSHOTS (13 Sep 2026)

Reported by the user from a desktop view: pills rendering as circles, and "Test your
understanding" doing nothing on click. Both were real. Investigating them surfaced two more.
**All four had passed every one of the 15 standing checks.**

#### BUG 1 — the course quiz was completely dead. 68 pages.

Four independent defects stacked on the same component:

| Defect | Scope | Effect |
|---|---|---|
| `checkAnswer()` **never defined anywhere on the site** | 68 pages | every option click threw `ReferenceError` |
| `onclick="checkAnswer(this,True)"` — **Python bools written into JavaScript** | 65 pages, **1,560 occurrences** | `True`/`False` are undefined identifiers in JS |
| `style="display:none"` on `.quiz-body` | 65 pages, 195 blocks | inline style beats `.quiz-body.open`, so the toggle silently did nothing — **this is what the user saw** |
| markup emits `.quiz-opts` / `.quiz-feedback` / `.qt-arrow`; CSS defines `.quiz-options` and neither of the others | 65 pages | options unstyled, feedback invisible, arrow never flipped |

**Root cause, in the builder**, `course_builder_v3.py` line 31:

```python
f'<button class="quiz-opt" onclick="checkAnswer(this,{j==cor})">{o}</button>'
#                                                    ^^^^^^^^ Python bool -> "True"
```

**Two generations of quiz markup were live at once.** 3 hand-built pages (google-ads, agentic-ai,
seo) use `answerQ()`, `.quiz-options` and `#id-icon` — and `answerQ` *is* defined on all 68 pages.
65 generated pages use `checkAnswer()`, `.quiz-opts` and `.qt-arrow`, none of which existed. The
generator drifted away from the stylesheet and nothing compared them.

**Fixed:** `checkAnswer()` written and shipped, bools lowercased, inline `display:none` removed,
missing CSS added, `toggleQuiz()` rewritten to find `.qt-arrow` and set `aria-expanded`. Quiz body
now renders **visible without JS** and collapses only under `html.js` — rule 6, same pattern as
`.track-panel`. Verified functionally against a DOM stub, not just parsed.

#### BUG 2 — `.art-meta` chips rendering as circles. 58 AI Atlas tool pages.

The "Visit <tool>" button block sat **inside** `.art-meta`, which is
`display:flex;flex-wrap:wrap;gap:8px` with default `align-items:stretch`. The button div became the
tallest flex item, every `.meta-tag` span stretched to match it, and `border-radius:100px` on a tall
span with two words of text renders as a **circle**. Exactly the screenshot.

Balanced-extracted and closed `.art-meta` before the button div on all 58. **Note for the record:
`tool_builder.py` emits this correctly** — those 58 pages predate it (they still said "Updated April
2026") and a later sweep dropped the closing tag. The builder was not at fault.

**Mobile was actually better, not worse.** With `flex-wrap`, `align-items:stretch` applies per flex
line — on a narrow viewport the button wraps to its own line and the chips render normally. The bug
is a desktop-width bug.

#### BUG 3 — the Codex hub search box was dead. Found by the new check, not reported.

`codex/index.html` calls `doSearch(...)` from two inline handlers. **`doSearch` was defined nowhere
on the site.** Typing in the hero search box threw on every keystroke.

There are **two** search controls on that page and only one worked: the nav search uses
`data-search-input` and is wired automatically by `theme-search.js` (which defines `search`, not
`doSearch`). The hero box was meant to filter the cards already on the page. `doSearch()` now
written: filters `.art-card` on `data-t`/`data-d`, hides emptied sections, toggles `#noResults`,
updates the `aria-live` `#searchFb` counter.

#### BUG 4 — `course_builder_v3.py` was unrunnable in a fresh session.

It read its stylesheet and behaviour script from `/tmp/c_style.txt` and `/tmp/c_script.txt` —
**neither was ever bundled in `_build/`**, despite the README claiming all build scripts live there.
This is why the CSS and the generated markup were free to drift apart: nobody could load them
together. Both templates are now bundled in `_build/`, and the builder resolves `_build/` first with
a `/tmp` fallback.

#### Stale counts on the Codex hub

The guide count has now gone stale **four times**: `313` → `253` → `218` → `220`. The hub showed
`218` in its headline stat and two different wrong numbers in two placeholders, against 364 actual
guide pages. Headline stat set to the true **364**; **the numbers are removed from both placeholders
entirely** ("Search the guides…", "Search all guides…") so there is nothing left to re-sync.

#### TWO NEW STANDING CHECKS + ONE METRIC — now 17 checks

Everything above passed all 15 checks because **nothing ever looked inside an inline event
attribute**. `rendercheck` ran `node --check` on `<script>` blocks only; `onclick="..."` was never
parsed, so 1,560 Python booleans were invisible.

| Check | Catches |
|---|---|
| **Inline handler errors** | inline event attributes that do not parse as JS, and top-level handlers called but never defined |
| **Inline-hidden content** | `style="display:none"` on `.quiz-body` / `.track-panel` / `.lane-section` / `.tab-panel` — inline always beats the class |
| *[metric]* stale stamps | `dateModified` or `Verified <month year>` more than 4 months behind the clock — currently **107** |

Implementation note: the undefined-handler rule must match **top-level calls only**
(`^\s*(?:return\s+)?name\(`). A naive `\b\w+\(` match flags `document.getElementById`,
`navigator.clipboard.writeText` and `rgba(` inside style strings — 218 false positives on the first
run, 1 true positive after tightening.

**Verification this session:** 851 pages · **17/17 at zero** · linkcheck 0 · 2,295 `<script>` blocks,
**10,675 inline handlers** and 1,801 JSON-LD blocks all parsing clean · quiz behaviour tested against
a DOM stub.

**The lesson, stated plainly:** a check that only inspects `<script>` tags gives false confidence
about a page whose behaviour lives in attributes. Three of these four bugs were shipped by a
generator, and the fourth was a builder that could not be run at all. **Screenshots from a real
browser found in one minute what fifteen automated checks had missed for months.** Look at the site.

---

### Session 47 — BUILD SHEET 04: AML & Compliance (DONE, 13 Sep 2026)

`/fintech-ai/aml-compliance/build-sheet/` — 6,561 words, 4 code blocks, 1 registry.
Linked from the top of the AML module in the same pattern as 01–03. Site 850 → **851**.

**Three corrections to what this file previously recorded.** All from the primary source
(OFSI Penalty Publication Notice, published 26 Jan 2026) rather than secondary coverage:

1. **The Bank of Scotland fine did NOT turn entirely on the list-enrichment decision.** There were
   **eight aggravating factors** and one mitigating. Enrichment (case factor E) was one. OFSI states
   the breach may have been prevented by resolving **either** of two issues — the engine could not
   reconcile the character changes, **or** the list lacked enhancement. Either alone was sufficient.
2. **The bigger failure was escalation, not detection.** A PEP review on 20 Feb 2023 *correctly*
   identified the customer as designated. Human error recorded them as delisted from both the UK and
   EU lists when only the EU listing had gone, and there was no explicit instruction to escalate a
   potential sanctions connection to a sanctions team. **£75,000 of the £76,000 credited arrived in
   the 20–24 Feb window — after a human already had the right answer.** The page leads on this.
3. Numbers for the record: £77,383.39 across 24 payments · Reg 11 and Reg 12 · statutory max
   £1,000,000 · pre-discount £320,000 · Notice of Intention £175,000 (28 Aug 2025) revised to
   £160,000 (10 Nov 2025) after representations · full 50% voluntary disclosure discount ·
   strict liability under s.146 PACA 2017 · assessed "serious", not "most serious".

**THE INDIA GAP — the largest finding of the session.** The AML module's registry lists OFAC, UN,
EU, UK OFSI, OpenSanctions and commercial providers. **None of those is legally binding on an Indian
reporting entity.** The binding set is:

| List | Basis |
|---|---|
| UNSC consolidated (1267 / 1988 / 1718 and successors) | UAPA 1967 **Section 51A** |
| **UAPA Schedules 1 and 4** | MHA domestic designations — separate from the UN lists, equally binding |
| WMD Act 2005 **Section 12A** list | MoF Order dated 30 Jan 2023 |

OFAC / EU / UK bind through correspondent banking, USD clearing and counterparty contract — not
Indian statute. Screen them anyway; the point is that **the consequence of a hit differs**.

**The mechanics** (UAPA Order 2 Feb 2021, amended 22 Apr 2024; RBI MD on KYC Section 51, WMD in
Section 52, nodal-officer list in Section 54):

1. MEA → regulators, FIU-IND, MHA → you. Daily verification of the customer base is the expectation.
2. On a match, **within 24 hours** inform: Joint Secretary (IS-I) MHA · UAPA nodal officer of the
   **state/UT where the account is held** · your regulator's UAPA nodal officer · FIU-IND.
3. Match beyond doubt → prevent transactions, under intimation.
4. MHA causes verification via state police / central agencies. If confirmed, a **s.51A order issues
   within 24 hours of that verification**, without prior notice to the customer.
5. File an STR as well — the sanctions report does not discharge the PMLA duty.
6. Delisting requests → **Joint Secretary (CTCR), MHA**. Not RBI, not the sponsor bank.
7. Unfreezing: if an order cannot be passed within **15 working days**, the nodal officer informs
   the applicant.

**Architectural consequence, now the module's structural fact:** in India **the freeze is a legal
order, not a product decision.** Build to detect, report, restrict and act on instruction — with an
unfreeze path. Same shape as the fraud module's lien guidance.

**Findings worth carrying forward (Verified September 2026):**

1. **OFAC SLS is a file service, not a screening API.** Free, no auth, no rate limit, no SLA, no
   webhooks. It returns **403 with no body if the User-Agent header is missing** — undocumented, and
   it looks exactly like an outage.
2. **The legacy flat-file series is FOUR files.** `SDN.CSV` is primary names only. Aliases —
   every transliteration variant — are in **`ALT.CSV`**, joined on `ent_num`. Plus `ADD.CSV` and
   `SDN_COMMENTS.CSV` (remarks past the 1,000-char cap, where passport and tax IDs land). OFAC's own
   tutorial warns about this. **Screening against SDN.CSV alone is structurally the Bank of Scotland
   failure.** Advanced XML avoids the join entirely.
3. **Filenames change without notice** — discover from `GET /sanctions-lists`, never hardcode.
   Other useful endpoints: `/entities`, `/changes/latest`, `/changes/history/{y}/{m}/{d}`, `/alive`.
4. **OpenSanctions licensing trap** (same shape as Surya in Module 01). Data is **CC BY-NC 4.0** —
   a fintech screening its own customers **is commercial use** and needs a licence (internal-financial
   / internal-other / reseller tiers). The `yente` server software is genuinely free; the **data** is
   what you licence. Found in diligence far more often than in evaluation.
5. **OpenSanctions `/match` bills logical queries, not HTTP requests.** A batch of 10 entities in one
   call costs 10. Only HTTP 200 is billed. ≈ **€0.10/call**, volume pricing above ~20,000/month.
   Self-hosting is the cost ceiling — but the licence is the price of the house, not the cost of
   living in it (Elasticsearch, memory, upgrades).
6. **The Fed paper says more than we quoted.** Allen & Hatfield, **FEDS 2025-092**: LLMs cut false
   positives ~92% and raised detection ~11% vs the best fuzzy baseline — **and were on average over
   four orders of magnitude slower.** The authors' own recommendation is a **cascade** (exact/fuzzy
   for easy cases, escalate only uncertain ones); their cascade ran ~2x faster than pure LLM at
   comparable accuracy. They also split by process: **high-velocity payment screening needs the
   cascade; onboarding CDD and lending can lean on models much harder.** Our audit position is
   unchanged — keep **alert generation deterministic** — but the reasoning is now latency + process,
   not only auditability.
7. **Two more open-source licence traps.** **Marble = Elastic Licence V2** — may not be provided to
   third parties as a hosted or managed service, which is *exactly* the BaaS/PSP case. **Jube =
   AGPLv3** — network copyleft. Tazama is Apache-2.0 and clean. Also: Marble's OSS build needs a real
   **Firebase auth app** in production (emulator only works locally) — an external dependency with a
   data-residency question inside an otherwise self-hosted stack.
8. **CTR is a calendar-month aggregate, not a per-transaction test.** Cash above ₹10 lakh **summed
   across the month**, including connected transactions. A rule written as `amount > 10 lakh` runs
   cleanly for years, throws no errors and silently under-files throughout. Aggregate in **IST** —
   UTC month boundaries push 5.5 hours into the wrong reporting month every month.
9. **The STR clock starts at "forming suspicion" — make that a stored, immutable timestamp.** If the
   case system records only the filing date there is no defensible answer to "when was suspicion
   formed". Delay is counted **per day** under PMLA.
10. **Normalise the pricing unit before comparing any quote.** Four units in play: per screen · per
    monitored entity · per seat · **per monitoring scan**. The last is the trap — one vendor charges
    ~$0.08 per monitoring scan *on top of* verification; daily re-screening is **365× the per-scan
    rate per customer per year** and does not appear on the pricing page. Other post-signature lines:
    sandbox calls billed at production rates, minimum monthly volumes, per-list add-on fees, and
    sanctions/PEP/adverse-media charged as three products.
11. **Enforcement reality in India.** PMLA **s.13 is ₹10,000–₹1,00,000 _per failure_** — trivial
    until multiplied. Actuals: Paytm Payments Bank **₹5.49 cr** · Binance **₹18.82 cr** · Bybit
    **₹9.27 cr** · Union Bank **₹54 lakh** · PayPal **~₹96 lakh** (failure to register). FIU-IND can
    also direct **MeitY to block URLs and delist apps** — far heavier than the fine for a consumer
    fintech. Registering after enforcement does **not** extinguish prior liability. The penalties land
    on **failure to file, diligence and record-keeping**, not on weak detection software.
12. **Coverage is the least useful vendor metric.** Everyone covers OFAC/UN/EU/UK — those are free.
    What you buy commercially is **alias density and identifier enrichment on the same entities**.
    Demand a trial on *your own* customer file: a provider strong on Russian/Iranian transliteration
    may be thin on Indian and Gulf name forms.

**Pricing captured (Verified September 2026):** official feeds **free** (cost is the pipeline) ·
OpenSanctions hosted ≈ **€0.10/call** · screening API entry ≈ **$99–120/mo** (ComplyAdvantage starter
≈ $99.99 — *confirm the entity allowance, sources disagree and it decides the price*) · Sanction
Scanner ≈ **€990/mo** for ~100 entities · Sandbar from ≈ **$500/mo** incl. OpenSanctions data ·
full AML platform mid-market ≈ **$30k–100k/yr** · enterprise suites ≈ **$100k–800k+/yr** ·
enriched list data quote-only. **The analyst queue is usually the largest line and nobody models it.**

**FIU-IND filing, confirmed:** FINGate 2.0 (successor interface to FINnet). CTR — cash > ₹10 lakh
per calendar month, by the **15th of the following month**. STR — no threshold, **includes attempted
transactions**, within **7 working days** of forming suspicion. CBWTR — cross-border wire transfers
above **₹5 lakh**. CCR, NTR per schedule. Records **5 years**. Principal Officer and Designated
Director must be two different people.

---

### SESSION 47 — TWO BUILDERS PATCHED (date drift)

Found while writing the Verified stamp: **the site was four months stale on its own timestamps.**

- **545 pages** carried `"dateModified": "2026-05-22"` or earlier; **56 registry blocks** said
  "Verified May 2026" or "Verified April 2026". The date was 13 September.
- Cause: `fintech_builder.py` hardcoded `'May 2026'` and `'2026-05-22'` in **three** places, and
  `rebuild_infra.py` hardcoded `'2026-05-22'` in sitemap `lastmod`, the `llms-full.txt` header and
  `manifest.last_updated`. Every page built or rebuilt after May shipped pre-aged.

**Patched, same session** (Rule 4 — fourth builder-patch in five sessions, the rule is holding):

```python
# fintech_builder.py — set once per session
VERIFIED = 'September 2026'   # hero meta-tag + registry() default
DATEMOD  = '2026-09-13'       # JSON-LD dateModified

# rebuild_infra.py — derived, nothing to set
TODAY = datetime.date.today().isoformat()
```

Documented in `_build/README.md` under "Dates — set these every session".

**Note the pattern, because it will recur:** anything hardcoded in a builder becomes a silent defect
the moment the calendar moves. None of the 15 standing checks caught this — a stale date is valid
HTML, valid JSON-LD and a working page.

**SUGGESTED 16th CHECK (not yet built):** flag any `dateModified` or `Verified <month year>` stamp
more than N months behind the system clock. Would have caught 545 + 56 instances. Worth adding in
Session 48 before the drift rebuilds.

---

### SESSION 31b — INCOMPLETE-CONTENT SWEEP (22 May 2026)

Triggered by a direct question: "which things on the site are greyed out and not complete?"
The answer was worse than expected, and the audit had not been catching it.

**Found and fixed:**

| Issue | Detail |
|---|---|
| **Courses hub corrupted** | All 8 courses added in Session 29 were injected into `<head>` and were **invisible on the page**. The hub showed 60 courses, not 68. |
| **8 pages with `</html>` before the script block** | Voice-audio tool pages. Browsers tolerate it; it is invalid HTML. |
| **10 orphan pages** | Section hubs built in Sessions 24–25 that nothing linked to: `/codex/seo/{technical,on-page,local}/`, `/codex/sem/google-ads/{shopping,display,youtube,advanced}/`, `/codex/paid-advertising/facebook-instagram/`, `/codex/ecommerce/subscription-commerce/`, `/ai-atlas/use-cases/studying/`. |
| **Stale hub title** | Said "60 Free Courses" after reaching 68. |

**Root cause of the courses corruption.** Session 29 used
`h.find('<div class="course-grid" id="courses-marketing">')` — but Session 25 had rebuilt that hub
using `data-section="marketing"` instead of `id=`. `find()` returned `-1`, and `h[:-1+len(needle)]`
silently sliced to a position inside `<head>`.

**NEVER use `str.find()` for insertion without checking the result.** Pattern to use:

```python
i = h.find(anchor)
assert i != -1, f"anchor not found: {anchor}"
```

Better still: rebuild hub listings from the filesystem rather than string-inserting into them.
`courses/index.html` is now regenerated by scanning `courses/*/index.html`.

**TWO NEW STANDING AUDIT CHECKS** — `/tmp/structcheck.py`, folded into `/tmp/audit.py`:

- **HTML structure errors** — content inside `<head>`, duplicate `<head>`/`<body>`/`</html>`/`<title>`,
  stray `<a` fragments, anchor open/close mismatch
- **Orphan pages** — any page with zero inbound internal links

Both must read 0. Every content-carrying check now sits in one table:

```
Broken internal links · HTML structure errors · Orphan pages · Empty directories
Duplicate flat/dir pages · Duplicate titles · Duplicate descriptions · Invalid JSON-LD
Broken search inputs · Missing meta description · Meta >165 · Titles >65
Missing GA4 · Missing og:image
```

**Confirmed NOT incomplete** (checked, these are fine):
- No "coming soon" course cards remain — all 68 are live with 15 lessons each
- The single "coming soon" phrase left on the site is inside the MVP marketing guide, describing
  fake-door testing. It is content, not a stub.
- Greyed dashed cards on `/fintech-ai/` are the 9 modules for Sessions 32–40. Deliberate,
  non-clickable, and converted to links as each ships.

---

## FINTECH AI SECTION — SESSIONS 31 to 42

A fifth top-level section at `/fintech-ai/`. Nine problem modules plus spine pages, built to
implementation depth: working code, tool registries, and copy buttons on every code and prompt block.

### Session 31 — page type + spine (DONE, 22 May 2026)
- `/fintech-ai/` — hub with nine module cards
- `/fintech-ai/why-every-fintech-ai-looks-the-same/` — the differentiation argument
- `/fintech-ai/regulation-india/` — RBI, V-CIP, Account Aggregator, digital lending, DPDP
- `/fintech-ai/regulation-global/` — EU AI Act, GDPR Art.22, FCA, US fair lending, MAS
- Added Fintech AI to nav on homepage, Codex, AI Atlas and Courses hubs
- `og-fintech.png` generated

### Session 32 — Module 01: Identity & Onboarding (DONE)

`/fintech-ai/identity-onboarding/` — 16 sections, 13 copy-able code/prompt blocks, 3 registries.
Hub card converted from dashed div to live link.

**Structure that all remaining modules should follow:**
- **Beginner (4 sections):** what the problem is · why it is hard · what AI can and cannot do (as a table) · the one structural fact that decides architecture
- **Intermediate (7):** the pipeline diagram · stage-by-stage with working code · tool comparison table with honest breaking points · the counter-intuitive finding · validation code · tool registry (direct/indirect/oss) · a specification prompt
- **Advanced (5):** thresholds and routing code · how it gets attacked · cost model · audit log schema · where this module ends and others begin

**Research findings worth carrying forward (verified May 2026, re-verify before reuse):**

1. **Engine choice matters less than assumed.** A 2026 controlled benchmark on identical receipt
   data found the best traditional engine (docTR) essentially tied the best VLM (Surya2) on character
   error rate — VLMs are *not* inherently more accurate on clean printed text. More importantly,
   once an LLM post-processor was added, **six of eight engines converged into the same field-accuracy
   band**. Spend effort on the quality gate before OCR and validation after it, not on engine selection.
2. **VLM OCR fails invisibly.** Classic OCR returns garbage on failure; a VLM returns a fluent invented
   name. Every VLM-extracted field must be grounded against the raw detected text. Code for this is in
   the module.
3. **Surya licensing trap.** Code is GPL-3.0 but the model is under a licence that is free for research
   and companies under a revenue threshold, requiring a commercial licence above it. Flag this anywhere
   Surya is recommended.
4. **Aadhaar eKYC is indirect-only.** Access requires a UIDAI-licensed KUA/KSA or aggregator; direct
   access needs RBI authorisation. This is the canonical example of why the registry marks
   direct / indirect / oss.
5. **RBI Master Direction update, 28 Nov 2025** made deepfake/liveness maturity and regional-language
   document handling decisive evaluation criteria for Indian KYC vendors.
6. **India-tuned face models materially outperform global ones** on Indian skin tones, low light and
   low-cost Android cameras (HyperVerge is the commonly cited example).
7. **Camera injection is the under-covered attack.** Virtual camera feeds bypass both passive and active
   liveness entirely. Device attestation is the control; web capture is structurally weaker than native.
8. **Human review is usually the largest cost line**, not API fees — and nobody models it.

**Pricing note:** this market is almost entirely quote-only. Hypersign publishes a public rate card
(~₹6/verification, ~₹15 full journey with face match at time of writing) which is useful mainly as a
negotiating benchmark.

### Session 33 — Module 02: Credit & Underwriting (DONE)

`/fintech-ai/credit-underwriting/` — 17 sections, 11 code/prompt blocks, 3 registries.

**Research findings worth carrying forward (verified May 2026):**

1. **Reason codes must be deterministic and reproducible.** Same applicant, same data, same model
   version → identical reason ranking. If it varies, the audit trail fails under examination. Sort
   keys fully specified, ties broken alphabetically, rounding pinned. A `determinism_hash` on the
   decision record turns this from a claim into a test.
2. **Regulators distinguish post-hoc explanation from the actual decision path.** If documented
   process says a linear scorecard decides but a neural net is deciding and SHAP describes it
   afterwards, that discrepancy is itself a compliance failure. CFPB has stated generic reason codes
   are insufficient for AI/ML decisions.
3. **SHAP is less stable than vendor material suggests.** Retraining or small input perturbation can
   reorder contributions, especially among correlated features. Mitigate by grouping aggressively,
   pinning model version to the decision, using TreeSHAP-exact, and asserting reproducibility in CI.
4. **Reject inference** — you only observe outcomes for approved applicants, so naive training
   reproduces existing policy including its errors. The random approval slice is the only unbiased
   fix and should be budgeted as a data acquisition cost.
5. **India: ~50 crore working-age adults have no bureau score.** Thin-file ≠ low-score. Thin file is
   an *unknown* borrower; low score is a *known bad* one. Conflating them is the largest source of
   unnecessary rejection.
6. **Four licensed Indian bureaus:** TransUnion CIBIL, Experian, Equifax, CRIF High Mark. All
   indirect access — membership requires being a regulated lender or going through one.
7. **Six underwriting paths Indian lenders ship:** bureau pull · AA bank statement analysis
   (the thin-file primary signal) · GST returns GSTR-1/3B (MSME unlock) · EPFO (employer-confirmed
   salaried income) · UPI velocity and MCC spread · utility/telecom regularity.
8. **Strongest alt-data signal is bounce/return history**, then FOIR, then income *stability* over
   income level, then surplus ratio, then recent credit-seeking bursts.
9. **Data cost per APPROVAL, not per application.** At 20% approval, ₹60/application = ₹300/approved
   loan. Declining cheaply is worth as much as approving accurately.
10. **Feature null rates are a silent killer.** When a provider degrades and returns nulls, tree
    models route down the default branch and keep scoring confidently. Monitor daily.

**Architecture recommendation the module makes:** hybrid — model produces a probability, an explicit
versioned policy layer turns probability + hard rules + affordability into the decision. Far easier to
defend than "the model said no", and it makes reason generation rest on policy rather than on SHAP
stability.

### Session 34 — Module 03: Fraud & Risk (DONE)

`/fintech-ai/fraud-risk/` — 16 sections, 11 code/prompt blocks, 3 registries.

**Research findings worth carrying forward (verified May 2026):**

1. **Only ₹0.57 crore of ₹2,294.79 crore lost to Indian cyber fraud in 2022 was recovered** (~0.25%).
   Parliamentary Standing Committee figure. The implication drives the whole module: prevention is
   the only thing that works; recovery investment is close to worthless.
2. **India's mule economy is the dominant fraud shape.** 2.47M Layer-1 mule accounts flagged
   nationally as of early 2026; 524,121 suspected mule accounts/VPAs flagged in March 2026 alone.
   Funds hop 4–6 times across UPI-linked accounts before withdrawal. Key signal: dormant account
   suddenly receiving and forwarding within minutes.
3. **National infrastructure to know:** MuleHunter.AI (RBI, ~4.7 lakh mules detected, live across
   dozens of banks) · DPIP with NPCI (cross-bank real-time fraud signal sharing) · CPFIR (fraud
   registry since 2024) · IDPIC (Section 8 company, incorporated Oct 2025) · I4C Suspect Registry
   with RBIH · .bank.in/.fin.in restricted domains.
4. **RBI April 2026 discussion paper** proposed transaction lag, customer kill switch, trusted-person
   auth and a cap on flows through flagged accounts. Proposals, consultation open — verify status.
5. **Courts are pushing back on account freezing.** Andhra Pradesh HC ruled a merchant's account
   cannot be frozen merely because a fraudster used it for a small UPI payment; similar rulings in
   Kerala and Rajasthan. Module treats freezing as a legal action with a technical trigger, and
   recommends lien-marking the amount rather than freezing the account.
6. **GNN + gradient-boosted ensembles** catch meaningfully more fraud than either alone; research
   reports ~33% false-positive reduction vs GNN baselines. Recommended progression: velocity features
   → hand-built graph features → GNN embeddings as extra columns into the existing tree model
   (keeps tree explainability).
7. **Latency budget:** total authorisation window 100–300ms; sub-50ms scoring at p99 is achievable.
   Feature assembly is the usual bottleneck, not inference.
8. **Training-serving skew** is the silent killer — compute features once in shared code.
9. **Step up, do not block.** RBI guidance and commercial incentive agree: step-up auth on high-risk
   rather than outright decline. Customers who hit a false decline are significantly more likely to
   churn within 90 days.
10. **APP scams remain genuinely unsolved.** Real customer, real device, real credentials, real
    intent — every signal says legitimate because it is. Module says so plainly rather than selling
    a tool as the answer.

**Metric guidance in the module:** report value-weighted (₹ fraud prevented / ₹ genuine volume
disrupted), precision at the block threshold, and analyst-hours per fraud caught. Never accuracy —
at a 0.1% fraud rate, predicting "not fraud" always scores 99.9%.

### Session 35 — Module 04: AML & Compliance (DONE)

`/fintech-ai/aml-compliance/` — 15 sections, 10 code/prompt blocks, 3 registries.

**Research findings worth carrying forward (verified May 2026):**

1. **Bank of Scotland / OFSI, November 2025 — £160,000 fine.** The anchor case study of the module.
   A UK-designated Russian individual opened an account; the passport name differed from the OFSI
   list entry by one changed character and one added character in the forename, a missing middle
   name, and one changed character in the surname — all common Russian-to-English transliteration
   equivalents. The individual was on the list. The system was configured correctly and operated as
   configured. No alert fired; manual identification came 18 days later. Two systemic failures:
   the system could not reconcile character changes, and the bank had not enriched its sanctions
   list with a commercial provider — **despite having done so for PEP screening, which did alert.**
2. **The precision paradox.** Loosening thresholds raises recall and destroys precision; tightening
   does the reverse. No setting gives both. FPR below ~2–3% generally produces unacceptable false
   negatives in high-risk jurisdictions. Be suspicious of any vendor claiming near-zero FPs.
3. **LLM evidence is strong; deployment advice is restrictive.** Comparative study found LLM matching
   cut false positives ~92% and raised detection ~11% vs the best fuzzy baseline, at higher compute
   cost; Fed research (Allen & Hatfield, 2025) reached a consistent conclusion. **But: never use an
   LLM as the primary screen** — non-deterministic and not auditable in the sense a regulator means.
   Deterministic methods raise alerts; LLMs work on alerts that already exist (triage, adverse media
   summarisation, rationale and SAR drafting).
4. **Layered cascade:** normalise → exact → fuzzy → phonetic (Double Metaphone handles
   transliteration best) → embedding → context scoring → LLM enrichment.
5. **Missing data must not count as a mismatch.** Sanctions entries routinely lack DOB or national ID.
   Treating absence as disconfirmation systematically discards real matches.
6. **OFAC:** use the official Consolidated Sanctions List API / weekly XML-CSV. Scraping the website
   breaches terms and fails audit expectations.
7. **India / FIU-IND under PMLA 2002:** register on FINnet 2.0; five reports — CTR (cash >₹10 lakh,
   monthly by 15th) · **STR (no monetary threshold, within 7 working days of forming suspicion,
   delay counted per day)** · CCR · NTR · CBWTR. Records retained 5 years.
8. **Principal Officer and Designated Director must be two different people.** Mapping both to one
   individual is a common, avoidable mistake.
9. **Tipping off is an offence** — constrains product design directly: no customer-visible status,
   no automated notification tied to an STR, agents must not be able to see the reason.
10. **Threshold sensitivity analysis is a regulatory expectation**, not an engineering nicety. Set
    minimum acceptable recall as a signed-off policy decision first, then minimise alert volume
    within that constraint, and record the analysis, date, test-set version and approver.

**Examination reality noted in the module:** most findings are documentation failures, not technology
failures. Threshold rationale, list-enrichment decisions, consistency across programmes, alert
backlog, filing timeliness, evidence of testing, and change control.

### Session 46 — BUILD SHEET 03: Fraud & Risk (DONE)

`/fintech-ai/fraud-risk/build-sheet/` — linked from the top of the module.

**The market splits into three categories, and most confused procurement compares across them:**

| Category | Gives you | Examples |
|---|---|---|
| Scoring platforms | A decision — approve / review / block | Sift, Kount, Forter, Feedzai, Sardine |
| Signal layers | Evidence for a decision you make | Fingerprint, SEON, IPQualityScore |
| Guarantee models | They underwrite the loss | Signifyd, Riskified |

A working stack needs **one from at least two categories**. Key blindness: **server-side scoring
platforms and consortium data cannot see AI-agent activity**, because the automation happens
client-side before any request reaches the backend.

**Pricing tiers (Verified May 2026):**
- Signal layers: **$99–$500/month**, usually with free tiers. Fingerprint ~1,000 calls/month free.
- SEON Starter: ~$699/month for ~2,500 API calls and 50 rules; case management and AML on higher
  tiers; no free tier, sales-led.
- Scoring platforms mid-market: **$2,000–$10,000/month**
- Enterprise: from **$50,000/year**, six-figure floors common
- Guarantee models: **0.6–1.5% of protected GMV**
- **Get all-in TCO before signing** — implementation, custom rules and dispute handling frequently
  double the invoice.

**How to rank vendors, stated in the page:** NOT on claimed model accuracy — no vendor lets you test
it independently and it is produced on their population. Rank on **explainability · evidence
readiness for chargeback disputes · false-positive economics · browser-layer visibility.**

**Gotchas documented:**
- **Always resolve the device requestId server-side.** A client-posted visitorId is an
  attacker-supplied string. The single most common device-intelligence integration error.
- **`confidence` is a property of the identification, not of risk.** Low confidence means "unsure
  it is the same device", not "this device is suspicious".
- **`firstSeenAt` is the highest-value field and the least used.** A device first seen 90 seconds ago
  applying for credit is a different proposition from one known for two years.
- **Shared device is not fraud in India** — families, shared phones, cyber cafes. Use as a graph
  edge and a review trigger, never a block.
- **Always TTL every Redis velocity key**, or it grows until it evicts something you needed, at peak.
- **The ratio matters more than the count** — store a per-customer baseline.
- **Beneficiary velocity across *different* senders is the mule signal.** Most teams count per-sender
  and miss it entirely.
- **Graph queries belong in batch, not the request path** — too slow for a <50ms budget. Precompute
  as columns for the real-time tree model.

**Build order recommended:** velocity counters first (a week of work, catches a surprising share of
the first wave) → hand-written graph features → model → GNN embeddings only if volume justifies.

**Stated plainly:** start lean deliberately. Buying a platform before you know your own fraud
patterns means tuning someone else's thresholds against a threat you have not characterised.

**Question to ask the sponsor bank that matters more than it sounds:** what is the unfreeze path and
how long does it take? Courts have been pushing back on account freezing; if the sponsor freezes
whole accounts with no fast unfreeze, that becomes your complaint and your conduct problem.

### Session 45 — BUILD SHEET 02: Credit & Underwriting (DONE)

`/fintech-ai/credit-underwriting/build-sheet/` — linked from the top of the module.

**Research findings (Verified May 2026 — negotiated pricing, re-verify):**

| Item | Typical range |
|---|---|
| CIBIL score only | **₹5–20 per pull** — cheapest surface, most used for instant pre-approval |
| CIBIL consumer full report | ₹15–50 low volume · ₹5–15 high-volume committed |
| Commercial / MSME report | ₹100–500 per pull |
| Mortgage check | ₹50–200 per pull |
| **Aggregator markup** | **+₹2–15 above the bureau rate** per pull |
| Bank statement analysis | ₹1–50 per statement (low end = extraction, high end = forensic fraud) |
| AA connectivity | Often a **premium add-on**, not included — confirm at contract |

- **No public rate card.** Bureau pricing is negotiated on signing a member agreement; the full-stack
  vendors run enterprise sales only — no self-serve sandbox, no public API key, no per-call page.
- **Two layers, routinely conflated:** Credit Information Companies (CIBIL, Experian, Equifax, CRIF
  High Mark) hold the data under CICRA 2005; aggregators/TSPs (Perfios — which absorbed Karza in
  2022 — IDfy, which acquired Signzy) are the integration plumbing. Direct bureau access requires
  being an **RBI-registered Credit Institution**.
- **Same split on AA:** licensed NBFC-AAs (Finvu, Setu, OneMoney, CAMSfinserv) move the data; TSPs
  consume it for FIU clients. The AA rail crossed ~252.9M linked accounts in 2026.
- **The obligation people miss:** under the RBI Master Direction on Credit Information Reporting, a
  regulated lender must **submit data to** as well as pull from at least one licensed CIC. Reporting
  is a build item, not a later problem, and getting it wrong affects real borrowers' scores.

**Gotchas documented:**
- **`match_confidence`** — a "partial" bureau match may be a different person with a similar name.
  Never decision on a partial match.
- **A bureau pull is itself a recorded enquiry.** Speculative pulls and testing against real PANs
  leave marks on real people's files. Sandbox for development; one pull per application.
- **Score version matters** — cut-offs tuned on one score version are invalid on another. Pin it.
- **"No hit" is not a low score.** It is a thin file and belongs on the alt-data path.
- **AA step-2 drop-off is 30–50%** and is mostly a UX problem. Instrument it per screen. The user may
  also share one account of five — check account count before scoring.
- **`data_life` ≠ `consent_expiry`** — one is how long you may keep it, the other how long you may
  fetch. DPDP purpose limitation applies to both.
- **Tampering flags apply to uploaded PDFs only.** AA-sourced data comes structured from the bank
  and bypasses the risk — the main reason to prefer AA over upload.
- **`scale_pos_weight` changes the shape of predicted probabilities.** Treating the output as a
  calibrated PD after setting it means your cut-offs mean something other than you think.
- **Never split credit data randomly** — time-based splits only, or the model leaks the future.

**The recommended build, stated plainly in the page:** buy the plumbing, own the model. The plumbing
is commodity; the repayment history you accumulate is the only thing competitors cannot buy. The
expensive full-stack build accumulates that history inside someone else's system — which is exactly
the asset that was meant to become the moat.

### Session 44 — BUILD SHEET 01: Identity & Onboarding (DONE)

`/fintech-ai/identity-onboarding/build-sheet/` — linked from the top of the module.
**This is the template for Build Sheets 02–09.**

**Structure (follow exactly):**
1. **How to read this** + the jobs table (what each job needs, can you skip it)
2. **Raw materials** — one table per category: Material · What it does · Verify at (official link)
3. **How to use each one** — per tool: what it is for · first working call as copy-able code ·
   **what to check, as an inline checklist inside the code** · the gotcha nobody documents
4. **Cost per unit** — in a `registry`-style block with a **Verified <date>** stamp
5. **Best combinations** + combinations that conflict
6. **Three recommended builds** — strong & expensive / strong & reasonable (marked as the default) /
   strong & lean, each with: build, use when, cost shape, trade
7. **What next** — the modules this feeds, plus the governance reminder

**Builder patched again** — `/tmp/fintech_builder.py` now emits the Session 43 consolidated pattern:
depth bands inside each lane, one continuous TOC with depth headings and dots, no depth buttons,
`.lane-section{display:block}`. Third builder-patch in three sessions; the rule is holding.

**Pricing findings captured (Verified May 2026, re-verify before reuse):**
- **Plain OCR is a commodity** — AWS, Google and Azure all ≈$1.50/1,000 pages, matching to the cent.
  Falls to ≈$0.60 at volume. **Price is not a reason to choose between them.**
- **The structured-extraction tier is where cost lives** — a 7x to 30x jump. Textract Tables ≈$15,
  Forms ≈$50, Forms+Tables+Queries ≈$65–70 per 1,000. Azure/Google custom extraction ≈$30.
  Azure classifier ≈$3 (cheapest). Textract **AnalyzeID ≈$10–25** is the right API for ID cards —
  using AnalyzeDocument instead costs several times more for a worse result.
- **Features stack; one document hits several meters.** Classifier (~$3) + custom extraction (~$30)
  = the real per-document cost is the sum of models that fire. *The most common estimating mistake.*
- **Google bills ~$0.05/hour per deployed custom processor version** (~$438/yr) whether or not it
  gets traffic. Azure charges no idle hosting fee.
- **Multi-page bills page-by-page** — a 40-page file is 40 billable pages even if you need page one.
- **Azure free tier caps at 2 pages per document** — silently truncates and returns a clean-looking
  result from an incomplete read.

**Gotchas documented that are not in any vendor doc:**
- Textract confidence is **0–100**; Azure and most others are **0–1**. Teams mix them and set a
  threshold of 0.95 that passes everything.
- Azure: check `doc_type` **first** — if it classified a PAN card as a passport, every field mapping
  below it is wrong.
- PaddleOCR downloads models on first run; in a no-egress container that fails at startup, not build.
  Bake models into the image.
- **A successful KYC verification response means the lookup succeeded, not that the person is who
  they claim.** Name matching between what you submitted and what came back is your job, and it is
  where fraud passes through.
- If a liveness vendor lets you POST an arbitrary image, that is not liveness — it is face matching
  on a file. Device attestation is what stops camera injection.

### Session 43 — LANE CONSOLIDATION (DONE)

**Depth tabs removed site-wide. 209 pages converted to one continuous page.**

Rationale: three-lane tabs hid two-thirds of every page. A reader on Beginner had no signal that
3,000 more words existed — a 4,300-word module read as a 1,400-word one. Tabs are now **signposting,
not a filter.**

| Section | Pages | Result |
|---|---|---|
| Fintech AI | 17 | Continuous page · merged TOC in the left rail with depth dots |
| AI Atlas | 124 | Sidebar moved LEFT (`order:-1`, grid `260px 1fr`) · TOC card added · lane tabs removed |
| Courses | 68 | Continuous page · rail tabs now scroll-to rather than switch |

**The pattern, now standard:**
```css
.lane-section{display:block}      /* or .track-panel — always visible */
.depth-band{...}                  /* inline Beginner/Intermediate/Advanced badge + note */
```
No `html.js` hiding. No tab filtering. Depth is legible; nothing is concealed.

### THREE BULK-EDIT FAILURES IN ONE SESSION — READ BEFORE ANY MASS EDIT

1. **Regex `.*?</div>` over-matched** on fintech pages — ate content, broke div balance.
2. **Same mistake repeated** on 115 of 124 AI Atlas pages minutes later.
3. **Global `h.replace('</button>','</a>')`** on courses replaced *every* button close on the page,
   not just the track tabs — broke all 68.

All three were caught by verification and restored from the previous zip. **Rules now:**

- **Never regex across nested HTML.** Use balanced extraction:
  ```python
  def bal(h,s):
      d=0
      for m in re.finditer(r'<div\b|</div>',h[s:]):
          d += 1 if m.group(0)=='<div' else -1
          if d==0: return s+m.end()
  ```
- **Never use a bare `str.replace` for a tag** that appears elsewhere on the page.
- **Verify div balance BEFORE writing**, not after — the consolidation scripts now compute the new
  body and skip the write if it would break.
- **Keep the previous zip.** All three recoveries came from `clarigital-v31.zip`.

### NEW STANDING CHECK — div balance

Added to `/tmp/structcheck.py`. It immediately exposed **25 pre-existing imbalances** that had been
invisible for the whole build:
- **22 AI Atlas tool pages** from Session 28 — `/tmp/tool_builder.py` emitted one extra `</div>` in
  the hero (`</div>\n</div>\n  </div>\n</section>`). **Builder patched.**
- 21 Codex pages with a dangling unclosed `<div class="wrap">`
- 4 others with surplus closes (one had 11)

All 847 pages now balance. Browsers auto-closed these, so nothing looked broken — which is exactly
why the check was worth adding.

### AGREED NEXT — the Build Sheet pattern (Sessions 44–52)

Each module gains: **raw materials** (every tool, name + official link for verification only) →
**how to use each one, on our page** (what you send, what comes back, what to check, first working
call, the undocumented gotcha, cost per unit) → **best combinations** → **recommended builds at three
grades** (strong & expensive / strong & reasonable / strong & lean) → **what next**.

Vendor links are for verifying our claims, not for learning. Everything is on our page.
Materials and pricing blocks carry a **Verified <date>** stamp, visually separate from the
instructions, so it is obvious which part has aged.

| Sessions | Scope |
|---|---|
| ~~44~~ | ~~Build Sheet 01 — Identity~~ — DONE |
| ~~45~~ | ~~Build Sheet 02 — Credit~~ — DONE |
| ~~46~~ | ~~Build Sheet 03 — Fraud~~ — DONE |
| ~~47~~ | ~~Build Sheet 04 — AML~~ — DONE |
| ~~48~~ | ~~Build infrastructure repair~~ — DONE |
| ~~49~~ | ~~Build Sheet 05 — Payments~~ — DONE |
| ~~50~~ | ~~Build Sheet 06 — Customer Ops~~ — DONE |
| ~~51~~ | ~~Build Sheet 07 — Wealth~~ — DONE |
| ~~52~~ | ~~Product Guide 01 — Document AI (NEW PAGE TYPE, prototype)~~ — DONE |
| ~~53~~ | ~~Site-wide navigation repair + check #18~~ — DONE |
| | **Full 42-session roadmap with QA cadence is above, under Session 54.** |

### Session 42 — Course migration + AI Finance rebuild (DONE) — FINTECH PROGRAMME COMPLETE

**1. `/courses/ai-finance/` rebuilt.** The old version was a placeholder — 13 of its 15 lessons
pointed at the same page (`/ai-atlas/agentic-ai/`). Replaced with a real 15-lesson course built on
the 13 fintech pages: 15 lessons, **15 unique targets**, all URL-verified.

**2. All 68 courses migrated to the sticky left rail.** Top tab bar → two-column layout with a
sticky rail, matching the fintech page type. Migration script pattern at `/tmp/migrate_courses.py`.

```css
.crs-layout{display:grid;grid-template-columns:232px minmax(0,1fr);gap:38px;align-items:start}
.crs-rail{position:sticky;top:72px;max-height:calc(100vh - 92px);overflow-y:auto}
.track-tabs{display:flex;flex-direction:column;gap:7px}   /* was a horizontal bar */
.track-panel{display:block;padding:0 0 32px}              /* visible without JS */
html.js .track-panel{display:none}
html.js .track-panel.active{display:block}
@media(max-width:900px){ .crs-layout{grid-template-columns:1fr} .track-tabs{flex-direction:row;flex-wrap:wrap} }
```

Markup: `<div class="crs-layout"><aside class="crs-rail">…tabs…</aside><main class="crs-main">…panels…</main></div>`

**Migration safety check that is worth reusing:** before wrapping a segment, assert `<div` and
`</div>` counts balance within it. Caught nothing this time, which is the point.

**3. Also fixed during migration**
- Malformed attribute `onclick="showTrack('advanced')")>` — a stray `)` before `>` on the advanced
  tab across the estate. Browsers tolerated it; it was still wrong.
- **`/tmp/course_builder_v3.py` was still emitting the pre-Session-36b markup** — beginner panel
  without `active`, intermediate and advanced with inline `display:none`, no `js` flag. Patched.
  It also never emitted `og:image`, and its title template ran to 80 characters. Both fixed.

**The recurring lesson, now three sessions running:** fixing pages without fixing the generator means
the next page regenerates the bug. Session 37 caught it in `fintech_builder.py`, this session caught
it in `course_builder_v3.py`. **When a render or metadata bug is found, patch the builder in the same
session.**

**4. Render check extended** — now also catches, on course pages: tracks hidden without JS, missing
`js` flag, the malformed `showTrack` attribute, and a missing `crs-layout` wrapper.

---

## FINTECH AI PROGRAMME — COMPLETE (Sessions 31–42)

| | |
|---|---|
| Pages | 17 (13 modules + spine + 4 playbook) |
| Words | ~52,000 |
| Copy-able code/prompt blocks | ~140 |
| Course | `/courses/ai-finance/`, 15 lessons |
| Site total | **847 pages** |

All 15 standing audit checks at zero.

### Session 41 — Build Playbook (DONE)

Four pages: `/fintech-ai/build-playbook/` (hub) · `licensing-and-access/` · `stack-selection/` ·
`go-live/`. Linked from the Fintech AI hub as a highlighted card.

**India licensing reference captured (verified May 2026 — verify before relying on it):**

| Licence | Minimum NOF | Notes |
|---|---|---|
| NBFC (standard / ICC) | **₹10 crore** | New applicants from inception; existing had until 31 Mar 2027 |
| NBFC-MFI | ₹5 crore | ₹7 crore in the North-East |
| NBFC-P2P | ₹2 crore | |
| NBFC-Account Aggregator | ₹2 crore | AA Directions 2025, notified 28 Nov 2025, replaced the 2016 Master Direction |
| Housing Finance Company | ₹20 crore | |
| Mortgage Guarantee | ₹100 crore | |
| Infrastructure Finance / IDF | ₹300 crore | |
| **Payment Aggregator** | **₹15 crore at application** | → ₹25 crore within 3 years, maintained permanently. PCI-DSS + data localisation. |

- **Timelines:** NBFC 3–6 months; PA 4–6 months, assuming complete documentation.
- **PA costs beyond capital:** ₹1–3 crore (infrastructure, certification, advisory, audits); total
  investment ~₹16–18 crore. 60+ entities held in-principle or final PA authorisation as of 2026.
- **Operating as a PA under an NBFC licence is not permitted.** Recurring, expensive misunderstanding.
- **Rejection causes:** MoA must list financial services as the **main** object, not ancillary ·
  ≥1/3 of directors with 10+ years in banking/financial services · NOF must be genuine promoter
  equity, not borrowed · clean director credit history · coherent business plan.
- **Portal:** applications go through RBI's online portal only — no walk-in or email route. Sources
  differ on which portal (COSMOS vs PRAVAAH); the module says to confirm the current channel rather
  than asserting one.
- **Feb 2026 draft** proposed exempting "Type I" NBFCs from registration — asset size <₹1,000 crore,
  no public funds, no direct customer interface. Draft at time of writing.
- **Change of control needs RBI prior written approval before it takes effect** (AA Directions 2025
  read with the shareholding directions) — a filing that sits between a founder and a priced round
  closing. Plan before the term sheet.

**The organising idea:** permission runs in **parallel** with the build, not after it. The most
common timeline failure is building for six months, then starting licence or partner conversations,
then waiting another six. The build was never the constraint.

**Data you cannot buy directly** (table in the module): Aadhaar eKYC, bureau data, AA bank statements,
CKYCR, GST, EPFO and UPI rails are all indirect. Only sanctions lists are freely available direct.

**Go-live gate:** a checklist where every line must be TRUE, not planned — permission, money, risk,
customer, evidence, operations. The two lines most often waved through are **kill switch exercised**
and **the concurrency test** (two simultaneous debits against a balance that can fund one). Both are
quick and both find real problems.

**Post-launch:** 30 = is it safe · 60 = is it right · 90 = is it a business. Never change thresholds
and increase volume in the same week.

### Session 40 — Module 09: Governance (DONE) — ALL NINE MODULES COMPLETE

`/fintech-ai/governance/` — 15 sections, 10 code/prompt blocks, 3 registries.
**Zero dashed "publishing shortly" cards remain on the hub.**

**Fintech AI section final state: 13 pages, 44,889 words, 118 copy-able code/prompt blocks.**
Module pages run 3,950–5,230 words each. This is the depth standard for the rest of the site.

**Research findings worth carrying forward (verified May 2026):**

1. **RBI FREE-AI Framework**, released 13 August 2025 by an RBI-constituted committee — *Framework
   for Responsible and Ethical Enablement of AI*. Seven "Sutras", 26 recommendations, six pillars:
   **Infrastructure · Policy · Capacity · Governance · Protection · Assurance.**
2. **RBI Draft Guidance on Regulatory Principles for Model Risk Management**, released
   **24 June 2026** for consultation (comments reportedly due 24 July 2026). **DRAFT at time of
   writing — verify before designing to any provision.** Scope is deliberately broad:
   - **11 categories of regulated entity** — commercial banks, NBFCs, payments banks, ARCs, CICs,
     co-operative banks, AIFIs and others
   - **All models**, not only credit or market risk
   - **Third-party models explicitly** — buying a model does not outsource accountability
   - **AI/ML, generative AI, agentic AI and rule-based systems**
   Requires board-approved frameworks, model inventories, risk-based classification, independent
   validation, AI-specific controls, vendor accountability, and **kill-switch arrangements** to
   override, suspend or deactivate models.
3. **Predecessor:** RBI draft circular 5 Aug 2024, "Regulatory Principles for Management of Model
   Risks in Credit". A broader RBI AI framework was reported under consideration as of Aug 2026,
   covering training data, localisation, third-party platforms and regulatory reporting.
4. **Maps onto** NIST AI RMF, ISO/IEC 42001, ISO/IEC 27001, DPDP Act. Global parallels: Basel
   Committee, EBA, Fed SR 11-7, MAS, FCA.
5. **AI governance is a corporate governance discipline, not a technology compliance one.** It
   belongs in enterprise risk management, not in an AI workstream reporting to engineering.

**The ideas the module is built on:**

- **Most model failures are misuse, not error.** A model built for one population applied to another,
  or built as a ranking input and used as a decision. Hence `approved_use` and `prohibited_use` as
  mandatory inventory fields.
- **Third-party models are HIGHER risk, not lower.** Firms tier them down because "the vendor
  validated it" — the vendor validated it on their population, for their use case, at a point in
  time you cannot see. The tiering function carries an explicit +2 for third-party.
- **The models that go missing from an inventory** are the ones nobody calls models: a pricing
  spreadsheet, a SQL flagging rule, a vendor score consumed via API, a prompt template drafting
  customer communications. All in scope.
- **A kill switch that has never been exercised is a design document.** The fallback is the hard
  part — "disable the credit model" is half a plan. Test in production quarterly, low-volume window.
- **Examiner question 7 is the real test:** "show me the last time a threshold was breached and what
  happened". A programme with no incidents in two years has either perfect models or no monitoring.
- **Recursion worth remembering:** if you use AI to help govern AI, that tool is itself a model and
  belongs in the inventory.

**Minimum viable programme for a small fintech** (stated in the module so it is not aspirational):
inventory · tiering rule · one named independent reviewer · kill switch · monitoring dashboard.
That is defensible at seed stage and maps onto the six pillars when asked.

### Session 39 — Module 08: Infrastructure (DONE)

`/fintech-ai/infrastructure/` — 15 sections, 11 code/prompt blocks, 3 registries.

**Research findings worth carrying forward (verified May 2026):**

1. **Build cost:** roughly 3–5x buying, on the order of $15–25M, 24–36 months to basic functionality —
   before the first customer. The happy path is easy; cost lives in reconciliation, interest accrual,
   statements and correctness on the worst day.
2. **Run cost:** cloud-native cores report ~$4–15 per account per year versus $40–80 on legacy. Noise
   at 10,000 accounts, the entire argument at 5 million.
3. **Enterprise cores do not fit early-stage fintechs.** Thought Machine and 10x require multi-year
   implementations and contract minimums sized for tier-1/2 banks. A seed/Series A team with <50
   engineers and an 18-month target should be on BaaS or a SaaS core.
4. **Pricing is almost entirely undisclosed and sales-negotiated.** A vendor quoting a number before
   understanding volume is usually excluding implementation or professional services — which
   frequently match year-one licence cost, with the SI often the largest single line.
5. **Vendor landscape:** Mambu · Thought Machine (Vault) · 10x (SuperCore) · Tuum · Finxact (Fiserv) ·
   Pismo (Visa) · Temenos / Finacle / FLEXCUBE / BaNCS as incumbents with cloud paths.
6. **India stack, by need:** simple acceptance → Razorpay/Cashfree/PayU · banking APIs without cards →
   Setu (Pine Labs) / Decentro · cards, lending OS, core replacement → M2P (acquired Syntizen for KYC
   and BSG for core) · lending lifecycle → LOS / LMS / BRE / collections / co-lending engine.
7. **Co-lending engines must be RBI-framework aligned** (CLM1/CLM2, triple schedules, blended rates,
   escrow). Retrofitting is painful.
8. **Data localisation is broader than cloud region.** It constrains which AI APIs you may call,
   where backups live, whether vendor support can access production from outside India, and —
   **the one teams miss — what your observability pipeline ships offshore by default.**
9. **Cloud exit strategy and vendor concentration** are now standing expectations in Indian BFSI
   architecture, framed as blast radius and portability rather than procurement.

**The three ideas the module is built on:**

- **The thin ledger pattern.** Mirror the provider's ledger in your own store, never authoritative,
  reconciled continuously. Buys independent error detection, a migration path, and analytics that do
  not depend on a vendor API. Cannot be retrofitted — history you never captured does not exist.
- **Three data planes kept separate.** Transactional (ACID, boring) · operational (event stream,
  the integration backbone) · analytical. **Analytics never reads the transactional database — not
  "should not", never.** One bad query during a settlement window is an outage.
- **Optimise for reversibility first, efficiency later.** Three day-one decisions determine whether
  the eventual migration is a project or a crisis: did you keep your own history, does product logic
  live in your code or the vendor's DSL, and are your internal events vendor-neutral.

**Ledger correctness properties to test rather than assume:** idempotency · atomicity across legs ·
ordering under concurrency · point-in-time reconstruction · immutability · integer minor units ·
determinism under replay. The concurrency test (two simultaneous debits against a balance that can
fund one) finds real bugs in systems that pass everything else.

### Session 38 — Module 07: Wealth & Advisory (DONE)

`/fintech-ai/wealth-advisory/` — 15 sections, 10 code/prompt blocks, 3 registries.
**Note: SEBI is the regulator for this module, not RBI.**

**Research findings worth carrying forward (verified May 2026):**

1. **SEBI's AI accountability position is the opposite of neutral.** Using AI does *not* reduce
   responsibility, it increases it. An adviser using AI or algorithmic tools must take full legal
   responsibility for AI-generated advice, ensure data security, integrity and transparency of the
   advice derived, and **disclose the extent of AI usage to clients**.
2. **Robo-specific expectations, usable as a build spec:** algorithm testing for correctness and
   transparency · a qualified person overseeing algorithm output · disclosure that advice comes from
   a system · no commission conflicts in the recommendable universe · inspection-ready at all times.
3. **Advice/execution segregation is structural.** Advisory and distribution must be segregated at
   client level, group level for non-individuals. SEBI circular 23.09.2020: an individual cannot
   provide advisory and execution simultaneously — a robo-advisory platform needs a separate entity
   (Company or LLP). Adviser recommends, client authorises, execution via brokers/AMCs. Fee-only;
   no commission from product manufacturers.
4. **Disclaimers do not change what something is.** SEBI enforcement is explicit that "for
   educational purposes only" does not excuse unregistered advisory activity — including inside
   courses, private groups or chatbot replies.
5. **Finfluencer framework** (Aug 2024 amendment + Jan 2025 circular): hard line between education
   and advice · registered entities may not pay or associate with unregistered finfluencers through
   money, referrals or data sharing · no stock price data less than three months old in educational
   content · no performance claims or return guarantees. **Dec 2025 order against Avadhut Sathe:
   ₹546 crore impounded plus a market ban.**
6. **RIA registration takes roughly 3–6 months.** Plan for it; do not discover it at launch.
7. **Accessibility obligations** under the Rights of Persons with Disabilities Act apply to regulated
   entities' digital platforms. Routinely missed by product teams, cheap to design in, expensive to
   retrofit.

**The two design ideas the module is built on:**

- **`binding = min(capacity, tolerance)`, and `required` is not a permission.** If the goal demands
  more risk than the client can bear, the *goal* changes — longer horizon, larger contributions,
  smaller target — not the portfolio. Automated advice systems get this wrong constantly because
  optimising toward a stated goal is the natural engineering framing and it inverts the obligation.
- **Suitability as deterministic rules, optimisation inside them.** Same hybrid pattern as the credit
  module. A model never decides what is permitted, only how to allocate within what is permitted.

**LLM boundary stated plainly:** the recommendation itself must never be generated. The determinism
argument is the strongest one and it is not about model quality — a suitability obligation requires a
reproducible, defensible decision, and a generative model produces a distribution of outputs.

### Session 37 — Module 06: Customer Operations (DONE)

`/fintech-ai/customer-operations/` — 15 sections, 11 code/prompt blocks, 3 registries.

**Builder fixed:** `/tmp/fintech_builder.py` still emitted the old JS-dependent lane CSS, so the new
render check caught a regression on the very first page built after Session 36b. The builder now
defaults to progressive enhancement (`.lane-section{display:block}` + `html.js` overrides + the
`classList.add("js")` flag in `<head>`). **The check earned its place immediately.**

**Research findings worth carrying forward (verified May 2026):**

1. **Air Canada set the governing principle.** A tribunal rejected the argument that a chatbot is a
   separate legal entity. When your AI tells a customer something, your organisation said it. The
   tribunal asked not whether the best model was used but whether **reasonable steps** were taken to
   ensure accuracy — a process question with documentable answers.
2. **Hallucination rates run 3–27%** even in controlled chatbot environments. Financial services
   production threshold is **below 0.1%** — a fabricated fee, rate or account status is a regulatory
   incident, not a CX problem.
3. **Containment reality:** contact volume follows ~40% easy / 40% medium / 20% hard. Pilot 4–8 weeks
   → 40–50%; 8–16 weeks → 55–65%; production stability 4–6 months; steady state 6–9 months. **Pushing
   past ~70–75% without human review increases complaint volume** as false resolutions compound.
   Emotional-labour share is 25–35% in financial services, not the 10–15% quoted for general support.
4. **Containment is measured dishonestly almost everywhere** — teams count "no escalation" but not
   "customer recontacted the same issue". Measure both. CSAT must be captured at resolution point,
   not 24h later. If "wrong answer given" exceeds ~3% of escalations, stop expanding scope.
5. **System prompts are not controls.** "Never promise a refund" in a prompt is a suggestion; the same
   rule in a validation regex is an evidenceable control. Regulators distinguish between them.
6. **RBI responsible business conduct directions on recovery, effective 1 July 2026:**
   contact only 08:00–19:00 **including digital** (an automated SMS at 22:00 is a reportable
   violation) · recovery calls and visits **recorded and retained 6 months** or until related
   litigation concludes · IIBF agent certification and identification disclosure · no visits without
   prior consent · ban on intimidation, public shaming and persistent calling · **prohibition on
   remotely disabling financed devices** · grievance acknowledged in 24h, resolved in 30 days, with
   **recovery suspended for that account while pending** · Internal Ombudsman at larger institutions ·
   **vicarious liability** — outsourcing collections does not outsource the obligation.
7. **RB-IOS 2026** (effective 1 July 2026) is the escalation path; BNS Section 351 criminal
   intimidation runs in parallel.
8. **The integration gap that causes most harm:** hardship disclosed to support that never reaches
   collections. Different vendors, different databases, legally compliant message that is
   indefensible in substance.
9. **ISO 42001** (AI management system) is increasingly expected by financial regulators as
   AI-specific governance distinct from SOC 2 / ISO 27001 infrastructure security.
10. **Liability in AI CX contracts is moving toward the deploying firm**, not the vendor. Read
    indemnity and limitation clauses specifically.

**Design rule stated in the module:** a classifier decides whether something *is* a complaint;
a human decides the *outcome*. Never the reverse.

### SESSION 36b — RENDER BUGS + CONTENT DEPTH AUDIT (23 May 2026)

Triggered by a user report: the ElevenLabs page is too thin, and on `/courses/ai-voice/` the
Intermediate and Advanced tracks do not load while Beginner is slow. Both were real. The second
was worse than reported.

### BUG 1 — 65 of 68 courses were effectively blank on first visit (FIXED)

Three compounding faults:
- CSS had `.track-panel{display:none}` and `.track-panel.active{display:block}`
- Intermediate and Advanced panels carried **inline `style="display:none"`**, which beats a class
  selector — so `.active` could never reveal them. They were unreachable, permanently.
- `#track-beginner` had no `active` class in the HTML, and the init script only restored a
  **saved** track from localStorage. A first-time visitor with no saved value got nothing at all —
  all three panels hidden until they clicked a tab.

Fix: strip the inline styles, mark the beginner panel `active` in the HTML, and default the init to
beginner when nothing is saved. Two courses (`agentic-ai`, `google-ads`) had variant init code and
were patched separately. All 68 verified.

### BUG 2 — 176 pages hid ALL content behind JavaScript (FIXED)

Every lane-based page — the AI Atlas tool pages **and all my own fintech modules** — used
`.lane-section{display:none}` with JS adding `.active`. **A crawler that does not execute JavaScript
saw an empty page.** That directly undermines the stated goal of the site being usable as an
LLM-readable reference.

Fix — progressive enhancement, now the required pattern:

```css
.lane-section{display:block}                 /* no JS: everything visible */
html.js .lane-section{display:none}          /* JS present: tabbed UI */
html.js .lane-section.active{display:block}
```
```html
<script>document.documentElement.classList.add("js");</script>  <!-- in <head> -->
```

**Any future tabbed or lane interface must follow this.** Content-visible-without-JS is now a
standing audit check.

### TWO NEW STANDING CHECKS — `/tmp/rendercheck.py`, folded into `/tmp/audit.py`

- **Render/JS problems** — inline `display:none` on a toggled panel, no default-visible panel,
  lane content hidden without JS, missing `js` flag, or any JS syntax error on the page. Must be 0.
- **Thin content** (reported metric, not a zero target) — content pages under 800 visible words.

### CONTENT DEPTH — the honest picture

| Section | Pages | Median words | Under 1,500 |
|---|---|---|---|
| Codex | 364 | 1,506 | 181 |
| AI Atlas | 158 | 1,406 | 90 |
| Courses | 69 | 747 | 65 |
| AI Kids | 117 | 450 | 117 |
| **Fintech AI** | **9** | **4,320** | **3** |

Benchmarks: the best AI Atlas pages (Claude 4,447 · Llama 4,681 · ChatGPT 4,130) and the fintech
modules sit around 4,000–4,500 words. **ElevenLabs is 1,371. My own Session 27 concept pages are
worse — reasoning-models is 478 words, token-economics 495, small-language-models 470.**

The fintech module depth is the standard the rest of the site should be held to. 224 content pages
sit under 800 words (excluding AI Kids activity pages, which are short by design).

### REMEDIATION PLAN ADDED — Sessions 43 to 48

| Session | Scope |
|---|---|
| 43 | Deepen the 11 `/ai-atlas/concepts/` pages to ~3,000+ words each (my own thin work first) |
| 44 | Deepen the 22 Session 28 tool pages to the Claude/Llama standard |
| 45 | ElevenLabs + the 20 thinnest pre-existing AI Atlas tool pages |
| 46 | The 12 AI Kids monthly pages (~120 words each — genuine stubs) + AI Kids hub depth |
| 47 | The 40 thinnest Codex guides |
| 48 | Section hub pages (many under 500 words) + final depth audit |

**Depth standard for any new or reworked page:** a tool page answers what it is, who it is for,
how to actually use it, what it costs, what it breaks on, how it compares, and when not to use it.
If a reader finishes the page still needing to visit the vendor site to understand the basics,
the page has failed.

---

### Session 36 — Module 05: Payments & Reconciliation (DONE)

`/fintech-ai/payments-reconciliation/` — 15 sections, 11 code/prompt blocks, 3 registries.

**Research findings worth carrying forward (verified May 2026):**

1. **Auto-match rates of 90–99%** are what mature platforms report. Published benchmark: 1,000
   records manually = ~7.2 hours; with AI matching = ~1.6 hours (78% reduction). Cycle time
   4.8 days → 1.9 days. The gains are on *matching*, not accountability.
2. **"Do not automate reconciliation and remove human sign-off in the same project."** Speed belongs
   on matching; accountability stays on approval.
3. **Exception aging is the metric that matters** — no unmatched item older than 30 days without a
   documented owner and plan. Report the distribution, not the average.
4. **Auto-match rate is trivially gamed by widening tolerances.** Treat tolerance changes as control
   changes: versioned, approved, dated, with before/after rates. If match rate improves sharply and
   exception *value* does not fall proportionately, someone widened a tolerance.
5. **India — RBI harmonised TAT** (circular RBI/2019-20/67, 20 Sept 2019, as amended): auto-reversal
   for failed UPI is T+1 working day, with compensation payable beyond it. A debit without a credit
   is not immediately a break — it is an item inside a defined reversal window.
6. **The deemed-acceptance trap, and how it was fixed.** Remitting banks could file chargebacks in
   URCS from T+0, before the beneficiary bank had reconciled; the beneficiary's RET would arrive too
   late and the chargeback closed with deemed acceptance, drawing RBI penalties. From 15 Feb 2025
   NPCI made URCS auto-accept/reject based on the TCC or RET raised in the *subsequent settlement
   cycle*. Generalisable lesson: **sequence disputes behind settlement, never in parallel.**
7. **UPI complaint volume exceeded 1.2M/month in Q1 2026**, ~60% "debited but not credited".
   RB-IOS 2026 replaced RB-IOS 2021 from 1 July 2026; awards up to ₹30 lakh consequential loss and
   ₹3 lakh for time/expense/harassment.
8. **Ledger design prevents most breaks:** integer minor units (never float) · `effective_at`
   separate from `recorded_at` (the two clocks) · UNIQUE `idempotency_key` supplied by the *caller*.
9. **Control totals catch silent file truncation.** A settlement file missing its last 200 rows
   reconciles with a perfect match rate on the rows present. Reconcile the header's declared count
   and total, not just the rows.
10. **Ambiguity in subset matching goes to a human.** Bound the combinatorial search; if more than
    one subset fits, never pick the first.

**The organising idea of the module:** the transaction clock and the settlement clock are different
clocks. Most exceptions are not errors — they are records observed at different points on two clocks.

### NEW PAGE TYPE — `/tmp/fintech_builder.py`

**This is the pattern all 68 courses migrate to in Session 42.** Key differences from every
earlier template:

- **Sticky left rail** (`.ft-rail`, `position:sticky`) carrying the depth selector — replaces the
  top tab bar used by courses. Collapses to inline buttons under 900px.
- **Three lanes**: green Beginner, indigo Intermediate, amber Advanced. `data-lane` attributes on
  both buttons and sections; `showLane()` toggles.
- **Auto table of contents** per lane, built from `h2`/`h3` ids, with scroll-spy via IntersectionObserver.
- **Copy buttons** on every code and prompt block (`.cb-copy`), clipboard API with execCommand fallback.
- **Tool registry component** (`registry()`) with direct / indirect / open-source pills and a
  mandatory `Verified <date>` badge.

Helper functions: `code(lang, body)`, `prompt(body)`, `registry(title, rows, verified)`,
`note(text)`, `warn(text)`, `page(path, title, meta, lead, label, crumbs, lanes)`.

`lanes` is a dict: `{'green': [(heading, html), ...], 'indigo': [...], 'amber': [...]}`.

Carries the overwrite guard and emits OG, Twitter, Article JSON-LD and BreadcrumbList.

### RULES FOR THIS SECTION

1. **Organise by problem, not by tool.** Tools are examples inside a module and are replaceable.
   This is what keeps the section useful in ten years.
2. **Every registry carries a verification date.** Registries decay fastest; keep them visually
   separate from the explanation so the page does not rot at the speed of its shortest-lived part.
3. **Implementation depth is the standard.** Not "use OCR" but: the pipeline, the engine comparison
   with honest trade-offs, where each breaks, validation, thresholds, working code, cost per 1,000.
4. **Do not build on `claude.ai/new?q=`.** It is undocumented, was removed once, and carries a
   documented prompt-injection vector. Copy buttons instead — stable and vendor-neutral.
5. **Unbuilt module cards on the hub are non-clickable divs**, not stub pages. Convert each to a
   link as its module ships. Never ship a stub.
6. **Code is illustrative.** Say once per module that anything touching KYC, AML, credit decisions
   or customer money needs qualified review.
7. **Search before writing registries and anything volatile.** Knowledge cutoff is May 2026.

### Remaining: Sessions 32 to 42

| Session | Module |
|---|---|
| ~~32~~ | ~~Identity \& Onboarding~~ — DONE |
| ~~33~~ | ~~Credit \& Underwriting~~ — DONE |
| ~~34~~ | ~~Fraud \& Risk~~ — DONE |
| ~~35~~ | ~~AML \& Compliance~~ — DONE |
| ~~36~~ | ~~Payments \& Reconciliation~~ — DONE |
| ~~37~~ | ~~Customer Operations~~ — DONE |
| ~~38~~ | ~~Wealth \& Advisory~~ — DONE |
| ~~39~~ | ~~Infrastructure~~ — DONE |
| ~~40~~ | ~~Governance~~ — DONE |
| ~~41~~ | ~~Build playbook~~ — DONE |
| ~~42~~ | ~~Course migration + AI Finance rebuild~~ — DONE |

---

## SESSION 30 — SEO SWEEP (22 May 2026) — BUILD COMPLETE

**No new content pages. Site-wide metadata and structured data brought to full coverage.**

### What was fixed

| Item | Before | After |
|---|---|---|
| Missing Open Graph | 231 | **0** |
| Missing Twitter card | 313 | **0** |
| Missing JSON-LD | 320 | **0** |
| Missing BreadcrumbList | 622 | **0** |
| Broken og:image | 830 | **0** |
| Invalid JSON-LD | 111 | **0** |
| Titles over 65 chars | 166 | **0** |

### Two real defects found and fixed

**1. og:image was broken site-wide.** 259 pages used a base64 `data:` URI for `og:image`. Social
platforms (Facebook, LinkedIn, X) **do not fetch data URIs** — every share was rendering without an
image. One page pointed at `/og-image.png`, which did not exist. Five real 1200x630 PNGs were generated
and every page now points at a section-appropriate one:

- `/og-image.png` (default) · `/og-codex.png` · `/og-ai-atlas.png` · `/og-ai-kids.png` · `/og-courses.png`

Regenerate them with PIL; the script pattern is in this session's history. **Update the counts on them
when page counts change** — they render "364 digital marketing guides" etc. as text.

**2. 111 JSON-LD blocks were invalid JSON.** Pre-existing blocks used single quotes for string values,
which Google's parser rejects outright. All 111 were rebuilt from each page's own title, description
and canonical URL across 57 pages.

### Metadata standard now enforced on every page

Every page carries: canonical · og:type/title/description/url/site_name/image (+width/height) ·
twitter:card/title/description/image · Article or Course JSON-LD · BreadcrumbList JSON-LD.
Homepage additionally carries WebSite and Organization schema. FAQPage added where FAQ content exists.

**The sweep script is reusable** — `/tmp/meta_sweep.py` pattern: it only adds what is missing, so it is
safe to re-run after adding pages. Run it, then re-run the JSON-LD validity check.

---

## BUILD COMPLETE — 30 SESSIONS

The build phase is finished. Every gap identified in the Session 22 audit has been closed.
From here the site is in **maintenance mode** — see the maintenance section below.

## SESSION 29 — NEW COURSES (22 May 2026)

**8 new courses, 120 lessons. 822 → 830. Courses: 60 → 68, lessons: 900 → 1,020.**

**AI courses (3)**
- ai-search-optimisation · open-source-ai-models · mcp-agent-infrastructure

**Marketing courses (5)**
- microsoft-ads · amazon-ads · emerging-ad-platforms · privacy-first-analytics · community-marketing

Courses hub updated — 68 cards, counts corrected, filter tabs updated (All 68 / AI 24 / Marketing 34 / Career 6 / Kids 4).

### COURSE BUILDER v3 — `/tmp/course_builder_v3.py`

**This version fixes the defect that caused the Session 19–22 breakage.** Every lesson URL is validated
with `vurl()` which **hard-fails before any file is written**:

```python
def vurl(u):
    b = u.rstrip('/')
    ok = (os.path.isfile(SITE+b+'/index.html') or os.path.isfile(SITE+b+'.html') or os.path.isfile(SITE+u))
    assert ok, f"⛔ LESSON URL DOES NOT EXIST: {u}"
    return u
```

It also carries the overwrite guard and emits Course JSON-LD, OG and Twitter tags.

**It earned its keep twice this session** — caught `/codex/sem/google-ads/google-ads-campaign-structure/`
(correct path is `search-campaign-setup`) and stopped an attempt to overwrite the existing `local-seo`
course. Nothing broken reached disk.

**Recommended practice:** run a pre-flight loop over all planned URLs before calling `build()`, so
failures surface as a list rather than one at a time.

**Rebuild the builder** by extracting `<style>`, the last `<script>`, and nav from `courses/seo/index.html`.

### Course integrity is now a standing check

```
1020 lesson links, 0 broken ✅
```
This was 28% broken at the start of Session 23. Verify it every session that touches courses.

**Note:** `local-seo` already existed as a course (Session 21) and already links correctly to the
`/codex/seo/local/` pages created in Session 23. Community Marketing was built in its place.

---

## SESSION 28 — AI ATLAS TOOLS (22 May 2026)

**22 new tool guides. 800 → 822.** All the tools flagged as missing in the audit are now covered.

**Models** — `/ai-atlas/tools/`
- deepseek · qwen · kimi · cohere · amazon-nova · apple-intelligence · manus

**Video** — `/ai-atlas/specialist-tools/video/`
- veo · opus-clip · captions

**Coding** — `/ai-atlas/specialist-tools/coding/`
- devin · cline · aider

**Business productivity** — `/ai-atlas/specialist-tools/business-productivity/`
- glean · clay · granola · fathom

**Voice** — deepgram · assemblyai (`voice-audio/`) · bland-ai (`voice-agents/`)
**Images** — recraft · krea (`images-design/`)

All 22 linked from their category hubs under a "Recently added" block.

### AI TOOL PAGE BUILDER — `/tmp/tool_builder.py`

Tool pages use the **three-lane** structure (Simple / Working / Deep) with `showLane` JS, which is
different from both the Codex guide template and the AI Atlas concept template. Rebuild the builder by
extracting from `/ai-atlas/tools/grok/index.html` (smallest complete example at ~29KB):

- `<style>`, nav+drawer, footer and the two `<script>` blocks
- Structure: `page-hero` → breadcrumb → `label-tag` → h1 → `hero-lead` → `art-meta` → **Visit button**
  → `lane-tabs` bar → `art-layout` with three `.lane-section` divs (`lane-green`, `lane-indigo`, `lane-red`)
  → sidebar with Quick facts / Official link / Related
- Every tool page MUST carry the Visit button in the hero (added Session 16) and an official link card
- Carries the same overwrite guard (`tsafe`)

**Three builders now exist and should be reused rather than rewritten:**
| Builder | For | Theme |
|---|---|---|
| `/tmp/guide_builder.py` | Codex guides and hubs | Dark Codex |
| `/tmp/atlas_builder.py` | AI Atlas concept pages | Dark Atlas |
| `/tmp/tool_builder.py` | AI Atlas tool pages (3-lane) | Dark Atlas |

**Session note:** 2 broken links were introduced and caught by the end-of-session check —
`/ai-atlas/specialist-tools/video/runway/` (correct path is `/ai-atlas/tools/runway/`) and
`/codex/email-marketing/email-marketing-strategy/` (no such page; use `/codex/email-marketing/`).
Both were already documented as wrong paths in earlier sessions. Check the file tree, not memory.

---

## SESSION 27 — ANALYTICS + AI CONCEPTS (22 May 2026)

**16 new pages. 784 → 800.**

**Analytics gaps closed** — `/codex/analytics-cro/`
- consent-mode-v2 · server-side-tagging · data-clean-rooms · customer-data-platforms

**NEW SECTION: `/ai-atlas/concepts/`** — 11 guides + hub (DARK theme)
- rag · embeddings-vector-databases · model-context-protocol · reasoning-models
- prompt-injection-ai-security · running-ai-locally · open-vs-closed-models
- ai-evals-benchmarks · token-economics · small-language-models · ai-regulation

Linked from the AI Atlas hub as a new card.

### AI ATLAS PAGE BUILDER — use this for all future Atlas pages

The AI Atlas uses the **dark** theme and a different structure from the Codex. Builder pattern saved at
`/tmp/atlas_builder.py`; rebuild it by extracting from any page in `/ai-atlas/concepts/`:

- `<style>` block, nav+drawer, and footer extracted from `/ai-atlas/fine-tuning/index.html`
- Structure: `page-hero` → `breadcrumb` → `label-tag` → `h1` → `hero-lead` → `art-meta`,
  then `art-layout` with `<main>` and `<aside class="art-sidebar">`
- Sidebar links use `class="sidebar-link"`, not the Codex `<ul class="sidebar-list">` pattern
- Ships with OG, Twitter card, Article JSON-LD and BreadcrumbList JSON-LD

**Both builders now carry the overwrite guard** (`safe_check` / `asafe`) — they refuse to write
`index.html` into a directory holding real content (>3KB, no `<title>Redirecting`).

**Reusable scripts now exist and should be reused, not rewritten:**
- `/tmp/linkcheck.py` — `scan()` returns broken link targets (uses `os.path.isfile`, catches empty dirs)
- `/tmp/rebuild_infra.py` — regenerates sitemap.xml, search-index.json, llms-full.txt, manifest.json
- `/tmp/audit.py` — full zero-check table

---

## SESSION 26 — SOCIAL PLATFORMS (22 May 2026)

**11 new guides + cleanup. 773 → 784.**

**New platform guides** — `/codex/social-media/`
- threads-marketing · bluesky-marketing · reddit-marketing · pinterest-marketing
- snapchat-marketing · discord-telegram-communities

**New strategy guides**
- short-form-video-strategy (cross-platform Reels/TikTok/Shorts/Spotlight)
- social-listening · user-generated-content · employee-advocacy · social-media-crisis-management

**Social Media hub** rebuilt with two new groups: Emerging Platforms, Strategy & Operations.

### Two infrastructure fixes

**1. Link checker had a false-negative.** The old check used `os.path.exists(path)` which returns True
for an *empty directory*. Twenty empty directories were left behind by Session 23's stub deletion and
one genuine broken link was hiding behind that hole. Corrected checker now at `/tmp/linkcheck.py`
pattern — must test `os.path.isfile()` on the actual served file:

```python
def resolves(l):
    b = l.rstrip('/')
    return (os.path.isfile('.'+b+'/index.html')
         or os.path.isfile('.'+b+'.html')
         or os.path.isfile('.'+l))
```

**2. 20 empty directories removed.** All already had 301 rules from Session 23. "Empty directories"
is now a standing audit check and must stay at 0.

**Overwrite guard added to the guide builder** — refuses to write `index.html` into a directory
already containing real content (>3KB and no `<title>Redirecting`). This is the guard that Session 25
needed and did not have.

---

## SESSION 25 — PAID ADVERTISING EXPANSION (22 May 2026)

**19 new pages. 754 → 773.** Every major paid platform now covered.

**New platform sections under `/codex/paid-advertising/`**
- `microsoft-ads/` (hub + 3) — microsoft-ads-fundamentals, importing-google-ads-campaigns, microsoft-audience-network
- `amazon-ads/` (hub + 3) — amazon-ads-fundamentals, sponsored-products, retail-media-networks
- `tiktok-ads/` (hub + 2) — tiktok-ads-fundamentals, tiktok-creative-best-practices
- `x-ads/` · `reddit-ads/` · `snapchat-ads/` · `apple-search-ads/` (single guides)

**Google Ads subsection hubs built** — these directories had guides but no index page
- `/codex/sem/google-ads/shopping/` (4) · `display/` (4) · `youtube/` (2) · `advanced/` (2)

**Paid Advertising hub** updated with 11 section links.

---

### ⚠️ CRITICAL LESSON — READ BEFORE BUILDING ANY HUB PAGE

During this session I overwrote a **real 44KB guide** (`/codex/sem/google-ads/bidding-strategies/`)
with a thin auto-generated hub page. It was restored from the v9 zip.

**Before writing any `index.html` into an existing directory, check whether one already exists and
whether it is real content or a stub.** Stubs are under ~3KB and contain `<title>Redirecting`.
Real guides are 40KB+.

```python
p = f"{dir}/index.html"
if os.path.exists(p):
    h = open(p).read()
    is_stub = '<title>Redirecting' in h or os.path.getsize(p) < 3000
    assert is_stub, f"REAL CONTENT at {p} — do not overwrite"
```

A full content-loss check against the previous zip was then run and confirmed **0 real pages
unreachable**. Run that check whenever files are deleted or overwritten in bulk:
compare every page in the previous zip against (file exists OR resolves through `_redirects`).

Note also: `/codex/sem/google-ads/bidding-strategies/` is the REAL guide.
`google-ads-bidding-strategies/` was a stub and is now a 301.

---

## SESSION 24 — SEO DEPTH (22 May 2026)

**17 new pages. 737 → 754.**

**NEW SECTION: `/codex/seo/ai-search/`** — the largest strategic gap closed
- ai-overviews-optimisation — how AI Overviews select and cite sources, passage-level optimisation, click-through reality
- generative-engine-optimisation — GEO, entity clarity, chunk-survivable structure
- answer-engine-optimisation — AEO across snippets, PAA, voice, AI answers
- llms-txt-seo — AI crawler landscape, robots.txt for AI bots, llms.txt proposal (flagged as non-standard)
- zero-click-search — causes, exposed query types, strategy that survives it
- ranking-in-ai-assistants — retrieval vs parametric visibility in ChatGPT/Perplexity/Copilot

**Local SEO completed** (`/codex/seo/local/` now 7 guides + hub)
- multi-location-seo, service-area-businesses

**E-commerce gaps closed**
- subscription-commerce, quick-commerce (India quick-commerce context), d2c-strategy

**6 SECTION HUB PAGES BUILT** — these were meta-refresh stubs redirecting to parent; now real pages
- /codex/seo/ai-search/ (6 guides) · /codex/seo/local/ (7) · /codex/seo/technical/ (15)
- /codex/seo/on-page/ (9) · /codex/sem/google-ads/ (11) · /codex/paid-advertising/facebook-instagram/ (24)
- 4 obsolete 301 rules removed from `_redirects` since those paths now serve real content
- /codex/seo/ hub updated with AI Search Optimisation and Local SEO guide groups

**Session note:** 3 broken links were introduced during this session by writing related-guide URLs from
assumption (featured-snippets, topical-authority, crawlability-indexability — none exist). Caught by the
end-of-session link check and fixed. THE CHECK IS WHY IT DID NOT SHIP. Never skip it.
Correct paths: SERP features = /codex/seo/fundamentals/serp-features/, crawlability =
/codex/seo/fundamentals/crawlability-indexation/. There is no topical-authority page.

## SESSION 23 — REPAIR (22 May 2026)

**Fixed**
- 93 broken internal links → 0. 126 instances remapped, 309 rewritten to skip redirect hops.
- 240 duplicate flat/dir page pairs → deleted + 301 redirected
- 26 meta-refresh stubs → converted to real 301s
- 7 duplicate policy/overview pages → consolidated + 301s
- 515 duplicate titles / 517 duplicate descriptions → 0
- sitemap.xml rebuilt to exactly match files on disk (737/737)
- search-index.json rebuilt: 26 stale entries removed, 191 added
- llms-full.txt regenerated, manifest.json → v9.0

**33 new Codex guides**
- `/codex/seo/local/` **NEW SECTION** (5) — local-seo-fundamentals, google-business-profile, local-citations, online-reviews-reputation, local-keyword-research
- `/codex/seo/technical/` (5) — mobile-seo, site-architecture, https-security, duplicate-content-canonicalisation, technical-seo-audit
- `/codex/analytics-cro/` (5) — web-analytics-fundamentals, bounce-rate-engagement-rate, utm-parameters-campaign-tracking, looker-studio-google-data-studio, analytics-audit-checklist
- `/codex/social-media/` (4) — influencer-marketing, social-commerce, social-media-community-management, choosing-social-media-platforms
- `/codex/business-strategy/` (5) — brand-strategy, brand-voice-tone, customer-segmentation, market-research, international-marketing
- `/codex/content-marketing/` (3) — thought-leadership-content, content-localisation, content-roi-measurement
- `/codex/paid-advertising/` (4) — media-buying-fundamentals, display-advertising, video-advertising, mobile-advertising
- `/codex/programmatic/` (1) — real-time-bidding
- `/codex/email-marketing/` (1) — email-design-templates

**New guide standard (use for all future Codex pages):** Open Graph tags, Twitter card, Article JSON-LD
and BreadcrumbList JSON-LD on every page. Rebuild the generator by copying the `<head>` of any guide
created in Session 23, e.g. `/codex/seo/local/local-citations/index.html`.

**RULE ADDED — MANDATORY**
Every session must end with a site-wide broken-link check. Never write a lesson or related-guide URL
from assumption — verify it against the real file tree first. Assumed URLs are what produced the 93
broken links across Sessions 19–22.

---

## SITE ARCHITECTURE

**100% static HTML.** No server-side code, no build process, no Node/npm required.
Every page is a pre-built `.html` file. CSS is inline `<style>` blocks inside each page.
One shared JS file: `theme-search.js` (client-side search only).
One shared JSON file: `search-index.json` (loaded client-side on search).

**Zero Cloudflare quota usage** — no Pages Functions, no Workers, no dynamic routes.

**Infrastructure files at root:**
- `sitemap.xml` — 712 URLs (all 846 pages covered, utility pages excluded intentionally)
- `sitemap-llm.xml` — 954 URLs with `<llm:type>` and `<llm:title>` semantic labels per URL
- `robots.txt` — allows all crawlers + references both sitemaps + all LLM discovery files
- `llms.txt` — comprehensive LLM access policy, all hub URLs, AI Kids section, topic map, wa.expert reference
- `llms-full.txt` — plain-text dump of all 846 pages (title | url | description) for bulk LLM use
- `manifest.json` — site identity, section counts, content policy, AI crawling permission
- `changelog.json` — full version history (v1.0 April 2026 → v3.0 May 2026)
- `humans.txt` — web credits file
- `.well-known/llm-context.json` — structured context block for LLMs
- `.well-known/schema-version.json` — schema version and format notes
- `.well-known/ai-plugin.json` — GPT/OpenAI-style AI plugin discovery
- `search-index.json` — 370 entries (client-side search)
- `theme-search.js` — client-side search engine
- `_headers` — Cloudflare Pages cache headers + security headers (X-Frame-Options, X-Content-Type etc.)
- `_redirects` — `/wsp/*` → `/csp/*` (301), `/home.html` → `/` (301)

---

## DIRECTORY STRUCTURE

```
/index.html                          ← Homepage (typewriter effect, 14 chips, 4 cards)
/sitemap.xml                         ← 712 URLs (all pages covered)
/sitemap-llm.xml                     ← 954 URLs with semantic type labels
/robots.txt                          ← All crawlers welcome + LLM discovery refs
/llms.txt                            ← AI/LLM access policy + AI Kids + all hubs
/llms-full.txt                       ← Full plain-text dump (846 entries)
/manifest.json                       ← Site identity + section counts
/changelog.json                      ← Version history v1.0→v3.0
/humans.txt                          ← Web credits
/search-index.json                   ← 370 search entries
/theme-search.js                     ← Client-side search
/_headers                            ← Cloudflare Pages cache + security headers
/_redirects                          ← URL redirects
/.well-known/llm-context.json        ← Structured LLM context block
/.well-known/schema-version.json     ← Schema version notes
/.well-known/ai-plugin.json          ← GPT/OpenAI plugin discovery

/what-is-digital-marketing/          ← Canonical definition page
/what-is-seo/                        ← Canonical definition page
/what-is-ai/                         ← Canonical definition page

/codex/                              ← Digital Marketing Codex (534 pages)
  /seo/ /sem/ /paid-advertising/ /email-marketing/ /analytics-cro/
  /business-strategy/ /social-media/ /content-marketing/ /case-studies/
  /ecommerce/ /programmatic/ /affiliate-marketing/ /history/ /tools-resources/

/ai-kids/                            ← AI Kids curriculum (60 pages — added May 2026)
  /safety/ /starter/ /explorer/ /builder/ /monthly/ /parents/
  /starter/session-1/ through session-8/
  /explorer/session-1/ through session-16/
  /builder/session-1/ through session-24/
  /monthly/may/session-1/ through session-4/

/ai-atlas/                           ← AI Atlas (125 pages)
  index.html
  /agentic-ai/                       ← NEW — Agentic AI section
    index.html                       ← What is Agentic AI
    /how-agents-work/                ← How AI Agents Work
    /multi-agent-systems/            ← Multi-Agent Systems
  /tools/                            ← Core AI tool guides (19 tools)
    chatgpt, claude, claude-ai, gemini, gemini-advanced, copilot, copilot-365,
    dall-e, elevenlabs, gemini-workspace, grok, llama, meta-ai, midjourney,
    mistral, notion-ai, perplexity, runway, sora
  /specialist-tools/                 ← 54 specialist tool guides
    /agentic-frameworks/ (4)         ← NEW — langchain, crewai, autogen, llamaindex
    /coding/ (7)                     ← bolt, claude-code, cursor, github-copilot, replit-agent, v0, windsurf
    /automation/ (5)                 ← lindy, make, n8n, relay, zapier
    /video/ (7)                      ← descript, heygen, invideo, kling, luma, pika, synthesia
    /images-design/ (5)              ← adobe-firefly, canva-ai, ideogram, leonardo, stable-diffusion
    /writing-content/ (7)            ← copy-ai, grammarly, hemingway, jasper, quillbot, sudowrite, wordtune
    /research-knowledge/ (5)         ← consensus, elicit, notebooklm, scite, semantic-scholar
    /voice-audio/ (13)               ← adobe-podcast, aiva, beatoven, descript-audio,
                                        elevenlabs-pro, murf, otter, resemble-ai,
                                        sarvam-ai, speechify, suno, udio, whisper
    /voice-agents/ (2)                ← vapi, retell-ai  ← NEW Session 10
    /business-productivity/ (6)      ← beautiful-ai, copilot-excel, fireflies, gamma, otter-meetings, tome
    /data-analysis/ (1)               ← julius-ai  ← NEW Session 9
  /use-cases/ (7 pages)              ← images, presentations, research, studying, video, writing
  /for-you/ (5 pages)                ← job-seekers, parents, small-business, students, teachers
  /glossary/, /history/, /prompt-library/, /which-ai/, /family-tree/, /start-here/
  /fine-tuning/, /vibe-coding/, /ai-careers/   ← NEW Session 11

/courses/                            ← Courses section (4 pages)
  index.html                         ← Hub page (filter by AI/Marketing/Career)
  /agentic-ai/                       ← Full course: Beginner/Intermediate/Advanced
  /seo/                              ← Full course: Beginner/Intermediate/Advanced
  /google-ads/                       ← Full course: Beginner/Intermediate/Advanced

/curriculum/                         ← Education section (5 pages, LIGHT CREAM THEME)
  index.html                         ← Hub with Student Programme cards at bottom
  /school/index.html                 ← 8-module school curriculum
  /school/assessments/index.html     ← 104 assessment questions
  /college/index.html                ← 12-module college curriculum (+Agentic AI Module 8)
  /college/assessments/index.html    ← 205 assessment questions (+13 agentic AI questions)

/csp/                                ← Clarigital Student Programme (107 pages)
  index.html                         ← CSP hub (2-week programme)
  1-month-internship.html            ← Pre-Sales Internship (1MI)
  2-month-internship.html            ← Expert Internship (2ME)
  /e/, /m/, /s/ subdirs              ← Daily task pages

/sources/index.html                  ← 874-source master reference
/about/, /privacy-policy/, /terms-of-use/, /cookie-policy/, /disclaimer/
```

---

## HOMEPAGE DESIGN (current — clean 3-card layout)

**Structure:**
1. Nav (sticky, dark)
2. Hero — headline + search bar + proof pills
3. Three cards: Marketing Codex / AI Atlas / Curriculum
4. Disciplines strip (14 Codex disciplines as clickable pills)
5. Footer

**Sections REMOVED from old homepage:** curriculum banner, student programmes section, courses section, two-products section, AI Atlas preview, "What is Clarigital" section, dual CTA.

**Key numbers:**
- Search placeholder: `"Search 346 guides"`
- Proof pills: `220 Marketing Guides · 127 AI Guides · 1,000+ Prompts · 0 Ads · 100% Official Sources`
- GA4: `G-7DFK94MRK7`

---

## TWO NAV TYPES — CRITICAL

The site has two distinct nav backgrounds. The logo colour must match:

| Section | Nav background | Logo text colour |
|---|---|---|
| Codex (`/codex/`) | White `#ffffff` via `var(--w)` | Navy `#1D4ED8` |
| All other pages | Dark navy `rgba(15,23,42,.93)` | White `#F1F5F9` |

**When editing any page:** always check which nav type it has before setting logo colour.
Detect with: `'.site-nav{background:var(--w)' in css` → white nav → navy text.

**Nav links (current standard — all non-Codex pages):**
```html
<a href="/codex/">Codex</a>
<a href="/ai-atlas/">AI Atlas</a>
<a href="/courses/">Courses</a>
<a href="/curriculum/">Curriculum</a>
<a href="/about/">About</a>
```

**Search input attribute (CRITICAL):** Must use `data-search-input` and `data-search-results` attributes — NOT `id="navSearch"` / `id="searchResults"`. Pages built before Sessions 1-5 used the wrong attributes and search was broken. All new pages must use:
```html
<input type="search" data-search-input ...>
<div class="search-results" data-search-results></div>
```

---

## TWO COLOUR THEMES

**Dark theme** (AI Atlas, specialist tools, homepage, courses, definition pages):
```css
--bg: #0F172A        /* page background */
--fg: #F1F5F9        /* body text */
--blue: #60A5FA      /* accent */
--indigo: #818CF8
```

**Light theme** (Codex, Curriculum):
```css
body { background: #FEF3EC; color: #374151; }  /* cream bg, dark text */
--navy: #1D4ED8      /* primary accent */
```

**CRITICAL:** Curriculum pages use dark CSS as base + `/* LIGHT THEME OVERRIDE — curriculum pages only */` on top. ANY new sections added to curriculum pages must use light theme colours (`#fff` cards, `#0F172A` headings, `#6B7280` body text, `#E2E8F0` borders). Do NOT inject dark-themed HTML into curriculum pages.

---

## SPECIALIST TOOL GUIDES — STANDARDS

54 guides across 9 categories. Each guide must have:
- 3 lane sections: Simple / Working / Deep
- Dark theme (`--bg:#0F172A`)
- Minimum 5 prompts (12+ preferred on complex tools)
- Lane tabs with `onclick="showLane('green'/'indigo'/'red')"`
- Breadcrumbs with full path
- Sidebar with pricing / related tools / official links
- Schema markup (Article + BreadcrumbList)
- `<time datetime="YYYY-MM-DD">Last verified: Month YYYY</time>` in hero
- GA4: `G-7DFK94MRK7`

**TEMPLATE WARNING:** Do NOT reuse the ElevenLabs page as a nav/footer template. ElevenLabs uses `<header>` wrapper with a different structure. Extract nav and footer from pages built in sessions 1+ (agentic-ai pages, crewai page etc.) instead.

**Lane JS (required on every specialist tool page):**
```javascript
function showLane(l){
  document.querySelectorAll('.lane-section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.lane-tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('lane-'+l).classList.add('active');
  document.getElementById('tab-'+l).classList.add('active');
}
document.addEventListener('DOMContentLoaded',function(){
  var f=document.querySelector('.lane-tab');if(f)f.click();
});
```

---

## SCHEMA MARKUP (added April 2026)

All major hub pages, new guides, and definition pages now have:
- `Article` schema (headline, url, dateModified, author, publisher)
- `BreadcrumbList` schema
- `FAQPage` schema on definition pages

The 3 definition pages additionally have full FAQ schema with 4 Q&A pairs each.

When building new pages, always add at minimum Article + BreadcrumbList in `<head>`.

---

## CURRICULUM SECTION

**5 pages, light cream theme, print-ready A4.**

School curriculum: 8 modules, ~12 hours, ages 15-18, accessible formal language
College curriculum: 12 modules, ~27 hours, undergraduate/professional, full academic language
College Module 8 now includes Agentic AI content (added April 2026)
College assessment bank: 205 questions (120 MCQ + 48 short answer + 24 essay + 13 agentic AI)
School assessment bank: 104 questions

**Student Programme section** on curriculum hub page (at bottom, LIGHT THEME cards):
- CSP (2-week starter) → `/csp/`
- Pre-Sales Internship (1MI, 1 month) → `/csp/1-month-internship.html`
- Expert Internship (2ME, 2 months) → `/csp/2-month-internship.html`

**Print stylesheet required on all curriculum pages:**
```css
@media print{
  nav,.site-nav,footer,.print-btn,.print-hide{display:none !important}
  body{background:#fff !important;color:#000 !important;font-size:11pt}
  @page{size:A4;margin:2cm 2.5cm}
  .answer-key-section{page-break-before:always}
}
```

---

## AGENTIC AI SECTION (built April 2026)

**Concept guides (`/ai-atlas/agentic-ai/`):**
- `index.html` — What is Agentic AI (3 lanes, OWASP Top 10, EU AI Act, MCP)
- `how-agents-work/` — The agent loop, ReAct pattern, tool calling, failure modes
- `multi-agent-systems/` — Orchestrators, patterns, cascading failure, MCP/A2A

**Frameworks hub + 4 guides (`/ai-atlas/specialist-tools/agentic-frameworks/`):**
- `index.html` — All 4 frameworks compared in a table
- `langchain/` — LangChain/LangGraph: StateGraph, checkpointing, MCP integration, LangSmith
- `crewai/` — Role-based crew, sequential/hierarchical, memory, Pydantic output
- `autogen/` — ⚠️ MAINTENANCE MODE — being merged into AG2. No new features. Covers ConversableAgent, GroupChat, code execution sandbox
- `llamaindex/` — RAG pipelines, HyDE, sentence window retrieval, RAGAS evaluation

---

## VOICE & AUDIO SECTION (built April 2026)

**12 tools at `/ai-atlas/specialist-tools/voice-audio/`:**

| Tool | Slug | Key content |
|---|---|---|
| ElevenLabs | `elevenlabs-pro` | Voice cloning, TTS, multilingual dubbing |
| OpenAI Whisper | `whisper` | Speech-to-text, 99 languages, $0.006/min API, open source |
| Murf | `murf` | Professional TTS, 120+ voices, SSML, e-learning |
| Suno | `suno` | AI music generation, v4, ⚠️ copyright litigation (UMG/Sony/Warner) |
| Speechify | `speechify` | Text-to-audio reading up to 4.5x speed, dyslexia tool |
| Udio | `udio` | AI music, stem export, audio conditioning, ⚠️ same litigation as Suno |
| Resemble AI | `resemble-ai` | Voice cloning API, real-time conversion, deepfake detection |
| AIVA | `aiva` | Orchestral/cinematic composition, MIDI export, SACEM 2017 |
| Beatoven.ai | `beatoven` | Royalty-free background music, video sync, India-founded |
| Adobe Podcast | `adobe-podcast` | AI audio cleanup |
| Descript Audio | `descript-audio` | Transcript-based editing |
| Otter.ai | `otter` | Meeting transcription |

**⚠️ TEMPLATE WARNING FOR VOICE PAGES:** Do NOT build new voice pages using ElevenLabs as template — it uses `<header>` wrapper which causes entire ElevenLabs content to bleed into new pages. Use nav/footer from agentic-ai or crewai pages.

---

## COURSES SECTION (partially built April 2026)

**`/courses/index.html`** — Hub with category filter (JS), 3 courses live, 13 coming soon.
**`/courses/agentic-ai/`** — Full course: 3 tracks, 5 lessons each, quizzes, LocalStorage progress
**`/courses/seo/`** — Full course: 3 tracks (Beginner/Intermediate/Advanced)
**`/courses/google-ads/`** — Full course: 3 tracks

Course pages use LocalStorage for:
- Lesson completion checkboxes (key: `cl-[topic]-lessons`)
- Track selection memory (key: `cl-[topic]-track`)

Courses section is **deprioritised** — only 3 built so far. Focus is on Codex and AI Atlas guides.

---

## CANONICAL DEFINITION PAGES (built April 2026)

Three entity-anchoring pages for LLM knowledge graph construction:
- `/what-is-digital-marketing/` — Full guide with Article + FAQPage + BreadcrumbList schema
- `/what-is-seo/` — Full guide with schema
- `/what-is-ai/` — Full guide with schema

All three are linked from the homepage footer "Definitions" column.

---

## KNOWN FILE STRUCTURE QUIRK

The Codex business-strategy section has TWO copies of each guide:
- Flat file: `codex/business-strategy/competitive-analysis-framework.html`
- Directory: `codex/business-strategy/competitive-analysis-framework/index.html`

**Both must be updated** when fixing links on these pages.
When scanning for issues, always use `*.html` not just `index.html` in the Codex.

---

## SOURCES PAGE

`/sources/index.html` — 874 unique external sources, 17 categories.
Has live search box (`id="srcSearch"`) that filters all 874 entries client-side.

**Source policy:** Official documentation, peer-reviewed research, regulatory bodies only.
No paywalls. No HBR, Forrester, Gartner, Statista, WARC links.

---

## GA4 TRACKING

All pages use: `G-7DFK94MRK7`
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7DFK94MRK7"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-7DFK94MRK7');</script>
```

---

## INTERACTIVE CAPABILITIES — WHAT STATIC HTML CAN DO

All of these work on Cloudflare Pages. No server. No framework. No build step.

1. **CSS Animations** (zero JS) — pulse, spin, slide, fade, bounce
2. **Tabs** — lane switching on guide pages, track switching on course pages
3. **Accordion** — expandable FAQ sections
4. **Scroll Reveal** — IntersectionObserver adds `.visible` class
5. **Interactive Quiz** — multiple choice, instant feedback, LocalStorage score
6. **Progress Bars** — LocalStorage-backed lesson completion
7. **Interactive SVG** — clickable diagrams
8. **LocalStorage** — persists track selection, quiz scores, lesson progress across sessions

**CONSTRAINTS (hard limits):** No user accounts, no server-side search, no real-time data, no database writes, no email sending.

---

## REMAINING BUILD WORK (as of 22 May 2026)

### Sessions remaining: 12 — Build Sheets 04–09 (47–52), content depth (53–58)

| # | Session | Scope | Est. output |
|---|---|---|---|

**At completion:** ~1,100 pages · 68 courses · 1,020 lessons · full schema coverage.

### Known content gaps still open (verified absent, 22 May 2026)


---

### Session 13 — Final Session (April 2026)
- ✅ Homepage search placeholder updated: "Search 313 guides…" → "Search 360+ guides"
- ✅ Homepage AI Guides count updated: 127 → 80 (accurate count of AI Atlas guides)
- ✅ llms.txt updated with all Sessions 9-11 new sections and topic relationship map
- ✅ Higgsfield guide built (mentioned in viral AI script, missing from site)
- ✅ All zeros across all technical checks
- ✅ SITE IS COMPLETE AND VERIFIED


---

## AI KIDS — COMPLETE CURRICULUM (added May 2026)

**URL:** `/ai-kids/`
**Purpose:** Supervised AI learning for children aged 7–13 — done with a parent or teacher
**Total pages:** 60 (hub pages + 48 session pages + safety + parents)
**Design theme:** LIGHT — warm white `#FFFBF5`, coral `#FF6B35`, sky blue `#0EA5E9`, purple `#7C3AED`, green `#10B981`
**Font:** Inter (Google Fonts) — NOT system font
**Nav template:** Extract from `/ai-kids/explorer/session-1/index.html` (light kids theme)

⚠️ **CRITICAL:** Do NOT use the dark AI Atlas theme for AI Kids pages. They use a completely separate light design system defined in their own `<style>` block.

### AI Kids page inventory

```
/ai-kids/                          ← Hub with smart MCQ onboarding quiz
/ai-kids/safety/                   ← Safety guide for parents (read first)
/ai-kids/parents/                  ← Parent resources, FAQ, session tracker
/ai-kids/starter/                  ← AI Starter hub (ages 7–10, 8 sessions)
/ai-kids/starter/session-1/ through session-8/
/ai-kids/explorer/                 ← AI Explorer hub (ages 8–11, 16 sessions)
/ai-kids/explorer/session-1/ through session-16/
/ai-kids/builder/                  ← AI Builder hub (ages 10–13, 24 sessions)
/ai-kids/builder/session-1/ through session-24/
/ai-kids/monthly/                  ← AI Monthly hub (12 months, all live, evergreen)
  /ai-kids/monthly/may/        ← May 2026: AI Basics Refresher
  /ai-kids/monthly/june/       ← June 2026: AI and Animals
  /ai-kids/monthly/july/       ← July 2026: AI and Space
  /ai-kids/monthly/august/     ← August 2026: AI and Cooking
  /ai-kids/monthly/september/  ← September 2026: AI and Art
  /ai-kids/monthly/october/    ← October 2026: AI and Stories
  /ai-kids/monthly/november/   ← November 2026: AI and Sport
  /ai-kids/monthly/december/   ← December 2026: AI and the Holidays
  /ai-kids/monthly/january/    ← January 2027: AI and Health
  /ai-kids/monthly/february/   ← February 2027: AI and History
  /ai-kids/monthly/march/      ← March 2027: AI and Money
  /ai-kids/monthly/april/      ← April 2027: AI and the Future
  Each month: hub + session-1/ through session-4/
```

### Smart onboarding quiz (on /ai-kids/)

- 4 MCQ questions: age → experience → role → time
- Q1 visible by default (hardcoded `visible` class) — NO JS dependency for Q1
- Q2-Q4 revealed by JS as each answer is selected
- Result: personalised roadmap + full session checklist with checkboxes
- Progress saved to `localStorage` (key: `clarigital_kids_progress`)
- All roadmap combinations pre-built in `const ROADMAPS` object
- `const SCHEDULES` appears ONCE only — duplicate declaration caused a critical JS bug previously
- `selectAnswer()`, `showResult()`, `toggleSession()`, `resetProgress()`, `resetQuiz()` are the key functions

### Session structure (every session)

Every session page has:
1. Progress dots (1–N showing current position)
2. Coloured session header with gradient
3. Info box (today's goal)
4. Warm Up (activity-block warmup)
5. Main Activity (activity-block main) — with copy-able prompt boxes
6. The Twist (activity-block twist)
7. Safety card (safety-card class)
8. Badge (badge-earn class)
9. Parent panel (collapsible, parent-panel class)
10. Session nav (prev/next buttons)

### AI Kids — programme details

**AI Starter** (8 sessions, ages 7–10, 25 min each)
S1: What is AI? | S2: Give AI a Job | S3: AI Tells Stories | S4: Make a Quiz
S5: Catch AI Lying | S6: Plan Something Fun | S7: Better Questions | S8: Graduation

**AI Explorer** (16 sessions, ages 8–11, 25 min each)
S1: AI Toolkit | S2: AI & Hobbies | S3: AI Explains Homework | S4: Debate Partner
S5: Research with AI | S6: Prompt Engineering | S7: AI in Real World | S8: AI & Feelings
S9: Creative Writing 2 | S10: AI & Maths | S11: AI & Languages | S12: Teach AI to Fail
S13: AI Ethics | S14: AI & Images | S15: AI Project | S16: Graduation

**AI Builder** (24 sessions, ages 10–13, 30 min each)
Month 1 (S1–S8): How AI Works, System Prompts, Structured Outputs, AI Bias,
  AI Safety & Society, AI for Data, AI for Communication, Month 1 Review
Month 2 (S9–S16): AI & News, Chain Prompting, Problem Solving, Building a Character,
  AI & Environment, AI & Future, AI & Storytelling, Month 2 Review
Month 3 (S17–S24): Advanced Prompting, AI in Workflows, Your Voice with AI,
  AI for Good, Capstone Part 1, Capstone Part 2, Capstone Part 3, Graduation

**AI Monthly — Full year (12 months, 48 sessions — all live)**
May: AI Basics Refresher | June: AI and Animals | July: AI and Space | August: AI and Cooking
September: AI and Art | October: AI and Stories | November: AI and Sport | December: AI and the Holidays
January: AI and Health | February: AI and History | March: AI and Money | April: AI and the Future

Each month = hub page + 4 sessions. All months are evergreen — any order, any time.
Hub: /ai-kids/monthly/ — rebuilt with full 12-month grid, all ✅ Live

---

## HOMEPAGE UPDATES (May 2026)

- Typewriter effect on headline — 5 phrases, 45ms/char, 22ms delete, hides cursor on load
- 14 WhatsApp-style prompt chips — including AI Kids chip (green) and WA.Expert chip
- 4th card added: AI Kids (green styling, links to /ai-kids/)
- AI Kids added to main nav (between AI Atlas and Courses, green colour)
- Hero search bar removed (was duplicating nav search) — only nav search remains
- WA.Expert cross-links: WhatsApp Marketing guide, Voice Agents hub, homepage chip

---

## WA.EXPERT CROSS-LINKS

- `/codex/social-media/whatsapp-marketing/` — green callout box + 4-card resource grid
- `/ai-atlas/specialist-tools/voice-agents/` — footer note about WA.Expert AI Integration
- Homepage — WA.Expert chip in prompt chips row

---

## NEW AI ATLAS PAGES (Sessions 9-13, April-May 2026)

**New specialist tool pages:**
- `/ai-atlas/specialist-tools/voice-agents/` ← new category hub
- `/ai-atlas/specialist-tools/voice-agents/vapi/`
- `/ai-atlas/specialist-tools/voice-agents/retell-ai/`
- `/ai-atlas/specialist-tools/voice-audio/sarvam-ai/`
- `/ai-atlas/specialist-tools/data-analysis/` ← new category hub
- `/ai-atlas/specialist-tools/data-analysis/julius-ai/`
- `/ai-atlas/specialist-tools/coding/lovable/`
- `/ai-atlas/specialist-tools/coding/replit/`
- `/ai-atlas/specialist-tools/images-design/higgsfield/`

**New concept guide pages:**
- `/ai-atlas/fine-tuning/` — What is Fine-Tuning?
- `/ai-atlas/vibe-coding/` — What is Vibe Coding?
- `/ai-atlas/ai-careers/` — How to Make Money with AI (ADAPT framework)

**Updated which-ai page:**
- Sections added for Data Analysis, App Building, Voice Agents, Vibe Coding, AI careers

### Session 12 — Final Comprehensive Audit (April 2026)
All issues resolved:
- ✅ 1 meta description over 165 chars (Sarvam AI) → fixed
- ✅ 8 voice-audio pages missing from sitemap → added (Whisper, Murf, Suno, Speechify, Udio, Resemble, AIVA, Beatoven)
- ✅ Which-AI page updated with Sessions 9-11 tools (Julius AI, Lovable, Vapi, Sarvam AI, Vibe Coding, Data Analysis, Voice Agents)
- ✅ All zeros: broken search, missing meta, missing GA4, EL bleed, junk files

**SITE IS COMPLETE.**







### Session 22 — May 2026 (60 Courses Complete)

**18 new courses built — total now 60:**

Career Tracks (6): SEO Specialist · PPC Specialist · Social Media Manager · Content Strategist · Marketing Analyst · AI Specialist

Marketing (6): Video Advertising · Marketing Analytics Advanced · International SEO · Mobile Marketing · PR & Communications · Retail & FMCG Marketing

AI (6): Gemini Masterclass · AI for Data Analysis · AI for Education · AI in Healthcare · AI in Finance · RAG and LLM Basics

**MILESTONE: 60 courses complete · 900 lessons · 3 tracks each**
Courses hub rebuilt with 5 filter tabs (All / AI / Marketing / Career / Kids)

**Final counts:** 978 HTML · 844 sitemap · 459 search

### Session 21 — May 2026 (20 More Courses — Total 42)

**20 new courses built:**
AI Automation · AI Business Productivity · AI for Coding · AI Research Tools
Technical SEO · AI Safety & Ethics · ChatGPT Masterclass · Vibe Coding
Claude Masterclass · Local SEO · Display Advertising · WhatsApp Marketing
Influencer Marketing · Growth Marketing · B2B Marketing · Brand Strategy
AI Kids Starter Guide · AI Kids Explorer Guide · AI Kids Builder Guide · AI Safety for Families

**Total: 42 courses live · 630 lessons · 3 tracks each**
Courses hub rebuilt with 4 filter tabs (All / AI / Marketing / AI for Kids)

**Updated counts:** 960 HTML · 826 sitemap · 441 search

### Session 20 — May 2026 (22 Courses Built)

**15 new courses built (22 total, 330 lessons):**
Affiliate Marketing · Content Marketing · CRO · E-commerce Marketing · Programmatic Advertising
Meta Ads · LinkedIn Ads · YouTube Marketing · TikTok Marketing
AI Image Generation · AI Video Tools · AI Voice and Audio · AI for Marketing
Prompt Engineering · Marketing Strategy

**Courses hub rebuilt:** 22 courses, filter by AI/Marketing, accurate stats

**Updated counts:** 940 HTML · 806 sitemap · 421 search

### Session 19 — May 2026 (Final Content + Learning Path)

**AI Kids Learning Path page built:**
- /ai-kids/learning-path/ — visual progression Starter → Explorer → Builder → Monthly
- Quick chooser by age, full path with session chips, FAQ, link from AI Kids hub

**New Codex guides (20 total):**
- Affiliate Marketing (8): Content Affiliate, SaaS Affiliate, Email Affiliate, B2B Affiliate, Fraud Prevention, Coupon/Deal, Programme Management, Influencer Affiliate
- Programmatic (6): Programmatic Direct, Header Bidding, Programmatic Audio, Contextual Targeting, CTV, Measurement & Viewability
- E-commerce (6): E-commerce SEO, Email Automation, Marketplace Strategy, Product Photography, Returns Management, International

**Updated counts:** 925 HTML · 791 sitemap · 406 search entries

### Session 18 — May 2026 (Courses + Educator Page)

**New courses built (4):**
- Social Media Marketing — 15 lessons, 3 tracks
- Email Marketing — 15 lessons, 3 tracks
- Analytics and Data — 15 lessons, 3 tracks
- AI Fundamentals — 15 lessons, 3 tracks

**Courses hub rebuilt:** 7 courses live, accurate stats, AI Kids in nav

**AI Kids Educator page:**
- /ai-kids/educators/ — classroom adaptation guide
- Downloadable Word doc: clarigital-ai-explorer-teacher-guide.docx
- Full classroom script for Session 5, safety briefing guide, parent template, quick reference card

**Stale search placeholder fixed:** "313 guides" → "360+ guides" across 43 pages

### Session 15 — May 2026 (All Monthly Months Built)

**AI Monthly programme completed:**
- June: AI and Animals (identification, conservation, research, challenge)
- July: AI and Space (exoplanets, universe, rover autonomy, challenge)
- August: AI and Cooking (recipes, food science, nutrition claims, challenge)
- September: AI and Art (image generation, visual description, art ethics, challenge)
- October: AI and Stories (structure, atmosphere, character voice, challenge)
- November: AI and Sport (statistics, scouting, probability, challenge)
- December: AI and the Holidays (gifts, cards, celebration planning, challenge)
- January: AI and Health (diagnosis, health data, claim evaluation, challenge)
- February: AI and History (primary sources, bias, AI recovering the past, challenge)
- March: AI and Money (money basics, finance AI, careers, challenge)
- April: AI and the Future (year reflection, predictions, manifesto, year-end project)

**Monthly hub rebuilt:** Full 12-month grid, all ✅ Live, evergreen — any order any time

**Updated counts:** 901 HTML pages · 767 sitemap URLs · 382 search entries

### Session 14 — May 2026 (AI Kids, LLM Infrastructure, Sitemap)

**AI Kids programme built (60 pages):**
- Smart onboarding quiz with personalised roadmaps and localStorage progress tracking
- AI Starter: 8 sessions (ages 7–10)
- AI Explorer: 16 sessions (ages 8–11)
- AI Builder: 24 sessions (ages 10–13) — 3 months, capstone project
- AI Monthly: May 2026 (4 sessions — AI Basics Refresher)
- Safety guide, Parent resources hub, all programme hubs

**Homepage updated:**
- Typewriter effect, 14 prompt chips, AI Kids 4th card, AI Kids in nav

**LLM infrastructure (new files):**
- llms-full.txt, sitemap-llm.xml, manifest.json, changelog.json, humans.txt
- .well-known/llm-context.json, schema-version.json, ai-plugin.json
- llms.txt rewritten with AI Kids section + all new pages

**Sitemap fixed:**
- 106 CSP task pages were missing — added
- sitemap.xml now has 712 URLs (covers all 846 pages)
- sitemap-llm.xml has 954 URLs with semantic type labels

**Quiz bug fixed:**
- Duplicate `const SCHEDULES` declaration caused entire JS to fail silently
- Q1 now has `visible` class hardcoded — shows without JS
- All onclick handlers verified working


### Session 8 — Final Audit Results (April 2026)
All issues resolved:
- ✅ 6 meta descriptions over 165 chars → fixed
- ✅ 134 CSP pages missing GA4 → GA4 added
- ✅ 3 definition pages missing from sitemap → added (priority 0.8)
- ✅ which-ai and family-tree missing from search index → added
- ✅ All zeros: broken search, missing meta, ElevenLabs bleed, junk files

## SESSION-END CHECKLIST

1. Update this MD file with any new pages, changed counts, new known issues
2. Verify nav links include Courses on all non-Codex pages
3. Verify search uses `data-search-input` / `data-search-results` (not id="navSearch")
4. Verify dark theme on specialist tool pages (`--bg:#0F172A`)
5. Verify light theme in curriculum additions (`#fff` cards, `#6B7280` text)
6. Verify no ElevenLabs template bleed on any new voice/audio pages
7. Verify schema markup on new pages
8. Update search-index.json with new page entries
9. Remove all junk files (`.DS_Store`, `.bak`, `.tmp`)
10. Rezip and present file
11. State what was built/changed
12. End with IST timestamp

---

## STARTER PROMPT FOR NEW CHAT

```
You are continuing work on clarigital.com — a free digital marketing and AI education website.

Read CLARIGITAL-MASTER.md fully before doing anything.
The user will provide a zip file of the current site — unzip it first.

Key facts:
- 100% static HTML, no build process needed
- 846 HTML pages as of 06 May 2026
- Two nav types: white nav (Codex) → navy logo text, dark nav (everything else) → white logo text
- Two colour themes: dark (#0F172A) for AI Atlas/courses, light cream (#FEF3EC) for Codex/Curriculum
- Nav search uses data-search-input / data-search-results attributes (NOT id="navSearch")
- NEVER use ElevenLabs page as template for new voice pages — use agentic-ai or crewai pages
- When editing Codex business-strategy pages, update BOTH flat .html and /index.html versions
- Curriculum additions must use light theme colours, not dark theme
- Update CLARIGITAL-MASTER.md at the end of every session before delivering the zip
- Always end responses with IST timestamp
- Package as zip at session end with no .DS_Store, .bak, or .tmp files

Today's task: [DESCRIBE WHAT YOU WANT TO DO]
```

---

## BUILD STATUS — ALL SECTIONS

### Agentic AI
| Page | Status |
|---|---|
| `/ai-atlas/agentic-ai/` | ✅ Built |
| `/ai-atlas/agentic-ai/how-agents-work/` | ✅ Built |
| `/ai-atlas/agentic-ai/multi-agent-systems/` | ✅ Built |
| `/ai-atlas/specialist-tools/agentic-frameworks/` | ✅ Built |
| `/ai-atlas/specialist-tools/agentic-frameworks/langchain/` | ✅ Built |
| `/ai-atlas/specialist-tools/agentic-frameworks/crewai/` | ✅ Built |
| `/ai-atlas/specialist-tools/agentic-frameworks/autogen/` | ✅ Built (maintenance mode noted) |
| `/ai-atlas/specialist-tools/agentic-frameworks/llamaindex/` | ✅ Built |

### Voice & Audio
| Page | Status |
|---|---|
| `/ai-atlas/specialist-tools/voice-audio/elevenlabs-pro/` | ✅ Built (original) |
| `/ai-atlas/specialist-tools/voice-audio/whisper/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/murf/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/suno/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/speechify/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/udio/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/resemble-ai/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/aiva/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/beatoven/` | ✅ Built April 2026 |
| `/ai-atlas/specialist-tools/voice-audio/adobe-podcast/` | ✅ Built (original) |
| `/ai-atlas/specialist-tools/voice-audio/descript-audio/` | ✅ Built (original) |
| `/ai-atlas/specialist-tools/voice-audio/otter/` | ✅ Built (original) |

### Courses
| Page | Status |
|---|---|
| `/courses/` | ✅ Built |
| `/courses/agentic-ai/` | ✅ Built |
| `/courses/seo/` | ✅ Built |
| `/courses/google-ads/` | ✅ Built |

### Infrastructure
| File | Status |
|---|---|
| `sitemap.xml` (712 URLs) | ✅ Rebuilt May 2026 |
| `llms.txt` (full entity map) | ✅ Rebuilt April 2026 |
| `robots.txt` (all AI crawlers) | ✅ Rebuilt April 2026 |
| `_headers` (Cloudflare cache) | ✅ Created April 2026 |
| `_redirects` | ✅ Created April 2026 |
| `search-index.json` (338 entries) | ✅ Updated April 2026 |

### Definition Pages
| Page | Status |
|---|---|
| `/what-is-digital-marketing/` | ✅ Built April 2026 |
| `/what-is-seo/` | ✅ Built April 2026 |
| `/what-is-ai/` | ✅ Built April 2026 |

### AI Tools Built in Session 4
| Tool | URL | Status |
|---|---|---|
| Meta AI | `/ai-atlas/tools/meta-ai/` | ✅ Built April 2026 |
| Claude.ai consumer guide | `/ai-atlas/tools/claude-ai/` | ✅ Built April 2026 |
| Gemini Advanced | `/ai-atlas/tools/gemini-advanced/` | ✅ Built April 2026 |

### Specialist Tools Built in Session 5
| Tool | URL | Status |
|---|---|---|
| Flux | `/ai-atlas/specialist-tools/images-design/flux/` | ✅ Built April 2026 |
| Luma Dream Machine | `/ai-atlas/specialist-tools/video/luma/` | ✅ Built April 2026 |
| Wordtune | `/ai-atlas/specialist-tools/writing-content/wordtune/` | ✅ Built April 2026 |
| QuillBot | `/ai-atlas/specialist-tools/writing-content/quillbot/` | ✅ Built April 2026 |
| InVideo AI | `/ai-atlas/specialist-tools/video/invideo/` | ✅ Built April 2026 |

### Pages Needing Work
| Page | Issue | Status |
|---|---|---|
| `/ai-atlas/which-ai/` | Expanded — Coding/Voice/Video/Agentic AI/Meta AI sections + 12-tool table | ✅ Done April 2026 |
| `/ai-atlas/family-tree/` | Rebuilt — 8 company cards + 15-event timeline + key concepts | ✅ Done April 2026 |

---

## KEY FACTS FOR CONTENT (verified April 2026)

### Agentic AI
- OWASP Top 10 for Agentic AI (2026) — primary risk: prompt injection
- EU AI Act Regulation 2024/1689 high-risk provisions take full effect August 2026
- Model Context Protocol (MCP) — Anthropic, adopted by LangGraph/CrewAI/Claude
- AutoGen: maintenance mode only, merging into Microsoft Agent Framework (AG2)
- LangSmith pricing: Free (5k traces/month), Developer $39/user/mo, Plus $299/user/mo
- CrewAI: Free, open source MIT. Enterprise: custom pricing

### Voice & Audio
- Whisper: open source MIT, API $0.006/min, large-v3 = best model, arXiv:2212.04356
- Murf: $29/month Creator (annual), $99/month Business (annual)
- Suno: ⚠️ Copyright litigation — RIAA v. Suno filed June 2024, ongoing April 2026
- Udio: ⚠️ Same litigation — RIAA v. Udio filed June 2024, ongoing April 2026
- Speechify: $139/year Premium, $239/year AI Studio (voice cloning)
- Resemble AI: Voice cloning from 3 min audio, real-time conversion, Resemble Detect
- AIVA: Free plan = AIVA owns copyright. Pro (€33/month) = user owns copyright. SACEM registered 2017
- Beatoven: From $6/month (annual). Founded Bengaluru 2021

### Pricing to verify on next session
- Relay.app: Free / $38 / $138 / Enterprise (old pricing may still be in original Relay guide)
