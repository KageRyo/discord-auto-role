# Changelog

All notable changes to Discord Auto Role are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.1.4] - 2026-10-06

### Changed

- `CONTRIBUTING.md` documents the GitHub Flow workflow, branch naming and
  required checks.
- `main` is protected: changes require a pull request with passing `Tests`
  and SonarCloud checks, linear history, and no force pushes or deletion.

## [2.1.3] - 2026-10-06

### Security

- CI installs dependencies from a committed, hash-verified `uv.lock` without
  building packages from source, and GitHub Actions are pinned to full commit
  SHAs (SonarCloud `githubactions:S8541`, `githubactions:S8544`,
  `text:S8565`).

### Changed

- Dependabot now updates `uv.lock` instead of pip requirements.
- `CONTRIBUTING.md` documents the uv-based development workflow.

## [2.1.2] - 2026-10-06

### Added

- Discord setup guide, troubleshooting table and Traditional Chinese README
  (`README-zh.md`).
- `CHANGELOG.md`, `CONTRIBUTING.md`, `CONTRIBUTORS.md` and a pull request
  template.
- Weekly Dependabot updates for Python dependencies and GitHub Actions.

## [2.1.1] - 2026-10-06

### Added

- GitHub Actions workflow running the unit tests on Python 3.11, 3.12 and 3.13
  for pushes to `main` and pull requests.
- Release, Tests, Python, License, Conventional Commits and Last commit badges
  in the README.

## [2.1.0] - 2026-10-06

### Added

- `/autorole` slash command, restricted to members with `Manage Roles` by
  default, showing the target role and whether the bot can assign it.
- Permission and role hierarchy checks before assigning a role.

### Changed

- Require `discord.py` 2.7 and request only the `guilds` and `members` gateway
  intents.
- Members in Membership Screening / Onboarding receive the role after they
  complete verification instead of on join.
- App commands are only synced when their names, descriptions or default
  permissions change, and leftover commands are removed when
  `DISCORD_GUILD_ID` is toggled.
- `.env` is loaded by the entry point instead of `load_settings()`.
- README translated to English.
- Package version aligned with the V2.x release tags.

### Fixed

- Bot accounts no longer receive the auto role.
- Role assignment failures are logged instead of raising inside the event
  listener.

## [2.0] - 2026-06-24

### Changed

- Refactored the project into a `src/`-based `discord.py` 2.x package with
  `commands.Bot`, `setup_hook()` and a cog.
- Replaced inline configuration with `.env`-driven settings and validation.
- Moved project metadata and dependencies to `pyproject.toml`.

### Added

- Unit tests for configuration loading and role selection.

## [1.2] - 2022-09-30

### Changed

- Merged `RoleID.py`, `RoleName.py` and `TOKEN.py` into a single `config.py`.

## [1.1] - 2022-09-29

### Added

- Assign the role by role ID.

## [1] - 2022-09-29

- First release of the AutoRole bot.

[Unreleased]: https://github.com/KageRyo/discord-auto-role/compare/v2.1.4...HEAD
[2.1.4]: https://github.com/KageRyo/discord-auto-role/compare/v2.1.3...v2.1.4
[2.1.3]: https://github.com/KageRyo/discord-auto-role/compare/v2.1.2...v2.1.3
[2.1.2]: https://github.com/KageRyo/discord-auto-role/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/KageRyo/discord-auto-role/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/KageRyo/discord-auto-role/compare/V2.0...v2.1.0
[2.0]: https://github.com/KageRyo/discord-auto-role/compare/V1.2...V2.0
[1.2]: https://github.com/KageRyo/discord-auto-role/compare/V1.1...V1.2
[1.1]: https://github.com/KageRyo/discord-auto-role/compare/V1...V1.1
[1]: https://github.com/KageRyo/discord-auto-role/releases/tag/V1
