---
proposal: docs/issue-62/proposals/execution-observation.md
---

# Hunt record — issue-62 execution-observation

## after-proposal — stance 0: assume the gate just touched is bypassable — find the bypass

Verdict: FINDING — the scout-brief, a phase-1 artifact, already renders a preliminary verdict on step-level checks S1/S3 that the phase boundary (declared explicitly by the proposal and the survey) reserves for phase 2, and nothing in the admissibility rules stops phase 2 from citing that pre-approval sentence as if it were independently-derived grounding.
Kind: design-error
Seed: docs/issue-62/proposals/execution-observation.md, docs/issue-62/reports/execution-observation/{survey,scout-brief}.md
cap_seconds: 60
tier: size:small
diff_stat_lines: 3 new files under docs/, no src/ or test/ line (per dispatcher)
started_at: 2026-08-08T03:43:26Z
ended_at: 2026-08-08T03:47:30Z

### Reproduce
Compare the phase boundary the proposal and survey each declare for themselves against the scout brief, all three being phase-1 artifacts written before any approval exists (`gh issue view 62` shows no `APPROVE issue-62/execution-observation` comment yet):

```
$ grep -n "No level" docs/issue-62/proposals/execution-observation.md docs/issue-62/reports/execution-observation/survey.md
docs/issue-62/proposals/execution-observation.md:30:them. No level — not even provisionally — is answered anywhere in this
docs/issue-62/reports/execution-observation/survey.md:5:No level of the three-level verdict is answered anywhere in this file.

$ sed -n '75,84p' docs/issue-62/reports/execution-observation/scout-brief.md
## Gap line

The current state already meets: three of the four must-bes are already
practiced by the *observed* role's own artifacts (residual-class hunting
via the warrant hunt, declared substitution for pixel verification,
sourced scouting). ...
```

The proposal's own checklist declares the very same two questions still open, unresolved, phase-2-only work: `survey.md`'s S-a ("Unknown: what residual exposure classes remain... and whether any of them is reachable") and S-c ("Unknown: how far a `getComputedStyle` assertion is evidence for a touch-target requirement, and whether the record's own framing of it matches"), which the proposal restates as checks S1 and S3 to be "resolved" in the phase-2 record. Nothing in the six admissibility rules, and nothing in checks S1/S3 as literally written, forbids phase 2 from citing the scout-brief's Gap line itself (`docs/issue-62/reports/execution-observation/scout-brief.md:77-79`, a valid `file:line` under rule 3) as the citation for a verdict-bearing sentence resolving S1/S3 favorably — the same document's admissibility rule 4 already normalizes citing scout brief content directly ("Per scout [5][6][7][8][9]") as grounding inside this plan's own prose.

### Observed
The Gap line's claim — "already practiced by the observed role's own artifacts" — is itself an unsourced summary sentence (no `[n]` marker, no commit SHA, no `file:line` into the *observed* artifacts) sitting in a phase-1 document that predates the approval comment (scout-brief is part of this branch's still-unapproved proposal bundle; per the proposal's own "Status: Proposed, awaiting approval", phase 2 "does not begin until an approval lands"). A phase-2 record that quotes or leans on this sentence for S1/S3 would satisfy rule 3's literal citation requirement (a `file:line` sits "inside the sentence itself") while never having independently walked the residual-whitespace classes S1 itself demands ("tab- or other-whitespace-separated paths, a trailing fragment whose following word contains no `/`, repeated spaces") or the declared-vs-rendered jsdom distinction S3 demands against `reports/implementation.md:163-169`. The verdict would be citable-as-written and still ungrounded in the actual PR #64 artifacts for the specific residual-class/declared-vs-rendered work S1/S3 assign.

### Expected
Either the scout-brief should carry the same "no verdict, provisionally or otherwise" disclaimer the proposal and survey each state for themselves, or the admissibility rules should explicitly bar citing scout-brief prose (as opposed to its numbered external sources) as grounding for an O/T/S verdict sentence — so that S1/S3 can only close against evidence drawn from the observed PR's own artifacts, never against phase 1's own pre-approval self-assessment of "already meets."

### Resolution (by the dispatching role, before commit)

Both halves of "Expected" applied, in the same session, before anything
was committed:

1. `docs/issue-62/reports/execution-observation/scout-brief.md`'s Gap
   line rewritten to be scoped to this observation plan's own coverage
   (what survey §4–§5 had before the brief), with an explicit sentence
   that it says nothing about the observed role's artifacts. The
   "already practiced by the observed role's own artifacts" claim is
   gone.
2. Admissibility rule 7 added to
   `docs/issue-62/proposals/execution-observation.md`: no verdict-bearing
   sentence may cite this proposal, the survey, or the scout brief as
   its evidence; the scout brief's numbered external sources supply
   criteria, never conclusions.

The finding is therefore closed against the artifacts as committed, not
carried into phase 2.

## before-landing — skipped: docs-only, no before-landing dispatch
