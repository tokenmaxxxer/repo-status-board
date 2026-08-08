# test-authoring record — issue #44 phase 2

code_under_review: test/package.json, test/rsb_tests/test_dashboard_dom.py, docs/handbooks/rsb.md
loop_state: landed

## Why

Approved via issue #44 comment `APPROVE issue-44/test-authoring`
(jjongkwann, 2026-08-03, single-account mode — PR #45's author and the
approver are the same account). This executes
`docs/issue-44/proposals/test-authoring.md`'s "Adopted methodology" and
"Phase-2 test list" exactly as approved, resting on
`docs/issue-44/reports/test-authoring/survey.md` (found the require-time
`typeof window !== "undefined"` seam that lets `dashboard.js`'s
DOM-wiring code be driven without any `src/**` change) and
`scout-brief.md` (jsdom over browser automation for this wiring-level,
no-layout-needed scope).

Issue #44's own framing: three real wiring defects (repo-filter
`<select>` never populated, row-toggle relying on `<tr>` bubbling with
no `sourceTable`, mobile overflow) plus one independent Absent-coverage
verdict (`load()`'s fetch path) all shipped through the same gap — a
DOM stub (`test_model.py`'s `_run_dashboard_js`) that returns `null` for
every element and structurally cannot reach any DOM-wiring code.

## What was done

- **`test/package.json`** (new) — declares `jsdom` (`^30.0.1`) as the
  sole dependency. `npm install --prefix test` installs
  `test/node_modules/` (38 packages).
- **`test/rsb_tests/test_dashboard_dom.py`** (new) — 8 pytest test
  functions covering repo-filter population (3), row-toggle click wiring
  (4), and `load()`'s fetch path (1). Full architecture, fixture
  strategy, technique citation, and traceability below.
- **`docs/handbooks/rsb.md`** — "Tests" section now documents the
  `npm install --prefix test` one-time prerequisite (skip-gated, same
  convention as the pre-existing implicit `node` prerequisite) and
  points future verification/smoke-check sessions at extending this
  harness instead of writing a new one-off script (issue #44
  requirement 3).
- `test/rsb_tests/test_model.py`/`_run_dashboard_js` — **not touched**;
  kept as-is per the phase-1 proposal's decision (see "`_run_dashboard_js`
  disposition" below).

### Suite architecture

On the test pyramid, this new suite sits at the **integration level**:
it exercises `dashboard.js`'s DOM-wiring integration with a real
(simulated) DOM and event system — one level above the **unit**-level
pure-function tests `_run_dashboard_js` already covers (no DOM
involved), and well below **end-to-end**/browser-level tests, which
issue #44 explicitly puts out of scope (no layout/rendering, no visual
regression).

New file `test/rsb_tests/test_dashboard_dom.py`, sibling to
`test_model.py` — plain pytest functions, no test classes, same
xUnit-style shape as the rest of this repo's suite (no second
test-organization convention introduced).

Shared helper `_run_dom_js(script, fetch_body)`: builds a jsdom `JSDOM`
instance from a minimal HTML fixture matching `index.html`'s seven
element ids, installs it as `global.window`/`global.document`, installs
a `global.fetch` stub that records every call into `global.__fetchCalls`,
`require()`s `dashboard.js` fresh, waits one macrotask tick for the
auto-init `load()` call's promise chain to settle, then runs the
caller's assertion script and prints its result as JSON on stdout — same
subprocess+JSON-on-stdout contract `_run_dashboard_js` already uses,
with a real DOM underneath instead of the null stub.

One `node -e` subprocess per pytest test function (not one shared
long-lived process) — each test gets a fresh require cache and a fresh
DOM for free, so the `delete require.cache[...]` line in the helper is
defensive, not load-bearing. No teardown/reset code is needed since
nothing outlives the subprocess.

### Fixture strategy

**Fresh-fixture per test**: every test gets its own `node -e`
subprocess, its own `JSDOM` instance, and its own `require.cache`, so no
fixture state is ever shared or reused across test boundaries at the
process/DOM level — see "Slow Tests" below for the cost this trades
against.

- `_board_payload(**overrides)` — an Object Mother-style factory
  returning a minimal but complete `board.json`-shaped dict (matching
  `render.py`'s `render_json_model` output: `generated_at_by_repo`,
  `owner_name_by_repo`, `decisions`, `flows`, `sessions`, `ledger`,
  `unattributed`, `closure_sweep`, `unapproved_open_prs`, `errors`), with
  per-call overrides. Keeps each test's actual concern (e.g.
  `decisions=[...]`) visible at the call site instead of hidden in an
  external fixture file — avoids Meszaros's Mystery Guest smell.
- `_fetch_ok(payload)` — one-line helper turning a payload dict into the
  fetch stub's JS return statement.
- `DASHBOARD_HTML` — a Minimal Fixture: only the seven ids
  `dashboard.js`'s module-scope consts actually read via
  `getElementById`, not a full copy of `index.html`. Keeps the fixture's
  intent legible and decouples the test from unrelated markup changes.
- `_ROWS_PAYLOAD` — one module-level **shared-fixture** Python dict
  (same issue+repo number, 7/"repo-a", present in both `decisions` and
  `flows`, to exercise the `sourceTable` cross-table isolation
  directly), reused by the four row-toggle tests as a read-only literal.
  Meszaros flags Shared Fixture as a smell when a mutation in one test
  can leak into another; that risk doesn't apply here because each test
  still runs in its own fresh subprocess/DOM per the fresh-fixture
  strategy above — nothing mutates the shared Python dict, and no
  DOM/JS state persists across tests regardless.

### Test-design technique

- **Equivalence Partitioning (EP)**: repo-filter suite
  (`test_repo_filter_options_empty_when_no_repos`,
  `test_repo_filter_options_populated_for_single_repo`,
  `test_repo_filter_options_populated_for_multiple_repos_including_errored`)
  partitions on repo count — zero repos, one repo, multiple repos
  (including one that only appears via `errors`, exercising
  `repoList`'s succeeded-union-errored logic). Row-toggle suite
  (`test_row_toggle_click_opens_detail_and_flips_aria_expanded` vs.
  `test_row_toggle_click_on_non_button_cell_does_not_open_detail`)
  partitions on click target (the `.row-toggle` button vs. a non-button
  cell); `test_row_toggle_click_only_affects_its_own_table` partitions
  on table identity (`decisions` vs. `flows` for the same issue+repo).
- **Boundary Value Analysis (BVA)**:
  `test_row_toggle_reactivating_open_button_closes_it` — re-activating
  an already-open toggle button, the boundary between the "opening" and
  "closing" transitions of the same control.
- Regression adequacy for the specific claim issue #44 makes ("would
  this test have failed under the actual shipped defect") was verified
  directly against this repo's own git history rather than merely
  asserted: each defect's pre-fix `dashboard.js` revision was extracted
  via `git show <fix-commit>^:src/rsb/web/dashboard.js` into a scratch
  path (not committed) and run through the corresponding new test with
  `DASHBOARD_JS` monkeypatched to point at it. See Verification below
  for the specific commits and results. This check is scoped to exactly
  the three named historical defects plus the one named Absent-coverage
  gap — it says nothing about suite coverage beyond those four items.

### Traceability

- `test_repo_filter_options_empty_when_no_repos`,
  `test_repo_filter_options_populated_for_single_repo`,
  `test_repo_filter_options_populated_for_multiple_repos_including_errored`
  → issue #44 defect #1 / issue #29 (`repoList`/`filterByRepo`
  implemented and tested but never called from `dashboard.js`, so the
  deployed `<select>` never got any options).
- `test_row_toggle_click_opens_detail_and_flips_aria_expanded`,
  `test_row_toggle_click_on_non_button_cell_does_not_open_detail`,
  `test_row_toggle_click_only_affects_its_own_table`,
  `test_row_toggle_reactivating_open_button_closes_it` → issue #44
  defect #2 / issue #29 (row-toggle relied on `<tr>` bubbling;
  `selectedIssue` had no `sourceTable`, so `aria-expanded` was
  permanently `false` and any row click — not just the button — opened
  the detail panel).
- `test_load_fetches_relative_board_json_path` → issue #44's
  Absent-coverage gap / issue #27 conformance-review (`load()`'s
  `fetch("api/board.json")` path had no test calling `load()` under any
  path).

### Smell list (Meszaros, *xUnit Test Patterns*) checked against this suite

- **Fragile Test / Interacting Tests** — avoided: one subprocess per
  test, no shared mutable state crosses a test boundary.
- **Slow Tests** — present but accepted: jsdom startup + `node` process
  spawn costs roughly 0.5s/test observed (8 tests, ~5s total against 63
  total suite tests in ~7s). This is the explicit trade the phase-1
  proposal already made (jsdom over browser automation, in-process DOM
  over layout-capable rendering) and is not revisited here.
- **Obscure Test** — mitigated via EP/BVA framing in each suite's
  header comment and self-descriptive test names stating the exact
  behavior under test.
- **Mystery Guest** — avoided; see Fixture strategy above.
- **Test Code Duplication** — the per-test JS click/query snippets are
  short (2-6 lines) and each encodes a genuinely distinct assertion
  path; a further helper-extraction layer was judged to cost more in
  indirection than it saves in line count at today's 8-test scale.
- **Conditional Test Logic** — none inside any test function; the only
  branching is the two `pytest.skip()` environment gates inside the
  shared helper (missing `node`, missing `jsdom`), mirroring
  `_run_dashboard_js`'s existing convention.

### Runtime dependency

`jsdom` (npm, `^30.0.1`; installed `30.0.1`), declared in
`test/package.json`, installed to `test/node_modules/` (38 packages).
This is the first JS runtime dependency this repo has ever had —
confined to `test/**`, dev/test-only, never reaches `src/**` or the
deployed static bundle. Selection rationale (jsdom vs. Playwright/
Selenium-class browser automation) is recorded in the phase-1 proposal
(`docs/issue-44/proposals/test-authoring.md`, "Rationale") and not
re-litigated here.

### `_run_dashboard_js` disposition

Kept as-is (`test_model.py`, 9 existing pure-function tests), per the
phase-1 proposal's decision — none of those tests read the DOM-element
consts, so routing them through jsdom would add setup cost for zero
coverage benefit. The new DOM suite is fully additive in a new file;
zero regression risk to the existing 9 tests.

## Verification

- `python -m pytest test/` (run via `PYTHONPATH=src` in this sandbox,
  since the package isn't `pip install -e .`'d into this container's
  Python — an environment-setup detail of this sandbox, not a suite
  defect): **66 collected, 64 passed, 2 failed, 0 skipped** (`node`
  v26.7.0 present, `test/node_modules/jsdom` installed). 57 pre-existing +
  9 new. Restates the section below against the merged artifact, per
  `docs/issue-44/reports/conformance-review.md` Finding 2 (R12a/R12c):
  this record's original "63 passed, 0 failed … 55 pre-existing + 8 new"
  described the branch base (`b621082`), not what shipped, since the
  branch never rebased onto or re-ran against the `f353910` tip it merged
  on top of. Independently re-measured here rather than copied forward
  from that review — its own cited "65 collected / 63 passed / 57
  pre-existing" is itself one commit further stale: `21c2359` (issue-56)
  landed on a branch that review's measurement predates and added a
  ninth `test_dashboard_dom.py` test. The 2 failures,
  `test_row_toggle_click_opens_detail_and_flips_aria_expanded` and
  `test_row_toggle_reactivating_open_button_closes_it`, are the
  pre-existing unguarded `window.matchMedia` call `f353910` introduced —
  attribution already settled in
  `docs/issue-36/reports/conformance-review.md` Appendix A4 and put
  outside this issue's judgment by issue #44's own `## Acceptance` note,
  not a defect in this suite's own 9 tests.
- Each of the 5 defect/gap-tracing tests re-run individually against its
  pre-fix `dashboard.js` revision, extracted via `git show` (scratch
  files, deleted after use, never committed):
  - repo-filter population tests vs. `c94e12d^` (pre issue-29
    fast-follow #33) — failed as expected.
  - row-toggle open/aria-expanded, empty-cell, and cross-table-isolation
    tests vs. `b621082^` (pre issue-36 #37 row-toggle relocation) —
    all three failed as expected.
  - `load()` relative-fetch-path test vs. `3ebecae^` (pre issue-27 #28
    relative-path fix, when the fetch call used `/api/board.json`) —
    failed as expected.
  - The BVA close-toggle test was not separately re-verified against a
    pre-fix revision — it depends on the open-toggle behavior already
    shown broken above, so it adds boundary coverage on top of an
    already-demonstrated regression rather than tracing to an
    independent historical defect.

## Acceptance criteria crosswalk (issue #44)

- [x] DOM 이벤트를 디스패치해 상태를 검증하는 테스트가 존재한다 —
      `.click()` dispatch against real jsdom elements, `aria-expanded`/
      `innerHTML` assertions.
- [x] 배경의 결함 3건 + Absent 1건에 각각 대응하는 테스트가 있고, 해당
      결함 상태에서 실제로 실패함이 확인된다 — repo-filter, row-toggle,
      fetch-path Absent gap: covered and verified failing pre-fix (see
      Verification). Mobile-overflow: intentionally not covered — see
      Open findings below; this is the approved phase-1 scope, not an
      oversight.
- [x] 기존 pytest 스위트가 계속 통과한다 — 57/57 pre-existing tests pass
      (66 collected overall: 64 passed, 2 failed; both failures are
      inside this suite's own new `test_dashboard_dom.py`, not the
      pre-existing suite — see Verification).
- [x] 실행 방법이 문서에 기록된다 — `docs/handbooks/rsb.md` "Tests"
      section, updated this phase.
- [x] 새 런타임 의존성이 생긴다면 그 선택 근거가 record 에 남는다 — see
      Runtime dependency above; full rationale in the phase-1 proposal.
- [x] PR 본문에 closing 키워드 금지 — observed in this PR's body.

## Open findings

- **`.gitignore` hand-off, unresolved.** Repo-root `.gitignore` needs a
  `node_modules/` entry — `test/node_modules/` is currently untracked
  and unignored. This sits outside this role's `test/**` write scope
  (per the role-handoff contract's boundary case), so it is not made
  this phase; this session's commit stages only files under
  `test/**`/`docs/**`, so `test/node_modules/` is not accidentally
  committed even without the ignore entry. Whichever role/session next
  touches repo-root config should add it.
- **Mobile-overflow (issue #38 P1-1) is not covered, by design, not
  oversight.** jsdom implements no layout engine, so computed widths
  are not meaningful in it. Issue #44's own minimum-coverage bullet
  list (requirement 2) already excludes this case — it names only the
  filter/toggle/fetch-path items — and its "범위 밖" section explicitly
  excludes visual/screenshot regression testing, which measuring
  rendered overflow at a viewport width would be. This reconciliation
  was flagged in the phase-1 proposal ("Note on the mobile-overflow
  defect") and approved as part of that proposal.
- **Two of this suite's own tests are red on `main`**
  (`test_row_toggle_click_opens_detail_and_flips_aria_expanded`,
  `test_row_toggle_reactivating_open_button_closes_it`), both the
  pre-existing unguarded `window.matchMedia` call `f353910` introduced —
  attribution already settled in
  `docs/issue-36/reports/conformance-review.md` Appendix A4, outside this
  issue's judgment per issue #44's `## Acceptance` note. First reported
  against this bullet by `docs/issue-44/reports/conformance-review.md`
  Finding 2 (R12c): the original "No other findings: 63/63 … pass" text
  here reported this open item as closed.
- Otherwise no other findings: all 5 defect/gap-tracing tests
  independently confirmed to fail against their real pre-fix code (see
  Verification), and the remaining 7 of this suite's 9 tests pass.
