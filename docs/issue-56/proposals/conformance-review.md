# Conformance-review proposal (issue #56)

Scope: score the merged delivery of issue #56 — PR #57
(`issue-56/implementation`), delivery commit `21c2359`, merged as
`93a60b3` — against issue #56's own text: its four `check:` acceptance
lines, its three 요구사항, and its one 제약. One verdict per requirement
row, from the artifact and the specification only. This role does not
fix, does not re-decide the design, and does not render a holistic
code-quality judgment; findings hand off to the owning role.

Current-state survey: `docs/issue-56/reports/conformance-review/survey.md`.
Scout brief: `docs/issue-56/reports/conformance-review/scout-brief.md`.

## Method

**Sampling derivation: none — full census.** `git show --stat 21c2359`
is 6 files, and 5 of them map 1:1 onto the four acceptance checkboxes
(the sixth is the building role's own record). Every requirement in the
issue therefore gets its own row set; nothing is sampled and nothing is
representative-of.

**Verdicts.** `verdict ∈ {Present, Surface, Absent, Incorrect,
Unverifiable}`, per the `finding-record` skill. *Present* — the
requirement is met on located evidence. *Surface* — the named artifact
exists but does not do what the requirement asks of it. *Absent* — no
artifact answers the requirement. *Incorrect* — an artifact exists and
is wrong about the thing the requirement specifies. *Unverifiable* — the
evidence that would settle it cannot be produced in this environment;
recorded as an open request, never rounded to a pass. Non-`Present`
verdicts are bolded in the cell, per house form.

**Severity**, applied to non-`Present` rows only, by the same four-band
lookup the issue-38 and issue-36 records use: **Blocking** (an
acceptance checkbox is unmet as written) / **Major** (user-visible or
requirement-defeating, reachable in a default scenario) / **Minor**
(narrow or non-default path) / **Note** (record or hygiene only).

**Evidence classes**, declared here so each row's evidence is readable
as a class rather than argued case by case:

- **A** — readable in the artifact at `21c2359` or current `main`:
  file:line in `src/`, `test/`, or `docs/specs/`.
- **B** — produced by executing something this session: `grep`,
  `node --check`, a `pytest` run, `gh` API state. Every B row's command
  and verbatim output goes into the record's Appendix.
- **C** — needs a rendering/layout engine. None exists here (no Chrome/
  Chromium, no Playwright/Selenium/Puppeteer —
  `docs/issue-38/reports/implementation.md:104-123`). C rows resolve to
  **Unverifiable** with a named settling artifact, never to an inferred
  pass and never to a fail.

**Harness.** `test/node_modules/` is absent, and
`test/rsb_tests/test_dashboard_dom.py` skips its whole module without
jsdom. Phase 2 runs `npm install --prefix test` first, following
`docs/issue-36/reports/conformance-review.md` Appendix A1, so that the
acceptance-check-1 rows are settled by execution rather than left
Unverifiable for want of a harness. If the install fails offline, the
affected rows become Unverifiable and say so.

**Mutant-kill probe (R1f only).** Assertion *power* is checked by
restoring `renderErrors` and its call site in a throwaway copy of
`dashboard.js` outside the repository tree, re-running the one new test,
and recording whether it fails. The probe file is deleted after the run
and is never committed — the same shape as
`docs/issue-36/reports/conformance-review.md` Appendix A4. No `src/` or
`test/` file in this branch is modified at any point.

**Regression baseline, carried in as settled.** `main` currently fails 2
tests in `test_dashboard_dom.py`. That is the pre-existing unguarded
`window.matchMedia` defect introduced by `f353910`, whose attribution is
already established in `docs/issue-36/reports/conformance-review.md`
finding F1 (`:196-221`) and Appendix A4 (`:441-471`). This review cites
that attribution and does not re-derive it; the only open question is
whether `21c2359` changed the count.

**Yardstick independence.** The yardstick is issue #56's text plus the
`docs/specs/` files the acceptance lines name.
`docs/issue-56/reports/implementation.md` is read for *claims to
re-verify* (S8) and never as evidence that the thing it claims is
conformant; the building role's stated intent does not enter any
verdict. Where a requirement makes a record's content the object of the
check (S2), that record is evidence for that row only.

## Requirement list

**R1 — `test/rsb_tests/test_dashboard_dom.py` 에 partial-failure 문서-범위
단언 테스트 추가·통과** (acceptance checkbox 1; 요구사항 3 second clause).

- R1a: a new test exists in that file exercising the partial-failure
  render path. Method: read the diff hunk. [A]
- R1b: the assertion is **문서-범위** as the checkbox words it — its DOM
  scope covers the places a regression could reappear. Method: compare
  the test's scope root against `src/rsb/web/index.html`'s structure,
  where `#partial-banner` (`:20`) is a *sibling* of `#main-content`
  (`:24`), and against the test's own in-file claim that it is document-
  scoped. [A]
- R1c: the assertion "실패 repo raw 메시지가 접히지 않은 채 등장하지 않는다"
  is present and discriminates *uncollapsed* exposure from the collapsed
  `<details>` the banner legitimately retains. [A]
- R1d: the assertion "renderErrors 가 만들던 Errors 섹션이 부재" is
  present. [A]
- R1e: the test passes on a fresh run. [B, after the jsdom install]
- R1f: the assertion has power — restoring `renderErrors` + its call site
  makes this test fail. Method: the mutant-kill probe above. [B]
- R1g: exactly one new test on the new surface, as 요구사항 3 asks
  ("신규 표면에 대한 테스트 1건"). [A]

**R2 — `src/rsb/web/dashboard.js` 에서 renderErrors 함수·호출부
제거(grep 0건)** (acceptance checkbox 2; 요구사항 1).

- R2a: the `renderErrors` function definition is gone. [A]
- R2b: the `${renderErrors(data.errors)}` interpolation in `renderData`'s
  `MAIN.innerHTML` template is gone. [A]
- R2c: `grep -rn renderErrors src/` returns zero matches. [B]
- R2d: the removal is surgical — the remaining template's section order
  and content are otherwise unchanged. Method: read the diff hunk for
  collateral edits. [A]
- R2e: `data.errors` is still consumed by the banner path, so the removal
  orphaned no payload field and changed no other reader of it. [A]

**R3 — `src/rsb/web/dashboard.css` 의 `.number-link` 에 24×24px 최소
크기(`.row-toggle` 패턴) 적용** (acceptance checkbox 3; 요구사항 2
parenthetical).

- R3a: `min-width: 24px` and `min-height: 24px` are declared on
  `.number-link`. [A]
- R3b: the element's box type honors them — `display: inline-flex`, as
  `.row-toggle` (`dashboard.css:212-228`) does. [A]
- R3c: pattern fidelity — which of `.row-toggle`'s declarations were
  carried over and which were not, and whether any omission bears on the
  24×24 guarantee. The checkbox names the pattern, so partial adoption is
  a real question, not a stylistic one. [A]
- R3d: the rule reaches both DOM contexts `.number-link` renders in —
  inside `.issue-cell` (`dashboard.js:243`), itself `display: inline-flex`
  so the link becomes a flex item, and inside `<span class="mono">`
  (`:254`). [A for the structure]
- R3e: the rendered box is actually ≥ 24×24 CSS px in both contexts. [C]
- R3f: the sizing introduces no adjacent-target regression inside
  `.issue-cell` (the `.row-toggle` + `.number-link` pair, `white-space:
  nowrap`, `gap: var(--space-1)`). [C, with the A-class structural facts
  recorded alongside]

**R4 — `docs/specs/screen-spec.md` §1.9 삭제 + §2.5 에 유일 표시 지점
명시, `design-system.md` 24px 목록 편입** (acceptance checkbox 4).

- R4a: `### 1.9 Errors panel — ErrorListItem` and its bullets are
  removed. [A]
- R4b: §2.5 states the partial-failure banner is the only surface that
  displays partial-failure repo errors. [A]
- R4c: no dangling reference to §1.9 or to the Errors panel survives
  anywhere in `docs/specs/` or `src/`. [B]
- R4d: `design-system.md`'s 24px **목록** now includes `.number-link` —
  judged against §5's enumeration of controls that "guarantee a 24×24px
  minimum touch target", not only against added prose. [A]
- R4e: §6's `DataTable` inventory row records the 24×24 for
  `.number-link`. [A]
- R4f: `design-system.md:189`'s `| ErrorListItem | status-error |`
  inventory entry, whose only `screen-spec.md` home was the §1.9 this
  change deleted. [A]
- R4g: spec and code agree after the change — no clause anywhere in
  `docs/specs/` still specifies a surface the code no longer renders.
  This is the standing conflict issue #38's conformance record raised as
  its Blocking finding; the checkbox exists to close it. [A]

## Requirements traceable to the issue body, not to an acceptance checkbox

- S1 (요구사항 1, second clause): the "통합/제거" judgment was actually made
  **in the proposal**, with the duplication argument stated, rather than
  performed silently in phase 2. Method: read
  `docs/issue-56/proposals/implementation.md` at `71a0dff`. [A]
- S2 (요구사항 2, first clause): "**실측**해 기록으로 보고" — a measurement
  was performed and reported; if a source-based determination was
  substituted, whether the substitution is disclosed **for this
  criterion** rather than only globally. This is precisely the deficiency
  shape issue #38 F3 named (`docs/issue-38/reports/execution-observation.md:320-334`),
  so a repeat of it is in scope. [A]
- S3 (요구사항 2, parenthetical): the determination's outcome and the CSS
  follow-through are consistent with each other and with WCAG 2.5.8's
  normative Inline exception text ("The target is in a sentence or its
  size is otherwise constrained by the line-height of non-target text").
  [A]
- S4 (요구사항 3, first clause): 기존 테스트 무회귀 — the suite result at
  `21c2359` versus its parent, with the 2 `test_dashboard_dom.py`
  failures cited to the settled `f353910` `matchMedia` attribution rather
  than re-litigated. [B]
- S5 (제약): "PR #43 이 랜딩한 나머지 8개 AC 구현은 무변경" — every hunk in
  `21c2359` belongs to one of issue #56's own four surfaces, and no
  element, attribute, or rule owned by another of PR #43's acceptance
  criteria is edited. Method: walk the diff hunk by hunk against issue
  #38's AC1-AC9. [A]
- S6: removal residue in CSS — `.error-list` rules (`dashboard.css:347-349`)
  and their `/* HygieneListItem / ErrorListItem */` comment header outlive
  the only producer that emitted that class. [A]
- S7: the substantive form of issue #38 F1, wider than R1's assertions —
  after the change, no always-visible surface anywhere in the rendered
  document prints a raw per-repo error message. Method: enumerate every
  writer of `data.errors` into the DOM. [A/B]
- S8: the factual claims in `docs/issue-56/reports/implementation.md` that
  this review depends on — the test counts, the `node --check` result,
  the grep results — reproduce when re-run. [B]

## How this will be judged

Externally checkable completion conditions for phase 2:

- Every row above carries exactly one verdict from the five-value set,
  with file:line or verbatim command output as evidence, and an evidence
  class.
- Every non-`Present` row carries a severity band and appears in the
  record's `## Open findings`, addressed to the owning role by name.
- Every `Unverifiable` row appears in a `| Row | What would settle it |`
  table naming the artifact that would settle it.
- The record's row set reconciles against this list; if a row is split or
  added, a row-count note says so and no row from this list is dropped.
- No `src/`, `test/`, or `docs/specs/` file differs on this branch.

## Out of scope for this role

- Fixing anything found, or proposing the fix's design. Findings hand off.
- Trajectory, process, and phase-gate judgment on PR #57 — the sibling
  `execution-observation` role's territory under the same 실행 계획 step.
- Re-deriving the `f353910` `matchMedia` attribution, settled in
  `docs/issue-36/reports/conformance-review.md` F1 / Appendix A4 and
  cited here.
- Holistic code-quality opinion on `dashboard.js` or `dashboard.css`
  beyond the rows above.
- Anything belonging to PR #43's other eight acceptance criteria, except
  as the S5 no-change check requires.

## Phase-2 deliverable

One file: `docs/issue-56/reports/conformance-review.md`, holding the
per-requirement verdicts for R1a–R4g and S1–S8, an `## Open findings`
section, an `## Unverifiable rows and what would settle each` table, an
`## Open-finding resolution path`, and an appendix of verbatim commands
and output for every B-class row.

Per contract v3 s19 this proposal is the whole of phase 1. Phase 2 opens
only on an Approve from a `docs/specs/approvers.md` account — a PR review
Approve from an account other than this PR's author, or, in
single-account mode, an issue-level comment whose entire body is exactly
`APPROVE issue-56/conformance-review`. No prose is read as approval.

## Warrant hunt

After-proposal dispatch, stance 0, 60s tier (docs-only write set).
Outcome: **FINDING**, recorded in
`docs/issue-56/reports/conformance-review/hunt.md`. It is not a defect in
this requirement list and changes no row above: it observes that the
approval gate's *mode* is inferred after the fact from whether a PR
review happens to exist, so an author who is also a listed approver can
route the gate into single-account mode by simply not filing one —
which is how both prior phase-2 gates on issue #56 opened
(`APPROVE issue-56/implementation`, `APPROVE issue-56/execution-observation`,
both authored by PR #57's own author, with `gh pr view 57 --json reviews`
returning `{"reviews":[]}` and the second `approvers.md` account never
involved). The mode rule lives in contract v3 s19 and the roster lives in
`docs/specs/approvers.md`; neither is in this role's write set, so the
finding is surfaced to the user and left unfixed. It does not license
this role to read approval any more loosely: the string test above stands
exactly as written.

Docs-only fast path: no before-landing dispatch for this landing.
