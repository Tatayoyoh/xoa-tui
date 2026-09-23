from __future__ import annotations

import asyncio
from dataclasses import dataclass

from .config import Config


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


async def run_remote_command(config: Config, command: str) -> CommandResult:
    """Exécute une commande XOA/xcp-ng sur l'hôte distant via le client ssh du système.

    Passe par le binaire `ssh` local (clés/agent/~/.ssh/config de l'utilisateur)
    plutôt que par une lib SSH embarquée ou l'API XO.
    """
    target = f"{config.ssh_user}@{config.host}"
    args = [
        "ssh",
        "-p", str(config.ssh_port),
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=10",
        target,
        command,
    ]
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    return CommandResult(
        returncode=process.returncode or 0,
        stdout=stdout.decode(errors="replace"),
        stderr=stderr.decode(errors="replace"),
    )
