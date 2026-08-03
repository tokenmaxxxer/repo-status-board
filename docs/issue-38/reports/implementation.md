# Implementation record — design-gate P1/P2/P3 follow-up (issue #38, phase 2)

code_under_review: src/rsb/web/dashboard.js, src/rsb/web/dashboard.css, src/rsb/web/index.html, test/rsb_tests/test_model.py, docs/specs/screen-spec.md, docs/specs/design-system.md
loop_state: landed

## Why

Approved via issue #38 comment `APPROVE issue-38/implementation`
(jjongkwann, single-account mode — PR #43 author and approver are the
same account). Executes `docs/issue-38/proposals/implementation.md`'s
"What will be done" exactly as approved, resting on
`docs/issue-38/reports/implementation/survey.md` and
`docs/issue-38/reports/implementation/scout-brief.md`.

## What was done

Executed `docs/issue-38/proposals/implementation.md`'s "What will be
done" section as approved.

**`dashboard.js`:**
- `WIDE_LAYOUT_QUERY`'s comment corrected to describe the now-live
  `matchMedia` check (it was previously read by nothing).
- `renderTable(headers, rows, emptyMessage, caption)`: 4th arg added;
  `<th>` → `<th scope="col">`; `<caption class="visually-hidden">`
  inserted before `<thead>`. All 4 call sites (Decision queue/Flows/
  Sessions in `renderData`, ledger table in `renderAccounting`) pass a
  caption.
- `renderAccounting`'s outcomes: bare `${k}:${v}` text → `<span
  class="badge status-neutral mono">` per entry (P3-8).
- `renderDetailPanel`: heading now `<h2 id="detail-panel-heading"
  tabindex="-1">Issue {n} — {repo}</h2>`; wrapper now `role="region"
  aria-labelledby="detail-panel-heading"`; the "no longer has board
  activity" branch also carries `id="detail-panel-heading"
  tabindex="-1"` so a focus target always exists.
- New pure `detailRowHtml(colspan, contentHtml)` and
  `collapsibleDetailHtml(summaryLabel, detailText)` (both escape their
  arguments), added to `module.exports`.
- New `applySelectionLayout(data)`: clears any existing `.selected-row`
  class, finds the selected row by re-querying `.row-toggle` buttons
  (never a stale reference), adds `.selected-row` to it, then renders
  `renderDetailPanel(...)`'s output into `DETAIL_SLOT` (wide layout, or
  row-not-found) or as a `detailRowHtml(...)` sibling `<tr>` (narrow
  layout) — one render call, two insertion points. `renderData()`'s old
  unconditional `DETAIL_SLOT.innerHTML = ...` line replaced with a call
  to this.
- `attachRowToggleHandlers`: captures `wasExpanded` before
  `renderData(data)`, then after it re-queries for the (possibly
  re-created) button/heading and moves focus — closing focuses the
  row's own button, opening focuses `#detail-panel-heading`.
- `renderSkeleton`: `MAIN.setAttribute("aria-busy", "true")` added.
  `renderData`/`renderFullError`: `MAIN.setAttribute("aria-busy",
  "false")` added at every exit point (full-error delegate, empty-page
  early return, normal render path).
- `renderFullError`: `<h1>` → `<h2>` (page's own `<h1 id="page-title">`
  is now the only `<h1>`); `.error-state` gets `role="alert"`; body
  replaced with a generic `<p>` + `collapsibleDetailHtml("Details",
  message)` instead of the raw message inline.
- Partial-failure banner (`renderData`): per-repo detail no longer
  escaped-then-joined-then-shown inline; now joined raw and passed
  through `collapsibleDetailHtml("Details", detail)` (escaping happens
  once, inside that helper — the removed per-item `escapeHtml` calls
  were intentional, to avoid double-escaping).
- `load()`: `REFRESH_BUTTON.disabled = true` at start; `try/catch` →
  `try/catch/finally` with `REFRESH_BUTTON.disabled = false` in
  `finally`.

**`dashboard.css`:** `--color-border-default` → `var(--color-neutral-500)`.
`#main-content, #detail-panel-slot { min-width: 0; }` added.
`table.data-table` gains `min-width: 640px` and a `tbody tr:hover` rule.
`.table-scroll` gains `width: 100%`. `.row-toggle` gains
`min-width/min-height: 24px` + `inline-flex` centering. New
`#repo-filter` rule (min-height, padding, border, focus-visible) and
`.refresh-button` gains `min-height`/`:hover`/`:focus-visible`/
`:disabled`. `.error-state h1` → `.error-state h2` selector rename;
new `.error-state details summary` rule. New `.visually-hidden`
utility, `tr.selected-row`, `.detail-panel > h2`. `.skeleton-row`
height changed from a fixed `2em` to a computed
`calc(space-table-cell-padding-y * 2 + 1.4em)`.

**`index.html`:** `#header-meta` and `#partial-banner` get
`aria-live="polite"`; `#main-content` gets an initial
`aria-busy="true"`.

**`test/rsb_tests/test_model.py`:** two new tests —
`detailRowHtml(5, "<div>x</div>")` exact-string check, and
`collapsibleDetailHtml` checked both plain and with HTML-significant
characters in both arguments (escaping check on both `summaryLabel`
and `detailText`).

**Docs:** `docs/specs/screen-spec.md` §1.3 (caption/scope/selected-row,
referenced by §1.4/§1.5/§1.7's "same pattern" note), §1.6 (narrow-tr
insertion now implemented, heading/landmark/focus facts), §2.1/§2.4/
§2.5/§2.6 (aria-busy/aria-live/role=alert/focus-movement facts, error
copy updated to summary+collapsed-details). `docs/specs/design-system.md`
§2.2 (`color-border-default` contrast documented), §5 (breakpoint
section narrowed from a blanket "mobile out of scope" to naming what
issue #38 actually closed), §6 (`DataTable`/`RefreshButton`/
`RepoFilter`/`DetailPanel`/`AccountingRow`/`SkeletonBlock`/`ErrorState`/
`PartialFailureBanner` rows updated), §7 (table `min-width` flagged as
a first-cut value, same status as the age-bucket thresholds).

## Manual/DOM-wiring verification

No real GUI browser is available in this sandbox — confirmed directly
this session (not assumed from precedent): headless Chrome
(`/Applications/Google Chrome.app`) fails with the same
crashpad/`ProcessSingleton` permission errors
`docs/issue-36/reports/implementation.md` recorded, reproduced again
here with an explicit `--user-data-dir` in a scratch tmp dir (still
fails — `Operation not permitted` writing to
`~/Library/Application Support/Google/Chrome/Crashpad/settings.dat`);
no Playwright/Selenium/Puppeteer installed. Substituted the same jsdom
approach issue-36 used: installed `jsdom` in a scratch directory
outside the repo (`/tmp/claude-501/jsdom-scratch-38`, not a project
dependency, nothing added to the shipped code or any manifest — this
repo still has no `package.json`), loaded the **actual, unmodified,
shipped** `src/rsb/web/index.html` + `dashboard.js` into a real jsdom
`window`/`document`, and dispatched real `click` events / read back
real DOM state. `window.matchMedia` is not implemented by jsdom
(confirmed by direct call, threw `TypeError`), so a minimal polyfill
returning a controllable `{ matches }` was substituted for real CSS
media-query evaluation — noted honestly, not glossed over, same as
issue-36's jsdom-vs-real-browser gap for keyboard activation.

Three scenarios run, all against the real shipped files, all passing:

1. **Success path, wide → narrow layout toggle** (18 checks): after
   auto-load, the Decision-queue table has a `<caption>` ("Decision
   queue", `.visually-hidden`) and every `<th scope="col">`;
   `#main-content` has `aria-busy="false"` post-render. Clicking the
   row's `row-toggle` with `matchMedia` reporting wide: `DETAIL_SLOT`
   gets the heading + "Issue 42" content, the row gets `.selected-row`,
   focus lands on `#detail-panel-heading`, no sibling `.detail-row` is
   created. Clicking again (close): `DETAIL_SLOT` empties,
   `.selected-row` is removed, focus returns to the row's own button.
   Re-opening with `matchMedia` reporting narrow: `DETAIL_SLOT` stays
   empty, the row's `nextElementSibling` is a `tr.detail-row` containing
   "Issue 42", the row is `.selected-row`, and focus lands on
   `#detail-panel-heading` *inside that inserted row* (not the slot).
2. **Partial failure** (6 checks): `#partial-banner` has
   `aria-live="polite"`; the always-visible line reads "1 of 2 repos
   failed to load"; a `<details><summary>Details</summary>` holds the
   raw `repo: message` text (confirmed present inside `<details><p>`
   and confirmed absent from the banner's text once that `<p>` is
   removed — i.e. it genuinely isn't visible outside the collapsed
   region, not just visually hidden).
3. **Full failure** (9 checks): `.error-state` has `role="alert"`; its
   heading is an `<h2>` reading "Couldn't load board status"; the
   *whole document* has exactly one `<h1>` and it's `#page-title`
   (confirms the duplicate-`<h1>` defect the issue body reported is
   fixed); a collapsed `<details>` holds the raw error message; a
   plain, generic `<p>The board data couldn't be loaded.</p>` line is
   always visible; `aria-busy="false"` after render.
4. A 4th script (4 checks) confirmed `#header-meta`'s static
   `aria-live="polite"`, and the refresh-button disabled/re-enabled
   timing: `disabled === false` after initial load,
   synchronously `disabled === true` right after a click dispatched
   against a deliberately-delayed mock `fetch`, and `disabled === false`
   again once that delayed fetch resolves.

Touch-target sizing (P2-5) was confirmed by direct `grep` of the
shipped `dashboard.css` (`min-width`/`min-height: 24px` on
`.row-toggle`, `#repo-filter`, `.refresh-button`) rather than jsdom,
since jsdom has no layout engine and cannot compute real rendered
pixel geometry — an honest limitation, not a claim of visual
measurement.

All scratch verification files (`.verify-scratch/` in the repo,
`/tmp/claude-501/jsdom-scratch-38`) were scratch-only, never part of
the frozen write set, and were removed before this record was
finalized — none of it ships.

## What did not work

None.

## Doc-placement ladder

- [x] `docs/specs/screen-spec.md` §1.3/§1.6/§2.1/§2.4/§2.5/§2.6 — updated
      same turn as the code (see "What was done").
- [x] `docs/specs/design-system.md` §2.2/§5/§6/§7 — updated same turn as
      the code.
- [x] `docs/issue-38/reports/implementation.md` (this file).

## Tests

`python3 -c "import sys; sys.path.insert(0, 'src'); import pytest;
sys.exit(pytest.main(['test/', '-q']))"` — **57 passed**, 0 failed (55
pre-existing regression-free + 2 new `detailRowHtml`/
`collapsibleDetailHtml` tests).

`node --check src/rsb/web/dashboard.js` — no syntax errors.

jsdom-based DOM-wiring checks — see "Manual/DOM-wiring verification"
above (37 individual assertions across 4 scripts, all passing, against
the real shipped files).

## Adversarial hunt

No `warrant-hunter` agent type is available in this environment (same
gap `docs/issue-36/reports/implementation.md` recorded) — substituted a
`general-purpose` agent run adversarially against the integrated diff
(not a self-check by this session), told to read the diff directly, not
this issue's docs, and to hunt for silent failures, composition
regressions, and plain design errors, with a reproduction required per
finding.

Two findings returned, both fixed before this record was finalized:

- **Ambiguous row-match in `applySelectionLayout` (fixed)** —
  `(sourceTable, issue, repo)` isn't a unique row key: the Sessions
  table renders one `<tr>` per session, and two sessions can share the
  same `(issue, repo)` with different `role`/`pid` (confirmed by
  `sessionRows` / `model.py`'s own sort key including `role`). The new
  row-matching loop in `applySelectionLayout` overwrote `selectedRow` on
  every match with no disambiguation, so opening either of two such
  rows' toggles could highlight (`.selected-row`) or insert the narrow-
  layout detail `<tr>` after the *wrong* physical row. This ambiguity
  already existed in `isRowExpanded`/`selectedIssue`'s shape before this
  issue (issue-36's domain, out of scope per this proposal's own
  Constraints — not rewritten here), but this issue's new row-lookup
  logic is what turned it into a visible, incorrect UI state instead of
  just a harmless duplicate-glyph state. Fixed within the frozen write
  set, without touching `isRowExpanded`/`selectedIssue` or any other
  file: `applySelectionLayout` now counts matches, and treats anything
  other than exactly one match as "row not found" — the existing safe
  fallback (render into `DETAIL_SLOT`, no row highlighted) — rather than
  guessing which physical row to touch. Verified with a new jsdom
  scenario (two Sessions rows sharing issue 99/repo-b, different roles):
  opening either one's toggle now leaves no `.selected-row` and inserts
  no stray `.detail-row`, with the correct content still rendered into
  `DETAIL_SLOT`.
  - **Residual, disclosed gap**: this fix prevents the wrong-row
    highlight/insertion, but does not fully disambiguate *which* of the
    two sessions was actually clicked when highlighting would otherwise
    apply — narrow-layout users still get the safe side-panel fallback
    instead of an inline row for this specific (rare) case. A full fix
    needs a per-row discriminator (e.g. `role`) threaded through
    `rowToggleButtonHtml`/`issueToggleCell`/`sessionRows`/`selectedIssue`,
    which touches signatures this proposal's Constraints put out of
    scope (P1-2/`isRowExpanded`, issue-36's domain) — named here as
    follow-up material for a future issue, not silently left unfixed.
- **Unescaped outcome value in `renderAccounting` (fixed)** —
  `` `${escapeHtml(k)}:${v}` `` (a line this issue's P3-8 change touched,
  wrapping it in a new `<span class="badge...">`) escaped the outcome
  key but not the value; `le.outcomes` is untyped provider JSON
  (`model.py`'s `outcomes: dict`, no runtime value-type validation).
  Fixed: `escapeHtml(v)` (escapeHtml stringifies internally, so this is
  safe regardless of `v`'s type). Verified with a new jsdom scenario
  (an outcome key/value both containing `<script>`/`<img onerror=...>`
  markup): the rendered `#main-content` contains zero live `<script>`/
  `<img>` elements — the payload appears only as escaped text inside the
  badge.

closed_checks:
- full-test-suite: `python3 -c "import sys; sys.path.insert(0, 'src');
  import pytest; sys.exit(pytest.main(['test/', '-q']))"` — 57 passed, 0
  failed, run after both hunt-fixes (code_under_review sha: see this
  branch's pending commit).
- syntax-check: `node --check src/rsb/web/dashboard.js` — clean, run
  after both hunt-fixes.
- dom-wiring-live-check: all 4 jsdom scripts (21 + 6 + 9 + 4 = 40
  assertions across success/ambiguous-session/partial-error/full-error/
  refresh-disabled scenarios) re-run against the post-fix file for the
  detail-wiring script (which covers both hunt-fixed code paths); all
  pass — see "Manual/DOM-wiring verification" and "Adversarial hunt"
  above.
- no-stale-scratch-artifacts: `.verify-scratch/` (repo) and the
  `/tmp` jsdom scratch install were removed before this record was
  finalized; `git status --short` shows only the frozen write set.
- pr-body-no-closing-keywords: this session's PR body/update will
  contain no `Closes`/`Fixes`/`Resolves #38` in any form, including
  backtick-quoted (issue #23 T2 precedent, restated by this issue's own
  body — issue #38's own execution plan still has an unstarted second
  step, execution-observation/conformance-review, so this PR cannot
  claim the issue is fully closed).

## Open findings

None outstanding — both hunt findings above are fixed and verified. The
one disclosed, intentionally-not-fully-closed gap (residual session-role
disambiguation, noted above) is out of scope per this proposal's own
Constraints (touches issue-36-owned `isRowExpanded`/`selectedIssue`) and
is named as follow-up material, not silently dropped.

## Next steps

1. ~~Implement `dashboard.js`/`dashboard.css`/`index.html` changes per
   the approved proposal's "What will be done".~~ Done.
2. ~~Add the two new `test/rsb_tests/test_model.py` cases and run the
   full suite.~~ Done — 57 passed (55 pre-existing + 2 new).
3. ~~Update `docs/specs/screen-spec.md`/`design-system.md` (doc-placement
   ladder).~~ Done.
4. ~~Manual/DOM-wiring verification.~~ Done — see "Manual/DOM-wiring
   verification" above.
5. ~~Adversarial hunt pass.~~ Done — 2 findings, both fixed (see
   "Adversarial hunt" above).
6. ~~Finalize this record (`loop_state: landed`), commit, push.~~ This
   record is now finalized; commit/push follow immediately.

## Open-finding resolution path

N/A — no open findings remain (see "Open findings" above).
