# Current-state survey — issue #4 (web dashboard pilot, product-discovery phase)

## What exists today
- `rsb` (src/rsb): terminal CLI, reads `<command> flows --json -C <path>` per
  registered repo, renders one screen — decision queue, flows, sessions,
  ledger/accounting, hygiene, errors. Config via TOML (`--config` /
  `$RSB_CONFIG` / `~/.config/rsb/boards.toml`). Has `--watch`, `--json`,
  `--repo` filter. No auth, no network exposure — local process only.
- Data contract: `docs/specs/flows-schema.md` (mirrored from upstream
  `on-the-record`, frozen for issue #172). Top-level: `decision_queue[]`
  (PRs awaiting phase-1/phase-2 approval, with `age_hours`, `awaiting`
  reason), `flows[]` (per-subject stage/role/verdict), `sessions[]`,
  `ledger[]` (cost/accounting), `hygiene{}`. This is the only data source;
  the dashboard has nothing to build on beyond this JSON payload.
- Consumer: solo operator (Jiwon Jung), running `rsb` themselves in a
  terminal today. No other consumers exist. No usage/adoption data exists
  because there is no distributed/web deployment yet — this is 0→1.

## Gaps relevant to this issue
- **No web/browser delivery path** — `rsb` is CLI-only, tied to one
  terminal on one machine; the issue's stated problem is exactly this
  (operator wants board state visible off-terminal, other devices).
  Unknown: static rebuild vs. live server vs. polling — none decided yet.
  Not this role's call (interaction-design/ux-engineering downstream).
- **No pre-registered success/kill signal** for a dashboard pilot —
  nothing in this repo defines what "worth keeping" or "worth killing"
  looks like for a web view. This is squarely product-discovery's gap to
  fill (issue #4 asks for hypotheses, metrics, thresholds, decision rule).
  See `docs/issue-4/proposals/hypotheses.md`.
- **No staleness/attention model** — `decision_queue[].age_hours` exists
  in the schema but `rsb` v1 does not appear to threshold or visually
  flag it (per `docs/issue-1/reports/implementation.md` — v1 renders flat
  sections, no bucketing/coloring by age). A web view inherits this gap
  unless product-discovery's hypothesis calls it out.
- **Single user** — the "operator" is one person (repo owner). Any
  hypothesis about "who needs this and why" must be scoped to a solo
  operator checking their own multi-repo agent fleet, not a team.

## Scope note
This survey covers product-discovery's write surface only: problem
framing, metrics, and decision rule. It does not propose UI, screens, or
implementation — those are interaction-design's and later roles' problem
per the issue's stated chain.
