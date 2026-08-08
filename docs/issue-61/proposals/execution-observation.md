# Proposal: execution-observation of issue #61 step 2 — the implementation role's PR #66 and PR #69

files (read-only for this role, all phases):
- `docs/issue-61/reports/implementation.md` (the observed record, 236 lines)
- `docs/issue-61/proposals/implementation.md`,
  `docs/issue-61/reports/implementation/{survey,scout-brief}.md`
- commits `3096092`, `f93c819`, `346a6c0`, `a762ef0`; merges `3f06ba6`,
  `d8082dc`; PR #66, PR #69; issue #61 comments `5224224718`,
  `5224266614`
- `docs/specs/approvers.md`, `docs/issue-56/{proposals,reports}/execution-observation*`
  (precedent shape only)

write target (phase 2 only):
`docs/issue-61/reports/execution-observation.md`

## Verdict levels this observation will check, declared before anything else

Per this role's contract the phase-2 record renders exactly three
levels. They are named here, with the evidence each will be answered
from, ahead of any method detail — so that everything below is
answerable to them and nothing in this document answers any of them.

| level | question it answers | evidence it will be answered from |
| --- | --- | --- |
| **outcome** | did PR #66 + PR #69 land what issue #61 asked | issue #61's 3 requirements and 3 `check:` acceptance bullets, read against the full diffs of `346a6c0` (dashboard.js, screen-spec.md, test_dashboard_dom.py) and `a762ef0` (test_model.py), PR #66's and PR #69's bodies, and `docs/issue-61/reports/implementation.md`'s own claims |
| **trajectory** | was the phase-1 → phase-2 path the one the contract prescribes | the eleven timestamps in `reports/execution-observation/survey.md` §2, `git show --stat` file lists for all four commits, `gh pr view 66/69 --json reviews` (both `[]`), `docs/specs/approvers.md`, issue comment `5224266614`'s exact body, and the observed role's own phase-1 artifacts (`reports/implementation/scout-brief.md:1-8`, `survey.md:72`, `:320`) |
| **step** | which specific artifact, if any, is deficient | the eighteen check surfaces enumerated in `reports/execution-observation/survey.md` §4, each resolved against the artifact cited there |

All three levels will be written out in the record even where a level
turns out not to apply, as "not applicable, because X" rather than
omitted. No level is answered in this document.

## What was read to arrive at this plan

`docs/issue-61/reports/execution-observation/survey.md` §1 lists it
exhaustively: issue #61 and both of its comments (verbatim bodies via
`gh issue view --json comments`), PR #66's and PR #69's full metadata and
bodies, all four commit messages with `--stat`, the complete phase-2 and
later-entry diffs for the four non-record files, the observed record
(236 lines), the observed proposal (151 lines), the observed survey's
section structure and its scout brief in full, `docs/specs/approvers.md`,
this role's own precedent under `docs/issue-56/`, and the repository
shape facts (`ls docs/specs/`, `ls .github/workflows/`,
`git config core.hooksPath`, `grep -rn "Later entry" docs/`). Scout
findings are in `.../execution-observation/scout-brief.md` (4-angle
parallel sweep + 1 deepening stage on G1/G3, 2 stages total).

## Evidence admissibility rules adopted for phase 2

Derived from this role's directive and sharpened by the scout brief's
must-bes:

1. **Artifacts only, never re-execution.** The diffs of `346a6c0` /
   `a762ef0`, the four commit messages, the merged trees at `3f06ba6` /
   `d8082dc` cited by SHA, the two PRs, the two issue comments, and the
   observed role's own documents are the admissible evidence. `pytest`
   will not be run, `node --check` will not be re-run, and no jsdom
   harness will be built or driven — each of those would be re-executing
   the observed role's task. The record's test claims are read as claims.
2. **`src/` at working-tree HEAD is not evidence of what happened.** Any
   markup, JS, or test text quoted in the record comes from the commit
   diff that produced it, never from an unpinned file read.
3. **One citation per verdict-bearing sentence, adjacent to it** — SHA,
   `file:line`, or comment URL, inside the sentence itself.
4. **A claim with no surviving artifact is recorded as
   author-attested-only** — neither verified nor contradicted. This is
   expected to apply to every pytest count in the record
   (`reports/implementation.md:89-104`, `:118-119`, `:178-184`) and to the
   `node --check` runs (`:84-85`, `:105-106`), since `ls
   .github/workflows/` returns `deploy-board.yml` alone and no CI run
   attests them.
5. **A disclosed limit is adjudicated on the adequacy of its
   disclosure**, not rounded up to a defect or down to a non-event
   (scout brief performance axis 2). The record's scope-exceeded stop
   (`:130-151`) is the case this rule is written for.
6. **Field yardsticks are applied only where the scout brief adopted
   them** — approval scope [1][2], red-main time box [3]–[6], APG
   `aria-controls` resolution and synchronization [7][10], exact-literal
   brittleness [11][12]. Patterns the brief marked skip are not used to
   generate findings.

## Checks phase 2 will run, and the evidence each is answered from

Numbering maps to the survey §4 rows.

**Outcome level.**

- **O1** — AC 1 (`test_dashboard_dom.py` 전건 통과, 0 skipped, main의
  적색 2건 green 전환): the record's Red-green section
  (`reports/implementation.md:87-109`) under admissibility rule 4, plus
  the new-case hunk in `346a6c0` and the guard hunk it depends on.
- **O2** — AC 2 (narrow 분기 aria-controls 해소를 단언하는 DOM 케이스):
  the four assertions in `346a6c0`'s `test_dashboard_dom.py` hunk —
  specifically whether `resolvedId == "detail-row"` asserts IDREF
  *resolution* as the AC words it, or a string identity that would pass
  without resolution.
- **O3** — AC 3 (screen-spec §1.3 양 분기 서술): the `screen-spec.md`
  hunk in `346a6c0`, both the §1.3 sentence and the §1.6 bullet, against
  the AC's literal wording (which names §1.3 only).
- **O4** — 요구사항 1 (수정 위치를 트레이드오프와 함께 결정 + red-green):
  `proposals/implementation.md:37-54` (inline guard adopted, harness stub
  rejected, `true` fallback justified) against what `346a6c0` actually
  emits, and against the record's Red-green framing.
- **O5** — 요구사항 3 (§20 무가드 브라우저 API 전수 열거 + 범위 판단):
  `proposals/implementation.md:56-75` and `reports/implementation.md:50-56`
  — whether the enumeration is complete as an enumeration and whether
  the exclusion decision is recorded where a later session will find it.
- **O6** — the issue's constraints (renderErrors 부활 금지, 새 의존성·새
  토큰 금지, #62 파일 겹침 rebase 조율): the four commits' `--stat` file
  lists and the diffs' content.

**Trajectory level.**

- **T1** — phase ordering: whether `3096092` (03:18:32Z) staged phase-1
  homes only, whether PR #66 opened (03:18:53Z) before the approval
  (03:20:33Z) and before any phase-2 file landed (`f93c819`, 03:23:20Z),
  from the `--stat` file lists and the survey §2 timeline.
- **T2** — the phase-1 spike: `reports/implementation/survey.md:72-73`
  heads a spike section whose measurement (9/9 and 66/66, before
  approval) is at `:89-90` and whose disposition (`git checkout --`로
  되돌림, "커밋 트리에는 반영되지 않음") is at `:75-77`; those three
  ranges, plus what `git show --stat 3096092` shows about whether any of
  it was committed. (Citation ranges corrected from a bare `:72` after
  this phase's warrant hunt — see survey §7.)
- **T3** — approval path under single-account mode: comment
  `5224266614`'s body against the exact string `APPROVE
  issue-61/implementation`, its author against `docs/specs/approvers.md`,
  and PR #66's `reviews: []` — including whether the record's own
  characterization (`:9-11`) matches those facts.
- **T4** — the later entry's authorization (survey row 10): whether the
  content of `a762ef0` / PR #69 falls inside what comment `5224266614`
  approved, given that the record's own Open findings prescribed "a
  follow-up proposal with write set `test/rsb_tests/test_model.py`"
  (`:160-163`) and the delivery instead recorded a "Later entry —
  `test_model.py` fix (contract s19)" section (`:167-184`) with PR #69
  carrying `reviews: []` and no second APPROVE comment on the issue.
  Adjudicated on the approval-scope must-be [1][2] and on
  `grep -rn "Later entry" docs/` returning this record alone.
- **T5** — the mainline window (survey row 9): merge `3f06ba6`
  (03:40:32Z) landed while the record itself stated 66 passed / 1 failed
  (`:111-128`); `d8082dc` (03:46:29Z) closed it 5m57s later. Adjudicated
  on the red-main time-box must-be [3]–[6] and on what PR #66's body
  disclosed at merge time.
- **T6** — the stranded-relay episode: comment `5224224718` (03:08:49Z,
  `pr-create-failed`, "No commits between main and
  issue-61/implementation") against the first commit's authored date
  (03:18:32Z) — what the artifacts show about how the session resumed,
  and whether any artifact records it.
- **T7** — the observed role's phase-1 scout obligations: whether
  `reports/implementation/scout-brief.md:1-8` states its mode (parallel
  or batched-sequential) and stage count as the directive requires, and
  whether its four sources (`:68-73`) back its claims.
- **T8** — commit hygiene the contract makes mechanical: `Subject:
  issue-61` on all four commits, one commit per subject, and PR #66/#69
  titles and bodies checked for closing keywords.
- **T9** — warrant-hunt record completeness across both transitions:
  `survey.md:320-360` (phase 1, stance 0) and
  `reports/implementation.md:186-206` (before-landing, stance 1), the
  stance rotation actually used, and whether `a762ef0` — a further
  landing — carries or accounts for a hunt.

**Step level.**

- **S1** — `aria-controls` staleness bound (survey row 7): whether
  anything in the `applySelectionLayout` hunk of `346a6c0` re-runs the
  override when the viewport crosses `WIDE_LAYOUT_QUERY` without a
  re-render, and whether the record or the `screen-spec.md` hunk states
  that bound. Yardstick: APG's synchronization must-be [7][10].
- **S2** — the singleton `id="detail-row"` (survey row 8): what the
  `detailRowHtml` and `applySelectionLayout` hunks in `346a6c0`
  guarantee about at-most-one occurrence, against the justification given
  at `proposals/implementation.md:93-98` and `reports/implementation.md:25-27`,
  and against the ARIA-id uniqueness expectation [8][9].
- **S3** — the wide-branch residue: in the wide branch the selected
  button keeps `aria-controls="detail-panel-slot"`
  (`346a6c0`'s `rowToggleButtonHtml` hunk), while the narrow branch
  overrides only `selectedRow.querySelector(".row-toggle")` — what the
  diff shows about the non-selected buttons' IDREF in the narrow branch,
  read against the F2 wording in issue #61's 배경.
- **S4** — the exact-literal class (survey row 18 and `a762ef0`):
  whether the delivery closed the coupling class or re-pinned it, and
  whether the record names the class. Yardstick: [11][12], applied as a
  characterization, not as a demand that the test be rewritten.
- **S5** — proposal frontmatter shape (survey row 17):
  `proposals/implementation.md:1-4` opens with a bare `files:` list, no
  `---` fence and no `status:` field; what the precedent proposals under
  `docs/issue-*/proposals/` show about the repository's own convention,
  and whether the deviation, if any, reaches anything a later session
  depends on.
- **S6** — record self-consistency: the record's `code_under_review`
  frontmatter names four files including `test_model.py` (`:2`), while
  its Scope section names a three-file frozen write set (`:64-68`); how
  the later entry is accounted for across both, and whether `loop_state:
  landed` (`:3`) matches the artifacts.

## Shape of any confirmed deficiency

Four parts, scaled to a single finding, no postmortem ceremony:
**impact** (what a reader or a later session gets wrong because of it),
**timeline** (timestamped facts only, no causal narrative), **root
cause**, **action item** (a verifiable verb with an owner-shaped
target). Blameless: the finding names the artifact, never the session's
diligence. Findings return only in
`docs/issue-61/reports/execution-observation.md` on this role's PR; this
role files no issue and edits nothing the observed role wrote.

## Deliberately out of scope

- Running `pytest`, `node --check`, any jsdom harness, or `rsb serve` —
  admissibility rule 1.
- Any edit under `src/**`, `test/**`, `docs/specs/**`, or
  `docs/issue-61/{proposals,reports}/implementation*`. This role's only
  write paths are `docs/issue-61/reports/execution-observation{,.md}` and
  `docs/issue-61/proposals/execution-observation.md`.
- Re-observing issues #36 / #38 / #44. Their findings are read only as
  the text issue #61's requirements were cut from.
- Issue #62's parallel work (`dashboard.css`, `src/rsb/fetch.py`,
  merge `8060c5a`) except where survey row 6's constraint check requires
  its file list.
- Re-litigating the design choice the human already approved (inline
  guard over harness stub, `true` fallback): the approved proposal's
  decisions are the yardstick, not the subject.
- Filing any issue, fixing `test_model.py`, or amending any spec — all
  outside this role's authority.
- The record file `docs/issue-61/reports/execution-observation.md`
  itself: phase-2 output, not created in this phase.

## How you'll know phase 2 worked

The record exists at `docs/issue-61/reports/execution-observation.md`,
committed on this branch, with: the independence statement placed above
every verdict-bearing sentence; all three levels present, including any
"not applicable, because X"; a citation adjacent to each verdict-bearing
sentence; each of O1–O6 / T1–T9 / S1–S6 resolved or explicitly recorded
as not-resolvable-from-artifacts; any confirmed deficiency in the
four-part shape above; and `loop_state` updated at each transition.

## Status

Proposed, awaiting approval. Phase 2 — the record at
`docs/issue-61/reports/execution-observation.md` and the three levels it
carries — does not begin until an approval lands per contract v3 s19.

## Sources

Annotated list with the claim each backs:
`docs/issue-61/reports/execution-observation/scout-brief.md` `Sources:`.

- <https://best.openssf.org/SCM-BestPractices/github/repository/dismisses_stale_reviews.html>
- <https://docs.github.com/articles/approving-a-pull-request-with-required-reviews>
- <https://trunkbaseddevelopment.com/committing-straight-to-the-trunk/>
- <https://blog.aspect.build/keeping-main-green>
- <https://dev.to/kevincox/how-to-keep-your-master-branch-green-with-git-4o99>
- <https://medium.com/@dingezzz/fix-forward-or-roll-back-making-the-right-call-in-software-development-df2c5e49764d>
- <https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-card/>
- <https://dequeuniversity.com/rules/axe/4.3/duplicate-id-aria>
- <https://www.accessibilitychecker.org/wcag-guides/ensure-every-id-attribute-value-used-in-aria-and-in-labels-is-unique/>
- <https://a11ysupport.io/tech/aria/aria-controls_attribute>
- <https://webcrawlerapi.com/glossary/playwright/how-to-fix-playwright-brittle-exact-text-assertions>
- <https://vitest.dev/guide/snapshot.html>
