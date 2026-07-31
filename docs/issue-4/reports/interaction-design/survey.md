# Current-state survey — issue #4, interaction-design phase 1

Status: phase-1 survey. Scope: interaction-design role only — inputs
consumed, gap this phase must fill. Screen/flow content itself is in
`docs/issue-4/proposals/screen-spec.md`, not here.

## 1. What exists today: `rsb` CLI (issue-1)

`rsb` (`src/rsb/`) is a terminal status board over one or more repos'
`flows --json` payloads (schema_version 1, `src/rsb/model.py`):

- **decisions** (`decision_queue`): repo, issue, pr, phase, role,
  opened_at, age_hours, awaiting — sorted by age_hours descending.
  This is the "does anything need me" queue.
- **flows**: repo, issue, stage (+ stage_derived flag), roles (each with
  loop_state, verdict), prs (list of PR numbers).
- **sessions**: repo, role, issue, elapsed_min, pid, alive, verdict,
  last_activity (ts/kind/detail or null).
- **ledger**: repo, issue, sessions count, cost_usd_total, outcomes
  (dict), plus a repo-level `unattributed` (sessions, cost_usd_total)
  bucket.
- **hygiene**: closure_sweep violations (issue, violation, detail) and
  unapproved_open_prs (issue, pr, role, opened_at).
- **errors**: per-repo `RepoError(repo, message)` — a repo that failed
  to fetch/normalize is dropped from the other sections but reported here,
  not treated as a whole-run failure (`_run_once` only fails when *every*
  repo failed).

CLI surface: `rsb [--config PATH] [--repo NAME...] [--watch [N] | --once]
[--no-color] [--json]`. `render_text` produces the exact single-screen
layout (header, decision queue, flows, sessions, accounting, hygiene,
errors) that today's pilot problem statement says is "tied to one
terminal". `render_json_model` is the exact shape the web dashboard would
consume — it is already the CLI's `--json` output, one BoardModel per
render.

## 2. What issue-4's product-discovery phase established

`docs/issue-4/proposals/hypotheses.md` (approved, phase-1 of the
product-discovery role):

- **Problem (hypothesis, unconfirmed):** operator away from the terminal
  cannot answer "does anything need my decision right now?" without
  switching back, causing missed/delayed decisions or needless
  context-switches.
- **H1 (need exists):** off-terminal checks ≥3x/week when available.
- **H2 (glance sufficiency):** a single-screen read-only web view of the
  same `flows --json` data answers "does anything need me" without a
  follow-up terminal check, for ≥80% of checks.
- **H3 (attention signal, deferred):** age-bucketed decision-queue
  surfacing reduces missed/late approvals — not gated for this pilot.
- Pre-registered metrics/thresholds and a mechanical day-14 decision
  rule (KILL / KILL / REVISE / SPEC) are fully specified; this phase
  proceeds under the assumption the chain has reached "SPEC" (the
  orchestrator has already routed this issue to interaction-design per
  the chain rule in the issue body).
- Explicitly deferred to interaction-design: screens/routes/visual
  design, and the auth/access model for exposing `flows --json`-derived
  data over the web (flagged as a hand-off, not decided — this survey
  does not resolve it either; screen-spec.md notes it as a structural
  open question, not a UI element).

## 3. Gap this phase must fill

Translate the validated hypotheses into a **concrete single-screen web
layout and flow spec**, grounded in the exact fields `BoardModel` /
`render_json_model` already exposes (no new fields invented), that:

- Answers "does anything need me" at a glance (serves H2 directly).
- Makes the decision queue's age visible (lays groundwork for H3 without
  gating on it).
- Specifies Loading/Empty/Error states per region, since a web view
  (unlike the CLI's synchronous render) has a network round trip and a
  now-explicit multi-repo partial-failure case (`model.errors`) that the
  CLI already models but a web UI must render distinctly from "nothing to
  show."

## 4. Scout brief (informed-assumptions mode)

This run used **informed-assumptions mode, not live web search** (session
budget constraint) — no external sources were fetched. The following are
therefore **assumptions**, drawn from general familiarity with established
ops/status dashboard UX (Grafana panels, Datadog/status-page style
single-glance views, GitHub's own status dashboard), not sourced
citations:

- **Top summary strip + detail table(s) below.** A glance-first layout
  puts the "does anything need me" answer (counts/badges) above the fold,
  with the full decision-queue/flows/sessions detail as scannable tables
  underneath — matches the CLI's existing section order and the
  glance-and-return usage pattern from hypotheses.md.
- **Skeleton/placeholder loaders per region, not a single full-page
  spinner.** Independent per-region loading avoids a slow ledger fetch
  blocking the decision queue from rendering — relevant here since
  multiple repos are fetched and can fail/succeed independently
  (`model.errors` is already per-repo).
- **Inline banner for partial failure vs. full-page error for total
  failure.** Distinguishing "some repos failed" (banner, rest of screen
  still useful) from "nothing loaded" (full-page error + retry) maps
  directly onto `_run_once`'s existing distinction between some-errors
  and all-repos-failed.
