import pytest

from rsb.config import ConfigError, load_config, resolve_config_path


def test_load_config_parses_multiple_repos(tmp_path):
    config_path = tmp_path / "boards.toml"
    config_path.write_text(
        """
[[repo]]
name = "on-the-record"
path = "/home/jiwon/src/on-the-record"

[[repo]]
name = "repo-status-board"
path = "/home/jiwon/src/repo-status-board"
command = ["python3", "spawn.py"]
"""
    )
    repos = load_config(str(config_path))
    assert [r.name for r in repos] == ["on-the-record", "repo-status-board"]
    assert repos[0].command == ["python", "spawn.py"]
    assert repos[1].command == ["python3", "spawn.py"]


def test_load_config_missing_file(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        load_config(str(tmp_path / "missing.toml"))


def test_load_config_missing_repo_entries(tmp_path):
    config_path = tmp_path / "boards.toml"
    config_path.write_text("")
    with pytest.raises(ConfigError, match="no \\[\\[repo\\]\\] entries"):
        load_config(str(config_path))


def test_load_config_missing_required_field(tmp_path):
    config_path = tmp_path / "boards.toml"
    config_path.write_text('[[repo]]\nname = "x"\n')
    with pytest.raises(ConfigError, match="missing required field 'path'"):
        load_config(str(config_path))


def test_load_config_duplicate_names(tmp_path):
    config_path = tmp_path / "boards.toml"
    config_path.write_text(
        '[[repo]]\nname = "x"\npath = "/a"\n\n[[repo]]\nname = "x"\npath = "/b"\n'
    )
    with pytest.raises(ConfigError, match="duplicate repo name"):
        load_config(str(config_path))


def test_resolve_config_path_precedence(monkeypatch):
    monkeypatch.delenv("RSB_CONFIG", raising=False)
    assert resolve_config_path("/explicit.toml") == "/explicit.toml"

    monkeypatch.setenv("RSB_CONFIG", "/env.toml")
    assert resolve_config_path(None) == "/env.toml"

    monkeypatch.delenv("RSB_CONFIG", raising=False)
    assert resolve_config_path(None).endswith("rsb/boards.toml")
