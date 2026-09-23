from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label

from ..config import Config


class ConnectScreen(Screen[Config]):
    """Demande le serveur et le login SSH, puis les mémorise sur le système."""

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="connect-form"):
            yield Label("Connexion à l'hôte XCP-ng / XOA")
            yield Input(placeholder="Serveur (hôte ou IP)", id="host")
            yield Input(placeholder="Utilisateur SSH", id="ssh_user")
            yield Input(placeholder="Port SSH (défaut : 22)", id="ssh_port")
            yield Button("Se connecter", id="connect", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#connect-form", Vertical).border_title = "xoa-tui"
        self.query_one("#host", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "connect":
            return
        host = self.query_one("#host", Input).value.strip()
        ssh_user = self.query_one("#ssh_user", Input).value.strip()
        port_raw = self.query_one("#ssh_port", Input).value.strip()
        if not host or not ssh_user:
            self.notify("Serveur et utilisateur SSH obligatoires", severity="error")
            return
        config = Config(
            host=host,
            ssh_user=ssh_user,
            ssh_port=int(port_raw) if port_raw.isdigit() else 22,
        )
        config.save()
        self.dismiss(config)
