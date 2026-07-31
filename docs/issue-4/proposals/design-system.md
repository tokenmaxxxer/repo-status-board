# Design system proposal — web dashboard pilot (issue #4, ux-engineering)

Status: phase-1 proposal. Scope: ux-engineering role only — this repo
is token-less (`docs/issue-4/reports/ux-engineering/survey.md` §2), so
this is the first design-system proposal, not a revision of an
existing one. Grounded in `docs/issue-4/proposals/screen-spec.md`
(approved). No code — this document defines names and values;
applying them to screen-spec.md's regions is phase-2 (post-approval)
systemization, and building them (`src/`) is implementation's job.

Scouting: see `docs/issue-4/reports/ux-engineering/scout-brief.md`.
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
`*-foreground` exists at the same semantic name. This is the naming
contract scout-brief.md flags as a must-be.

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
| `color-border-default` | `neutral-300` | table/panel borders |
| `color-text-primary` | `neutral-900` | body text, table cells |
| `color-text-secondary` | `neutral-500` | timestamps, secondary labels |
| `color-action-primary-background` | `blue-500` | refresh button, links |
| `color-action-primary-foreground` | `neutral-0` | text/icon on the above |

Contrast: `neutral-900` on `neutral-0` = 17.9:1. `neutral-0` on
`blue-500` = 4.6:1 (passes 4.5:1 normal-text floor).
`color-text-secondary` (`neutral-500` on `neutral-0`) = 4.6:1 — passes
at normal-text size; do not drop this pairing below 14px without
re-checking.

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
sizes — a fix for the scout-brief gap ("current state has zero
status tokens") rather than a scouted pattern per se, since none of
the swept sources specified this exact tint mechanic; treat the tint
hex values as this proposal's assumption, not a sourced claim.

### 2.4 Status → screen-spec mapping (resolves screen-spec.md's deferred items)

- **Age buckets (screen-spec §1.3, threshold undecided)**: `fresh`
  (age_hours < 4) → `status-neutral`; `aging` (4 ≤ age_hours < 24) →
  `status-warning`; `stale` (age_hours ≥ 24) → `status-error`.
  Thresholds are this proposal's decision, not sourced — pick values
  reviewable/adjustable in phase 2 without a token rename, since the
  bucket *names* (fresh/aging/stale) are the token contract, not the
  hour cutoffs.
- **Alive/dead badge (§1.5)**: alive → `status-success`, dead →
  `status-neutral` (not `status-error` — a stopped session isn't
  necessarily a problem).
- **Hygiene violations (§1.8), repo errors (§1.9)**: `status-error`.
- **Partial-failure banner (§2.5)**: `status-warning` (some data still
  usable). **Full-page error (§2.4)**: `status-error`.
- **Summary strip chips (§1.2)**: "N awaiting decision" →
  `status-neutral` unless N > 0 uses the same bucket coloring as the
  oldest item in the queue; "N repo errors" → `status-error` when
  N > 0, hidden when N = 0 (matches screen-spec's own rule).

## 3. Spacing scale

4px base unit, matches the "dense data table" performance axis from
scout-brief.md (Carbon's density-first pattern) rather than an 8px
marketing-page scale:

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

Single-route screen (screen-spec §1); one primary desktop breakpoint,
plus a floor so the pilot isn't unusable narrower:

| Token | Value | Behavior |
|---|---|---|
| `breakpoint-md` | 768px | below this: summary-strip chips wrap to 2 rows, detail panel (§1.6) forced to expandable-row mode instead of side panel |
| `breakpoint-lg` | 1200px | at/above: detail panel may render as a side panel (screen-spec §1.6's deferred layout choice — this proposal resolves it: side panel ≥1200px, expandable row below) |
| `grid-max-width` | 1440px | content max-width, centered, `space-page-margin` gutters |

Multi-device/mobile optimization is out of scope (not hypothesis-
gated per screen-spec §5); the 768px floor exists only so the single
screen degrades gracefully, not to support a mobile flow.

## 6. Component inventory

Named here (per screen-spec.md region), not built. Each maps to §2–5
tokens above.

| Component | Screen-spec region | Key tokens |
|---|---|---|
| `PageHeader` | §1.1 | `font-size-heading`, `color-text-secondary` (timestamp), `space-page-margin` |
| `RefreshButton` | §1.1 | `color-action-primary-*` |
| `SummaryChip` | §1.2 | `status-*` pair matching its metric, `font-size-300` |
| `DataTable` | §1.3–§1.5, §1.7 | `space-table-cell-padding-*`, `font-size-body`, `color-border-default`, `color-surface-raised` |
| `AgeBucketBadge` | §1.3 | `status-neutral/warning/error` per §2.4 |
| `RoleChip` (role:loop_state) | §1.4 | `status-neutral`, `font-family-mono` for state text |
| `AliveBadge` | §1.5 | `status-success/neutral` per §2.4 |
| `DetailPanel` | §1.6 | `breakpoint-lg` layout switch, `space-4` internal gaps |
| `AccountingRow` | §1.7 | `font-family-mono` (cost/counts), `color-text-secondary` |
| `HygieneListItem` | §1.8 | `status-error`, `font-size-body` |
| `ErrorListItem` | §1.9 | `status-error` |
| `SkeletonBlock` | §2.1 | `color-neutral-100/300` (no motion token defined — pilot scope; static or CSS-default pulse, implementation's call) |
| `EmptyStateMessage` (page + region) | §2.2, §2.3 | `color-text-secondary`, `font-size-body` |
| `ErrorState` (full-page) | §2.4 | `status-error`, `font-size-heading` |
| `PartialFailureBanner` | §2.5 | `status-warning` |

## 7. Open items for phase 2

- Apply this token set to every screen-spec.md region/state as an
  annotated systemization pass (the phase-2 deliverable this proposal
  unblocks).
- Age-bucket hour thresholds (§2.4) are a first cut, not user-tested —
  flag for revision once H3 (deferred per hypotheses.md) is picked up.
- No dark-mode token set defined — not requested by screen-spec.md or
  hypotheses.md; add only if a future issue asks for it.
