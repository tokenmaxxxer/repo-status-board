# issue-44 execution-observation — current-state survey

## 0. Observation scope (who/what is under observation)

- **Issue**: #44 — "JS DOM 계층 테스트 하네스 도입 — 배선 결함 3건이 통과한
  공백 메우기" (`gh issue view 44`, state OPEN, author `jjongkwann`).
- **Observed role**: `test-authoring` — issue #44's 실행 계획 step 1.
- **Observed session**: the single test-authoring session that produced both
  phases on branch `issue-44/test-authoring`, 2026-08-03 12:07:05Z →
  12:24:41Z (commit author timestamps below).
- **Observed PR**: **#45** —
  <https://github.com/tokenmaxxxer/repo-status-board/pull/45>, author
  `jjongkwann`, state MERGED at 2026-08-03T12:31:44Z, merge commit
  `b2f6b63`.
- **Observed commits**: `4696840` (phase 1) and `d2b8feb` (phase 2), squashed
  into `b2f6b63` on `main`.
- **Observed record**: `docs/issue-44/reports/test-authoring.md` (262 lines,
  added by `d2b8feb`).
- **This role**: execution-observation, issue #44 실행 계획 step 2, branch
  `issue-44/execution-observation`. This survey is phase-1 material; it
  describes what exists and what is unknown, and renders no judgment.

## 1. What was actually read this session

Read first-hand in this session, not summarized from elsewhere:

- `gh issue view 44` — full issue body: 4 requirements, 3 out-of-scope
  bullets, 6 acceptance criteria, 2-step 실행 계획.
- `gh issue view 44 --json comments` — the sole issue comment,
  <https://github.com/tokenmaxxxer/repo-status-board/issues/44#issuecomment-5166133297>,
  author `jjongkwann`, created 2026-08-03T12:10:44Z, body exactly
  `APPROVE issue-44/test-authoring`.
- `gh pr view 45 --json number,title,body,state,mergedAt,mergeCommit,commits,reviews,comments,headRefOid,files,createdAt,latestReviews`
  — PR body, both commit messages and SHAs, the 8-file change list,
  `reviews: []`, `latestReviews: []`, `comments: []`, `createdAt`
  2026-08-03T12:07:38Z.
- `git show d2b8feb` — phase-2 diff: `--stat`, the `docs/handbooks/rsb.md`
  hunk, `test/package.json`, and the full 259-line
  `test/rsb_tests/test_dashboard_dom.py` as committed.
- `git show --stat --format=... b2f6b63` — the squash merge commit and its
  two-part message body.
- `docs/issue-44/reports/test-authoring.md` — the observed role's own
  record, all 262 lines.
- `docs/issue-44/proposals/test-authoring.md` — the observed role's
  phase-1 proposal, all 294 lines.
- `docs/issue-44/reports/test-authoring/survey.md` (162 lines) and
  `.../scout-brief.md` (75 lines) — the observed role's phase-1 research.
- `docs/specs/approvers.md`, `.gitignore`, `docs/handbooks/rsb.md` "Tests"
  section, `ls .github/workflows/` — repo state on `b2f6b63`.

Not read as evidence, deliberately: `src/rsb/web/dashboard.js` at HEAD.
Per this role's directive, current `src/` shows what exists now, not what
the observed role did; the observed role's write scope was `test/**` and
it changed no `src/` file (`git show d2b8feb --stat` lists no `src/`
path).

## 2. Delivery timeline reconstructed from artifacts

| time (UTC, 2026-08-03) | artifact | source |
| --- | --- | --- |
| 12:07:05 | commit `4696840` "issue-44 phase 1: DOM-layer test harness survey + scout + proposal", trailer `Subject: issue-44` | `gh pr view 45 --json commits` |
| 12:07:38 | PR #45 opened | `gh pr view 45 --json createdAt` |
| 12:10:44 | issue #44 comment, body exactly `APPROVE issue-44/test-authoring`, by `jjongkwann` | issuecomment-5166133297 |
| 12:24:41 | commit `d2b8feb` "issue-44 phase 2: jsdom DOM-wiring test harness for dashboard.js", trailer `Subject: issue-44` | `gh pr view 45 --json commits` |
| 12:31:44 | PR #45 merged as `b2f6b63` | `gh pr view 45 --json mergedAt,mergeCommit` |

Mode facts bearing on which approval path applies: PR #45's author is
`jjongkwann` (`gh pr view 45 --json author` via `gh pr list`), and the
approval-comment author is `jjongkwann`; `docs/specs/approvers.md` lists
exactly `JiwonJung94` and `jjongkwann`. PR #45 carries no PR-review
Approve (`reviews: []`, `latestReviews: []`).

## 3. What landed, by file (`git show d2b8feb --stat`, `4696840`)

Phase 1 (`4696840`, docs only):
`docs/issue-44/reports/test-authoring/survey.md` (+162),
`docs/issue-44/reports/test-authoring/scout-brief.md` (+75),
`docs/issue-44/proposals/test-authoring.md` (+294).

Phase 2 (`d2b8feb`, 1060 insertions / 0 deletions):
`test/rsb_tests/test_dashboard_dom.py` (+259),
`test/package.json` (+8), `test/package-lock.json` (+514),
`docs/handbooks/rsb.md` (+17), `docs/issue-44/reports/test-authoring.md`
(+262). No `src/**` path appears in either commit's stat.

`test/rsb_tests/test_dashboard_dom.py` as committed defines 8 pytest
functions over one `_run_dom_js(script, fetch_body)` helper: 3 repo-filter
option tests, 4 `.row-toggle` click tests, 1 `load()` fetch-path test.
The helper spawns `node -e` per test, builds a `JSDOM` from a 7-id
`DASHBOARD_HTML` fixture, installs `global.window`/`global.document`/a
recording `global.fetch`, `delete`s the require-cache entry, `require`s
`DASHBOARD_JS`, awaits one `setTimeout(…, 0)` tick, then runs the
caller's assertion snippet and parses its JSON stdout. Two
`pytest.skip()` gates: `shutil.which("node") is None`, and
`TEST_DIR/"node_modules"/"jsdom"` missing.

## 4. Write surfaces this observation has to reach, and what is known about each

Ordered by how much of the answer already sits in an artifact.

1. **Requirement 1 (harness exists)** — `test_dashboard_dom.py` and
   `test/package.json` are in `d2b8feb`. Fully documentary; nothing
   unknown.
2. **Requirement 3 (temp-script replacement documented)** — the
   `docs/handbooks/rsb.md` hunk in `d2b8feb` adds the
   `npm install --prefix test` prerequisite and the sentence "Future
   verification/smoke-check sessions should extend this harness … instead
   of writing a new one-off script". Fully documentary.
3. **Requirement 4 (`_run_dashboard_js` disposition)** — proposal
   `docs/issue-44/proposals/test-authoring.md:84-90` decides "kept as-is,
   not migrated"; record `docs/issue-44/reports/test-authoring.md:191-197`
   repeats it; `d2b8feb --stat` shows `test_model.py` unchanged. Fully
   documentary.
4. **AC "새 런타임 의존성 근거가 record 에 남는다"** — record lines 180-189
   plus proposal "Rationale". Documentary.
5. **AC "기존 pytest 스위트가 계속 통과한다"** — asserted at record line
   204-205 ("63 passed, 0 failed, 0 skipped") and in the PR body. *Unknown
   from artifacts*: `ls .github/workflows/` returns only
   `deploy-board.yml`; there is no test-gate workflow on `main`, so no CI
   run attests this independently, and this role may not re-run the
   observed role's suite to check. What evidence can substitute is an open
   question — scout angle A/C below.
6. **AC "결함 3건 + Absent 1건 … 해당 결함 상태에서 실제로 실패함이 확인된다"**
   — the contested surface. The record's Verification section (lines
   206-221) claims per-test failure against pre-fix revisions `c94e12d^`,
   `b621082^`, `3ebecae^`, with the extracted scratch files "deleted after
   use, never committed" (line 208). So the failing runs left no artifact.
   Two sub-unknowns:
   - **Count discrepancy, unadjudicated.** Record line 206 says "each of
     the **5** defect/gap-tracing tests"; the enumeration immediately
     below it (lines 209-216) names the repo-filter population tests
     (3 functions exist), three row-toggle tests, and the fetch-path test
     — 7 by that reading — with line 217-221 excluding only the BVA
     close-toggle test from the 8. The PR body instead says "the 3 defect
     + 1 Absent-gap tests". Which number the artifacts support is exactly
     what phase 2 has to settle; this survey records the discrepancy
     without resolving it.
   - **Defect #3 (mobile overflow, issue #38 P1-1) has no test.** Record
     lines 251-259 and proposal lines 210-218 both state this is by
     design, arguing issue #44's own requirement-2 bullet list names only
     three items and its 범위 밖 excludes visual regression, while the AC
     text says "결함 3건 + Absent 1건". Reading the AC against the
     requirement-2 bullet list is a judgment the phase-2 verdict must
     make explicitly, not inherit from the record.
7. **`.gitignore` hand-off** — record lines 243-250 flag `node_modules/`
   as needed and outside scope. `.gitignore` on `b2f6b63` still reads
   exactly `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`,
   `*.egg-info/` — no `node_modules/` entry. Under contract v3 this role
   may not file the issue; whether the record's hand-off shape is
   sufficient disposition is a phase-2 question.
8. **PR title/content mismatch.** PR #45's title is "issue-44 **phase 1**:
   DOM-layer test harness survey + scout + proposal" while the PR carries
   both phases (its own body opens "issue #44 (test-authoring role), both
   phases."). Recorded here as a fact about the artifact; its weight is a
   phase-2 question.
9. **Test-artifact validity.** Whether each committed assertion actually
   discriminates the behavior it claims to trace to — e.g.
   `test_row_toggle_click_on_non_button_cell_does_not_open_detail`
   selects `main table tbody tr td` (first cell) and asserts no detail
   opens. Determining whether that first `<td>` is genuinely a non-button
   cell requires evidence about the markup `renderData` emits. Which
   evidence source is admissible for that under this role's src/-reading
   prohibition is an open method question — scout angle B/D below.

## 5. Gaps this survey hands to scout

- **A.** How do strong delivery/execution audits substantiate a "this
  test would have caught the defect" claim when the failing run left no
  artifact — what is the field's evidence standard (mutation testing,
  committed red-run output, CI attestation)?
- **B.** What is the field-standard shape of a single audit finding that
  must carry impact / timeline / root cause / action item without
  becoming a full postmortem?
- **C.** How do review practices treat self-reported test results in the
  absence of CI — accepted as attestation, or treated as unverified?
- **D.** How do requirement→test traceability audits check an AC-coverage
  claim, in particular a deliberate partial-coverage exclusion argued
  from the requirement text itself?
