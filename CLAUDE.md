# xoa-tui

TUI simple pour piloter un XOA / XCP-ng en remote SSH : l'app ouvre une session SSH vers l'hôte et y lance les commandes XOA/xcp-ng (`xe`, `xo-cli`…). Projet personnel.

**Pas d'API XO (REST / JSON-RPC) : tout passe par SSH.** C'est un choix assumé, pas une étape intermédiaire.

## Stack
- Langage : Python 3.13, gestion de projet et de venv avec `uv`
- TUI : `textual` (≥ 8.2 — rester sur la dernière version, ne pas retomber sur les API 0.x)
- SSH : binaire `ssh` du système via `asyncio.create_subprocess_exec` (aucune lib SSH embarquée) — hérite des clés, de l'agent et de `~/.ssh/config` de l'utilisateur
- Exécution : Docker (`docker compose run --rm xoa-tui`) ou en local via `uv run`
- Dépôt distant : GitHub `Tatayoyoh/xoa-tui` (créé par l'utilisateur, ne pas modifier le remote)

## Commandes
- Lancer la TUI : `uv run xoa-tui`
- Lancer via Docker : `docker compose run --rm xoa-tui`
- Tests : `uv run pytest`
- Console de debug Textual : `uv run textual console` dans un terminal, puis `uv run textual run --dev src/xoa_tui/app.py` dans un autre
- Ajouter une dépendance : `uv add <paquet>` (jamais `pip install`)

## Conventions
- Un commit unitaire par tâche, Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`).
- Identité git locale : `tatayoyoh`.
- Aucune action hors de la VM (déploiement, API tierces, ssh vers de vrais hôtes) sans accord explicite de l'utilisateur.
- Aucun secret dans le dépôt ni dans la config : l'authentification SSH repose sur les clés / l'agent de l'utilisateur, jamais sur un mot de passe stocké.
- `BatchMode=yes` sur les appels SSH : une commande ne doit jamais bloquer la TUI sur un prompt de mot de passe.
- Les commandes distantes sont construites en dur dans le code (dictionnaire `COMMANDS`), pas assemblées à partir de saisies utilisateur — éviter toute injection dans la commande SSH.

## Architecture
- `src/xoa_tui/app.py` — `XoaApp`, racine Textual ; au montage, charge la config et route vers l'écran de connexion ou le dashboard.
- `src/xoa_tui/config.py` — `Config` (host, ssh_user, ssh_port) persistée dans `~/.config/xoa-tui/config.toml` en `0600`. Le serveur et le login sont demandés une seule fois puis mémorisés.
- `src/xoa_tui/ssh.py` — `run_remote_command()` : exécution asynchrone d'une commande sur l'hôte distant, renvoie `CommandResult` (returncode, stdout, stderr).
- `src/xoa_tui/screens/connect.py` — saisie serveur / login SSH, sauvegarde la config et rend la main à l'app.
- `src/xoa_tui/screens/dashboard.py` — écran principal : boutons d'actions (`COMMANDS`) et sortie des commandes dans un `RichLog`.
- `src/xoa_tui/app.tcss` — feuille de style Textual.

## Points d'attention
- `push_screen_wait()` ne fonctionne que dans un worker Textual (`@work`) — d'où `XoaApp.start()`.
- Les tests TUI tournent en headless via `app.run_test()` ; la config est isolée en monkeypatchant `config.CONFIG_DIR` / `config.CONFIG_FILE` (constantes de module, lues à l'appel).
- En Docker, `~/.ssh` est monté en lecture seule et `~/.config/xoa-tui` en volume pour que le serveur reste mémorisé entre deux runs ; il faut `stdin_open`/`tty` pour une TUI.
- Aucun hôte XOA/XCP-ng réel n'est joignable depuis la VM : les commandes distantes ne peuvent pas être testées en vrai ici, seulement mockées.
- La VM n'a ni clé SSH ni agent (`~/.ssh` ne contient qu'`authorized_keys`) : `git push` vers GitHub échoue tant qu'une clé n'y est pas installée et déclarée côté GitHub.
