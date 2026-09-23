from pathlib import Path

import pytest

from xoa_cli import config as config_module
from xoa_cli.app import XoaApp
from xoa_cli.config import Config
from xoa_cli.screens.connect import ConnectScreen
from xoa_cli.screens.dashboard import DashboardScreen


@pytest.fixture(autouse=True)
def isolated_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    config_file = tmp_path / "config.toml"
    monkeypatch.setattr(config_module, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(config_module, "CONFIG_FILE", config_file)
    return config_file


@pytest.mark.asyncio
async def test_asks_for_server_when_not_configured() -> None:
    async with XoaApp().run_test() as pilot:
        assert isinstance(pilot.app.screen, ConnectScreen)


@pytest.mark.asyncio
async def test_goes_straight_to_dashboard_when_configured() -> None:
    Config(host="xoa.lan", ssh_user="root").save()

    async with XoaApp().run_test() as pilot:
        assert isinstance(pilot.app.screen, DashboardScreen)


@pytest.mark.asyncio
async def test_connect_screen_saves_server_and_opens_dashboard(
    isolated_config: Path,
) -> None:
    async with XoaApp().run_test() as pilot:
        await pilot.click("#host")
        await pilot.press(*"xoa.lan")
        await pilot.click("#ssh_user")
        await pilot.press(*"root")
        await pilot.click("#connect")
        await pilot.pause()

        assert isinstance(pilot.app.screen, DashboardScreen)

    assert Config.load() == Config(host="xoa.lan", ssh_user="root", ssh_port=22)
