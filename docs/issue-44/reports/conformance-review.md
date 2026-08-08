# Conformance-review record (issue #44)

loop_state: reported

code_under_review: `b2f6b637c372ceec3ba4654b363f0af1ddc0d800` (PR #45,
merged 2026-08-03T12:31:44Z) — `test/rsb_tests/test_dashboard_dom.py`,
`test/package.json`, `test/package-lock.json`, `docs/handbooks/rsb.md`
§Tests, `docs/issue-44/reports/test-authoring.md`,
`docs/issue-44/proposals/test-authoring.md`.
`git diff --stat b2f6b63..HEAD -- src/ test/` is empty, so every runtime
measurement below is equally a measurement of the merged artifact.

spec_under_review: issue #44 body — 요구사항 1–4, 범위 밖, 수용 기준 AC1–AC6,
and the issue's `## Acceptance` check list.

## What was done

Scored PR #45 against the requirement list in this role's approved
phase-1 proposal (`docs/issue-44/proposals/conformance-review.md`,
R1a–R12c). Verdicts were derived from direct inspection of the shipped
files, from fresh runs in this session, and from a replay of the harness
against three real pre-fix `dashboard.js` revisions extracted with
`git show` into scratch paths (deleted, never committed). The
test-authoring role's proposal and record were read as claims to
re-derive, never as evidence — every "failed as expected" assertion in
`docs/issue-44/reports/test-authoring.md:199-221` was independently
reproduced here rather than accepted.

**Requirement-count correction.** The approved proposal's summary line
(`docs/issue-44/proposals/conformance-review.md:56`) states "12 groups,
31 sub-requirements"; the list it actually itemizes totals **32**
(R1: 5, R2: 3, R3: 3, R4: 2, R5: 1, R6: 3, R7: 3, R8: 3, R9: 2, R10: 3,
R11: 1, R12: 3). All 32 itemized sub-requirements are scored below. No
requirement was dropped or added — the "31" is an arithmetic undercount
in that document's own summary, noted here rather than carried forward.

**Excluded from judgment by the spec itself.** Issue #44's `## Acceptance`
note records that `main`'s two `test_dashboard_dom.py` failures are the
pre-existing unguarded `window.matchMedia` defect introduced by
`f353910`, with attribution already settled in
`docs/issue-36/reports/conformance-review.md` (Appendix A4), and states
they are "이 이슈의 판정 대상 아님". This record therefore cites that
attribution and does not re-derive it: no verdict below scores the
`src/**` defect. What *is* scored is the effect that defect's presence
has on claims the artifact itself makes (R12a, R12c).

## Upstream basis

Rests on `docs/issue-44/proposals/conformance-review.md` (this role's
approved phase-1 requirement list) plus
`docs/issue-44/reports/conformance-review/survey.md` and
`.../scout-brief.md`. Phase 2 opened on issue #44 comment
`APPROVE issue-44/conformance-review` (jjongkwann, 2026-08-04T10:01:58Z),
whose entire body is that exact string; the account is listed in
`docs/specs/approvers.md`. Single-account mode — PR #53's author and the
approver are the same account — so the issue-comment path of contract v3
§19 applies. The two other approval comments on issue #44
(`APPROVE issue-44/test-authoring`, `APPROVE issue-44/execution-observation`)
are other roles' gates and were not read as this role's approval.

## Reviewer-environment note

The sandbox this review ran in refuses an inline `VAR=value cmd` shell
prefix, so `PYTHONPATH=src python -m pytest …` could not be issued
literally. Every suite run below used the equivalent
`python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
sys.exit(pytest.main([...]))"`, which produces the same module
resolution. The interpreter is Python 3.11.8 / pytest 8.4.1, `node`
v26.7.0, `test/node_modules/jsdom` 30.0.1. This substitution is
disclosed because it is a deviation from the command the artifact
documents, and R7c scores the documented command separately and on its
own terms.

## Verdicts

Verdict enum: **Present / Surface / Absent / Incorrect / Unverifiable**.

| Requirement | spec_ref | Verdict | Evidence | Rationale |
| --- | --- | --- | --- | --- |
| R1a: the shipped `dashboard.js` is loaded against a real DOM, not a stub | 요구사항 1; AC1 | Present | `test/rsb_tests/test_dashboard_dom.py:33` resolves `parents[2]/"src"/"rsb"/"web"/"dashboard.js"` — the shipped path, interpolated at `:88` and `require()`d at `:79`; `:67,70-72` build a real `JSDOM` and install it as `global.window`/`global.document` | The module under test is the deployed file itself, and the DOM under it is jsdom, not `test_model.py:170`'s `{ getElementById: () => null }` stub — no copy, no re-implementation |
| R1b: tests dispatch real events rather than calling handlers directly | 요구사항 1; AC1 | Present | `.click()` on jsdom elements at `test_dashboard_dom.py:182`, `:201`, `:217`, `:235-236` | `HTMLElement.click()` dispatches a real bubbling click through jsdom's event system; no test reaches into `dashboard.js` to invoke a handler by name — and it cannot, since the wiring functions are unexported (`src/rsb/web/dashboard.js:681`) |
| R1c: assertions are on resulting DOM state, not a helper's return value | 요구사항 1; AC1 | Present | `test_dashboard_dom.py:131` (`select.options` values), `:186-187` (`aria-expanded`, `#detail-panel-slot` `innerHTML`), `:221-222`, `:238-239` | Seven of eight tests read state back off the DOM after the event. The eighth (`:256`) reads `global.__fetchCalls`, a stub-recorded side effect — the only observable for a fetch-path requirement, and the correct surface for it rather than a substitute for DOM state |
| R1d: harness choice and entry point decided in the proposal, and the landed code matches | 요구사항 1 ("수단… 진입점은 제안서에서 결정") | Present | Decision: `docs/issue-44/proposals/test-authoring.md:60-63` (jsdom, per-test Node subprocesses) and `:123-127` ("Entry point stays `python -m pytest test/`"). Match: `test/package.json` has no `scripts` key; no `conftest.py` exists anywhere in the repo; `git show --stat b2f6b63` adds no runner and no CI entry | The issue required the decision be made in the proposal; it was, and the tree carries no second runner that would contradict it |
| R1e: the harness runs — at least one DOM test executes and passes, not skips | AC1; `## Acceptance` check 1 | Present | `pytest test/rsb_tests/test_dashboard_dom.py -v -rs` → `collected 8 items`, `6 passed`, `2 failed`, **0 skipped**, no skip-reason section printed | Both `pytest.skip()` gates (`test_dashboard_dom.py:62-65`) were passed, so all 8 tests are executed, not collected-then-skipped. The two failures are the excluded `matchMedia` defect (see header), not a harness that fails to run |
| R2a: a test exists for repo-filter `<select>` population | 요구사항 2 bullet 1; AC2 | Present | `test_dashboard_dom.py:128`, `:137`, `:146` | Three tests partitioned on repo count (zero / one / multiple-including-errored) |
| R2b: it asserts the options are populated with repo values, not merely that the element exists | 요구사항 2 bullet 1; AC2 | Present | `test_dashboard_dom.py:143` (`== ["", "repo-a"]`), `:155` (`== ["", "repo-a", "repo-b"]`) | Exact-list equality on option `value`s, including a repo reachable only through `errors` — an existence check could not distinguish the shipped defect from the fix |
| R2c: it fails against the pre-fix `dashboard.js` (`c94e12d^`) | AC2 ("해당 결함 상태에서 실제로 실패함이 확인된다") | Present | `c94e12d^` = `3ebecaebcc3be9aa6a42c6622254e422b0069ecd`. Harness re-pointed at that file in a scratch copy (only `DASHBOARD_JS`/`TEST_DIR` changed): `test_..._single_repo` → `AssertionError: assert [''] == ['', 'repo-a']`; `test_..._multiple_repos_including_errored` → `assert [''] == ['', 'repo-a', 'repo-b']`; `2 failed, 1 passed` | Both populated-repo tests reproduce the shipped defect. Qualification, recorded rather than smoothed over: the zero-repo test (`:128`) **passes** pre-fix, since an empty option list is indistinguishable either way — a valid EP partition that contributes no regression detection, so the record's blanket "repo-filter population tests … failed as expected" (`reports/test-authoring.md:209-210`) overstates by one test |
| R3a: clicking `.row-toggle` flips `aria-expanded` to `true` | 요구사항 2 bullet 2; AC2 | Present | `test_dashboard_dom.py:177-194`; assertions `:192-193` (`before == "false"`, `afterExpanded == "true"`) both hold on the merged tree — the test's failure is at `:194` (`detailHasContent`) | The `aria-expanded` half of the bullet is asserted and currently true. The adjacent `:194` assertion is red for the excluded `matchMedia` reason, which does not touch the attribute flip this sub-requirement covers |
| R3b: clicking an empty/plain cell does not open the detail | 요구사항 2 bullet 2 (negative half); AC2 | Present | `test_dashboard_dom.py:197-211`; clicks `main table tbody tr td` at `:200-201`, asserts `expanded == "false"` and `detailHasContent is False`; **PASSED** on the merged tree | The negative case is present, executed, and green |
| R3c: R3a and R3b both fail against the pre-fix revision (`b621082^`) | AC2 | Present | `b621082^` = `5d05b5f5227c0b8073bed3d16455664bcafd0a5a`. Replay: `test_row_toggle_click_opens_detail_and_flips_aria_expanded` → `assert 'false' == 'true'`; `test_row_toggle_click_on_non_button_cell_does_not_open_detail` → `assert True is False`; `test_row_toggle_reactivating_open_button_closes_it` → `assert True is False`; `3 failed` | Both required tests reproduce the pre-fix defect. Additionally the BVA re-click test (`:231`) — which `reports/test-authoring.md:217-221` states was *not* separately pre-fix-verified — was verified here and does fail pre-fix, so it too is regression-adequate; the record's caveat was conservative, not wrong |
| R4a: a test asserts the fetched URL is exactly `api/board.json` | 요구사항 2 bullet 3; AC2 | Present | `test_dashboard_dom.py:254-259`, `assert result["fetchCalls"] == ["api/board.json"]` | Exact-list equality on the recorded fetch argument closes the issue #27 **Absent** verdict's stated gap — a change to an absolute path now fails a test |
| R4b: it fails against the pre-fix revision (`3ebecae^`) | AC2 | Present | `3ebecae^` = `b6302925088820d3cff97e402c67249fbfe926ca`. Replay: `AssertionError: assert ['/api/board.json'] == ['api/board.json']`; `1 failed` | The pre-fix tree fetched the absolute path and the test catches exactly that. Revision bookkeeping: `c94e12d^` and `3ebecae` are the **same** commit, so R2c's tree (`3ebecae`) and R4b's tree (`b630292`) are one commit apart and distinct — the proposal's note at `:103-104` is correct and is discharged here by full SHA |
| R5a: whether a test corresponds to the mobile-overflow defect, and if not, whether the omission is within spec | AC2 ("결함 3건 + Absent 1건에 **각각**") vs 요구사항 2 (three bullets) vs 범위 밖 (visual regression excluded) | Absent | No width, viewport, `getBoundingClientRect`, `scrollWidth`, or screenshot assertion exists anywhere in `test_dashboard_dom.py:1-260`; `git show --stat b2f6b63` adds no other test file. The omission is declared at `reports/test-authoring.md:251-259` | Scored against the spec as written, not against the builder's intent. AC2's checkbox counts four items and only three are covered, so the fourth is **Absent**. The three spec passages are in genuine tension — 요구사항 2's 최소 커버리지 list enumerates exactly three bullets and omits mobile overflow, and 범위 밖 excludes the visual-regression technique any overflow measurement would need — so this is an unresolved contradiction in the spec, not a silent gap in the artifact. It is addressed to the issue author for reconciliation, not to test-authoring as a defect (see Open findings) |
| R6a: a full `python -m pytest test/` run passes with the new module present | AC3 ("기존 pytest 스위트가 계속 통과한다") | Present | Full run: `collected 65 items`, `2 failed, 63 passed in 6.07s`, exit 1. The 57 pre-existing tests (`test_cli` 8, `test_config` 6, `test_fetch` 10, `test_model` 24, `test_render` 5, `test_webserver` 4) are **all** `PASSED`; both failures are inside the new `test_dashboard_dom.py` | AC3's subject is the pre-existing suite, and no pre-existing test regressed. The non-zero exit is real and is recorded here rather than rounded off: it comes from the two new tests hitting the excluded `matchMedia` defect. Scoring that as a failure of AC3 would charge this artifact for an `src/**` defect issue #44 explicitly removes from judgment; the record-accuracy consequence is scored separately at R12a/R12c |
| R6b: the pass is not a disguised skip | AC3; scout-brief "executed ≠ collected" must-be | Present | The `-rs` run reports **0 skipped** and prints no skip-reason section; 65 collected = 63 passed + 2 failed | Every collected test produced an executed outcome, including all 8 DOM tests. The `node`/`jsdom` skip gates at `test_dashboard_dom.py:62-65` did not fire |
| R6c: no pre-existing test was modified or removed | AC3 | Present | `git show --stat b2f6b63 -- test/` lists exactly three files, all additions: `package-lock.json` (+514), `package.json` (+8), `rsb_tests/test_dashboard_dom.py` (+259); the whole commit is `8 files changed, 1591 insertions(+)` with zero deletions | The new coverage is purely additive; `test_model.py` and every other pre-existing module are byte-unchanged |
| R7a: how to run the harness, including the one-time prerequisite, is recorded | 요구사항 3; AC4 | Present | `docs/handbooks/rsb.md:37-41` (`python -m pytest test/`) and `:54-58` (`npm install --prefix test`, labelled "One-time prerequisite"), plus `:60-61` documenting the skip-instead-of-fail behavior | Both commands and the prerequisite's one-time nature are written down in the handbook |
| R7b: the documentation instructs future sessions to extend this harness instead of writing throwaway scripts | 요구사항 3 ("임시 스크립트 대체") | Present | `docs/handbooks/rsb.md:61-63`: "Future verification/smoke-check sessions should extend this harness (add a test function, reusing `_run_dom_js`) instead of writing a new one-off script — this is what it exists to replace." | 요구사항 3's stated purpose is written as an instruction, names the reuse seam (`_run_dom_js`), and names the behavior it replaces |
| R7c: the documented commands work as written | AC4 | Surface | Following `## Tests` alone, from a shell with no `PYTHONPATH` and the package not installed: `python3 -m pytest test/ --collect-only -q` → `8 tests collected, 6 errors`, `ERROR test/rsb_tests/{test_cli,test_config,test_fetch,test_model,test_render,test_webserver}.py`, each `ModuleNotFoundError: No module named 'rsb'`, `Interrupted: 6 errors during collection`. The missing step, `pip install -e .`, is at `docs/handbooks/rsb.md:10`, under the separate `## Install / run` heading, and `## Tests` (`:37-63`) never references it | The section exists and its second command (`npm install --prefix test`, exit 0) works, but the first does not run from a clean environment for a reader who follows `## Tests` alone — 57 of 65 tests never reach execution. Documentation shaped like a runnable procedure that is not one: Surface, not Present. Noted for fairness: this handbook layout pre-dates PR #45, which extended the section rather than introducing the gap |
| R8a: the record states that a new runtime dependency was introduced | AC5 | Present | `docs/issue-44/reports/test-authoring.md:180-189` — names `jsdom` `^30.0.1` (installed `30.0.1`), `test/package.json`, `test/node_modules/`, and "the first JS runtime dependency this repo has ever had" | The introduction itself is recorded explicitly, with version and install location |
| R8b: the 선택 근거 is in the record | AC5 ("그 선택 근거가 record 에 남는다") | Surface | `reports/test-authoring.md:186-189`: "Selection rationale (jsdom vs. Playwright/Selenium-class browser automation) is recorded in the phase-1 proposal … and not re-litigated here." The reasoning itself lives at `docs/issue-44/proposals/test-authoring.md:129+` ("Alternatives considered and rejected") | The record carries a pointer where AC5 asks for the 근거. The pointer resolves and its target is durable and in-repo, so nothing is lost — but the record read on its own states *that* a choice was justified, not *why*. A field in the required shape that does not carry the required content is Surface. Low materiality; recorded for fidelity, not as a blocker |
| R8c: the declared dependency scope matches the documented scope | AC5; npm packaging convention | Incorrect | `test/package.json:5-7` puts `jsdom` under `"dependencies"`; the file has no `"devDependencies"` key. `reports/test-authoring.md:184-186` and PR #45's body both describe it as "dev/test-only" | The manifest declares a production runtime dependency while every prose description declares a test-only one. `"private": true` (`test/package.json:3`) means nothing is published, so blast radius is small, but `npm install --omit=dev` in `test/` would still install jsdom, and a future reader takes the manifest as the source of truth. See spec_vs_built below |
| R9a: a keep-vs-absorb decision on `_run_dashboard_js` is made and recorded | 요구사항 4 | Present | Decision: `docs/issue-44/proposals/test-authoring.md:84-90` ("kept as-is, not migrated"). Recorded: `reports/test-authoring.md:191-197` (`### _run_dashboard_js disposition`) with the reason — those tests never read DOM-element consts | 요구사항 4 asks only that the relationship be settled and written down; both the decision and its reason exist in both phase documents |
| R9b: the landed code matches that decision | 요구사항 4 | Present | `test/rsb_tests/test_model.py:170` (`_run_dashboard_js`) and its call sites at `:186,204,223,261,289,317,331,342,353,360` are untouched — `git show --stat b2f6b63 -- test/` lists no change to `test_model.py` | Kept means kept: the helper and every test using it are unmodified, matching the recorded decision exactly |
| R10a: no visual/screenshot-regression test was added | 범위 밖 bullet 1 | Present | Full read of `test_dashboard_dom.py:1-260`: no screenshot, pixel, viewport, `scrollWidth`, `offsetWidth`, or `getBoundingClientRect` reference; assertions are attribute-, option-value-, `innerHTML`-emptiness-, and fetch-argument-based | Nothing in the artifact crosses into pixel comparison |
| R10b: no CI test gate was added | 범위 밖 bullet 2 | Present | `git show --stat b2f6b63` touches 8 files, none under `.github/` | The commit adds no workflow and modifies none |
| R10c: no `src/**` change; any needed production change is recorded as a hand-off | 범위 밖 bullet 3 | Present | `git show --stat b2f6b63` touches only `docs/**` and `test/**`; zero `src/` paths. Hand-off recorded at `reports/test-authoring.md:243-250`, and it is genuinely still open — `.gitignore` (5 lines: `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, `*.egg-info/`) has no `node_modules/` entry, and `git status --short` still shows `?? test/node_modules/` | The harness was built entirely on the pre-existing `typeof window !== "undefined"` seam, so no production change was needed; the one repo-root change that *was* needed was flagged out rather than made, exactly as 범위 밖 requires |
| R11a: PR #45's body contains no closing keyword, including inside backticks | AC6; issue #23 T2 | Present | `gh pr view 45 --json body` matched case-insensitively for `clos(e\|es\|ed)\|fix(e[sd])?\|resolv(e\|es\|ed)`: the only hits are substrings inside `--prefix` (`npm install --prefix test`) and `pre-fix` ("fail against its real pre-fix `dashboard.js` revision"). The issue is referenced as "issue #44 (test-authoring role)" and "issue #44's" — never preceded by a keyword | GitHub's auto-close parser requires `<keyword> #<number>`; no hit is adjacent to an issue reference, and no standalone keyword form appears at all |
| R12a: the record's AC crosswalk claims match the artifact | AC5 (makes the record load-bearing) | Incorrect | `reports/test-authoring.md:234` claims "기존 pytest 스위트가 계속 통과한다 — 63/63 passed" and `:204-205` claims "**63 passed**, 0 failed, 0 skipped … 55 pre-existing + 8 new". Measured on the merged artifact: **65 collected, 63 passed, 2 failed** — 57 pre-existing, not 55, and the run exits 1. Cause is structural: PR #45 branched from `b621082` (`dashboard.js` 595 lines, no `matchMedia`) and merged after `f353910` landed, without a rebase or a re-run — `git show b2f6b63:src/rsb/web/dashboard.js` already carries `window.matchMedia(WIDE_LAYOUT_QUERY)` at `:520` | The crosswalk's numbers were true on the branch base and untrue of the merged result the moment it landed. The underlying `src/**` defect is attributed elsewhere and not scored here; what is scored is that the record's own verification claim does not describe the artifact it ships with. See spec_vs_built below |
| R12b: citations the record and the test module make about the code resolve | AC5 | Incorrect | Three stale citations, all measured against `b2f6b63:src/rsb/web/dashboard.js` (682 lines): (1) the auto-init seam is cited as `dashboard.js:584-591` at `test_dashboard_dom.py:9-10` and `proposals/test-authoring.md:42-43`; it is at `src/rsb/web/dashboard.js:671-679`. (2) `test_dashboard_dom.py:4-5` and `proposals/test-authoring.md:39` say the export guard exports "exactly 8" pure helpers; `src/rsb/web/dashboard.js:681` lists **10** (`detailRowHtml`, `collapsibleDetailHtml` added by `f353910`), of which `test_model.py` actually exercises **6** (`buildPlanSteps`, `selectSummary`, `filterByRepo`, `numberLinkHtml`, `detailRowHtml`, `collapsibleDetailHtml`). (3) `reports/test-authoring.md:193` says `_run_dashboard_js` covers "8 existing pure-function tests"; there are **9** `test_dashboard_js_*` functions in `test_model.py`. All three were correct against the branch base `b621082` (595 lines, seam at `:584`, 8 exports) | Same merge-time drift as R12a, not fabrication: every citation resolved when written and none resolves now. They are load-bearing — a future session following `dashboard.js:584-591` lands in the middle of `load()`'s error handling. See spec_vs_built below. Adjacent, outside R12b's scope but due the same correction pass: `docs/handbooks/rsb.md:48-49` tells readers the whole `module.exports` list has `node -e` coverage, when 4 of the 10 exports (`ageBucket`, `ageBucketStatus`, `isPageEmpty`, `buildGithubUrl`) are not directly exercised by `test_model.py` |
| R12c: items the record leaves open are actually open, and nothing closed is reported as open | AC5 | Incorrect | Two of three Open-findings bullets check out: the `.gitignore` hand-off (`reports/test-authoring.md:243-250`) is genuinely open (see R10c), and the mobile-overflow omission (`:251-259`) is genuinely uncovered (see R5a). The third (`:260-262`) asserts "**No other findings**: 63/63 suite tests pass, and all 5 defect/gap-tracing tests independently confirmed to fail against their real pre-fix code" — but 2 of the 8 tests this PR shipped are red on the artifact as merged | An open item is reported as closed. The second clause of that bullet is independently confirmed correct by this review (R2c/R3c/R4b all reproduce, and the BVA test does too); the first clause is not. See spec_vs_built below |

**Tally:** Present 25 · Surface 2 · Absent 1 · Incorrect 4 · Unverifiable 0
(32 of 32 scored; nothing was left unchecked).

## spec_vs_built (required for `Incorrect` verdicts)

**R8c.** Spec required: a dependency introduced for `test/**` only, which
both AC5's record entry and PR #45's body describe as "dev/test-only",
and which npm expresses as `devDependencies`. Built:
`test/package.json:5-7` declares `jsdom` under `"dependencies"`, with no
`"devDependencies"` key present at all.

**R12a.** Spec required (AC3 + AC5): a record whose stated verification
result describes the artifact being delivered. Built: a record stating
"63 passed, 0 failed, 0 skipped … 55 pre-existing + 8 new" for a merged
artifact that yields 65 collected / 63 passed / 2 failed / 57
pre-existing, because the branch was never rebased onto or re-run
against the `f353910` tip it merged on top of.

**R12b.** Spec required (AC5): citations in the load-bearing record and
in the shipped test module that resolve against the shipped code. Built:
`dashboard.js:584-591` for a seam now at `:671-679`; "exactly 8" exports
for a guard now listing 10; "8 existing pure-function tests" for 9.

**R12c.** Spec required (AC5): an Open-findings section where open items
are listed as open. Built: a "No other findings … 63/63 suite tests pass"
bullet, while two of the eight tests the PR shipped fail on the merged
artifact.

## Open findings

Findings are recorded and addressed; this role does not fix them and has
made no change to `src/**`, `test/**`, `.gitignore`, or any other role's
record.

1. **`jsdom` is declared as a production dependency (R8c).**
   *addressed_to: test-authoring.* Move `jsdom` from `"dependencies"` to
   `"devDependencies"` in `test/package.json`, or amend the record and
   PR description to stop calling it dev-only. Either resolves the
   contradiction; the manifest change is the smaller one.

2. **The record's verification numbers describe the branch base, not the
   merged artifact (R12a, R12c).** *addressed_to: test-authoring.*
   `docs/issue-44/reports/test-authoring.md:199-205, 234, 260-262` should
   be restated against `b2f6b63` — 65 collected, 63 passed, 2 failed, 57
   pre-existing — and the "No other findings" bullet reopened to name the
   two red tests and point at the already-settled `f353910` attribution.
   The correction is to the record, not to the tests: nothing here asks
   for a test change.

3. **Three code citations went stale on merge (R12b).**
   *addressed_to: test-authoring.* `test_dashboard_dom.py:9-10`,
   `docs/issue-44/proposals/test-authoring.md:39,42-43`, and
   `docs/issue-44/reports/test-authoring.md:193` cite line ranges and
   counts from `b621082`. Re-point at `src/rsb/web/dashboard.js:671-679`,
   10 exports, 9 `_run_dashboard_js` tests. The docstring citation is the
   one that matters most — it is what a future session reads first.

4. **`docs/handbooks/rsb.md` §Tests is not runnable as written (R7c).**
   *addressed_to: test-authoring* (the section is this role-chain's
   output; the `pip install -e .` line it needs to reference is already
   in the same file at `:10`). Either add the prerequisite reference to
   `## Tests` or cross-link `## Install / run`. Worth correcting in the
   same pass: `:48-49` overstates `_run_dashboard_js`'s coverage as the
   whole `module.exports` list (6 of 10 exports are exercised).

5. **AC2 asks for four defect-tracing tests; the spec elsewhere asks for
   three (R5a).** *addressed_to: the issue author.* This is a
   contradiction inside issue #44 itself — AC2's "결함 3건 + Absent 1건에
   각각", 요구사항 2's three-bullet 최소 커버리지 list, and 범위 밖's
   exclusion of visual regression cannot all hold. The artifact covers
   the three enumerated bullets and declares the fourth out of reach
   (jsdom has no layout engine). This role scores the literal AC2 count
   as Absent and does not resolve the contradiction: whether AC2's fourth
   item is struck, or moved to a different harness class in a separate
   issue, is the author's decision, not this review's and not
   test-authoring's.

6. **Not a finding against this PR, recorded so the chain stays legible:**
   the two failing DOM tests on `main` are the pre-existing unguarded
   `window.matchMedia` defect from `f353910`
   (`src/rsb/web/dashboard.js:520`), whose attribution
   `docs/issue-36/reports/conformance-review.md` (Appendix A4) already
   settled and which issue #44's `## Acceptance` note puts outside this
   issue's judgment. It is cited here, not re-derived, and it belongs to
   `src/**` — the implementation role — not to test-authoring. Worth
   noting on its own terms: the harness introduced by PR #45 is what
   makes that defect visible at all, which is precisely the gap issue
   #44 was opened to close.

## Open-finding resolution path

Every finding above is a report, never a patch. The resolution path for
each is the one the role-handoff contract already defines, and none of it
runs in this branch:

- Findings 1–4 are `addressed_to: test-authoring`. Their resolution path
  is a test-authoring session on issue #44, working on
  `issue-44/test-authoring`, delivering through its own PR against `main`
  — findings 1 and 4 touch `test/package.json` and
  `docs/handbooks/rsb.md`, findings 2 and 3 touch that role's own record
  and proposal. This role edits none of those files, and a
  conformance-review PR is not a vehicle for them.
- Finding 5 is `addressed_to: the issue author`. Its resolution path is a
  human decision on issue #44's own text — either AC2's fourth item is
  struck, or it is re-scoped into a separate issue with a harness class
  that can measure layout. No role can resolve it by building.
- Finding 6 is not a finding against this PR and needs no action here;
  its owning role is implementation, under whichever issue takes up the
  `src/rsb/web/dashboard.js:520` guard.

A finding is discharged when the owning role's PR carrying the change is
merged to `main` — an open PR does not discharge it. Re-verification, if
the author wants it, is a fresh conformance-review pass, never an edit to
this record.

## Next steps

1. This record ships as phase-2 output of PR #53 on
   `issue-44/conformance-review`. Nothing further is built in this
   branch; the role's work on issue #44 is complete at delivery.
2. The human decides PR #53 by GitHub act — merge accepts these 32
   verdicts onto the board, closed-unmerged refuses them. This role
   neither merges nor self-approves.
3. Finding 5 needs an authoring decision on issue #44's AC2 / 요구사항 2
   contradiction before any further work targets the mobile-overflow
   item; it blocks nothing else in this record.
4. Findings 1–4 wait on a test-authoring session; this record is the
   hand-off document for it. No follow-up conformance-review pass is
   scheduled or implied — the corrections would be a fresh subject if the
   author wants them re-scored.

## Method notes

- No sampling. All 32 itemized sub-requirements were checked in full, as
  the approved proposal committed to.
- No severity banding was applied; this review's scope was not extended
  into risk weighting.
- Pre-fix replays modified only scratch copies under `$TMPDIR`
  (`DASHBOARD_JS`/`TEST_DIR` re-pointed, every assertion byte-identical),
  deleted after use. A control run of the scratch harness against the
  shipped `dashboard.js` reproduced the real module's outcome (2 failed /
  1 passed over the row-toggle selection), confirming the re-pointing did
  not itself change behavior. `git status --short` is unchanged from
  session start.
- The approved methodology choice (jsdom over browser automation, pytest
  over a second runner) was not re-litigated; R1d checks only that the
  decision was made in the proposal and honored in the tree.
