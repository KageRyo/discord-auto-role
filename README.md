# Discord Auto Role

[![Release](https://img.shields.io/github/v/release/KageRyo/discord-auto-role)](https://github.com/KageRyo/discord-auto-role/releases/latest)
[![Tests](https://github.com/KageRyo/discord-auto-role/actions/workflows/tests.yml/badge.svg)](https://github.com/KageRyo/discord-auto-role/actions/workflows/tests.yml)
![Python](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FKageRyo%2Fdiscord-auto-role%2Fmain%2Fpyproject.toml&logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.7%2B-5865F2?logo=discord&logoColor=white)
[![License](https://img.shields.io/github/license/KageRyo/discord-auto-role)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-FE5196?logo=conventionalcommits&logoColor=white)](https://www.conventionalcommits.org/en/v1.0.0/)
[![Last commit](https://img.shields.io/github/last-commit/KageRyo/discord-auto-role)](https://github.com/KageRyo/discord-auto-role/commits/main)

**A Python Discord bot that automatically assigns a role to new members when they join your server.**

[正體中文](README-zh.md)

## Features

- Manages the bot token and role settings through `.env`
- Selects the target role by role `ID` or role `name`
- Optionally restricts auto-role to a single guild/server
- Skips bot accounts, so other bots joining the server are left untouched
- Respects Membership Screening / Onboarding: pending members get the role once they complete verification
- Checks the bot's `Manage Roles` permission and role hierarchy before assigning, and logs a clear warning instead of failing
- `/autorole` slash command (admins with `Manage Roles` only) to check the configuration and whether the role can be assigned
- Requests only the gateway intents it needs (`guilds` + `members`)
- Modern structure built on `commands.Bot`, `setup_hook()`, cogs and app commands

## Project Structure

```text
.
├─ src/discord_auto_role/
│  ├─ __main__.py
│  ├─ bot.py
│  ├─ command_sync.py
│  ├─ config.py
│  ├─ logging_config.py
│  ├─ role_selector.py
│  └─ cogs/auto_role.py
├─ tests/
├─ .env.example
├─ pyproject.toml
└─ uv.lock
```

## Requirements

- Python 3.11+
- A Discord application with a bot user
- The bot's highest role placed **above** the role it should assign

## Discord Setup

1. Open the [Discord Developer Portal](https://discord.com/developers/applications), create an application and copy the bot token from the **Bot** page.
2. On the same page, enable **Server Members Intent** under *Privileged Gateway Intents*. Without it the bot never receives join events.
3. Invite the bot with the `bot` and `applications.commands` scopes and the `Manage Roles` permission. Replace `YOUR_APPLICATION_ID` with the ID from the **General Information** page:

   ```text
   https://discord.com/oauth2/authorize?client_id=YOUR_APPLICATION_ID&scope=bot+applications.commands&permissions=268435456
   ```

4. In **Server Settings → Roles**, drag the bot's role above the role it should assign. Discord does not let a bot assign a role at or above its own highest role.
5. Enable **Developer Mode** in Discord (*User Settings → Advanced*) so you can right-click the server and the role to copy their IDs for `.env`.

After the bot starts, run `/autorole` in your server to confirm it reports **Ready to assign**.

## Quick Start

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env`:

   ```dotenv
   DISCORD_BOT_TOKEN=your-bot-token
   DISCORD_GUILD_ID=123456789012345678
   DISCORD_ROLE_ID=987654321098765432
   DISCORD_ROLE_NAME=
   ```

4. Start the bot:

   ```bash
   python -m discord_auto_role
   ```

## Environment Variables

| Name | Required | Description |
| --- | --- | --- |
| `DISCORD_BOT_TOKEN` | Yes | Discord bot token |
| `DISCORD_GUILD_ID` | No | Only auto-assign roles in this guild; slash commands are also synced to it instantly |
| `DISCORD_ROLE_ID` | Recommended | ID of the role to assign |
| `DISCORD_ROLE_NAME` | Optional fallback | Name of the role to assign |

Prefer `DISCORD_ROLE_ID`, since role names can be duplicated or renamed later.

## Slash Commands

| Command | Who can use it | Description |
| --- | --- | --- |
| `/autorole` | Members with `Manage Roles` | Shows the target role and whether the bot is able to assign it (ephemeral reply) |

When `DISCORD_GUILD_ID` is set, commands are registered to that guild and appear immediately. Without it, commands are registered globally, which can take a while to show up.

On startup the bot compares its commands with what Discord already has and only syncs when names, descriptions or default permissions differ, so routine restarts do not hit the command rate limits. Switching `DISCORD_GUILD_ID` on or off also removes the leftover commands from the previous mode, so commands are never listed twice.

## Development

Run the unit tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Syntax check:

```bash
python -m compileall src tests
```

GitHub Actions runs both checks on Python 3.11, 3.12 and 3.13 for every push to `main` and every pull request, using the hash-verified versions pinned in `uv.lock`. See [CONTRIBUTING.md](CONTRIBUTING.md) for the uv-based workflow.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| New members never get the role | Enable **Server Members Intent** in the Developer Portal and restart the bot |
| Log says `the bot is missing the Manage Roles permission` | Grant `Manage Roles` to the bot's role, or re-invite it with the URL above |
| Log says the role `is not below the bot's highest role` | Move the bot's role above the target role in **Server Settings → Roles** |
| Log says `Role not found` | Check `DISCORD_ROLE_ID` / `DISCORD_ROLE_NAME` and `DISCORD_GUILD_ID` in `.env` |
| `/autorole` does not appear | Re-invite the bot with the `applications.commands` scope; global commands can take a while to appear without `DISCORD_GUILD_ID` |
| Members with screening enabled get the role late | Expected: the role is assigned once they complete Membership Screening / Onboarding |

## Notes

- `.env` is listed in `.gitignore` and will not be pushed to GitHub. Never commit bot tokens.
- If the role cannot be found or assigned, the bot logs a warning instead of crashing
- To add welcome messages, more slash commands or other events, add new modules under `cogs/`

## Release History

See [CHANGELOG.md](CHANGELOG.md) for every release and the [GitHub Releases](https://github.com/KageRyo/discord-auto-role/releases) page for release notes.

## Contributing

Bug reports, documentation improvements and pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Thanks to everyone listed in [CONTRIBUTORS.md](CONTRIBUTORS.md).

## License

Discord Auto Role is released under the [MIT License](LICENSE).

Copyright © 2022–2026 **Chien-Hsun Chang** and [contributors](CONTRIBUTORS.md).
