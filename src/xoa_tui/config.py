from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "xoa-tui"
CONFIG_FILE = CONFIG_DIR / "config.toml"


@dataclass
class Config:
    host: str
    ssh_user: str
    ssh_port: int = 22

    @classmethod
    def load(cls) -> "Config | None":
        if not CONFIG_FILE.exists():
            return None
        with CONFIG_FILE.open("rb") as f:
            data = tomllib.load(f)
        return cls(
            host=data["host"],
            ssh_user=data["ssh_user"],
            ssh_port=data.get("ssh_port", 22),
        )

    def save(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        content = (
            f'host = "{self.host}"\n'
            f'ssh_user = "{self.ssh_user}"\n'
            f"ssh_port = {self.ssh_port}\n"
        )
        CONFIG_FILE.write_text(content)
        CONFIG_FILE.chmod(0o600)
