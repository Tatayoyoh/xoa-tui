# xoa-tui

TUI simple pour piloter un XOA / XCP-ng en remote SSH, sans passer par l'API Xen Orchestra.

Au premier lancement, l'application demande le serveur et le login SSH, puis les mémorise
dans `~/.config/xoa-tui/config.toml`. L'authentification repose sur les clés SSH / l'agent
de l'utilisateur.

```sh
uv run xoa-tui              # en local
docker compose run --rm xoa-tui   # via Docker
```
