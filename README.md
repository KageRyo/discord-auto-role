# Discord Auto Role

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.7%2B-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

A Python Discord bot that automatically assigns a role to new members when they join your server.

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
└─ pyproject.toml
```

## Requirements

- Python 3.11+
- `Server Members Intent` enabled for the bot in the Discord Developer Portal
- The bot invited to your server with the `bot` and `applications.commands` scopes and the `Manage Roles` permission
- The bot's highest role placed **above** the role it should assign

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

## Notes

- `.env` is listed in `.gitignore` and will not be pushed to GitHub
- If the role cannot be found or assigned, the bot logs a warning instead of crashing
- To add welcome messages, more slash commands or other events, add new modules under `cogs/`
