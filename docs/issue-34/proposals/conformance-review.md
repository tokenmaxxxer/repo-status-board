# Conformance-review proposal (issue #34)

Scope: check the merged implementation (PR #35, `issue-34/implementation`,
merged to `main` at commit `5d05b5f`) against issue #34's 7
acceptance-criteria checkboxes, working from the artifact and the issue
text directly per this role's phase-2 mandate — not from
`docs/issue-34/reports/implementation.md`'s self-report of what was done
(that self-report, and this survey's own observations, are read only to
orient where to look; see `docs/issue-34/reports/conformance-review/
survey.md`).

## Method

Phase 2 will produce `docs/issue-34/reports/conformance-review.md` as a
per-requirement verdict table using `review-traceability`'s
`finding-record` skill: one row per requirement below, verdict ∈
{Present, Surface, Absent, Incorrect, Unverifiable}, an evidence pointer
(file:line, test name, live-URL fetch, or "no local means to observe"),
and a rationale. `review-severity`'s `severity-classification` is applied
only to findings that are not Present, if any survive.

Per this task's own framing, each of the 7 acceptance-criteria checkboxes
below is its **own** requirement (R1–R7), kept 1:1 traceable to the
issue's 7 `- [ ]` items — unlike this repo's issue-23 conformance-review
precedent (`docs/issue-23/proposals/conformance-review.md`), which
decomposed each AC into independently-checkable sub-facts, this proposal
does not split or merge any checkbox. No verdicts are assigned here —
only the verification method each Rn will use.

## Requirement list

**R1 — "board.json 의 각 레코드에서 owner/name 을 얻을 수 있다"**
(owner/name is obtainable from each record in board.json).
- Method: read `src/rsb/model.py` (`BoardModel.owner_name_by_repo`
  field, `normalize_payload()`'s `owner_name` extraction, `merge_repos()`
  population) and `src/rsb/render.py` (`render_json_model()`'s
  `owner_name_by_repo` output key); read
  `test/rsb_tests/test_model.py`/`test_render.py`/`test_webserver.py`'s
  owner-name assertions.
- Method: load the live `https://tokenmaxxxer.github.io/repo-status-board/api/board.json`
  and inspect whether `owner_name_by_repo` is present and non-null for
  the 3 configured repos (`on-the-record`, `repo-status-board`,
  `tokenmaxxxer-core`, per `.github/boards.ci.toml`).

**R2 — "이슈 번호에서 GitHub 이슈로 이동한다 (3개 레포 모두)"**
(issue number navigates to the GitHub issue, all 3 repos).
- Method: read `src/rsb/web/dashboard.js`'s `buildGithubUrl`,
  `externalLinkHtml`, `issueToggleCell`, and its four call sites
  (`decisionRows`, `flowRows`, `sessionRows`, `renderAccounting`).
- Method: run `node -e` against the shipped, unmodified `dashboard.js`
  (via its `module.exports`), calling `buildGithubUrl`/`externalLinkHtml`
  with each of the 3 repos' real `owner/name` values (fetched per R1) and
  a sample issue number, confirming the resulting URL string is exactly
  `https://github.com/<owner>/<name>/issues/<n>`.
- Method: manually click an issue-number's external-link affordance in
  the deployed UI (or a locally served `rsb serve` instance) in a real
  browser, for at least one row from each of the 3 repos, and confirm
  the rendered `<a href>` navigates to the correct GitHub issue URL.

**R3 — "PR 번호(decision queue, flows PRs 열)에서 GitHub PR 로 이동한다"**
(PR number navigates to the GitHub PR, decision-queue + Flows PRs
column).
- Method: read `src/rsb/web/dashboard.js`'s `prCellHtml` and its two call
  sites (`decisionRows`'s single-PR cell, `flowRows`'s multi-PR cell).
- Method: run `node -e` against the shipped `dashboard.js`, calling
  `buildGithubUrl(ownerName, "pull", n)` and confirming
  `.../pull/<n>`.
- Method: manually click a PR-number link in both the Decision queue and
  the Flows table's PRs column in the deployed UI or a local `rsb serve`
  instance, confirming each navigates to the correct GitHub PR URL.

**R4 — "상세 패널을 여는 기존 동작이 회귀하지 않는다 (클릭·키보드 모두)"**
(the existing detail-panel-opening behavior does not regress, both click
and keyboard).
- Method: diff `src/rsb/web/dashboard.js`'s `issueToggleCell`,
  `attachRowClickHandlers`, `rowToggleId`, `isRowExpanded` against the
  pre-PR-#35 version (`git show <parent-of-5d05b5f>:src/rsb/web/dashboard.js`)
  to confirm the `row-toggle` button's own markup/click-handler wiring is
  byte-identical, with the new `external-link` anchor only appended as
  trailing sibling markup.
- Method: manually click the `row-toggle` button (not the external-link
  icon) in the deployed UI or a local `rsb serve` instance and confirm
  the detail panel still opens/closes as before.
- Method: manually Tab through a table row's Issue cell in a real
  browser and confirm focus visits `row-toggle` and `external-link` as
  two separate stops with no overlap, and that Enter/Space activates
  each control's own action (`row-toggle` → panel toggle,
  `external-link` → navigation) without either intercepting the other's
  keypress.

**R5 — "owner/name 없는 레코드가 깨진 링크를 만들지 않는다"**
(a record without owner/name does not produce a broken link).
- Method: read `buildGithubUrl`/`externalLinkHtml`'s falsy/non-string
  guard clauses in `src/rsb/web/dashboard.js`.
- Method: run `node -e` against the shipped `dashboard.js`, calling
  `buildGithubUrl(null, "issues", 5)` and `externalLinkHtml(null,
  "issues", 5, "...")` directly and confirming `null`/`""` respectively
  (no `href="undefined"`/`href="null"` string).
- Method: run `python3 -c "import sys; sys.path.insert(0, 'src'); import
  pytest; sys.exit(pytest.main(['test/rsb_tests/test_model.py', '-q',
  '-k', 'owner_name']))"` to confirm the `MISSING_OWNER_NAME_PAYLOAD`
  (`test/rsb_tests/fixtures.py:190`) test cases pass on `main`.
- Method: if the live/local board has any repo with a null
  `owner_name_by_repo` entry, inspect that repo's rendered rows in a
  browser's DOM inspector and confirm no `<a class="external-link">`
  element is present for that repo's cells (plain text only).

**R6 — "기존 테스트 전부 통과"** (all existing tests pass).
- Method: run the full suite on `main` at commit `5d05b5f` via
  `python3 -c "import sys; sys.path.insert(0, 'src'); import pytest;
  sys.exit(pytest.main(['test/', '-q']))"`, record the exact pass/fail/
  skip counts and exit code, and compare against
  `docs/issue-34/reports/implementation.md`'s self-reported "53 passed,
  0 failed, 0 skipped" rather than accepting that figure unverified.

**R7 — "주의: PR 본문에 closing 키워드 금지 (issue #23 T2 — 백틱 인용도
파싱됨)"** (caution: no closing keywords in the PR body, backtick-quoted
included).
- Method: `gh pr view 35 --json body` (or view PR #35 on github.com
  directly) and read the full body text — including any backtick-quoted
  or code-fenced spans — for `Closes`/`Fixes`/`Resolves`/`Close`/`Fix`/
  `Resolve` immediately adjacent to `#34` in any casing/form, per the
  issue #23 T2 precedent that GitHub parses closing keywords inside
  backticks too.

## Out of scope for this role

- Fixing anything found — per contract, conformance-review records
  findings; it does not patch `src/`/`test/`/`docs/`. Any non-Present
  verdict hands off to a follow-up issue, matching this repo's
  `docs/issue-4/reports/conformance-review.md` /
  `docs/issue-23/reports/conformance-review.md` precedent.
- Re-litigating PR #35's own internal self-check
  (`docs/issue-34/reports/implementation.md`'s "Self-check" section) —
  phase 2 independently re-checks R1–R7 against the artifact, it does
  not re-run or grade that self-check.
- Anything outside issue #34's 7 acceptance criteria (e.g. `render.py`
  CLI-renderer links, additional GitHub API calls) — both are explicitly
  out of scope per the issue body's own "범위 밖" section, unchanged by
  this review.

## Deliverable

`docs/issue-34/reports/conformance-review.md`: one row per R1–R7 above,
verdict (Present/Surface/Absent/Incorrect/Unverifiable), evidence
pointer, rationale; a findings section, severity-classified, for any
non-Present row. Gated behind a human Approve per role-handoff contract
v3 §19 (see this role's PR body for the exact approval mechanism) —
not produced by this phase-1 PR.
