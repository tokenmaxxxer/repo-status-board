# execution-observation record — issue #44 step 1 (test-authoring, PR #45)

code_under_review: PR #45 (commits `4696840`, `d2b8feb`; squashed to `b2f6b63`), `docs/issue-44/reports/test-authoring.md`
loop_state: landed

## Independence

This role did not author, edit, or contribute to any artifact judged
below. `test/rsb_tests/test_dashboard_dom.py`, `test/package.json`,
`test/package-lock.json`, the `docs/handbooks/rsb.md` hunk, and
`docs/issue-44/reports/test-authoring.md` were all written by the
test-authoring role and landed in `d2b8feb` before this session opened;
nothing under `src/**`, `test/**`, or
`docs/issue-44/{proposals,reports}/test-authoring*` was touched this
session, and this session's only write path is this file. No verdict
below rests on re-executing the observed role's task: the pytest suite
was not run, `npm install --prefix test` was not run, and the harness was
not pointed at any historical revision — per the admissibility rules
fixed in `docs/issue-44/proposals/execution-observation.md:39-71` before
approval. Every verdict-bearing sentence from here on carries its source
adjacent to it.

## Why

Issue #44's 실행 계획 makes execution-observation step 2, observing step
1 (test-authoring). Phase 2 of this observation opened on the issue-level
comment whose entire body is `APPROVE issue-44/execution-observation`,
posted by `jjongkwann`, an account listed in `docs/specs/approvers.md`
(`gh issue view 44 --comments`, this session) — single-account mode,
since PR #52's author is the same account and `gh pr view 52 --json
reviews` carries no PR-review Approve. This record executes
`docs/issue-44/proposals/execution-observation.md` as approved: the three
verdict levels declared at `:17-25`, the admissibility rules at `:39-71`,
and the checks O1–O7 / T1–T4 / S1–S4 at `:72-138`. Its upstream basis is
`docs/issue-44/reports/execution-observation/survey.md` (the observation
scope, the artifact timeline, and the nine write surfaces) and
`.../scout-brief.md` (the evidence standards for a lost red run, for a
single audit finding's shape, and for a deliberate partial-coverage
exclusion).

## What was done

Read first-hand this session, as evidence: `gh issue view 44` (state
OPEN, 4 requirements / 6 ACs / 2-step 실행 계획) and `gh issue view 44
--comments`; `gh pr view 45 --json
number,title,body,author,mergedAt,createdAt,commits,reviews,baseRefName`
(`reviews: []`, author `jjongkwann`, created 2026-08-03T12:07:38Z, merged
2026-08-03T12:31:44Z); `git show --stat --format=… 4696840` and
`… d2b8feb` (full messages, trailers, file lists); `git show d2b8feb --
test/rsb_tests/test_dashboard_dom.py` (all 259 lines as committed),
`… -- docs/handbooks/rsb.md`, `… -- test/package.json`; `git show
b2f6b63:.gitignore`; `docs/issue-44/reports/test-authoring.md` (all 262
lines); `docs/issue-44/proposals/test-authoring.md` and
`docs/issue-44/reports/test-authoring/{survey,scout-brief}.md`;
`docs/specs/approvers.md`; `ls .github/workflows/`; and, as the
historical-markup artifact admitted by rule 2, `git show b621082 --
src/rsb/web/dashboard.js` plus `git show
b621082:src/rsb/web/dashboard.js`. `src/rsb/web/dashboard.js` at HEAD was
deliberately not read as evidence — current `src/` shows what exists now,
not what the observed role did.

Produced: this record — a three-level verdict (outcome, trajectory,
step) with per-sentence citation, and three findings in the four-part
blameless shape. No file outside this path was created or modified, and
no issue was filed.

## Level 1 — outcome: did PR #45 land what issue #44 asked

**Verdict: landed, with one pre-approved scope reduction disclosed and
one acceptance criterion resting on author attestation alone.**

- **O1 — requirement 1 (harness loads `dashboard.js` into a real DOM,
  dispatches events, asserts state): met.** `d2b8feb` adds
  `test/rsb_tests/test_dashboard_dom.py` (+259) whose `_run_dom_js`
  helper builds a `JSDOM` from a 7-id fixture, assigns
  `global.window`/`global.document`, deletes the require-cache entry and
  `require`s the shipped `dashboard.js`, then runs the caller's assertion
  snippet — and the row-toggle tests drive it with real `.click()`
  dispatch (`d2b8feb`, `test_dashboard_dom.py` `_run_dom_js` and
  `test_row_toggle_click_opens_detail_and_flips_aria_expanded`).
- **O2 — requirement 2's three minimum-coverage bullets: all three met,
  and each committed assertion actually asserts the named behavior.**
  Filter-select population is asserted by option-value equality in three
  committed functions (`d2b8feb`:
  `test_repo_filter_options_empty_when_no_repos` → `[""]`,
  `…_populated_for_single_repo` → `["", "repo-a"]`,
  `…_for_multiple_repos_including_errored` → `["", "repo-a", "repo-b"]`);
  `aria-expanded` flipping to `true` on `.row-toggle` click plus a
  non-button-cell click leaving it `false` are asserted by
  `test_row_toggle_click_opens_detail_and_flips_aria_expanded` and
  `test_row_toggle_click_on_non_button_cell_does_not_open_detail`
  (`d2b8feb`); the relative fetch path is asserted as exact string
  equality `result["fetchCalls"] == ["api/board.json"]` in
  `test_load_fetches_relative_board_json_path` (`d2b8feb`).
- **O3 — requirement 3 (usage documented so throwaway scripts stop):
  met.** The `docs/handbooks/rsb.md` hunk in `d2b8feb` adds the
  `npm install --prefix test` prerequisite, the skip-instead-of-fail
  behaviour, and the instruction "Future verification/smoke-check
  sessions should extend this harness (add a test function, reusing
  `_run_dom_js`) instead of writing a new one-off script — this is what
  it exists to replace."
- **O4 — requirement 4 (`_run_dashboard_js` disposition decided): met.**
  The phase-1 proposal decides "`_run_dashboard_js`/`test_model.py` are
  **kept as-is, not migrated**" with its reason
  (`docs/issue-44/proposals/test-authoring.md`, "Adopted methodology"),
  the record restates it at `docs/issue-44/reports/test-authoring.md:191-197`,
  and `git show --stat d2b8feb` lists no `test_model.py` path — decision
  and artifact agree.
- **O5 — the six ACs.** AC1 met per O1's citations. AC2 is addressed
  under O7. **AC3 ("기존 pytest 스위트가 계속 통과한다") is recorded as
  author-attested-only, neither verified nor disputed**: the only claim
  is `docs/issue-44/reports/test-authoring.md:201-205` ("63 passed, 0
  failed, 0 skipped"), and `ls .github/workflows/` this session returns
  only `deploy-board.yml`, so no CI run on `main` attests it
  independently and re-running the suite is barred by admissibility rule
  1. AC4 met per O3. AC5 met — the dependency rationale is at
  `docs/issue-44/reports/test-authoring.md:180-189` (jsdom `^30.0.1`,
  first JS runtime dependency, `test/**`-scoped) with selection rationale
  in the proposal. **AC6 (closing-keyword prohibition) met**: `gh pr view
  45 --json title,body` shows no close/fix/resolve keyword adjacent to
  any `#<n>` reference — the only "fix"-shaped strings are the
  hyphenated "pre-fix" in the Test plan — and issue #44 is still OPEN
  after `b2f6b63` merged at 2026-08-03T12:31:44Z, which independently
  confirms nothing parsed as a closing link.
- **O6 — the count discrepancy is real and resolves against the
  record's own summary line.** `docs/issue-44/reports/test-authoring.md:206`
  says "each of the **5** defect/gap-tracing tests", while its own
  enumeration immediately below names three repo-filter tests, three
  row-toggle tests, and one fetch-path test at
  `docs/issue-44/reports/test-authoring.md:209-216` — seven — and
  `:217-221` excludes exactly one of the eight committed functions (the
  BVA close-toggle case) from re-verification. Counting the artifact
  rather than preferring a number: `d2b8feb` commits 8 test functions,
  8 − 1 = 7, matching the enumeration and not the "5". Recorded as
  finding F1.
- **O7 — the mobile-overflow exclusion is dispositioned, not silent, but
  AC2's literal text remains unmet on one of its four items.** The
  exclusion is written down with its reason (jsdom implements no layout
  engine; measuring rendered width is the visual-regression class issue
  #44's 범위 밖 excludes) in `docs/issue-44/proposals/test-authoring.md`
  ("Note on the mobile-overflow defect"), which was already committed in
  `4696840` at 12:07:05Z — i.e. it sat inside the artifact that the
  approval comment at 12:10:44Z approved
  (<https://github.com/tokenmaxxxer/repo-status-board/issues/44#issuecomment-5166133297>)
  — and it is repeated with the same reason at
  `docs/issue-44/reports/test-authoring.md:251-259`. On the
  documented-deviation standard adopted in
  `docs/issue-44/proposals/execution-observation.md:98-106` that makes it
  a ratified concession rather than a coverage gap, and the record does
  not hide it: the AC2 checkbox at
  `docs/issue-44/reports/test-authoring.md:228-233` carries the exclusion
  inline rather than claiming clean coverage. The residual fact, stated
  plainly because only the human can close it: issue #44's AC2 as
  literally written asks for "결함 3건 + Absent 1건", and 3 of those 4
  have tests. No deficiency finding is raised, because the deviation was
  declared before approval and disclosed after it.

## Level 2 — trajectory: was the phase-1 → phase-2 path sound

**Verdict: sound on all four checks.**

- **T1 — phase ordering held.** `git show --stat 4696840` (2026-08-03
  T12:07:05Z) lists exactly three docs paths — the proposal, the survey,
  and the scout brief — and no `test/**` path and no record file, so
  nothing phase-2-shaped landed before the PR opened at 12:07:38Z
  (`gh pr view 45 --json createdAt`); every phase-2 artifact, the record
  included, arrives in `d2b8feb` at 12:24:41Z, after the 12:10:44Z
  approval.
- **T2 — the approval path is the valid one for this repo's mode.** PR
  #45's author is `jjongkwann` and `docs/specs/approvers.md` lists
  exactly `JiwonJung94` and `jjongkwann`, so with `gh pr view 45 --json
  reviews` returning `[]` this is single-account mode and the
  issue-comment path applies; comment 5166133297's body is exactly
  `APPROVE issue-44/test-authoring` by `jjongkwann`
  (<https://github.com/tokenmaxxxer/repo-status-board/issues/44#issuecomment-5166133297>),
  an exact string match for `APPROVE issue-<n>/<role>` under
  string-equality-only. No approval-shaped near-miss comment exists on
  issue #44 to report.
- **T3 — the survey-then-scout obligation was met, in that order.**
  `4696840` commits `docs/issue-44/reports/test-authoring/survey.md`
  (+162) and `scout-brief.md` (+75) together, and the scout brief is
  demonstrably aimed at the survey's gaps rather than at the issue text
  — it cites "survey §3" and "survey §5" in its own gap line — while
  declaring its mode and budget in its opening line ("parallel sweep, 4
  angles in one turn … 1 stage total, ~20s") and carrying a 10-URL
  `Sources` list. The proposal's declared phase-2 scope
  (`docs/issue-44/proposals/test-authoring.md`, "Status": test code,
  `test/package.json`, the `.gitignore` hand-off, the handbook update,
  the record) matches what `git show --stat d2b8feb` actually landed,
  with the `.gitignore` item converted to a hand-off — see F2.
- **T4 — commit hygiene is mechanically clean.** `git show -s
  --format=%B` on both `4696840` and `d2b8feb` shows a `Subject:
  issue-44` trailer on each, one commit per phase per subject, and
  neither commit's `--stat` stages a path belonging to another issue.

## Level 3 — step: which specific artifact is deficient

**Verdict: the test artifact itself is sound; three record- and
PR-metadata-level deficiencies, F1–F3 below.**

- **S1 — the `.gitignore` hand-off is disclosed but unowned.** `git show
  b2f6b63:.gitignore` returns exactly `.venv/`, `__pycache__/`, `*.pyc`,
  `.pytest_cache/`, `*.egg-info/` — no `node_modules/` — while `d2b8feb`
  adds a handbook instruction to run `npm install --prefix test`; the
  record discloses this at
  `docs/issue-44/reports/test-authoring.md:243-250`, and its mitigating
  claim that the commit staged nothing under `test/node_modules/` is
  confirmed by `git show --stat d2b8feb`'s five-file list. The deficiency
  is in the hand-off's addressing, not its disclosure — finding F2.
- **S2 — PR #45's title contradicts its content, and that title is what
  reached `main`.** The title reads "issue-44 **phase 1**: DOM-layer test
  harness survey + scout + proposal" while the body's first line reads
  "issue #44 (test-authoring role), both phases." and `d2b8feb` is in the
  same PR; the squash merge carried the title into `main`'s history as
  `b2f6b63 issue-44 phase 1: DOM-layer test harness survey + scout +
  proposal (#45)` (`git log --oneline`). Finding F3.
- **S3 — the non-button-cell test does discriminate; resolved against
  the historical markup artifact.** The selector `main table tbody tr td`
  lands on the first `<td>` of the first row, which at revision
  `b621082` is `` `<td>${escapeHtml(d.repo)}</td>` `` — `decisionRows`'
  `cells[0]`, plain text, no button (`git show
  b621082:src/rsb/web/dashboard.js`, `decisionRows`) — so the click
  genuinely targets a non-button element, and pre-fix at `b621082^` the
  handler sat on the `<tr>` (the diff of `b621082` removes `` `<tr
  data-issue="${r.issue}" …>` `` and adds a binding that "Binds only to
  `.row-toggle` buttons"), meaning the same click would have bubbled and
  opened the panel. The test function's name is accurate; the record's
  shorthand for it at
  `docs/issue-44/reports/test-authoring.md:212` ("empty-cell") is not —
  that cell renders the repo name. Nit, not a finding.
- **S4 — the BVA test's un-reverified status is completely
  self-disclosed.** `docs/issue-44/reports/test-authoring.md:217-221`
  names the test, states it was not re-run against a pre-fix revision,
  and gives the reason (it builds on behaviour already shown broken), so
  nothing about its limit has to be inferred; no deficiency.

## Findings

### F1 — the record's defect-tracing test count contradicts its own enumeration

- **Impact.** The pre-fix verification runs left no artifact — the
  extracted revisions were "scratch files, deleted after use, never
  committed" (`docs/issue-44/reports/test-authoring.md:207-208`) — so the
  record's count is the only surviving statement of how much
  re-verification actually happened. A later session reading it cannot
  tell whether 4, 5, or 7 tests were re-run against pre-fix code, and
  cannot reproduce the check to find out.
- **Timeline.** 2026-08-03T12:24:41Z — `d2b8feb` commits the record
  carrying "each of the 5 defect/gap-tracing tests" at `:206` above an
  enumeration of 3 + 3 + 1 at `:209-216`. 2026-08-03T12:31:44Z — PR #45
  merges as `b2f6b63` with a Test plan line reading "Each of the 3 defect
  + 1 Absent-gap tests", a third number.
- **Root cause.** Two counting granularities coexist in one section —
  defect *categories* in the summary line and the PR body, test
  *functions* in the enumeration — and were never reconciled before the
  commit.
- **Action item.** Restate
  `docs/issue-44/reports/test-authoring.md:206` as a test-function count
  matching its own enumeration (7 of the 8 committed functions, the BVA
  case excluded per `:217-221`). Verifiable by reading that line against
  `:209-221`. Owner-shaped target: the test-authoring role, on an issue
  the human files if they agree — this role files none.

### F2 — the `.gitignore` hand-off names no owner, and nothing routes it

- **Impact.** `test/node_modules/` (38 packages,
  `docs/issue-44/reports/test-authoring.md:182-183`) is untracked and
  unignored at `b2f6b63` (`git show b2f6b63:.gitignore`), while
  `d2b8feb`'s handbook hunk instructs every future session to create it
  via `npm install --prefix test`. The first session that does so and
  stages broadly can commit a vendored dependency tree into the repo.
- **Timeline.** 2026-08-03T12:24:41Z — `d2b8feb` adds both the handbook
  instruction and the hand-off note. 2026-08-03T12:31:44Z — merged as
  `b2f6b63` with `.gitignore` unchanged.
- **Root cause.** The `test/**` write scope correctly stopped the
  observed role from editing repo-root `.gitignore`, but the disposition
  it chose — a sentence addressed to "Whichever role/session next touches
  repo-root config" (`docs/issue-44/reports/test-authoring.md:250`) — is
  addressed to nobody, and under contract v3 issues are user-authored
  only, so no mechanism delivers it to a role.
- **Action item.** Add `node_modules/` to repo-root `.gitignore` through
  a role with that write scope. Verifiable by `git show main:.gitignore`
  containing the entry. Owner-shaped target: an implementation-scoped
  session on an issue the human files; this role neither files it nor
  makes the edit.

### F3 — PR #45's "phase 1" title carried into `main`'s history for a two-phase PR

- **Impact.** The board is what is merged to `main`, and `main`'s history
  line for this work is `b2f6b63 issue-44 phase 1: DOM-layer test harness
  survey + scout + proposal (#45)` (`git log --oneline`). Any session or
  reader reconstructing issue #44's state from merged titles — the
  cheapest and most common way to read the board — concludes only the
  proposal landed and the harness is still to be built, when `d2b8feb`
  in fact added 259 lines of DOM tests.
- **Timeline.** 2026-08-03T12:07:38Z — PR #45 opened with the phase-1
  title, carrying only `4696840`, correctly per contract v3 s19.
  12:24:41Z — `d2b8feb` lands phase 2 on the same PR; title unchanged.
  12:31:44Z — squash-merged as `b2f6b63`, title now permanent in history.
- **Root cause.** Contract v3 s19 requires the PR to be opened at the
  phase-1 boundary and reused for phase 2, but says nothing about
  updating its title when phase 2 lands, so the accurate-at-open title
  became inaccurate-at-merge with no step prompting a revision.
- **Action item.** Add a phase-2 step requiring the PR title to be
  updated when phase-2 commits are pushed, in the role handbook or
  contract text. Verifiable by that line existing under `docs/`. The
  title of the already-merged PR #45 is not retroactively fixable in
  `main`'s squashed history. Owner-shaped target: the human, via the
  contract document — this role files no issue.

## Verdict summary

| level | verdict | anchor |
| --- | --- | --- |
| outcome | landed — 4/4 requirements and 5/6 ACs met outright; AC2 met as scoped by the pre-approved mobile-overflow concession; AC3 author-attested only | `d2b8feb`, `docs/issue-44/reports/test-authoring.md:201-239` |
| trajectory | sound — survey→scout→proposal→PR→approval→phase 2, in that order, with a valid single-account approval | `4696840` / `d2b8feb` stats and timestamps, issuecomment-5166133297 |
| step | test artifact sound; three documentation/metadata deficiencies F1–F3 | `docs/issue-44/reports/test-authoring.md:206`, `:250`, PR #45 title |

No level was omitted; none was "not applicable" this observation. All of
O1–O7, T1–T4 and S1–S4 declared in
`docs/issue-44/proposals/execution-observation.md:72-138` are resolved
above, except AC3 under O5, which is recorded as
not-resolvable-from-artifacts and left as author attestation rather than
being converted into a finding.

## Open findings

- **F1, F2, F3 above remain open.** None is actionable by this role:
  under contract v3 issues are user-authored only, and this role may not
  edit the observed role's `docs/issue-44/reports/test-authoring.md`, the
  repo-root `.gitignore`, or PR #45's already-merged title. They are
  returned here, on this role's PR, for the human to judge and route.
- **AC3 stays unattestable from artifacts.** `ls .github/workflows/`
  shows only `deploy-board.yml`, so "63 passed" at
  `docs/issue-44/reports/test-authoring.md:204-205` has no independent
  corroboration and cannot acquire one until a test-gate workflow exists
  on `main` — which issue #44's 범위 밖 explicitly defers. Recorded as a
  standing limit of this observation, not as a defect in PR #45.
- No other findings.
