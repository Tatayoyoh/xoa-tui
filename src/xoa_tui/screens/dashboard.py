from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, RichLog

from ..config import Config
from ..ssh import run_remote_command

COMMANDS = {
    "vm-list": ("VMs", "xe vm-list params=name-label,power-state"),
    "host-list": ("Hôtes", "xe host-list params=name-label,enabled"),
    "sr-list": ("Stockages", "xe sr-list params=name-label,type,physical-utilisation"),
}


class DashboardScreen(Screen):
    """Écran principal : lance les commandes XOA/xcp-ng sur l'hôte distant."""

    BINDINGS = [("q", "app.quit", "Quitter")]

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal(id="actions"):
                for action_id, (label, _) in COMMANDS.items():
                    yield Button(label, id=action_id)
            yield RichLog(id="output", wrap=True, highlight=True, markup=False)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"xoa-tui — {self.config.ssh_user}@{self.config.host}"

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        entry = COMMANDS.get(event.button.id or "")
        if entry is None:
            return
        _, command = entry
        log = self.query_one("#output", RichLog)
        log.write(f"$ {command}")
        result = await run_remote_command(self.config, command)
        if result.stdout:
            log.write(result.stdout)
        if result.stderr:
            log.write(f"[stderr] {result.stderr}")
