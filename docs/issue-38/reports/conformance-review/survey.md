# Conformance-review survey (issue #38, phase 1)

Subject: issue #38. Branch: `issue-38/conformance-review`. Current-state
survey only — no verdicts, no pass/fail, no quality judgment.

## Artifact under review

PR #43 landed as one squashed merge commit `f3539107628a3a519eefe2f45b0e8d6f766a7912`
(`f353910`), jjongkwann, 2026-08-03T21:25:48+09:00, directly on `main`
between `b621082` (issue-36/#37) and `7bca5be` (issue-27). Its commit
message contains two trailer paragraphs — "issue-38 phase 1: ...survey +
proposal" and "issue-38 phase 2: mobile overflow, inline detail row,
live regions, touch targets, error UX" — i.e. phase 1 (building role's
own proposal/survey) and phase 2 (the code) are one commit; `git diff
--stat f353910^ f353910` is the only way to isolate phase-2 content.

`git diff --stat f353910^ f353910` (10 files, 1311(+)/81(-)):

| File | +/- |
|---|---|
| `docs/issue-38/proposals/implementation.md` | 327 (new) |
| `docs/issue-38/reports/implementation.md` | 303 (new) |
| `docs/issue-38/reports/implementation/scout-brief.md` | 123 (new) |
| `docs/issue-38/reports/implementation/survey.md` | 224 (new) |
| `docs/specs/design-system.md` | +65/-8 |
| `docs/specs/screen-spec.md` | +70/-8 (78 changed) |
| `src/rsb/web/dashboard.css` | +82/-5 |
| `src/rsb/web/dashboard.js` | +113/-26 |
| `src/rsb/web/index.html` | +3/-3 |
| `test/rsb_tests/test_model.py` | +32 (new tests only) |

**Scope boundary.** The frozen contract names six files as artifact
under review: `dashboard.js`, `dashboard.css`, `index.html`,
`screen-spec.md`, `design-system.md`, `test_model.py`. The other four
(`docs/issue-38/proposals/implementation.md` and the
`docs/issue-38/reports/implementation*` tree) are the building role's
own process artifacts — read as adjacent context (§5), not as code/spec
under review.

**P1-2 confirmed out of scope from git history.** Issue #38's body
assigns P1-2 (toggle wiring: real `<button>`, `sourceTable` tracking,
working `aria-expanded`/`aria-controls`) to issue #36/PR #37. `b621082`
("issue-36 ... row-toggle relocation (#37)") merged 2026-08-03T20:30:29
+09:00, 55 minutes before `f353910`, i.e. already on `main` when PR #43
opened. Its commit body: "Fixes the pre-existing aria-expanded/
aria-controls wiring gaps ... (sourceTable was never tracked,
aria-controls pointed at a nonexistent id)." Current `isRowExpanded`/
`rowToggleButtonHtml` (`src/rsb/web/dashboard.js:200-239`) already carry
`sourceTable` and a fixed `aria-controls="detail-panel-slot"`, untouched
by the phase-2 diff (`js.diff` has no hunk on these functions).

## What the phase-2 diff changed, per surface

Pointers are `path:line` in the working tree; `f353910^` used to confirm
pre-diff absence where noted.

**P1-1 — mobile page-wide overflow.** `dashboard.css:181` —
`table.data-table` gains `min-width: 640px` (absent pre-diff).
`dashboard.css:205` — `.table-scroll` gains `width: 100%` (was
`overflow-x: auto;` only). `dashboard.css:372-374` — new `#main-content,
#detail-panel-slot { min-width: 0; }`. `screen-spec.md:49-52` and
`design-system.md:156-167` both narrate the same three-part fix, tagged
"issue #38 P1-1".

**P1-3 — narrow-screen (<1200px) inline detail row.**
`dashboard.js:464-466` — new pure `detailRowHtml(colspan, contentHtml)`
→ `<tr class="detail-row"><td colspan=...>`. `dashboard.js:485-526` —
new `applySelectionLayout(data)`: clears `.selected-row`, re-queries
`.row-toggle` buttons matching `selectedIssue`, and when exactly one
matches and `window.matchMedia(WIDE_LAYOUT_QUERY).matches` (`:16`,
`"(min-width: 1200px)"`) is false, inserts `detailRowHtml(...)` via
`insertAdjacentHTML("afterend", ...)` instead of `DETAIL_SLOT`. Pre-diff
`renderData` did an unconditional `DETAIL_SLOT.innerHTML = ...` with no
`matchMedia` call anywhere in the file (`js.diff`; §5 below has the
prior review's independent record of that pre-diff state).
`dashboard.js:642` — `renderData` now calls `applySelectionLayout`.
`dashboard.css:263-267` — `.detail-row td` rule, previously dead CSS,
now has an emitter.

**P1-4 — dynamic-state accessibility.** `index.html:13,20,24` —
`#header-meta`/`#partial-banner` gain `aria-live="polite"`;
`#main-content` gains initial `aria-busy="true"` (all absent pre-diff).
`dashboard.js:138` — `renderSkeleton` sets `aria-busy="true"`.
`dashboard.js:170,615,644` — `aria-busy="false"` set at three exit
points (`renderFullError`, empty-page return, normal `renderData` end).
`dashboard.js:161-171` — `renderFullError` gains `role="alert"`,
heading `<h1>`→`<h2>` (page's `<h1 id="page-title">` becomes sole
`<h1>`), message now behind `collapsibleDetailHtml(...)`.
`dashboard.js:448-449` — `renderDetailPanel` wrapper gets `role="region"
aria-labelledby="detail-panel-heading"`; heading is
`<h2 id="detail-panel-heading" tabindex="-1">`; the empty-state branch
(`:444`) carries the same id/tabindex. `dashboard.js:549-573` —
`attachRowToggleHandlers` now captures `wasExpanded`, then focuses the
re-queried toggle button (closing) or `#detail-panel-heading` (opening);
pre-diff ended at `renderData(data)` with no focus call (`js.diff`).

**P2-5 — touch targets (24×24px).** `dashboard.css:220-228` —
`.row-toggle` gains `min-width/min-height: 24px` + `inline-flex`
centering, comment cites WCAG 2.5.5. `dashboard.css:123,137-138` —
`.refresh-button`/`#repo-filter` gain `min-height: 24px`.
`design-system.md:176-179` cites "24×24px minimum size (issue #38
P2-5)" for all three.

**P2-6 — error-state cognitive load / internal-path exposure.**
`dashboard.js:474-476` — new `collapsibleDetailHtml(summaryLabel,
detailText)`, both args escaped, → `<details><summary>...</summary><p>...</p></details>`.
`dashboard.js:165` — `renderFullError` uses it (previously the raw
message was visible `<p>` text). `dashboard.js:600-610` — partial-banner
`detail` string now passed through `collapsibleDetailHtml("Details",
detail)` instead of interpolated directly; pre-diff had no `<details>`
on this path. `test_model.py:344-368` — two new tests
exact-string-asserting both helpers, incl. an HTML-escaping case.

**P2-7 — table/detail semantics + selected-row highlight.**
`dashboard.js:177` — `<th>`→`<th scope="col">`. `dashboard.js:183,188`
— new `<caption class="visually-hidden">` before `<thead>`; `renderTable`
gains a 4th `caption` param, all four call sites pass one
(`"Decision queue"` `:622`, `"Flows"` `:626`, `"Sessions"` `:630`,
`"Accounting ledger"` `:339`). `dashboard.css:89-99` — new
`.visually-hidden` clip-rect utility. `dashboard.js:448-449` — same
`role="region"` wiring as P1-4. `dashboard.js:486,516` —
`applySelectionLayout` adds/removes `.selected-row`. `dashboard.css:197-199`
— new `tr.selected-row { background: var(--color-status-info-background); }`.

**P3-8 — visual states/tokens.** `dashboard.css:20` —
`--color-border-default` `neutral-300`→`neutral-500` (contrast
≈1.47:1→4.6:1 per `design-system.md:68-73`, no new primitive).
`dashboard.css:125-135` — `.refresh-button:hover/:focus-visible/:disabled`
added. `dashboard.css:144-147` — `#repo-filter:focus-visible` added.
`dashboard.css:192-194` — `table.data-table tbody tr:hover` added.
`dashboard.css:291` — `.skeleton-row` height `2em`→
`calc(var(--space-table-cell-padding-y) * 2 + 1.4em)`. `dashboard.js:336`
— outcomes cells: bare `${escapeHtml(k)}:${v}` → `<span class="badge
status-neutral mono">${escapeHtml(k)}:${escapeHtml(v)}</span>` (also
newly escapes `v`). `dashboard.css:324,329-332` —
`.error-state h1`→`h2` selector rename; new `details summary` rule.
`dashboard.css:355-359` — new `.detail-panel > h2` rule.

## Verification surfaces available today

**Python suite.** `test/rsb_tests/` holds `test_cli.py`, `test_config.py`,
`test_dashboard_dom.py`, `test_fetch.py`, `test_model.py`,
`test_render.py`, `test_webserver.py`, `fixtures.py`. A bare `python3 -m
pytest test -q` fails (`ModuleNotFoundError: No module named 'rsb'` — no
installed package, no `conftest.py`). Using this repo's documented
convention (`docs/issue-38/reports/implementation.md:187-190`,
`docs/issue-29/reports/conformance-review.md:51-53`): `python3 -c
"import sys; sys.path.insert(0,'src'); import pytest;
sys.exit(pytest.main(['test/','-q']))"` → **57 passed, 8 skipped** in
3.71s, this session. `pytest -rs` shows all 8 skips are
`test_dashboard_dom.py:65`, `"jsdom is not installed; run npm install
--prefix test first"`. `node` is present (v26.5.1) but
`test/node_modules/` does not exist.

**`test_dashboard_dom.py`.** Not added by the diff under review — `git
log --follow` shows it landed in a later, separate squashed commit
`b2f6b637` ("issue-44 phase 1: DOM-layer test harness ... (#45)"),
after `f353910`; present in the working tree but not this artifact.
Mechanism: `_run_dom_js(script, fetch_body)` (`:51-95`) spawns `node -e`
per test, builds `new JSDOM(...)` from a 7-element HTML stub mirroring
`index.html`'s ids (`:40-48`), installs it as `global.window`/`document`,
stubs `fetch`, deletes+`require()`s `dashboard.js` fresh (firing the
`typeof window !== "undefined"` guard at `dashboard.js:671-678`), awaits
one tick, runs the script, returns JSON stdout. 8 tests: 3 on
repo-filter population (`:128-155`), 4 on `.row-toggle`/`aria-expanded`
(`:177-245`), 1 on `load()`'s fetch URL (`:254-259`). None exercise
`aria-busy`, focus movement, narrow-layout `<tr>` insertion
(`matchMedia`), `.selected-row`, `<caption>`/`scope="col"`, or
`collapsibleDetailHtml` in a live DOM — none target this review's
P1-3/P1-4/P2-6/P2-7 additions; its own traceability comments (`:20-23`)
name issue #29's two defects and issue #27's fetch gap, not issue #38.

**`test/package.json`/`package-lock.json`.** One dependency,
`"jsdom": "^30.0.1"`, full `lockfileVersion: 3` lockfile present. Not
runnable offline right now: `test/node_modules/` absent; installing
would need `registry.npmjs.org` (an allowed host here, but not attempted
— writing `test/node_modules/` is outside the owned path and the
package.json/skip-message already establish "is it wired").

**`.github/workflows/`.** One workflow, `deploy-board.yml` (cron +
`workflow_dispatch`): checkout, `pip install -e .`, `rsb --json`, copy
`src/rsb/web/*` + `board.json` into a Pages artifact, deploy. No
`pytest`/`npm install` step anywhere — no CI test gate for either suite.

## Evidence gaps and unknowns

Per issue #38 acceptance checkbox, what this sandbox cannot settle:

- **390px page-wide-scroll (P1-1).** No layout engine here (no headless
  Chrome — `docs/issue-38/reports/implementation.md:104-111` confirmed a
  crashpad/permission failure this same repo-session; jsdom has no
  layout engine or `matchMedia`, per that record). CSS values are
  readable (§2) but rendered/scrollable width at 390px isn't computable.
  Settles it: a real browser or working headless-Chrome/Playwright run
  measuring `scrollWidth` vs `innerWidth` at 390px.
- **<1200px inline detail placement (P1-3).** Code path/DOM insertion
  order are inspectable; whether it visually lands with no
  overlap/clipping at 1024px needs rendering. `test_dashboard_dom.py`
  doesn't exercise this branch (§3). Settles it: a
  jsdom+matchMedia-polyfill structural check plus a real browser render
  at 1024px for the visual claim.
- **Screen-reader announcement of loading/error/detail-open (P1-4).**
  `aria-live`/`aria-busy`/`role="alert"`/focus attributes are
  source/jsdom-inspectable; actual AT announcement timing/phrasing isn't
  producible by either (no accessibility tree/announcement queue).
  Settles it: a real VoiceOver/NVDA/JAWS session, or an automated AT
  tool (e.g. axe-core) against a rendered page.
- **24×24px touch targets on mobile (P2-5).** `min-width`/`min-height`
  declarations are grep-visible (as `docs/issue-38/reports/implementation.md:161-166`
  itself did — a grep, not a measurement); computed/rendered box size
  needs a layout engine. Settles it: `getBoundingClientRect()` from a
  real/headless browser at a mobile viewport.
- **Collapsed-by-default error/partial-failure detail (P2-6).**
  `<details>`/`<summary>` presence and escaping are directly tested
  (`test_model.py:344-368`); whether `<details>` actually renders
  visually collapsed by default is a browser-default behavior neither
  test file checks. Settles it: a rendered check of `details.open ===
  false` / the `<p>`'s visible state.
- **Table caption/scope + selected-row visual distinction (P2-7).**
  `<caption>`/`scope="col"` presence is source-verifiable (§2); whether
  `.visually-hidden` is actually screen-reader-only (not accidentally
  visible or unreachable) needs an AT session or accessibility-tree
  read. `.selected-row`'s rendered contrast is a pixel/contrast-checker
  question — `design-system.md:81-87` gives computed, not measured,
  ratios only.
- **"기존 테스트 전부 통과, 1440px 밀도 회귀 없음."** Test-pass half is
  directly checked (§3: 57/0/8). The 1440px visual-density-regression
  half needs a rendered screenshot vs. a pre-#38 baseline — not
  producible here.
- **PR-body closing-keyword / "browser-verified" process checkboxes.**
  Former is a `gh pr view 43` text check, not run in this survey
  (process/meta, not a code fact). Latter reduces to reading
  `docs/issue-38/reports/implementation.md`'s own disclosure (§5) that
  headless Chrome failed and jsdom was substituted as a non-real-browser
  proxy.

## Adjacent role records already on main

- **`docs/issue-38/reports/implementation.md`** (building role's
  self-report, `loop_state: landed`) and
  **`docs/issue-38/proposals/implementation.md`** (its approved
  proposal). Both read for §1/§2 corroboration and line pointers (e.g.
  its "Adversarial hunt" section naming the ambiguous-row-match and
  unescaped-outcome-value fixes, independently visible at
  `dashboard.js:494-514` and `:336`) — not accepted as a verdict source;
  this review works from artifact + spec.
- **`docs/issue-29/reports/conformance-review.md`** — prior
  conformance-review record, already on `main`. R4c bears directly on
  P1-1: `"R4c: no page-level horizontal scroll is structurally possible
  at narrow widths | Present | ... | Code/CSS inspection only — no
  narrow-viewport render was driven this session (no browser in this
  sandbox), matching ... docs/issue-4 and docs/issue-23"` (line 99). Its
  R7a/R7b (lines 121-122) independently found the pre-#38 narrow-screen
  inline-detail path Absent (dead `WIDE_LAYOUT_QUERY`, no `matchMedia`/
  `insertDetailRow`) — the gap P1-3 now has code for.
- **`docs/issue-44/proposals/test-authoring.md`** — issue #44's approved
  ADR for the jsdom harness (landed with its phase-2 code in the later
  squashed commit `b2f6b637`). What it unlocks: real-DOM event/state
  assertions with no browser binary, for the 3 items it actually
  delivered (§3). Explicitly excludes visual/screenshot regression and
  the P1-1 overflow class by design (`:210-218`: "jsdom does not
  implement layout ... structurally cannot detect a CSS-overflow
  regression"), and as landed does not cover P1-3/P1-4/P2-6/P2-7 (§3).
- **`docs/issue-36` material** — the P1-2-owning issue. Source for the
  git-history confirmation in §1; not read further since P1-2 is out of
  this review's scope.

## Open unknowns for the scout pass to aim at

- Does `applySelectionLayout`'s ambiguous-row-match guard
  (`dashboard.js:494-514`) correctly fall back for every multi-row case
  the four tables can construct, or only the Sessions
  same-`(issue,repo)`-different-`role` case the building role's own hunt
  found?
- Is any rendered-layout method available to a future pass — this
  survey found none (no headless Chrome, no Playwright/Selenium/
  Puppeteer) — or is the entire P1-1/P1-3/P2-5 visual-layer claim set
  Unverifiable-within-this-repo for phase 2?
- `registry.npmjs.org` is an allowed network host but jsdom isn't
  installed — is running `npm install --prefix test` in scope for a
  future pass, and would the *landed* `test_dashboard_dom.py` (8 tests,
  none touching P1-3/P1-4/P2-6/P2-7) plus a new hand-scripted jsdom
  probe be sufficient to structurally close that gap?
- Are the `design-system.md:70-73`/`:81-87` contrast figures (computed
  from documented hex values) worth independently recomputing with a
  contrast-checker tool, distinct from needing an actual browser?
- `test/package.json`/`package-lock.json` is this repo's first JS
  runtime dependency; `docs/issue-44/proposals/test-authoring.md:256-257`
  flags a still-open `.gitignore` hand-off for `test/node_modules/` —
  does its absence create any risk in a future session that does run
  `npm install`?
- Has `gh pr view 43`'s actual body been checked for GitHub
  closing-keyword grammar adjacent to `#38` (issue's own explicit
  checkbox, same precedent as issue #23 T2 / issue #29 R9)? Not run in
  this survey.
