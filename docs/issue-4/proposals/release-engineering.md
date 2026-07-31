# Release-engineering proposal (issue #4, phase 1)

loop_state: proposed

This is a **phase-1 proposal**, not a phase-2 execution record. No git
tag is cut, no GitHub issue is filed, and no `docs/issue-4/reports/
release-engineering.md` record exists yet — that record is gated on a
human `APPROVE issue-4/release-engineering` comment per contract v3,
same pattern every prior role in this chain followed.

Basis: `docs/issue-4/reports/release-engineering/survey.md` (current-
state survey) and `docs/issue-4/reports/release-engineering/scout-brief.md`
(external-convention check), both written by this role in this same
pass.

## a. Release readiness verdict (go/no-go)

**Proposed verdict: GO.**

Rationale, per conformance-review.md (commit `09dcd2b`, the chain's
most recent and authoritative record):

- All four numbered findings from execution-observation.md (F1 —
  full-page ErrorState unreachable; F2 — partial-banner contrast
  failure; F3 — detail-panel breakpoint-lg layout; F4 — breakpoint-md
  explicit rule) are verified **fixed** by issue-13's fix loop and
  re-confirmed **Present** in conformance-review.md's verdict table
  (§2/§3).
- Token-name conformance (§1), state-handling completeness across all
  six spec'd states (§2), code-quality/consistency (§3, aside from the
  one Minor exception below), and record-chain integrity (§4) all read
  **Present** with no gaps.
- The only open finding is **RoleChip mono mismatch**, severity
  **Minor**, explicitly assessed by conformance-review.md as
  "cosmetic ... does not block or mislead on any of H1/H2/H3" — i.e.
  it does not threaten the pilot's own success hypotheses.
- The `:has()` browser-support item is a **Note**, not a spec
  violation, and requires no fix.
- No **Blocking** or **Major/significant** findings remain open
  anywhere in the chain.

Per this project's own severity-classification scheme
(conformance-review.md's method section: Blocking/Major/Minor/Note),
a release with zero Blocking and zero Major findings, and exactly one
Minor cosmetic finding with an already-agreed non-blocking hand-off
plan, meets a reasonable go bar for a **pilot** release (not a
general-availability release — see version plan below for how that
distinction is signaled).

## b. Version tagging plan

**Proposed tag: `v0.1.0-pilot`.**

Reasoning:

- `pyproject.toml` and `src/rsb/__init__.py` already declare
  `version = "0.1.0"` (pre-existing, set by an earlier role/commit,
  not chosen here). No repo package file needs editing to match a
  `0.1.0` tag.
- Per `scout-brief.md` §1: semver's own spec treats the entire `0.x`
  range as "anything may change," which fits a pilot explicitly built
  to test H1/H2/H3 with several items still deferred (auth model,
  refresh interval, age-bucket thresholds — conformance-review.md
  §6). Jumping straight to `1.0.0` would overstate the API/behavior
  stability commitment this project isn't ready to make.
- The `-pilot` pre-release suffix makes the provisional nature visible
  directly in the tag/release name, not just in prose — useful given
  this is explicitly a pilot for the role-chain process itself
  (per the issue's framing), not only for the dashboard feature.
- Git tag mechanism (for phase-2 execution, not run in this phase):
  `git tag -a v0.1.0-pilot -m "..."` (annotated tag, so it carries a
  message and is distinguishable from a lightweight tag) on the commit
  that merges this chain's final state to `main`, then `git push
  origin v0.1.0-pilot`.
- Release-notes/changelog content to include (also not written in this
  phase, since no `CHANGELOG.md` exists yet and creating one is a
  phase-2 action):
  - Summary: first pilot release of the `rsb` status-board web
    dashboard (issue #4).
  - What's included: the 6 spec'd dashboard states (screen-spec.md
    §2), token-based design system (design-system.md), all F1-F4
    defects from execution-observation.md fixed.
  - **Known Issues** section (per scout-brief.md §2's convention):
    RoleChip `.mono` mismatch (`dashboard.js:131`), severity Minor,
    cosmetic-only, tracked as a backlog item (see §c below) — not
    silently omitted.
  - Deferred/out-of-scope note: H1/H2/H3 hypothesis validation itself,
    auth/access model, auto-refresh interval, and age-bucket hour
    thresholds remain open per conformance-review.md §6 and are not
    part of this release's claims.

## c. Backlog disposition: RoleChip mono finding

**Proposal: track as a standalone backlog item, non-blocking, not
filed as a real GitHub issue in this phase.**

Description of the proposed follow-up item (textual only — no real
issue number is fabricated, per this phase's constraints):

> Title (proposed): "Fix RoleChip `.mono` class scope to state segment
> only". Body (proposed): `dashboard.js:131` applies the `.mono` CSS
> class to the entire `role:loop_state` chip span; design-system.md's
> component table specifies `font-family-mono` for the state segment
> only. Fix: split the span so `.mono` wraps only the `loop_state`
> portion, e.g. `role:<span class="mono">loop_state</span>` (exact
> markup change left to whichever implementation role picks this up).
> Severity: Minor / cosmetic. First identified: execution-observation.md
> (un-numbered item); formally recorded: conformance-review.md
> (commit `09dcd2b`).

Reasoning why this is non-blocking for the v0.1.0-pilot release:

- Conformance-review.md's own assessment: "Cosmetic (monospace font on
  an extra few characters), does not block or mislead on any of
  H1/H2/H3, not part of issue-13's scope."
- It does not affect data correctness, accessibility contrast, or any
  of the six spec'd dashboard states — purely a font-family styling
  scope error on a few extra characters within an already-legible
  chip.
- issue-13's fix loop, which already closed the four numbered findings
  from execution-observation.md, deliberately scoped itself to F1-F4
  only and left this out — consistent precedent for treating it as a
  separate, lower-priority follow-up rather than a release blocker.
- Deferring it to backlog matches the hand-off pattern
  conformance-review.md itself already proposed (§5: "hand off to a
  follow-up issue for a future implementation role to pick up"); this
  role's contribution is to make that hand-off's non-blocking status
  explicit in the release record, per scout-brief.md §2's convention
  of naming known-accepted issues in release notes rather than
  omitting them.

## Explicit non-actions in this phase

Per contract v3 phase-1 scope, this proposal does **not**:

- Create a real git tag (`git tag`/`git push --tags`).
- File a real GitHub issue for the RoleChip backlog item.
- Write `docs/issue-4/reports/release-engineering.md` (the phase-2
  record — gated on human `APPROVE issue-4/release-engineering`).
- Modify `pyproject.toml`, `src/rsb/__init__.py`, or create
  `CHANGELOG.md` (all phase-2 actions if this proposal is approved).
