# issue-56 execution-observation — current-state survey

No verdict is rendered anywhere in this file. It records what was read
first-hand this session, what the artifacts state, and which questions
are left open for the phase-2 record. Statements below are observations
of artifact content, not judgments of it.

## 0. Observation scope (who / what / which session / which PR)

- **Observed role**: `implementation`, issue #56, branch
  `issue-56/implementation`.
- **Observed session**: the two-phase session that produced PR #57
  (<https://github.com/tokenmaxxxer/repo-status-board/pull/57>), title
  "issue-56: renderErrors 제거 + .number-link 24px 최소 크기 (phase 1+2)",
  author `jjongkwann`, MERGED 2026-08-08T02:39:24Z, merge commit
  `93a60b3`.
- **Observed commits**: `71a0dff` (phase 1, 2026-08-04T10:11:51Z, 3 files
  / +402) and `21c2359` (phase 2, 2026-08-08T02:36:12Z, 6 files / +261
  −20).
- **Observed record**: `docs/issue-56/reports/implementation.md`
  (209 lines, added whole by `21c2359`).
- **Observing role**: `execution-observation`, issue #56, branch
  `issue-56/execution-observation`. Its parallel sibling in issue #56's
  실행 계획 step 2 (`conformance-review`) has no PR on
  `gh pr list --state all` as of this session — nothing of that role's
  is on the board, and nothing here depends on it.
- **Out of observation**: PR #43 / issue #38 (the upstream that produced
  findings F1·F3) is read only as the yardstick issue #56's requirements
  were written from, never re-observed.

## 1. What was read first-hand this session

Every item below was opened this session; nothing here is secondhand.

1. Issue #56 body and its single comment, via `gh issue view 56` and
   `gh api repos/tokenmaxxxer/repo-status-board/issues/56/comments`
   (comment id 5177783505, exact body, author, timestamp).
2. PR #57 metadata: `gh pr view 57` (title, body, state, +663/−20) and
   `gh pr view 57 --json commits,mergedAt,mergeCommit,author,headRefOid,reviews,comments`.
3. Both commits' full messages and `--stat`: `git show --stat 71a0dff`,
   `git show --stat 21c2359`.
4. The phase-2 diff itself for the five non-record files:
   `git show 21c2359 -- src/rsb/web/dashboard.js src/rsb/web/dashboard.css
   docs/specs/screen-spec.md docs/specs/design-system.md
   test/rsb_tests/test_dashboard_dom.py`.
5. `docs/issue-56/reports/implementation.md` — all 209 lines.
6. `docs/issue-56/proposals/implementation.md` — all 143 lines.
7. `docs/issue-56/reports/implementation/survey.md` and
   `.../scout-brief.md` — section headings, the scout brief's mode/stage
   statement (`:4-8`) and its `Sources:` list (`:74-79`).
8. `docs/issue-38/reports/execution-observation.md` — the AC4 and AC5
   table rows (`:139`, `:140`) and the four finding headings (`:247`,
   `:290`, `:320`, `:354`), i.e. the upstream text issue #56 was cut
   from.
9. `docs/specs/approvers.md` (two accounts: `JiwonJung94`,
   `jjongkwann`).
10. The merged tree at `93a60b3` via `git grep`/`git show` for
    `ErrorListItem`, `error-list`, `renderErrors`, `§1.9`, and
    `index.html`'s `#main-content` / `#partial-banner` elements — read as
    the state PR #57 produced, cross-checked against what `21c2359`'s
    diff did and did not touch.
11. `docs/issue-44/proposals/execution-observation.md` — the house shape
    a prior instance of this role used, read as a format precedent only.

Not read as evidence, deliberately: `src/rsb/web/dashboard.js` and
`dashboard.css` at working-tree HEAD. Where markup or CSS shape is
needed, it is taken from `21c2359`'s diff or from the tree at `93a60b3`
with the SHA cited.

## 2. Delivery timeline reconstructed from artifacts

| when (UTC) | what | source |
| --- | --- | --- |
| 2026-08-04T10:02:20Z | issue #56 opened by `jjongkwann` | `gh issue view 56 --json createdAt` |
| 2026-08-04T10:11:51Z | `71a0dff` — phase 1: proposal + survey + scout brief only (3 files, docs-only) | `git show --stat 71a0dff` |
| 2026-08-04T10:12:22Z | PR #57 opened | `gh pr view 57 --json createdAt` |
| 2026-08-04T10:29:48Z | issue comment 5177783505, body exactly `APPROVE issue-56/implementation`, author `jjongkwann` | `gh api .../issues/56/comments` |
| 2026-08-08T02:15:00Z → 02:31:32Z | before-landing warrant hunt window as self-recorded | `docs/issue-56/reports/implementation.md:172-173` |
| 2026-08-08T02:36:12Z | `21c2359` — phase 2: code + CSS + 2 specs + test + record | `git show --stat 21c2359` |
| 2026-08-08T02:39:24Z | PR #57 merged as `93a60b3` | `gh pr view 57 --json mergedAt,mergeCommit` |

`gh pr view 57 --json reviews` returns `[]` — no PR-review Approve
exists; the approval path taken was the issue-level comment above.
PR #57's author and that comment's author are the same account.

## 3. What landed, by file (`git show 21c2359`)

| file | change as it appears in the diff |
| --- | --- |
| `src/rsb/web/dashboard.js` | −13: `renderErrors()` definition deleted; `${renderErrors(data.errors)}` call site inside `renderData` deleted. No other hunk. |
| `src/rsb/web/dashboard.css` | +9 inside the existing `.number-link` block: a 4-line comment plus `min-width: 24px; min-height: 24px; display: inline-flex; align-items: center; justify-content: center`. No other hunk. |
| `docs/specs/screen-spec.md` | −5 (§1.9 "Errors panel — `ErrorListItem`" deleted), +5 (§2.5 gains a sole-surface sentence naming the removal). |
| `docs/specs/design-system.md` | +3 in §5 prose (a sentence appended after the existing "…not a redesign."), and the §6 `DataTable` row gains "24×24px minimum size per issue #56 F3". |
| `test/rsb_tests/test_dashboard_dom.py` | +33: one new test `test_partial_failure_raw_message_absent_from_main_content_and_errors_section_gone` plus a comment block tracing it to issue-38 F1's root cause. |
| `docs/issue-56/reports/implementation.md` | +209, new file — the phase-2 record. |

## 4. Check surfaces this observation must reach, and what is known now

Each row is a surface the phase-2 record will have to resolve; the
right-hand column states only what the artifacts already show, with no
conclusion attached.

1. **AC "renderErrors 제거(grep 0건)"** — `git grep -n renderErrors
   93a60b3 -- src test` returns one hit,
   `test/rsb_tests/test_dashboard_dom.py:252`, inside the new test's own
   explanatory comment. The record anticipates exactly this
   (`implementation.md:155-157`, "0 functional hits… expected"). Open
   question: how the AC's literal "grep 0건" reads against a comment-only
   hit that the record disclosed in advance.
2. **AC ".number-link 24×24px (.row-toggle 패턴)"** — the CSS diff adds
   the four `.row-toggle` properties verbatim. Open question: whether the
   record's substitute for pixel measurement (jsdom `getComputedStyle`,
   `implementation.md:32-39`, `:90-97`) is the substitution the approved
   proposal pre-authorized (`proposals/implementation.md:30-36`,
   `:80-83`) or an unannounced one.
3. **AC "screen-spec §1.9 삭제 + §2.5 유일 표시 지점 명시"** — both edits
   are in the diff. `git grep -n "§1.9" 93a60b3 -- docs/specs` returns
   nothing, so no dangling section pointer remains in the specs.
4. **AC "design-system 24px 목록 편입"** — two facts sit side by side.
   The §6 `DataTable` row now names the 24×24px minimum for
   `.number-link` (`93a60b3:docs/specs/design-system.md:184`). The §5
   prose sentence that enumerates the guaranteed controls still reads
   "every interactive control (`row-toggle`, `repo-filter`,
   `refresh-button`)" with `.number-link` added by a following sentence
   rather than into that parenthetical
   (`93a60b3:docs/specs/design-system.md:163-170`). Open question:
   whether "목록 편입" is satisfied by the appended sentence.
5. **Residue of the deleted component** — `21c2359` did not touch
   `docs/specs/design-system.md`'s §6 row `| ErrorListItem |
   status-error |` (`93a60b3:docs/specs/design-system.md:189`), whose
   §6 preamble states components are "applied per-region in
   `docs/specs/screen-spec.md`" (`:174`) — and §1.9 was the region that
   applied it. Likewise `21c2359` did not touch
   `93a60b3:src/rsb/web/dashboard.css:347-349`, where the comment
   `/* HygieneListItem / ErrorListItem */` and the `.error-list`
   selectors remain (shared with `.hygiene-list`, which is still
   rendered). The record's grep verification covered
   `grep -n "ErrorListItem" docs/specs/screen-spec.md` only
   (`implementation.md:158-159`, `:190-191`). Open question: whether
   issue #56's ACs reach these, and if not, whether the residue is
   nonetheless a step-level observation.
6. **AC "partial-failure 문서-범위 단언 테스트"** — the committed test
   asserts `mainContent.textContent.includes(marker) === false` and
   `document.getElementById("partial-banner").innerHTML.includes(marker)
   === true` in the same run (`21c2359:test/rsb_tests/test_dashboard_dom.py`
   hunk). At `93a60b3:src/rsb/web/index.html:20,24`, `#partial-banner`
   is a sibling *outside* `<main id="main-content">`, so the first
   assertion's scope structurally excludes the banner. Two of the four
   assertions (`document.querySelectorAll("h2")`,
   `document.querySelector(".error-list")`) are scoped to `document`.
   Open question: how "문서-범위" in the AC reads against a mixed
   `#main-content`-subtree / `document` scoping, and whether the record's
   own wording (`implementation.md:49-54`, "document-scoped to
   `#main-content` itself") describes it accurately.
7. **Test-suite claim** — the record states 64 passed / 2 failed with the
   two failures attributed to `f353910`'s unguarded
   `window.matchMedia` (`implementation.md:136-149`). This role does not
   run the suite; the open question is only whether the claim is
   internally consistent with the artifacts and disclosed, and whether
   any independent attestation exists (`ls .github/workflows/` is a
   phase-2 read, not yet done).
8. **Approval path** — comment 5177783505's body, author, timestamp, and
   PR #57's empty `reviews` array are all in §2. Open question: which of
   contract v3 s19's two paths this satisfies and whether the string
   equality holds exactly.
9. **Phase ordering** — `71a0dff` staged docs only; `21c2359` staged code
   and record; the approval sits between them (§2). Open question: none
   of the ordering facts are in doubt; what phase 2 must state is what
   they add up to.
10. **Commit hygiene** — both commit messages carry a `Subject: issue-56`
    trailer (`git show --stat 71a0dff`, `21c2359`). PR #57's body ends
    "References #56." and its title carries no closing keyword; the title
    reads "(phase 1+2)", which is the shape issue-38's F4
    (`docs/issue-38/reports/execution-observation.md:354`) flagged as
    wrong on PR #43. Open question: whether any closing keyword appears
    anywhere in PR #57's body (full body read this session; to be quoted
    in the record).
11. **The observed role's own phase-1 obligations** — `71a0dff` contains
    a survey (180 lines), a scout brief (79 lines, stating "3 parallel
    `WebSearch` calls, one turn… 2 stages total, ~35s wall-clock",
    `scout-brief.md:4-8`, with 5 sources at `:74-79`), and a proposal
    (143 lines). Open question: whether the proposal's plan and the
    delivered phase 2 correspond item-for-item, and whether the record's
    single declared deviation (`implementation.md:106-124`, the
    `PYTHONPATH=` env-prefix refusal) is the only one.
12. **Warrant-hunt record placement** — the hunt is recorded inside
    `docs/issue-56/reports/implementation.md:163-195` rather than at
    `docs/reports/<date>-hunt-<slug>.md`; the repository has no
    `docs/reports/` standing bucket (`ls docs/` — only `handbooks`,
    `specs`, and per-issue trees exist). Only one hunt section
    (`before-landing`) appears. Open question: whether an
    `after-proposal` hunt was owed given `71a0dff` was docs-only, and
    what the absence of a second section means for the record's
    completeness.

## 5. Gaps this survey hands to scout

Scout's angles are aimed at these four, in this order — they are the
surfaces above where the artifacts alone do not tell this role what the
bar is:

- **G1 (row 6)** — what strong review practice says about *assertion
  scope* in a regression test written to close a previously-missed
  surface: is subtree-scoping with a companion document-scoped assertion
  the accepted shape, or is whole-document the bar?
- **G2 (rows 4, 5)** — how design-system / component-inventory documents
  are expected to be kept consistent when a component's only applying
  region is deleted: is orphan-entry cleanup part of the same change or
  a separate hygiene task?
- **G3 (row 2, 7)** — how audits treat a **substituted verification**
  (measurement replaced by a structural/computed-value check because the
  environment lacks the instrument) that was pre-declared in the
  approved plan: what makes such a substitution acceptable versus a
  reported gap.
- **G4 (rows 1, 10, 12)** — what a review of a *self-approved,
  single-account* two-phase change is expected to check that a
  two-reviewer change would not, and which literal-criterion mismatches
  (a grep hit that is a comment) reviewers of this class treat as
  satisfied-with-note versus unmet.

## 6. Warrant-hunt skip record (this role's own phase 1)

`proposal: docs/issue-56/proposals/execution-observation.md` —
**after-proposal dispatch not run, and it is recorded here rather than
left silent.** Two reasons, both binding: this phase-1 write set is
docs-only (three files, all under `docs/issue-56/`), and this is a
headless single-shot session, where contract v3 s22 forbids ending the
turn with a dispatched agent whose result has not been consumed and
explicitly permits not dispatching rather than dispatching-and-abandoning.
The before-landing dispatch is skipped under the same docs-only fast
path. No hunt findings exist for this phase because no hunt ran.
</content>
