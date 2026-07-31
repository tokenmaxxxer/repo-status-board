# Conformance-review proposal (issue #4)

Scope: pilot fitness review of the merged issue-4 chain (rsb serve,
`src/rsb/web/`, including issue-13's F1-F4 fixes) against
`docs/specs/design-system.md` and `docs/specs/screen-spec.md`, plus
contract-norm checks (record chain, write-scope discipline).

## Method

Phase 2 will produce `docs/issue-4/reports/conformance-review.md` as a
per-requirement verdict table, using `review:finding-record` (one
verdict per spec requirement) and `review:severity-classification`
(only for findings that survive, to rank them). Requirements are drawn
from the frozen specs' own structure, not re-derived:

1. **Token-name conformance** — every token design-system.md §2-§6
   defines, checked against actual `var(--...)` usage in
   `dashboard.css`/class names in `dashboard.js`. Basis: the survey's
   spot check (all hex confined to `:root`) plus re-verifying
   execution-observation.md's item-by-item table rather than
   redoing it from scratch — this role's job is to confirm that record
   is accurate and complete, not re-derive it independently.
2. **State-handling completeness** — all six states in screen-spec.md
   §2 (loading, page-empty, region-empty, page-error, partial-failure,
   detail-empty), verified against the current (post-issue-13) code,
   since execution-observation.md's F1 finding (full-page error
   unreachable) has since been fixed and needs re-verification, not
   just citation.
3. **Code quality/consistency** — no raw hex outside `:root`, no
   invented backend fields, consistent naming between spec component
   names (§6) and CSS class names, `escapeHtml` used consistently on
   any interpolated user/repo-controlled string.
4. **Record-chain integrity** — every phase-2 record cites its
   approving comment and predecessor artifact; commit `Subject:`
   trailers match branch/issue; issue-13's fix-loop stayed inside its
   own write-scope (`src/rsb/web/*`, no spec edits).

## Findings carried in as known, to be re-verified (not re-discovered)

- F1-F4 (execution-observation.md): re-verify each against current
  code as **fixed** or **not fixed**, per the survey's read (all four
  read as fixed on this pass — phase 2 re-confirms formally with
  verdicts).
- RoleChip mono mismatch: un-numbered, still present, not part of
  issue-13's scope. Phase 2 will record this as a new finding of this
  role (it was never formally recorded as a standalone actionable
  item; execution-observation.md's own conformance table lists it but
  its "Findings" section (§6) only numbers F1-F4) — severity to be set
  in phase 2, expected low given it's cosmetic and doesn't block any
  hypothesis.
- `:has()` selector browser-support gap (F3's fix): to be recorded as
  an observation, not necessarily a defect — screen-spec.md never
  states a browser-support floor, so this isn't a spec violation, but
  worth flagging since it's the only modern-CSS-feature dependency in
  the file.

## Out of scope for this role

- Re-litigating H1/H2/H3 or the age-bucket hour thresholds
  (design-system.md §7 — explicitly open, tracked for future pickup).
- Auth/access model, auto-refresh interval — both explicitly deferred
  by screen-spec.md §5, not this role's to resolve.
- Fixing anything found — per contract, conformance-review records
  findings; it does not patch `src/`/`test/`. Any new finding (e.g.
  RoleChip) hands off the same way execution-observation.md handed off
  F1-F4, to a follow-up issue.

## Deliverable

`docs/issue-4/reports/conformance-review.md`: one row per requirement
above (tokens, states, code quality, record chain), verdict
(Conformant/Non-conformant/Partial), and a findings section for
anything non-conformant, severity-classified.
