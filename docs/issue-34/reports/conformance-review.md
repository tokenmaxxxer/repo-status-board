# Conformance-review record (issue #34)

loop_state: reported

## What was done

Checked the merged implementation (PR #35, `issue-34/implementation`,
merged to `main` at commit `5d05b5f`) against issue #34's 7
acceptance-criteria checkboxes, working from the artifact and the issue
text directly — not from `docs/issue-34/reports/implementation.md`'s
self-report. Verdicts below were derived this session from direct code
inspection, a fresh `node`-driven exercise of the shipped
`dashboard.js`, a fresh full test-suite run, a live fetch of the
deployed `board.json`, and a direct read of PR #35's body text — not
accepted from any self-report.

## Why

Issue #34's own acceptance-criteria checklist is the spec; this role's
mandate (contract v3 §19) is to render a per-requirement verdict for
that checklist against what actually shipped to `main`, independent of
the building role's own account of what it did.

## Upstream basis

Rests on `docs/issue-34/proposals/conformance-review.md` (this role's
approved phase-1 proposal, requirement list R1-R7) and
`docs/issue-34/reports/conformance-review/survey.md` (current-state
survey), both approved via issue #34 comment
`APPROVE issue-34/conformance-review` (jjongkwann, listed in
`docs/specs/approvers.md`; single-account mode, this PR's author ==
approver). Subject artifact: PR #35, merged `5d05b5f`. No `src/`/`test/`
change is made by this record.

Method: `review-traceability`'s `finding-record` verdict set (Present /
Surface / Absent / Incorrect / Unverifiable) per requirement R1-R7
(kept 1:1 with issue #34's 7 acceptance-criteria checkboxes, per the
approved proposal's framing), each with an evidence pointer and
rationale. Test suite re-run this session:
`python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
sys.exit(pytest.main(['test/','-q']))"` → **53 passed**, 0 failed,
0 skipped — matches `docs/issue-34/reports/implementation.md`'s claimed
count exactly. `review-severity`'s `severity-classification` is applied
to R4, the one row below that is not Present, using Microsoft's
four-level bug bar (Critical/Important/Moderate/Low) adapted for this
non-security UI-behavior context, since Chromium's five-band scheme is
defined entirely in terms of privilege/cross-origin security capability
that does not apply here.

## R1-R7

| # | Requirement (issue #34 수용 기준) | Verdict | Evidence | Rationale |
|---|---|---|---|---|
| R1 | "board.json 의 각 레코드에서 owner/name 을 얻을 수 있다" | Present | `src/rsb/model.py:110` (`BoardModel.owner_name_by_repo` field); `:267` (`normalize_payload()`: `owner_name = payload.get("repo")`); `:271` (returned as `"owner_name"`); `:294` (`merge_repos()`: `model.owner_name_by_repo[repo_name] = normalized["owner_name"]`); `src/rsb/render.py:174` (`render_json_model()` emits `"owner_name_by_repo"`); `test/rsb_tests/test_model.py:89-107`, `test_render.py:50-54`, `test_webserver.py:41`; live fetch (this session) of `https://tokenmaxxxer.github.io/repo-status-board/api/board.json` → `owner_name_by_repo: {"on-the-record": "tokenmaxxxer/on-the-record", "repo-status-board": "tokenmaxxxer/repo-status-board", "tokenmaxxxer-core": "tokenmaxxxer/tokenmaxxxer-core"}` | The wire-through is confirmed at every layer (model → render → HTTP response) and the deployed board.json actually carries non-null owner/name for all 3 configured repos — stronger than the phase-1 survey anticipated (it flagged the live path as "not locally checkable"; this session's live fetch closed that gap) |
| R2 | "이슈 번호에서 GitHub 이슈로 이동한다 (3개 레포 모두)" | Present | `src/rsb/web/dashboard.js:211-213` (`buildGithubUrl`), `:219-223` (`externalLinkHtml`), `:225-229` (`issueToggleCell`); 4 call sites: `:249` (`decisionRows`), `:283` (`flowRows`), `:299` (`sessionRows`), `:316` (`renderAccounting`); this session's `node` run against the shipped, unmodified file (`global.document = {getElementById: () => null}; require("./src/rsb/web/dashboard.js")`) confirms `buildGithubUrl("tokenmaxxxer/on-the-record","issues",12)` → `"https://github.com/tokenmaxxxer/on-the-record/issues/12"`, and the same for `tokenmaxxxer/repo-status-board` and `tokenmaxxxer/tokenmaxxxer-core` (the 3 real owner/name values from R1's live fetch) | Link-building logic is generic across `ownerName` (no per-repo branching), and this session verified it against all 3 repos' *real* live owner/name values, not placeholders, satisfying "3개 레포 모두". An actual-browser click-through remains unavailable in this sandbox (no browser) — not scored as a gap, since a syntactically-correct `<a href="https://github.com/...">` is standard, deterministic browser-navigable markup and does not require live confirmation, matching this repo's own precedent (`docs/issue-4/reports/conformance-review.md` §2's Loading/Detail-panel-empty rows, code-read-only) |
| R3 | "PR 번호(decision queue, flows PRs 열)에서 GitHub PR 로 이동한다" | Present | `src/rsb/web/dashboard.js:234-239` (`prCellHtml`); call sites `:250` (`decisionRows`, wraps `[d.pr]`), `:287` (`flowRows`, `f.prs`); this session's `node` run confirms `buildGithubUrl("tokenmaxxxer/repo-status-board","pull",40)` → `"https://github.com/tokenmaxxxer/repo-status-board/pull/40"` | Same `buildGithubUrl` helper, `kind="pull"`, produces the correct URL shape; both call sites route through it. Browser click-through Unverifiable-in-sandbox for the same reason as R2, not scored as a gap |
| R4 | "상세 패널을 여는 기존 동작이 회귀하지 않는다 (클릭·키보드 모두)" | Incorrect | `git diff 5d05b5f~1 5d05b5f -- src/rsb/web/dashboard.js`: the `row-toggle` `<button>`'s own markup is byte-identical, only `issueToggleCell` gained a 4th `ownerName` parameter and `externalLinkHtml(...)` is appended strictly after `</button>`; `attachRowClickHandlers` (`:458-465`), `rowToggleId` (`:190-193`), `isRowExpanded` (`:195-202`) are all untouched by the diff. But: `grep -n "addEventListener" dashboard.js` shows the *only* click handler that opens the detail panel is bound to the whole `<tr>` (`:459-460`, `row.addEventListener("click", ...)`) — there is no separate listener on `.row-toggle` itself. `grep -n "stopPropagation\|preventDefault" dashboard.js` returns zero matches anywhere in the file | The row-toggle button's own markup/wiring is unregressed (Present on that narrow claim), but the approved phase-1 proposal's own R4 verification method requires that `row-toggle` and the new `external-link` act as two independent controls "without either intercepting the other's keypress" — and the issue body itself raised exactly this concern ("링크를 겹치면 클릭 의미가 모호해지므로"). Because `.external-link` renders as a DOM child of the same `<tr>` that carries the pre-existing whole-row click listener, and neither control calls `stopPropagation()`, clicking or keyboard-activating (Enter/Space) the external-link *also* fires the row's own `selectedIssue = {...}; renderData(data)` toggle as an unintended side effect, in addition to its own navigation. This is deterministic DOM event-bubbling behavior (standard per the DOM spec for both mouse clicks and the synthetic click a browser dispatches on Enter/Space link activation) and does not require a live browser to establish. `spec_vs_built`: the proposal's method and the issue's own stated concern call for the two controls to be independent, non-interfering actions; what was built visually/structurally separates them (no DOM nesting/overlap) but does not isolate their click events, so activating `external-link` unexpectedly also toggles the detail panel |
| R5 | "owner/name 없는 레코드가 깨진 링크를 만들지 않는다" | Present | `src/rsb/web/dashboard.js:211-212` (`buildGithubUrl` falsy/non-string guard), `:221` (`externalLinkHtml` returns `""` when the URL is `null`); `test/rsb_tests/fixtures.py:190` (`MISSING_OWNER_NAME_PAYLOAD`); `test/rsb_tests/test_model.py:94-107` (asserts `owner_name is None` / `owner_name_by_repo` maps to `None`); this session's `node` run: `buildGithubUrl(null,"issues",5)` → `null`, `buildGithubUrl("","issues",5)` → `null`, `buildGithubUrl(123,"issues",5)` → `null`, `externalLinkHtml(null,"issues",5,"...")` → `""` | Guard clauses cover falsy, empty-string, and non-string `ownerName` inputs uniformly, and the fallback is a plain `""` (issue number/PR number still renders as plain text via the unchanged `${issue}`/`${prNumber}` interpolation in the caller) — never a broken `href="undefined"`/`href="null"`. The live board currently has no repo with a null `owner_name_by_repo` entry (R1), so this path isn't observable live this session, but the guard is unit-tested and directly `node`-verified against the shipped code |
| R6 | "기존 테스트 전부 통과" | Present | This session: `python3 -c "import sys; sys.path.insert(0, 'src'); import pytest; sys.exit(pytest.main(['test/', '-q']))"` → **53 passed, 0 failed, 0 skipped** | Freshly re-run against `main`'s current state (not accepted from `docs/issue-34/reports/implementation.md`'s self-report), exit code 0, count matches the self-report exactly |
| R7 | "주의: PR 본문에 closing 키워드 금지 (issue #23 T2 — 백틱 인용도 파싱됨)" | Present | `gh pr view 35 --json body` (fetched this session, full text read) | No `Closes`/`Fixes`/`Resolves`/`Close`/`Fix`/`Resolve` (plain or backtick-quoted) appears adjacent to `#34` anywhere in PR #35's body text; the only `#34` occurrence is "Phase 1 (research/survey/proposal) for #34." — "for" is not a closing keyword |

## Open findings

Resolution path: the one non-Present finding (R4) hands off to a
follow-up issue for a future implementation role to pick up (this role
does not patch `src/`/`test/` itself, per contract).

Next steps: file a follow-up GitHub issue covering the
external-link/row-toggle click coupling below.

- **External-link click also toggles the detail panel (R4)**

  severity: Low

  `src/rsb/web/dashboard.js`'s whole-row click listener
  (`attachRowClickHandlers`, `:458-465`) fires on any click within a
  table row, including the new `.external-link` anchor (`:219-223`),
  because neither control calls `stopPropagation()`. Activating an
  issue/PR link (mouse or keyboard) therefore also opens or closes that
  row's detail panel as an unintended side effect, alongside its own
  GitHub navigation. Low, not higher, because: both individual actions
  still complete correctly (the link still navigates, the panel still
  toggles), the side effect is instantly reversible (click again to
  re-close), there is no data loss or security implication, and this is
  a natural extension of a pre-existing whole-row-click convention that
  already applied uniformly to every other cell in the row before this
  PR — not a newly-introduced class of bug, but a newly-exposed instance
  of it on the one element type (a real, `target="_blank"` link) where
  the coupling is most visible to a user. No browser was available in
  this sandbox to visually confirm, but the finding rests on
  deterministic DOM event-bubbling semantics (confirmed by the absence
  of any `stopPropagation`/`preventDefault` call in the file), not on an
  assumption requiring live confirmation.

No other findings. R1, R2, R3, R5, R6, R7 all verdict Present.

## Scope notes

- The narrative "새 탭 여부도 결정해 문서화" (decide and document whether
  links open in a new tab) item from issue #34's requirement 4 prose is
  **not** one of the 7 acceptance-criteria checkboxes and was therefore
  not assigned its own Rn by the approved phase-1 proposal (R1-R7 are
  kept strictly 1:1 with the 7 checkboxes, per that proposal's explicit
  framing choice) — not scored here. For the record: the code does open
  links in a new tab (`target="_blank" rel="noopener noreferrer"`,
  `dashboard.js:222`), but this choice is not written down anywhere as a
  documented decision (no `docs/issue-34/decisions/` entry covers it;
  `docs/specs/screen-spec.md` is also silent on `.external-link`) — left
  as-is per this review's scope, not folded into R4.
- `src/rsb/render.py` (CLI text renderer) links and additional GitHub API
  calls remain out of scope, per the issue body's own "범위 밖" section
  and the approved proposal's out-of-scope list.
- Per contract, this record reports verdicts only; no `src/`/`test/`
  change is made by this role. This record is this role's terminal
  phase-2 deliverable for issue #34 per contract v3 §19; next steps are
  the human PR-merge decision on this PR (acceptance) or a requested
  revision on the same branch (feedback).
