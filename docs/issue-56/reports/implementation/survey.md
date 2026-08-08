# issue-56 current-state survey

Read end-to-end this session: `src/rsb/web/dashboard.js`,
`src/rsb/web/dashboard.css`, `src/rsb/web/index.html`,
`docs/specs/screen-spec.md`, `docs/specs/design-system.md`,
`test/rsb_tests/test_model.py`, `test/rsb_tests/test_dashboard_dom.py`;
plus the upstream chain issue #56 cites: issue #38's body,
`docs/issue-38/reports/execution-observation.md` (all 487 lines, F1/F3),
`docs/issue-38/proposals/implementation.md`, and
`docs/issue-38/reports/implementation.md`. `docs/specs/approvers.md` was
also read (two accounts, `JiwonJung94`/`jjongkwann`).

## 1. Requirement 1 — `renderErrors`, the third error surface (F1)

`renderErrors(errors)` (`dashboard.js:355-365`) returns `""` when
`errors.length === 0`; otherwise it emits a `<section class="region">`
with an always-visible `<ul class="error-list">` of `{repo}: {message}`
lines (`:361`, `escapeHtml`-only — no `<details>`). It is called once,
unconditionally, at `dashboard.js:632` inside `renderData`'s
`MAIN.innerHTML` template, between the "Sessions" and "Hygiene"
sections.

Tracing `renderData`'s control flow (`dashboard.js:575-645`) shows this
call site is reachable only when **all** of these hold:
- `data.errors.length > 0` (line 577's full-error branch, which returns
  early when `succeededRepoCount === 0`, did not fire — so at least one
  repo succeeded too), and
- `isPageEmpty(data)` is false (line 612's early return did not fire).

The partial-failure banner (`PARTIAL_BANNER.innerHTML`, lines 597-610)
fires on the exact same compound condition:
`failedRepos.length > 0 && Object.keys(data.generated_at_by_repo).length > 0`
— arithmetically identical to "errors present and at least one repo
succeeded." So every time `renderErrors` produces non-empty output, the
partial banner has, moments earlier in the same `renderData` call,
already rendered the identical `{repo}: {message}` pairs
(`failedRepos.map((e) => \`${e.repo}: ${e.message}\`).join(", ")`, line
600) inside a `collapsibleDetailHtml("Details", detail)` — i.e., the
exact summary+collapsed-detail structure AC5 requires. `renderErrors`'s
own output is always a 100%-overlapping, always-visible duplicate of
data the banner already shows collapsed. There is no reachable state
where `renderErrors` shows information the banner does not.

`renderErrors` is untested (`grep -rn "renderErrors\|error-list\|Errors</h2>" test/`
→ zero hits) and unexported (`dashboard.js:681`'s `module.exports` list
does not include it, unlike the sibling pure functions
`collapsibleDetailHtml`/`numberLinkHtml`/`detailRowHtml` it sits next
to).

`docs/specs/screen-spec.md` documents this surface at §1.9 ("Errors
panel — `ErrorListItem`", lines 143-146): "Only rendered when non-empty.
`status-error` marker, `font-size-body` `{repo}: {message}` per line" —
still describing the always-visible, non-collapsed shape.
`git log --follow -S"Errors panel"` shows this section was written once,
in `119983d` (issue #4, the foundational spec commit), and has never
been touched since — not by issue #29 (which introduced the
collapsed-`<details>` pattern generally) and not by issue #38 P2-6
(`e8443ea`), which rewrote the neighboring §2.5 "Partial failure
(banner)" to the collapsed shape and explicitly cites "issue #38 P2-6"
in its own text (screen-spec.md:207-210) — §1.9 carries no such
citation. The spec for this surface was never reconciled when the
banner absorbed the same data; it is stale by omission, not by a
deliberate keep-both decision recorded anywhere.

## 2. Requirement 2 — `.number-link` measurement (F3)

`.number-link` (`dashboard.css:248-259`) carries `color` and
`text-decoration` rules only — no `min-width`/`min-height`, unlike its
sibling `.row-toggle` (`dashboard.css:212-228`), which the same issue
#38 P2-5 pass gave `min-width: 24px; min-height: 24px; display:
inline-flex; align-items: center; justify-content: center` specifically
to guarantee the WCAG 2.5.5/2.5.8 24×24px minimum "regardless of font
size" (comment at `dashboard.css:220-222`).

`numberLinkHtml` (`dashboard.js:223-227`) is invoked in two DOM
contexts, neither of which places it inside a run of prose text:
- `dashboard.js:243`, inside `<span class="issue-cell">`, immediately
  preceded by the icon-only `.row-toggle` button
  (`rowToggleButtonHtml`) — the cell's only two children are the button
  and this link.
- `dashboard.js:254`, inside `<span class="mono">`, as the sole content
  of a "PR" table-cell entry.

Font metrics: `--font-size-body` resolves to `--font-size-200` = `14px`
(`dashboard.css:54-55,59`); `grep -n "line-height" dashboard.css`
returns zero matches anywhere in the file, so the rendered line box
falls back to the browser default (`normal`, ≈1.15-1.2×), i.e. roughly
16-17px tall for 14px text — consistent with issue #38's own body
(`gh issue view 38`, requirement 5), which already reports a real-device
measurement of exactly **8×17px** for this link ("외부 링크 8×17px").
That figure is a pre-existing human measurement this survey does not
need to redo; what issue #56 asks is the WCAG 2.5.8 **exception
determination** the approved issue-38 proposal deferred, never
performed.

Environment check for a live re-measurement: no `google-chrome`,
`chromium`, or `chromium-browser` binary is on `PATH`, and
`python3 -c "import playwright"` raises `ModuleNotFoundError` — no
browser automation is available in this sandbox, the same blocker
`docs/issue-38/reports/implementation.md:104-123` hit and disclosed.
`test/rsb_tests/test_dashboard_dom.py` uses `jsdom`
(`test/node_modules/jsdom`), which does not compute real layout
(`getBoundingClientRect` is not backed by a rendering engine), so it
cannot produce a pixel measurement either — only a DOM-structure/CSS
tracing determination is possible here, same substitution class as
issue #38's own phase 2.

`docs/specs/design-system.md` corroborates the current exclusion was
already implicit, if never confirmed against WCAG text: §5's prose
(lines 156-167) states "every interactive control (`row-toggle`,
`repo-filter`, `refresh-button`) now guarantees a 24×24px minimum touch
target" — `.number-link` is not in that list — and §6's component table
(line 179) names `.number-link` only for its color token
(`color-action-primary-background`), with no size note, while the same
row's `row-toggle` entry explicitly carries "24×24px minimum size per
issue #38 P2-5."

The approved condition this requirement resolves:
`docs/issue-38/proposals/implementation.md:310-312` put `.number-link`
out of scope for P2-5 "phase-2 실측으로 확인만 하고 CSS 는 건드리지
않는다" (confirm by phase-2 measurement only, don't touch the CSS). That
confirmation was never performed or disclosed
(`docs/issue-38/reports/execution-observation.md` F3, `.number-link`
appears zero times in `docs/issue-38/reports/implementation.md`).

## 3. Constraint boundary — PR #43's other 8 ACs (issue #56's 제약)

Not touched by this survey's proposed write set: `.row-toggle`,
`#repo-filter`, `.refresh-button` sizing (AC4, already 24×24px);
`renderFullError` (AC5, full-failure path, already collapsed);
`applySelectionLayout`/`attachRowToggleHandlers` (AC2/AC3); `renderTable`
caption/`th[scope]` (AC6); the P3-8 polish items (row hover/selected,
skeleton height, badge styling, border contrast). AC1's `min-width: 0`
grid fix and AC7/AC8/AC9 process items are unrelated code paths this
issue does not touch.

## 4. Test conventions available for requirement 3 (1 new test)

Two committed harnesses already exist and cover the two relevant
shapes:
- `test/rsb_tests/test_model.py`'s `_run_dashboard_js` (`node -e`
  subprocess, DOM stubbed to `getElementById: () => null`) — the
  convention already used for `collapsibleDetailHtml`
  (`test_dashboard_js_collapsible_detail_html_escapes_summary_and_detail`,
  line 350) and `numberLinkHtml` (lines 313-337). Suits a pure-function
  assertion (e.g. on `collapsibleDetailHtml`'s escaping, or on whatever
  `renderErrors` becomes if it survives as a pure helper).
- `test/rsb_tests/test_dashboard_dom.py`'s jsdom harness (real
  `document`, fresh `node -e` subprocess per test) — suits a rendered-
  output assertion (e.g. "the partial-failure `#main-content` text does
  not contain the raw un-escaped repo error message outside a
  `<details>`," closing the document-vs-element-scope gap
  `docs/issue-38/reports/execution-observation.md` F1's root-cause
  section names). No partial-failure scenario exists in either committed
  test file today — the one the issue-38 execution-observation record
  describes (`docs/issue-38/reports/implementation.md:143-146`) was an
  ad hoc, never-committed script.

## 5. Open decisions this survey leaves for the proposal

- **Requirement 1 shape**: remove `renderErrors` and its call site
  entirely (the banner already fully subsumes its output on every
  reachable path — §1 above), versus keep it but route it through
  `collapsibleDetailHtml` like the banner (keeps a section-per-concern
  structure, at the cost of the same data appearing twice, both
  collapsed). This survey establishes the 100% overlap as fact; the
  proposal's Rationale must pick between the two and say why.
- **Requirement 2 shape**: this survey establishes the exception
  determination (§2) but not the exact CSS technique — the natural
  in-repo precedent is `.row-toggle`'s `min-width`/`min-height` +
  `display: inline-flex` pattern, which the proposal should evaluate
  against the two contexts `.number-link` actually appears in
  (`.issue-cell` flex row, `.mono` standalone cell) for layout
  side-effects (row height, cell alignment) before committing to it.
- **Doc placement**: if requirement 1 changes `renderErrors`,
  `screen-spec.md` §1.9 (and §2.5's cross-reference, if the section is
  removed rather than merged) needs a matching edit; if requirement 2
  sizes `.number-link`, `design-system.md` §5's prose and §6's
  `DataTable` row both need their "24×24px" language extended to name
  it, same ladder issue #38's own proposal followed for `.row-toggle`.
