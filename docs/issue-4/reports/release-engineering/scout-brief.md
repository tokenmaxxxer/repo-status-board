# Scout brief: versioning + backlog-disposition conventions (issue #4, phase 1)

loop_state: reported

Scope: lightweight external-convention check (live web search) feeding
this role's proposal. Two questions: semver for a first pilot release,
and how teams typically record "known minor issue accepted,
non-blocking" decisions.

## Must-bes

- Semver's own spec (semver.org) is explicit that MAJOR=0 means
  "initial development... anything MAY change at any time... the
  public API SHOULD NOT be considered stable." `1.0.0` signals a
  stability/back-compat promise the maintainer chooses to make going
  forward, not a completeness milestone.
- `0.1.0` (not `0.0.x`) is the conventional choice for "first release
  with real, usable functionality" — `0.0.x` is reserved for
  pre-functional/placeholder scaffolding.

## Patterns observed

- This repo's `pyproject.toml`/`src/rsb/__init__.py` already declare
  `0.1.0` — consistent with the convention above (working CLI + web
  dashboard, not a placeholder). No prior git tag exists.
- Pre-release suffix conventions (`-pilot`, `-alpha`, `-rc.1`) are
  widely used and explicitly supported by semver's `-<identifiers>`
  grammar to mark a release as provisional without inventing a
  separate numbering scheme.
- Decision-log/issue-log convention: known-and-accepted minor issues
  get logged with a severity rating, an impact note, and an explicit
  "accepted, non-blocking" disposition at release-approval time — not
  silently dropped from release notes, and not required to block a
  release just because it exists. A decision log is described as the
  connective record between issue logs and backlogs (i.e., the record
  of *the decision to defer*, separate from wherever the work item
  itself eventually lives).

## Adopt / skip

- **Adopt**: stay in `0.x` for this tag (proposed `v0.1.0-pilot`) —
  matches semver's own guidance and the project's already-declared
  `0.1.0`; do not jump to `1.0.0` given open H1/H2/H3 hypotheses and
  deferred design questions (auth model, refresh interval, age-bucket
  thresholds — screen-spec.md §5 / design-system.md §7).
- **Adopt**: record the RoleChip-mono disposition as an explicit
  "accepted, non-blocking, deferred to backlog" decision with
  severity, evidence pointer, and reasoning in release notes — not a
  silent carry-forward.
- **Skip**: adopting a full formal decision-log/issue-log tool or
  template (e.g. a Jira-style decision log or separate risk register)
  — this repo has no such infrastructure, and standing one up is out
  of proportion to a single Minor, non-blocking cosmetic finding on a
  pilot release.

## Sources

- [Semantic Versioning 1.0.0](https://semver.org/spec/v1.0.0.html)
- [Semantic Versioning 0.1.0](https://semver.org/spec/v0.1.0.html)
- [Semantic Versioning and Conventional Commits — negg Blog](https://negg.blog/en/semantic-versioning-and-conventional-commits/)
- [Decision log using Jira and Automation — Bethink (Medium)](https://medium.com/bethink-pl/decision-log-using-jira-and-automation-the-holy-grail-of-documenting-decisions-8d37ad3f1f2b)
- [Decision Logs & Records — Platform Development Playbook](https://playbook.platformdev.amdigital.co.uk/Ways-of-Working/Toolkit/Decision-Records/)
