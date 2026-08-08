---
observed_artifacts: PR #66 (3096092, f93c819, 346a6c0; merge 3f06ba6), PR #69 (a762ef0; merge d8082dc), docs/issue-61/reports/implementation.md, docs/issue-61/proposals/implementation.md
loop_state: landed
---

# issue-61 step 2 — execution observation of the implementation role's PR #66 and PR #69

## Independence

This role did not author, edit, or execute any part of the artifact it
observes. Nothing under `src/`, `test/`, `docs/specs/`, or
`docs/issue-61/{proposals,reports}/implementation*` was written or
modified by this session; the only files this session writes are this
record and its phase-1 siblings under
`docs/issue-61/reports/execution-observation/` and
`docs/issue-61/proposals/execution-observation.md`. No test suite, no
`node --check`, and no jsdom harness was re-run — the observed role's
produced artifacts (commit diffs, commit messages, PR metadata and
bodies, issue comments, and its own record) are the sole admissible
evidence, per the six admissibility rules fixed in
`docs/issue-61/proposals/execution-observation.md` before approval.

Every verdict-bearing sentence below carries its own citation adjacent
to it. Where a count is derived rather than quoted, the derivation
method is stated with it.

## What was done

Phase 2 was opened by issue comment
<https://github.com/tokenmaxxxer/repo-status-board/issues/61#issuecomment-5224396196>
(author `jjongkwann`, listed in `docs/specs/approvers.md`), whose entire
body is the exact string `APPROVE issue-61/execution-observation` —
single-account mode per contract v3 s19, since PR author and approver
are the same account.

Read first-hand this session, as the evidence base for everything below:
issue #61 in full and all three of its comments (`5224224718`,
`5224266614`, `5224396196`, verbatim bodies via `gh issue view 61 --json
comments`); PR #66 and PR #69 metadata and bodies (`gh pr view`,
`reviews: []` and `comments: []` on both); the four commit messages with
`--stat` (`3096092`, `f93c819`, `346a6c0`, `a762ef0`) and the full
non-record diffs of `346a6c0` (`dashboard.js`, `screen-spec.md`,
`test_dashboard_dom.py`) and `a762ef0` (`test_model.py`);
`docs/issue-61/reports/implementation.md` (236 lines);
`docs/issue-61/proposals/implementation.md` (151 lines); the observed
role's `reports/implementation/{survey,scout-brief}.md`; the commit
graph around the two merges (`git log --format='%h parents:%p'`); and
static `^def test_` counts on four pinned trees.

The three verdict levels the approved proposal declared —
**outcome**, **trajectory**, **step** — are rendered below, in that
order. All three are addressed; the eighteen check surfaces resolve into
them as O1–O6 / T1–T9 / S1–S6.

## Why

Issue #61's 실행 계획 names step 2 as `execution-observation`, and this
record is that step's only artifact that matters. The approved plan
(`docs/issue-61/proposals/execution-observation.md`) declared the three
levels, the eighteen surfaces, and the admissibility rules before
approval, so no verdict here is shaped by what turned out convenient to
find.

---

# Level 1 — Outcome

**Verdict: the delivery landed what issue #61 asked.** All three
`check:` acceptance bullets are met by the merged artifacts, and all
three 요구사항 are discharged; one acceptance-adjacent claim is
author-attested only, and one delivered test is narrower than the
approved plan promised (finding **F-3**).

**O1 — AC 1 (`test_dashboard_dom.py` 전건 통과, 0 skipped, main 적색
2건 green 전환): met, on an author-attested measurement that the
artifacts corroborate structurally but no CI attests.** The record
claims red `2 failed, 7 passed` before the edit and green `10 passed`,
0 skipped after (`docs/issue-61/reports/implementation.md:89-101`), and
`ls .github/workflows/` returns `deploy-board.yml` alone, so no CI run
attests either number — both are recorded here as author-attested-only
per admissibility rule 4. The red half is independently corroborated by
issue #61's own body, which states `main 의 test_dashboard_dom.py 2건이
현재 적색(65 중 63 통과)` — a user-authored artifact, not the observed
role's claim. The green half is structurally consistent with the diff:
`346a6c0`'s `applySelectionLayout` hunk falls back to `isWideLayout =
true` when `matchMedia` is absent, so the two previously-crashing cases
take the wide branch and their existing `#detail-panel-slot` assertions
hold, and a static `^def test_` count on the pinned tree `346a6c0`
returns 10 for `test/rsb_tests/test_dashboard_dom.py`, matching the
record's `10 passed` exactly.

**O2 — AC 2 (narrow 분기 aria-controls IDREF 해소를 단언하는 DOM
케이스): met.** The new case
`test_row_toggle_narrow_layout_aria_controls_resolves_to_detail_row` in
`346a6c0`'s `test_dashboard_dom.py` hunk computes `const resolved =
document.getElementById(ariaControls)` and asserts `result["resolvedId"]
== "detail-row"` where the script emits `resolved ? resolved.id : null`
— so a non-resolving IDREF yields `null` and fails the assertion, which
is IDREF *resolution* as the AC words it, not a string identity check
(`346a6c0`, `test/rsb_tests/test_dashboard_dom.py` hunk, lines
`resolvedId: resolved ? resolved.id : null` and `assert
result["resolvedId"] == "detail-row"`).

**O3 — AC 3 (screen-spec §1.3 양 분기 서술): met, and exceeded.**
`346a6c0`'s `docs/specs/screen-spec.md` hunk adds to §1.3 the clause
"`aria-controls="detail-panel-slot"` by default (wide layout, or narrow
with no selection), updated to `"detail-row"` when the narrow (<1200px)
layout has that row's panel expanded as a sibling `<tr>` (§1.6)", and
adds a symmetric §1.6 bullet naming `id="detail-row"` and
cross-referencing §1.3 — the AC names §1.3 only, so the §1.6 bullet is
above requirement.

**O4 — 요구사항 1 (수정 위치를 트레이드오프와 함께 결정 + red-green):
met, and the delivered guard is byte-identical to the approved one.**
`docs/issue-61/proposals/implementation.md:37-54` adopts the call-site
inline feature-detection guard, records `하네스 matchMedia 스텁 주입` as
`alternative considered and rejected` with the reason (a harness stub
leaves the production call site unguarded), and justifies the `true`
fallback against the measured alternative; the two statements
`346a6c0`'s `applySelectionLayout` hunk emits — `const mql = typeof
window.matchMedia === "function" ? window.matchMedia(WIDE_LAYOUT_QUERY)
: null;` and `const isWideLayout = mql && typeof mql.matches ===
"boolean" ? mql.matches : true;` — are character-for-character the ones
written at `docs/issue-61/proposals/implementation.md:87-90`, so nothing
was swapped between approval and delivery.

**O5 — 요구사항 3 (§20 무가드 브라우저 API 전수 열거 + 범위 판단): the
판단 half is discharged and durably recorded; the 전수 half is
author-attested only.** The exclusion decision is recorded in three
places a later session will reach — the approved proposal's Rationale
(`docs/issue-61/proposals/implementation.md:56-75`), its Out of scope
list (`:125-128`), and the record's item 6
(`docs/issue-61/reports/implementation.md:50-56`) — plus the delivery
commit message itself (`346a6c0`: `§20 요구사항 3 … 모듈 스코프
document.getElementById 7건을 범위 밖으로 유지(코드 변경 없음)`). The
enumeration's completeness — that the unguarded-browser-API class in
`dashboard.js` contains exactly module-scope `document.getElementById`
×7, `matchMedia` ×1, `fetch` ×1, and in-context `getElementById` ×3
(`docs/issue-61/proposals/implementation.md:56-63`) — rests on a
full-file scan the artifacts do not reproduce, and verifying it would
require reading `src/` at HEAD, which admissibility rule 2 excludes;
it is recorded here as author-attested-only, not as a defect.

**O6 — the issue's 제약: two met from the diffs, one not exercised as
written (see finding F-1).** `renderErrors` appears nowhere in the
non-record diffs of `346a6c0` and `a762ef0` (`git show 346a6c0 a762ef0
-- src test docs/specs | grep -n renderErrors` → no hits), so the
"renderErrors 부활 금지" constraint holds; no dependency manifest appears
in any of the four commits' `--stat` output and no new token appears in
the `screen-spec.md` hunk of `346a6c0`, so "새 의존성·새 토큰 금지"
holds. The third constraint — "issue #62와 파일이 겹치면 phase 2 시작
시 rebase 로 조율" (`docs/issue-61/proposals/implementation.md:25-29`) —
is the subject of finding **F-1**.

---

# Level 2 — Trajectory

**Verdict: the phase-1 → phase-2 path was sound in its gated
structure — scouted, surveyed, proposed, opened the PR, waited for a
real human approval, and only then built — with two departures from it
after the first delivery landed: the un-exercised #62 overlap constraint
(F-1) and the undisclosed substitution of the record's own prescribed
resolution path (F-2).**

**T1 — phase ordering: correct, by the commit graph and the
timestamps.** `git show --stat 3096092` (03:18:32Z) lists exactly three
files, all under `docs/issue-61/` (`proposals/implementation.md`,
`reports/implementation/scout-brief.md`,
`reports/implementation/survey.md`, +579) — the two phase-1 homes and
nothing else; PR #66 opened at 03:18:53Z (`gh pr view 66 --json
createdAt`), 100 seconds before the approval comment at 03:20:33Z
(`5224266614`); and the first phase-2 file landed at 03:23:20Z
(`f93c819`, 1 file, the record), after it. No phase-2 artifact predates
the approval.

**T2 — the phase-1 spike did not leak into the commit tree.**
`docs/issue-61/reports/implementation/survey.md:72-77` heads the spike
section and states its disposition — `git diff`, 실행 후 `git checkout
--`로 되돌림 … 이 survey 작성 시점 기준 커밋 트리에는 반영되지 않음 —
and `git show --stat 3096092` confirms it: three docs files, zero
`src/` or `test/` paths. The measurement the spike produced
(`test_dashboard_dom.py` 9/9, 전체 스위트 66/66) is at `survey.md:89-90`
and is what the approved proposal's Rationale cites, so the spike
functioned as evidence for the decision rather than as an uncommitted
delivery.

**T3 — the approval path is valid under single-account mode.** The
entire body of comment
<https://github.com/tokenmaxxxer/repo-status-board/issues/61#issuecomment-5224266614>
is the exact string `APPROVE issue-61/implementation`, its author is
`jjongkwann`, who is one of the two entries in `docs/specs/approvers.md`
(`JiwonJung94`, `jjongkwann`), and PR #66's author is the same account
with `reviews: []` (`gh pr view 66 --json author,reviews`) — precisely
the single-account path contract v3 s19 defines. The record's own
characterization at `docs/issue-61/reports/implementation.md:9-11`
matches those facts exactly, including naming the single-account
condition rather than claiming a review Approve.

**T4 — the later entry's authorization is defensible on a
branch-scoped reading of the approval, but the route to it was
substituted without disclosure — finding F-2.** PR #69's `headRefName`
is `issue-61/implementation` (`gh pr view 69 --json headRefName`), the
same branch the approval string names, so the work is not unapproved on
its face; what the artifacts show is that the record prescribed one
route at `docs/issue-61/reports/implementation.md:160-163` and took
another at `:164-167`, with no second APPROVE comment on the issue (the
issue carries exactly three comments, `5224224718`, `5224266614`,
`5224396196`) and `reviews: []` on PR #69. Detailed in **F-2**.

**T5 — the red-mainline window was disclosed at merge time and closed
in 5m57s: adequate, not a defect.** PR #66's body discloses the
remainder before the merge — `Known remainder, disclosed in the record:
test_model.py exact-string assertion (outside the frozen write set)
needs a one-line expected-string update; a later-entry fix follows
before step 2` (`gh pr view 66 --json body`) — and the record states the
failing state in its own text rather than hiding it
(`docs/issue-61/reports/implementation.md:111-128`). The window measures
5m57s from `3f06ba6` (03:40:32Z) to `d8082dc` (03:46:29Z), which sits
inside the field's time-boxed fix-forward expectation the scout brief
adopted (`docs/issue-61/reports/execution-observation/scout-brief.md:26-29`,
sources [5][6]); under admissibility rule 5 this is adjudicated on the
adequacy of the disclosure, and the disclosure names the exact test, the
exact reason, and the follow-up — adequate.

**T6 — the stranded-relay episode is visible only in the issue's own
comment, not in any artifact the observed role produced: an observation,
not a finding.** Comment
<https://github.com/tokenmaxxxer/repo-status-board/issues/61#issuecomment-5224224718>
(03:08:49Z) records `pr-create-failed … No commits between main and
issue-61/implementation`, and the first commit on the branch is
`3096092` at 03:18:32Z — 9m43s later — so the artifacts show a session
that produced nothing committed, then a session that committed the full
phase-1 set. Neither the record nor the observed survey mentions the
episode (no hit for it in either file), which leaves no artifact
answering what the stranded session had produced; because contract v3
puts stranded-relay handling on the human and the delivered phase-1 set
is complete on its own terms (`git show --stat 3096092`, +579 across the
three phase-1 files), this is recorded as an observation rather than a
deficiency.

**T7 — the observed role's scout brief states its stage count but not
its mode — finding F-5.**
`docs/issue-61/reports/implementation/scout-brief.md:3-6` states
`WebSearch 2회 … 2회로 종료` and names its four sources at `:66-73`,
but nowhere states whether the pass ran parallel or fell back to
batched-sequential, which the scout directive requires the brief to say.
Detailed in **F-5**.

**T8 — commit and PR hygiene: clean on every mechanical check.** All
four commits carry a `Subject: issue-61` trailer (`git show -s
--format=%B` on `3096092`, `f93c819`, `346a6c0`, `a762ef0`), one subject
per commit, with no second subject anywhere. Neither PR title carries a
closing keyword (`issue-61 phase 1: matchMedia 가드 위치 + aria-controls
IDREF 정합 proposal`, `issue-61 later-entry: test_model.py detail-row id
정합`). PR #66's body contains the phrase `Resolves the design questions
#61 raises`, which is a near-miss on GitHub's closing-keyword grammar —
the keyword is not adjacent to the reference, so it does not link, and
the empirical proof is that issue #61 is still `OPEN` after both merges
(`gh issue view 61` → `state: OPEN`); the same body also states `Plan
step 1 of 2 — no closing keyword` explicitly, and PR #69's body uses the
non-linking form `관련: #61`. Recorded as a near-miss worth avoiding in
phrasing, not as a violation.

**T9 — warrant-hunt coverage is complete for the first landing and
absent for the second — finding F-4.** The phase-1 hunt is recorded at
`docs/issue-61/reports/implementation/survey.md` ("Warrant hunt (phase
1)", stance 0) and the before-landing hunt at
`docs/issue-61/reports/implementation.md:186-206` (stance 1, correctly
rotated, `NO FINDING`, seed and tier named); `a762ef0` is a second
landing touching `test/rsb_tests/test_model.py` — outside the docs-only
fast path — and the record carries neither a hunt nor the mandatory skip
line for it. Detailed in **F-4**.

---

# Level 3 — Step

**Verdict: five artifacts carry deficiencies (F-1 … F-5), none of them
in the product change itself.** The `dashboard.js` guard, the
`aria-controls` override, the `id="detail-row"` addition, and the
`screen-spec.md` update are sound as delivered on every surface this
observation could resolve from artifacts; the deficiencies are in what
was measured after the merge, what was disclosed about the route, and
what the tests and briefs claim about themselves.

**S1 — the `aria-controls` override cannot go stale against the DOM it
describes; the bound is real but undisclosed.** `346a6c0`'s
`applySelectionLayout` hunk sets `aria-controls="detail-row"` inside the
same render pass that inserts the `<tr id="detail-row">`
(`selectedRow.insertAdjacentHTML("afterend", detailRowHtml(...))`
immediately followed by `selectedButton.setAttribute("aria-controls",
"detail-row")`), and the hunk adds no `matchMedia` change listener and
no resize listener, so a viewport crossing `WIDE_LAYOUT_QUERY` without a
re-render leaves attribute and element equally unchanged — the IDREF
still resolves to the element actually in the DOM, which is what APG's
synchronization must-be protects
(`docs/issue-61/reports/execution-observation/scout-brief.md:31-36`).
The pre-existing render-time-only layout switch is therefore the bound,
not a new staleness class introduced here; neither
`docs/issue-61/reports/implementation.md` nor `346a6c0`'s
`screen-spec.md` hunk states that bound, which is a documentation gap
too small to carry a finding on its own and is noted here instead.

**S2 — the singleton `id="detail-row"` is not shown to be violable by
anything in the delivery.** `346a6c0`'s `detailRowHtml` hunk emits the
static id, and the only insertion site in the same commit's
`applySelectionLayout` hunk sits inside the `else` branch reached only
when `selectedRow` is truthy — one selected row, one insertion. The
justification for a static id (a single `selectedIssue`, plus
`renderData`'s full `MAIN.innerHTML` rewrite clearing the prior row) is
recorded at `docs/issue-61/proposals/implementation.md:93-98` and
restated at `docs/issue-61/reports/implementation.md:25-27`; the
`renderData` rewrite it leans on is not touched by `346a6c0` and so is
not re-verified here, and the scout brief explicitly declined to treat
duplicate-`id` audit framing as a finding source
(`.../scout-brief.md:63-66`). No defect.

**S3 — the wide-branch and non-selected-button residue is described
accurately by the delivered spec text, so it is not a defect.** In
`346a6c0`, `rowToggleButtonHtml`'s emitted markup line is unchanged and
still hardcodes `aria-controls="detail-panel-slot"`, and the narrow
branch overrides only `selectedRow.querySelector(".row-toggle")` — so in
narrow layout the non-selected, collapsed buttons keep an IDREF pointing
at `#detail-panel-slot`, an element that exists (the branch sets
`DETAIL_SLOT.innerHTML = ""`, it does not remove it) but is not where
their panel would render at that width. Issue #61's F2 frames the false
relation as the case where the panel *is* expanded and the slot is
deliberately emptied, which is exactly the case the override closes, and
the delivered §1.3 text scopes itself correctly — `updated to
"detail-row" when the narrow (<1200px) layout has **that row's** panel
expanded` (`346a6c0`, `screen-spec.md` hunk) — so the spec does not
overclaim. Recorded as understood residue, not a deficiency.

**S4 — the exact-literal coupling class was re-pinned, not closed; the
record names the class but not its recurrence.** `a762ef0`'s
`test_model.py` hunk changes one expected literal from `'<tr
class="detail-row">…'` to `'<tr class="detail-row"
id="detail-row">…'`, which is the field's "update the literal" response
that the scout brief recorded as maintenance overhead rather than
closure (`docs/issue-61/reports/execution-observation/scout-brief.md:37-40`,
sources [11][12]). The record does name the class —
`Kind: test-coupling, not a product defect`
(`docs/issue-61/reports/implementation.md:155-156`) — but its later
entry describes the fix as `설계 결정 없음, 순수 기계적 수정`
(`a762ef0` commit message) without noting that the next markup change to
`detailRowHtml` will break the same assertion again. Per the approved
plan this is recorded as a characterization, not as a demand that the
test be rewritten.

**S5 — the proposal's frontmatter shape follows this repository's own
mixed convention; no defect.** `docs/issue-61/proposals/implementation.md:1-4`
opens with a bare `files:` list, no `---` fence and no `status:` field —
identical to `docs/issue-56/proposals/implementation.md:1-6` and
`docs/issue-44/proposals/test-authoring.md`, and different from
`docs/issue-62/proposals/implementation.md:1-3`, which uses the fenced
`status: proposed` form. Since the repository carries both shapes and
nothing downstream reads the field, the deviation reaches nothing a
later session depends on.

**S6 — the record's own accounting of the later entry is consistent in
its narrative and incomplete in its checklist.** `a762ef0`'s record hunk
adds `test/rsb_tests/test_model.py` to the frontmatter
`code_under_review` (`docs/issue-61/reports/implementation.md:2`) while
the Scope section still names the three-file frozen write set (`:64-68`)
— correct, since the write set was frozen at proposal time and the
frontmatter tracks what was ultimately touched — and marks open finding
1 `RESOLVED` with a pointer (`:164-165`). What was not updated is
`Closed checks` (`:208-221`), which still enumerates only the
three-file `code_under_review` and carries no entry for the later
entry's own verification, leaving that evidence only in the narrative at
`:178-184`. `loop_state: landed` (`:3`) matches the artifacts: `d8082dc`
merged PR #69 at 03:46:29Z. Minor, and folded into **F-1**'s action item
rather than raised separately.

---

# Findings

## F-1 — the merged mainline was never measured; issue #62's actual file overlap was not exercised

**Impact.** A later session reading the record's `67 passed, 0 failed`
(`docs/issue-61/reports/implementation.md:178-180`, repeated in
`a762ef0`'s commit message) as a statement about `main` is wrong by five
tests, and no artifact anywhere attests the tree that both merges
actually produced. The delivery's own green claims describe a branch
that never contained issue #62's concurrently-merged additions to two of
issue-61's three frozen write-set files.

**Timeline** (timestamps only, UTC).
- 02:52:17 — `a70097b` (merge of PR #53), the commit `3096092`'s parent
  points at: the branch base (`git log --format='%h parents:%p' -1
  3096092`).
- 03:23:20 — `f93c819` opens the phase-2 record; at this moment nothing
  of issue #62 is on `main` yet.
- 03:31:11 / 03:33:56 — `6887979` / `8060c5a` land issue #62, whose
  `--stat` includes `test/rsb_tests/test_dashboard_dom.py | 66 +++++-`
  and `docs/specs/screen-spec.md | 16 +-` — two of the three files in
  issue-61's frozen write set (`docs/issue-61/proposals/implementation.md:1-4`).
- 03:38:15 — `346a6c0` is authored with parent `f93c819`, i.e. still on
  the pre-#62 base; no rebase commit exists on the branch.
- 03:40:32 — `3f06ba6` merges with parents `8060c5a 346a6c0` (`git log
  --format='%h parents:%p' -1 3f06ba6`) — a textual auto-merge, not a
  rebase.
- 03:43:06 — `a762ef0` is authored with parent `346a6c0`, not `3f06ba6`
  (`git log --format='%h parents:%p' -1 a762ef0`), so the later entry's
  full-suite run also predates the merged state.
- 03:46:29 — `d8082dc` merges with parents `3f06ba6 a762ef0`.

**Root cause.** The constraint as written was conditional and aimed at
the wrong file: `병렬 진행 중인 issue #62 … 와 파일이 겹치면 phase 2 시작
시 rebase 로 조율한다` names `dashboard.js` as the predicted overlap
surface (`docs/issue-61/proposals/implementation.md:25-29`), and issue
#62's delivery did not touch `dashboard.js` at all — it touched
`test_dashboard_dom.py` and `screen-spec.md` instead (`git show --stat
6887979`). With the prediction wrong and the check written as a
one-time gate at "phase 2 시작", the actual overlap arrived after the
gate had already been passed and nothing re-fired.

**Evidence that the numbers diverge.** Static `^def test_` counts on
pinned trees (`git grep -c "^def test_" <sha> -- test/`; a static count,
not a pytest collection, so parametrization could shift it): `a762ef0` →
67 (8+6+10+10+24+5+4), exactly the record's number; `8060c5a` → 71;
`d8082dc` → 72. The five-test delta is issue #62's two
`test_dashboard_dom.py` cases and three `test_fetch.py` cases. In
mitigation, the merge preserved issue-61's own work — `git grep -c
detail-row d8082dc` returns 3 in `screen-spec.md`, 3 in `dashboard.js`,
3 in `test_dashboard_dom.py`, 1 in `test_model.py` — so there is no
evidence of a regression, only of an unattested state.

**Action item.** For the next role that lands a change while a sibling
issue is open: state the overlap check as a re-fired condition at
delivery time rather than a one-time gate at phase-2 start, and record
the post-merge suite result — or record explicitly that the merged tree
is unmeasured — in the `Closed checks` section rather than in narrative
prose. Owner-shaped target: whoever authors the next
`docs/issue-<n>/proposals/implementation.md` that carries a parallel-issue
constraint.

## F-2 — the record's own prescribed resolution path was substituted without recording the basis

**Impact.** A later session reading
`docs/issue-61/reports/implementation.md:160-163` sees a follow-up
proposal promised, and three lines later
(`:164-167`) sees a "Later entry" that never became one — with nothing
in between stating why the route changed. The mechanism it cites,
`contract s19`, is not a checked-in text in this repository (`ls
docs/specs/` → `approvers.md`, `design-system.md`, `flows-schema.md`,
`screen-spec.md`), and `grep -rn "Later entry" docs/` returns only this
record and this observation's own files, so the precedent a reader would
check against does not exist.

**Timeline.** 03:38:15 `346a6c0` records the remainder and prescribes
`a follow-up proposal with write set test/rsb_tests/test_model.py`
(`:160-163`). 03:40:32 `3f06ba6` merges. 03:43:06 `a762ef0` writes
`RESOLVED (later entry, contract s19, approval already on the issue)`
(`:164-165`) and a new `## Later entry` section (`:167-184`). 03:44:42 →
03:46:29 PR #69 opens and merges with `reviews: []` (`gh pr view 69
--json reviews`), and the issue carries no second APPROVE comment — its
three comments are `5224224718`, `5224266614`, `5224396196`.

**Root cause.** The scope-exceeded rule the record invokes at
`:139-141` ends with "the remainder becomes the next proposal", and the
record restated that as its own resolution path; when the remainder
turned out to be a single mechanical line, the cheaper route was taken
without amending the paragraph that promised the expensive one. The
authorization itself is defensible — the approval string names the
branch `issue-61/implementation` and PR #69's `headRefName` is that same
branch — so what is deficient is the silence about the substitution, not
the act.

**Action item.** When a recorded resolution path is not the one taken,
amend the paragraph that recorded it in the same commit that departs
from it, naming the authorization the substitute route relies on (here:
the branch-scoped reading of comment `5224266614`). Owner-shaped target:
the author of the next record that closes one of its own open findings
by a route other than the one it wrote down.

## F-3 — the delivered narrow-layout DOM case is narrower than the approved plan, undisclosed

**Impact.** A regression in which the narrow branch inserts an *empty*
`<tr id="detail-row">` passes the new case, because nothing in it looks
at the row's contents — the approved plan promised that assertion and
the delivered test does not carry it, and the record's deviations
section never says so.

**Timeline.** 03:18:32 `3096092` commits the plan, whose step 4 promises
`#detail-row`가 존재하고 **패널 콘텐츠를 담는 것**
(`docs/issue-61/proposals/implementation.md:110`). 03:38:15 `346a6c0`
delivers a case asserting four values — `detailSlotEmpty`,
`detailRowExists`, `ariaControls`, `resolvedId` — none of which reads the
row's content (`346a6c0`, `test_dashboard_dom.py` hunk). The record
enumerates the same four at
`docs/issue-61/reports/implementation.md:39-44` and its
`Rationale for deviations` (`:130-151`) discusses only the full-suite
deviation.

**Root cause.** The plan's step 4 packed four assertions into one
sentence and the delivery implemented the three that the acceptance
criterion names, dropping the fourth clause; because the record
described what was delivered rather than diffing it against what was
promised, the drop never surfaced as a deviation.

**Action item.** Add a content assertion to
`test_row_toggle_narrow_layout_aria_controls_resolves_to_detail_row` —
that the resolved element's `innerHTML`/`textContent` is non-empty and
carries the rendered panel — or record the omission as a deliberate
narrowing. Owner-shaped target: the role that next opens
`test/rsb_tests/test_dashboard_dom.py`; this observation neither edits
that file nor files an issue for it.

## F-4 — no warrant hunt and no skip line for the later-entry landing

**Impact.** The hunt record reads as complete for the issue while
covering only the first of two landings, so a reader cannot tell whether
the second landing was hunted and found nothing or was never hunted —
which is precisely the ambiguity the mandatory skip line exists to
remove.

**Timeline.** 03:38:15 `346a6c0` records the before-landing hunt at
`docs/issue-61/reports/implementation.md:186-206`, whose seed is named
as the three-file working-tree diff `~44 lines across 3 files, tier:
default, cap_seconds: 120`. 03:43:06 `a762ef0` lands a second time,
touching `test/rsb_tests/test_model.py` — a non-`docs/` path, so the
docs-only fast path does not apply — and adds no hunt section and no
skip line to the record.

**Root cause.** The hunt cadence is defined per proposal transition
(after-proposal, before-landing), and the later entry re-opened a
landing the record had already closed; with the unit treated as already
past its before-landing moment, the second landing inherited no
dispatch and no skip obligation in the author's reading.

**Action item.** For a later entry that touches a non-`docs/` path,
append either a hunt section or the one-line skip record naming the
reason, in the same commit as the entry — the sibling precedent
`docs/reports/2026-08-08-hunt-issue-62-implementation.md` (from
`6887979`) shows the standing-bucket form this repository already uses.
Owner-shaped target: the author of the next later entry.

## F-5 — the scout brief does not state its mode

**Impact.** A reader cannot tell from
`docs/issue-61/reports/implementation/scout-brief.md:3-6` whether the
sweep ran genuinely concurrently or was serialized, which is the one
fact the directive requires to be stated precisely because a serialized
sweep dressed up as fan-out is otherwise indistinguishable in the
output.

**Timeline.** 03:18:32 `3096092` commits the brief, which states
`WebSearch 2회(jsdom/matchMedia 커뮤니티 관례, MDN 자체 가이드) — … 2회로
종료` and lists four sources at `:66-73`, and states its survey-first
aim (`survey §7이 남긴 열린 설계 결정 … 에 대한 짧은 스카우팅`,
`:3-6`) — but never names parallel or batched-sequential.

**Root cause.** The brief reported a *search count* where the directive
asks for a *stage count and mode*; with only two searches on a
well-trodden decision the distinction reads as immaterial, and it was
omitted rather than stated as immaterial.

**Action item.** State mode and stage count in the brief's opening
lines, in the shape the sibling brief already uses
(`docs/issue-56/reports/execution-observation/scout-brief.md:3-8`:
`Mode: parallel … 2 stages total … inside the 5-stage / 3-min budget`).
Owner-shaped target: the author of the next `scout-brief.md`.

---

## Open findings

F-1 through F-5 above, all against artifacts this role does not own and
does not edit. None is a product defect: the guard, the `id`, the
`aria-controls` override, and the spec text are sound as delivered on
every surface resolvable from artifacts (Level 1, O1–O4).

### Resolution path

Each finding carries its own action item with an owner-shaped target
above. This role's authority ends at recording them: it files no issue,
edits nothing under `src/`, `test/`, `docs/specs/`, or the observed
role's `docs/issue-61/**/implementation*`, and returns these findings
only through this record on this branch's PR. The human judges them
there and, if valid, authors any issue themselves — contract v3 makes
issues user-authored only.

## Claims recorded as author-attested-only

Per admissibility rule 4, with `ls .github/workflows/` returning
`deploy-board.yml` alone so that no CI run attests any of them:
`2 failed, 7 passed` and `10 passed, 0 skipped`
(`docs/issue-61/reports/implementation.md:89-101`); `66 passed, 1
failed` (`:118-119`); `67 passed, 0 failed` (`:178-180`, and see F-1 for
which tree that number describes); `node --check` clean before and after
(`:84-85`, `:105-106`); and the completeness of the §20 API enumeration
(`docs/issue-61/proposals/implementation.md:56-63`). None of these is
contradicted by any artifact; none is independently verified either.

## Next steps

None for this role — this record is issue #61's step 2 and its last
planned artifact. The issue's own execution plan, its final body update,
and any merge are the orchestrator's and the human's acts, not this
role's; this record's PR body carries a flat `#61` reference and no
closing keyword.

`loop_state` transitions: `observing` (`fd88189`) → `landed` (this
commit).
