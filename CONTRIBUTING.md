# Contributing to Discord Auto Role

Thanks for helping improve Discord Auto Role. Bug fixes, documentation
improvements, tests and new features are all welcome.

## Before you start

- Check the open [issues](https://github.com/KageRyo/discord-auto-role/issues)
  and comment before starting a larger change.
- Never commit bot tokens, `.env` files or other credentials. `.env` is ignored
  by default; only `.env.example` with placeholder values belongs in Git.

## Development setup

```bash
git clone https://github.com/KageRyo/discord-auto-role.git
cd discord-auto-role
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
```

Run the same checks used by CI before opening a pull request:

```bash
python -m compileall -q src tests
PYTHONPATH=src python -m unittest discover -s tests -v
```

CI runs these checks on Python 3.11, 3.12 and 3.13.

To try the bot end to end, use a separate test server and test role, and
follow the [Discord setup](README.md#discord-setup) steps in the README.

## Commits

Commit messages follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```text
feat(commands): add /autorole status slash command
fix(auto-role): skip bot accounts when assigning roles
docs: translate README to English
```

Common types are `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci` and
`chore`. Keep each commit focused on one change and make sure the tests pass at
every commit.

## Branches and pull requests

Use a branch named after the change, for example:

```text
feature/<issue-number>-<short-description>
```

Keep each pull request focused on one issue or one reviewable change. Add tests
for behaviour changes, update both `README.md` and `README-zh.md` when
user-facing behaviour changes, add an entry under `[Unreleased]` in
`CHANGELOG.md`, and list the checks you ran in the pull request description.

Pull requests are merged with **rebase** so the Conventional Commits history is
kept on `main`.

## Releases

1. Move the `[Unreleased]` entries in `CHANGELOG.md` to a new version section.
2. Bump `version` in `pyproject.toml` and `__version__` in
   `src/discord_auto_role/__init__.py` with a
   `chore(release): bump version to X.Y.Z` commit.
3. After the pull request is merged, tag the merge result as `vX.Y.Z` and
   publish a GitHub Release titled `AutoRole vX.Y.Z`.

## License

By contributing, you agree that your contribution is licensed under the
[MIT License](LICENSE). Your contribution is credited through Git history and
[CONTRIBUTORS.md](CONTRIBUTORS.md).
