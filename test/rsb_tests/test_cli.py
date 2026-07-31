import json

from rsb import cli
from rsb.model import merge_repos, normalize_payload

from .fixtures import EMPTY_PAYLOAD, WORKED_EXAMPLE


def test_main_renders_text_and_returns_zero(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "on-the-record"\npath = "/x"\n')

    monkeypatch.setattr(
        cli,
        "fetch_board",
        lambda repo_configs: merge_repos(
            [("on-the-record", normalize_payload("on-the-record", WORKED_EXAMPLE), None)]
        ),
    )

    exit_code = cli.main(["--config", str(config_path)])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "DECISION QUEUE" in captured.out


def test_main_json_flag_prints_json(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "empty-repo"\npath = "/x"\n')

    monkeypatch.setattr(
        cli,
        "fetch_board",
        lambda repo_configs: merge_repos([("empty-repo", normalize_payload("empty-repo", EMPTY_PAYLOAD), None)]),
    )

    exit_code = cli.main(["--config", str(config_path), "--json"])
    captured = capsys.readouterr()
    assert exit_code == 0
    parsed = json.loads(captured.out)
    assert parsed["decisions"] == []


def test_main_watch_and_json_are_incompatible(tmp_path, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "x"\npath = "/x"\n')
    try:
        cli.main(["--config", str(config_path), "--watch", "--json"])
        assert False, "expected SystemExit"
    except SystemExit as e:
        assert e.code == 2


def test_main_missing_config_returns_2(tmp_path, capsys):
    exit_code = cli.main(["--config", str(tmp_path / "missing.toml")])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "not found" in captured.err


def test_main_unknown_repo_filter_returns_2(tmp_path, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "on-the-record"\npath = "/x"\n')
    exit_code = cli.main(["--config", str(config_path), "--repo", "nonexistent"])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "unknown --repo" in captured.err


def test_main_all_repos_failed_returns_1(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "broken"\npath = "/x"\n')

    monkeypatch.setattr(cli, "fetch_board", lambda repo_configs: merge_repos([("broken", None, "boom")]))

    exit_code = cli.main(["--config", str(config_path)])
    assert exit_code == 1
