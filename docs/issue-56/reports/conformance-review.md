# Conformance review — issue #56 vs PR #57 (33 requirement rows)

reviewed_artifact: PR #57 <https://github.com/tokenmaxxxer/repo-status-board/pull/57>,
delivery commit `21c2359`, merged 2026-08-08T02:39:24Z as `93a60b3`
specification: issue #56's own text — its four `check:` acceptance lines,
its three 요구사항, its one 제약 — plus the `docs/specs/` files those
lines name
requirement list: `docs/issue-56/proposals/conformance-review.md`,
approved unchanged; 33 rows, full census, no sampling
code_under_review: none — this role authors no code. The artifacts
scored are `21c2359`'s five non-record files and the two `docs/specs/`
files its acceptance lines name.
loop_state: landed
loop_state transitions: `auditing` (this record created as the first act
of phase 2, before any verdict was written) → `landed` (33 verdicts
rendered, six findings recorded, committed on
`issue-56/conformance-review`).

## Why

Issue #56 exists to close two gaps issue #38's execution-observation
record left open — its F1 (the untouched third error surface
`renderErrors`, `docs/issue-38/reports/execution-observation.md:247-261`)
and its F3 (the `.number-link` 실측 promised by
`docs/issue-38/proposals/implementation.md:310-312` and never reported,
`:320-334`). That is the concrete upstream basis for the specification
scored below; issue #56's 배경 section quotes both. Its 실행 계획 step 2
is `execution-observation ‖ conformance-review`; this is the
conformance half.

Phase 2 opened through contract v3 s19's single-account path: issue #56
comment
<https://github.com/tokenmaxxxer/repo-status-board/issues/56#issuecomment-5224181226>,
author `jjongkwann` (listed in `docs/specs/approvers.md`), body exactly
`APPROVE issue-56/conformance-review` and nothing else. String equality
was checked against the raw body read this session
(`gh issue view 56 --json comments`, Appendix A6), not inferred from
prose. `gh pr list --state all` shows PR #63's author is the same
account, so single-account mode is the applicable path. **No near-miss
exists and that is stated here rather than left to inference:** issue #56
carries exactly three comments, all exact-string `APPROVE
issue-56/<role>` lines for three different roles, and no
affirmative-sounding prose comment exists anywhere on the issue that
could be mistaken for approval.

The account-identity limit on what this approval demonstrates is the
same one the phase-1 warrant hunt recorded
(`docs/issue-56/reports/conformance-review/hunt.md`): the gate's *mode*
is inferred after the fact from whether a PR review happens to exist, so
an author who is also a listed approver can route the gate into
single-account mode by not filing one. That finding is out of this
role's write set and is surfaced, not fixed; it licenses no looser
reading of the string test above.

## What was done

Executed `docs/issue-56/proposals/conformance-review.md` as approved, row
for row, with no change to the requirement list and no sampling.

Artifacts opened first-hand this session, none taken from a summary:

1. Issue #56's body and all three comments, with exact bodies and
   permalinks (`gh issue view 56`, `gh issue view 56 --json comments`).
2. `docs/specs/approvers.md`, and PR state for every branch on the board
   (`gh pr list --state all --json number,title,headRefName,author,url`).
3. `21c2359` in full — commit message, `git show --stat`, and the
   complete diff for all five non-record files.
4. The merged tree at `93a60b3` / current `main` for every file a row
   cites: `src/rsb/web/dashboard.js`, `src/rsb/web/dashboard.css`,
   `test/rsb_tests/test_dashboard_dom.py`, `docs/specs/screen-spec.md`,
   `docs/specs/design-system.md`.
5. `docs/issue-56/proposals/implementation.md` (row S1) and
   `docs/issue-56/reports/implementation.md` in full (rows S2, S8).
6. `docs/issue-56/reports/execution-observation.md`, merged as `c005cb2`
   — read for its two findings, which are cited below and not
   re-investigated.

Executed this session, all recorded verbatim in the Appendix: the jsdom
harness install (A1); the suite on the delivered tree and on a
parent-equivalent baseline tree (A2); a four-cell mutant-kill probe on
two throwaway trees outside the repository (A3); the record's own three
greps plus four residue/enumeration sweeps (A4); `node --check` (A5).

Then: one verdict per row for R1a–R4g and S1–S8, a row-count
reconciliation, six findings addressed to the owning role, a settling
table for the two `Unverifiable` rows, and this record's own hunt
section.

## Independence of the yardstick

The yardstick is issue #56's text plus the `docs/specs/` files its
acceptance lines name. `docs/issue-56/reports/implementation.md` — the
building role's own record — is read only for **claims to re-verify**
(row S8) and, for row S2, as the object of a check that is *about* a
record's content; it is never evidence that the thing it claims is
conformant, and the building role's stated intent enters no verdict.

This role wrote nothing under `src/`, `test/`, or `docs/specs/` in
either phase. `git status --short` on this branch shows one untracked
path, `test/node_modules/`, created by the harness install in Appendix
A1 and not committed.

Two findings already recorded by the sibling `execution-observation`
role on the same 실행 계획 step
(`docs/issue-56/reports/execution-observation.md`, merged as `c005cb2`)
are **cited, not re-derived**: its F1 (`ErrorListItem` surviving as a
dead reference at `design-system.md:189` and `dashboard.css:347`) and
its F2 (no `after-proposal` hunt section in the building role's record).
F2 is trajectory-class and belongs to that role; it appears here only as
a citation. Rows R4f, R4g and S6 below reach the same artifacts F1
names, and each says so rather than re-arguing the case.

## Method as approved

Verdicts are `Present | Surface | Absent | Incorrect | Unverifiable`,
defined at `docs/issue-56/proposals/conformance-review.md` "Method". Non-
`Present` verdicts are bolded. Severity, applied to non-`Present` rows
only: **Blocking** (an acceptance checkbox unmet as written) / **Major**
(user-visible or requirement-defeating in a default scenario) / **Minor**
(narrow or non-default path) / **Note** (record or hygiene only).

Evidence classes: **A** — readable in the artifact at `21c2359` or
current `main`. **B** — produced by executing something this session;
every B row's command and verbatim output is in the Appendix. **C** —
needs a rendering/layout engine, of which none exists here; C rows
resolve to **Unverifiable** with a named settling artifact, never to an
inferred pass and never to a fail.

`Unverifiable` rows carry severity **Note** by construction: they assert
no defect, only an evidence gap, and they are handed off as open
requests rather than absorbed as passes.

## Verdicts — R1 (acceptance checkbox 1: partial-failure 문서-범위 단언 테스트)

| Row | Requirement | Verdict | Sev | Cls | Evidence |
|---|---|---|---|---|---|
| R1a | a new test exists exercising the partial-failure render path | Present | — | A | `test/rsb_tests/test_dashboard_dom.py:258-278`, one function on the partial-failure payload; the banner branch it reaches is `src/rsb/web/dashboard.js:586-598` |
| R1b | the assertion's DOM scope root covers where a regression could reappear | Present | — | A | scope root is `#main-content` (`:265`), which is exactly the element `renderErrors`' output was interpolated into (`MAIN`, `dashboard.js:7`, template at `:607`). The root is right; its *reach* under this payload is row R1f |
| R1c | the assertions discriminate *uncollapsed* exposure from the collapsed `<details>` the banner legitimately retains | **Surface** | Minor | A | the fourth assertion is `document.getElementById("partial-banner").innerHTML.includes(...)` (`:270`, asserted `is True` at `:278`) under the name `bannerHasCollapsedMessage`. `innerHTML.includes` is satisfied by the string appearing anywhere in the banner's markup, collapsed or not: it never inspects the `<details>` element `collapsibleDetailHtml` (`dashboard.js:462`, called at `:591`) produces, and never checks for the absence of an `open` attribute. The named artifact exists; it does not test the property its own name claims. See CR-F2 |
| R1d | the assertion "renderErrors 가 만들던 Errors 섹션이 부재" is present | Present | — | A | `:268-269` / `:276-277` — no `<h2>` with text `Errors`, no `.error-list` node. Present as written; its power is row R1f |
| R1e | the test passes on a fresh run | Present | — | B | Appendix A2 — `64 passed, 2 failed`, the new test among the 64 |
| R1f | the assertion has power — restoring `renderErrors` + its call site makes this test fail | **Incorrect** | Major | B | Appendix A3, four-cell probe. With `renderErrors` and its call site restored verbatim from `71a0dff`, the committed test **still passes** (`1 passed`). Cause, located at `dashboard.js:88-96` and `:600-605`: the test's payload leaves all seven lists `isPageEmpty` reads empty, so `renderData` returns at the empty-state branch *before* reaching the template `${renderErrors(data.errors)}` lived in. Disabling only that early return flips the same test to `1 failed` against the restored `renderErrors`, and leaves it passing against the delivered code — so the three negative assertions are vacuous under the payload as committed. See CR-F1 |
| R1g | exactly one new test on the new surface (요구사항 3, "신규 표면에 대한 테스트 1건") | Present | — | A | `21c2359` adds `+33 −0` to that file, one `def test_...` (`:258`) plus its 8-line provenance comment (`:248-255`) |

## Verdicts — R2 (acceptance checkbox 2: `renderErrors` 함수·호출부 제거)

| Row | Requirement | Verdict | Sev | Cls | Evidence |
|---|---|---|---|---|---|
| R2a | the `renderErrors` function definition is gone | Present | — | A | `git show 21c2359 -- src/rsb/web/dashboard.js` deletes the whole `:355-365` block; nothing at that site now |
| R2b | the `${renderErrors(data.errors)}` interpolation in `renderData`'s `MAIN.innerHTML` is gone | Present | — | A | same hunk removes the single line formerly at `:632`, between the Sessions and Hygiene sections |
| R2c | `grep` for `renderErrors` returns zero matches in the file the checkbox names | Present | — | B | Appendix A4 — `grep -rn "renderErrors" src/` returns nothing. One text hit survives repo-wide, at `test/rsb_tests/test_dashboard_dom.py:252`, inside the new test's own provenance comment; the checkbox scopes itself to `src/rsb/web/dashboard.js`, where the count is zero |
| R2d | the removal is surgical — remaining template order and content otherwise unchanged | Present | — | A | `git show --numstat 21c2359` records `dashboard.js` as `0 13`: a pure deletion, no compensating hunk. Render order Decision queue → Flows → Sessions → Hygiene → Accounting is intact at `:607` onward |
| R2e | `data.errors` is still consumed by the banner path; the removal orphaned no payload field | Present | — | A | five surviving readers of `data.errors`: `dashboard.js:84` (summary chip count), `:116` (`filterByRepo`), `:130` (`repoList`), `:565-566` (total-failure branch), `:570-571` and `:585-596` (header count and banner). None was edited by `21c2359` |

## Verdicts — R3 (acceptance checkbox 3: `.number-link` 24×24px, `.row-toggle` 패턴)

| Row | Requirement | Verdict | Sev | Cls | Evidence |
|---|---|---|---|---|---|
| R3a | `min-width: 24px` and `min-height: 24px` declared on `.number-link` | Present | — | A | `src/rsb/web/dashboard.css:255-256`, inside the `.number-link` block opened at `:248` |
| R3b | the element's box type honors them — `display: inline-flex`, as `.row-toggle` does | Present | — | A | `dashboard.css:257` vs `.row-toggle`'s `:225`. `min-height` has no effect on a non-replaced inline box; `inline-flex` makes the link a block container in an inline formatting context, where both minima apply |
| R3c | pattern fidelity — which of `.row-toggle`'s declarations were carried over, and whether any omission bears on the 24×24 guarantee | Present | — | A | `.row-toggle` (`:212-228`) carries twelve declarations; `.number-link` adopted the five that constitute the touch-target pattern (`min-width`, `min-height`, `display`, `align-items`, `justify-content`, `:255-259`) and omitted seven — `background: none`, `border: none`, `font: inherit`, `color: inherit`, `cursor: pointer`, `padding: 0`, `text-align: left` (`:213-219`). All seven are `<button>`-chrome resets: an `<a>` has no UA background, border, or padding to reset, inherits `font`/`text-align` already, and gets `cursor: pointer` from the UA for an `href`-bearing anchor. `.number-link` sets its own `color` deliberately (`:249`). No omission touches the box minima |
| R3d | the rule reaches both DOM contexts `.number-link` renders in | Present | — | A | context 1, inside `.issue-cell` — `dashboard.js:243`, and `.issue-cell` is `display: inline-flex` (`dashboard.css:237-242`), so the link is a flex item whose own minima still apply and whose cross-axis is `align-items: center`, not `stretch`. Context 2, inside `<span class="mono">` — `dashboard.js:254`, and `.mono` sets only `font-family` (`dashboard.css:84`). The two `:hover`/`:focus` rules (`dashboard.css:261-265`) touch `text-decoration`/`outline` only; no other rule in the file sets `display`, `min-width` or `min-height` on this selector or either ancestor |
| R3e | the rendered box is actually ≥ 24×24 CSS px in both contexts | **Unverifiable** | Note | C | no layout engine exists in this environment — no Chrome/Chromium, no Playwright/Selenium/Puppeteer (`docs/issue-38/reports/implementation.md:104-123`). The A-class facts in R3a-R3d are what is established; the rendered geometry is not. See CR-F5 and the settling table |
| R3f | no adjacent-target regression inside `.issue-cell` after the sizing change | **Unverifiable** | Note | C | structural facts on record: `.issue-cell` sets `gap: var(--space-1)` and `white-space: nowrap` (`dashboard.css:240-241`), and both children now declare a 24×24 minimum (`.row-toggle` `:223-224`, `.number-link` `:255-256`), so on the declared boxes the pair cannot overlap. Whether the widened link changes the pair's laid-out spacing, or pushes the issue column against `table.data-table`'s `min-width: 640px` overflow behaviour, needs the same absent engine. See CR-F6 |

## Verdicts — R4 (acceptance checkbox 4: screen-spec §1.9 삭제 + §2.5 명시, design-system 24px 목록 편입)

| Row | Requirement | Verdict | Sev | Cls | Evidence |
|---|---|---|---|---|---|
| R4a | `### 1.9 Errors panel — ErrorListItem` and its bullets removed | Present | — | A | `git show 21c2359 -- docs/specs/screen-spec.md` deletes the five-line block; `grep -n "ErrorListItem" docs/specs/screen-spec.md` returns nothing (Appendix A4) |
| R4b | §2.5 states the banner is the only surface displaying partial-failure repo errors | Present | — | A | `docs/specs/screen-spec.md:209-213`. The sentence is scoped to *partial-failure* errors, which is what makes it true alongside `renderFullError`'s total-failure output at `dashboard.js:565-566` — a different branch, itself routed through the same collapsed `collapsibleDetailHtml` |
| R4c | no dangling reference to §1.9 or to the Errors panel survives in `docs/specs/` or `src/` | Present | — | B | Appendix A4 — the only `Errors panel` hit repo-wide is `screen-spec.md:213`, inside the new §2.5 sentence that describes the removal. No `§1.9` cross-reference anywhere |
| R4d | `design-system.md`'s 24px **목록** now includes `.number-link`, judged against §5's enumeration of controls guaranteeing a 24×24px minimum | **Surface** | Note | A | §5's enumerating parenthetical still reads "every interactive control (`row-toggle`, `repo-filter`, `refresh-button`) now guarantees a 24×24px minimum touch target" (`docs/specs/design-system.md:163-165`); the `.number-link` extension arrives as a separate following sentence (`:167-170`) rather than as a fourth entry in that list, so the list a reader greps still enumerates three. The added prose does state the guarantee. The sibling `execution-observation` record reached the same reading independently (its O7, "a legibility nit, not an unmet AC") and this row concurs rather than restating it. See CR-F4 |
| R4e | §6's `DataTable` inventory row records the 24×24 for `.number-link` | Present | — | A | `docs/specs/design-system.md:182` — "…trailing `#<n>` link (`.number-link`, …, 24×24px minimum size per issue #56 F3)". On this row the checkbox's "목록 편입" is satisfied on any reading |
| R4f | the `ErrorListItem` inventory entry, whose only `screen-spec.md` home was the deleted §1.9 | **Surface** | Note | A | `docs/specs/design-system.md:189` still carries `\| ErrorListItem \| status-error \|` while §6's own preamble says components are "applied per-region in `docs/specs/screen-spec.md`" (`:174`) and the only region applying it was deleted by the same commit. **This is `docs/issue-56/reports/execution-observation.md` finding F1 and is cited, not re-derived**; the conformance-side consequence is that this row's artifact exists but no longer does what the requirement asks of it. See CR-F3 |
| R4g | spec and code agree after the change — no clause in `docs/specs/` still specifies a surface the code no longer renders | **Surface** | Minor | A/B | the standing conflict issue #38's conformance record raised as Blocking is closed for the *panel* — §1.9 is gone and no code renders it — but not closed for the *component*: `design-system.md:189` remains a normative inventory entry for a component with no region and no emitter, and `src/rsb/web/dashboard.css:347`'s header still reads `/* HygieneListItem / ErrorListItem */` over selectors whose only surviving producer is `.hygiene-list` (Appendix A4). Same artifacts as execution-observation F1, cited. The checkbox's four named edits all landed; what is Surface is the wider agreement claim this row states. See CR-F3 |

## Verdicts — S1–S8 (요구사항 / 제약 traceable to the issue body, not to a checkbox)

| Row | Requirement | Verdict | Sev | Cls | Evidence |
|---|---|---|---|---|---|
| S1 | 요구사항 1's "통합/제거" judgment was actually made **in the proposal**, with the duplication argument stated | Present | — | A | `docs/issue-56/proposals/implementation.md:39-55` at `71a0dff`: states that every reachable state producing non-empty `renderErrors` output is one where the banner already rendered the identical `{repo}: {message}` pairs in a collapsed `<details>`, names the keep-and-collapse alternative, and rejects it on a stated single-source-of-truth ground. The judgment is on the record before the phase-2 commit, not performed silently inside it |
| S2 | 요구사항 2's "**실측**해 기록으로 보고" — a measurement performed and reported; if substituted, the substitution disclosed **for this criterion** | Present | — | A | no rendered-pixel measurement exists, and the record says so *at the criterion*, not only in a global constraints list: `docs/issue-56/reports/implementation.md:90-97` names the substitute (jsdom `getComputedStyle` against the shipped CSS), names the reason (no browser binary, `ModuleNotFoundError` for playwright), and labels it a planned substitution traceable to the approved proposal. That per-criterion disclosure is exactly what issue #38 F3 found missing (`docs/issue-38/reports/execution-observation.md:320-334`), and it is present here. The substitute's own execution is author-attested and not reproducible in this session — recorded under S8, not silently folded into this row |
| S3 | the determination's outcome and the CSS follow-through are consistent with each other and with WCAG 2.5.8's normative Inline exception text | Present | — | A | the exception reads "The target is in a sentence or its size is otherwise constrained by the line-height of non-target text". Neither `.number-link` context contains non-target prose: `dashboard.js:243` pairs it with a `.row-toggle` button inside `.issue-cell`, and `:254` makes it the sole content of a `<span class="mono">`. 판정 = 불성립 (`docs/issue-56/reports/implementation.md:60-61`), which triggers 요구사항 2's parenthetical, and the CSS at `dashboard.css:255-259` applies the minimum. Determination, parenthetical and code agree |
| S4 | 기존 테스트 무회귀 — the suite at `21c2359` versus its parent | Present | — | B | Appendix A2: parent tree `63 passed, 2 failed`; delivered tree `64 passed, 2 failed`. Delta is exactly the one added test, no new failure. The two failures are the same two in both runs and are cited to the settled `f353910` unguarded-`matchMedia` attribution (`docs/issue-36/reports/conformance-review.md` F1 `:196-221`, Appendix A4 `:441-471`), not re-derived here |
| S5 | 제약 — "PR #43 이 랜딩한 나머지 8개 AC 구현은 무변경" | Present | — | A | `git show --numstat 21c2359` lists six files: `dashboard.js` `0 13` (the two `renderErrors` hunks only), `dashboard.css` `9 0` (every added line inside the `.number-link` block, `:251-259`), the two spec files at the §1.9/§2.5 and §5/§6 sites, the new test, and the building role's own record. No element, attribute, or rule owned by PR #43's other eight ACs is edited. Recorded boundary, not a defect: `.number-link` widening from its former inline box to a 24px minimum is a geometric change inside a table cell that AC1's `min-width: 640px` overflow behaviour also concerns — the *implementation* of AC1 is untouched, but the laid-out interaction is C-class and is covered by R3f |
| S6 | removal residue in CSS — `.error-list` rules and their comment header outliving the only producer that emitted that class | **Surface** | Note | A | `src/rsb/web/dashboard.css:347` header `/* HygieneListItem / ErrorListItem */` over `:348-349`, whose selectors are shared with `.hygiene-list` and therefore correctly retained; only the name in the header is stale. Repo-wide, the sole surviving non-CSS `error-list` occurrence is the new test's own negative assertion (`test/rsb_tests/test_dashboard_dom.py:269`), Appendix A4. Same artifact as execution-observation F1, cited. See CR-F3 |
| S7 | the substantive form of issue #38 F1 — after the change, no always-visible surface anywhere in the rendered document prints a raw per-repo error message | Present | — | A/B | every writer of `data.errors` into the DOM, enumerated from `grep -n "errors" src/rsb/web/dashboard.js` (Appendix A4): `:571` header meta writes a **count** only; `:84` summary chip a **count** only; `:130` `repoList` writes repo **names** into the filter `<select>`, never messages; `:565-566` total-failure passes the joined pairs to `renderFullError`, which wraps them in `collapsibleDetailHtml` (`:165`, `:462`) — collapsed, escaped; `:585-596` partial-failure wraps the joined pairs in the same helper (`:591`). No always-visible raw message path remains. The removed `renderErrors` was the last one |
| S8 | the factual claims in `docs/issue-56/reports/implementation.md` this review depends on reproduce when re-run | Present | — | B | test counts reproduce exactly — `64 passed, 2 failed`, same two failing names (Appendix A2). `node --check src/rsb/web/dashboard.js` exits 0 (Appendix A5). All three greps reproduce with the scopes the record states (Appendix A4), including the record's own advance disclosure that the `renderErrors` sweep leaves one comment-text hit. Not reproducible and therefore *not* relied on by any verdict above: the record's jsdom `getComputedStyle` run (`:36-39`, `:177-178`) and its two hunt repros, none of which were committed — R3e/R3f are Unverifiable rather than resolved by those claims |

## Row-count reconciliation

33 rows in, 33 rows out — R1a–R1g (7), R2a–R2e (5), R3a–R3f (6),
R4a–R4g (7), S1–S8 (8). No row from the approved list was split, merged,
added or dropped.

Tally: **25 Present, 5 Surface, 1 Incorrect, 2 Unverifiable, 0 Absent.**

All four acceptance checkboxes are met as written. Every non-`Present`
verdict falls either on a derived row the checkboxes do not restate
(R1c, R1f, R4d, R4g, S6) or on the residue row the sibling record
already named (R4f).

## Open findings

Six, addressed to the **implementation** role. This role does not fix
them, does not edit the target artifacts, and does not open issues
(contract v3: issues are user-authored only).

### CR-F1 — the new regression test has no power against the regression it names. Major. Row R1f

The test at `test/rsb_tests/test_dashboard_dom.py:258-278` passes
unchanged against a `dashboard.js` in which `renderErrors` and its call
site are fully restored (Appendix A3, cell 2: `1 passed`). Its payload
`_board_payload(generated_at_by_repo={...}, errors=[...])` leaves
`decisions`, `flows`, `sessions`, `ledger`, `unattributed`,
`closure_sweep` and `unapproved_open_prs` all empty, which is exactly
`isPageEmpty`'s condition (`src/rsb/web/dashboard.js:88-96`); `renderData`
therefore takes the empty-state early return at `:600-605` and never
evaluates the template at `:607` that `${renderErrors(data.errors)}` was
interpolated into. `#main-content` holds one `.empty-state` div, so
`mainContentHasRawMessage is False`, `errorsHeadingExists is False` and
`errorListExists is False` are true of *any* implementation, correct or
regressed.

The 2×2 probe isolates the cause: disabling only the early return makes
the same test fail against restored `renderErrors` (Appendix A3, cell 4)
and still pass against the delivered code (cell 3). So the vacuity is
the payload's shape, not the assertions' wording, and not the scope root
— `#main-content` is the right root (row R1b).

Why this is Major and not Blocking: acceptance checkbox 1 asks for the
test to be added, to assert those two facts, and to pass. Read literally
it is met (rows R1a, R1d, R1e). What is defeated is the requirement's
purpose — issue #56 exists because issue #38's own partial-failure
assertion was too narrow to catch a second surface, and the replacement
inherits a different form of the same blindness.

Nearest artifact that would settle it for a future editor: a payload
with one non-empty row in any list `isPageEmpty` reads, which is the
same isolation Appendix A3's cells 3 and 4 performed by other means.
Choosing the fix is the implementation role's call, not this role's.

The sibling record's S1 examined this test's *scope root* and found it
adequate; that reading is not contradicted here. Payload reachability is
a separate question and is the one this finding turns on.

### CR-F2 — the banner assertion does not verify collapsedness. Minor. Row R1c

`bannerHasCollapsedMessage` (`test/rsb_tests/test_dashboard_dom.py:270`,
asserted at `:278`) checks only that the marker string occurs somewhere
in `#partial-banner`'s `innerHTML`. It would pass identically if the
banner printed the message as always-visible text, because it never
looks at the `<details>` element `collapsibleDetailHtml`
(`src/rsb/web/dashboard.js:462`) emits, and never asserts the absence of
an `open` attribute. Issue #56's checkbox wording — "실패 repo raw
메시지가 접히지 않은 채 등장하지 않고" — makes *un*collapsed exposure the
thing under test, and the collapsed-side assertion is the one that would
notice if the banner regressed to it. The assertion's name states a
property the assertion does not test.

### CR-F3 — `ErrorListItem` and `.error-list` survive as dead references. Note. Rows R4f, R4g, S6

`docs/specs/design-system.md:189` still carries
`| ErrorListItem | status-error |` in the §6 inventory whose preamble
(`:174`) says components are applied per-region in `screen-spec.md`,
after the same commit deleted the only region that applied it; and
`src/rsb/web/dashboard.css:347`'s comment header still names
`ErrorListItem` over selectors (`:348-349`) reachable only through
`.hygiene-list`.

**This is `docs/issue-56/reports/execution-observation.md` finding F1,
already recorded on the board with its own impact / timeline / root
cause / action item; it is cited here, not re-investigated.** What this
record adds is only the conformance consequence: three of its 33 rows
(R4f, R4g, S6) resolve to `Surface` on those artifacts. The selectors
themselves must not be deleted — `.hygiene-list` still renders through
them — which is the constraint F1's action item already states.

### CR-F4 — §5's enumeration of 24×24 controls still lists three. Note. Row R4d

`docs/specs/design-system.md:163-165` enumerates `row-toggle`,
`repo-filter`, `refresh-button`; the `.number-link` extension is a
separate sentence at `:167-170`. A reader grepping the enumeration finds
three controls and must read one sentence further to find the fourth.
The checkbox's "24px 목록 편입" is satisfied by §6's `DataTable` row
(R4e Present) on any reading, so this is record hygiene only. The
sibling `execution-observation` record reached the same reading
independently as its O7 note; this row concurs.

### CR-F5 — rendered 24×24 geometry unverified. Note (open request). Row R3e

No layout engine exists in this environment, so the declared minima at
`dashboard.css:255-256` are established as *declarations* and not as
rendered boxes. Handed off as a request, not scored as a pass.

### CR-F6 — adjacent-target spacing after the widening unverified. Note (open request). Row R3f

The declared boxes cannot overlap given `.issue-cell`'s `gap` and both
children's minima, but the laid-out result — including any interaction
with `table.data-table`'s `min-width: 640px` overflow behaviour, which
PR #43's AC1 owns — needs the same absent engine. Handed off as a
request.

## Unverifiable rows and what would settle each

| Row | What would settle it |
|---|---|
| R3e | A measurement from a real layout engine — `getBoundingClientRect()` on a `.number-link` in each of its two contexts (inside `.issue-cell`, inside `<span class="mono">`) at the deployed board, reporting both `width` and `height` in CSS px. A browser-driver dependency (Playwright/Puppeteer) added to `test/package.json` would make this a committed check rather than a one-off. |
| R3f | The same engine, reporting the laid-out gap between the `.row-toggle` and `.number-link` boxes inside one `.issue-cell`, plus the issue column's resulting width against the 640px table minimum at the narrowest supported viewport. |

## Open-finding resolution path

CR-F1 and CR-F2 target `test/rsb_tests/test_dashboard_dom.py`; CR-F3 and
CR-F4 target `docs/specs/**` and `src/rsb/web/dashboard.css`; CR-F5 and
CR-F6 target the test harness's dependency set. All are outside this
role's write authority — it wrote only this file in phase 2 and only the
three phase-1 homes before it.

The path is therefore: the human reads this record on PR #63, decides
whether any finding warrants an issue, and authors it. CR-F3 reaches the
same artifacts the sibling record already handed over, so one issue
would close both records' rows. If the human judges none of them worth
an issue, they stand as recorded verdicts against `93a60b3` and need no
further action. This role files no issue and proposes no fix.

## Scope limitations

1. **No rendered-pixel check** (R3e, R3f). The absence is environmental,
   identical to the one the building role and the sibling observer both
   worked under.
2. **The building record's jsdom `getComputedStyle` run is
   author-attested only.** It was not committed and no CI runs tests
   (`.github/workflows/deploy-board.yml` has no test step). No verdict
   above rests on it.
3. **Single account.** PR #57's author, its approver, this review's
   author and this review's approver are all `jjongkwann`. What this
   review supplies is role-and-session independence over a fixed
   artifact set — a reader who did not build the change checking it
   against the specification — not account-level separation of duties.
4. **Trajectory and process are out of scope**, including phase-gate
   conduct on PR #57. That is the sibling `execution-observation` role's
   territory under the same 실행 계획 step, and its record is on main.

## Appendix — verbatim commands and output for every B-class row

Working directory is the repository root unless a `cd` is shown. All
probe trees live under `$TMPDIR` (`/tmp/claude-501`), outside the
repository; none of them is committed and no `src/`, `test/` or
`docs/specs/` file on this branch was modified at any point.

### A1 — harness install (prerequisite for A2, A3)

```
$ npm install --prefix test
added 38 packages, and audited 39 packages in 620ms

8 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

`test/node_modules/` is untracked and deliberately not committed.
Without it `test_dashboard_dom.py` skips its whole module, which would
have made every acceptance-check-1 row Unverifiable for want of a
harness rather than for want of a browser.

### A2 — suite runs (rows R1e, S4, S8)

Delivered tree, current branch (`src/`, `test/` identical to `93a60b3`):

```
$ cd src && python3 -m pytest ../test/ -q
...
FAILED ../test/rsb_tests/test_dashboard_dom.py::test_row_toggle_click_opens_detail_and_flips_aria_expanded - assert False is True
FAILED ../test/rsb_tests/test_dashboard_dom.py::test_row_toggle_reactivating_open_button_closes_it - AssertionError: assert 'true' == 'false'
2 failed, 64 passed in 6.74s
```

Parent baseline. The tree at `/tmp/claude-501/rsb-base` is a copy of the
working tree with `dashboard.js`, `dashboard.css` and
`test_dashboard_dom.py` replaced by their `71a0dff` versions — i.e.
`21c2359`'s parent for every file that affects the suite:

```
$ cd /tmp/claude-501/rsb-base/src && python3 -m pytest ../test/ -q
...
FAILED ../test/rsb_tests/test_dashboard_dom.py::test_row_toggle_click_opens_detail_and_flips_aria_expanded - assert False is True
FAILED ../test/rsb_tests/test_dashboard_dom.py::test_row_toggle_reactivating_open_button_closes_it - AssertionError: assert 'true' == 'false'
2 failed, 63 passed in 6.53s
```

63 → 64 passed, 2 → 2 failed, same two names: the delta is exactly the
one added test. The two failures are the settled `f353910`
unguarded-`matchMedia` defect, attributed in
`docs/issue-36/reports/conformance-review.md` F1 and Appendix A4 and not
re-derived here.

### A3 — mutant-kill probe, 2×2 (row R1f, finding CR-F1)

Two throwaway trees outside the repository, each a copy of the working
tree with one mutation:

- `/tmp/claude-501/rsb-mutant` — `dashboard.js` replaced by its
  `71a0dff` version, i.e. `renderErrors` (`:355`) and the call site
  (`:632`) restored verbatim. `21c2359` records this file as `0 13`, a
  pure deletion, so the restored file is byte-identical to the
  pre-change state.
- `/tmp/claude-501/rsb-ctrl` — delivered `dashboard.js`, unmutated.

Both then optionally get the second mutation, applied with
`sed -i '' 's|if (isPageEmpty(data)) {|if (false) { // probe: disable empty-state early return|'`,
which disables only the empty-state early return.

| # | `renderErrors` | empty-state early return | command | result |
|---|---|---|---|---|
| 1 | absent (delivered) | active | `cd src && python3 -m pytest ../test/ -q` | `2 failed, 64 passed` — new test among the 64 |
| 2 | **restored** | active | `cd /tmp/claude-501/rsb-mutant/src && python3 -m pytest ../test/rsb_tests/test_dashboard_dom.py -q -k partial_failure_raw_message` | `1 passed, 8 deselected in 0.55s` — **mutant survives** |
| 3 | absent (delivered) | **disabled** | `cd /tmp/claude-501/rsb-ctrl/src && python3 -m pytest ../test/rsb_tests/test_dashboard_dom.py -q -k partial_failure_raw_message` | `1 passed, 8 deselected in 0.56s` |
| 4 | **restored** | **disabled** | `cd /tmp/claude-501/rsb-mutant/src && python3 -m pytest ../test/rsb_tests/test_dashboard_dom.py -q -k partial_failure_raw_message` | `1 failed` — `assert result["mainContentHasRawMessage"] is False` → `E assert True is False` |

Cell 4 also proves cells 2 and 3 exercised the intended tree: only a
`dashboard.js` containing `renderErrors` can put the marker string into
`#main-content`, so the mutant copy — not the repository's file — is
what the harness loaded
(`DASHBOARD_JS = Path(__file__).resolve().parents[2] / "src" / "rsb" / "web" / "dashboard.js"`,
`test/rsb_tests/test_dashboard_dom.py:33`).

Reading: cell 2 alone shows the assertion has no power. Cells 3 and 4
isolate why — with the early return disabled the same test kills the
mutant, and the delivered code still passes, so the empty-state
short-circuit is the whole of the difference.

### A4 — greps (rows R2c, R4a, R4c, S6, S7, S8)

```
$ grep -rn "renderErrors" src/
$ grep -rn "renderErrors" test/rsb_tests/
test/rsb_tests/test_dashboard_dom.py:252:# second, always-visible surface (`renderErrors`, since removed) rendered
$ grep -rn "ErrorListItem" docs/specs/ src/
docs/specs/design-system.md:189:| `ErrorListItem` | `status-error` |
src/rsb/web/dashboard.css:347:/* HygieneListItem / ErrorListItem */
$ grep -rn "1\.9\|Errors panel" docs/specs/ src/
docs/specs/screen-spec.md:213:  errors (issue #56 F1) — the former standalone "Errors panel" section
$ grep -rn "error-list" src/ test/rsb_tests/
src/rsb/web/dashboard.css:348:.hygiene-list, .error-list { list-style: none; margin: 0; padding: 0; }
src/rsb/web/dashboard.css:349:.hygiene-list li, .error-list li {
test/rsb_tests/test_dashboard_dom.py:269:          errorListExists: document.querySelector(".error-list") !== null,
$ grep -n "ErrorListItem" docs/specs/screen-spec.md
$ grep -n "number-link" docs/specs/design-system.md
168:`.number-link` (the `#<n>` issue/PR link) after determining WCAG
182:| `DataTable` | … + trailing `#<n>` link (`.number-link`, `color-action-primary-background`, issue #36, 24×24px minimum size per issue #56 F3) |
$ grep -n "errors" src/rsb/web/dashboard.js
84:    errors: { label: `${data.errors.length} repo errors`, … count: data.errors.length },
116:    errors: data.errors.filter((e) => e.repo === repo),
125:// (`errors[].repo`) — i.e. every repo the board is configured for,
130:    ...data.errors.map((e) => e.repo),
565:  if (data.errors.length > 0 && succeededRepoCount === 0) {
566:    renderFullError(data.errors.map((e) => `${e.repo}: ${e.message}`).join("; "));
570:  const repoCount = Object.keys(data.generated_at_by_repo).length + data.errors.length;
571:  HEADER_META.textContent = `as of ${data.generated_at} — ${repoCount} repos, ${data.errors.length} errors`;
585:  const failedRepos = data.errors;
```

The `design-system.md:182` and `dashboard.js:84` lines are elided at `…`
for width; both are quoted in full in the rows that rely on them.

### A5 — syntax check (row S8)

```
$ node --check src/rsb/web/dashboard.js
node --check exit: 0
```

### A6 — approval-gate state (Why section)

```
$ gh issue view 56 --json comments
  jjongkwann  2026-08-04T10:29:48Z  "APPROVE issue-56/implementation"
  jjongkwann  2026-08-08T02:48:41Z  "APPROVE issue-56/execution-observation"
  jjongkwann  2026-08-08T02:57:50Z  "APPROVE issue-56/conformance-review"
$ cat docs/specs/approvers.md
- JiwonJung94
- jjongkwann
```

Three comments, three exact-string APPROVE bodies, no prose comment. The
third is this role's gate.

## Next steps

None for this role — phase 2 is complete with this record committed on
`issue-56/conformance-review` and reported through PR #63. The six
findings return to the human through that PR.

## Warrant hunt

`proposal: docs/issue-56/proposals/conformance-review.md` — **phase-2
before-landing dispatch not run, recorded here rather than left
silent.** Two binding reasons, the same pair the sibling role recorded
for its own phase 2: this role's entire phase-2 write set is a single
file under `docs/`, which triggers the docs-only fast path exempting the
before-landing dispatch; and this is a headless single-shot session,
where contract v3 s22 forbids ending the turn with a dispatched agent
whose result has not been consumed and therefore permits not dispatching
over dispatching-and-abandoning.

The `after-proposal` dispatch for this unit already ran, in phase 1, and
returned a FINDING recorded at
`docs/issue-56/reports/conformance-review/hunt.md` and restated in the
proposal's closing section — the approval gate's mode being inferable
after the fact. It is not a defect in any row above and changes no
verdict; it is out of this role's write set and stays surfaced, not
fixed. `docs/issue-56/reports/execution-observation.md` F2 records the
same skip-line obligation against the building role's record; this
section discharges it for this record.
