# Conformance-review proposal (issue #38)

Scope: check the landed implementation of issue #38 — the phase-2 half of
merged PR #43, squashed as commit `f353910` on `main`, touching
`src/rsb/web/dashboard.js`, `dashboard.css`, `index.html`,
`docs/specs/screen-spec.md`, `docs/specs/design-system.md`, and
`test/rsb_tests/test_model.py` — against issue #38's 9 acceptance-criteria
checkboxes, working from the artifact and the issue text directly per this
role's phase-2 mandate, deliberately without reading
`docs/issue-38/reports/implementation.md` as authority for what was built.
That self-report exists (`docs/issue-38/reports/implementation.md`) and is
read in exactly one place: R9, where the issue's own criterion makes the
record's *content* the thing being checked.

Current-state survey: `docs/issue-38/reports/conformance-review/survey.md`.
Scout brief: `docs/issue-38/reports/conformance-review/scout-brief.md`.

## Method

Phase 2 produces `docs/issue-38/reports/conformance-review.md` as a
per-requirement verdict record via `review-traceability`'s `finding-record`
skill: one row per requirement below, verdict ∈ {Present, Surface, Absent,
Incorrect, Unverifiable}, an evidence pointer (`path:line` or test name), and a
rationale. `review-severity`'s `severity-classification` is applied only to
findings that are not Present, if any survive.

**Sampling derivation: none — full census.** The artifact is a ~230-line net
diff across three web-asset files plus two spec files; every touched line is in
scope and each of the 9 criteria maps onto a bounded set of named symbols. A
representative-sample step (WCAG-EM step 3) exists to make site-wide audits
tractable and has no work to do on a single-page dashboard; recording the
derivation rather than silently skipping it is the point.

**Evidence classes.** Every verdict carries one, because determinacy differs
sharply by criterion:

- **A — rendered measurement** (viewport at a stated width, computed geometry,
  screen-reader announcement). *Not available in this environment*: no browser,
  no Playwright/Puppeteer/Selenium, and jsdom implements no layout engine, so
  `getBoundingClientRect`/`offsetWidth` return zeros. Installing a browser stack
  to close this is deliberately out of scope — the harness decision belongs to
  issue #44, and a review that modifies the repo in order to grade it stops
  being independent.
- **B — automated assertion** (pytest suite, incl. `test_model.py`'s two new
  tests). Available and cheap; the survey records the working invocation.
- **C — source inspection** at `path:line`.

A requirement reachable only by class A is verdicted **Unverifiable**, never
guessed favourably, and its verdict names the artifact that would settle it. A
requirement whose *structural precondition* is class-C-checkable but whose
*observable outcome* is class A is split into two sub-facts so the determinable
half still gets a real verdict — this split is why the list below is finer than
the checkbox list.

**Yardstick independence rule.** `f353910` edited `screen-spec.md` and
`design-system.md` in the same commit as the code under review, and those edits
are where R1–R6's precise technical shape (the `<tr colspan>` insertion rule,
the 24×24 guarantee, the `aria-busy`/`aria-live` placement, the summary+
collapsed-`<details>` error structure) is stated. Spec text authored alongside
the code it describes cannot serve as the independent yardstick for that code:
both can encode the same misreading. Phase 2 therefore grades R1–R6 against
(a) issue #38's checkbox wording, which predates the commit, and (b) only the
portions of the spec files **unchanged** by `f353910` (`breakpoint-lg` = 1200px,
the four-table Repo-first-column rule, the token architecture). The
commit-added spec sentences are treated as *the author's stated intent*, useful
for locating what to look at, never as proof that the criterion was met. Where
an added spec sentence is materially narrower than the criterion it claims to
satisfy, that narrowing is itself a finding (see R5d).

## Requirement list

R-numbers follow the order of issue #38's acceptance-checkbox list. No verdicts
are assigned here; the decomposition is the phase-1 deliverable.

**R1 — 390px 에서 페이지 본문이 가로 스크롤되지 않고 표만 개별 스크롤된다.**
- R1a: at 390px the page body produces no horizontal scroll (class A).
- R1b: the *structural precondition* for R1a — every element on the grid/flex
  ancestor chain from `#main-content` down to `.table-scroll` carries an
  explicit `min-width: 0`, defeating the `min-width: auto` default that is the
  standard cause of this overflow class (`dashboard.css:372-374`; class C).
- R1c: each `.table-scroll` wrapper scrolls its own table independently
  (`dashboard.css:205`, `table.data-table { min-width: 640px }` at `:181`;
  class C for the rules, class A for the behaviour).
- R1d: R1a and R1c can diverge — tables can scroll correctly while the page
  still overflows, and vice versa; each needs its own observation, not one
  combined glance.
- R1e: the `min-width: 640px` floor does not itself introduce overflow at a
  width where the content would otherwise fit (interacts with R7).

**R2 — <1200px 에서 상세가 선택 행 바로 아래에 나타난다.**
- R2a: below 1200px, activating a `row-toggle` inserts the detail as a `<tr>`
  immediately following the selected row's `<tr>` rather than into the fixed
  slot (`dashboard.js:519-525`, `:464-466`).
- R2b: at/above 1200px the same interaction still renders into `DETAIL_SLOT`
  (`dashboard.js:520-521`, `WIDE_LAYOUT_QUERY` at `:16`) — split from R2a
  because a boundary-condition error breaks exactly one side.
- R2c: the inserted row's `colspan` equals the selected row's real column count
  (`dashboard.js:524`). Note the landed test
  `test_dashboard_js_detail_row_html_wraps_content_in_a_tr_with_colspan`
  (`test/rsb_tests/test_model.py`) exercises `detailRowHtml`'s formatting only,
  not that `applySelectionLayout` passes a correct count for a real row — so a
  passing test is not evidence for R2c.
- R2d: when the toggled row cannot be uniquely located (`matchCount !== 1`),
  the code falls back to `DETAIL_SLOT` rather than dropping the panel or
  attaching it to the wrong row (`dashboard.js:493-514`).
- R2e: `WIDE_LAYOUT_QUERY` is live — the issue records it as a dead constant
  before this change, so "the constant is now referenced" and "the branch it
  gates is reached" are separate facts.

**R3 — 로딩·오류·상세 열림이 스크린리더에 전달된다(live region/포커스 이동).**
Three states × two mechanisms; a subset can work while another silently does not.
- R3a: loading→loaded text change is announced from a live region present in
  the *initial* HTML (`index.html:13`), not one created at announce time — a
  region injected when the message arrives is a known non-announcement.
- R3b: that region is **empty at page load** and receives text only afterwards.
- R3c: `#main-content` brackets each load with `aria-busy` true→false
  (`index.html:24`, `dashboard.js:138,170,615,644`).
- R3d: the full-page error carries `role="alert"` (`dashboard.js:162`).
- R3e: the partial-failure banner's `aria-live` is static in `index.html:20`,
  present and empty at load (same reasoning as R3a/R3b).
- R3f: opening a detail moves focus to `<h2 id="detail-panel-heading"
  tabindex="-1">` (`dashboard.js:568-569`).
- R3g: closing a detail returns focus to the originating `row-toggle`
  (`dashboard.js:562-566`) — a separate code path from R3f.
- R3h: the stale-selection branch (`dashboard.js:444`) also carries the
  `detail-panel-heading` focus target, so R3f holds on that path too.
- R3i: actual assistive-technology announcement (class A) — distinct from
  R3a–R3h, which are all class C.

**R4 — 모바일에서 모든 인터랙티브 컨트롤이 최소 24×24px.**
Checked per control, and with the criterion's standard exceptions rather than as
a bare `min-*` grep: a target under 24×24 still conforms if it is Inline (within
a sentence/text block), Essential, or passes the **spacing** test (a 24px-diameter
circle centred on each undersized target intersects no other target or circle).
- R4a: `.row-toggle` ≥ 24×24 (`dashboard.css:223-224`).
- R4b: `.refresh-button` — `min-height: 24px` is set, `min-width` is not
  (`dashboard.css:114-124`); width is content-derived, so this is class A.
- R4c: `#repo-filter` — same shape (`dashboard.css:137-143`), native `<select>`.
- R4d: `#retry-button` (`dashboard.js:166`) — inherits R4b's rules but lives
  only on the error branch, so it is a separate observation.
- R4e: `#partial-retry` (`dashboard.js:604`) is styled by
  `.partial-banner button.link` (`dashboard.css:302-310`) with `padding: 0` and
  **no min-height/min-width at all** — a distinct rule set, not covered by R4b.
- R4f: inline link targets (`.number-link` and the external repo links) —
  determine whether each falls under the Inline exception or is a bare
  under-size failure; the issue's P2-5 measured the external link at 8×17px.
- R4g: scope reconciliation — the checkbox says *every* interactive control,
  while the commit-added `design-system.md` §5 text names only three. Under the
  independence rule the checkbox wins; the narrowing is recorded, not adopted.

**R5 — 부분/전체 오류가 요약+접힌 상세 구조이고 내부 경로를 노출하지 않는다.**
- R5a: the partial banner renders an always-visible `{M} of {N}` summary plus a
  collapsed `<details>` (`dashboard.js:601-606`, `:474-476`).
- R5b: the full-page error renders a generic summary plus a collapsed
  `<details>` (`dashboard.js:161-168`).
- R5c: neither `<details>` carries `open` (`dashboard.js:475`).
- R5d: internal paths are not exposed. The messages plumbed in
  (`dashboard.js:578,600,653,661`) are HTML-escaped, not path-redacted, and
  their content originates upstream in `rsb.fetch` — so this sub-fact must
  determine whether "collapsed" is being treated as equivalent to "not
  exposed." The commit-added `screen-spec.md` §2.5 phrasing ("no longer expose
  themselves *at a glance*") is materially narrower than the criterion's
  unqualified wording; per the independence rule the criterion governs and the
  narrowing is itself reportable.
- R5e: the duplicate-`<h1>` defect the issue names under P2-6 (header `h1` plus
  error `h1`) is gone — a distinct fact from R5b's structure.

**R6 — 표에 caption/th scope 가 있고 선택 행이 시각적으로 구분된다.**
- R6a: all four tables have a `<caption>` — checked at each call site
  (`dashboard.js:622,626,630,339` against `renderTable`'s `:183`), four facts,
  since one caller can omit the argument.
- R6b: the caption is `visually-hidden` (`dashboard.css:89-99`) — recorded
  because a sighted spot-check would not find it, and because "has a caption"
  and "the caption is perceivable to the intended audience" differ.
- R6c: every `<th>` carries `scope="col"` (`dashboard.js:177`).
- R6d: the selected row is visually distinguished (`tr.selected-row`,
  `dashboard.js:486,516`, `dashboard.css:197-199`) — class C for the rule,
  class A for whether it is distinguishable from `tr:hover` (`:192-194`).
- R6e: the highlight survives a re-render (select a row, Refresh, confirm it
  persists on the same logical row) — class A.

**R7 — 기존 테스트 전부 통과, 1440px 기본 화면 밀도에 회귀 없음.**
- R7a: every test that existed before `f353910` passes after it (class B).
- R7b: the two tests this commit added pass (class B) — separated because
  "기존" names pre-existing tests only, and a commit cannot discharge this
  criterion with its own new tests.
- R7c: the 8 `test_dashboard_dom.py` tests are **not** part of this artifact —
  they landed later with issue #44 (`b2f6b63`) and skip without jsdom; whether
  they run at all is not evidence about `f353910`.
- R7d: 1440px density is unchanged (class A). Flag for reconciliation:
  `color-border-default` changed `neutral-300`→`neutral-500`
  (`dashboard.css:20`), which is visible at every width including 1440px —
  whether an intended P3-8 contrast fix counts as a density regression is a
  judgment the record must state, not assume.

**R8 — 주의: PR 본문에 closing 키워드 금지 (issue #23 T2).**
- R8a: PR #43's body contains no auto-close keyword bound to an issue reference
  — checked against the PR body text itself (`gh pr view 43`), not against any
  repo file, and not against the merge-commit body's "References #38".
- R8b: this session's own PR body is subject to the same rule.

**R9 — 주의: DOM 배선 변경은 브라우저 실제 조작으로 확인하고 record 에 기재.**
- R9a: the record documents browser-operated confirmation of the wiring this
  commit introduces — the `matchMedia` layout branch, open/close focus
  movement, the `aria-busy` lifecycle, the static live regions.
- R9b: that documentation exists in `docs/issue-38/reports/implementation.md`.
- R9c: it names *which* behaviours at *which* viewports, enough to separate
  "checked" from "assumed."
- R9d: the confirmations are about behaviour (interaction → observed DOM/focus
  change), not element presence — the exact failure mode the criterion cites
  issue #29 for having produced twice.

## Requirements traceable to spec, not to a checkbox

Recorded with verdicts but reported separately from R1–R9, since no acceptance
criterion covers them.

- S1: Refresh button `:hover`/`:focus-visible`/`:disabled` states
  (`design-system.md:176`; `dashboard.css:125-135`).
- S2: table row `:hover` state (`design-system.md:179`; `dashboard.css:192-194`).
- S3: accounting outcomes render as `.badge` chips (`design-system.md:184`;
  `dashboard.js:336`).
- S4: `.skeleton-row` height matches a real row (`design-system.md:187`;
  `dashboard.css:291`).
- S5: `color-border-default` clears the 3:1 non-text-contrast floor
  (`design-system.md:68-73`; `dashboard.css:20`) — recomputable from documented
  hex values without a browser, so class C, not class A.
- S6: repo filter border + `:focus-visible` outline (`design-system.md:177`;
  `dashboard.css:140,144-147`).
- S7: detail panel is `position: sticky` at ≥1200px (`dashboard.css:376-382`) —
  implied by the "side panel" framing, graded as implementation-only intent.

## Scope exclusions

- **P1-2 (detail-toggle wiring)** → issue #36 / PR #37, landed before `f353910`.
  Whether the toggle opens/closes at all and whether `aria-expanded` flips are
  #36's work; issue #38 only governs *where* the opened content is placed
  (R2). Phase 2 does not re-litigate open/close itself.
- **New JS test harness** → repo-wide exclusion, and `test_dashboard_dom.py`
  arrived with issue #44 after this commit (see R7c).
- **`render.py`** → untouched by `f353910`.

## Phase-2 deliverable

One file, `docs/issue-38/reports/conformance-review.md`: the verdict table over
R1–R9 (sub-facts as rows) plus S1–S7, each row carrying verdict, evidence class,
pointer, and rationale; severity bands attached only to non-Present findings;
and a short section listing every Unverifiable row with the artifact that would
settle it, so the gap is handed off as a named request rather than absorbed as a
pass. Findings are addressed to the owning role and are not fixed here.
