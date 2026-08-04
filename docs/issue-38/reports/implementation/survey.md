# issue-38 current-state survey

Read end-to-end: `src/rsb/web/index.html`, `src/rsb/web/dashboard.css`,
`src/rsb/web/dashboard.js`, `docs/specs/screen-spec.md`,
`docs/specs/design-system.md`, `test/rsb_tests/test_model.py`. Line
numbers below are current-file anchors — the issue body's own line
numbers (e.g. `dashboard.css:139`, `dashboard.js:533`) predate issue-36
(PR #37, merged) and no longer line up; this survey re-anchors every
item.

## 0. P1-2 confirmed already fixed by issue-36 (PR #37, merged to main)

`attachRowToggleHandlers` (`dashboard.js:479-491`) binds only to
`.row-toggle` buttons, reading each button's own
`data-issue`/`data-repo`/`data-table`. `isRowExpanded` (`dashboard.js:199-206`)
now correctly compares `selectedIssue.sourceTable` against the clicked
button's table, and `selectedIssue` is populated with `sourceTable` on
every toggle. `aria-expanded` genuinely flips per-button, and
`aria-controls="detail-panel-slot"` (`rowToggleButtonHtml`,
`dashboard.js:237`) points at the one container that actually exists
(`index.html:25`). Confirms the issue body's own framing: this item is
issue-36's domain, not re-touched here. `WIDE_LAYOUT_QUERY`
(`dashboard.js:19`) is unused (no `matchMedia` call anywhere) — still a
dead constant, named explicitly by issue #38 P1-3, cleaned up as part of
that item below (not this item).

## 1. P1-1 — mobile page-wide horizontal scroll

`#page-body` (`dashboard.css:293-297`) is a CSS grid
(`grid-template-columns: 1fr`) with two items: `#main-content` (`<main>`,
`index.html:24`) and `#detail-panel-slot` (`index.html:25`). Neither grid
item has `min-width` set, so each defaults to `min-width: auto` — a grid
item's automatic minimum size is its content's min-content size
(scout-brief below), which for a wide `<table>` can exceed the
viewport. `.table-scroll` (`dashboard.css:154`, `overflow-x: auto`) only
constrains scrolling *within* the table's own box; it does nothing to
stop that box's min-content size from inflating `#main-content`'s (and
therefore `.page`'s and the viewport's) width, because the grid-item
minimum is computed from the *unclamped* content, not the post-scroll
box. `.page` (`dashboard.css:78-82`) has `max-width` but no
`min-width: 0` either, and sits directly in normal flow (not a flex/grid
child itself, so its own overflow is driven entirely by what
`#page-body`/`#main-content` allow through).

`.page-header` (flex, `flex-wrap: wrap`) and `.summary-strip` (flex,
`flex-wrap: wrap`) already wrap their children and are not the
overflow's source — confirmed by the issue body's own description
("표별 스크롤이 아니라 페이지 본문이 통째로 밀린다", i.e. the table
region specifically). The Sessions table (7 columns, 2 of them
`font-family-mono`: Elapsed, PID) is the widest of the four
(`sessionRows`, `dashboard.js:308-324`) and the most likely single
driver of the measured 621px content width at a 390px viewport.

## 2. P1-3 — narrow-screen detail position

`design-system.md` §5 and `screen-spec.md` §1.6 both specify: side panel
at/above `breakpoint-lg` (1200px), **expandable row** below it. Today
only one render path exists: `DETAIL_SLOT.innerHTML = selectedIssue ?
renderDetailPanel(...) : ""` (`dashboard.js:559`), called unconditionally
regardless of viewport width. `dashboard.css:299-305`'s `@media
(min-width: 1200px)` block only changes whether `#page-body` becomes a
two-column grid with `.detail-panel` sticky — it never changes *where*
the panel's markup is inserted, so below 1200px the same
`DETAIL_SLOT` block simply renders at the bottom of `#page-body`, after
`#main-content`, regardless of which of the four tables and which row
triggered it. This confirms the issue body's own diagnosis (1024px:
selected row bottom ~282px, detail panel appears ~1190px).

`.detail-row td` (`dashboard.css:203-208`) is dead CSS — no JS ever
creates an element with class `detail-row`; it was written in
anticipation of the row-insertion path issue-36's survey §2 already
flagged as unimplemented. `WIDE_LAYOUT_QUERY = "(min-width: 1200px)"`
(`dashboard.js:19`) is a matching dead constant — defined, never read by
`matchMedia` or anything else. Building the row-insertion path
(`insertDetailRow`, named only in a stale code comment,
`dashboard.js:11-18`) is this item's actual work: on narrow screens, the
toggled row's `<tr>` needs a sibling `<tr><td colspan="N">` immediately
after it holding the same detail content `renderDetailPanel` already
produces, and `DETAIL_SLOT` needs to stay empty on narrow screens so the
content doesn't render twice.

There is no existing viewport-check helper in `dashboard.js` — no
`matchMedia`/`window.innerWidth` call anywhere in the file today.

## 3. P1-4 — dynamic-state accessibility

Grepped `dashboard.js`/`index.html` for `aria-live`, `aria-busy`,
`role=`: zero matches outside `.row-toggle`'s own `aria-expanded`/
`aria-controls` (already handled, §0). `HEADER_META` (`index.html:13`,
`textContent = "Loading…"` in `renderSkeleton`, `dashboard.js:141`) is a
plain `<span>` with no `aria-live`. `PARTIAL_BANNER`
(`index.html:20`) and `#partial-banner`'s content
(`dashboard.js:519-524`) render into a plain `<div>` with no live
region. `DETAIL_SLOT` (`index.html:25`) likewise has no `aria-live` and
nothing moves focus into it when a row toggle opens it — a keyboard/
screen-reader user who activates `.row-toggle` gets no signal that new
content appeared elsewhere on the page. `renderFullError`
(`dashboard.js:158-171`) replaces the entire `<main>` synchronously with
no live-region announcement either — for a screen-reader user this is a
silent content swap.

## 4. P2-5 — touch target size

No CSS rule targets `#repo-filter` (`index.html:14-16`) at all — it
renders at native browser `<select>` height, which is what the issue's
390px measurement (~19px) reflects. `.row-toggle` (`dashboard.css:161-173`)
has `padding: 0` and holds only a decorative glyph
(`rowToggleButtonHtml`, `dashboard.js:237`) sized by inherited
`font-size-body` (14px) — well under 24×24px. `.refresh-button`
(`dashboard.css:100-109`) has `space-2 space-3` (8px/12px) padding
around 14px text, giving it roughly 30px height already — likely already
compliant, confirmed only by measurement in phase 2, not assumed here.
`.number-link` (`dashboard.css:189-200`) is inline text within a
sentence-like cell (`#<n>` alongside surrounding table text) — WCAG
2.5.8's own inline-text-target exception plausibly applies to it (see
scout-brief); this survey does not assume it is exempt, that's a
judgment the proposal makes.

## 5. P2-6 — error-state cognitive load

`renderFullError` (`dashboard.js:158-171`) renders `<h1>Couldn't load
board status</h1>` inside `<main>` while `index.html:12`'s
`<h1 id="page-title">rsb status board</h1>` is still present in the
DOM (`MAIN` is a `<main>` nested under `.page`, not a replacement for the
page header) — **two `<h1>`s coexist on the full-error screen**,
confirming the issue body's "제목도 중복된다" claim exactly.
`renderFullError`'s message (`{message}`) is whatever `err.message` the
`fetch`/`res.json()` call throws (`load()`, `dashboard.js:563-578`) or
the raw `data.errors[].message` string the provider/backend returned
(`renderData`, `dashboard.js:495-496` full-failure branch) — neither is
sanitized or summarized, so a provider-side stack trace or file path
propagates verbatim to the DOM. The partial-banner path
(`dashboard.js:516-528`) joins every failed repo's `"{repo}: {message}"`
pair with `, ` into one always-visible line — `design-system.md` §6's
own `PartialFailureBanner` note already records that the approved
issue-29 proposal called for a collapsed `<details>` here and it was
never wired up; this item is that still-open gap. Notably,
`dashboard.css:252-258` (`.partial-banner summary` /
`.partial-banner details[open] summary`) already has CSS written for
this exact `<details>`/`<summary>` shape with no matching markup
anywhere in `dashboard.js` — dead CSS mirroring the dead
`.detail-row`/`WIDE_LAYOUT_QUERY` pattern in §2, confirming this gap
predates issue #38 and was anticipated but never finished.

## 6. P2-7 — table/detail semantic structure

`renderTable` (`dashboard.js:173-188`) emits `<th>${h}</th>` with no
`scope` attribute, and no `<table>` anywhere in `dashboard.js` has a
`<caption>`. `renderDetailPanel` (`dashboard.js:439-456`) wraps its
content in a plain `<div class="detail-panel">` — no heading element (the
issue number line is a `<div><strong>...</strong></div>`, not an `<h2>`
or `role="region"`/`aria-label`), so it isn't reachable as a landmark or
by heading-navigation. No expanded/selected `<tr>` ever receives a
distinguishing class — `renderTable`'s row-building (`dashboard.js:182`)
emits every `<tr>` identically regardless of `isRowExpanded`, so after a
re-render (e.g. after Refresh) there is no visual anchor showing which
row is currently expanded beyond the toggle glyph itself.

## 7. P3-8 — visual states and tokens

Grepped `dashboard.css` for `focus`/`hover`/`disabled`: only
`.row-toggle:focus-visible` and `.number-link:hover/:focus/:focus-visible`
exist. `.refresh-button` and `#repo-filter` have no explicit
`:hover`/`:focus-visible`/`:disabled` rules — both rely entirely on
browser UA defaults, which are visually inconsistent with this page's
own `--color-blue-500` focus-ring convention. No `tr:hover` or row
`.selected` rule exists (ties into §6's missing expanded-row
indicator — same gap, two symptoms). `.skeleton-row` (`dashboard.css:232`,
`height: 2em`) vs. an actual `table.data-table` data row
(`--space-table-cell-padding-y` ×2 + line-height, `dashboard.css:146-150`)
— not verified equal, plausible mismatch, phase-2 measurement item.
`renderAccounting`'s outcomes (`dashboard.js:335`, plain
`${k}:${v}` text with no wrapping element) have no badge/chip styling
unlike every other status value on the page (`AgeBucketBadge`,
`RoleChip`, `AliveBadge` all use `.badge`). `--color-border-default`
(`--color-neutral-300`, `#d1d5db`) on `--color-surface-page`
(`#ffffff`) — design-system.md itself never states this pairing's
contrast ratio (only `color-text-secondary`'s 4.6:1 is documented, §2.2);
computed, `neutral-300` on `neutral-0` is ≈1.47:1, well under the 3:1
WCAG 1.4.11 non-text-contrast floor for a UI-component boundary
(table/panel borders convey structure, not pure decoration). This
survey does not assume a fix (new token vs. reusing an existing darker
neutral) — that's the proposal's call, see Rationale.

## 8. approvers

`docs/specs/approvers.md`: `JiwonJung94`, `jjongkwann` (unchanged since
issue #36).

## 9. test surface

`test/rsb_tests/test_model.py` shells out to plain `node` against the
shipped `dashboard.js` via its `module.exports` guard
(`dashboard.js:593-595`) — currently exports `ageBucket`,
`ageBucketStatus`, `selectSummary`, `isPageEmpty`, `buildPlanSteps`,
`filterByRepo`, `buildGithubUrl`, `numberLinkHtml`. Baseline: `python3 -m
pytest test/` → 55 passed (confirmed this session, `PYTHONPATH=src`
required — no installed package in this environment, matches
`pyproject.toml`'s `src/` layout). No `package.json`/JS framework in the
repo (`find . -name package.json` → no matches outside caches); issue
#23's approved phase-1 proposal ruled out adding one, still true and
still the issue body's own explicit "범위 밖" ("새 JS 테스트 하네스
도입"). Any new pure/DOM-free helper (e.g. a viewport-width check
extracted for testability) should follow the same `module.exports`
convention. `render.py` (`src/rsb/render.py`, CLI plain-text renderer)
has no CSS/DOM/link/ARIA concept at all — confirmed by grep, out of
scope exactly as the issue body states and as issues #23/#29/#34/#36 all
treated it.

## gaps this survey leaves for scout to aim at

- Whether `min-width: 0` belongs on `#main-content` alone or also on
  `#page-body`'s grid item computation more broadly, and whether a grid
  vs. flex fix pattern is more idiomatic here.
- Live-region role choice per state (`role="status"` vs `aria-live="polite"`
  vs `"assertive"`) for loading/partial/full-error/detail-open, and
  whether/where focus should move on each.
- Whether padding-based sizing (vs. explicit `min-width`/`min-height`) is
  the right touch-target fix for `.row-toggle`/`#repo-filter`, and
  whether `.number-link` genuinely qualifies for WCAG 2.5.8's inline-text
  exception.
- Where exactly to insert the narrow-screen detail `<tr>` (immediately
  after the toggled row vs. end of `<tbody>`) and what happens to
  `DETAIL_SLOT` at that width (empty vs. removed from the DOM).
