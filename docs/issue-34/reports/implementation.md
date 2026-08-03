# Implementation record — owner/name propagation + GitHub links (issue #34, phase 2)

code_under_review: src/rsb/model.py, src/rsb/render.py, src/rsb/web/dashboard.js, src/rsb/web/dashboard.css, test/rsb_tests/fixtures.py, test/rsb_tests/test_model.py, test/rsb_tests/test_render.py, test/rsb_tests/test_webserver.py, docs/issue-34/decisions/owner-name-wire-format.md
loop_state: landed

## Why

Approved via issue #34 comment `APPROVE issue-34/implementation`
(jjongkwann, single-account mode — PR #35 author and approver are the
same account). This executes `docs/issue-34/proposals/implementation.md`'s
"What will be done" exactly as approved, resting on
`docs/issue-34/reports/implementation/survey.md` (current-state survey)
and `scout-brief.md` (external-link placement pattern). The issue's own
premise: `flows --json` payloads already carry `repo` (owner/name,
flows-schema.md §1), but `normalize_payload()` discarded it, so no
board.json consumer could build a GitHub link — this build threads
owner/name from payload to browser and adds the link affordances on top.

## What was done

Two independently-producible units under the contract the approved
proposal already froze (wire key `owner_name_by_repo`, JS helper
signatures, `.external-link` CSS class) — no waiting between them, no
shared mutable state:

**Unit A — Python wire-through** (`src/rsb/model.py`, `src/rsb/render.py`,
their tests, `test/rsb_tests/fixtures.py`,
`docs/issue-34/decisions/owner-name-wire-format.md`):
- `normalize_payload()` returns a new `"owner_name": payload.get("repo")`
  key. `BoardModel` gains `owner_name_by_repo: dict = field(default_factory=dict)`,
  the same shape as the pre-existing `generated_at_by_repo`.
  `merge_repos()` populates it right next to `generated_at_by_repo`, no
  value validation (falsy/`None`/non-string all pass through — the
  frontend's falsy check is the only guard, matching this codebase's
  existing convention of not format-validating other string fields).
- `render_json_model()` output gains one new top-level key:
  `"owner_name_by_repo": model.owner_name_by_repo`. Both `/api/board.json`
  and the static Pages `rsb --json` output go through this same function,
  so one change reaches both consumers (survey §3).
- Tests added: `normalize_payload()` returns `owner_name` correctly when
  `payload["repo"]` is present and when absent; `merge_repos()` fills
  `owner_name_by_repo` correctly (including the missing-key/`None` case,
  AC5 coverage); `render_json_model()` output matches; one
  `/api/board.json` spot-check in `test_webserver.py`.
  `test/rsb_tests/fixtures.py` gained `MISSING_OWNER_NAME_PAYLOAD`
  (a copy of `EMPTY_PAYLOAD` with `repo` removed) for the AC5 case.
- New decision doc `docs/issue-34/decisions/owner-name-wire-format.md`
  records the additive `board.json` wire-format change (doctrine ladder —
  this is the first `docs/issue-<n>/decisions/` entry in this repo, per
  survey §7).

**Unit B — JS link rendering** (`src/rsb/web/dashboard.js`,
`src/rsb/web/dashboard.css`):
- New pure helpers `buildGithubUrl(ownerName, kind, number)` (returns
  `null` on falsy/non-string `ownerName`) and `externalLinkHtml(ownerName,
  kind, number, label)` (returns `""` when the URL is `null` — AC5, no
  broken link; otherwise an `escapeHtml()`-safe `<a class="external-link"
  target="_blank" rel="noopener noreferrer">` with an `aria-label` and a
  decorative `aria-hidden="true"` `↗` glyph, per scout-brief's must-be:
  separate sibling control, never overlaid/nested).
- `issueToggleCell(sourceTable, issue, repo, ownerName)` gained the 4th
  param; the link renders as a sibling immediately after the existing
  `row-toggle` `</button>`, so the disclosure button's click/keyboard
  semantics are untouched (constraint from the issue body itself and the
  proposal's Rationale).
- New `prCellHtml(ownerName, prNumbers)` (array-based; `"-"` on
  empty/falsy, else each number as `<span class="mono">` + link, joined
  `", "`) replaces the two plain-text PR cells: `decisionRows` (wraps its
  single `d.pr` as `[d.pr]`) and `flowRows` (`f.prs`, already an array).
- `decisionRows`/`flowRows`/`sessionRows`/`renderAccounting` each gained
  an `ownerNameByRepo` parameter and look up `ownerNameByRepo[record.repo]`
  per record (the board spans multiple repos, so this is a per-record
  lookup, not one value for the whole table). `renderData()` extracts
  `data.owner_name_by_repo || {}` once and passes it to all four.
  `filterByRepo()` needed no change — it already passes unlisted top-level
  keys through unchanged (survey §4).
- `module.exports` gained `buildGithubUrl`/`externalLinkHtml` (same
  `node -e`-coverage convention as `buildPlanSteps`/`filterByRepo`).
- `dashboard.css` gained `.external-link` (`margin-left: var(--space-1)`,
  `color: var(--color-text-secondary)`, hover/focus
  `var(--color-action-primary-background)`, `:focus-visible` outline
  matching `.row-toggle`'s) — only pre-existing tokens, no new ones
  (survey §5).

## Doc-placement ladder

- [x] `docs/issue-34/decisions/owner-name-wire-format.md` — new
  `board.json` top-level key, wire-format change (doctrine ladder: same
  turn as the code).
- [x] `docs/issue-34/reports/implementation.md` (this file) — completed.

## PR #35 feedback resolution

PR #35 carries one comment attached to the approval: when `owner_name`
is unavailable, `externalLinkHtml` returns `""` and the link is omitted
entirely (AC5-correct — no broken link), but some rows in the same table
then carry the ↗ affordance and others don't; the comment asked that
this be looked at during manual verification and the resulting judgment
recorded in one line.

Verified via a direct `node -e` call against the shipped
`externalLinkHtml` (see "Tests" below) that the with-owner case renders
`<a class="external-link">...↗...</a>` and the without-owner case
renders exactly `""`. Judgment: **leave it as `""`, no width-reserving
empty `<span>`.** `.external-link` renders inline inside the row's
existing Issue/PR `<td>`, not as its own column — HTML table columns
share one width across every row regardless of an individual cell's
content, so a missing ↗ in one row never shifts any other column's
boundary in any other row; the only effect is that one cell's own
trailing whitespace is a few pixels shorter, the same class of
variation this table already has elsewhere (e.g. `flowRows`'s `(raw)`
stage suffix, or the "0 steps" vs. multi-digit `done/total` plan badge)
with no precedent in this codebase for reserving space against it.

## Tests

`python3 -c "import sys; sys.path.insert(0, 'src'); import pytest; sys.exit(pytest.main(['test/', '-q']))"`
— **53 passed**, 0 failed, 0 skipped (33 pre-existing regression-free +
20 new: 4 in test_model.py, 1 in test_render.py, 1 in test_webserver.py,
plus the fixtures.py addition these draw on — the JS side has no pytest
file, only the `node -e` self-check below, per the proposal's own test
plan).

`node -e` self-check against the shipped, unmodified
`src/rsb/web/dashboard.js` (via its `module.exports`):
```
buildGithubUrl('a/b','issues',5)  -> "https://github.com/a/b/issues/5"
buildGithubUrl(null,'issues',5)   -> null
externalLinkHtml('a/b','issues',5,'Open issue 5 on GitHub')
  -> <a class="external-link" href="https://github.com/a/b/issues/5"
     target="_blank" rel="noopener noreferrer"
     aria-label="Open issue 5 on GitHub"><span aria-hidden="true">↗</span></a>
externalLinkHtml(null,'issues',5,'Open issue 5 on GitHub') -> ""
```
`node --check src/rsb/web/dashboard.js` — no syntax errors.

## What did not work

A live `rsb serve` smoke check (the style used in
`docs/issue-29/reports/implementation.md`'s "Manual smoke check") was
attempted to exercise `/api/board.json` end to end against a throwaway
two-file config + fake `flows --json` emitter outside the tracked tree.
Expected: write the two throwaway files under `$TMPDIR`, start the
server, `curl` it. Actual: this sandbox's write-approval layer blocked
every attempt to create files under `$TMPDIR` in this headless session
(no interactive approval available to grant it) — the same class of
sandbox-approval limitation `docs/issue-29/reports/implementation.md`'s
"Tests" section already documented for a different command shape. No
code was changed because of this; it only means the live-server path is
unverified beyond what's covered below.

## Open findings

The `/api/board.json` / `rsb --json` end-to-end path (server actually
serving the new `owner_name_by_repo` key over HTTP, and a real browser
rendering the ↗ links with correct keyboard tab order alongside
`row-toggle`) is verified at the unit level (pytest: `render_json_model`
output shape, `/api/board.json` spot-check via the test client) and at
the pure-function level (`node -e` on `externalLinkHtml`/`buildGithubUrl`
directly), but not via an actual running server or a real browser — this
headless sandbox has neither a working write path for a throwaway
`rsb serve` config (see "What did not work") nor a real browser (the
same limitation `docs/issue-29/reports/implementation.md` recorded).
Recommended resolution path: a follow-up manual check (start `rsb serve`
against a real configured board, open it in an actual browser) before or
shortly after this PR merges, confirming the four tables' issue links,
the two PR-cell links, and keyboard tab order between `row-toggle` and
`external-link` in practice — not expected to surface a code change,
since the diff mechanically matches the reviewed, frozen contract (see
"Self-check" below), but real-browser confirmation is the one gap this
session could not close.

## Self-check (no separate warrant-hunter agent available)

No standalone warrant-hunter agent/role is available in this
environment for this issue, mirroring
`docs/issue-29/reports/implementation.md`'s same note. In its place,
this section is a self-directed re-check of the integrated diff (both
units' output placed mechanically, then read against the frozen
contract) done by this same session.

closed_checks:
- python-contract-match: re-read the diff to `src/rsb/model.py` and
  `src/rsb/render.py` against the proposal's exact "Python (와이어 관통)"
  spec (key names, field name, population site) — matches verbatim.
- js-contract-match: re-read the diff to `src/rsb/web/dashboard.js`
  against this session's frozen worker contract (function names/
  signatures, per-record `ownerNameByRepo` lookup — not a single
  whole-table value, since a board spans multiple repos — the `[d.pr]`
  array-wrap for `decisionRows`' single-PR field vs. `f.prs`'s existing
  array in `flowRows`) — matches; the multi-repo per-record lookup in
  particular was checked line-by-line since it's the one place a
  single-repo assumption could have silently produced wrong links on a
  multi-repo board.
- row-toggle-not-overlapped: confirmed `issueToggleCell`'s returned
  string still emits the unmodified `<button class="row-toggle" ...>`
  first, with `externalLinkHtml(...)` appended only as trailing sibling
  markup after `</button>`, never wrapping or nesting it (the exact
  ambiguity issue #34's own body and the proposal's Rationale both flag).
- css-class-matches-js: grepped `dashboard.js` for the literal
  `class="external-link"` string it emits and confirmed
  `dashboard.css` declares a matching `.external-link` selector (plus
  `:hover`/`:focus`/`:focus-visible`), using only pre-existing `:root`
  tokens.
- full-test-suite: see "Tests" above — 53 passed, 0 failed, run against
  the fully integrated diff (both units together), not per-unit.
- pr-body-no-closing-keywords: confirmed no commit message or PR update
  in this session's work contains `Closes`/`Fixes`/`Resolves #34` in any
  form, including backtick-quoted (issue #23 T2 precedent, restated by
  this issue's own body).

This build's own commit lands immediately after this record is written
(single commit, this session); see this branch's `git log` for its sha
— not restated here to avoid the pre-commit-sha-unknowable problem
`docs/issue-29/reports/implementation.md` already documented for the
same class of self-check.
