# Screen/flow spec, systemized — web dashboard pilot (issue #4)

Status: accepted, systemized. Base structure/behavior from
`docs/issue-4/proposals/screen-spec.md` (interaction-design, approved).
This document adds token/rule annotations from
`docs/specs/design-system.md` (ux-engineering, approved) to every
region and state — the phase-2 delivery that closes design-system.md
§7's "apply this token set" item. Behavior is unchanged from the
interaction-design proposal; only visual tokens and previously-deferred
layout/threshold decisions are added here. No code — this remains a
spec, not an implementation.

Grounding: every field named below is one already produced by
`render_json_model` (`src/rsb/render.py`) from a `BoardModel`
(`src/rsb/model.py`). No new backend fields are invented here.

## 1. Single-screen layout

One route, one screen, read-only. Page shell: `grid-max-width` 1440px,
centered, `space-page-margin` (`space-6`) gutters, `color-surface-page`
background, `font-family-base` for all text unless noted.

### 1.1 Header — `PageHeader` + `RefreshButton`

- Content: dashboard title (`font-size-heading`), "as of
  {generated_at}" and "{N} repos, {M} errors" chip
  (`color-text-secondary`).
- Refresh button: `color-action-primary-background` /
  `color-action-primary-foreground`.
- Layout: `space-page-margin` outer padding, `space-4` gap between
  title/timestamp/chip/button.

### 1.2 Summary strip — `SummaryChip` row

- Row of chips, `space-2` internal chip padding, `space-3` gap between
  chips, `font-size-300` labels.
- Each chip takes the `status-*` pair per design-system.md §2.4: "N
  awaiting decision" → `status-neutral` (or oldest-item bucket color
  when N > 0), "N flows in progress" → `status-neutral`, "N sessions
  active" → `status-success` when N > 0 else `status-neutral`, "N
  hygiene issues" → `status-error` when N > 0 else `status-neutral`,
  "N repo errors" → `status-error`, rendered only when N > 0.
- Below header, `space-4` region gap.

### 1.3 Decision queue — `DataTable` + `AgeBucketBadge`

- `DataTable`: `color-surface-raised` background, `color-border-default`
  border, `space-table-cell-padding-y/x` per cell, `font-size-body`
  text.
- Columns: Repo, Issue, PR, Phase, Role, Awaiting, Age. Age column
  renders raw hours plus an `AgeBucketBadge` using the design-system.md
  §2.4 bucket rule: `fresh` <4h → `status-neutral`, `aging` 4–24h →
  `status-warning`, `stale` ≥24h → `status-error`.
- Issue cell renders a leading icon-only `<button class="row-toggle">`
  (▸/▾ glyph, `aria-expanded`, `aria-controls="detail-panel-slot"`,
  `aria-label="Toggle details for issue {n}"` — issue #23
  execution-observation finding; issue #29 requirement 5; relocated to
  this leading-button-only form by issue #36) followed by the issue
  number as a `#<n>` link (`color-action-primary-*`, plain `#<n>` text
  when the repo has no owner/name on record). Clicking the button opens
  `DetailPanel` (§1.6); clicking the link navigates to GitHub. Not a
  clickable `<tr>`. PR column uses the same `#<n>` link rule, with no
  disclosure button (PR cells have no detail panel to open).
- Region-empty state: `EmptyStateMessage` "Nothing awaiting decision"
  (per §2.3 below).
- All four data tables (Decision queue, Flows, Sessions, Accounting
  ledger) render **Repo as the first column** (issue #29 requirement 3)
  and each wraps in its own `.table-scroll` container (`dashboard.css`)
  so a wide table scrolls horizontally on its own at narrow widths —
  there is no page-level horizontal scroll and no separate mobile card
  layout.

### 1.4 Flows table — `DataTable` + `RoleChip`

- Same `DataTable` tokens as §1.3. Stage column: `(raw)` suffix in
  `color-text-secondary` when `stage_derived` is false.
- Roles column: one `RoleChip` per `role:loop_state` pair —
  `status-neutral` background, `font-family-mono` for the state text.
- PRs column: `font-family-mono` for issue/PR numbers.
- Issue cell: same leading `row-toggle` button + trailing `#<n>` link
  pattern as §1.3. PRs column: same `#<n>` link rule as Issue. Region-empty:
  `EmptyStateMessage` "(none)".

### 1.5 Sessions table — `DataTable` + `AliveBadge`

- Same `DataTable` tokens. Elapsed/PID columns: `font-family-mono`.
- Issue cell: same §1.3 pattern.
- Alive column: `AliveBadge`, `status-success` (alive) /
  `status-neutral` (dead) per design-system.md §2.4.
- Last activity: `font-family-mono` timestamp + kind:detail, em-dash
  (`color-text-secondary`) when null.
- Region-empty: `EmptyStateMessage` "(none)".

### 1.6 Detail panel — `DetailPanel`

- Layout choice resolved: side panel at/above `breakpoint-lg` (1200px),
  expandable row below `breakpoint-lg` (design-system.md §5).
- Internal spacing: `space-4` between the four sub-sections (decision
  row, flow row, session rows, ledger entry).
- Empty (stale selection): inline message "This issue no longer has
  board activity", `color-text-secondary`.

### 1.7 Accounting strip — `AccountingRow`

- Issue cell: same §1.3 pattern.
- Compact table/summary line, `font-family-mono` for cost and counts,
  `color-text-secondary` for the outcome chips and "unattributed: N
  sessions, $X — repo" line.
- `space-8` separation from the hygiene panel above it (lowest visual
  priority per the glance-first ordering).
- Region-empty: `EmptyStateMessage` "(none)".

### 1.8 Hygiene panel — `HygieneListItem`

- Flat list, one line per violation, `status-error` left-border or
  marker, `font-size-body` text.
- Counted into the summary strip's "hygiene issues" chip (§1.2).
- Region-empty: `EmptyStateMessage` "No hygiene issues".

### 1.9 Errors panel — `ErrorListItem`

- Only rendered when non-empty. `status-error` marker, `font-size-body`
  "{repo}: {message}" per line.

## 2. States

### 2.1 Page-level Loading

- `SkeletonBlock` in header (date), summary strip (chip outlines
  `color-neutral-300` border, `color-neutral-100` fill), and each table
  region (grey placeholder rows) — independent per-region skeletons,
  not one full-page spinner.
- Header copy: "Loading…" replaces "as of {timestamp}"
  (`color-text-secondary`).

### 2.2 Page-level Empty

- Summary strip: all-zero chips, `status-neutral` (visible, not
  hidden — the zero state is itself the answer).
- Tables replaced by one `EmptyStateMessage`: "No activity to show for
  the configured repos.", `color-text-secondary`, `font-size-body`, no
  CTA.

### 2.3 Region-level Empty

- That table's body → one centered `EmptyStateMessage` row/line:
  "Nothing awaiting decision" (§1.3), "(none)" (§1.4/§1.5/§1.7), "No
  hygiene issues" (§1.8). `color-text-secondary`, `font-size-body`,
  low-emphasis (plain text, no illustration).

### 2.4 Page-level Error (total failure) — `ErrorState`

- Full-page state replacing summary strip and all table regions:
  heading "Couldn't load board status" (`font-size-heading`), joined
  repo error messages (`color-text-secondary`), primary Retry button
  (`color-action-primary-*`). Icon/heading area uses `status-error`
  accent. No stale content shown underneath.

### 2.5 Partial failure (banner) — `PartialFailureBanner`

- `status-warning` background/foreground/border, placed directly under
  the header, `space-4` gap above the summary strip.
- Copy (as actually rendered by `dashboard.js`'s `renderData()`
  `PARTIAL_BANNER.innerHTML` block): a single always-visible line, `"{M}
  of {N} repos failed to load — {repo}: {message}, {repo}: {message},
  …"` — every failed repo's `repo: message` pair joined with `, ` after
  the em dash — followed by the `Retry` link/button. (The approved
  proposal for issue #29 additionally specifies collapsing the per-repo
  detail behind `<details><summary>Details</summary>...</details>`,
  leaving only the `"{M} of {N} repos failed to load"` line always
  visible; that collapse is not yet wired into `dashboard.js` as of this
  writing — see `docs/issue-29/reports/implementation.md` "Open
  findings". This line documents the copy as it actually renders today,
  not the not-yet-built collapsed form.)
- Retry action styled as a text/link button in
  `color-action-primary-foreground` on the warning background (falls
  back to `status-warning`'s foreground token if the action-primary
  pairing fails contrast on the tint — both pass per design-system.md
  §2.3's listed ratios, no fallback needed in practice).
- Rest of the screen renders normally with succeeded repos' data.

### 2.6 Detail panel states

- Loading: not applicable (no independent fetch).
- Empty: see §1.6.

## 3. Traceability table

Unchanged from `docs/issue-4/proposals/screen-spec.md` §3 — every
hypothesis (H1, H2, H3) traces to a region above; this document adds
tokens, not new elements or new traceability.

## 4. Basic interaction flow

Unchanged from `docs/issue-4/proposals/screen-spec.md` §4 (load → render
→ view summary → scan tables → drill in → resolve or leave → optional
refresh). Visual states referenced above (§2.1–§2.5) slot into steps 1–2
of that flow.

## 5. Resolved vs. still-deferred

Resolved by this document (previously "deferred to ux-engineering" in
the interaction-design proposal, per design-system.md):

- Detail panel layout choice: `breakpoint-lg` (1200px) side panel vs.
  expandable row (§1.6).
- Age-bucket visual mapping and hour thresholds (§1.3, first cut).
- Alive/dead badge, hygiene/error, partial/full-failure color mapping.

Still deferred (out of scope for both interaction-design and
ux-engineering, unchanged from the proposal):

- Auth/access model for exposing this data over the web.
- Auto-refresh/poll interval, if any.
- Implementation (`src/`).
