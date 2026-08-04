# Design system — web dashboard pilot (issue #4)

Status: accepted. Approved via issue #4 comment `APPROVE issue-4/ux-engineering`
(JiwonJung94, approvers.md). Promoted from
`docs/issue-4/proposals/design-system.md` unchanged in substance; this is
the standing spec other work should reference going forward. Grounded in
`docs/specs/screen-spec.md` (systemized companion spec, phase 2).

Scouting record: `docs/issue-4/reports/ux-engineering/scout-brief.md`.
Adopted: three-layer primitive→semantic→component tokens, paired
foreground/background naming, WCAG contrast floor. Skipped: automated
token build pipeline, multi-density switcher (see brief for why).

## 1. Token architecture

Three layers, `category-purpose-variant` naming, kebab-case:

- **Primitive**: raw values, no meaning attached. `color-blue-500`,
  `space-4`, `font-size-200`.
- **Semantic**: purpose, references a primitive. `color-action-primary`,
  `space-table-cell-padding`, `font-size-body`.
- **Component**: specific element, references a semantic (only where a
  component's usage diverges from its semantic default — most
  components consume semantic tokens directly). `color-button-primary-
  background`.

Every color token that can appear as a background/surface has a
same-layer paired foreground token: seeing `*-background` implies
`*-foreground` exists at the same semantic name.

## 2. Color tokens

### 2.1 Primitives (values)

| Token | Value |
|---|---|
| `color-neutral-0` | `#ffffff` |
| `color-neutral-100` | `#f3f4f6` |
| `color-neutral-300` | `#d1d5db` |
| `color-neutral-500` | `#6b7280` |
| `color-neutral-700` | `#374151` |
| `color-neutral-900` | `#111827` |
| `color-blue-500` | `#2563eb` |
| `color-blue-700` | `#1d4ed8` |
| `color-green-500` | `#16a34a` |
| `color-green-700` | `#15803d` |
| `color-amber-500` | `#d97706` |
| `color-amber-700` | `#92400e` |
| `color-red-500` | `#dc2626` |
| `color-red-700` | `#b91c1c` |

### 2.2 Semantic — surface & text

| Token | References | Use |
|---|---|---|
| `color-surface-page` | `neutral-0` | page background |
| `color-surface-raised` | `neutral-0` | table/panel background, w/ border |
| `color-border-default` | `neutral-500` | table/panel borders |
| `color-text-primary` | `neutral-900` | body text, table cells |
| `color-text-secondary` | `neutral-500` | timestamps, secondary labels |
| `color-action-primary-background` | `blue-500` | refresh button, links |
| `color-action-primary-foreground` | `neutral-0` | text/icon on the above |

Contrast: `neutral-900` on `neutral-0` = 17.9:1. `neutral-0` on
`blue-500` = 4.6:1 (passes 4.5:1 normal-text floor).
`color-text-secondary` (`neutral-500` on `neutral-0`) = 4.6:1 — passes
at normal-text size; do not drop this pairing below 14px without
re-checking. `color-border-default` (`neutral-500` on `neutral-0`,
issue #38) = 4.6:1 — well above the 3:1 WCAG 1.4.11 non-text-contrast
floor for a UI-component boundary (table/panel borders convey
structure); previously `neutral-300` on `neutral-0` ≈ 1.47:1, below
that floor. Reuses the already-defined `neutral-500` primitive, no new
token added.

### 2.3 Semantic — status (drives age buckets, badges, hygiene, errors)

Five statuses, each a background/foreground pair plus a border for use
on `color-surface-page` (chips/badges need a border since they sit on
white, not a colored surface):

| Status | Background | Foreground (on-color) | Border | Contrast (fg/bg) |
|---|---|---|---|---|
| `status-neutral` | `neutral-100` | `neutral-700` | `neutral-300` | 8.3:1 |
| `status-info` | `blue-500` (10% tint: `#eff6ff`) | `blue-700` | `blue-500` | 8.6:1 |
| `status-success` | `green-500` tint `#f0fdf4` | `green-700` | `green-500` | 6.4:1 |
| `status-warning` | `amber-500` tint `#fffbeb` | `amber-700` | `amber-500` | 6.8:1 |
| `status-error` | `red-500` tint `#fef2f2` | `red-700` | `red-500` | 6.9:1 |

Tint backgrounds (not the raw 500-value) are used for chip/badge fills
so foreground text stays legible without needing white text at small
sizes. Tint hex values are this spec's assumption, not a sourced claim.

### 2.4 Status → screen mapping

- **Age buckets**: `fresh` (age_hours < 4) → `status-neutral`; `aging`
  (4 ≤ age_hours < 24) → `status-warning`; `stale` (age_hours ≥ 24) →
  `status-error`. Bucket *names* are the token contract; hour cutoffs
  are a reviewable first cut (see §7).
- **Alive/dead badge**: alive → `status-success`, dead →
  `status-neutral` (not `status-error` — a stopped session isn't
  necessarily a problem).
- **Hygiene violations, repo errors**: `status-error`.
- **Partial-failure banner**: `status-warning`. **Full-page error**:
  `status-error`.
- **Summary strip chips**: "N awaiting decision" → `status-neutral`
  unless N > 0, then uses the same bucket coloring as the oldest item
  in the queue; "N repo errors" → `status-error` when N > 0, hidden
  when N = 0.

## 3. Spacing scale

4px base unit (dense data table, not an 8px marketing-page scale):

| Token | Value | Primary use |
|---|---|---|
| `space-1` | 4px | icon-to-label gap |
| `space-2` | 8px | table cell vertical padding, chip padding |
| `space-3` | 12px | table cell horizontal padding |
| `space-4` | 16px | region gap (between header/summary/tables) |
| `space-6` | 24px | page margin |
| `space-8` | 32px | section separation (e.g. accounting strip from hygiene panel) |

Semantic: `space-table-cell-padding-y` = `space-2`,
`space-table-cell-padding-x` = `space-3`, `space-region-gap` =
`space-4`, `space-page-margin` = `space-6`.

## 4. Typography scale

| Token | Size | Weight | Use |
|---|---|---|---|
| `font-size-100` | 12px | regular | table cell secondary text, timestamps |
| `font-size-200` | 14px | regular | table cell primary text (default body) |
| `font-size-300` | 16px | medium | chip/badge labels, section headings |
| `font-size-400` | 20px | semibold | page title |
| `font-family-base` | system-ui stack | — | all text (no webfont dependency for a pilot) |
| `font-family-mono` | ui-monospace stack | — | PR/issue numbers, elapsed time, cost figures |

Semantic: `font-size-body` = `font-size-200`, `font-size-caption` =
`font-size-100`, `font-size-heading` = `font-size-400`.

## 5. Grid & breakpoints

Single-route screen; one primary desktop breakpoint, plus a floor so
the pilot isn't unusable narrower:

| Token | Value | Behavior |
|---|---|---|
| `breakpoint-md` | 768px | below this: summary-strip chips wrap to 2 rows, detail panel forced to expandable-row mode instead of side panel |
| `breakpoint-lg` | 1200px | at/above: detail panel renders as a side panel; below, expandable row |
| `grid-max-width` | 1440px | content max-width, centered, `space-page-margin` gutters |

Issue #29 added per-table horizontal scroll (`.table-scroll`,
`dashboard.css`) so a wide table (e.g. Flows' Repo/Issue/Stage/Plan/
Roles/PRs columns) can scroll independently of the page at narrow
widths instead of forcing a page-level horizontal scroll or wrapping.
Issue #38 closed the remaining gap that scroll alone didn't cover: the
grid items around `.table-scroll` (`#main-content`,
`#detail-panel-slot`) now carry `min-width: 0` and `table.data-table`
carries an explicit `min-width: 640px`, so the page itself no longer
gets pushed into horizontal scroll at narrow viewports (previously it
did, despite `.table-scroll` existing — a grid item's automatic
min-width is computed from its *unclamped* content, not the
post-scroll box), and every interactive control (`row-toggle`,
`repo-filter`, `refresh-button`) now guarantees a 24×24px minimum touch
target. Full responsive/mobile optimization (e.g. a card layout) is
still out of scope — this is overflow-prevention plus touch-target
sizing, not a redesign.

## 6. Component inventory

Named here, applied per-region in `docs/specs/screen-spec.md`.

| Component | Key tokens |
|---|---|
| `PageHeader` | `font-size-heading`, `color-text-secondary`, `space-page-margin` |
| `RefreshButton` | `color-action-primary-*`, `:hover` (`blue-700`)/`:focus-visible` (`blue-500` outline)/`:disabled` (0.5 opacity, disabled while a load is in flight — issue #38 P2-5/P3-8), 24×24px minimum size |
| `RepoFilter` | native `<select>`, `font-size-body` (issue #29 requirement 2 — client-side filter over an already-fetched payload, no refetch); `color-border-default` border, `:focus-visible` (`blue-500` outline), 24×24px minimum size (issue #38 P2-5) |
| `SummaryChip` | `status-*` pair matching its metric, `font-size-300` |
| `DataTable` | `space-table-cell-padding-*`, `font-size-body`, `color-border-default`, `color-surface-raised`, `min-width: 640px` (issue #38 P1-1), visually-hidden `<caption>` + `th[scope=col]` (issue #38 P2-7), `tr:hover` (`neutral-100`)/`tr.selected-row` (`status-info-background`) row states (issue #38 P2-7/P3-8). Issue/PR cells: leading icon-only `row-toggle` disclosure button (▸/▾, no color token — inherits text color, 24×24px minimum size per issue #38 P2-5) + trailing `#<n>` link (`.number-link`, `color-action-primary-background`, issue #36) |
| `AgeBucketBadge` | `status-neutral/warning/error` per §2.4 |
| `RoleChip` | `status-neutral`, `font-family-mono` |
| `AliveBadge` | `status-success/neutral` per §2.4 |
| `DetailPanel` | `breakpoint-lg` layout switch — now actually wired (issue #38 P1-3): side panel at/above, `<tr>` inserted immediately after the selected row below it. `role="region" aria-labelledby="detail-panel-heading"`, `<h2 id="detail-panel-heading" tabindex="-1">` (issue #38 P1-4/P2-7); focus moves to this heading on open, back to the row's `row-toggle` on close. `space-4` internal gaps |
| `AccountingRow` | `font-family-mono`, `color-text-secondary`; outcomes now render as `.badge.status-neutral` chips like every other status value on the page (issue #38 P3-8), not bare text |
| `HygieneListItem` | `status-error`, `font-size-body` |
| `ErrorListItem` | `status-error` |
| `SkeletonBlock` | `color-neutral-100/300` (no motion token — static or CSS-default pulse, implementation's call); `.skeleton-row` height now matches a real data row's computed height (`space-table-cell-padding-y` × 2 + line-height, issue #38 P3-8) instead of a fixed `2em` guess |
| `EmptyStateMessage` | `color-text-secondary`, `font-size-body` |
| `ErrorState` (full-page) | `status-error`, `font-size-heading`, now an `<h2>` (not `<h1>` — the page's own `<h1>` stays the document's only one, issue #38 P2-6); `role="alert"`; summary line + collapsed `<details>` holding the raw provider/backend message (issue #38 P2-6) |
| `PartialFailureBanner` | `status-warning`; `aria-live="polite"` static on `#partial-banner` (issue #38 P1-4) |

`PartialFailureBanner` note (issue #29/#38): the approved issue-29
proposal called for collapsing the per-repo `"{repo}: {message}"` detail
behind `<details><summary>Details</summary>...</details>`, leaving only
the `"{M} of {N} repos failed to load"` line always visible. That gap
(tracked in `docs/issue-29/reports/implementation.md` "Open findings")
is now closed by issue #38 P2-6 — `dashboard.js` wires the collapse
using the same `collapsibleDetailHtml` helper the full-page `ErrorState`
uses. `docs/specs/screen-spec.md` §2.5 documents the exact copy as
currently rendered.

## 7. Open items (not blocking, tracked for follow-up)

- Age-bucket hour thresholds are a first cut, not user-tested — flag
  for revision once H3 (deferred per hypotheses.md) is picked up.
- `table.data-table`'s `min-width: 640px` (issue #38 P1-1) is a
  first-attempt value, same status as the age-bucket thresholds above —
  revisit if a table's real content needs more or less.
- No dark-mode token set defined — not requested; add only if a future
  issue asks for it.
- Implementation (`src/`) is out of scope for this spec.
