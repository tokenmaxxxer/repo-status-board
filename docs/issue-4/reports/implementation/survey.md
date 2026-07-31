# Current-state survey — implementation (issue #4)

## What exists (`src/rsb/`)

- `config.py` (63 lines): loads `boards.toml`, `RepoConfig` list.
- `fetch.py` (70 lines): `run_flows_json` shells out to `<command> flows
  --json -C <path>` per repo; `fetch_board` aggregates all repos,
  captures per-repo failures without aborting the whole run (partial
  failure already modeled here).
- `model.py` (261 lines): normalizes raw `flows --json` payloads (per
  `docs/specs/flows-schema.md`) into typed dataclasses — `BoardModel`
  with `decision_queue`, `flows`, `sessions`, `ledger`, `unattributed`,
  `hygiene`, plus per-repo `errors`.
- `render.py` (182 lines): `render_text` (terminal layout) and
  `render_json_model` (`_dataclass_to_dict` serialization of `BoardModel`
  — a JSON-safe dict, generated_at included). This is the field-source
  screen-spec.md's §"Grounding" note points to.
- `cli.py` (89 lines): argparse entrypoint, one-shot terminal render.

## Write surfaces this role owns (`src/`, `test/`)

No web/server code exists yet. Nothing under `src/` currently serves
HTTP or emits static assets — `rsb` is CLI-only, one-shot process exit.

## Gaps this implementation phase must close

1. No HTTP-servable JSON endpoint — `render_json_model` output currently
   only reaches stdout via the CLI. Needs a thin server (or a
   file-writing "dump" mode + static server) exposing the same JSON.
2. No frontend at all — no HTML/CSS/JS implementing screen-spec.md's
   regions, tokens, or states (loading/empty/partial-failure/full-error).
3. No polling/refresh loop (screen-spec.md's refresh button + implicit
   auto-refresh is deferred per spec §5, but manual refresh must work).
4. No tests for any new web-serving code (`test/rsb_tests` currently
   covers CLI/model/fetch only — confirmed by directory name, not
   re-read in full since only the new surface needs new tests).

## Frozen upstream contracts available (no re-negotiation needed)

- `docs/specs/flows-schema.md` — data shape, already consumed by
  `model.py`/`render.py`.
- `docs/specs/design-system.md` — tokens (accepted).
- `docs/specs/screen-spec.md` — layout, states, traceability (accepted).

## Skip condition check (scout-directive)

Scouting was NOT skipped — the implementation stack (server mechanism,
frontend approach) is an open design decision not fixed by any frozen
spec (screen-spec.md explicitly excludes `src/` from its scope). See
`scout-brief.md` for the sweep result.
