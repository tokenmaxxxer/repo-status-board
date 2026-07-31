"""`rsb` CLI entrypoint — see docs/issue-1/proposals/cli-design.md for the design."""

import argparse
import json
import sys
import time

from rsb.config import ConfigError, load_config, resolve_config_path
from rsb.fetch import fetch_board
from rsb.render import CLEAR_SCREEN, render_json_model, render_text
from rsb.webserver import run_server

DEFAULT_WATCH_INTERVAL = 30
DEFAULT_SERVE_HOST = "127.0.0.1"
DEFAULT_SERVE_PORT = 8420


def build_arg_parser():
    parser = argparse.ArgumentParser(prog="rsb", description="status board CLI for tokenmaxxxer subjects")
    parser.add_argument("--config", metavar="PATH", help="config file path (default: ~/.config/rsb/boards.toml or $RSB_CONFIG)")
    parser.add_argument("--repo", metavar="NAME", action="append", help="restrict render to this repo (repeatable)")
    watch_group = parser.add_mutually_exclusive_group()
    watch_group.add_argument(
        "--watch",
        nargs="?",
        const=DEFAULT_WATCH_INTERVAL,
        type=int,
        metavar="INTERVAL",
        help=f"re-render every INTERVAL seconds (default {DEFAULT_WATCH_INTERVAL})",
    )
    watch_group.add_argument("--once", action="store_true", help="single render and exit (default behavior)")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI styling")
    parser.add_argument("--json", action="store_true", help="print normalized payload as JSON instead of rendering")

    subparsers = parser.add_subparsers(dest="command")
    serve_parser = subparsers.add_parser("serve", help="serve the web dashboard over HTTP")
    serve_parser.add_argument("--host", default=DEFAULT_SERVE_HOST, help=f"bind host (default {DEFAULT_SERVE_HOST})")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_SERVE_PORT, help=f"bind port (default {DEFAULT_SERVE_PORT})")
    serve_parser.add_argument("--log", metavar="PATH", help="H1 request-log file path (default: no logging)")

    return parser


def _select_repos(repo_configs, names):
    if not names:
        return repo_configs
    by_name = {rc.name: rc for rc in repo_configs}
    unknown = [n for n in names if n not in by_name]
    if unknown:
        raise ConfigError(f"unknown --repo name(s): {', '.join(unknown)}")
    return [by_name[n] for n in names]


def _now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _run_once(repo_configs, as_json):
    model = fetch_board(repo_configs)
    generated_at = _now_iso()
    if as_json:
        print(json.dumps(render_json_model(model, generated_at), indent=2))
    else:
        print(render_text(model, generated_at), end="")
    all_failed = len(repo_configs) > 0 and len(model.errors) == len(repo_configs)
    return 1 if all_failed else 0


def main(argv=None):
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.watch is not None and args.json:
        parser.error("--watch is incompatible with --json")

    try:
        config_path = resolve_config_path(args.config)
        repo_configs = load_config(config_path)
        repo_configs = _select_repos(repo_configs, args.repo)
    except ConfigError as e:
        print(f"rsb: {e}", file=sys.stderr)
        return 2

    if getattr(args, "command", None) == "serve":
        print(f"rsb: serving dashboard on http://{args.host}:{args.port}")
        run_server(repo_configs, args.host, args.port, fetch_board, log_path=args.log)
        return 0

    if args.watch is not None:
        interval = args.watch
        try:
            while True:
                sys.stdout.write(CLEAR_SCREEN)
                _run_once(repo_configs, as_json=False)
                sys.stdout.flush()
                time.sleep(interval)
        except KeyboardInterrupt:
            return 0

    return _run_once(repo_configs, as_json=args.json)


if __name__ == "__main__":
    sys.exit(main())
