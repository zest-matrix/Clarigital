# Build scripts — Clarigital

These generate and verify the site. In a fresh session, copy them to /tmp first:

```bash
cd /home/claude/audit/<site root>
cp _build/*.py /tmp/
```

| Script | Purpose |
|---|---|
| `fintech_builder.py` | Fintech AI pages and Build Sheets (sticky left rail, consolidated depth bands) |
| `course_builder_v3.py` | Courses. Has hard URL validation via `vurl()` |
| `guide_builder.py` | Codex guides and section hubs |
| `atlas_builder.py` | AI Atlas concept pages (dark theme) |
| `tool_builder.py` | AI Atlas tool pages |
| `linkcheck.py` | `scan()` — broken internal links |
| `structcheck.py` | `check()` — HTML structure, orphans, **div balance** |
| `rendercheck.py` | `render_check()` — content visible without JS, depth bands, JS syntax · `handler_check()` — **inline `onclick=` attributes: JS syntax + undefined handlers** · `inline_hidden_check()` — inline `display:none` on togglable content · `thin_content()`, `stale_stamps()` metrics |
| `rebuild_infra.py` | sitemap, search-index, llms-full, manifest |
| `audit.py` | The **17**-check table. **Run before every package.** |
| `bs04_aml.py` | Session 47 build script for the AML Build Sheet. Reference for Build Sheets 05–09. |
| `meta_sweep.py` | Adds missing OG / Twitter / JSON-LD / BreadcrumbList |
| `fix_quiz.py` | Session 47b one-off. Repaired 6 quiz defects across 68 courses. Kept as a reference pattern for verified-before-write bulk edits. |
| `c_style.txt`, `c_script.txt` | **Templates `course_builder_v3.py` requires.** Were /tmp-only until Session 47b, which made the builder unrunnable in a fresh session. |
| `migrate_courses.py`, `consolidate.py`, `cons_atlas2.py` | One-off migrations, kept as reference patterns for balanced HTML extraction |

## Dates — set these every session

`fintech_builder.py` carries two module constants. They were hardcoded to May 2026 until
Session 47, which meant every page built after May shipped a stale verification stamp.

```python
VERIFIED = 'September 2026'   # hero meta-tag + default for registry() blocks
DATEMOD  = '2026-09-13'       # JSON-LD dateModified
```

`rebuild_infra.py` now derives sitemap `lastmod`, the `llms-full.txt` header and
`manifest.last_updated` from the system clock. Nothing to set.

## Templates — all 12 are now bundled here

Four of the five page builders read their stylesheet, nav, footer and script templates from
`/tmp/*.txt` and **none of those files was ever bundled**, so those builders could not run in a
fresh session. That is the root cause of the Session 47b quiz failure: the generator and the
stylesheet were free to drift because nobody could load them together.

`atlas_style.txt` · `atlas_nav.txt` · `atlas_footer.txt` · `codex_style.txt` · `codex_nav.txt` ·
`tool_style.txt` · `tool_nav.txt` · `tool_footer.txt` · `tool_scripts.txt` · `c_style.txt` ·
`c_script.txt` · `c_nav.txt`

Each builder resolves `_build/` first, then falls back to `/tmp`, then raises.

**Provenance — read before regenerating anything.** These were reconstructed from live pages, not
recovered from the originals. Seven were byte-identical across every page of their type and are
safe. **Five had multiple live generations and hold the _dominant_ variant only:**

| Template | Variants live | Dominant |
|---|---|---|
| `atlas_style.txt` | **12** | 52 / 155 pages |
| `atlas_footer.txt` | 19 | 22 / 155 pages |
| `c_nav.txt` | 3 | 52 / 64 pages |
| `tool_scripts.txt` | 3 | 15 / 23 pages |

Regenerating an AI Atlas page will therefore restyle it to the majority template. That may be what
you want — 12 stylesheet generations in one section is itself a defect — but **do it deliberately
and diff the output**, do not assume a regenerated page matches what was there.

## Why there are 17 checks, not 15

Session 47b: four live bugs passed all 15 checks because **nothing inspected inline event
attributes**. `node --check` only ever saw `<script>` blocks, so 1,560 Python booleans written into
`onclick="checkAnswer(this,True)"` were invisible, and `checkAnswer` was never defined at all.

- **Inline handler errors** — every `on*="..."` must parse as JS, and every top-level function it
  calls must exist on the page. Match **top-level calls only**; a naive `\b\w+\(` flags
  `document.getElementById` and `rgba(` inside style strings (218 false positives vs 1 real).
- **Inline-hidden content** — `style="display:none"` always beats a `.open` / `.active` class.

`structcheck` also balances every block tag now, not just `<div>`. Session 48 found **22 pages with
a stray `</header>`** and no opener, and **3 codex pages that never closed `<main>` or `<section>``**.
Browsers silently repair all of it; HTML parsers and LLM crawlers do not, and this site exists to be
machine-readable.

## Writing build-sheet content — one trap that has cost two builds

`note()` and `warn()` are called from inside f-strings. **A backslash cannot appear inside an
f-string expression**, so `warn("... \\"quoted\\" ...")` is a SyntaxError, not a runtime error —
the whole build script refuses to parse. It cost a session in 47 and again in 50.

Use HTML entities for quotes in any string passed to `note()`, `warn()` or `registry()`:

```python
warn("track &ldquo;wrong answer given&rdquo; as a share of escalations")   # correct
warn("track \\"wrong answer given\\" as a share of escalations")           # SyntaxError
```

Same rule for apostrophes inside single-quoted f-strings. Entities always work; escapes do not.

## Usage

```bash
cd /home/claude/audit/<site root>
python3 /tmp/rebuild_infra.py
python3 /tmp/audit.py                 # all 15 checks must read 0
python3 -c "exec(open('/tmp/linkcheck.py').read()); scan()"
```
