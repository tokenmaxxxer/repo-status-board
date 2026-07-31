import json
import threading
import urllib.request

from rsb.model import merge_repos, normalize_payload
from rsb.webserver import make_handler

from .fixtures import EMPTY_PAYLOAD, WORKED_EXAMPLE


def _serve(fetch_board_fn, log_path=None):
    from http.server import ThreadingHTTPServer

    handler = make_handler(fetch_board_fn, repo_configs=[], log_path=log_path)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop(server, thread):
    server.shutdown()
    thread.join(timeout=5)
    server.server_close()


def test_api_board_json_returns_normalized_shape(tmp_path):
    def fetch_board_fn(_repo_configs):
        return merge_repos([("on-the-record", normalize_payload("on-the-record", WORKED_EXAMPLE), None)])

    server, thread = _serve(fetch_board_fn)
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/board.json") as resp:
            assert resp.status == 200
            assert resp.headers.get("Content-Type") == "application/json"
            payload = json.loads(resp.read())
        assert payload["decisions"][0]["issue"] == 172
        assert payload["flows"][0]["stage"] == "implementing"
        assert "generated_at" in payload
    finally:
        _stop(server, thread)


def test_api_board_json_partial_failure_returns_200_with_errors():
    def fetch_board_fn(_repo_configs):
        return merge_repos([
            ("on-the-record", normalize_payload("on-the-record", EMPTY_PAYLOAD), None),
            ("broken-repo", None, "flows --json failed: boom"),
        ])

    server, thread = _serve(fetch_board_fn)
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/board.json") as resp:
            assert resp.status == 200
            payload = json.loads(resp.read())
        assert payload["errors"] == [{"repo": "broken-repo", "message": "flows --json failed: boom"}]
        assert payload["decisions"] == []
    finally:
        _stop(server, thread)


def test_api_board_json_logs_request(tmp_path):
    log_path = tmp_path / "requests.ndjson"

    def fetch_board_fn(_repo_configs):
        return merge_repos([("empty-repo", normalize_payload("empty-repo", EMPTY_PAYLOAD), None)])

    server, thread = _serve(fetch_board_fn, log_path=str(log_path))
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/board.json"):
            pass
    finally:
        _stop(server, thread)

    lines = log_path.read_text().strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert "ts" in record
    assert record["ua_class"] in ("terminal-tool", "browser")


def test_index_html_is_served_as_static_file():
    def fetch_board_fn(_repo_configs):
        return merge_repos([])

    server, thread = _serve(fetch_board_fn)
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/") as resp:
            assert resp.status == 200
            body = resp.read().decode("utf-8")
        assert "<title>rsb" in body
    finally:
        _stop(server, thread)
