# Proposal: execution-observation of issue #56 step 1 (implementation, PR #57)

files (read-only for this role, all phases):
- docs/issue-56/reports/implementation.md (observed record)
- docs/issue-56/proposals/implementation.md, .../reports/implementation/{survey,scout-brief}.md
- commits 71a0dff, 21c2359; merge 93a60b3; PR #57; issue #56 comment 5177783505
- docs/issue-38/reports/execution-observation.md (upstream findings F1·F3, yardstick only)

write target (phase 2 only): docs/issue-56/reports/execution-observation.md

## Verdict levels this observation will check, declared before anything else

Per this role's contract the phase-2 record renders exactly three levels.
They are named here, with the evidence each will be answered from, ahead
of any method detail — so that everything below is answerable to them and
nothing in this document answers any of them.

| level | question it answers | evidence it will be answered from |
| --- | --- | --- |
| **outcome** | did PR #57 land what issue #56 asked | issue #56's 3 requirements and 4 `check:` acceptance criteria, read against `git show 21c2359` (the five non-record files), `git show --stat 71a0dff`, PR #57's body, and `docs/issue-56/reports/implementation.md`'s own claims |
| **trajectory** | was the phase-1 → phase-2 path the one the contract prescribes | the seven timestamps in survey §2 (issue 10:02:20Z, `71a0dff` 10:11:51Z, PR #57 10:12:22Z, comment 5177783505 10:29:48Z, hunt window 02:15:00–02:31:32Z, `21c2359` 02:36:12Z, merge 02:39:24Z), `gh pr view 57 --json reviews` (empty), `docs/specs/approvers.md`, each commit's `--stat` file list, and the phase-1 artifacts' own mode/stage statements (`reports/implementation/scout-brief.md:4-8`) |
| **step** | which specific artifact, if any, is deficient | the twelve check surfaces enumerated in survey §4, each resolved against the artifact cited there |

All three levels will be written out in the record even where a level
turns out not to apply, as "not applicable, because X" rather than
omitted. No level is answered in this document.

## What was read to arrive at this plan

`docs/issue-56/reports/execution-observation/survey.md` §1 lists it
exhaustively: issue #56 and its one comment (exact body via
`gh api`), PR #57's full metadata and body, both commit messages with
`--stat`, the entire phase-2 diff for the five non-record files, the
observed record (209 lines), the observed proposal (143 lines), the
observed survey and scout brief, `docs/specs/approvers.md`, the two
upstream rows and four finding headings in
`docs/issue-38/reports/execution-observation.md`, and targeted
`git grep` reads of the merged tree at `93a60b3`. Scout findings are in
`.../execution-observation/scout-brief.md` (4-angle parallel sweep +
1 deepening stage, 2 stages).

## Evidence admissibility rules adopted for phase 2

Derived from this role's directive and sharpened by the scout brief's
must-bes:

1. **Artifacts only, never re-execution.** PR #57's diff, commits
   `71a0dff`/`21c2359`, the merged tree at `93a60b3`, and the observed
   record are the admissible evidence. `pytest` will not be run,
   `node --check` will not be re-run, and no jsdom harness will be built
   — doing any of those would be re-executing the observed role's task.
   The record's own test claims are read as claims.
2. **`src/` at working-tree HEAD is not evidence of what happened.**
   Where markup or CSS shape is needed, it is taken from `21c2359`'s
   diff, or from the tree at `93a60b3` with the SHA cited as the state
   the PR produced — never from an unpinned file read.
3. **One citation per verdict-bearing sentence, adjacent to it** —
   commit SHA, `file:line`, or comment URL, inside the sentence itself.
4. **A claim with no surviving artifact is recorded as
   author-attested-only** — neither verified nor contradicted. This is
   expected to apply to the "64 passed, 2 failed" run
   (`docs/issue-56/reports/implementation.md:136-149`) and to the hunt's
   two jsdom repros (`:177-178`), which were not committed. Whether any
   independent attestation exists will be established from
   `ls .github/workflows/` (a directory listing, not a run).
5. **A substituted verification is adjudicated on the
   alternative-procedures test** (scout brief [3][4]): pre-declared in
   the approved plan and documented as a substitution ⇒ treated as
   satisfied; undeclared or undocumented ⇒ recorded as a scope
   limitation. This is the criterion, not an action taken.

## Checks phase 2 will run, and the evidence each is answered from

**Outcome level.**

- **O1** — requirement 1 (`renderErrors` brought under the AC5 rule *or*
  merged/removed if it duplicates the banner): the `dashboard.js` hunk in
  `21c2359` against issue #56 requirement 1's two-branch wording, plus
  the proposal's rejection of the keep-and-collapse alternative
  (`proposals/implementation.md:40-55`).
- **O2** — requirement 2 (`.number-link` inline-exception determination
  reported as a measurement): `docs/issue-56/reports/implementation.md:58-97`
  read against admissibility rule 5, with the approved plan's own
  pre-declaration (`proposals/implementation.md:30-36`, `:80-83`) as the
  thing the substitution is checked against.
- **O3** — requirement 3 (no regression + one new test on the new
  surface): the `test_dashboard_dom.py` hunk in `21c2359` and the
  record's Tests section (`:134-161`), under admissibility rule 4.
- **O4** — AC 1 (document-scoped partial-failure test): the four
  committed assertions against `93a60b3:src/rsb/web/index.html:20,24`,
  adjudicated on the scope-vs-recurrence-surface criterion (scout brief
  [1][2]) — does the assertion reach where the surface could reappear, or
  only where it was found — and against the record's own description of
  its scope (`:49-54`).
- **O5** — AC 2 (`renderErrors` grep 0건): `git grep -n renderErrors
  93a60b3 -- src test`'s single comment-only hit at
  `test/rsb_tests/test_dashboard_dom.py:252`, read against the AC's
  literal wording and the record's advance disclosure (`:155-157`).
- **O6** — AC 3 (`.number-link` 24×24px, `.row-toggle` pattern): the
  `dashboard.css` hunk in `21c2359`, property by property against
  `.row-toggle`'s own rule as it stands at `93a60b3`.
- **O7** — AC 4 (screen-spec §1.9 deleted + §2.5 sole-surface line;
  design-system 24px list): the `screen-spec.md` and `design-system.md`
  hunks in `21c2359`, plus whether §5's enumerating parenthetical or only
  a following sentence carries `.number-link`
  (`93a60b3:docs/specs/design-system.md:163-170`, `:184`).
- **O8** — the constraint issue #56 attached ("PR #43 이 랜딩한 나머지 8개
  AC 구현은 무변경"): `git show --stat 21c2359`'s file list and the two
  `src/` hunks' line ranges, checked for any edit outside them.

**Trajectory level.**

- **T1** — phase ordering: whether `71a0dff` staged phase-1 homes only
  and the PR opened before any phase-2 file landed, from both `--stat`
  file lists and the two timestamps.
- **T2** — approval path: which of contract v3 s19's two paths applies
  given PR #57's author, `gh pr view 57 --json reviews` returning `[]`,
  comment 5177783505's author against `docs/specs/approvers.md`, and
  whether its body is an exact string match under string-equality-only.
  Under the separation-of-duties expectation the scout brief records
  ([7][8]), what the record additionally shows about the approval act
  being tamper-evident is part of this check, not a separate one.
- **T3** — the observed role's own phase-1 obligations: whether survey,
  scout brief, and proposal all exist in `71a0dff`, whether the scout
  brief states its mode and stage count (`:4-8`) and carries sources
  (`:74-79`), and whether the proposal's "What will be done" (`:85-111`)
  corresponds item-for-item to what `21c2359` landed.
- **T4** — commit hygiene the contract makes mechanical: `Subject:
  issue-56` trailer on both commits, one commit per subject, and PR
  #57's title/body checked for closing keywords — including whether the
  "(phase 1+2)" title avoids the shape issue-38 F4 flagged on PR #43
  (`docs/issue-38/reports/execution-observation.md:354`).
- **T5** — declared deviations: whether the record's one declared
  deviation (`:106-124`, the refused `PYTHONPATH=` env-prefix) is the
  only divergence the artifacts show between the approved plan and the
  delivery, or whether O1–O8 surface an undeclared one.

**Step level.**

- **S1** — the new test's assertion scope: `#main-content`-subtree for
  the raw-message assertion versus `document` for the two
  structure assertions, against `93a60b3:src/rsb/web/index.html:20,24`
  placing `#partial-banner` outside `<main>`, and against the record's
  and proposal's use of the phrase "문서 범위 / document-scoped"
  (`reports/implementation.md:49-54`,
  `proposals/implementation.md:101-108`).
- **S2** — residue of the deleted component: `21c2359` leaving
  `| ErrorListItem | status-error |` at
  `93a60b3:docs/specs/design-system.md:189` while deleting the §1.9
  region that §6's preamble (`:174`) says applies it, and leaving
  `/* HygieneListItem / ErrorListItem */` plus the `.error-list`
  selectors at `93a60b3:src/rsb/web/dashboard.css:347-349` (shared with
  `.hygiene-list`, which still renders). Adjudicated on the
  dead-reference criterion in the scout brief ([5][6]) and bounded by
  whether issue #56's ACs reach it.
- **S3** — verification-coverage of the record's own grep checks: the
  three greps at `:155-161` are scoped to `src/`, `test/`,
  `screen-spec.md`, and `design-system.md`'s `number-link` occurrences;
  what that scoping does and does not reach is read against S2's
  findings.
- **S4** — warrant-hunt record completeness: one `before-landing`
  section exists (`:163-195`) and no `after-proposal` section does, with
  `71a0dff` being docs-only; and the hunt is recorded inside the role
  record rather than under a `docs/reports/` bucket that this repository
  does not have (`ls docs/`). What phase 2 determines is whether the
  record as written accounts for both facts.
- **S5** — the hunt's own disclosed tension: its finding that
  `renderFullError` does put a message into `#main-content` on the
  total-failure path (`:177`) against §2.5's new sentence that the banner
  is "the only surface that displays partial-failure repo errors"
  (`21c2359:docs/specs/screen-spec.md` hunk) — checked for whether the
  spec sentence's scoping and the hunt's scoping agree as written.

## Shape of any confirmed deficiency

Four parts, scaled to a single finding, no postmortem ceremony:
**impact** (what a reader or a later session gets wrong because of it),
**timeline** (timestamped facts only, no causal narrative), **root
cause**, **action item** (a verifiable verb with an owner-shaped
target). Blameless: the finding names the artifact, never the session's
diligence. Findings return only in
`docs/issue-56/reports/execution-observation.md` on this role's PR; this
role files no issue and edits nothing the observed role wrote.

## Deliberately out of scope

- Running `pytest`, `node --check`, any jsdom harness, or `rsb serve` —
  admissibility rule 1.
- Any edit under `src/**`, `test/**`, `docs/specs/**`, or
  `docs/issue-56/{proposals,reports}/implementation*`. This role's only
  write paths are `docs/issue-56/reports/execution-observation{,.md}` and
  `docs/issue-56/proposals/execution-observation.md`.
- Re-observing PR #43 / issue #38. Its findings F1·F3 are read only as
  the text issue #56's requirements were cut from — including the label
  collision noted in survey §1 item 8, which is issue #38's artifact and
  not chargeable to PR #57.
- A conformance matrix over the ACs as a compliance exercise — that is
  issue #56 실행 계획 step 2's parallel `conformance-review` role, which
  has no PR on the board as of this session; this observation reads the
  ACs only as the yardstick for the outcome level.
- Filing any issue, fixing the `ErrorListItem` residue, or amending any
  spec — all outside this role's authority.
- The record file `docs/issue-56/reports/execution-observation.md`
  itself: phase-2 output, not created in this phase.

## How you'll know phase 2 worked

The record exists at `docs/issue-56/reports/execution-observation.md`,
committed on this branch, with: the independence statement placed above
every verdict-bearing sentence; all three levels present, including any
"not applicable, because X"; a citation adjacent to each
verdict-bearing sentence; each of O1–O8 / T1–T5 / S1–S5 resolved or
explicitly recorded as not-resolvable-from-artifacts; any confirmed
deficiency in the four-part shape above; and `loop_state` updated at
each transition.

## Status

Proposed, awaiting approval. Phase 2 — the record at
`docs/issue-56/reports/execution-observation.md` and the three levels it
carries — does not begin until an approval lands per contract v3 s19.

## Sources

Annotated list with the claim each backs:
`docs/issue-56/reports/execution-observation/scout-brief.md` `Sources:`.

- <https://github.com/testing-library/eslint-plugin-testing-library/blob/main/docs/rules/prefer-screen-queries.md>
- <https://kentcdodds.com/blog/common-mistakes-with-react-testing-library>
- <https://www.accountingtools.com/articles/alternative-procedures>
- <https://pcaobus.org/oversight/standards/archived-standards/pre-reorganized-auditing-standards-interpretations/details/AU330>
- <https://newsletter.baselinedesign.com/what-the-system-is-trying-to-tell-you/>
- <https://www.uxpin.com/studio/blog/design-system-maintenance-checklist/>
- <https://medium.com/@aneeqr25/ensuring-fair-code-reviews-how-to-block-self-approval-in-github-pull-requests-6338341e4765>
- <https://www.propelcode.ai/blog/code-review-compliance-sox-hipaa-pci-requirements>
- <https://en.wikipedia.org/wiki/Regression_testing>
</content>
