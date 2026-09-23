from __future__ import annotations

from textual import work
from textual.app import App

from .config import Config
from .screens.connect import ConnectScreen
from .screens.dashboard import DashboardScreen


class XoaApp(App):
    """TUI de pilotage XOA/xcp-ng en remote SSH."""

    CSS_PATH = "app.tcss"
    TITLE = "xoa-tui"

    def on_mount(self) -> None:
        self.start()

    @work
    async def start(self) -> None:
        config = Config.load()
        if config is None:
            config = await self.push_screen_wait(ConnectScreen())
        await self.push_screen(DashboardScreen(config))
