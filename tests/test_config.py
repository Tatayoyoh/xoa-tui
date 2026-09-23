from pathlib import Path

import pytest

from xoa_cli import config as config_module
from xoa_cli.config import Config


@pytest.fixture(autouse=True)
def isolated_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    config_file = tmp_path / "config.toml"
    monkeypatch.setattr(config_module, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(config_module, "CONFIG_FILE", config_file)
    return config_file


def test_load_returns_none_without_config() -> None:
    assert Config.load() is None


def test_save_then_load_roundtrip() -> None:
    Config(host="xoa.lan", ssh_user="root", ssh_port=2222).save()

    loaded = Config.load()

    assert loaded == Config(host="xoa.lan", ssh_user="root", ssh_port=2222)


def test_saved_config_is_owner_readable_only(isolated_config: Path) -> None:
    Config(host="xoa.lan", ssh_user="root").save()

    assert isolated_config.stat().st_mode & 0o777 == 0o600
