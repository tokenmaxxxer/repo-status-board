# Conformance-review record (issue #4)

loop_state: reported

## What was done

Re-verified F1-F4 (execution-observation.md) against current code as
fixed/not-fixed, formally recorded the RoleChip mono mismatch as a new
standalone finding, recorded the `:has()` browser-support gap as a
non-defect observation, and re-confirmed token-name/code-quality/
record-chain conformance per the approved proposal's four requirement
groups (§1-§4 below).

## Upstream basis

Rests on `docs/issue-4/proposals/conformance-review.md` (this role's
approved phase-1 proposal) and
`docs/issue-4/reports/conformance-review/survey.md` (this role's
current-state survey), both approved via issue #4 comment
`APPROVE issue-4/conformance-review`; and on
`docs/issue-4/reports/execution-observation.md` (predecessor record,
commit `0673bc2`), whose F1-F4 findings this record re-verifies against
the current code state (commit `d99a73c`, issue-13's fix loop). This
role records findings only — no code under `src/`/`test/` was changed
as part of this work.

Method: `review:finding-record` verdict set (Present / Surface / Absent
/ Incorrect / Unverifiable) per requirement, each with an evidence
pointer and rationale; `review:severity-classification` applied to
findings that survive, using a deterministic four-band lookup adapted
for this non-security context — **Blocking** (violates a spec
requirement in a way that defeats the pilot's hypotheses or misleads
the operator), **Major** (spec violation, user-visible, doesn't defeat
a hypothesis), **Minor** (spec violation, cosmetic/non-blocking), **Note**
(not a spec violation — an observation worth flagging).

## 1. Token-name conformance

| Requirement | verdict | Evidence | Rationale |
|---|---|---|---|
| No raw hex/px outside `:root` token block | Present | `dashboard.css:1-65` is the `:root` block; `grep -n '#[0-9a-fA-F]\{3,6\}' dashboard.css` returns zero hits outside it | All color values elsewhere in the file consume `var(--...)`, matching design-system.md's token-architecture requirement and the file's own header comment |
| Component→token mapping matches design-system.md §2-§6 | Present | `dashboard.css:127` (`.status-warning`), `:181/188` (`.partial-banner`), `:236-237` (breakpoint-lg media query) all reference the named tokens (`--color-status-warning-*`, `--breakpoint-lg`) | Spot-checked against execution-observation.md's item-by-item table (§5, 19 items); this pass re-confirms rather than re-derives |
| No invented backend fields | Present | `dashboard.js` field reads (`data.errors`, `data.generated_at_by_repo`, etc.) match `render_json_model` (`src/rsb/render.py`) output shape | Carried forward from survey's spot check; no new mismatch found on this pass |

## 2. State-handling completeness (screen-spec.md §2, six states)

| State | verdict | Evidence | Rationale |
|---|---|---|---|
| Loading (§2.1) | Present | `dashboard.js` `load()` calls `renderSkeleton()` before `fetch()` resolves (code read; no browser available to drive live, same limitation execution-observation.md recorded) | Matches spec by code reading; unchanged since execution-observation.md, not re-litigated |
| Page-empty (§2.2) | Present | `dashboard.js:264` `isPageEmpty(data)` branch; execution-observation.md §3 reproduced live | Carried forward, unaffected by issue-13's fixes |
| Region-empty (§2.3) | Present | `renderTable` `rows.length === 0` branch; execution-observation.md §3 reproduced live | Carried forward |
| Page-level Error / total failure (§2.4) | Present (was F1, now fixed) | `dashboard.js:234-236`: `succeededRepoCount = Object.keys(data.generated_at_by_repo).length; if (data.errors.length > 0 && succeededRepoCount === 0) renderFullError(...)` | Branch is now payload-based (checks `data.errors`/`generated_at_by_repo` directly), independent of HTTP status, so an all-repos-error payload reaches `renderFullError()` — the gap execution-observation.md's F1 identified (HTTP-status-only trigger, server always returns 200) no longer exists. Re-verified by code read; not re-driven live over HTTP in this session, matches survey's read |
| Partial failure / banner (§2.5) | Present (was F2, now fixed) | `dashboard.css:181,188`: `.partial-banner`/`.partial-banner a, .partial-banner button.link { color: var(--color-status-warning-foreground) }`; `:36` defines the token as `var(--color-amber-700)` | Retry link now uses the warning-foreground fallback token screen-spec.md §2.5 anticipated, replacing the prior white-on-near-white pairing (F2's ~1:1 contrast failure) |
| Detail-panel-empty (§2.6/§1.6) | Present | `renderDetailPanel` copy match, code read only (same browser-automation limitation as Loading) | Unchanged since execution-observation.md, not re-litigated |

## 3. Code quality/consistency

| Requirement | verdict | Evidence | Rationale |
|---|---|---|---|
| Detail-panel breakpoint-lg layout switch (§1.6/§5) | Present (was F3, now fixed) | `dashboard.css:236-237`: `@media (min-width: 1200px) { #page-body:has(#detail-panel-slot:not(:empty)) { ... } }` restructures to a two-column grid with `position: sticky` | Two-column grid now exists above `--breakpoint-lg` (1200px), matching §1.6/§5's side-panel-vs-row description; the prior single-column-at-every-width gap (F3) is closed |
| `breakpoint-md` (768px) explicit rule (§5) | Present (was F4, now fixed) | `dashboard.css:244-245`: `@media (max-width: 768px) { .summary-strip { gap: var(--space-2); } }` | An explicit `max-width: 768px` rule now exists; execution-observation.md's F4 noted its absence (chip-wrap worked incidentally via unconditional `flex-wrap`, but no dedicated rule existed) |
| RoleChip: `font-family-mono` on state segment only | Incorrect | `dashboard.js:131`: `` `<span class="badge status-neutral mono">${escapeHtml(r.role)}:${escapeHtml(r.loop_state)}</span>` `` — `.mono` class applied to the whole span, covering `role:loop_state` | spec_vs_built: design-system.md's component table specifies `font-family-mono` for the state text only; the built span applies it to the entire `role:loop_state` string including the role segment. Same defect execution-observation.md recorded as an un-numbered item, confirmed still present and unfixed — issue-13's fix loop scoped itself to F1-F4 only, this was never in its scope |
| `escapeHtml` used consistently on interpolated user/repo-controlled strings | Present | `dashboard.js:131` (`escapeHtml(r.role)`, `escapeHtml(r.loop_state)`), and consistent use across `renderTable`/`renderHygiene`/`renderErrors` call sites | Spot-checked call sites all wrap repo/session/role-controlled string interpolation; no bare interpolation of untrusted strings found |

## 4. Record-chain integrity

| Requirement | verdict | Evidence | Rationale |
|---|---|---|---|
| Every phase-2 record cites its approving comment + predecessor artifact | Present | `docs/issue-4/reports/execution-observation.md:3-7`, this file's own header above | Both cite `APPROVE issue-4/<role>` and the proposal they built from |
| Commit `Subject:` trailers match branch/issue | Present | `git log --oneline`: `d99a73c issue-13 phase 2...`, `202ebc1 issue-13 phase 1...`, `0673bc2 issue-4 phase 2...` | Subject lines consistently prefix the issue number matching their branch |
| issue-13's fix-loop stayed inside its own write-scope | Present | `git show --stat` on PRs #14/#15 (per survey) touches only `src/rsb/web/*` and `docs/issue-13/*` | No edits to `docs/specs/*` or other roles' `docs/issue-4/*` areas from the fix loop |

## 5. Open findings

Resolution path: both findings below hand off to a follow-up issue for
a future implementation role to pick up (same hand-off pattern
execution-observation.md used for F1-F4); this role does not patch
`src/`/`test/` itself. Next steps: file a follow-up GitHub issue
covering the RoleChip mismatch (the `:has()` item needs no fix, only
awareness).

- **RoleChip mono mismatch** — severity: **Minor**. `dashboard.js:131`
  applies `.mono` to the entire `role:loop_state` chip text instead of
  only the state segment, per §3 above. Cosmetic (monospace font on an
  extra few characters), does not block or mislead on any of H1/H2/H3,
  not part of issue-13's scope. First formally recorded here as a
  standalone finding (execution-observation.md named it but only
  numbered F1-F4; this was its explicit un-numbered item).
- **`:has()` selector browser-support gap** — severity: **Note** (not a
  spec violation). `dashboard.css:237` uses `#page-body:has(...)`,
  a CSS feature with real but not universal browser support (baseline-
  newly-available as of 2023 in evergreen browsers; absent in older
  ones). screen-spec.md states no browser-support floor anywhere, so
  this is not a defect against the spec as written — flagged because
  it is the only modern-CSS-feature dependency in the file and the
  spec is silent on a support baseline, which is itself worth naming
  for whoever picks up the open design-system.md §7 items.

No other findings. F1-F4 (execution-observation.md) all re-verified as
fixed by direct code inspection (§2, §3 above); none reopened.

## 6. Scope notes

- H1/H2/H3, age-bucket hour thresholds (design-system.md §7), auth/
  access model, and auto-refresh interval remain open/deferred per
  screen-spec.md §5 and are not addressed by this role, per the
  proposal's stated out-of-scope list.
- Per contract, this record reports findings; it does not patch
  `src/`/`test/`. The RoleChip finding hands off the same way F1-F4
  did, to a follow-up issue.
