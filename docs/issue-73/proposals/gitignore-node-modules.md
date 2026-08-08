---
status: proposed
files:
  - .gitignore
---

## Request

Add a `node_modules/` ignore entry to the repo-root `.gitignore` so `npm install --prefix test` (as documented in the test handbook) does not leave untracked files in the tree.

## Constraints

- Pure bugfix, one line, no design decision: scout-directive and survey-order-directive skip condition "pure bugfix" applies — no scout brief or survey.md written.
- Scope is exactly the write set below; nothing else in `.gitignore` changes.

## Rationale

Chosen approach: append a `node_modules/` line to root `.gitignore`. Rejected alternative: scoping the ignore to `test/node_modules/` specifically — rejected because `node_modules/` as a gitignore pattern already matches at any depth (including under `test/`), so a narrower path-qualified entry adds no coverage and only adds a second line to maintain if another `node_modules/` directory appears elsewhere later.

## What will be done

- Add `node_modules/` to `.gitignore`.
- Run `npm install --prefix test` and confirm `git status --porcelain` shows no untracked `test/node_modules` entries.
- Run `python3 -m pytest test/ -q` to confirm it still passes.

## Out of scope

- Any other `.gitignore` cleanup.
- Changes to the test handbook or npm setup.

## How you'll know it worked

- `grep -q node_modules .gitignore` succeeds.
- After `npm install --prefix test`, `git status --porcelain` shows no untracked `test/node_modules` entries.
- `python3 -m pytest test/ -q` passes.
