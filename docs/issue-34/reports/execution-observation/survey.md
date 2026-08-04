# Current-state survey — execution-observation (issue #34)

Scope statement: this is the execution-observation role, current session,
observing issue #34 ("이슈·PR 번호에서 GitHub 으로 바로 이동 — owner/name
관통 + 링크"), specifically PR #35 ("issue-34 phase 1: owner/name
propagation + GitHub link proposal", merged). Read this session to arrive
at this scope: `gh issue view 34` (body + comments),
`gh issue view 34 --json comments,createdAt,state`,
`gh pr view 35 --json commits,mergeCommit,headRefName,baseRefName,url,mergedAt,reviews,comments,body,createdAt`,
`gh pr diff 35 --patch` (full diff, both commits, every hunk),
`git show --stat` on both of PR #35's commits, `git log --oneline -15`,
`git branch -a`, `gh pr list --state all --search issue-34`,
`gh issue view 36` (body + comments, the post-deploy follow-up issue named
in this session's invocation), `docs/specs/approvers.md`, and — as
in-repo comparators for this role's own record shape —
`docs/issue-23/reports/execution-observation/{survey.md,scout-brief.md}`,
`docs/issue-23/proposals/execution-observation.md`,
`docs/issue-27/reports/execution-observation/scout-brief.md` and
`docs/issue-27/proposals/execution-observation.md` (via
`git show origin/issue-27/execution-observation:<path>`, that branch's
docs never having reached `main`).

## What exists already

- **Issue #34: OPEN** (`createdAt: 2026-08-03T08:18:44Z`). Body specifies
  the owner/name-propagation requirement, 6 acceptance-criteria
  checkboxes, and a "## 실행 계획" block naming step 1 (implementation,
  done) and step 2 (`execution-observation ‖ conformance-review`, this
  role's own step, not yet closed out — consistent with the issue still
  being open). One issue-level comment:
  `APPROVE issue-34/implementation` (jjongkwann, `2026-08-03T10:33:42Z`,
  `issuecomment-5165247317`) — approves the **implementation** role only.
  **No `APPROVE issue-34/execution-observation` comment exists on the
  issue**, and this role's own `docs/issue-34/` tree
  (`reports/execution-observation/`, `proposals/execution-observation.md`)
  did not exist before this session — this is this role's first phase-1
  pass for issue #34.
- **PR #35**: `issue-34/implementation` → `main`, **MERGED**
  (`createdAt: 2026-08-03T08:33:54Z`, `mergedAt: 2026-08-03T10:48:19Z`,
  merge commit `5d05b5f5227c0b8073bed3d16455664bcafd0a5a`, `reviews: []` —
  no formal GitHub PR review anywhere in this PR's history). Two commits:
  - `696cd940cd88493be3d02ce29d7812c7b3b5d6d7` (08:33:07Z) — phase 1:
    3 files, all under `docs/issue-34/` (`proposals/implementation.md`,
    `reports/implementation/{survey.md,scout-brief.md}`), 351 insertions,
    0 deletions, confirmed via `git show --stat` — no `src/`/`test/`
    touched in this commit.
  - `027b6f07cddffe4da6fc69a776b9686d1d50956e` (10:46:55Z) — phase 2:
    10 files (`src/rsb/model.py` +4, `src/rsb/render.py` +1,
    `src/rsb/web/dashboard.js` +54/-17, `src/rsb/web/dashboard.css` +17,
    `test/rsb_tests/{fixtures.py,test_model.py,test_render.py,test_webserver.py}`
    +35, plus the new decision doc and the role's own
    `reports/implementation.md`), 367 insertions / 17 deletions.
  - Two PR-level comments, both jjongkwann: (a) `issuecomment-5165247526`
    (`10:33:43Z`, one second after the issue-level APPROVE comment) — a
    "승인 별첨 피드백" (approval-attached feedback) flagging that
    `externalLinkHtml` returning `""` when owner/name is absent means some
    rows in a table carry the ↗ affordance and others don't, asking that
    manual verification judge whether this reads as misaligned and that
    the judgment be recorded in one line; (b) `issuecomment-5165370070`
    (`10:47:35Z`) — the implementation role's own phase-2-complete
    announcement, citing commit `027b6f0`, 53 passed tests, and its
    resolution of feedback (a): "leave it as `""`, no width-reserving
    empty `<span>`" with a stated rationale (CSS `.external-link` is
    inline content inside the existing `<td>`, not its own column, so a
    missing ↗ never shifts any other column's boundary).
  - Commit-and-comment ordering confirmed strictly monotonic and contract-
    compliant: phase-1 commit (08:33:07) → PR opened (08:33:54) →
    issue-level APPROVE (10:33:42) + PR feedback comment (10:33:43,
    1s later, same author) → phase-2 commit (10:46:55, **after** approval)
    → phase-2-complete PR comment (10:47:35) → merge (10:48:19). Approver
    account `jjongkwann` is listed in `docs/specs/approvers.md` (alongside
    `JiwonJung94`); PR #35's author is also `jjongkwann` — single-account
    mode, matching the pattern `docs/issue-23/reports/implementation.md`
    and this role's issue-23 precedent already established as valid for
    this repo.
  - PR body (`gh pr view 35 --json body`, read in full): states "Phase 1
    ... This PR stops at the proposal — no implementation code yet. Phase
    2 opens on an approver's Approve" and contains no closing keyword
    (`Closes`/`Fixes`/`Resolves #34`) in any form, including backtick
    quotes — matches issue #34's own "PR 본문에 closing 키워드 금지"
    constraint and the implementation record's `pr-body-no-closing-keywords`
    self-check claim.
- `docs/issue-34/reports/implementation.md` (the observed role's own
  phase-2 record, read in full this session): `loop_state: landed`, states
  its approval basis, breaks the work into "Unit A — Python wire-through"
  and "Unit B — JS link rendering", documents the feedback-comment
  resolution (see above) with an explicit rationale, claims
  `python -m pytest test/` → 53 passed / 0 failed / 0 skipped (33
  pre-existing + 20 new) and a `node -e` self-check + `node --check` for
  the JS side, an explicit **"What did not work"** section (this
  session's sandbox blocked all `$TMPDIR` writes, so no live `rsb serve` +
  browser smoke check happened), an **"Open findings"** section stating
  plainly that the `/api/board.json` → browser rendering path — including
  "keyboard tab order between `row-toggle` and `external-link`" — is
  verified only at the unit/pure-function level, not via "an actual
  running server or a real browser", and recommends "a follow-up manual
  check ... before or shortly after this PR merges", and a
  **"Self-check"** section with 5 named `closed_checks` (python-contract-
  match, js-contract-match, row-toggle-not-overlapped, css-class-matches-
  js, full-test-suite, pr-body-no-closing-keywords).
- `docs/issue-34/proposals/implementation.md` and
  `docs/issue-34/reports/implementation/{survey.md,scout-brief.md}` (read
  in full this session, not just confirmed to exist): the proposal's
  "Rationale" section explicitly records two rejected alternatives (per-
  record `owner_name` field instead of a lookup map; wrapping/overlaying
  the `row-toggle` button instead of a sibling anchor) with reasons; the
  scout-brief documents a 3-angle parallel sweep (Adrian Roselli's
  expando-table pattern, GitLab's row-identifier-adjacent-link
  convention, W3C APG button pattern) converging on "separate sibling
  control" as the must-be, one stage, saturation reached.
- `docs/issue-34/decisions/owner-name-wire-format.md` (read in full):
  documents the additive `board.json` top-level key
  `owner_name_by_repo: dict[str, str | None]`, non-breaking, no
  `schema_version` bump — matches what the diff actually does (see next
  section).
- **Issue #36** (`createdAt: 2026-08-03T10:53:14Z`, **5 minutes after PR
  #35 merged**, state **OPEN**): user-authored (this session never files
  issues), titled "링크 표기 변경 — ↗ 아이콘 대신 번호를 #<n> 파란 링크로,
  상세 트리거 재배치". Body explicitly frames itself as a *post-deploy*
  finding against PR #35's shipped behavior, citing two concrete problems
  observed at `https://tokenmaxxxer.github.io/repo-status-board/`: (1) the
  ↗ icon doesn't visually read as a link target; (2) "Flows 표의 Issue 열이
  좁아 ↗ 가 번호 아래 줄로 떨어진다" (실측) — the ↗ wraps to a second line in
  the Flows table's narrower Issue column, while Decision queue's wider
  column keeps it inline. Issue #36 already has its own single-account
  `APPROVE issue-36/implementation` comment (`11:08:44Z`) and an open PR
  #37 (`issue-36/implementation`, not this role's scope to evaluate).
  Issue #36's body treats this as new scope (a design change: numeric
  `#<n>` links replacing the ↗ icon, plus relocating the disclosure
  trigger), not as a bug report against issue #34's stated acceptance
  criteria — none of which mention line-wrapping or icon legibility.

## What was independently read and diffed this session (not taken on the implementation record's word)

- `src/rsb/model.py` diff (`BoardModel.owner_name_by_repo` field,
  `normalize_payload()`'s new `"owner_name": payload.get("repo")` line,
  `merge_repos()`'s new `model.owner_name_by_repo[repo_name] = ...` line)
  — read hunk-by-hunk against the proposal's "Python (와이어 관통)" spec.
- `src/rsb/render.py` diff (`render_json_model()` gains
  `"owner_name_by_repo": model.owner_name_by_repo`) — one line, matches.
- `src/rsb/web/dashboard.js` full diff: `buildGithubUrl(ownerName, kind,
  number)` (falsy/non-string → `null`), `externalLinkHtml(ownerName, kind,
  number, label)` (`null` URL → `""`, otherwise an `escapeHtml()`-safe
  `<a class="external-link" target="_blank" rel="noopener noreferrer">`
  with `aria-label` and an `aria-hidden="true"` `↗` `<span>`),
  `issueToggleCell`'s new 4th `ownerName` param appending the link as a
  trailing sibling after the unmodified `<button class="row-toggle">`
  (never wrapping/nesting it), new `prCellHtml(ownerName, prNumbers)`
  replacing the plain-text PR `<td>`s in `decisionRows` (wraps `d.pr` as
  `[d.pr]`) and `flowRows` (`f.prs`, already an array), all four row-
  builder functions gaining an `ownerNameByRepo` parameter and doing a
  per-record `ownerNameByRepo[record.repo]` lookup (not a single whole-
  table value), `renderData()` extracting `data.owner_name_by_repo || {}`
  once, and the `module.exports` addition of `buildGithubUrl`/
  `externalLinkHtml`.
- `src/rsb/web/dashboard.css` diff: `.external-link` (`margin-left:
  var(--space-1)`, `color: var(--color-text-secondary)`, hover/focus
  `var(--color-action-primary-background)`, `:focus-visible` outline) —
  only pre-existing custom-property tokens referenced, no new tokens
  declared in this diff.
- `test/rsb_tests/fixtures.py`, `test_model.py`, `test_render.py`,
  `test_webserver.py` diffs: read every new fixture
  (`MISSING_OWNER_NAME_PAYLOAD`, derived from `EMPTY_PAYLOAD` with the
  `repo` key removed) and every new assertion (owner-name-present,
  owner-name-absent-is-`None`, `merge_repos` fills the dict correctly for
  both a present and an absent case, `render_json_model` output includes
  the key, one `/api/board.json` spot-check) — not just the test names.
- Prior, directly comparable in-repo precedent for this role's own record
  shape: `docs/issue-23/reports/execution-observation/{survey.md,
  scout-brief.md}`, `docs/issue-23/proposals/execution-observation.md`,
  and (via `git show origin/issue-27/execution-observation:<path>`)
  `docs/issue-27/reports/execution-observation/scout-brief.md` and
  `docs/issue-27/proposals/execution-observation.md` — all read in full
  this session to calibrate record structure/rigor and to check what
  verification method and scout mode those passes actually used.

## Gaps / unknowns this proposal must resolve

1. **Method under the re-execution prohibition** — already settled by the
   issue-23/issue-27 precedent (static diff/config tracing, test results
   reported as *claimed*, not independently reproduced); this pass
   restates it rather than re-deriving it from scratch.
2. **How to treat issue #36 in the three-level verdict — genuinely new,
   not covered by either precedent.** Issue-23's PR was already merged
   with no post-merge follow-up issue; issue-27's PR was pre-merge with
   live-runner-only ACs, also no post-merge split. Here PR #35 disclosed,
   in its own "Open findings", that live-browser rendering (including
   layout) was unverified in this sandbox and recommended a follow-up
   manual check "before or shortly after this PR merges" — and 5 minutes
   after merge, a real-browser check surfaced exactly a layout problem
   (↗ wrapping in the Flows table) that this role's implementation-record
   read could not have caught by diff-tracing alone (CSS/HTML wrapping
   under real column widths is not something a static diff shows). The
   proposal must state explicitly whether this is (a) evidence that the
   implementation role's own disclosed gap materialized as predicted and
   was correctly handled by opening a new issue rather than hiding it, or
   (b) a step-level deficiency in PR #35 itself — and against what
   evidence that distinction will be drawn.
3. **The feedback-comment (별첨 피드백) resolution's own soundness** — the
   implementation record's stated reasoning ("`.external-link` is inline
   content inside the existing `<td>`, not its own column, so a missing ↗
   never shifts any other column's boundary") is about *within-column,
   across-row* width consistency (some rows have owner/name, some don't),
   which is a different phenomenon from issue #36's *within-cell content
   wrap* finding (the icon itself wrapping to a second line when the
   column is narrow, independent of whether every row has one). Phase 2
   must trace whether these two are actually consistent (both true
   simultaneously) or whether the implementation's answer to the PR
   feedback comment overlooked the wrap case now reported in issue #36.
4. **Six acceptance criteria** need explicit per-criterion evidence
   pointers to the diff/decision-doc in phase 2, not a global "looks
   done" — AC6 ("기존 테스트 전부 통과") in particular can only be reported
   as *claimed* (53 passed), consistent with this role's re-execution
   prohibition, not independently reproduced.
5. **Trajectory-level evidence** (commit/comment/approval ordering) is
   already fully pulled above from raw `gh`/`git` output, but phase 2
   must restate it with citations rather than re-deriving it, and must
   explicitly address whether the PR feedback comment's request ("그
   판단을 record 에 한 줄 남길 것") was actually satisfied by the
   implementation record — it was (see "PR #35 feedback resolution"
   section, cited above) — as part of the trajectory verdict.
