# Release-engineering survey (issue #4, phase 1)

loop_state: surveyed

Scope: current-state survey feeding this role's phase-1 proposal
(`docs/issue-4/proposals/release-engineering.md`). Read-only role at
this stage — no code or foreign-role docs touched.

## 1. Build/version state

- `pyproject.toml:1-3`: `name = "repo-status-board"`, `version =
  "0.1.0"`, `description = "Status board CLI consuming
  tokenmaxxxer's \`spawn.py flows --json\`"`.
- `src/rsb/__init__.py:3`: `__version__ = "0.1.0"` — matches
  `pyproject.toml`, no drift between the two version declarations.
- `[project.scripts]` in `pyproject.toml:9-10` registers `rsb =
  "rsb.cli:main"` as a console-script entry point.
- Build backend: `setuptools>=61.0` / `setuptools.build_meta`
  (`pyproject.toml:12-14`); packages discovered from `src/`
  (`[tool.setuptools.packages.find] where = ["src"]`).
- No `CHANGELOG`/`CHANGELOG.md` file exists anywhere in the repo root
  (checked with `find . -maxdepth 2 -iname "CHANGELOG*"`, zero hits).
- No git tags exist (`git tag -l` returns empty) — this would be the
  first tagged release if one is cut.
- No `Makefile`, no CI/release-workflow config discovered at repo
  root beyond the standard Python packaging files; no PyPI/registry
  publishing config found.
- Web assets ship as plain static files under `src/rsb/web/`
  (`index.html`, `dashboard.js`, `dashboard.css`) served by
  `rsb.webserver` — no separate JS build/bundle step, no `package.json`
  in the repo (confirmed: only `pyproject.toml` matches at
  `find . -maxdepth 2 -iname package.json` — zero hits).

## 2. Deployment/packaging state

- Distribution mechanism: standard `setuptools` sdist/wheel via
  `pyproject.toml`; installed via `pip install` (editable or built),
  exposing the `rsb` CLI entry point. No containerization
  (no `Dockerfile` found), no deployment manifests found in this
  survey pass.
- The web dashboard (issue #4's subject) is served by `rsb serve`
  (implemented in `src/rsb/web/` + `rsb.webserver`), not deployed as a
  separate artifact — it ships inside the same package as the rest of
  the `rsb` CLI. There is no separate versioning for the dashboard vs.
  the CLI as a whole.

## 3. Versioning scheme

- Current single version number (`0.1.0`) is shared by the whole
  package (CLI + web dashboard); no independent versioning for the
  dashboard feature.
- No evidence of any prior release cut for this repo (no tags, no
  changelog, no release notes anywhere in `docs/`).

## 4. Upstream verdicts and severities (docs/issue-4/reports/ chain)

### conformance-review.md (phase-2 record, commit `09dcd2b`)

Per-requirement verdict table (`review:finding-record` verdict set:
Present/Surface/Absent/Incorrect/Unverifiable), §1-§4:

- §1 Token-name conformance — all three requirements: **Present**.
- §2 State-handling completeness (6 states) — all six: **Present**,
  explicitly noting page-error and partial-failure are "(was F1, now
  fixed)" / "(was F2, now fixed)".
- §3 Code quality/consistency — detail-panel breakpoint-lg layout
  ("was F3, now fixed"): **Present**; `breakpoint-md` explicit rule
  ("was F4, now fixed"): **Present**; RoleChip
  `font-family-mono`-on-state-segment: **Incorrect** (see §5 below);
  `escapeHtml` consistency: **Present**.
- §4 Record-chain integrity — all three requirements: **Present**.

No single "PASS/CONDITIONAL/FAIL" headline verdict word appears in
the file; the operative signal is the verdict table itself — every
requirement reads **Present** except the one **Incorrect** (RoleChip
mono), which the same document classifies as **Minor** severity and
explicitly non-blocking (see §5). §5 "Open findings" states:
"Cosmetic (monospace font on an extra few characters), does not block
or mislead on any of H1/H2/H3, not part of issue-13's scope."

Quoted directly from `docs/issue-4/reports/conformance-review.md:73-100`
(§5 "Open findings"):
> - **RoleChip mono mismatch** — severity: **Minor**. `dashboard.js:131`
>   applies `.mono` to the entire `role:loop_state` chip text instead of
>   only the state segment, per §3 above. Cosmetic (monospace font on an
>   extra few characters), does not block or mislead on any of H1/H2/H3,
>   not part of issue-13's scope. First formally recorded here as a
>   standalone finding (execution-observation.md named it but only
>   numbered F1-F4; this was its explicit un-numbered item).
> - **`:has()` selector browser-support gap** — severity: **Note** (not a
>   spec violation). ... this is not a defect against the spec as
>   written — flagged because it is the only modern-CSS-feature
>   dependency in the file and the spec is silent on a support
>   baseline...

Closing line of §5: "No other findings. F1-F4 (execution-observation.md)
all re-verified as fixed by direct code inspection (§2, §3 above); none
reopened."

### execution-observation.md (predecessor phase-2 record, commit `0673bc2`)

- `test/` re-run: "33 passed, 0 failed" (§1), independently reproduced,
  matching implementation.md's own claim.
- §5 spec-conformance pass: "Total: 15 of 19 checked items match; 4
  mismatches (2 significant — F1, F2; 2 minor — F3/RoleChip-mono, F4)."
- §6 named four numbered findings (F1 significant/correctness, F2
  significant/accessibility-contrast, F3 minor, F4 minor), plus an
  un-numbered "RoleChip minor mismatch" item (later formally elevated
  to a standalone Minor finding by conformance-review.md).
- All four numbered findings (F1-F4) are recorded by
  conformance-review.md as **fixed** by issue-13's fix loop (commits
  `202ebc1`/`d99a73c`); only the RoleChip mono item and the `:has()`
  observation remain open as of the latest record.

## 5. RoleChip mono finding — exact location and text (as requested)

- **Severity**: Minor (per conformance-review.md §5; also listed as
  one of the "2 minor" mismatches in execution-observation.md §5's
  "15 of 19... 4 mismatches" tally).
- **Location**: `src/rsb/web/dashboard.js:131` — confirmed by direct
  read in this survey:
  ```
  `<td>${f.roles.map((r) => `<span class="badge status-neutral mono">${escapeHtml(r.role)}:${escapeHtml(r.loop_state)}</span>`).join(" ")}</td>`,
  ```
  The `.mono` class is applied to the whole `<span>`, covering the
  entire `role:loop_state` string, not only the `loop_state` segment.
- **Spec requirement**: `docs/specs/design-system.md`'s component
  table specifies `font-family-mono` for the state text only (per
  conformance-review.md §3's rationale column).
- **Disposition already on record**: conformance-review.md §5 states
  resolution path is "hand off to a follow-up issue for a future
  implementation role to pick up (same hand-off pattern
  execution-observation.md used for F1-F4)"; explicitly not blocking
  ("does not block or mislead on any of H1/H2/H3").

## 6. Open findings summary (as of latest record, commit `09dcd2b`)

| Finding | Severity | Status |
|---|---|---|
| F1 full-page ErrorState unreachable | Significant | Fixed (issue-13) |
| F2 partial-banner Retry-link contrast | Significant | Fixed (issue-13) |
| F3 detail-panel breakpoint-lg layout | Minor | Fixed (issue-13) |
| F4 breakpoint-md explicit rule missing | Minor | Fixed (issue-13) |
| RoleChip `.mono` on whole span | **Minor** | **Open**, no owner yet |
| `:has()` browser-support gap | Note (not a spec violation) | Open observation only, no fix needed |

Only one substantive open finding remains at Minor severity; no
Blocking or unresolved Major/significant findings on record.

## 7. Scouting-applies judgment

This deliverable (release readiness verdict + version-tag plan +
backlog disposition for the RoleChip finding) is judgment-bearing —
it commits to a semver choice and a release-readiness call that later
roles/consumers will rely on. Scouting applies; see
`docs/issue-4/reports/release-engineering/scout-brief.md` for the
lightweight external-convention sweep.
