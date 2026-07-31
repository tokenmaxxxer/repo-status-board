"""Config file loading for `rsb` (TOML, `[[repo]]` entries)."""

import os
import sys
from dataclasses import dataclass

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/rsb/boards.toml")


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class RepoConfig:
    name: str
    path: str
    command: list


def resolve_config_path(explicit_path):
    if explicit_path:
        return explicit_path
    env_path = os.environ.get("RSB_CONFIG")
    if env_path:
        return env_path
    return DEFAULT_CONFIG_PATH


def load_config(config_path):
    if not os.path.isfile(config_path):
        raise ConfigError(f"config file not found: {config_path}")
    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"invalid TOML in {config_path}: {e}") from e

    raw_repos = data.get("repo")
    if not raw_repos:
        raise ConfigError(f"no [[repo]] entries found in {config_path}")

    repos = []
    seen_names = set()
    for i, entry in enumerate(raw_repos):
        name = entry.get("name")
        path = entry.get("path")
        if not name:
            raise ConfigError(f"[[repo]] entry #{i + 1} is missing required field 'name'")
        if not path:
            raise ConfigError(f"[[repo]] entry '{name}' is missing required field 'path'")
        if name in seen_names:
            raise ConfigError(f"duplicate repo name in config: {name!r}")
        seen_names.add(name)
        command = entry.get("command") or ["python", "spawn.py"]
        repos.append(RepoConfig(name=name, path=path, command=list(command)))

    return repos
