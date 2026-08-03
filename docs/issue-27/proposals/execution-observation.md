# Verification proposal — execution-observation (issue #27)

Status: phase-1 proposal. Scope: this role only, observing PR #28
(`issue-27/implementation` → `main`, **open, unmerged**, commits
`f51fc76050110119fc40e8c7d70bad6409cfb3ff` phase 1 and
`c02eee3fe6103764a9fd6bcd5543bc41d503241e` phase 2). Grounded in
`docs/issue-27/reports/execution-observation/survey.md`'s gaps and
`scout-brief.md`'s adopt/skip decisions. No code changes this phase. This
document proposes a *method*, not a result: no verdict on whether PR #28
is sound appears anywhere below — that judgment is phase-2-only, gated on
approval, and goes into `docs/issue-27/reports/execution-observation.md`.

## 0. Which verdict levels will be checked, and against what evidence

Phase 2 will render all three levels required by this role's contract:

1. **Outcome** — did PR #28 land what issue #27 asked, checked against:
   the issue's 6 acceptance-criteria checkboxes, each mapped either to a
   specific file/line or config block in the diff (`git show
   c02eee3 -- <path>`) for the 3 criteria checkable from static artifacts
   (dashboard fetch-path fix, empty sessions/ledger empty-state handling
   reused unchanged, PR-body closing-keyword check), or explicitly marked
   "not yet verifiable — requires a live workflow run against an enabled
   Pages environment" for the 3 that are structurally live-runner-only
   (merged 3-repo Pages render, cron-tick `generated_at` advance,
   fail-safety-on-broken-config demonstration). The PR comment #2
   (`fetch.py` timeout/truncation finding, 2026-08-03T05:45:57Z, split to
   issue #29) will be cited as an outcome-level merge-readiness caveat —
   not folded into a step finding, since the commenter states plainly it
   is not this PR's defect.
2. **Trajectory** — was the implementation role's own phase-1→phase-2
   path sound, checked against: the commit-timestamp ordering already
   pulled in the survey (phase-1 commit → PR opened → issue-level
   approval comment → PR feedback comment #1 → phase-2 commit, all in
   that order), whether the phase-2 commit actually incorporated PR
   comment #1's feedback (already spot-checked in the survey via the
   `docs/handbooks/rsb.md` diff — will be restated with citation in
   phase 2, not re-derived), and the full content (not just existence) of
   `docs/issue-27/reports/implementation/survey.md`, `scout-brief.md`,
   and `docs/issue-27/proposals/implementation.md` — already read in full
   this session, per the survey's "What was independently read" section.
3. **Step** — which specific artifact, if any, is deficient, checked
   against: line-by-line comparison of `.github/workflows/deploy-board.yml`
   and `.github/boards.ci.toml`'s actual content (already read in full
   this session) against the proposal's own "What will be done" §1-2 text,
   the one-line `dashboard.js:406` diff against requirement 2's stated
   fix, and a fresh grep of `dashboard.js`/`index.html`/`dashboard.css`
   for any other absolute-path `fetch`/`href`/`src` the implementation
   record's self-hunt might have missed.

## 1. Method (substituting for live execution — see scout-brief "Adopt")

This session's role directive prohibits re-running the observed role's
code; per `docs/issue-23/reports/execution-observation.md`'s
already-settled precedent, phase 2 will:

1. **Static diff/config tracing, not execution.** For the workflow YAML,
   the TOML config, and the `dashboard.js` fetch-path fix, trace the
   actual merged-branch file content (`git show
   origin/issue-27/implementation:<path>`) against the proposal's "What
   will be done" text and the issue's requirements, hunk by hunk — not
   just cite that the file exists.
2. **Test-file/claim reading as corroboration, not proof.** The
   implementation record's claimed 41/41 `pytest` pass and YAML/TOML
   syntax-validation will be reported in phase 2 as *claimed, not
   independently reproduced* — this pass will not invoke `pytest`,
   `yaml.safe_load`, or `tomllib.load` itself.
3. **Acceptance-criteria mapping with explicit not-yet-verifiable
   marking.** Each of the issue's 6 checkboxes gets one row in phase 2:
   criterion text → either a specific diff/config citation (for the 3
   checkable now) or an explicit "not yet verifiable pre-merge/pre-live-run"
   note (for the 3 live-runner-only ones) — never a silent pass.
4. **PR comment #2 handling.** The `fetch.py` timeout finding will be
   cited by its PR comment URL/timestamp and treated as outcome-level
   deployment-readiness context (the sequencing constraint: issue #29
   should land before PR #28's first live run), explicitly not as a step
   deficiency in PR #28's own diff, per the commenter's own framing.
5. **Trajectory read.** Already completed this session (see survey's
   "What was independently read"); phase 2 restates it with citations
   rather than re-reading from scratch.
6. **Independence statement** will open the phase-2 record, before any
   verdict language, per this role's ordering requirement.

## 2. Record format

`docs/issue-27/reports/execution-observation.md` (phase-2 output) will
contain: the independence statement first; the three-level verdict
(outcome/trajectory/step), each verdict-bearing sentence with an adjacent
citation (commit SHA / file:line / PR comment URL); a per-acceptance-
criterion table (6 rows, each marked checkable-now-and-passed,
checkable-now-and-failed, or not-yet-verifiable-pre-live-run); any
deficiency finding in the four-part blameless shape (impact, timeline,
root cause, action item); and a `loop_state` field updated at each
transition.

## 3. Out of scope

- Any code fix for a discovered defect — hand-off only, per this role's
  prohibition on editing the observed role's `src/`/`test/`.
- Re-judging `conformance-review`'s parallel step-2 work — separate role,
  no branch exists yet for it this session, not this role's write
  surface.
- Independently verifying issue #29 / PR #30's own soundness — out of
  this role's assigned scope (issue #27 only); phase 2 will cite issue
  #29's open/unmerged state as a fact, not evaluate its content.
- Triggering or simulating a live GitHub Actions run, enabling Pages, or
  any other action against the real GitHub Actions/Pages environment —
  this session has no such access and the role directive prohibits
  re-executing the observed role's code regardless.
