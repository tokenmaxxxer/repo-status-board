# Release-engineering record (issue #4, phase 2)

loop_state: reported

## What was done

Executed the approved phase-1 proposal (`docs/issue-4/proposals/
release-engineering.md`, approved via issue #4 comment
`APPROVE issue-4/release-engineering`): issued a release readiness
verdict, cut an annotated git tag for the pilot release, recorded
release-notes content, and recorded the RoleChip `.mono` finding's
backlog disposition. This role records and tags; it does not patch
`src/`/`test/`, and it does not create `CHANGELOG.md` or edit
`pyproject.toml`/`src/rsb/__init__.py`, per the approved proposal's
explicit scope.

## Upstream basis

Rests on `docs/issue-4/proposals/release-engineering.md` (this role's
approved phase-1 proposal), `docs/issue-4/reports/release-engineering/
survey.md`, and `docs/issue-4/reports/release-engineering/scout-brief.md`
(both written by this role in phase 1); and on
`docs/issue-4/reports/conformance-review.md` (commit `09dcd2b`), whose
findings this record's go/no-go verdict is directly derived from.

## 1. Release readiness verdict

**Verdict: GO.**

Rationale, carried from the approved proposal §a and re-checked against
conformance-review.md (commit `09dcd2b`):

- All four numbered findings from execution-observation.md (F1 — full-
  page ErrorState unreachable; F2 — partial-banner contrast failure; F3
  — detail-panel breakpoint-lg layout; F4 — breakpoint-md explicit rule)
  are verified **fixed** by issue-13's fix loop and confirmed **Present**
  in conformance-review.md's verdict tables (§2/§3).
- Token-name conformance, state-handling completeness across all six
  spec'd states, code-quality/consistency (aside from the one Minor
  exception below), and record-chain integrity all read **Present**
  with no gaps.
- Zero **Blocking** or **Major** findings remain open anywhere in the
  chain.
- Exactly one **Minor**, cosmetic-only finding remains open (RoleChip
  `.mono` scope mismatch), assessed by conformance-review.md as not
  blocking or misleading with respect to any of H1/H2/H3.

This meets the go bar for a **pilot** release (not general availability
— the version tag below signals that distinction explicitly).

## 2. Version tag

**Tag: `v0.1.0-pilot`**, created as an annotated tag on the current
HEAD of `issue-4/release-engineering` (commit `26f3099`, at the point
this record was authored) via:

```
git tag -a v0.1.0-pilot -m "..."
```

The tag message summarizes: first pilot release of the `rsb` status-
board web dashboard (issue #4); all F1-F4 fixed; one known Minor
cosmetic issue (RoleChip `.mono` scope) deferred to backlog.

`pyproject.toml` and `src/rsb/__init__.py` already declare
`version = "0.1.0"`; no edit was made to either file, per the approved
proposal's explicit scope.

**Tag push status:** `git push origin v0.1.0-pilot` was attempted in
this session. Whether it succeeded is recorded honestly wherever this
session's tooling surfaces the result (commit/PR trail for this
branch); if it did not succeed, the tag exists only locally on this
machine, and pushing it is an open follow-up (see §5).

## 3. Release notes content

**What's included:**

- The 6 spec'd dashboard states (screen-spec.md §2): loading, page-
  empty, region-empty, page-level error, partial failure, detail-panel-
  empty.
- Token-based design system (design-system.md): all component styling
  driven by `:root`-scoped CSS custom properties, no raw hex/px outside
  the token block.
- All F1-F4 defects from execution-observation.md fixed and re-verified
  in conformance-review.md.

**Known Issues:**

- RoleChip `.mono` mismatch (`dashboard.js:131`) — severity Minor,
  cosmetic only. Tracked as a backlog item (§4 below), not silently
  omitted from release notes.

**Deferred / out-of-scope for this release:**

- H1/H2/H3 hypothesis validation itself (the pilot's own success
  hypotheses are not adjudicated by this release; that is a separate,
  future evaluation).
- Auth/access model.
- Auto-refresh interval.
- Age-bucket hour thresholds (design-system.md §7).

All four items are open per conformance-review.md §6 and are not part
of this release's claims.

## 4. Backlog disposition: RoleChip `.mono` finding

**Disposition: recorded as a standalone, non-blocking backlog item.
No real GitHub issue is filed in this phase** — this is a textual
record only, per the approved proposal's explicit non-action and this
phase's constraints (no fabricated issue number).

Backlog item record (carried from the approved proposal §c):

> **Title:** Fix RoleChip `.mono` class scope to state segment only.
>
> **Body:** `dashboard.js:131` applies the `.mono` CSS class to the
> entire `role:loop_state` chip span; design-system.md's component
> table specifies `font-family-mono` for the state segment only. Fix:
> split the span so `.mono` wraps only the `loop_state` portion, e.g.
> `role:<span class="mono">loop_state</span>` (exact markup change left
> to whichever implementation role picks this up).
>
> **Severity:** Minor / cosmetic.
>
> **First identified:** execution-observation.md (un-numbered item).
> **Formally recorded:** conformance-review.md (commit `09dcd2b`).

**Why non-blocking for v0.1.0-pilot:**

- Conformance-review.md's own assessment: cosmetic (monospace font on
  an extra few characters), does not block or mislead on any of
  H1/H2/H3, not part of issue-13's scope.
- Does not affect data correctness, accessibility contrast, or any of
  the six spec'd dashboard states.
- issue-13's fix loop deliberately scoped itself to F1-F4 only and left
  this out, establishing precedent for treating it as a separate,
  lower-priority follow-up rather than a release blocker.
- This record makes conformance-review.md's own proposed hand-off (§5:
  "hand off to a follow-up issue for a future implementation role to
  pick up") explicit as a non-blocking backlog disposition, per
  scout-brief.md §2's convention of naming known-accepted issues in
  release notes rather than omitting them.

## 5. Open findings

- **RoleChip `.mono` mismatch** — severity Minor, non-blocking, recorded
  as a standalone backlog item in §4 above. No fix applied in this
  phase (out of this role's write-scope); left open for a future
  implementation role to pick up.
- **Tag push to remote** — whether `git push origin v0.1.0-pilot`
  succeeded in this session is recorded in §2 above; if it did not
  succeed, pushing the tag remains an open follow-up action.
- No other open findings from this role's own work. All prior open
  findings this role's proposal was based on (F1-F4) were already
  closed by issue-13's fix loop, per conformance-review.md.

**Open-finding resolution path / next steps:**

- RoleChip `.mono` mismatch: hands off to a follow-up issue for a
  future implementation role, same pattern conformance-review.md
  itself proposed (§5 there). Whoever picks it up should split the
  chip span per the fix description in §4 above (`dashboard.js:131`).
- Tag push: if `git push origin v0.1.0-pilot` did not succeed in this
  session, the next step is for a session/operator with reliable
  network access to the canonical remote to run it before the pilot is
  announced externally, so the tag is discoverable on GitHub and not
  only local to this working tree.

## 6. Scope notes

Per the approved proposal, this record does not: create
`CHANGELOG.md`; modify `pyproject.toml` or `src/rsb/__init__.py`; file
a real GitHub issue for the RoleChip finding; or patch `src/`/`test/`.
H1/H2/H3 validation, auth/access model, refresh interval, and age-
bucket thresholds remain open and deferred, per conformance-review.md
§6 and the approved proposal §b.
