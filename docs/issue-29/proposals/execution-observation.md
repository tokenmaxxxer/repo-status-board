# Verification proposal — execution-observation (issue #29)

Status: phase-1 proposal. Scope: this role only, observing PR #30
(`issue-29/implementation` → `main`, merged `b6302925`) and PR #33
(`issue-29/implementation` → `main`, merged `c94e12d9`). Grounded in
`docs/issue-29/reports/execution-observation/survey.md`'s 7 named gaps
and `scout-brief.md`'s adopt/skip decisions. No code changes. This
document proposes a *method*, not a result: no verdict on whether PR #30
or PR #33 is sound appears anywhere below — that judgment is
phase-2-only, gated on approval, and goes into
`docs/issue-29/reports/execution-observation.md`.

## 0. Which verdict levels will be checked, and against what evidence

Phase 2 will render all three levels required by this role's contract.

1. **Outcome** — did PR #30/#33 land what issue #29 asked, checked
   against: each of issue #29's 7 acceptance-criteria checkboxes, each
   mapped to a specific file:line in `git show 05d632f5 -- <path>` /
   `git show d462b6d0 -- <path>` or to the current `main` file (for
   facts about what state shipped, not what the diff intended) — never
   to `docs/issue-29/reports/implementation.md`'s own prose summary of
   itself. Scoped explicitly to what PR #30/#33 *themselves* delivered
   (survey gap 1): AC6/requirement-5 will get two separate lines — one
   for PR #30/#33's own delivery (which the survey already shows left
   it substantially unmet) and one noting current-`main` state with
   correct attribution to PR #37/issue #36 where that separate PR
   closed part of the gap, without folding that separate role's work
   into this outcome verdict. Survey gap 2 (the banner-collapse item
   implementation.md self-disclosed but no issue comment mentions) gets
   its own AC-row check against current `dashboard.js`'s actual
   `PARTIAL_BANNER.innerHTML`, independent of whether any comment
   flagged it.
2. **Trajectory** — was the implementation role's own phase-1→phase-2
   path sound across *both* PRs, checked against: `git show --stat` on
   all 3 commits (`cc3466a1`, `05d632f5`, `d462b6d0`) confirming which
   touched only `docs/issue-29/` versus `src/`/`test/`; the commit-
   timestamp ordering versus the issue-level approval-comment timestamp
   and the PR #30 feedback-comment timestamp; the crash-recovery
   disclosure in `docs/issue-29/reports/implementation.md` (survey gap
   4) read against what the two issue comments independently say about
   the same crash window, to check whether the specific defects found
   trace back to the inherited uncommitted code rather than to fresh
   phase-2 work; and PR #33's authorization path specifically (survey
   gap 5) — whether proceeding without its own approval comment/review,
   on the strength of the original approval plus the predecessor
   record's self-recommendation, is consistent with contract v3's
   approval-gate text, read plainly rather than assumed compliant by
   analogy to issue-23's T1 finding.
3. **Step** — which specific artifact, if any, is deficient, checked
   against: a real-call-site trace (scout-brief "Adopt" (a)) for every
   export the implementation record claims is wired up
   (`filterByRepo`, `repoList`, `updateRepoFilterOptions`), not just
   confirmation that a test file references it; a real-state-transition
   trace (scout-brief "Adopt" (b)) for `aria-expanded`/`aria-controls`
   on the `.row-toggle` button, tracing `selectedIssue` assignment
   through to what `isRowExpanded()` actually reads, on **current
   `main`** (post issue-36's squash-merge) since that is what a live
   user now sees, with the PR #30/#33-scoped outcome verdict kept
   separate per item 1 above; and independent verification of the two
   already-reported defects' specific citations
   (`dashboard.js:458-465`, `:461`, the missing `module.exports` entry,
   the dangling `aria-controls` id) against the actual file, rather
   than accepting the issue comments' line numbers as already
   self-evidently correct.

## 1. Method (substituting for live execution — see scout-brief "Skip")

This session's role directive prohibits re-running the observed role's
code (`pytest`, `node`, `rsb serve`, a real browser) — consistent with
`docs/issue-29/reports/implementation.md`'s own repeated disclosures
that it, too, had no real browser available and substituted jsdom/curl
checks. Phase 2 will instead:

1. **Real-call-site / real-state-transition tracing, not execution**
   (scout-brief "Adopt"). For each function the implementation record
   claims is wired up, grep every call site in non-test `src/` files
   and read the surrounding code, not just confirm a `module.exports`
   entry or test name exists. For the ARIA pair, trace
   `selectedIssue`'s assignment and every place `isRowExpanded()`/
   `aria-controls` reads from it, on the current file, writing the
   traced path out explicitly rather than citing a line number and
   asserting an outcome.
2. **Independent re-verification of both issue comments' citations.**
   Neither comment's specific file:line claims (`dashboard.js:458-465`,
   `:461`, etc.) will be taken as given; each will be re-read against
   the actual current file this session, and the record will state
   plainly whether each citation checks out, checks out differently
   (e.g. line numbers shifted after issue #36's merge), or does not
   check out.
3. **Backend acceptance criteria (survey gap 3).** Requirement 1
   (parallel fetch + timeout) and requirement 3 (Repo-first columns)
   will get the same diff-tracing treatment as the frontend items —
   `git show 05d632f5 -- src/rsb/fetch.py src/rsb/cli.py` traced by
   hand for the `ThreadPoolExecutor(max_workers=min(...))` construction
   and the `--timeout` flag's threading through `_run_once()`/`serve`,
   and the header-array-vs-cells-array reordering fix for Flows/
   Sessions traced the same way issue-23's precedent traced
   `dashboard.js` branches. The implementation record's own claimed
   "49 passed" test count and its jsdom/curl manual-check narrative
   will be reported as *claimed, not independently reproduced*, per the
   re-execution prohibition — same treatment issue-23's precedent gave
   the "41 passed" claim it inherited.
4. **AC7 (no closing keyword) literal re-check.** Both PR bodies'
   literal raw text (`gh pr view 30/33 --json body`, already pulled)
   will be scanned specifically for `[Cc]lose[sd]?\s+#29`,
   `[Ff]ix(es|ed)?\s+#29`, `[Rr]esolve[sd]?\s+#29` (including inside
   backticks, per issue #23's T2 precedent that a quoted keyword still
   parses) rather than relying on this phase-1 pass's first read.
5. **Trajectory read.** `docs/issue-29/reports/implementation/
   survey.md`, `scout-brief.md`, and `docs/issue-29/proposals/
   implementation.md` (their content, not just their existence — the
   frozen 279-line proposal in particular, to confirm item 6's exact
   original wording against what the "Open findings" sections describe
   as unimplemented) will be read in full before the trajectory verdict
   is written; likewise the crash-recovery and PR #33-authorization
   questions named in survey gaps 4-5.
6. **Independence statement** will open the phase-2 record, before any
   verdict language, per this role's ordering requirement.

## 2. Record format

`docs/issue-29/reports/execution-observation.md` (phase-2 output) will
contain: the independence statement first; the three-level verdict
(outcome/trajectory/step), each verdict-bearing sentence with an
adjacent citation (commit SHA / file:line / PR or issue comment URL); a
per-acceptance-criterion table across all 7 of issue #29's checkboxes;
any deficiency finding in the four-part blameless shape (impact,
timeline, root cause, action item); explicit attribution where a gap
was closed by a different issue/PR rather than by PR #30/#33
themselves; and a `loop_state` field updated at each transition.

## 3. Out of scope

- Any code fix for a discovered defect — hand-off only, per this role's
  prohibition on editing the observed role's `src/`/`test/`.
- Rendering any verdict on issue #36 / PR #37's own trajectory or
  outcome — separate issue, separate role's write surface; this
  proposal only permits *noting* its effect on issue #29's current-
  `main` state where relevant to an issue-29 acceptance criterion.
- Re-judging `conformance-review`'s parallel step-2 work on issue #29 —
  separate role, separate branch/PR, not this role's write surface.
- Running any linter, coverage tool, `pytest`, `node`, or live `rsb
  serve`/browser instance — scout-brief "Skip"; all verification is
  static tracing per §1 above.
