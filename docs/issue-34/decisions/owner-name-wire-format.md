# Decision: `board.json` gains `owner_name_by_repo`

## What changed

`board.json` — both the live `/api/board.json` endpoint and the static
Pages `rsb --json` output, since both are produced by the same
`render_json_model()` — gains a new top-level key:

```
owner_name_by_repo: dict[str, str | None]
```

Keyed by each configured repo's short config `name` (the same key already
used by `generated_at_by_repo`), mapping to that repo's `owner/name`
GitHub identifier as reported in its `flows --json` payload's top-level
`repo` field. The value is `None` (or the key is simply pointing at
`None`) when the source payload didn't carry `repo`.

## Why

Issue #34 needs to build `https://github.com/<owner>/<name>/issues/<n>`
and `.../pull/<n>` links on the dashboard. The `repo` (owner/name) field
already exists in every provider payload (`flows-schema.md` §1) but was
being dropped during normalization, so the frontend had no way to
construct a link. Rather than duplicating `owner_name` onto every one of
the 8 per-record dataclasses, this follows the existing
`generated_at_by_repo` pattern: one small map, keyed by the same short
repo name records already carry, populated in `merge_repos()`.

## Non-breaking / additive

- `schema_version` is unchanged — the upstream `flows --json` wire format
  is untouched; only `rsb`'s own normalization/aggregation output gains a
  field.
- Purely additive: existing consumers of `board.json` that don't know
  about `owner_name_by_repo` continue to work unmodified.
- No validation is performed on the value's shape — a falsy/`None`/
  non-string value passes through as-is; the frontend treats any falsy
  value as "no link available" (see `docs/issue-34/proposals/
  implementation.md`, Out-of-scope section).
