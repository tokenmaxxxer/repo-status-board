---
status: proposed
files:
  - docs/issue-62/reports/execution-observation/survey.md
  - docs/issue-62/reports/execution-observation/scout-brief.md
  - docs/issue-62/proposals/execution-observation.md
  - docs/issue-62/reports/execution-observation.md
  - docs/reports/2026-08-08-hunt-issue-62-execution-observation.md
---

# Proposal — execution-observation of issue #62 step 1 (implementation, PR #64)

Read-only for this role in every phase (the observed artifacts):
`docs/issue-62/reports/implementation.md`,
`docs/issue-62/proposals/implementation.md`,
`docs/issue-62/reports/implementation/{survey,scout-brief}.md`,
`docs/reports/2026-08-08-hunt-issue-62-implementation.md`, commits
`caae317` and `6887979`, merge `8060c5a`, PR #64, issue #62 comment
`5224227464`.

Write target in phase 2: `docs/issue-62/reports/execution-observation.md`
(plus this role's own hunt record). Nothing under `src/`, `test/`,
`docs/specs/`, or `docs/issue-62/**/implementation*` is ever written by
this role.

## The three verdict levels this observation will check, named first

Declared here ahead of any method detail, so that everything after it is
answerable to these three and nothing in this document answers any of
them. No level — not even provisionally — is answered anywhere in this
proposal.

| level | question it will answer | evidence it will be answered from |
| --- | --- | --- |
| **outcome** | did PR #64 land what issue #62 asked | issue #62's 4 요구사항, 3 제약 and 4 Acceptance rows, read against the full diff of `6887979`, `git show --stat caae317`, PR #64's body, and the claims in `docs/issue-62/reports/implementation.md` |
| **trajectory** | was the phase-1 → phase-2 path the one contract v3 s19 prescribes | the seven timestamps in survey §2, `gh pr view 64 --json reviews` (`[]`), issue comment `5224227464`'s exact 31-byte body, `docs/specs/approvers.md`, both commits' `--stat` file lists and trailers, and the phase-1 artifacts' own mode/stage statements (`reports/implementation/scout-brief.md:3-7`) |
| **step** | which specific artifact, if any, is deficient | the surfaces S1–S6 enumerated below, each resolved against the artifact cited with it |

All three will be written out in the phase-2 record even where a level
turns out not to apply — as "not applicable, because X", never omitted.

## What was read to arrive at this plan

`docs/issue-62/reports/execution-observation/survey.md` §1.1 lists it
item by item: issue #62 and its single comment (raw API JSON, exact
body length), PR #64's full metadata, both commit messages with
`--stat`, the complete phase-2 diff for all six non-record files, the
253-line observed record, the observed proposal/survey/scout brief, the
hunt record, `docs/specs/approvers.md`, one SHA-pinned `git show` of the
merged proposal, and a trailer census of the whole history. Scout
findings and their sources are in
`docs/issue-62/reports/execution-observation/scout-brief.md` (1 sweep
round, 4 concurrent angles).

## Evidence admissibility rules adopted for phase 2

1. **Artifacts only, never re-execution.** `pytest` will not be run, the
   jsdom harness will not be built, `node` will not be invoked, and the
   hunt's repro script will not be executed. The observed role's test
   claims are read as claims.
2. **No unpinned `src/`/`test/` read.** Where markup, CSS or Python
   shape is needed it comes from `6887979`'s diff or from
   `git show 8060c5a:<path>`, with the SHA cited as the state the PR
   produced — never from a working-tree path.
3. **One citation adjacent to every verdict-bearing sentence** — commit
   SHA, `file:line`, or comment URL, inside the sentence itself.
4. **Author-attested-only claims are labelled, not upgraded.** Per scout
   [5][6][7][8][9], any claim whose evidence was never committed (the
   "69 passed, 2 failed" run at `reports/implementation.md:139-149`, the
   red-green sequences at `:151-161`, the individually-run DOM tests at
   `:163-169`) is recorded as *attested, uncorroborated* and carried as a
   declared scope limitation of this observation — never as verified,
   and never as contradicted.
5. **Arithmetic re-derivation from literals in the diff is admissible;
   running repo code is not.** The three WCAG ratios are recomputed from
   the hex values the diff itself contains (`#2563eb`, `#ffffff`,
   `#f3f4f6`, `#eff6ff`), using the relative-luminance formula and no
   repository import, no test invocation, and no observed-role code
   path. This re-derives a published number; it does not re-perform the
   observed task. If the approver reads rule 1 as excluding even this,
   the fallback is to compare the three independent statements of the
   numbers already in the artifacts (`proposals/implementation.md:161-165`,
   `reports/implementation.md:174-182`,
   `6887979:docs/specs/design-system.md` §2.2 hunk) for internal
   consistency only, and to record the arithmetic as unchecked.
6. **The two red `test_dashboard_dom.py` tests are cited, never
   re-established.** They are `f353910`-preexisting and issue #61's
   subject; phase 2 quotes `reports/implementation.md:139-149` and stops
   there. No root-cause work, no reproduction.
7. **Phase-1 prose is never grounding for a phase-2 verdict.** No
   verdict-bearing sentence may cite this proposal, the survey, or the
   scout brief as its evidence — the scout brief's *numbered external
   sources* supply criteria, never conclusions, and this role's own
   phase-1 files are not artifacts of PR #64. Every O/T/S sentence
   closes against a commit SHA, a SHA-pinned `file:line`, or a comment
   URL from the observed artifacts. (Added after this proposal's
   after-proposal warrant hunt showed rule 3's literal wording would
   otherwise accept a phase-1 `file:line` as a valid citation —
   `docs/reports/2026-08-08-hunt-issue-62-execution-observation.md:35-41`.)

## Checks phase 2 will run, and the evidence each is answered from

**Outcome level** (issue #62 요구사항 1–4, 제약, Acceptance).

- **O1** — 요구사항 1 (`#partial-retry` 24×24px via the existing
  `.row-toggle` pattern): the `dashboard.css` hunk in `6887979`
  (`.partial-banner a, .partial-banner button.link`), property by
  property against `.row-toggle`'s own rule as it stands at
  `8060c5a:src/rsb/web/dashboard.css`, plus a pinned read of
  `8060c5a:src/rsb/web/dashboard.js` to establish that `#partial-retry`
  is in fact the element that rule selects (survey O-a's unknown).
- **O2** — 요구사항 2 (both `<summary>` controls ≥24px, same pattern
  reused): the two `min-height` hunks in `6887979`, read against the
  proposal's stated `min-height`-only rationale
  (`proposals/implementation.md:78-88`) and against 요구사항 2's "같은
  패턴 재사용" wording — i.e. whether a deliberately *different* box
  model is within what the requirement asked, given the proposal
  declared and justified the divergence before approval.
- **O3** — 요구사항 3 (contrast target, mechanism, hover specificity
  order decided by the proposal, computed numbers recorded): the
  `tr.selected-row td:first-child` rule and its comment in `6887979`,
  the proposal's rationale (`proposals/implementation.md:58-76`), the
  record's three ratios (`reports/implementation.md:174-182`), and the
  `design-system.md` §2.2 hunk — with admissibility rule 5 applied to
  the numbers and the specificity claim checked as a claim about which
  properties `tr:hover` sets in `8060c5a:src/rsb/web/dashboard.css`.
- **O4** — 요구사항 4 (masking point and form decided with tradeoffs,
  red-green): the `fetch.py` hunk in `6887979`, the two rejected
  alternatives recorded at `proposals/implementation.md:42-56` and
  `reports/implementation/survey.md:119-130`, and the three
  `test_fetch.py` cases — with the red-green *runs* under admissibility
  rule 4 and the *tests themselves* read as committed artifacts.
- **O5** — the four Acceptance rows one by one: the two `check:` test
  rows against the committed test hunks; the `check:` docs row against
  the `design-system.md` §5/§2.2/§6 and `screen-spec.md` §2.4/§2.5
  hunks; the `unverifiable:` row against whether the record states the
  pixel-verification substitution in the terms that row requires
  (`reports/implementation.md:163-169`, `:171-182`).
- **O6** — the three 제약: no new token / no new hex / no new dependency
  (checked against `6887979`'s full diff for any `:root` or manifest
  line), declared-value computation as the disclosed substitute, and the
  issue #61 rebase-coordination clause against the record's account of
  it (`reports/implementation.md:17-22`).

**Trajectory level.**

- **T1** — phase ordering: whether `caae317` staged phase-1 homes only
  (`git show --stat caae317` — 3 files, all `docs/issue-62/`), whether
  PR #64 opened before any phase-2 file landed, and whether `6887979`
  postdates the approval, from the survey §2 timestamps.
- **T2** — approval path: PR #64 has zero reviews and the PR author and
  the commenter are the same `approvers.md` account, so which of
  contract v3 s19's two paths applies is itself part of the check;
  comment `5224227464`'s body is tested for byte-exact string equality
  (`body|length` = 31), and the comment list is checked for any
  approval-shaped near-match that would have to be reported as a
  near-miss.
- **T3** — the observed role's phase-1 obligations: survey, scout brief
  and proposal all present in `caae317`; the scout brief's declared mode
  and stage count (`reports/implementation/scout-brief.md:3-7`) and its
  per-angle `Sources:` lines; and whether the proposal's "What will be
  done" items 1–7 correspond item-for-item to what `6887979` landed.
- **T4** — the deviation this observation was specifically pointed at:
  the `_redact_paths` regex → word-scan replacement made after the
  03:09:38Z approval and before the 03:31:11Z commit. Criterion, taken
  from scout angle 1 [1][2][3]: did the *approved procedure* survive the
  change, or did the approval's conditions stop holding — applied to
  the proposal's literal item 4 wording
  (`proposals/implementation.md:103-111`, which names a regex over
  whitespace-free tokens) against the landed implementation
  (`6887979:src/rsb/fetch.py` `_redact_paths`), the record's own
  classification (`reports/implementation.md:113-127`), and whether the
  frozen write set was respected (`git show --stat 6887979` file list vs
  the proposal's frontmatter). Pre-landing self-detection is weighed as
  mitigation of severity [3], not as erasure.
- **T5** — commit and PR hygiene: `Subject: issue-62` on both commits,
  one commit per subject, no closing keyword in PR #64's title or body
  (`References #62`), and the phase-2 addendum in the body. The
  `Proposal:` trailer is checked only against this repository's own
  precedent (2 of 70 subject-trailered commits carry it, survey §1.1
  item 12) — i.e. whether it is a criterion here at all is part of the
  check, not an assumption going in.

**Step level.**

- **S1** — `_redact_paths` residual classes: the helper splits on the
  literal single space (`6887979:src/rsb/fetch.py`), so phase 2
  enumerates what that leaves — tab- or other-whitespace-separated
  paths, a trailing fragment whose following word contains no `/`,
  repeated spaces — and asks the scout-angle-3 question [10][11][12][13][14]:
  is the *claim's wording* (the record's, `design-system.md`'s and
  `screen-spec.md`'s "masked at generation") scoped to what the
  mechanism guarantees. Reachability is argued from the committed sink
  chain the artifacts themselves describe, never by executing anything.
- **S2** — assertion tightness: the two new DOM tests assert
  `== "24px"` (`6887979:test/rsb_tests/test_dashboard_dom.py`) where the
  Acceptance row says "24px 최소 박스" and the approved plan said "`>=
  24px`" (`proposals/implementation.md:123-124`, `:156-160`), judged on
  the over-specification/eager-test criterion [15][16][17].
- **S3** — evidence grade of the DOM assertions: jsdom performs no
  layout [18], so `getComputedStyle` there is evidence of declared and
  cascaded CSS, not rendered geometry [19][20]; phase 2 checks whether
  the record's own framing (`reports/implementation.md:163-169`) states
  that distinction or overstates it, against the `unverifiable:`
  Acceptance row's disclosure requirement.
- **S4** — hunt-record placement: the record filed under
  `docs/reports/` with a stated reason
  (`reports/implementation.md:193-201`,
  `docs/reports/2026-08-08-hunt-issue-62-implementation.md:7-14`), with
  `git log --oneline -- docs/reports/` showing `6887979` as that
  directory's only commit; checked against the six-standing-buckets
  layout rule and against whether the record accounts for the placement
  as written.
- **S5** — proposal lifecycle state: the frontmatter still reads
  `status: proposed` at `8060c5a:docs/issue-62/proposals/implementation.md:2`
  after the work landed; checked against this repository's own precedent
  for the field (whether any merged proposal ever advanced it) before
  any weight is placed on it.
- **S6** — completeness of the record's own disclosures: whether the
  "Open findings" section (`reports/implementation.md:239-243`), the
  "What did not work" section (`:91-111`) and the `closed_checks` list
  (`:223-237`) together account for everything O1–O6 / T1–T5 / S1–S5
  surface, or whether any surfaced item has no counterpart in the
  record.

## Shape of any confirmed deficiency

Four parts, scaled to a single finding, no postmortem ceremony:
**impact** (what a reader or a later session gets wrong because of it),
**timeline** (timestamped artifact facts only), **root cause**, **action
item** (a verifiable verb with an owner-shaped target). Blameless: the
finding names the artifact, never the session's diligence. Findings
return only in `docs/issue-62/reports/execution-observation.md` on this
role's PR — this role files no issue and edits nothing the observed role
wrote; the human judges the finding there.

## Deliberately out of scope

- Running `pytest`, `npm`, `node`, the jsdom harness, or the hunt's
  repro — admissibility rule 1.
- Re-establishing the two red `test_dashboard_dom.py` tests. They are
  `f353910`-preexisting and issue #61's subject; cited only.
- Re-observing issue #38's conformance-review or PR #43. R4e/R4e2/R6d/R5d
  are read only as the text issue #62's 요구사항 were cut from.
- A conformance matrix over the Acceptance rows as a compliance exercise
  — issue #62's 실행 계획 has no `conformance-review` step; the rows are
  read here only as the yardstick for the outcome level.
- Any edit under `src/**`, `test/**`, `docs/specs/**`, or
  `docs/issue-62/{proposals,reports}/implementation*`.
- Filing an issue, fixing anything found, or amending any spec — outside
  this role's authority.
- The phase-2 record itself: phase-2 output, not created in this phase.

## How you'll know phase 2 worked

`docs/issue-62/reports/execution-observation.md` exists and is committed
on this branch, with: the independence statement placed above every
verdict-bearing sentence; all three levels present, including any "not
applicable, because X"; a citation adjacent to each verdict-bearing
sentence; each of O1–O6 / T1–T5 / S1–S6 either resolved or explicitly
recorded as not-resolvable-from-artifacts under a named admissibility
rule; every author-attested-only claim labelled as such; any confirmed
deficiency in the four-part shape above; and `loop_state` updated at
each transition.

## Warrant hunt

One after-proposal dispatch, stance 0 (`.warrant-hunt.count` absent →
count 0), 60s cap, tier `size:small` — every path this transition
touches is under `docs/`. Dispatched foreground and consumed in the same
turn per contract v3 s22 (headless/single-shot). Its record is
`docs/reports/2026-08-08-hunt-issue-62-execution-observation.md`. The
before-landing dispatch is skipped under the docs-only fast path, and
that skip is stated in the hunt record rather than left silent.

## What did not work

- The scout brief's first Gap line asserted that "three of the four
  must-bes are already practiced by the *observed* role's own
  artifacts". Expected: a gap line describes the deliverable's own
  current state. What happened: because the deliverable here *is* a
  judgment of another role's artifacts, that sentence read as a
  provisional step-level verdict inside a phase-1 file, which the phase
  boundary forbids — caught by the after-proposal warrant hunt before
  commit. Rewritten to scope the gap line to this observation plan's own
  coverage, and admissibility rule 7 added so phase 2 cannot cite
  phase-1 prose as grounding either.

## Status

Proposed, awaiting approval. Phase 2 — the record at
`docs/issue-62/reports/execution-observation.md` and the three levels it
carries — does not begin until an approval lands per contract v3 s19.

## Sources

Numbered as in
`docs/issue-62/reports/execution-observation/scout-brief.md`'s
`Sources:` list, which carries the claim each backs.
