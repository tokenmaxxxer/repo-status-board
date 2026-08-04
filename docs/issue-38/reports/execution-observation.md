# Execution-observation record (issue #38, phase 2)

Subject observed: the **implementation** role's phase-1→phase-2 execution
on issue #38 ("디자인 게이트 P1/P2 보완 — 모바일 overflow, 인라인 상세,
live region, 터치 영역, 오류 UX"), as landed in **PR #43**
(`issue-38/implementation` → `main`, MERGED 2026-08-03T12:25:48Z, merge
commit `f3539107628a3a519eefe2f45b0e8d6f766a7912`,
`https://github.com/tokenmaxxxer/repo-status-board/pull/43`), commits
`7c50201ef142498f29b265d7d98111a824f31d5e` (phase 1) and
`e8443ea6536ff4aa131842143491f963d9d292d6` (phase 2), and its own record
`docs/issue-38/reports/implementation.md`. Scope, method, and evidence
sources for this record were fixed in advance by this role's own phase-1
proposal `docs/issue-38/proposals/execution-observation.md` and survey
`docs/issue-38/reports/execution-observation/survey.md`, committed at
`c037c65`.

code_under_review: PR #43 (`issue-38/implementation` → `main`, merged @
`f353910`) — `src/rsb/web/dashboard.js`, `src/rsb/web/dashboard.css`,
`src/rsb/web/index.html`, `test/rsb_tests/test_model.py`,
`docs/specs/screen-spec.md`, `docs/specs/design-system.md`,
`docs/issue-38/reports/implementation.md`
loop_state: reported

loop_state transitions this session:
1. `proposed` — phase-1 survey/scout-brief/proposal committed at
   `c037c65`, PR #50 opened.
2. `approved` — issue comment `APPROVE issue-38/execution-observation`
   (`issuecomment-5175886254`) read and validated against
   `docs/specs/approvers.md`; phase 2 opened.
3. `reported` — this record written as the first act of phase 2, verdict
   rendered, committed on `issue-38/execution-observation`.

## Why

Approved via the issue #38 comment whose entire body is the 38-character
string `APPROVE issue-38/execution-observation` (author `jjongkwann`,
`2026-08-04T07:26:15Z`,
`https://github.com/tokenmaxxxer/repo-status-board/issues/38#issuecomment-5175886254`).
This record executes `docs/issue-38/proposals/execution-observation.md`
§0–§2: static diff/blob tracing in place of live re-execution (this
role's contract prohibits re-running the observed role's code), a
three-level verdict (outcome / trajectory / step), a per-acceptance-
criterion table carrying a three-way evidence bucket, an explicit
substituted-verification treatment, and any deficiency finding in the
four-part blameless shape.

## What was done

Read PR #43 in full — its metadata, title, body, file list, and its
(empty) `reviews`/`comments` arrays; both of its commits' messages,
trailers, and diffstats; the complete `e8443ea` diffs for
`dashboard.js`, `index.html`, `dashboard.css`, and `test_model.py`; and
the `dashboard.js`/`dashboard.css` **blobs at `e8443ea`** for the
unchanged context the diff does not show. Read the observed role's own
record (`docs/issue-38/reports/implementation.md`, all 303 lines), its
approved proposal, and its phase-1 survey and scout brief. Read issue
#38's body and both of its comments, `docs/specs/approvers.md`, and issue
#36's state. Then traced, by hand and against those artifacts, each of
issue #38's nine acceptance criteria, the five open questions this role's
own phase-1 survey left (`docs/issue-38/reports/execution-observation/survey.md`
§5), and the phase-1→phase-2 timestamp chain — and wrote the three-level
verdict this role's contract requires, with an adjacent citation on every
verdict-bearing sentence.

No `pytest`, `node`, `node --check`, jsdom script, or `rsb serve` command
was executed this session; no file under `src/`, `test/`, or
`docs/issue-38/reports/implementation*` was written or modified; and no
working-tree file was read as evidence of what the observed role did —
every code claim below reads the historical blob or diff at `e8443ea`.

## How phase 2 was opened for this role

`gh pr list --head issue-38/execution-observation` returns PR #50
(`https://github.com/tokenmaxxxer/repo-status-board/pull/50`, OPEN),
which carries this role's phase-1 artifacts. Its author is `jjongkwann`;
`docs/specs/approvers.md` (read in full this session) lists exactly two
accounts, `JiwonJung94` and `jjongkwann`. PR author and approver are the
same account → **single-account mode**, so the gate is an issue-level
comment whose entire body is exactly `APPROVE issue-38/execution-observation`
from an approvers.md account. `gh issue view 38 --json comments` returns
exactly two comments on issue #38, and both are exact-string approvals:
`APPROVE issue-38/implementation` (31 chars, `issuecomment-5165966474`,
`2026-08-03T11:53:53Z`) and `APPROVE issue-38/execution-observation`
(38 chars, `issuecomment-5175886254`, `2026-08-04T07:26:15Z`), both by
`jjongkwann`. The second is this role's gate string, string-exact with no
surrounding prose. No near-miss, prose-approval, or otherwise
affirmative-sounding non-matching comment exists on issue #38 to report.
Phase 2 for this role is authorized.

## What was read first-hand this session

| Artifact | How it was read |
| --- | --- |
| Issue #38 body, 9 acceptance checkboxes, 실행 계획 | `gh issue view 38` |
| Both issue #38 comments (URL, author, timestamp, byte length, body) | `gh issue view 38 --json comments --jq ...` |
| PR #43 metadata, title, body, file list, `reviews`, `comments` | `gh pr view 43 --json number,title,body,state,author,mergedAt,mergeCommit,createdAt,headRefName,baseRefName,reviews,comments,files` — `reviews: []`, `comments: []` |
| Both observed commits: full message + trailer + diffstat | `git show --stat --format=... 7c50201` / `e8443ea` |
| The full `dashboard.js` and `index.html` diffs of `e8443ea` | `git show e8443ea --format='' -- src/rsb/web/dashboard.js src/rsb/web/index.html` |
| The full `dashboard.css` diff of `e8443ea` | `git show e8443ea -- src/rsb/web/dashboard.css` |
| The full `test_model.py` diff of `e8443ea` | `git show e8443ea --format='' -- test/rsb_tests/test_model.py` |
| `dashboard.js` / `dashboard.css` blobs **at `e8443ea`** (unchanged context) | `git show e8443ea:src/rsb/web/dashboard.js`, `git show e8443ea:src/rsb/web/dashboard.css` |
| The observed role's record, all 303 lines | `docs/issue-38/reports/implementation.md` |
| The observed role's approved proposal (frozen write set, 수동 검증, Out of scope, How you'll know it worked) | `docs/issue-38/proposals/implementation.md` |
| The observed role's phase-1 survey and scout brief | `docs/issue-38/reports/implementation/survey.md`, `.../scout-brief.md` |
| `docs/specs/approvers.md` | read in full |
| Issue #36 state (for the AC8 closing-keyword check) | `gh issue view 36 --json number,state,stateReason` — `OPEN` |
| Comparator record shape | `git show origin/main:docs/issue-34/reports/execution-observation.md` |

## Independence statement

This role did not author, edit, or execute any part of the observed
artifact — PR #43, its commits `7c50201` / `e8443ea`, or
`docs/issue-38/reports/implementation.md` — in this session or any prior
one, and has written nothing outside its own record area
(`docs/issue-38/reports/execution-observation*`,
`docs/issue-38/proposals/execution-observation.md`). Every claim below is
drawn from the merged diff, the commit objects, the GitHub artifacts, and
the observed role's own record — never from re-running the observed
role's code, and never from treating the current working tree as evidence
of what that role decided or did. No verdict language appears before this
statement.

## Three-level verdict

### 1. Outcome — did PR #43 land what issue #38 asked?

Issue #38's body lists nine "수용 기준" checkboxes (seven functional, two
"주의" constraints). Each row carries an evidence bucket per this role's
proposal §0.1: **[A]** established here from the artifacts; **[B]**
claimed by the observed role and not independently reproducible (the
re-execution prohibition); **[C]** not establishable by anyone in this
environment (no browser, no screen reader).

| # | Criterion (issue #38 body) | Evidence | Verdict |
|---|---|---|---|
| AC1 | 390px 에서 페이지 본문이 가로 스크롤되지 않고 표만 개별 스크롤된다 | `git show e8443ea:src/rsb/web/dashboard.css` line 373 adds `#main-content, #detail-panel-slot { min-width: 0 }`; line 181 adds `table.data-table { min-width: 640px }`; line 205 rewrites `.table-scroll { overflow-x: auto; width: 100% }`. These are exactly the three change points issue #38 P1-1 named, and they are the grid-item automatic-minimum-size fix the observed role's own scout brief documents at `docs/issue-38/reports/implementation/scout-brief.md:14-22` @ `7c50201`. | **Mechanism met [A]** — `e8443ea` css:181,205,373. **Rendered 390px outcome [C]** — no pixel measurement exists in the record and none is possible here |
| AC2 | <1200px 에서 상세가 선택 행 바로 아래에 나타난다 | `e8443ea:src/rsb/web/dashboard.js:485` — `applySelectionLayout(data)` calls `selectedRow.insertAdjacentHTML("afterend", detailRowHtml(selectedRow.children.length, contentHtml))` when `!window.matchMedia(WIDE_LAYOUT_QUERY).matches`; `:464` — `detailRowHtml(colspan, contentHtml)` emits `<tr class="detail-row"><td colspan="…">`. In the same diff, `renderData`'s old unconditional `DETAIL_SLOT.innerHTML = …` line is replaced by the `applySelectionLayout(data)` call, and the previously-dead `WIDE_LAYOUT_QUERY` constant is now actually read. | **Wiring met [A]** — `e8443ea` js:464,485. **Behavior under a real media query [B]** — `docs/issue-38/reports/implementation.md:119-123` discloses jsdom has no `matchMedia` and a controllable `{ matches }` polyfill was substituted |
| AC3 | 로딩·오류·상세 열림이 스크린리더에 전달된다(live region/포커스 이동) | `e8443ea:src/rsb/web/index.html:13,20` add `aria-live="polite"` to `#header-meta` and `#partial-banner`; `:24` gives `#main-content` an initial `aria-busy="true"`. The `dashboard.js` diff: `renderSkeleton` sets `aria-busy="true"`; `renderData` (both the empty-page early return and the normal path) and `renderFullError` set it back to `"false"`; `.error-state` gains `role="alert"`; `renderDetailPanel` emits `<h2 id="detail-panel-heading" tabindex="-1">` inside `role="region" aria-labelledby="detail-panel-heading"`; `attachRowToggleHandlers` moves focus to that heading on open and back to the row's own button on close. | **Attributes and focus wiring met [A]** — `e8443ea` index.html:13,20,24 plus the `dashboard.js` diff hunks. **Actual screen-reader announcement [C]** — no AT run is claimed in the record and none is possible here |
| AC4 | 모바일에서 모든 인터랙티브 컨트롤이 최소 24×24px | `e8443ea:src/rsb/web/dashboard.css:223-225` gives `.row-toggle` `min-width: 24px; min-height: 24px; display: inline-flex`, and `inline-flex` is a box type that honors both (this pass's scout brief, `docs/issue-38/reports/execution-observation/scout-brief.md:34-36`); `:123` and `:138` add `min-height: 24px` to `.refresh-button` and `#repo-filter`. **But** `.number-link` — the 8×17px external link issue #38 P2-5 measured — sits at `e8443ea:src/rsb/web/dashboard.css:248-259` with no `min-width`/`min-height`. The approved proposal put it out of scope on the WCAG 2.5.8 inline-text exception *conditional on a phase-2 measurement* (`docs/issue-38/proposals/implementation.md:310-312`: "phase-2 실측으로 확인만 하고 CSS 는 건드리지 않는다"), and the record's touch-target paragraph (`docs/issue-38/reports/implementation.md:161-166`) covers only `.row-toggle`/`#repo-filter`/`.refresh-button`, never naming `.number-link`. | **Met for the three sized controls [A]** — `e8443ea` css:123,138,223-225. **Not met as literally written ("모든")** for `.number-link` at `e8443ea` css:248-259 — excluded by an approved scope decision whose own promised confirmation was never reported (**F3**) |
| AC5 | 부분/전체 오류가 요약+접힌 상세 구조이고 내부 경로를 노출하지 않는다 | Full error: `renderFullError` replaces the raw inline message with a generic `<p>` plus `collapsibleDetailHtml("Details", message)` (`e8443ea` `dashboard.js` diff, `renderFullError` hunk) — met. Partial banner: `e8443ea:src/rsb/web/dashboard.js:603` wraps the joined per-repo detail in `collapsibleDetailHtml("Details", detail)` — met. **A third error surface is untouched**: `renderErrors(errors)` at `e8443ea:src/rsb/web/dashboard.js:355-365` still emits `<section class="region"><h2>Errors</h2><ul class="error-list">` whose line 361 renders `<li>${escapeHtml(e.repo)}: ${escapeHtml(e.message)}</li>` **always visible**, and it is called at `e8443ea:src/rsb/web/dashboard.js:632` inside `renderData`'s `MAIN.innerHTML` — on the same `data.errors.length > 0` condition that raises the collapsed partial banner. `escapeHtml` prevents markup injection, not disclosure. | **Not met [A]** — `e8443ea` js:355-365 and js:632 (**F1**) |
| AC6 | 표에 caption/th scope 가 있고 선택 행이 시각적으로 구분된다 | `e8443ea:src/rsb/web/dashboard.js:177` emits `<th scope="col">`; `:183` emits `<caption class="visually-hidden">`; `renderTable`'s new 4th `caption` argument is supplied at all four call sites ("Decision queue", "Flows", "Sessions" in `renderData`; "Accounting ledger" in `renderAccounting` — all four visible in the `e8443ea` diff). `e8443ea:src/rsb/web/dashboard.css:197` adds `tr.selected-row { background: var(--color-status-info-background) }`, applied by `applySelectionLayout` (js:485); `.visually-hidden` is the standard clip technique at css:89. | **Met [A]** — `e8443ea` js:177,183 and css:89,197 |
| AC7 | 기존 테스트 전부 통과, 1440px 기본 화면 밀도에 회귀 없음 | `docs/issue-38/reports/implementation.md:187-190` states **57 passed**, 0 failed (55 pre-existing + 2 new); `:192` states `node --check src/rsb/web/dashboard.js` clean; `:256-261` (`closed_checks`) states both were re-run after the two adversarial-hunt fixes. The "+2" is itself verifiable in the diff — `git show e8443ea --format='' -- test/rsb_tests/test_model.py` adds `test_dashboard_js_detail_row_html_wraps_content_in_a_tr_with_colspan` and `test_dashboard_js_collapsible_detail_html_escapes_summary_and_detail` — even though the run is not. | Test suite: **claimed, not reproduced [B]** — implementation.md:187-190; re-running is prohibited for this role. 1440px density regression: **[C]** — no such measurement appears anywhere in the record |
| AC8 | 주의: PR 본문에 closing 키워드 금지 (issue #23 T2) | `gh pr view 43 --json body`, read in full this session: the body's closing paragraph reads "Referencing #38, not closing it — …". No `Closes`/`Fixes`/`Resolves` bound to `#38` appears in any form, plain or backtick-quoted. The one keyword-family word present is "already fixed by #36 (PR #37, merged)", which is not GitHub's closing form (the keyword must directly precede the reference) and targets a different issue; `gh issue view 36 --json state` returns `OPEN`, confirming no auto-close fired. | **Met [A]** — PR #43 body + issue #36 state `OPEN` |
| AC9 | 주의: DOM 배선 변경은 브라우저 실제 조작으로 확인하고 record 에 기재 | Browser operation did **not** happen. `docs/issue-38/reports/implementation.md:104-123` records that headless Chrome fails with crashpad/`ProcessSingleton` permission errors — reproduced by the observed role that session with an explicit `--user-data-dir`, not assumed from precedent — that no Playwright/Selenium/Puppeteer exists, and that a jsdom harness loading the real shipped `index.html` + `dashboard.js` was substituted with a hand-written `matchMedia` polyfill. The substitution *is* recorded, which is what the second half of AC9 asks. | **Substituted and disclosed [A]** — implementation.md:104-123. **The "브라우저 실제 조작" half unmet [C]**, by environment rather than by choice; the disclosure is global rather than per-criterion (**F3**) |

**Outcome verdict: PR #43 landed eight of issue #38's nine acceptance
criteria. AC5 is not met, on the evidence of
`e8443ea:src/rsb/web/dashboard.js:355-365` and `:632`; AC4 is met only
for the three controls the observed role actually sized
(`e8443ea:src/rsb/web/dashboard.css:123,138,223-225`) and not for
`.number-link` at `e8443ea:src/rsb/web/dashboard.css:248-259`.** All
seven P-items PR #43's body claims (P1-1, P1-3, P1-4, P2-5, P2-6, P2-7,
P3-8, per `gh pr view 43 --json body`) have real, traceable code behind
them at `e8443ea` — including P1-3, which the observed role's own survey
correctly identified as dead code before the change
(`docs/issue-38/reports/implementation/survey.md:23-25` @ `7c50201`,
"`WIDE_LAYOUT_QUERY` … is unused (no `matchMedia` call anywhere) — still
a dead constant") and which `e8443ea:src/rsb/web/dashboard.js:485` now
actually implements. The shortfall is one uncovered surface inside P2-6,
not a missing item.

### 2. Trajectory — was the phase-1→phase-2 path sound?

**Surveyed before proposing.** `git show --stat 7c50201` shows the
phase-1 commit (`2026-08-03T11:48:44Z`) touched exactly three files, all
under `docs/issue-38/`, +674/−0: `proposals/implementation.md` (327),
`reports/implementation/survey.md` (224),
`reports/implementation/scout-brief.md` (123). No `src/` or `test/` path
appears in that diffstat — the phase boundary held on the way in. The
survey opens by naming the six files it read end-to-end and, at
`docs/issue-38/reports/implementation/survey.md:5-9`, explicitly
re-anchors issue #38's own stale line numbers (which predate PR #37)
instead of quoting them secondhand — a survey that did the reading it
claims.

**Scouted when required.**
`docs/issue-38/reports/implementation/scout-brief.md:3-10` @ `7c50201`
documents a 4-angle parallel sweep (grid/flex `min-width: 0` overflow,
ARIA live-region/`aria-busy` practice, WCAG 2.5.8 target size, accessible
expandable-row insertion), a judge point 1 that found nothing to swap, a
judge point 2 saturation stop before any deepening round, and ~25s
wall-clock. Its must-bes at `:14-32` are precisely what the delivered code
implements — `min-width: 0` on the grid item (`e8443ea` css:373),
`min-width`/`min-height` for 24×24 (css:223-225), `aria-live="polite"` vs
`role="alert"` (index.html:20 and the `renderFullError` hunk) — so the
brief steered the build rather than decorating it.

**Real human approval, in the right order.** The chain is unbroken and
correctly ordered: phase-1 commit `7c50201` 11:48:44Z → PR #43 opened
11:49:04Z (`gh pr view 43 --json createdAt`) → issue comment `APPROVE
issue-38/implementation`, exact 31-character body, `jjongkwann`,
11:53:53Z (`issuecomment-5165966474`) → phase-2 commit `e8443ea`
12:24:20Z → merge 12:25:48Z. `jjongkwann` is listed in
`docs/specs/approvers.md` and is PR #43's author, so single-account mode
applies and the issue-comment path is the correct gate;
`gh pr view 43 --json reviews,comments` returns `[]` for both, so no
competing or approval-shaped artifact exists elsewhere on the PR. No
phase-2 byte predates the approval.

**Commit hygiene.** Both `7c50201` and `e8443ea` carry a `Subject:
issue-38` trailer in their message bodies (`git show --format=%b`, read
this session), one commit per subject, as contract v3 s13 requires.

**Write-set discipline.** `git show --stat e8443ea` touched exactly the
six paths the approved proposal froze at
`docs/issue-38/proposals/implementation.md:1-7`, plus the role's own
record — and no scratch or verification artifact appears in either
diffstat, which independently corroborates the record's own
`no-stale-scratch-artifacts` claim at
`docs/issue-38/reports/implementation.md:268-270`.

**Adversarial pass actually ran and changed the code.** The record
discloses at `docs/issue-38/reports/implementation.md:198-206` that no
`warrant-hunter` agent type exists here and a `general-purpose` agent was
substituted, and its two findings are visible in the merged code, not
only in prose: the ambiguous-row-match guard (`matchCount !== 1 →
selectedRow = null`) is at `e8443ea:src/rsb/web/dashboard.js:485`'s
function body, and the `escapeHtml(v)` outcome-value fix is in the
`renderAccounting` hunk of the same diff. A hunt whose fixes are traceable
in the diff is a hunt that happened.

**The one qualification.** The approved proposal's "수동 검증 (phase 2)"
section (`docs/issue-38/proposals/implementation.md:285-294`) promised
`rsb serve` at 390px/1024px/1200px+, a VoiceOver pass, and a Tab
traversal; phase 2 substituted a jsdom harness
(`docs/issue-38/reports/implementation.md:104-123`). Judged the way audit
practice judges a substituted procedure — on disclosure and on
re-assessed sufficiency, not on whether jsdom equals a browser
(`docs/issue-38/reports/execution-observation/scout-brief.md:21-27`) — the
disclosure limb passes cleanly: the substitution is surfaced in the record
*and* in PR #43's own body ("no browser automation available in this
sandbox — jsdom substitute"), with the blocking Chrome failure reproduced
rather than assumed. The re-assessed-sufficiency limb is where it falls
short, and that lands as F3 below rather than against the trajectory.

**Trajectory verdict: sound.** Survey → scout → proposal → PR → real
exact-string approval from an `approvers.md` account → phase-2 work →
merge, in that order, with no phase-boundary violation and no fabricated
or prose-inferred approval, on the evidence of `git show --stat 7c50201`,
`issuecomment-5165966474`, and `git show --stat e8443ea`.

### 3. Step — which specific artifact is deficient?

Four findings, each in the four-part blameless shape. F1 is the material
one; F2–F4 are record and metadata hygiene.

#### F1 — `renderErrors` leaves a third, always-visible error surface (AC5 unmet)

- **Impact.** On any partial failure (≥1 repo failed, ≥1 succeeded) the
  dashboard renders the collapsed `<details>` banner *and*, lower on the
  same page, an always-visible "Errors" section listing `repo: message`
  for every failed repo — `e8443ea:src/rsb/web/dashboard.js:361` inside
  `renderErrors`, called at `e8443ea:src/rsb/web/dashboard.js:632` from
  `renderData`'s `MAIN.innerHTML` template. Issue #38's AC5 ("부분/전체
  오류가 요약+접힌 상세 구조이고 내부 경로를 노출하지 않는다") and its
  P2-6 body text ("전체 오류는 provider 내부 경로까지 그대로 표시한다")
  are therefore not satisfied for the partial-failure case: the raw
  provider message, internal paths included, is still on screen by
  default. `escapeHtml` on that line prevents markup injection, not
  disclosure.
- **Timeline.** The surface predates issue #38 and is untouched by
  `e8443ea` — it appears in the `renderData` hunk only as unchanged
  context. `grep -n "renderErrors\|error-list\|Errors"` across
  `docs/issue-38/reports/implementation/survey.md`,
  `docs/issue-38/proposals/implementation.md`, and
  `docs/issue-38/reports/implementation.md` returns **zero matches** — the
  function is named in none of the three, so it was never surveyed, never
  scoped in, and never scoped out.
- **Root cause.** The survey and proposal anchored P2-6 on the two error
  surfaces issue #38's body cited by line number (`dashboard.js:155`,
  `:489` — the partial banner and `renderFullError`) and did not enumerate
  the error-rendering surfaces independently of those anchors. The
  verification then inherited the same blind spot: the jsdom
  partial-failure scenario asserted the raw text was absent from the
  *banner* once its `<p>` was removed
  (`docs/issue-38/reports/implementation.md:143-146`) and drew from that
  the wider conclusion that "it genuinely isn't visible outside the
  collapsed region" — a claim about the whole document supported by an
  assertion scoped to one element. The assertion was sound; the inference
  drawn from it was one scope level too wide.
- **Action item (for the human to judge — this role does not file
  issues).** Route `renderErrors`' per-repo message through
  `collapsibleDetailHtml(...)`, or drop the section on the
  partial-failure path now that the banner carries the same content; and
  make the corresponding assertion document-scoped (`#main-content` text
  does not contain the raw message) rather than element-scoped. Contract
  v3 makes issues user-authored; this finding is handed off on PR #50 for
  that decision.

#### F2 — the record states its assertion counts twice and never reconciles them

- **Impact.** A reader cannot tell how many DOM assertions actually ran.
  `docs/issue-38/reports/implementation.md:125` says "Three scenarios
  run" and then enumerates **four** items (`:127`, `:140`, `:147`,
  `:154`); those four are labelled 18 + 6 + 9 + 4 = 37 checks, and
  `:194-196` restates "37 individual assertions across 4 scripts"; but
  `closed_checks` at `:262-264` says "21 + 6 + 9 + 4 = 40 assertions
  across success/ambiguous-session/partial-error/full-error/
  refresh-disabled scenarios" — five scenario names for four scripts.
  Both sums are internally correct (18+6+9+4=37, 21+6+9+4=40); they
  simply disagree with each other, and nothing in the record says which
  is current.
- **Timeline.** The narrative section describes the pre-hunt run; the
  adversarial hunt then added an ambiguous-session scenario
  (`docs/issue-38/reports/implementation.md:228-232`, "Verified with a new
  jsdom scenario (two Sessions rows sharing issue 99/repo-b, different
  roles)"), which plausibly accounts for the 18→21 delta, and
  `closed_checks` was written after that re-run. The narrative section was
  not brought forward to match.
- **Root cause.** Two sections of the same record describe the same
  artifact at two different points in time, with no restatement pass after
  the hunt-fix re-run to tie them together.
- **Action item.** One reconciling sentence in the narrative section
  ("18 → 21 after the ambiguous-session scenario was added post-hunt;
  total 40") plus "Three scenarios run" → "Four scenarios run" closes it.
  No re-run is needed: this is a documentation defect and not a phantom
  number — each total is arithmetically self-consistent and the delta has
  a stated cause elsewhere in the same document.

#### F3 — the substituted-verification disclosure is global, never mapped per criterion

- **Impact.** `docs/issue-38/reports/implementation.md:104-123` discloses
  the jsdom substitution and the `matchMedia` polyfill once, globally, and
  `:161-166` separately concedes jsdom cannot compute rendered pixel
  geometry. What is absent is the per-criterion re-assessment: which of
  issue #38's nine criteria the substitute still establishes, and which it
  leaves open. The concrete cost is AC4 — the approved proposal
  (`docs/issue-38/proposals/implementation.md:310-312`) excluded
  `.number-link` from resizing *on the condition* that phase 2 confirm the
  WCAG 2.5.8 inline-text exception by measurement ("phase-2 실측으로
  확인만 하고 CSS 는 건드리지 않는다"). That measurement never happened
  and its non-performance is nowhere named: `.number-link` appears zero
  times in the record, and `e8443ea:src/rsb/web/dashboard.css:248-259`
  still carries no `min-width`/`min-height`. A reader of the record cannot
  tell that an approved conditional was left unresolved. AC1 (390px, no
  pixel measurement) and AC3 (screen-reader announcement, no AT run) sit
  in the same unmapped space.
- **Timeline.** The proposal set the condition at 11:48:44Z (`7c50201`);
  the environment blocked the browser at phase-2 time and the record
  disclosed that globally at 12:24:20Z (`e8443ea`); the conditional was
  never revisited.
- **Root cause.** The disclosure was written as an environment note ("here
  is what this sandbox cannot do") rather than as an evidence
  re-assessment ("here is what each acceptance criterion now rests on").
  The former is honest and was necessary; on its own it is not sufficient
  to close criteria the approved plan had tied to a measurement.
- **Action item.** When a promised verification procedure is substituted,
  carry the substitution through to each criterion the original procedure
  was going to close — a two-column list (criterion → what the substitute
  establishes / what it leaves open) next to the global disclosure. For
  this delivery specifically, `.number-link`'s WCAG 2.5.8 exception is an
  open, approved-but-unconfirmed assumption rather than a settled one.

#### F4 — PR #43's merged title says "phase 1" while the PR contains phase 2

- **Impact.** `gh pr view 43 --json title` returns `issue-38 phase 1:
  design-gate P1/P2/P3 survey + proposal`, while the same PR's body opens
  "Phase 1 + phase 2 for #38" and the PR contains `e8443ea`, the phase-2
  commit carrying every `src/` change. The merged title — the durable,
  board-visible label on the artifact — under-describes it: anyone reading
  merge history for what landed on `main` would see a
  survey-and-proposal PR.
- **Timeline.** PR #43 was opened 11:49:04Z when the title was accurate
  (phase 1 only); `e8443ea` was pushed to the same branch and PR at
  12:24:20Z per contract v3 s19's same-branch/same-PR rule, and the body
  was updated to "Phase 1 + phase 2" while the title was not; merged
  12:25:48Z.
- **Root cause.** The two-phase-one-PR flow makes the title stale by
  construction at the phase-2 transition, and nothing in that flow prompts
  a title update. The body *was* updated, so this is mechanical omission
  rather than a disclosure failure.
- **Action item.** Update the PR title at the phase-1→phase-2 transition
  alongside the body. Cosmetic relative to F1; recorded for completeness,
  not as a blocker.

#### Observation (not a finding): trailing em dash before a block element

`e8443ea:src/rsb/web/dashboard.js:603` renders
`` `${failedRepos.length} of ${total} repos failed to load — ${collapsibleDetailHtml("Details", detail)}` ``,
so the always-visible text ends in a dangling "— " immediately before a
block-level `<details>`. The record's report that the visible line reads
"1 of 2 repos failed to load"
(`docs/issue-38/reports/implementation.md:141-142`) is accurate as a
substring claim. This is cosmetic, affects no acceptance criterion, and is
noted only so the reading is on the record.

## What could not be verified

- **Anything requiring a rendered page.** AC1's 390px horizontal-scroll
  outcome, AC4's rendered pixel geometry, and AC7's 1440px density
  regression are layout facts. No browser is available here, and this
  role's contract prohibits re-running the observed role's code in any
  case — so these are reported as mechanism-present /
  outcome-unestablished, never as measurements.
- **Anything requiring assistive technology.** AC3's actual announcement
  behavior needs a real screen reader. Attribute presence and focus wiring
  are established from the diff; announcement is not.
- **Every re-executable result the observed role reports.** `57 passed`,
  `node --check`, and all four jsdom scripts
  (`docs/issue-38/reports/implementation.md:187-196`, `:255-267`) are
  recorded here as **claimed by the observed role**, with the
  re-execution prohibition as the stated reason. Their internal
  consistency was checked (F2); their truth was not, and could not be,
  tested here.
- **The real evaluation of `window.matchMedia(WIDE_LAYOUT_QUERY)`.** The
  observed role's harness polyfilled it
  (`docs/issue-38/reports/implementation.md:119-123`), so AC2's wiring is
  established from the code at `e8443ea:src/rsb/web/dashboard.js:485`
  while the media query's real behavior at a real viewport width is
  established by nobody.
- **The parallel step-2 `conformance-review` role's work on issue #38**,
  and issue #36 / PR #37 on their own merits — out of scope per this
  role's proposal §3. Issue #36 was read here only for the AC8
  closing-keyword check.

## Upstream basis

- Issue #38 (body, nine acceptance criteria, 실행 계획 naming `step 1
  implementation` and `step 2 execution-observation ‖ conformance-review`)
  — the requirement this observation measures against.
- `docs/issue-38/proposals/execution-observation.md` @ `c037c65` — this
  role's own approved phase-1 proposal; §0 fixed the three verdict levels
  and their evidence, §1 the static-tracing method, §2 this record's
  format, §3 the exclusions.
- `docs/issue-38/reports/execution-observation/survey.md` @ `c037c65` —
  the five open questions (Q1, Q3, Q4, Q5, Q7) this record resolves at F4,
  F2, F1, the Observation, and AC1/AC4 respectively.
- `docs/issue-38/reports/execution-observation/scout-brief.md` @ `c037c65`
  — the audit frame applied to the substituted verification (judge on
  disclosure + re-assessed sufficiency), the phantom-number probe, and the
  static-CSS-readability decision for the two layout criteria.
- `docs/issue-34/reports/execution-observation.md` @ `origin/main` — the
  settled record shape this record follows.
- `docs/specs/approvers.md` @ `origin/main` — the two-account approver
  list underpinning the single-account-mode determination.

## Open findings

- **F1 — `renderErrors` leaves an always-visible error surface; AC5
  unmet.** Confirmed against `e8443ea:src/rsb/web/dashboard.js:355-365`
  and `:632`. Open: the human's decision on whether this becomes an issue.
- **F2 — unreconciled assertion counts (37 vs 40; "Three scenarios" then
  four items) in `docs/issue-38/reports/implementation.md:125,194-196,262-264`.**
  Documentation defect, no re-run implied. Open for the same decision.
- **F3 — substituted-verification disclosure is global, not
  per-criterion; the proposal's promised `.number-link` WCAG 2.5.8
  confirmation (`docs/issue-38/proposals/implementation.md:310-312`) was
  neither performed nor its non-performance named.** Open for the same
  decision.
- **F4 — PR #43's merged title still says "phase 1".** Cosmetic. Open for
  the same decision.

No finding here was fixed by this role, and none could be: this role does
not edit the observed role's `src/`, `test/`, or record, and does not file
issues.

## Open-finding resolution path

All four findings return to the human on **PR #50**
(`https://github.com/tokenmaxxxer/repo-status-board/pull/50`), this
role's own PR, in this record — the only channel this role has. Contract
v3 makes issues user-authored: if the human judges F1 valid, they file it
and it becomes a subsequent issue's `step 1`; if not, the finding closes
when PR #50 is merged or refused. This role neither files, fixes, nor
relays any of them elsewhere.

## Delivery

This record is the sole phase-2 artifact for
`issue-38/execution-observation`, committed on that branch with a
`Subject: issue-38` trailer and delivered through PR #50 against `main`.
No closing keyword for issue #38 appears in this record or in PR #50's
body — issue #38's own 실행 계획 still lists a parallel step-2
`conformance-review`, so nothing here claims the issue is resolved.

## Next steps

1. ~~Validate the phase-2 approval against `docs/specs/approvers.md` and
   the single-account-mode rule.~~ Done — `issuecomment-5175886254`.
2. ~~Read PR #43, both commits, and the observed role's record and
   phase-1 artifacts first-hand.~~ Done — see "What was read first-hand".
3. ~~Render the three-level verdict with adjacent citations.~~ Done —
   outcome (8 of 9 ACs), trajectory (sound), step (F1–F4).
4. ~~Commit this record on `issue-38/execution-observation` and push to
   PR #50.~~ Done with this commit.
5. Human judgment on F1–F4 at PR #50 — this role takes no further action.
