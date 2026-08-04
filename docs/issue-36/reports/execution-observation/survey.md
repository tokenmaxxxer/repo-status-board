# Current-state survey — execution-observation (issue #36)

Scope statement: this is the **execution-observation** role, **this
session**, observing **issue #36** ("링크 표기 변경 — ↗ 아이콘 대신 번호를
`#<n>` 파란 링크로, 상세 트리거 재배치"), specifically the single merged PR
that delivered its execution-plan step 1 (`implementation`): **PR #37**
("issue-36 phase 1: link-as-text proposal + row-toggle relocation",
head `issue-36/implementation`, merged 2026-08-03T11:30:30Z, merge commit
`b621082`).

Read this session to arrive at that scope (nothing below is secondhand):

- `gh issue view 36` — title, body (6 requirements, 7 acceptance
  criteria, 2-step execution plan), state OPEN, author `jjongkwann`.
- `gh issue view 36 --json comments` — the issue's only comment.
- `gh pr list --state all --search issue-36` and
  `gh pr list --head issue-36/execution-observation --state all`.
- `gh pr view 37 --json number,title,state,url,author,mergedAt,
  mergeCommit,body,commits,reviews,comments` — full body, both commit
  SHAs, the (empty) reviews array, both PR comments.
- `git show --stat --format=... 403dbd0` and `... 2c462e0` — PR #37's two
  commits, full messages and file/line stats.
- `git show 2c462e0 -- src/rsb/web/dashboard.js` — the full phase-2 diff
  of the file the issue's requirements 1-4 land in.
- `git show origin/main:docs/issue-36/reports/implementation.md` — the
  observed role's own phase-2 record (280 lines).
- `git show origin/main:docs/issue-36/proposals/implementation.md` — the
  approved proposal.
- `git ls-tree -r origin/main --name-only | grep '^docs/issue-36/'`,
  `git log origin/main --oneline -20`, `cat docs/specs/approvers.md`.
- `git show origin/main:docs/issue-29/reports/execution-observation/
  survey.md` and `.../proposals/execution-observation.md` — this same
  role's most recent prior pass, read for artifact-structure precedent
  only, never as evidence about issue #36.

Not read as evidence, deliberately: the working tree's `src/**` files.
`src/` shows what exists on `main` now (including later issues' commits),
not what PR #37 did — this role's admissible evidence is the diff, the
commits, and the observed role's own record.

## 1. What issue #36 asked for

Six numbered requirements (number-as-link; reuse
`color-action-primary-background`, no new token; remove the ↗
`.external-link` anchor; relocate the detail-panel trigger with
`aria-expanded`/`aria-controls` and keyboard operation preserved and an
explicit ban on regressing to whole-row click; plain `#<n>` text when
owner/name is absent; sync `design-system.md`/`screen-spec.md`) and seven
acceptance-criteria checkboxes (blue `#<n>` link navigating to GitHub;
single-line in the Flows table; keyboard-only open/close with no row-click
regression; no broken link when owner/name is missing; all existing tests
pass; spec docs match the implementation; no closing keywords in the PR
body). Execution plan: `step 1 implementation`, then
`step 2 execution-observation ‖ conformance-review`. Both plan checkboxes
are unchecked as of this session's `gh issue view 36`.

## 2. The observed artifact set

PR #37 carries exactly two commits:

| commit | authored | scope | stat |
|---|---|---|---|
| `403dbd0` | 2026-08-03T20:03:51+09:00 | phase 1 — proposal + scout-brief + survey | 3 files, +436 |
| `2c462e0` | 2026-08-03T20:28:51+09:00 | phase 2 — implementation + record | 6 files, +412/−59 |

`2c462e0`'s six files: `docs/issue-36/reports/implementation.md` (+280),
`docs/specs/design-system.md` (1 line), `docs/specs/screen-spec.md` (21
lines), `src/rsb/web/dashboard.css` (36), `src/rsb/web/dashboard.js`
(106), `test/rsb_tests/test_model.py` (+26). Both commit messages carry a
`Subject: issue-36` trailer.

From the `dashboard.js` diff in `2c462e0`, the shipped shape is:
`externalLinkHtml` → `numberLinkHtml(ownerName, kind, number)` returning
`escapeHtml('#'+number)` when `buildGithubUrl` is `null` and an
`<a class="number-link" … >#<n></a>` otherwise; a new
`rowToggleButtonHtml(...)` emitting a `<button class="row-toggle">` with
`aria-expanded`, a literal `aria-controls="detail-panel-slot"`, an
`aria-label="Toggle details for issue <n>"` and an `aria-hidden` `▸`/`▾`
glyph; `issueToggleCell` wrapping button-then-link in
`<span class="issue-cell">`; `rowToggleId` deleted; `renderTable`'s `<tr>`
no longer emitting `data-issue`/`data-repo`; `attachRowClickHandlers`
(bound to `tbody tr[data-issue]`) replaced by `attachRowToggleHandlers`
bound to `.row-toggle` with toggle-to-close via `isRowExpanded`; and the
`module.exports` list swapping `externalLinkHtml` for `numberLinkHtml`.

## 3. Phase-gating trail as observed

- `docs/specs/approvers.md` lists two accounts: `JiwonJung94`,
  `jjongkwann`.
- PR #37's author is `jjongkwann`; `gh pr view 37 --json reviews` returns
  `[]` — no PR review Approve exists on it.
- Issue #36's single comment (`jjongkwann`, 2026-08-03T11:08:44Z) has the
  body `APPROVE issue-36/implementation` — read byte-for-byte this
  session, no surrounding prose.
- A second comment, on PR #37 (`jjongkwann`, 2026-08-03T11:08:45Z, one
  second later), attaches feedback to that approval: it mandates that the
  disclosure rewiring (row-click removal, the button's own handler,
  `sourceTable` preservation, `aria-controls` target) be **operated in an
  actual browser** and the result recorded, citing issue #29 shipping the
  same defect class twice, and lists three minimum checks.
- Ordering as timestamped: phase-1 commit 11:03:51Z → approval comment
  11:08:44Z → phase-2 commit 11:28:51Z → PR summary comment 11:29:18Z →
  merge 11:30:30Z.
- PR #37's title and body still read as phase-1-only ("No code changes
  yet — this commits the current-state survey, scout brief, and build
  proposal"; a "Test plan (phase 2, once approved)" section with four
  unchecked boxes), while its head commit `2c462e0` is the phase-2 build.
  The phase-2 outcome is instead reported in the 11:29:18Z PR comment.

## 4. What the observed record claims

`docs/issue-36/reports/implementation.md` (created in `2c462e0`,
`loop_state: landed`) states: 55 passed / 0 failed for the pytest suite;
`node --check` clean; a `node` scratch-file self-check of
`numberLinkHtml`/`buildGithubUrl`; and — in place of the mandated browser
check — a **jsdom** run against the shipped unmodified file covering the
three feedback items, with raw JSON output inline. It records the browser
attempt that failed (Chrome `crashpad`/`ProcessSingleton` permission
errors in the sandbox, no Playwright/Selenium/Puppeteer) and states
plainly that jsdom is a substitute, not equivalent, and that keyboard
activation specifically was exercised via `.click()` because jsdom does
not translate `keydown` into a button activation. It also records an
adversarial `general-purpose` hunt pass that found and fixed two things
after the approved proposal was written: an unescaped `#${number}` in
`numberLinkHtml`'s link-text branch, and dead `data-issue`/`data-repo`
attributes on `<tr>`. `Open findings: None outstanding`, with the
jsdom-vs-browser gap named as the one honest gap.

## 5. Gaps and unknowns this survey cannot settle

These are the write surfaces where evidence is thin or absent — they aim
this role's scout angles and the phase-2 method.

1. **AC-by-AC evidence is self-attested.** Every acceptance-criterion
   claim currently traces to the record's own prose, not to an
   independently located diff hunk. No cross-check of the seven ACs
   against `2c462e0`'s hunks exists yet.
2. **AC2 (Flows single-line) has no execution evidence of any kind.**
   The record attributes it to `.issue-cell { white-space: nowrap }`;
   jsdom performs no layout, so nothing in the record's run output
   speaks to rendered wrapping.
3. **The browser-check substitution is unadjudicated.** The record
   discloses the gap; whether jsdom closes the *specific* feedback items
   is a judgment, not a fact, and independent evidence now exists on
   `main` — issue #44's PR #45 (commit `b2f6b63`) added
   `test/rsb_tests/test_dashboard_dom.py` whose message states its tests
   were verified to fail against `b621082^`, i.e. against the tree
   immediately before PR #37 merged.
4. **Scope delta vs. the approved proposal is unmeasured.** `2c462e0`
   fixes two bugs issue #36 never asked about (`sourceTable` never
   tracked; `aria-controls` pointing at a nonexistent id) plus two
   post-proposal hunt fixes. The proposal declares the first pair with a
   rationale; the hunt fixes postdate it. Whether the shipped diff stays
   inside what was approved is checkable (`403dbd0`'s proposal text vs.
   `2c462e0`'s hunks) but unchecked.
5. **Requirement 6 / AC6 (doc sync) is unread.** `2c462e0`'s
   `screen-spec.md` (21 lines) and `design-system.md` (1 line) diffs have
   not been read this session, and the `dashboard.js` comment change in
   the same commit asserts `screen-spec.md` §1.6's narrow-layout behavior
   remains unimplemented — leaving open whether a spec section still
   describes behavior that does not exist.
6. **Trajectory facts are collected but unjudged.** Single-account mode
   legitimacy (author == approver, both on `approvers.md`, exact-string
   comment), survey-before-proposal ordering, scout-before-proposal, and
   the phase-1-titled PR carrying phase-2 content are all now on the
   record above as facts; none has been assessed.
7. **AC7 (no closing keywords) is asserted, not verified.** The record's
   `closed_checks` claims it for "this session's PR update"; the PR body
   and both PR comments were read this session but not yet checked
   line-by-line against the backtick-quoted-form precedent issue #23 T2
   established.
