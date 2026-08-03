# Verification proposal — execution-observation (issue #34)

Status: phase-1 proposal. Scope: this role only, observing PR #35
(`issue-34/implementation` → `main`, **merged**, merge commit
`5d05b5f5227c0b8073bed3d16455664bcafd0a5a`, commits
`696cd940cd88493be3d02ce29d7812c7b3b5d6d7` phase 1 and
`027b6f07cddffe4da6fc69a776b9686d1d50956e` phase 2). Grounded in
`docs/issue-34/reports/execution-observation/survey.md`'s gaps and
`scout-brief.md`'s adopt/skip decisions. No code changes this phase. This
document proposes a *method*, not a result: no verdict on whether PR #35
is sound appears anywhere below — that judgment is phase-2-only, gated on
approval, and goes into `docs/issue-34/reports/execution-observation.md`.

## 0. Which verdict levels will be checked, and against what evidence

Phase 2 will render all three levels required by this role's contract:

1. **Outcome** — did PR #35 land what issue #34 asked, checked against:
   the issue's 6 acceptance-criteria checkboxes, each mapped to a specific
   file:line in commit `027b6f0` (`git show 027b6f0 -- <path>`) or to
   `docs/issue-34/decisions/owner-name-wire-format.md`'s wire-format text
   — not to the implementation record's summary of itself. AC6 ("기존
   테스트 전부 통과") will be reported as *claimed* (53 passed, per
   `docs/issue-34/reports/implementation.md`'s "Tests" section), not
   independently reproduced, per this role's re-execution prohibition.
   Issue #36 (opened 2026-08-03T10:53:14Z, 5 minutes after merge) will be
   cited as an outcome-level fact — a real post-deploy defect discovered
   in exactly the area (`/api/board.json` → real-browser rendering) that
   `docs/issue-34/reports/implementation.md`'s own "Open findings" section
   disclosed it could not verify in this sandbox — with an explicit
   statement of whether that counts against PR #35's outcome or is a
   correctly-scoped follow-up, not left ambiguous.
2. **Trajectory** — was the implementation role's own phase-1→phase-2
   path sound, checked against: the commit/comment timestamp ordering
   already pulled in the survey (phase-1 commit 08:33:07 → PR opened
   08:33:54 → issue-level `APPROVE issue-34/implementation` 10:33:42 + PR
   feedback comment 10:33:43 → phase-2 commit 10:46:55, **after**
   approval → phase-2-complete PR comment 10:47:35 → merge 10:48:19),
   `git show --stat` confirming phase 1 touched only `docs/issue-34/`
   (already done in the survey), single-account-mode validity (approver
   `jjongkwann` in `docs/specs/approvers.md`, same account as PR author,
   matching the issue-23 precedent's already-established valid pattern),
   and whether the PR feedback comment's explicit request ("그 판단을
   record 에 한 줄 남길 것") was actually satisfied by
   `docs/issue-34/reports/implementation.md`'s "PR #35 feedback
   resolution" section — a line-by-line comparison of what the comment
   asked for against what the record actually says, not just confirming
   the section exists.
3. **Step** — which specific artifact, if any, is deficient, checked
   against: line-by-line diff tracing of `src/rsb/model.py`'s
   `normalize_payload()`/`merge_repos()` additions and
   `src/rsb/web/dashboard.js`'s `buildGithubUrl`/`externalLinkHtml`/
   `issueToggleCell`/`prCellHtml`/`renderData()` changes (already read in
   full this session per the survey), run by hand against the specific
   cases: owner/name present, owner/name absent (`None`), a
   multi-PR `flows[].prs` array, and — the pass's own added scope per the
   scout-brief's skip decision — whether `dashboard.css`'s
   `.external-link` rule (`display` left as the element's default inline,
   no `white-space`/`overflow` handling) is consistent with the
   implementation record's stated rationale for the PR feedback comment
   (row-to-row column-width stability) or whether that rationale, read
   literally, never addressed within-cell wrap at narrow column widths —
   the exact defect issue #36 reports. This is a **static CSS/HTML
   reading**, not a rendered-browser measurement (out of reach in this
   sandbox, same limitation the implementation record itself disclosed);
   phase 2 will state that boundary explicitly rather than imply a
   rendered-pixel judgment it cannot make.

## 1. Method (substituting for live execution — see scout-brief "Adopt")

This session's role directive prohibits re-running the observed role's
code; per this role's already-settled issue-23/issue-27 precedent, phase
2 will:

1. **Static diff tracing, not execution.** For each case in §0.3, trace
   the actual merged-code path by hand from the relevant
   `git show 027b6f0 -- <path>` hunk, following each case through every
   conditional it hits, and write the traced path out explicitly in the
   phase-2 record — not just cite the line number and assert an outcome.
2. **Test-file reading as corroboration, not proof.** `test/rsb_tests/
   {test_model.py,test_render.py,test_webserver.py}`'s new assertions
   (already read in full this session per the survey) will be re-cited to
   confirm they actually assert the traced behavior — but the claimed
   53/53-pass result is reported as *claimed, not independently
   reproduced*, per the re-execution prohibition.
3. **Acceptance-criteria mapping.** Each of the issue's 6 checkboxes gets
   one row in phase 2: criterion text → the specific diff hunk or
   decision-doc line that addresses it, with AC6 marked claimed-not-
   reproduced as noted above.
4. **Issue #36 handling — this pass's own added method, per the scout-
   brief's skip decision.** Phase 2 will (a) quote the exact sentence in
   `docs/issue-34/reports/implementation.md` that resolves the PR feedback
   comment, (b) quote the exact sentence in issue #36's body describing
   the wrap defect, (c) state plainly whether (a) as written covers,
   contradicts, or simply never addresses (b) — these are two distinct
   CSS/layout phenomena (across-row width stability vs. within-cell
   content wrap) and phase 2 must not conflate them by default — and
   (d) render the resulting judgment as part of the outcome/step verdict,
   not as a silent aside.
5. **Trajectory read.** Already completed this session (see survey's
   "What was independently read"); phase 2 restates it with citations
   rather than re-reading from scratch.
6. **Independence statement** will open the phase-2 record, before any
   verdict language, per this role's ordering requirement.

## 2. Record format

`docs/issue-34/reports/execution-observation.md` (phase-2 output) will
contain: the independence statement first; the three-level verdict
(outcome/trajectory/step), each verdict-bearing sentence with an adjacent
citation (commit SHA / file:line / PR or issue comment URL); a
per-acceptance-criterion table (6 rows); the issue-#36 handling from §1.4
as its own subsection, not folded silently into another section; any
deficiency finding in the four-part blameless shape (impact, timeline,
root cause, action item); and a `loop_state` field updated at each
transition.

## 3. Out of scope

- Any code fix for a discovered defect — hand-off only, per this role's
  prohibition on editing the observed role's `src/`/`test/`. If §1.4
  concludes the implementation record's rationale did not cover the wrap
  case, that becomes a finding in this role's own record, not an edit to
  `dashboard.css`/`dashboard.js`.
- Evaluating issue #36 or PR #37's own content, soundness, or design
  choices — issue #36 is cited only as a fact (what it reports, when it
  was filed) relevant to judging PR #35's outcome/trajectory, never
  reviewed on its own merits; that is out of this role's assigned scope
  (issue #34 only).
- Re-judging `conformance-review`'s parallel step-2 work on issue #34 —
  separate role, separate branch/PR, not this role's write surface.
- Triggering, loading, or rendering the live deployment at
  `https://tokenmaxxxer.github.io/repo-status-board/` — this session has
  no browser and the role directive prohibits re-executing the observed
  role's code regardless; any layout judgment in phase 2 is a static
  CSS/HTML reading, stated as such.
