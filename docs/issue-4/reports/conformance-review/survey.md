# Conformance-review survey (issue #4)

Subject: issue-4 pilot fitness review of the full merged chain (product-
discovery → interaction-design → ux-engineering → implementation →
execution-observation, plus the issue-13 fix loop) against the frozen
specs and contract norms.

Scout: skipped. Reason — this is a conformance check against an already-
frozen spec set (`docs/specs/design-system.md`,
`docs/specs/screen-spec.md`) and a fixed contract (role-handoff v3); no
open product/design decision exists for this role to steer. The
methodology itself is contract-mandated (`review:finding-record`,
`review:severity-classification`), not a field to benchmark against
external exemplars.

## What's merged (main, as of this survey)

- `docs/specs/design-system.md` — accepted token spec (ux-engineering).
- `docs/specs/screen-spec.md` — accepted, token-annotated screen/flow
  spec (ux-engineering phase 2).
- `src/rsb/web/{index.html,dashboard.css,dashboard.js}` — implementation
  (issue-4/implementation), 27+246+317 lines.
- `docs/issue-4/reports/execution-observation.md` — phase-2 verification
  record (execution-observation role). Ran pytest (33/33), drove
  `webserver.run_server` live over HTTP for 5 of 6 spec states, did a
  line-by-line spec-vs-code pass (19 items: 15 match, 4 mismatch — F1
  full-page ErrorState unreachable, F2 retry-link contrast failure, F3
  detail-panel breakpoint layout not implemented, F4 no `breakpoint-md`
  media rule; plus one un-numbered minor: RoleChip mono applied to
  whole `role:state` string instead of just the state segment).
- `docs/issue-13/proposals/implementation.md`,
  `docs/issue-13/reports/implementation/survey.md`,
  `docs/issue-13/reports/implementation.md` — issue-13's fix-loop
  (survey → proposal → fix) for F1-F4, approved and merged (PRs #14,
  #15).

## Fix-loop verification (this session, code read + pytest re-run)

Re-ran `python3 -m pytest test/ -q` from repo root: **33 passed**,
matches both implementation.md and execution-observation.md's counts.

Read `dashboard.js`/`dashboard.css` post-fix against the four numbered
findings:

- **F1**: `renderData()` now branches on `data.errors.length > 0 &&
  succeededRepoCount === 0` (payload-based, not HTTP-status-based) and
  calls `renderFullError()` — independent of the server's always-200
  contract. Fixed.
- **F2**: `.partial-banner button.link` now uses
  `var(--color-status-warning-foreground)` (amber-700 on the
  near-white warning tint, 6.8:1 per design-system.md §2.3) instead of
  the white action-primary-foreground token. Fixed.
- **F3**: `#page-body:has(#detail-panel-slot:not(:empty))` at
  `min-width: 1200px` switches to a two-column grid
  (`1fr minmax(280px, 340px)`) with `position: sticky` on the panel;
  single-column below. Matches screen-spec.md §1.6/§5's breakpoint-lg
  side-panel-vs-row description. Fixed (caveat: `:has()` is a modern
  browser feature — no compatibility statement was made anywhere in
  spec or record; not a spec violation, but worth naming since the
  original screen-spec doesn't discuss browser support baseline).
- **F4**: `@media (max-width: 768px) { .summary-strip { gap:
  var(--space-2); } }` now exists explicitly. The row-mode
  detail-panel behavior below breakpoint-md was already true by
  default (single-column below 1200px covers below-768 too), so no
  separate rule was needed for that half of F4. Fixed.
- **RoleChip minor mismatch** (not one of F1-F4, not in issue-13's
  scope): `dashboard.js` line 131 still applies `.mono` to the whole
  `<span class="badge status-neutral mono">${role}:${loop_state}</span>`
  text, not just the state segment as design-system.md's component
  table implies. Confirmed still present, unfixed, not hidden or
  silently dropped from either record — execution-observation.md
  named it as a separate un-numbered item and issue-13's records only
  claim F1-F4.

## Token-name conformance (spot check beyond execution-observation's pass)

- Every raw hex value in `dashboard.css` lives inside the `:root` token
  block (grep confirmed no hex outside lines 3-40); everything else
  consumes a `var(--...)` reference. Matches the file's own header
  comment ("No raw hex/px outside this block") and design-system.md's
  token-architecture intent.
- `render_json_model` (`src/rsb/render.py`) field names
  (`generated_at_by_repo`, `errors`, etc.) match what `dashboard.js`
  reads — no invented backend fields, consistent with screen-spec.md's
  "Grounding" clause.

## Record-chain integrity

- Every phase-2 record in the chain cites its approving comment
  (`APPROVE issue-4/<role>`) and the prior artifact it built on; issue
  numbers in commit trailers (`Subject: issue-N`) are consistent with
  branch names throughout.
- `docs/specs/design-system.md` and `docs/specs/screen-spec.md` are
  both marked "Status: accepted" and point back to their
  `docs/issue-4/proposals/` originals — matches the standing-spec
  promotion pattern used elsewhere in this repo.
- issue-13's fix loop correctly scoped itself to `src/rsb/web/*` only
  and did not touch `docs/specs/*` — consistent with
  execution-observation.md's explicit hand-off framing ("hands them off
  as findings for a follow-up issue/PR, not a defect to patch here").

## Open question carried into the proposal

Whether the RoleChip mono mismatch and the `:has()` browser-support gap
are worth a finding in this role's record, and at what severity, given
neither blocks the pilot's core hypotheses (H1/H2/H3) — resolved in
the proposal below.
