from __future__ import annotations

from textual import work
from textual.app import App
from textual.theme import Theme

from .config import Config
from .screens.connect import ConnectScreen
from .screens.dashboard import DashboardScreen

MINIMAL_THEME = Theme(
    name="xoa-minimal",
    primary="#c4a7e7",
    secondary="#6e6a86",
    accent="#c4a7e7",
    warning="#f6c177",
    error="#eb6f92",
    success="#9ccfd8",
    background="#131217",
    surface="#131217",
    panel="#1a1922",
    dark=True,
)


class XoaApp(App):
    """TUI de pilotage XOA/xcp-ng en remote SSH."""

    CSS_PATH = "app.tcss"
    TITLE = "xoa-tui"

    def on_mount(self) -> None:
        self.register_theme(MINIMAL_THEME)
        self.theme = "xoa-minimal"
        self.start()

    @work
    async def start(self) -> None:
        config = Config.load()
        if config is None:
            config = await self.push_screen_wait(ConnectScreen())
        await self.push_screen(DashboardScreen(config))
