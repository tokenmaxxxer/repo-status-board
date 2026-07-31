# Current-state survey — issue #4, ux-engineering phase 1

Status: phase-1 survey. Scope: ux-engineering role only.

## 1. Write surface handed to this role

`docs/issue-4/proposals/screen-spec.md` (approved, interaction-design
phase 1) explicitly defers all visual/token design to ux-engineering:
"Visual design tokens, spacing, color, typography — ux-engineering"
(§5), plus two concrete open decisions it leaves numeric: age-bucket
thresholds for the decision queue (§1.3) and the detail-panel layout
choice (side panel vs. expandable row, §1.6).

## 2. What exists today: nothing token-shaped

- This repo (`src/rsb/`) is a Python CLI (`render_text` /
  `render_json_model`, `src/rsb/render.py`). No CSS, no component
  library, no color/spacing/type values anywhere in the tree —
  confirmed by `find . -name '*.css' -o -name '*.scss'` returning
  nothing and no `web*` directory existing. The issue names this
  explicitly: "token-less 프로젝트".
- No prior `docs/specs/design-system.md` or any design-token file
  exists under `docs/specs/` (only `approvers.md` and
  `flows-schema.md` are there today).
- There is therefore no legacy naming/value scheme to reconcile against
  — this proposal is a from-scratch token system, not a migration.

## 3. What screen-spec.md requires the token system to cover

Reading every region in screen-spec.md §1–§2 for token-shaped needs:

- **Status/semantic color**: age-bucket bands (fresh/aging/stale, §1.3,
  threshold undecided), alive/dead badges (§1.5), decision-vs-hygiene
  vs-error distinctions (§1.2 chips, §1.8 hygiene, §1.9 errors), and
  partial-failure banner vs. full-page error state (§2.4/§2.5) — each
  needs a distinct semantic color with a paired on-color (readable
  text/icon on that background) per WCAG contrast.
- **Density-sensitive spacing/type**: five data tables (decisions,
  flows, sessions, accounting, hygiene) rendered on one screen (§1.3–
  §1.8) — this is a dense, data-heavy layout, not a marketing page;
  spacing scale needs a compact rhythm, and type scale needs a stable
  small body size for table cells distinct from headings/chips.
- **Grid/breakpoints**: single-route, single-screen (§1) with a
  deferred-layout side panel / expandable row (§1.6) — needs to work
  at minimum on one desktop breakpoint; screen-spec doesn't rule out
  narrower viewports, so a baseline responsive breakpoint set is
  needed even though multi-device use isn't hypothesis-gated.
- **Component inventory implied by the regions**: header w/ refresh
  button, summary strip chips/badges, data table (5 uses), status
  badge (alive/dead, hygiene violation, error), age-bucket indicator,
  detail panel, banner (partial-failure), full-page error state,
  loading skeleton (per-region, §2.1), empty-state row/message
  (§2.2/§2.3).

## 4. Gap this phase must fill

Everything in §3 needs a name and a value, and nothing in this repo
supplies either today. Phase-1 deliverable is the proposal at
`docs/issue-4/proposals/design-system.md`: primitive→semantic token
layers, spacing/type scale, color + on-color pairs (including the
status semantics screen-spec needs), grid/breakpoints, and a component
inventory naming (not building) each element listed above. Numeric
age-bucket thresholds (deferred by screen-spec §5) are decided here as
part of the status-color semantics, since a bucket is meaningless
without a paired token.

Phase-2 (post-approval, not this phase): apply these tokens to
screen-spec.md's regions/states as a systemized annotation — no code,
per role write_scope (implementation owns `src/`).
