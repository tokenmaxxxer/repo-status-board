# Verification proposal — execution-observation (issue #38)

Status: phase-1 proposal. Scope: this role only, observing the
`implementation` role's session on issue #38 — PR #43
(`issue-38/implementation` → `main`, **merged** 2026-08-03T12:25:48Z,
merge commit `f3539107628a3a519eefe2f45b0e8d6f766a7912`, commits
`7c50201ef142498f29b265d7d98111a824f31d5e` phase 1 and
`e8443ea6536ff4aa131842143491f963d9d292d6` phase 2) and its record
`docs/issue-38/reports/implementation.md`. Grounded in
`docs/issue-38/reports/execution-observation/survey.md`'s open questions
and `scout-brief.md`'s adopt/skip decisions. No code changes this phase.

This document proposes a **method, not a result**: nothing below states
or implies whether PR #43's work was sound, complete, or otherwise —
that judgment is phase-2-only, gated on approval, and belongs in
`docs/issue-38/reports/execution-observation.md`.

## 0. Which verdict levels will be checked, and against what evidence

Phase 2 will address all three levels this role's contract requires, and
will write "not applicable, because X" rather than omit a level.

1. **Outcome — did PR #43 land what issue #38 asked.** Evidence: issue
   #38's nine acceptance-criteria checkboxes, each mapped to a specific
   hunk of `e8443ea` (`git show e8443ea -- <path>`), to PR #43's body
   text, or to a named line of `docs/issue-38/reports/implementation.md`
   — never to the record's summary of itself where a diff hunk exists.
   Each criterion will be filed into exactly one of three buckets, per
   the scout-brief's performance axis 2: **established from the
   artifacts** / **claimed by the observed role and not independently
   reproducible here** / **not establishable by anyone in this
   environment**. The seventh criterion ("기존 테스트 전부 통과") falls in
   bucket 2 by construction — 57 passed is reported at record lines
   187–190 and re-running it is prohibited for this role.
2. **Trajectory — was the phase-1→phase-2 path sound.** Evidence: the
   timestamp chain already pulled first-hand in the survey (phase-1
   commit `7c50201` 11:48:44Z → PR #43 opened 11:49:04Z → issue comment
   `APPROVE issue-38/implementation` 11:53:53Z, issuecomment-5165966474 →
   phase-2 commit `e8443ea` 12:24:20Z → merge 12:25:48Z); `git show
   --stat 7c50201` confirming phase 1 wrote only under `docs/issue-38/`;
   `docs/specs/approvers.md` for the approver listing and single-account
   mode; the observed role's own scouting artifacts
   (`docs/issue-38/reports/implementation/{survey,scout-brief}.md`, to be
   read in phase 2) for whether it surveyed and scouted before proposing;
   and PR #43's `reviews`/`comments` arrays (both empty) for whether any
   approval-shaped artifact exists outside the issue comment. Phase 2
   will also compare the approved proposal's own promised verification
   method (`docs/issue-38/proposals/implementation.md` lines 285–294 and
   316–327: `rsb serve`, 390px/1024px/1440px widths, VoiceOver, Tab
   traversal) against what the record reports it actually ran (record
   lines 102–171) — treating the substitution the way audit practice
   treats a substituted procedure (scout-brief "Adopt": judged on
   disclosure and on re-assessed sufficiency per criterion, not on
   whether jsdom equals a browser).
3. **Step — which specific artifact, if any, is deficient.** Evidence:
   the five open questions the survey left that resolve against readable
   artifacts —
   - Q1, PR #43's title (`phase 1: … survey + proposal`) vs. its body's
     "Phase 1 + phase 2 for #38" and the presence of `e8443ea` in the
     same PR;
   - Q3, the record's internal assertion arithmetic (line 125 "Three
     scenarios run" followed by four enumerated items; scenario 1's "(18
     checks)"; lines 194–196's "37 individual assertions across 4
     scripts"; `closed_checks` lines 262–264's "21 + 6 + 9 + 4 = 40
     assertions") — the scout-brief's "phantom results" probe, run as a
     pure arithmetic/consistency reading of the record;
   - Q4, whether `renderErrors(data.errors)` — untouched by `e8443ea`,
     visible as unchanged context inside `renderData`'s template — leaves
     an error surface outside the new summary+collapsed structure the
     fifth acceptance criterion asks for;
   - Q5, whether the partial banner's always-visible text as constructed
     (`` `${failedRepos.length} of ${total} repos failed to load — ${collapsibleDetailHtml(...)}` ``)
     matches what record lines 140–146 report it reads;
   - Q7, whether the `dashboard.css` hunk's own properties settle the
     first and fourth criteria statically (`#main-content,
     #detail-panel-slot { min-width: 0 }`, `table.data-table { min-width:
     640px }`, `.table-scroll { width: 100% }`, and `display:
     inline-flex` + `min-width`/`min-height: 24px` on `.row-toggle`),
     per the scout-brief's stage-2 finding that these outcomes are
     determined by statically readable properties.

## 1. Method (substituting for live execution)

This role may not re-run the observed role's code. Following the
issue-23/issue-27/issue-34 precedent, phase 2 will:

1. **Static diff tracing, not execution.** For each acceptance criterion
   and each open question above, trace the merged code by hand from the
   relevant `git show e8443ea -- <path>` hunk and write the traced path
   out in the record, rather than citing a line number and asserting a
   result. Where a hunk's meaning needs surrounding context, phase 2 will
   read the blob at that commit (`git show <sha>:<path>`) — a historical
   artifact read — and will never read the working tree's `src/`.
2. **Record-vs-artifact consistency.** Every claim in
   `docs/issue-38/reports/implementation.md` that describes a code change
   gets checked against the corresponding hunk; every reported count gets
   checked against the record's own other statements of that count.
   Mismatches are reported as mismatches, matches as matches.
3. **Test and jsdom results reported as claimed.** `57 passed`,
   `node --check`, and all four jsdom scripts are recorded as *claimed by
   the observed role, not independently reproduced*, with the prohibition
   named as the reason.
4. **Substituted-verification handling — this pass's own added method.**
   Phase 2 will (a) quote the exact promise in the approved proposal
   (lines 285–294) and the exact disclosure in the record (lines
   104–123); (b) state, criterion by criterion, what the jsdom substitute
   plus its hand-written `matchMedia` polyfill can and cannot establish —
   attribute/wiring facts yes, rendered layout and screen-reader
   announcement no, per the scout-brief's must-bes; and (c) state
   plainly whether the record's disclosure covers that partition or is
   global-only. This is the gap the comparator passes never had to
   handle and is not folded silently into another section.
5. **Trajectory read from timestamps already gathered**, restated in the
   record with citations rather than re-derived.
6. **Independence statement first.** The phase-2 record opens with the
   statement that this role did not author or edit any observed artifact
   this session, before any verdict language appears.

## 2. Record format

`docs/issue-38/reports/execution-observation.md` (phase-2 output) will
contain, in order: `code_under_review` + `loop_state` fields; the
independence statement; the three-level verdict (outcome / trajectory /
step) with an adjacent citation — commit SHA, `file:line`, or comment
URL — on every verdict-bearing sentence; a nine-row acceptance-criterion
table carrying the three-way bucket from §0.1; the substituted-
verification subsection from §1.4; any deficiency finding in the
four-part blameless shape (impact, timeline, root cause, action item),
scaled to the finding; and an explicit "what this session could not
check" section. `loop_state` is updated at each transition.

## 3. Out of scope

- Any code, test, or spec fix for anything found — this role may not edit
  the observed role's `src/`, `test/`, or record. Findings return only
  through this role's own record on this role's PR.
- Filing a GitHub issue for a finding — issues are user-authored under
  contract v3; the record hands off, the human decides.
- Reviewing the parallel step-2 `conformance-review` role's work on issue
  #38, or issue #36 / PR #37 on their own merits — #36 is citable only as
  the scope boundary the observed role invoked.
- Any rendered-pixel, real-browser, or screen-reader measurement, and any
  re-run of pytest, `node --check`, or the jsdom scripts — unavailable
  and prohibited respectively; phase 2 states that boundary rather than
  implying a measurement it did not make.
- Re-judging issue #38's design-gate findings themselves (whether the
  P1/P2/P3 list was the right list) — that is the issue author's call,
  not this role's.
</content>
