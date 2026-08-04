# Verification proposal — execution-observation (issue #36)

Status: phase-1 proposal. Scope: this role only, observing **PR #37**
(`issue-36/implementation` → `main`, merged 2026-08-03T11:30:30Z, merge
commit `b621082`, commits `403dbd0` and `2c462e0`) — the merged
execution-plan step 1 of issue #36. Grounded in
`docs/issue-36/reports/execution-observation/survey.md`'s seven named
gaps and `scout-brief.md`'s adopt/skip decisions.

This document proposes a **method, not a result**. No judgment about
whether PR #37 is sound appears anywhere below — not stated, not
implied, not provisional. That judgment is phase-2-only, gated on an
approval per contract v3 §19, and goes into
`docs/issue-36/reports/execution-observation.md`. Nothing in this
proposal changes any file outside this role's own two phase-1 homes.

## 0. Which verdict levels will be checked, and against what evidence

Phase 2 will render all three levels this role's contract requires. A
level that turns out not to apply will be written as "not applicable,
because X", never omitted.

1. **Outcome** — did PR #37 land what issue #36 asked. Checked against
   issue #36's seven acceptance-criteria checkboxes, each mapped to a
   specific hunk of `git show 2c462e0 -- <path>` across the five
   non-record files that commit touched (`src/rsb/web/dashboard.js`,
   `src/rsb/web/dashboard.css`, `test/rsb_tests/test_model.py`,
   `docs/specs/screen-spec.md`, `docs/specs/design-system.md`), or to a
   named third-party artifact — never to
   `docs/issue-36/reports/implementation.md`'s own prose about itself.
   Per scout-brief's adopt decision, each of the seven carries an
   explicit **demonstrated** / **asserted-only** label, where
   "demonstrated" requires a primary artifact other than the observed
   role's own record.
2. **Trajectory** — was the phase-1 → phase-2 path sound. Checked
   against: the file list of `403dbd0` (whether a survey and a scout
   brief existed before the proposal that `2c462e0` executes);
   `git show 403dbd0 -- docs/issue-36/proposals/implementation.md`
   against `2c462e0`'s hunks (whether what shipped is what was
   proposed); `docs/specs/approvers.md` plus PR #37's author field plus
   the byte-exact body of issue #36's single comment
   (https://github.com/tokenmaxxxer/repo-status-board/issues/36) and the
   empty `gh pr view 37 --json reviews` array (whether the single-account
   approval path contract v3 §19 defines was actually the one used); and
   the five timestamps in survey §3 (whether phase-2 work postdates the
   approval).
3. **Step** — which specific artifact, if any, is deficient. The
   candidate artifacts are enumerated in advance so the check cannot
   drift into whatever happens to look interesting: (a) the jsdom
   substitution recorded under "PR #37 feedback resolution" measured
   against the three items the PR #37 feedback comment
   (https://github.com/tokenmaxxxer/repo-status-board/pull/37) actually
   named; (b) `2c462e0`'s `docs/specs/screen-spec.md` and
   `design-system.md` hunks against issue #36 requirement 6 / AC6;
   (c) the two post-proposal "adversarial hunt" fixes against the
   approved proposal's stated scope; (d) the evidence backing AC2
   (single-line rendering in the Flows table); (e) PR #37's title and
   body text against what the PR actually carries at merge.

## 1. Method, per level

**Outcome.** Walk issue #36's ACs 1-7 in order. For each: locate the
hunk that implements it and cite it as `<sha> <path>` plus the changed
identifier, then apply the demonstrated/asserted-only label from §0.
Where the only support is the record's prose, the label is
asserted-only and the verdict sentence says so — per scout-brief's
must-be, an untraceable result is an assertion, not evidence. For AC3
specifically, the three concrete disclosure checks scout-brief adopted
(real `<button>`; `aria-expanded` synchronized with actual visibility;
`aria-controls` pointing at a container that exists) are each traced to
the `rowToggleButtonHtml`/`attachRowToggleHandlers` hunks of `2c462e0`,
and cross-referenced against the independent artifact already on `main`:
`test/rsb_tests/test_dashboard_dom.py`, added by commit `b2f6b63`
(issue #44, PR #45), whose commit message states its `.row-toggle`
click/`aria-expanded` cases were verified to fail against `b621082^`.
That cross-reference is read as a third-party artifact; it is not
re-run.

**Trajectory.** Three sub-questions, each answered with a citation:
did it scout when required (presence and content of
`docs/issue-36/reports/implementation/scout-brief.md` in `403dbd0`); did
it survey before proposing (same commit's file list plus whether the
proposal's Rationale cites survey sections); did it get real human
approval (the four facts in §0.2 — approvers.md membership, author
identity, byte-exact comment body, empty reviews array — evaluated
against contract v3 §19's single-account clause, with the near-miss
disclosure duty applied if the comment fails string equality).

**Step.** Each candidate in §0.3 is either cleared with a citation or
written up as a deficiency. Every deficiency finding carries the
four-part blameless shape scaled to one finding: **impact** (what a
reader or user of the merged tree gets wrong because of it),
**timeline** (the commit/comment timestamps that bracket it), **root
cause** (the mechanism, stated without attributing it to a person), and
**action item** (what would close it, addressed to the human, never
filed as an issue by this role).

## 2. What phase 2 will not do

- **No re-execution.** The pytest suite, `node --check`, the jsdom
  script, and any browser or axe-core run are all off the table — this
  role's rules make the observed role's produced artifacts the only
  admissible evidence, never a re-run of its task. A claim that can only
  be settled by re-running is therefore reported as unsettled, with the
  reason, rather than settled by re-running.
- **No reading `src/**` as evidence of what PR #37 did.** `main` now
  also carries `b2f6b63` and others; current file state is not this PR's
  diff.
- **No edits to the observed role's paths.** Nothing under
  `src/`, `test/`, `docs/specs/`, `docs/issue-36/proposals/implementation.md`,
  `docs/issue-36/reports/implementation.md` or
  `docs/issue-36/reports/implementation/` is touched by this role, in
  any phase. Findings return only through this role's own record on this
  role's own PR.
- **No issue filing.** Under contract v3 issues are user-authored only;
  a confirmed deficiency lands as a finding in this role's record for
  the human to judge.
- **No verdict on issue #36's conformance-review step.** That is the
  parallel role in the same plan step; this record speaks only to PR #37.

## 3. Record shape (phase-2 output)

`docs/issue-36/reports/execution-observation.md`, written as the first
act of phase 2 with `loop_state` updated at every transition, ordered
so that the independence statement — that this role neither authored nor
edited PR #37's artifacts in any session — appears **before** the first
verdict-bearing sentence, not merely somewhere in the file. Sections:
independence statement → what was read this session → outcome verdict
(AC table with demonstrated/asserted-only labels) → trajectory verdict →
step verdict (cleared items and any findings in the four-part shape) →
open findings. Every verdict-bearing sentence carries its citation
adjacent to it, in the same sentence or the one it directly qualifies.

## 4. How you'll know the phase-2 pass worked

- All seven of issue #36's ACs appear in the record with a label and a
  citation; none is silently dropped.
- All three verdict levels appear, including any that resolves to
  "not applicable, because X".
- No verdict-bearing sentence lacks an adjacent `<sha>` / `file:line` /
  PR-or-issue-comment URL.
- The independence statement precedes the first verdict sentence in
  document order.
- `git diff --name-only main...HEAD` for this branch touches only
  `docs/issue-36/reports/execution-observation.md`,
  `docs/issue-36/reports/execution-observation/*` and
  `docs/issue-36/proposals/execution-observation.md`.
- The PR body carries no closing keyword in any form, backticked
  included (issue #23 T2 precedent, restated by issue #36's own body).
