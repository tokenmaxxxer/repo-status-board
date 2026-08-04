# Conformance-review record (issue #38)

loop_state: reported

code_under_review: `src/rsb/web/dashboard.js`, `src/rsb/web/dashboard.css`,
`src/rsb/web/index.html`, `docs/specs/screen-spec.md`,
`docs/specs/design-system.md`, `test/rsb_tests/test_model.py`
code_sha: `f3539107628a3a519eefe2f45b0e8d6f766a7912` (PR #43, squashed onto
`main` 2026-08-03T21:25:48+09:00)

## What was done

Checked the landed implementation of issue #38 — the phase-2 half of merged
PR #43 (`f353910`) — against issue #38's 9 acceptance-criteria checkboxes,
decomposed per the approved phase-1 proposal into R1–R9 plus the seven
spec-traceable rows S1–S7. **60 rows total.** Verdicts come from direct
inspection of the artifact, a fresh local test run this session, GitHub API
state for the PR/issue, and contrast recomputation from the CSS file's own
hex values — not from `docs/issue-38/reports/implementation.md`'s
self-report, which is read as a verdict source in exactly one place (R9,
where issue #38's own criterion makes that record's *content* the thing
being checked).

Headline: the P1-3 narrow-layout insertion (R2), the `aria-busy`/focus/
live-region wiring (R3), the table semantics (R6a–c), and the P3-8 visual
states (S1–S7) landed as specified. Four criteria are not met as written —
error-path internal-path exposure (R5), touch targets outside the three
controls the commit named (R4), the selected-row highlight's actual visual
distinctness (R6d), and the browser-operation clause of R9 — and one defect
is introduced by this change itself: below 1200px the toggle's
`aria-controls` points at the now-empty side-panel slot rather than at the
row it actually opened (R2f).

**Row-count note.** The approved proposal itemizes R1a–R9d plus S1–S7. This
record scores 60 rows: it folds the proposal's R1d (a methodology
instruction — "grade R1a and R1c separately", which is done) into prose
rather than scoring it as a requirement, and adds eight rows the artifact
forced into existence: R1f, R2f, R2g, R4e2, R4h, R4i, R5f, R9e. Each
addition is named at its section. No proposal row was dropped.

## Why

Issue #38's execution plan puts conformance-review in step 2, after the
implementation landed, and the issue itself explains why the check is worth
running: its own body records that issue #29's acceptance criterion
"좁은 화면에서 페이지 본문이 가로 스크롤되지 않는다" had been accepted while
being unmet in practice, and that issue #29 landed markup without wiring on
two separate occasions. This role's job is therefore a per-requirement
verdict against the specification as written — not a code-quality opinion,
and not a fix.

## Upstream basis

Rests on `docs/issue-38/proposals/conformance-review.md` (this role's
approved phase-1 proposal) and
`docs/issue-38/reports/conformance-review/survey.md` +
`.../scout-brief.md`, approved via issue #38 comment
`APPROVE issue-38/conformance-review` (jjongkwann, listed in
`docs/specs/approvers.md`; single-account mode, PR author == approver, so
the exact-string issue-comment path of contract v3 s19 applies — string
equality confirmed, not prose-interpreted). No `src/` or `test/` file is
changed by this record; findings are reported, never fixed here.

**Method.** `review-traceability`'s `finding-record` verdict set (Present /
Surface / Absent / Incorrect / Unverifiable), one row per requirement, each
carrying a `spec_ref`, an evidence pointer, and a rationale.
`review-severity`'s `severity-classification` is applied to the 13
Surface/Absent/Incorrect rows using this repo's precedent four-band lookup
(`docs/issue-4/reports/conformance-review.md`,
`docs/issue-29/reports/conformance-review.md`): **Blocking** (defeats the
requirement's purpose or misleads the operator), **Major** (spec violation,
user-visible, doesn't defeat the requirement's core purpose), **Minor**
(spec violation, cosmetic/non-blocking), **Note** (not itself a proven
violation — an observation worth flagging). Unverifiable rows carry no
band: an unmeasured requirement is not a graded defect, and inventing a
severity for one would be the favorable guess this role is forbidden.

**Evidence classes**, per the approved proposal. **A** — rendered
measurement (viewport at a stated width, computed geometry, AT
announcement): *not available in this environment* (no browser; headless
Chrome fails with crashpad permission errors, reconfirmed by the building
role at `docs/issue-38/reports/implementation.md:104-111`; jsdom implements
no layout engine and no `matchMedia`). **B** — automated assertion. **C** —
source inspection at `path:line`, including arithmetic recomputable from
values the source itself states. A requirement reachable only by class A is
**Unverifiable**, never guessed favorably, and its row names the artifact
that would settle it (see "Unverifiable rows" below).

**Test run this session.**
`python3 -c "import sys; sys.path.insert(0,'src'); import pytest;
sys.exit(pytest.main(['test/','-q','-rs']))"` → **57 passed, 8 skipped** in
3.29s. All 8 skips are `test/rsb_tests/test_dashboard_dom.py:65`, "jsdom is
not installed; run `npm install --prefix test` first"; `test/node_modules/`
is absent.

**Yardstick independence.** `f353910` edited `screen-spec.md` and
`design-system.md` in the same commit as the code they describe, so those
added sentences cannot serve as the yardstick for that code — both can
encode the same misreading. R1–R6 are graded against (a) issue #38's
checkbox wording, which predates the commit, and (b) only the portions of
the spec files **unchanged** by `f353910`. Commit-added spec text is used to
locate what to look at, and where it is materially narrower than the
criterion it claims to satisfy, the narrowing is itself recorded (R4g,
R5d). Two unchanged spec passages carried real weight as independent
yardstick: `design-system.md:69-70`'s adoption of the 3:1 WCAG 1.4.11
non-text-contrast floor (bears on R6d) and `screen-spec.md:143-146`'s §1.9
Errors panel, confirmed untouched by the diff — the hunk boundaries
`@@ -94,11 +104,24 @@` and `@@ -132,6 +155,12 @@` bracket it without
covering it (bears on R5f).

## Verdict summary

| Verdict | Count |
|---|---|
| Present | 41 |
| Surface | 6 |
| Absent | 4 |
| Incorrect | 3 |
| Unverifiable | 6 |
| **Total** | **60** |

Severity of the 13 non-Present, non-Unverifiable rows: Blocking 1, Major 7,
Minor 3, Note 2.

## R1 — 390px 에서 페이지 본문이 가로 스크롤되지 않고 표만 개별 스크롤된다

`spec_ref`: issue #38 acceptance checkbox 1; `screen-spec.md:72-77` (§1.3,
unchanged clause: "there is no page-level horizontal scroll").

Per the proposal's R1d, the page-level fact (R1a) and the per-table fact
(R1c) are graded as separate observations, since tables can scroll
correctly while the page still overflows and vice versa.

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R1a: at 390px the page body produces no horizontal scroll | Unverifiable | class A — no layout engine in this environment; `docs/issue-38/reports/implementation.md:104-111` (headless Chrome crashpad failure), no Playwright/Selenium/Puppeteer | Rendered/scrollable width at a stated viewport is not computable from source; recorded as unsettled rather than inferred from the CSS that is supposed to prevent it |
| R1b: the `min-width: 0` clamp covers the actual grid-item chain | Present | `dashboard.css:361-365` (`#page-body { display: grid; grid-template-columns: 1fr }`), `:372-374` (`#main-content, #detail-panel-slot { min-width: 0 }`); `index.html:23-25` | `#page-body`'s only two grid items are exactly the two selectors clamped, so the `min-width: auto` default that causes this overflow class is defeated at the one place it applies; `section.region` and `.table-scroll` below them are block boxes, where `min-width: auto` does not apply |
| R1c: each `.table-scroll` scrolls its own table independently | Present | `dashboard.css:205` (`overflow-x: auto; width: 100%`), `:177-186` (`table.data-table { min-width: 640px }`); emitted for all four tables by the single `renderTable` at `dashboard.js:188` | One emitter wraps every table, so the per-table scroll container is structurally universal; `width: 100%` keeps the wrapper itself from inflating past its parent. Rendered scroll behaviour is class A |
| R1e: the `min-width: 640px` floor does not itself create overflow where content would fit | Present | `dashboard.css:181` inside the `.table-scroll` wrapper at `:205`; column counts at `dashboard.js:622,626,630,339` (7/6/7/5 columns) | The floor's effect is contained inside the scroll wrapper and cannot reach the page body; and no table has fewer than 5 columns, so none would have fitted 390px unclamped. The code's own comment marks 640px a first-attempt value |
| R1f: no *other* container on the page can inflate the body at 390px | Unverifiable | `dashboard.css:102-108` (`.page-header { display: flex; flex-wrap: wrap }`), `:150-155` (`.summary-strip { display: flex; flex-wrap: wrap }`) — neither's items carry `min-width: 0` | Two flex containers sit outside `#page-body` and were not part of the fix. `flex-wrap: wrap` lets items reflow but does not break *within* an item, so a single long unbroken token (a long repo name in a chip) could still exceed 390px. Whether real content does needs class A. Added row — the proposal's R1b scoped the chain to `#main-content`→`.table-scroll` only |

## R2 — <1200px 에서 상세가 선택 행 바로 아래에 나타난다

`spec_ref`: issue #38 acceptance checkbox 2; `screen-spec.md:104-111` (§1.6).

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R2a: below 1200px the detail is inserted as a `<tr>` immediately after the selected row | Present | `dashboard.js:519-525`, esp. `:524` `selectedRow.insertAdjacentHTML("afterend", detailRowHtml(...))`; `detailRowHtml` at `:464-466` | `afterend` on a `<tr>` places a sibling `<tr>` in the same `<tbody>` — DOM-order-adjacent to the selected row, which is what the criterion asks for. Replaces the pre-#38 unconditional `DETAIL_SLOT.innerHTML` path |
| R2b: at/above 1200px the same interaction still renders into the slot | Present | `dashboard.js:520-521`; `WIDE_LAYOUT_QUERY = "(min-width: 1200px)"` at `:16`, matching `dashboard.css:376`'s `@media (min-width: 1200px)` | The JS constant and the CSS breakpoint are the same literal, so the layout switch and the media query cannot disagree at the boundary. Graded separately from R2a because a boundary error breaks exactly one side |
| R2c: the inserted row's `colspan` equals the row's real column count | Present | `dashboard.js:524` (`selectedRow.children.length`); row construction at `:182` (`<tr>${r.cells.join("")}</tr>`), one `<td>` per cell, no `colspan` on any cell | The count is read off the live row rather than assumed, so it tracks whichever of the four tables the row came from. Note the landed test `test_dashboard_js_detail_row_html_wraps_content_in_a_tr_with_colspan` (`test/rsb_tests/test_model.py:339-347`) exercises `detailRowHtml`'s string formatting only — it passes a hard-coded `5` and is *not* evidence for this row |
| R2d: an ambiguous row match falls back safely | Present | `dashboard.js:493-514`, esp. `:512-514` (`if (matchCount !== 1) selectedRow = null`) and `:520` | `(sourceTable, issue, repo)` is not a unique row key — the Sessions table can hold several rows per pair — and the code detects that rather than guessing, degrading to the side-panel slot with no highlight instead of attaching the panel to an arbitrary row |
| R2e: `WIDE_LAYOUT_QUERY` is live, and the branch it gates is reached | Present | `dashboard.js:520` (sole reference, per a whole-file grep); `applySelectionLayout` called unconditionally from `renderData` at `:642` | The issue records this constant as dead before the change. It is now read on every render, so the narrow branch is reachable on every data render, not only on a code path some other condition might never enter |
| R2f: the toggle's `aria-controls` names the container that actually opened | **Incorrect** | `dashboard.js:238` (`aria-controls="detail-panel-slot"`, fixed literal) against `:523` (`DETAIL_SLOT.innerHTML = ""`) and `:524` (content inserted into the table instead) | Below 1200px this change empties the slot and puts the panel in a new `<tr>`, but every toggle still points `aria-controls` at `detail-panel-slot`. A screen-reader user following the control's own pointer lands on an empty `<div>` while the content sits elsewhere in the DOM. Added row: `aria-controls` was wired by issue #36, but the condition that makes it wrong is created here, and issue #38 owns *where* the opened content is placed |
| R2g: the panel visually lands below the row with no overlap/clipping at 1024px | Unverifiable | class A — see R1a. `test_dashboard_dom.py` does not exercise this branch (no `matchMedia` coverage) | DOM insertion order is settled (R2a); rendered geometry is not. The issue's own P1-3 defect was a *positional* one (282px vs 1190px), so the visual claim is the half that mattered and it remains unmeasured here |

`spec_vs_built` (R2f) — **Spec**: `screen-spec.md:104-111` states the panel
content is inserted after the selected row below `breakpoint-lg` and the
side-panel slot "stays empty at that width", while `:114-120` requires the
panel be reachable by landmark/heading navigation. **Built**: the content
moves, the `aria-controls` reference does not, so the programmatic
relationship points at the element the spec says is deliberately empty.

## R3 — 로딩·오류·상세 열림이 스크린리더에 전달된다 (live region/포커스 이동)

`spec_ref`: issue #38 acceptance checkbox 3; `screen-spec.md:191-192`
(§2.4), `:198-200` (§2.5), `:218-227` (§2.6).

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R3a: the header live region is present in the *initial* HTML | Present | `index.html:13` (`<span id="header-meta" class="text-secondary" aria-live="polite">`) | The region is parsed with the document rather than created at announce time — the known non-announcement failure mode — so later `textContent` writes are observed by the AT |
| R3b: that region is empty at page load and receives text only afterwards | **Surface** | `index.html:13` ships the literal `Loading…` inside the live region; `dashboard.js:139` writes the same literal `"Loading…"` in `renderSkeleton` | The region is live but its initial state is parse-time content, and the first render writes a string identical to it, so no mutation occurs and no polite announcement is queued for the *initial* loading state. Later transitions do announce (loaded→"Loading…" on Refresh, "Loading…"→"as of …" on completion). The loading state is still conveyed statically and via `aria-busy` (R3c), so this is a shape mismatch, not a broken requirement — severity **Note** |
| R3c: `#main-content` brackets each load with `aria-busy` true→false | Present | `index.html:24` (initial `aria-busy="true"`); `dashboard.js:138` (true), `:170`, `:615`, `:644` (false); `load()` at `:647-665` | Every exit from `load()` routes through one of the three false-setters — full error, empty page, normal render — so the attribute cannot be left stuck true on any path, including the `catch` at `:660-661` |
| R3d: the full-page error carries `role="alert"` | Present | `dashboard.js:162` (`<div class="error-state" role="alert">`) | For `role="alert"` creation-at-announce-time is the correct pattern — insertion is what triggers the announcement — so the R3a reasoning does not apply here in reverse |
| R3e: the partial-failure banner's live region is static and empty at load | Present | `index.html:20` (`<div id="partial-banner" aria-live="polite"></div>`) | Present at parse, genuinely empty, filled only when a partial failure occurs (`dashboard.js:601-608`) — so the banner's *appearance* is the mutation that gets announced |
| R3f: opening a detail moves focus to the panel heading | Present | `dashboard.js:567-570`; target `<h2 id="detail-panel-heading" tabindex="-1">` at `:449` | `tabindex="-1"` makes the heading programmatically focusable, and focus is set after `renderData` has rebuilt the DOM, so it targets the live node rather than a detached one |
| R3g: closing returns focus to the originating toggle | Present | `dashboard.js:561-566` — `wasExpanded` captured before the re-render, then the button re-queried by `(table, issue, repo)` and focused | A separate code path from R3f, and correctly re-queried: the original button object is destroyed by the `MAIN.innerHTML` rewrite, so focusing the captured reference would silently do nothing |
| R3h: the stale-selection branch also carries the focus target | Present | `dashboard.js:444` (`<div class="detail-panel text-secondary" id="detail-panel-heading" tabindex="-1">`) | The empty-state branch carries the same id and `tabindex`, so `getElementById` at `:568` resolves and R3f holds when the selected issue no longer has board activity |
| R3i: actual assistive-technology announcement | Unverifiable | class A — no AT, no accessibility tree, no announcement queue available here | R3a–R3h are all class-C attribute facts. That the attributes are right does not establish that VoiceOver/NVDA/JAWS actually announce; recorded as unsettled |

Cross-reference: R2f is also an R3-class defect — below 1200px the
programmatic relationship a screen-reader user follows from the toggle
points at the empty slot. It is scored once, under R2.

## R4 — 모바일에서 모든 인터랙티브 컨트롤이 최소 24×24px

`spec_ref`: issue #38 acceptance checkbox 4 (and P2-5 in the issue body,
which names the measured failures: issue button 25×17px, external link
8×17px, filter height 19px). Graded with WCAG 2.5.8's standard exceptions
(Inline, Essential, and the spacing test — a 24px-diameter circle centred on
each undersized target intersecting no other target or circle), not as a
bare `min-*` grep.

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R4a: `.row-toggle` ≥ 24×24 | Present | `dashboard.css:223-224` (`min-width: 24px; min-height: 24px`) with `display: inline-flex` centring at `:225-227` | Both axes are declared, and `inline-flex` makes the box honour them despite the glyph being font-sized. This is the control the issue measured at 25×17px |
| R4b: `.refresh-button` ≥ 24×24 | Present | `dashboard.css:114-124` (`min-height: 24px`, `padding: var(--space-2) var(--space-3)` = 8px/12px); label "Refresh" at `index.html:17` | `min-width` is not declared, so width is content-derived — but a "Refresh" text label plus 24px of horizontal padding cannot render under 24px wide in any font this page could load. Reasoned from source, not measured; the measured form is class A (R4h) |
| R4c: `#repo-filter` ≥ 24×24 | Present | `dashboard.css:137-143` (`min-height: 24px`); native `<select>` with the "All repos" option at `index.html:14-15` | Same shape as R4b: height declared, width content-derived, and a native select's option text plus its dropdown chrome exceeds 24px. This is the control the issue measured at 19px tall |
| R4d: `#retry-button` ≥ 24×24 | Present | `dashboard.js:166` (`class="refresh-button"`) → `dashboard.css:114-124` | Inherits R4b's rule set including `min-height: 24px`; graded separately because it exists only on the full-error branch |
| R4e: `#partial-retry` ≥ 24×24 | **Absent** | `dashboard.js:604` (`<button class="link" id="partial-retry">Retry</button>`) styled solely by `dashboard.css:302-310` (`padding: 0; font: inherit`, **no** `min-height`/`min-width`) | A distinct rule set the 24×24 work never touched: with zero padding the box collapses to one inherited line box, well under 24px tall. WCAG 2.5.8's Inline exception does not rescue it — the preceding `<details>` (`dashboard.js:603`) is a block box and no rule makes it inline, so this button starts its own line rather than sitting in a sentence. Severity **Major** |
| R4e2: the two `<summary>` disclosure controls ≥ 24×24 | **Absent** | `dashboard.css:311-313` (`.partial-banner summary`) and `:329-332` (`.error-state details summary`) — both declare only `cursor` and `margin` | `<summary>` is an interactive disclosure control and therefore a target. Both are full-width (horizontal axis passes) but line-height tall, so the vertical axis fails. Added row, and the sharpest one: these targets *did not exist before this commit* — the same P2-6 change that added them is in the same commit as the P2-5 work that was supposed to guarantee 24×24 |
| R4f: inline link targets (`.number-link`, external repo links) | **Absent** | `dashboard.css:248-259` (no `padding`, no `min-*`); `dashboard.js:226` (`<a class="number-link" … target="_blank">#{n}</a>`); container `.issue-cell` at `dashboard.css:237-242` (`display: inline-flex; gap: var(--space-1)` = 4px) | Nothing in the diff changed link sizing, so the issue's own 8×17px measurement stands unrefuted. The Inline exception is arguable for a link in a text cell; the spacing test is not — the link sits 4px from the 24×24 `.row-toggle` in the same `.issue-cell`, so a 24px circle centred on the link necessarily intersects the button's target. Severity **Major** |
| R4g: scope — the criterion says *every* interactive control | **Incorrect** | `design-system.md:161-167` (commit-added): "every interactive control (`row-toggle`, `repo-filter`, `refresh-button`) now guarantees a 24×24px minimum touch target" | The parenthetical redefines "every" as those three, in the same commit as the code, and R4e/R4e2/R4f are the controls that fall outside it. Under the independence rule the checkbox governs; the narrowing is recorded, not adopted. Severity **Minor** |
| R4h: rendered geometry at a mobile viewport | Unverifiable | class A — `getBoundingClientRect()` needs a layout engine | R4a–R4d are reasoned from declarations, and the building role's own record (`docs/issue-38/reports/implementation.md:161-166`) discloses that its P2-5 check was a `grep`, not a measurement. Neither establishes rendered pixel geometry |
| R4i: the cited success criterion | **Incorrect** | `dashboard.css:220-222` ("guarantee the 24x24px **WCAG 2.5.5** touch target") | 24×24 is SC 2.5.8 Target Size (Minimum), AA in WCAG 2.2. SC 2.5.5 Target Size (Enhanced) is the 44×44 AAA criterion — which this code does not meet and was never asked to. Cosmetic in effect but it misdirects the next reader auditing against the wrong bar. Severity **Note** |

`spec_vs_built` (R4g) — **Spec/criterion**: issue #38 checkbox 4,
"모바일에서 **모든** 인터랙티브 컨트롤이 최소 24×24px". **Built**: three
controls sized, plus a spec sentence added in the same commit that defines
"every interactive control" as exactly those three.

`spec_vs_built` (R4i) — **Spec**: a 24×24px minimum, which is WCAG 2.2 SC
2.5.8 Target Size (Minimum), AA. **Built**: the implementing comment cites
SC 2.5.5 Target Size (Enhanced), the 44×44 AAA criterion.

## R5 — 부분/전체 오류가 요약+접힌 상세 구조이고 내부 경로를 노출하지 않는다

`spec_ref`: issue #38 acceptance checkbox 5; `screen-spec.md:143-146` (§1.9,
**unchanged** by this commit), `:182-193` (§2.4), `:195-215` (§2.5).

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R5a: the partial banner is an always-visible summary plus a collapsed `<details>` | Present | `dashboard.js:601-606`, esp. `:603` (`${failedRepos.length} of ${total} repos failed to load — ${collapsibleDetailHtml("Details", detail)}`); helper at `:474-476` | The count line is outside the disclosure and the per-repo strings are inside it, which is the structure the criterion names. Closes the gap `docs/issue-29/reports/implementation.md` left open |
| R5b: the full-page error is a generic summary plus a collapsed `<details>` | Present | `dashboard.js:161-168` — `<h2>Couldn't load board status</h2>`, `<p>The board data couldn't be loaded.</p>`, then `collapsibleDetailHtml("Details", message)` | The always-visible copy is generic and carries no upstream text; the raw joined messages moved behind the disclosure. Previously the raw message was visible `<p>` text |
| R5c: neither `<details>` is open by default | Present | `dashboard.js:475` — the emitted string is `<details><summary>…` with no `open` attribute, and it is the only `<details>` emitter | A single helper builds both, so "collapsed by default" cannot drift between the two call sites |
| R5d: internal paths are not exposed | **Surface** | `src/rsb/fetch.py:35` (`failed to launch {argv[0]!r}: {e}`), `:40` (`flows --json failed: {excerpt}` — the provider's last stderr line), returned verbatim at `:54`, `:59`, `:64`; consumed unmodified at `dashboard.js:600`, `:653`, `:661` | `collapsibleDetailHtml` escapes for HTML and hides behind a disclosure; it never redacts. The provider path is one click away, unchanged. The commit-added `screen-spec.md:188-190` narrows the claim to "no longer expose themselves *at a glance*" — materially narrower than the criterion's unqualified wording, so under the independence rule the criterion governs and the collapse alone does not discharge it. Severity **Major** |
| R5e: the duplicate `<h1>` is gone | Present | `dashboard.js:163` (`<h2>`, was `<h1>`); `index.html:12` (`<h1 id="page-title">`, the only remaining `<h1>`); `dashboard.css:324` (`.error-state h2`, the `h1` selector no longer exists) | Markup, page structure and stylesheet all moved together, so no orphaned `.error-state h1` rule can resurrect the old heading level |
| R5f: the collapsed structure actually governs what the page shows on a partial failure | **Absent** | `dashboard.js:355-365` (`renderErrors`, `<li>${escapeHtml(e.repo)}: ${escapeHtml(e.message)}</li>` at `:361`), called unconditionally at `:632` inside `MAIN.innerHTML`; styled visible at `dashboard.css:339-345` | On the partial-failure path the *same* per-repo strings the banner just collapsed are simultaneously rendered as a plain visible `<ul>` in main content, a few sections below. Every repo error — provider paths included — is in plain view, which is precisely the "부분 실패가 모든 레포 오류를 한 줄로 노출" defect the issue names under P2-6, and it defeats both halves of this criterion on that path. (The full-failure path returns early at `:579-582`, so it is unaffected.) Added row. This is not a simple oversight: `screen-spec.md:143-146` §1.9, **unchanged** by this commit and therefore valid independent yardstick, positively specifies an always-visible "{repo}: {message}" Errors panel — so the criterion and the standing spec are in direct conflict and reconciling them is a spec decision, not a one-line patch. Severity **Blocking** |

## R6 — 표에 caption/th scope 가 있고 선택 행이 시각적으로 구분된다

`spec_ref`: issue #38 acceptance checkbox 6; `screen-spec.md:53-55` (§1.3
caption/scope), `:78-81` (§1.3 selected-row highlight);
`design-system.md:68-73` (**unchanged** 3:1 WCAG 1.4.11 non-text floor).

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R6a: all four tables have a `<caption>` | Present | `dashboard.js:183,188` (emitter) against all four call sites: `:622` "Decision queue", `:626` "Flows", `:630` "Sessions", `:339` "Accounting ledger" | Checked per call site rather than at the emitter, since a caller can omit the argument — none does. A whole-file grep confirms `renderTable` is the only `<table` emitter, so there is no fifth uncaptioned table |
| R6b: the caption is visually hidden | Present | `dashboard.css:89-99` (`.visually-hidden`: absolute, 1×1, `clip: rect(0,0,0,0)`, `overflow: hidden`, `white-space: nowrap`) | The standard clip-rect technique — kept in the AT tree, out of the visual layer. Recorded because a sighted spot-check would not find these captions, and "has a caption" and "the caption is perceivable to its intended audience" are different facts |
| R6c: every `<th>` carries `scope="col"` | Present | `dashboard.js:177` — the sole `<th>` emitter, applied to every mapped header | Single emitter, so the attribute cannot be present on some tables and missing on others |
| R6d: the selected row is *visually distinguished* | **Surface** | `dashboard.css:197-199` (`tr.selected-row { background: var(--color-status-info-background) }`) = `#eff6ff` (`:29`) on the table's `--color-surface-raised` = `#ffffff` (`:19`, `:3`); and `:192-194` (`table.data-table tbody tr:hover`, `#f3f4f6` at `:4`) | The rule exists and is applied, but recomputing from the file's own hex values (WCAG relative-luminance formula, class C — no browser needed) gives **1.09:1** against an unselected row and **1.01:1** against the hover state. Two independent problems: (a) 1.09:1 is far below the 3:1 non-text floor this repo's own `design-system.md:69-70` adopts for state indicators, and is the same order as the 1.47:1 border the issue itself calls too faint under P3-8; (b) `table.data-table tbody tr:hover` has specificity 0-2-3 against `tr.selected-row`'s 0-1-1, so hovering the selected row *replaces* its highlight with the hover grey. Severity **Major** |
| R6e: the highlight survives a re-render | Present | `dashboard.js:642` (`applySelectionLayout` runs on every `renderData`), `:486` (clear), `:516` (re-apply), keyed on `(sourceTable, issue, repo)`; `selectedIssue` at `:429` is module-level and is reset only by the repo-filter handler at `:674` | Refresh wipes `MAIN` via `renderSkeleton` and rebuilds it, and the class is re-derived from `selectedIssue` rather than preserved on a DOM node, so it lands back on the same logical row. Whether it is then *seen* is R6d's problem, not this one |

## R7 — 기존 테스트 전부 통과, 1440px 기본 화면 밀도에 회귀 없음

`spec_ref`: issue #38 acceptance checkbox 7.

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R7a: every test that existed before `f353910` passes after it | Present (class B) | `git diff --numstat f353910^ f353910 -- test/` → `32 0` (additions only, zero deletions, no renames); `git diff --stat f353910 HEAD -- src/ test/` → `src/` untouched since; suite run this session: 57 passed, 8 skipped | Because the commit deleted no test line and `src/` has not moved since, the 55 pre-existing tests are exactly the run's 57 minus the 2 added, and all pass. No test was weakened or removed to make the suite green |
| R7b: the two tests this commit added pass | Present (class B) | `test/rsb_tests/test_model.py:339-347`, `:350-368`; included in the 57 | Graded separately because "기존" names pre-existing tests only — a commit cannot discharge this criterion with its own new tests. Recorded for completeness of the count, not as evidence for R7a |
| R7c: the 8 `test_dashboard_dom.py` tests are not part of this artifact | Present | `git diff --stat f353910 HEAD -- test/` shows `test_dashboard_dom.py`, `package.json`, `package-lock.json` all arriving after `f353910` (with `b2f6b63`, issue #44) | They skip for want of `test/node_modules/`, but that is issue #44's state, not evidence about this commit either way. Recorded so the 8 skips are not read as a gap in this artifact's coverage |
| R7d: 1440px density is unchanged | Unverifiable | class A — needs a rendered screenshot against a pre-#38 baseline | The reconciliation the proposal demanded, stated rather than assumed: `--color-border-default` moved `neutral-300`→`neutral-500` (`dashboard.css:20`), which is visible at every width including 1440px. This record does **not** count it as a density regression — it is the contrast fix the issue itself asks for under P3-8, and no spacing, font-size or padding token changed (`dashboard.css:42-60` untouched by the diff), so density in the sense the criterion uses it is not altered. The visual half remains unmeasured |

## R8 — 주의: PR 본문에 closing 키워드 금지 (issue #23 T2)

`spec_ref`: issue #38 acceptance checkbox 8.

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R8a: PR #43's body contains no auto-close keyword bound to an issue reference | Present | `gh pr view 43 --json body`: the only keyword tokens are "fixed **by** #36" (keyword not immediately followed by the reference, so GitHub's grammar does not link it), "findings + fixes"/"both fixed" (no reference at all), and a backticked generic `` `Closes #n` `` inside an explanatory sentence. Empirical confirmation: `gh issue view 36` → `{"state":"OPEN","closedAt":null}` and issue #38 → OPEN, both after PR #43 merged 2026-08-03 | Checked against the PR body text itself, not the merge commit's "References #38", then corroborated by outcome rather than by grammar-lawyering: had any keyword bound, GitHub would have closed #36 or #38 at merge. Neither closed. The body also states the abstention explicitly and gives the issue #23 T2 reason |
| R8b: this session's own PR body is subject to the same rule | Present | The PR body opened for this branch states "References #38" with no closing keyword | Self-applied; the criterion binds every PR on this issue, not only the implementation one |

## R9 — 주의: DOM 배선 변경은 브라우저 실제 조작으로 확인하고 record 에 기재

`spec_ref`: issue #38 acceptance checkbox 9 (citing issue #29's two
markup-landed-but-unwired cases as the failure mode to prevent).

This is the one criterion whose subject is the building role's record, so
`docs/issue-38/reports/implementation.md` is read here as the artifact
under review rather than as an account of intent.

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| R9a: the wiring was confirmed by real browser operation | **Surface** | `docs/issue-38/reports/implementation.md:104-123` — headless Chrome fails (crashpad/`ProcessSingleton` permission errors, reproduced with an explicit `--user-data-dir`), no Playwright/Selenium/Puppeteer; jsdom substituted; `:119-123` "`window.matchMedia` is not implemented by jsdom … so a minimal polyfill returning a controllable `{ matches }` was substituted for real CSS media-query evaluation" | Not Absent: real `click` events were dispatched against the real shipped `index.html`+`dashboard.js` in a real DOM and real state was read back, which is genuine behavioural exercise. But "브라우저 실제 조작" did not happen, and the substitution lands exactly on the branch that most needed it — P1-3's entire correctness rests on `matchMedia`, and `matchMedia` is the one thing the verifier hand-wrote. The limitation is disclosed honestly and prominently, which is why this is Surface and not a misrepresentation. Severity **Major** |
| R9b: the documentation exists in the record | Present | `docs/issue-38/reports/implementation.md:102-171`, a dedicated "Manual/DOM-wiring verification" section | The criterion's second clause ("record 에 기재") is met plainly: the section exists, is findable by heading, and states its own method and limits |
| R9c: it names *which* behaviours at *which* viewports | **Surface** | `:125-159` names four scripted scenarios with 18/6/9/4 checks, each stating the DOM/focus fact asserted; but a full-file search for `viewport`, `390`, `1024`, `1440` returns **no matches** | The behaviour half is met in detail — enough to tell "checked" from "assumed". The viewport half is not: wide/narrow appears only as the polyfill's boolean, so the record cannot say the narrow path was exercised at any width a user has, and the issue's P1-3 defect was measured at a specific width (1024px). Severity **Minor** |
| R9d: the confirmations are about behaviour, not element presence | Present | `:130-139` (dispatch click → assert `.selected-row` applied, `nextElementSibling` is a `tr.detail-row` containing the expected content, focus on `#detail-panel-heading`), `:134-135` (click again → slot empties, class removed, focus returns to the button) | This is the exact failure mode the criterion cites issue #29 for producing twice, and it is genuinely avoided: every claim is interaction→observed-change, not "the attribute is in the markup" |
| R9e: the touch-target claim is a confirmation | **Surface** | `:161-166` — "confirmed by direct `grep` of the shipped `dashboard.css` … rather than jsdom, since jsdom has no layout engine … an honest limitation, not a claim of visual measurement" | A grep confirms a declaration exists, not that a control renders ≥24×24 — and R4e/R4e2/R4f are precisely the controls a grep for `min-*: 24px` cannot surface, because their rule sets contain no such declaration to find. The record's own disclaimer is accurate; the gap it discloses is the one that let three undersized targets ship. Added row. Severity **Minor** |

## Spec-traceable rows (no acceptance checkbox)

Reported separately, per the approved proposal. All against
`design-system.md` §6's component inventory and §2.2's contrast floors.

| Requirement | Verdict | Evidence | Rationale |
|---|---|---|---|
| S1: Refresh `:hover`/`:focus-visible`/`:disabled` states | Present | `dashboard.css:125-127`, `:128-131`, `:132-135`; spec at `design-system.md:176` | All three states declared, focus-visible as a 2px `blue-500` outline with offset, and `load()` at `dashboard.js:648,663` actually toggles `disabled`, so the `:disabled` style has an emitter |
| S2: table row `:hover` state | Present | `dashboard.css:192-194`; spec at `design-system.md:179` | Declared. Its specificity is also what breaks R6d — recorded there, not here |
| S3: accounting outcomes render as badge chips | Present | `dashboard.js:336` (`<span class="badge status-neutral mono">`), `.badge` at `dashboard.css:269-275`; spec at `design-system.md:184` | Replaces bare `k:v` text, and the same hunk newly escapes the value (`escapeHtml(v)`), closing an injection path that had been open on the value side |
| S4: `.skeleton-row` height matches a real row | Present | `dashboard.css:291` (`calc(var(--space-table-cell-padding-y) * 2 + 1.4em)`) against the real cell padding at `:187-191`; spec at `design-system.md:187` | Derived from the same tokens the real cells use rather than a hard-coded height, so the two cannot drift apart when the token changes |
| S5: `color-border-default` clears the 3:1 non-text floor | Present | `dashboard.css:20` → `:6` (`--color-neutral-500: #6b7280`) on `:3` (`--color-neutral-0: #ffffff`) | Recomputed from those hex values: **4.83:1**, comfortably over 3:1, and a real improvement on the `neutral-300` predecessor. `design-system.md:68-69` states this pairing as 4.6:1 — the figure appears carried over from the `neutral-0`-on-`blue-500` row at `:65`. The requirement holds either way; the documented number is off by ~0.2 and is worth correcting when that file is next touched |
| S6: repo filter border + `:focus-visible` outline | Present | `dashboard.css:140` (border), `:144-147` (outline); spec at `design-system.md:177` | Both declared, matching the focus treatment used on the other controls |
| S7: detail panel is `position: sticky` at ≥1200px | Present | `dashboard.css:381`, inside the `@media (min-width: 1200px)` block opened at `:376` | Scoped to the wide layout only, consistent with the panel becoming an in-table row below that width. Rendered stickiness is class A; the rule and its scope are what is graded |

## Open findings

13 findings, all addressed to the **implementation** role (issue #38's
owning role). This role reports and does not fix; nothing below is patched
here, and no `src/`, `test/`, or `docs/specs/` file was modified by this
review.

**Blocking**

1. **R5f** — on a partial failure, every repo error string is rendered
   uncollapsed and in plain view by `renderErrors` (`dashboard.js:355-365`,
   called at `:632`) at the same time the banner collapses them, so
   acceptance criterion 5 is unmet on that path and provider paths are
   visible without interaction. Reconciling this requires a decision on
   `screen-spec.md:143-146` §1.9, which positively specifies that panel.

**Major**

2. **R2f** — below 1200px the toggle's `aria-controls="detail-panel-slot"`
   (`dashboard.js:238`) points at the element this change deliberately
   empties (`:523`), not at the inserted `<tr>` holding the panel.
3. **R4e** — `#partial-retry` has no minimum size (`dashboard.css:302-310`,
   `padding: 0`) and no applicable WCAG exception.
4. **R4e2** — both `<summary>` disclosure controls added by this commit
   (`dashboard.css:311-313`, `:329-332`) are under 24px tall.
5. **R4f** — `.number-link` and the external repo links keep the issue's
   measured 8×17px and fail the spacing test against the adjacent 24×24
   toggle (`dashboard.css:237-242`, 4px gap).
6. **R5d** — internal paths are collapsed, never redacted
   (`src/rsb/fetch.py:35,40` → `dashboard.js:600`).
7. **R6d** — the selected-row highlight is 1.09:1 against an unselected row
   and 1.01:1 against hover, and loses to `tr:hover` on specificity
   (`dashboard.css:197-199` vs `:192-194`).
8. **R9a** — DOM-wiring confirmation used jsdom with a hand-written
   `matchMedia` polyfill, not browser operation, on the branch whose
   correctness rests entirely on `matchMedia`.

**Minor**

9. **R4g** — commit-added `design-system.md:161-167` narrows "every
   interactive control" to three named controls.
10. **R9c** — the verification record names behaviours but no viewport
    widths.
11. **R9e** — the touch-target check was a grep, which structurally cannot
    surface the three controls that have no `min-*` declaration to find.

**Note**

12. **R3b** — `#header-meta` ships non-empty (`index.html:13` `Loading…`)
    and the first render writes the identical string, so the initial
    loading state is never an announced mutation.
13. **R4i** — `dashboard.css:220-222` cites WCAG 2.5.5 (44×44 AAA) for a
    24×24 target; the applicable criterion is 2.5.8.

Carried alongside, not a finding against this artifact:
`design-system.md:68-69` states the `neutral-500`-on-`neutral-0` border
pairing as 4.6:1 where recomputation gives 4.83:1 (S5). The requirement
holds either way.

## Unverifiable rows and what would settle each

Six rows could not be checked from the evidence and access available. None
is a pass; each is a named request. Every one is class A — the same single
missing capability, a real rendering engine, which this review deliberately
did not install: the harness decision belongs to issue #44, and a review
that modifies the repo in order to grade it stops being independent.

| Row | What would settle it |
|---|---|
| R1a — no page-level horizontal scroll at 390px | A browser (or working headless Chrome/Playwright) at 390px comparing `document.documentElement.scrollWidth` to `window.innerWidth` |
| R1f — no other container inflates the body at 390px | The same run, with a realistic longest-repo-name payload loaded so `.page-header` and `.summary-strip` are exercised at their widest |
| R2g — the panel lands below the row, unclipped, at 1024px | A render at 1024px with a row expanded, checking the inserted `<tr>`'s geometry against the selected row's |
| R3i — actual AT announcement of loading/error/detail-open | A VoiceOver/NVDA/JAWS session, or axe-core against a rendered page |
| R4h — rendered control geometry at a mobile viewport | `getBoundingClientRect()` on each control at 390px — which would also settle R4a–R4d as measurements rather than as reasoning |
| R7d — 1440px density unchanged | A 1440px screenshot against a pre-`f353910` baseline |

Issue #44's jsdom harness, already on `main`, cannot close any of these:
`docs/issue-44/proposals/test-authoring.md:210-218` states jsdom implements
no layout and "structurally cannot detect a CSS-overflow regression". It
could, however, close the *structural* halves of R2g and R3f–R3h with a
`matchMedia` polyfill — the same substitution R9a flags, which is
acceptable as a regression test even though it is not acceptable as the
browser confirmation criterion 9 asks for. The eight tests it landed
exercise none of this commit's additions (`test_dashboard_dom.py:128-259`).

## Next steps

1. ~~Decompose issue #38's 9 acceptance checkboxes into a scored
   requirement list.~~ Done in phase 1 (approved proposal).
2. ~~Collect evidence across the three artifact surfaces, run the test
   suite, check the PR body and the building role's record.~~ Done — see
   "Upstream basis".
3. ~~Score all 60 rows with verdict + evidence + rationale, and band the
   non-Present ones.~~ Done — see the R1–R9 and S1–S7 sections.
4. ~~Finalize this record, commit, push, report through the same PR.~~
   Finalized at `loop_state: reported`; commit/push follow immediately.
5. Remaining, and **not this role's to perform**: the 13 open findings go
   to the implementation role, and the 6 Unverifiable rows stay open until
   someone with a rendering engine settles them. This role does not fix,
   and does not re-open the artifact to re-grade it.

## Open-finding resolution path

`loop_state` stays `reported`, not `landed`: 13 findings are open and 6
rows are unsettled, and neither becomes closable by anything this role can
do.

- **Owner.** All 13 findings are addressed to the **implementation** role
  for issue #38. This role reports; it never edits the target artifact and
  never resolves its own findings by patching them.
- **R5f first, and it is a spec decision before it is a code change.**
  Issue #38's criterion 5 and `screen-spec.md:143-146` §1.9 cannot both be
  satisfied as currently written — one requires error detail be collapsed,
  the other requires an always-visible per-repo error list. Whoever owns
  `docs/specs/screen-spec.md` decides which governs; only then is there a
  patch to write. Changing the code against the criterion while §1.9
  stands would leave the same conflict for the next reviewer.
- **The other 12** are ordinary implementation follow-ups against evidence
  pointers already given, and need no decision from this role: R2f, R4e,
  R4e2, R4f, R5d, R6d, R9a (Major); R4g, R9c, R9e (Minor); R3b, R4i
  (Note). Whether they warrant a follow-up issue, get folded into other
  work, or are accepted as-is is the human's call on merge, not this
  record's.
- **The 6 Unverifiable rows** are evidence requests, not defects, and are
  discharged only by a rendering engine — see the table above for what
  settles each. They must not be converted to passes by re-reading the
  same source; if a future session gains a browser stack (issue #44's
  scope, not this one's), these are the rows to re-run first.
- **Disputes.** If the implementation role disputes a finding, it is
  recorded here against the same row and the evidence re-examined; a
  dispute is not itself a request to change the verdict, and this role
  does not fix what it found either way.

## Hand-off

The 13 open findings are addressed to the implementation role for issue
#38. R5f additionally needs a spec decision from whoever owns
`docs/specs/screen-spec.md` §1.9 before it can be implemented either way.
R9a/R9c/R9e are record-quality findings against
`docs/issue-38/reports/implementation.md`, not code defects. The six
Unverifiable rows are handed off as named evidence requests, not as passes.
