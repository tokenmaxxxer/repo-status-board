---
proposal: docs/issue-62/proposals/implementation.md
---

# Hunt record — issue-62 implementation

Note on report path: the dispatch prompt named a per-issue report path
under the issue-62 reports tree owned by another role, but the repo's
board-gate hook (contract v3 s11) refuses that filename for the current
role (CLAUDE_ROLE=implementation, branch=issue-62/implementation) as a
foreign record — that role may write only its own record and subtree
there. Filing this hunt record under the standing top-level reports
bucket instead, which the same gate allows for a role session in a board
repo.

## before-landing — stance 0: assume the gate just touched is bypassable — find the bypass

Verdict: FINDING — `_redact_paths` in fetch.py fails to redact any path whose directory component contains a space, leaking the internal directory structure verbatim into the RuntimeError message (and from there into BoardModel.errors[].message / api/board.json / the rendered dashboard).
Kind: silent-failure
Seed: src/rsb/fetch.py (`_PATH_PATTERN` / `_redact_paths`, applied at the OSError and nonzero-exit RuntimeError sites in `run_flows_json`); test/rsb_tests/test_fetch.py new masking tests
cap_seconds: 180
tier: size:large
diff_stat_lines: 216 insertions / 14 deletions across 6 files (per dispatcher's git diff --stat)
started_at: 2026-08-08T03:19:53Z
ended_at: 2026-08-08T03:24:30Z

### Reproduce
```
python3 - <<'PY'
import sys, subprocess
sys.path.insert(0, "src")
from rsb.config import RepoConfig
from rsb.fetch import run_flows_json

fixture_path = "/Users/Jane Doe/.secret-checkout/repo"

class FakeCompleted:
    returncode = 1
    stdout = ""
    stderr = "Traceback (most recent call last):\nFileNotFoundError: %s/flows.json not found\n" % fixture_path

def fake_run(argv, **kwargs):
    return FakeCompleted()

subprocess.run = fake_run
repo = RepoConfig(name="broken-flows", path="/x", command=["python", "spawn.py"])

try:
    run_flows_json(repo)
except RuntimeError as e:
    print("message:", str(e))
PY
```

### Observed
```
message: flows --json failed: FileNotFoundError: Jane Doe/.secret-checkout/repo/flows.json not found
```
`.secret-checkout` (the sensitive directory name the redaction is specifically supposed to hide) and the `Jane Doe` username fragment both survive in the message that `fetch_and_normalize_one` returns verbatim as `error_message`, which `merge_repos` places into `BoardModel.errors[].message` — the exact sink the R5d claim says never sees an internal path. Root cause: `_PATH_PATTERN = re.compile(r"(?<!\S)/(?:[^\s/]+/)+[^\s/]*")` requires every path segment to contain no whitespace (`[^\s/]+`), so on a directory name containing a space the match terminates at the space and `os.path.basename()` is applied only to the truncated prefix (`/Users/Jane` → `Jane`), leaving everything after the space (`Doe/.secret-checkout/repo/flows.json`) untouched and unredacted.

The two new tests that back this claim (`test_run_flows_json_oserror_masks_internal_path`, `test_run_flows_json_nonzero_exit_masks_internal_path`) both use fixture paths with no spaces (`/Users/ci-runner/.secret-checkout/spawn.py`, `/Users/ci-runner/.secret-checkout/repo`), so this gap is untested and currently invisible — the guard looks like it fully masks paths but silently stops working the moment a real-world path (e.g. any macOS home directory with a space in the account's full name, "Program Files", a cloud-sync folder like "OneDrive - Company Name") appears in subprocess stderr.

### Expected
Either the regex should match path segments containing spaces (or the function should fall back to whole-string basename-per-token more conservatively), or the masking claim should be scoped to "paths without embedded whitespace" rather than "internal absolute filesystem paths never reach the caller."
