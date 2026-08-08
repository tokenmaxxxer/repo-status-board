---
kind: coding-record
subject: issue-73
produced_by: implementation
code_under_review: .gitignore
type: fix
breaking: false
verdict: pass
loop_state: landed
---

## What was done

Added a `node_modules/` entry to the repo-root `.gitignore`, per the approved
phase-1 proposal (`docs/issue-73/proposals/gitignore-node-modules.md`).

## Why

Closes the unowned hand-off from issue-44: `npm install --prefix test`
(documented in the test handbook) creates `test/node_modules/`, which was
untracked but not ignored, leaving `git status` dirty after a routine setup
step.

## Upstream basis

docs/issue-73/proposals/gitignore-node-modules.md, approved via the
issue-level comment `APPROVE issue-73/implementation`.

## Verification run this session

- `grep -q node_modules .gitignore` — passes.
- `npm install --prefix test` — installed jsdom (38 packages) into
  `test/node_modules/`.
- `git status --porcelain` after install — shows only `M .gitignore`; no
  untracked `test/node_modules` entries.
- `python3 -m pytest test/ -q` — 77 passed.

## What did not work

None.

## Doc placement

No env var, config key, dependency, migration, or setup step was
introduced — nothing to place on the handbook/decisions/reports ladder
beyond this record itself.

## Open findings

None.

## Hunt cadence

Warrant-hunter dispatch is subordinate to contract v3 s22 in this headless,
single-shot session: a background hunter's result could not be consumed
within this turn, so none was dispatched. This is a docs+config-only,
single-line change (`.gitignore` add) with no code-path or logic surface for
a hunter to probe.
