import json

from rsb import cli
from rsb.fetch import DEFAULT_TIMEOUT_SECONDS
from rsb.model import merge_repos, normalize_payload

from .fixtures import EMPTY_PAYLOAD, WORKED_EXAMPLE


def test_main_renders_text_and_returns_zero(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "on-the-record"\npath = "/x"\n')

    monkeypatch.setattr(
        cli,
        "fetch_board",
        lambda repo_configs, **kwargs: merge_repos(
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
        lambda repo_configs, **kwargs: merge_repos([("empty-repo", normalize_payload("empty-repo", EMPTY_PAYLOAD), None)]),
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

    monkeypatch.setattr(cli, "fetch_board", lambda repo_configs, **kwargs: merge_repos([("broken", None, "boom")]))

    exit_code = cli.main(["--config", str(config_path)])
    assert exit_code == 1


def test_main_partial_failure_returns_1_without_allow_partial(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text(
        '[[repo]]\nname = "on-the-record"\npath = "/x"\n\n[[repo]]\nname = "broken"\npath = "/y"\n'
    )

    monkeypatch.setattr(
        cli,
        "fetch_board",
        lambda repo_configs, **kwargs: merge_repos(
            [
                ("on-the-record", normalize_payload("on-the-record", WORKED_EXAMPLE), None),
                ("broken", None, "boom"),
            ]
        ),
    )

    exit_code = cli.main(["--config", str(config_path), "--json"])
    assert exit_code == 1


def test_main_partial_failure_with_allow_partial_returns_0(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text(
        '[[repo]]\nname = "on-the-record"\npath = "/x"\n\n[[repo]]\nname = "broken"\npath = "/y"\n'
    )

    monkeypatch.setattr(
        cli,
        "fetch_board",
        lambda repo_configs, **kwargs: merge_repos(
            [
                ("on-the-record", normalize_payload("on-the-record", WORKED_EXAMPLE), None),
                ("broken", None, "boom"),
            ]
        ),
    )

    exit_code = cli.main(["--config", str(config_path), "--json", "--allow-partial"])
    assert exit_code == 0


def test_main_default_timeout_reaches_fetch_board(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "on-the-record"\npath = "/x"\n')

    captured_kwargs = {}

    def fake_fetch_board(repo_configs, **kwargs):
        captured_kwargs.update(kwargs)
        return merge_repos(
            [("on-the-record", normalize_payload("on-the-record", WORKED_EXAMPLE), None)]
        )

    monkeypatch.setattr(cli, "fetch_board", fake_fetch_board)

    exit_code = cli.main(["--config", str(config_path)])
    assert exit_code == 0
    assert captured_kwargs["timeout"] == DEFAULT_TIMEOUT_SECONDS


def test_main_explicit_timeout_reaches_fetch_board(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "on-the-record"\npath = "/x"\n')

    captured_kwargs = {}

    def fake_fetch_board(repo_configs, **kwargs):
        captured_kwargs.update(kwargs)
        return merge_repos(
            [("on-the-record", normalize_payload("on-the-record", WORKED_EXAMPLE), None)]
        )

    monkeypatch.setattr(cli, "fetch_board", fake_fetch_board)

    exit_code = cli.main(["--config", str(config_path), "--timeout", "42"])
    assert exit_code == 0
    assert captured_kwargs["timeout"] == 42
