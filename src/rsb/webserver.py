"""`rsb serve` HTTP server: static dashboard + `/api/board.json` (proposal §1, §3)."""

import json
import os
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from rsb.render import render_json_model

WEB_DIR = os.path.join(os.path.dirname(__file__), "web")


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _ua_class(user_agent):
    ua = (user_agent or "").lower()
    if "mozilla" in ua or "chrome" in ua or "safari" in ua or "firefox" in ua:
        return "browser"
    return "terminal-tool"


def _log_request(log_path, user_agent):
    if not log_path:
        return
    record = {"ts": _now_iso(), "ua_class": _ua_class(user_agent)}
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass


def make_handler(fetch_board_fn, repo_configs, log_path=None):
    class DashboardHandler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=WEB_DIR, **kwargs)

        def do_GET(self):
            if self.path == "/api/board.json":
                self._serve_board_json()
                return
            super().do_GET()

        def _serve_board_json(self):
            _log_request(log_path, self.headers.get("User-Agent"))
            model = fetch_board_fn(repo_configs)
            body = json.dumps(render_json_model(model, _now_iso())).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            pass

    return DashboardHandler


def run_server(repo_configs, host, port, fetch_board_fn, log_path=None):
    handler = make_handler(fetch_board_fn, repo_configs, log_path=log_path)
    server = ThreadingHTTPServer((host, port), handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
