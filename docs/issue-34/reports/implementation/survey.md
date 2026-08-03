# issue-34 current-state survey

## 1. owner/name exists upstream, is discarded locally

`flows-schema.md` §1 (`docs/specs/flows-schema.md:21,34`) documents a
top-level `repo: "<owner/name>"` field on every `flows --json` payload.
Every test fixture already carries it
(`test/rsb_tests/fixtures.py:8,58,69,98,118,144,190`, e.g.
`"tokenmaxxxer/on-the-record"`) — the provider side needs no change, exactly
as the issue body states.

`normalize_payload(repo_name, payload)` (`src/rsb/model.py:124-276`) never
reads `payload["repo"]`. It only pulls `schema_version`, the per-section
arrays, and `generated_at`. Every one of the 8 record dataclasses
(`Decision`, `Flow`, `Session`, `LedgerEntry`, `Unattributed`,
`HygieneClosureViolation` (via `raw`), `HygieneUnapprovedPr`, `RepoError`)
stamps its `repo` field from the `repo_name` **argument** — the config's
short `name` (`boards.toml`, `src/rsb/config.py:21,51-61`) — never from the
payload. `config.py` enforces short-name uniqueness per config
(`seen_names` set, `config.py:49,57-59`), so it's a safe map key.

## 2. an existing precedent for a parallel per-repo lookup

`merge_repos()` (`model.py:279-304`) already builds
`BoardModel.generated_at_by_repo: dict[short_name, str]` — a per-repo
lookup dict that sits alongside the flat per-record lists, keyed by the
same short name every record carries. This is a directly reusable shape
for owner/name: a second `dict[short_name, owner/name]`, populated the
same way, needs no change to the 8 record dataclasses themselves.

## 3. wire path from Python to the browser

`render.render_json_model()` (`render.py:169-182`) serializes `BoardModel`
via `_dataclass_to_dict` into the JSON blob returned by
`webserver.py`'s `/api/board.json` handler (`webserver.py:41-54`) and
by `rsb --json` (used by `.github/workflows/deploy-board.yml` for the
static Pages `board.json`, per `docs/handbooks/rsb.md` "Static deploy").
Both paths go through the same `render_json_model`, so one change there
reaches both consumers. Nothing here reads or emits owner/name today.

`render.py`'s CLI text renderer (`render_text`) is explicitly out of scope
per the issue body, mirroring the #23/#29 precedent — confirmed it has no
link concept to begin with (plain fixed-width text table).

## 4. frontend: where numbers render today

`dashboard.js` renders four tables — `decisionRows`, `flowRows`,
`sessionRows`, and the ledger rows inside `renderAccounting` — all through
`renderTable()` and all keyed off each row's `.repo` (short name) for the
issue-#29 repo filter (`filterByRepo`, `dashboard.js:105-121`) and the
`<select>` population (`repoList`, `updateRepoFilterOptions`,
`dashboard.js:127-133,418-425`).

- **Issue cells**, all four tables: already a real `<button
  class="row-toggle">` (`issueToggleCell`, `dashboard.js:204-208`), added
  by issue #23's execution-observation finding + issue #29 requirement 5
  specifically to replace a click-only `<tr>`. Issue #34's own text flags
  that overlaying a link on this same control would make the click target
  ambiguous — confirmed correct by reading the code: the button already
  owns `aria-expanded`/`aria-controls` for the detail-panel disclosure.
- **PR cells**: plain text today, no competing control —
  `decisionRows`'s `<td class="mono">${d.pr}</td>` (`dashboard.js:219`)
  and `flowRows`'s `<td class="mono">${f.prs.join(",") || "-"}</td>`
  (`dashboard.js:256`, comma-joined, can hold >1 PR number per flow).

`filterByRepo` (`dashboard.js:105-121`) returns a shallow copy
(`{...data, decisions: ..., flows: ..., ...}`) that only overrides the
fields it explicitly lists — any *other* top-level key on `data` (e.g. a
new `owner_name_by_repo`) passes through unchanged automatically, with no
edit needed to that function.

## 5. styling has room already reserved

`docs/specs/design-system.md` already documents `--space-1` as "icon-to-
label gap" (line 111) and `color-action-primary-*` as covering "refresh
button, links" / "text/icon on the above" (lines 61-62) — token support
for an icon-adjacent link exists; no new design tokens are needed.
`src/rsb/web/dashboard.css` has no icon/SVG usage anywhere yet — this
would be the first.

## 6. test surface (none assert an exact JSON key-set)

- `test/rsb_tests/test_model.py`: exercises `normalize_payload` /
  `merge_repos` per-field (spot-checks specific attributes, e.g.
  `normalized["decisions"][0].issue`).
- `test/rsb_tests/test_render.py`: exercises `render_json_model` /
  `render_text` from the same fixtures; `test_render_json_model_is_serializable_and_matches_data`
  spot-checks specific keys (`parsed["decisions"][0]["issue"]`, etc.), no
  `set(payload.keys()) == {...}` assertion anywhere.
- `test/rsb_tests/test_webserver.py`: exercises the full HTTP path,
  same spot-check style.

Adding one new additive top-level field to the normalized dict / JSON
output is a non-breaking change to all three — none needs an update for
existing assertions to keep passing, though new assertions should be
added to cover the new behavior (including the AC5 no-owner-name
fallback, which needs payloads/fixtures missing the `repo` key or holding
it as `None`).

## 7. no existing decisions-doc precedent

`docs/decisions/` doesn't exist at the repo-wide level, and no
`docs/issue-*/decisions/*.md` file exists in this repo yet (checked via
`find`). This issue's wire-format addition (`owner_name_by_repo`, a new
top-level `board.json` key) would be the first such doc under the
doctrine ladder (a changed public wire format gets a
`docs/issue-<n>/decisions/` entry).

## 8. approvers

`docs/specs/approvers.md`: `JiwonJung94`, `jjongkwann`.

## gaps this survey leaves for scout to aim at

- Where to place the external-link affordance for issue cells without
  colliding with the existing `row-toggle` button's click/keyboard
  semantics (issue's own req 2 flags this as unresolved).
- What accessible-name / decorative-icon pattern to use for an icon-only
  external link inside a table cell.
- New-tab vs. same-tab convention — no internal precedent exists to
  mirror (nothing in this codebase currently opens an external link).
