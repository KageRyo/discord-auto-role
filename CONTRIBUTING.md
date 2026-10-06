# Contributing to Discord Auto Role

Thanks for helping improve Discord Auto Role. Bug fixes, documentation
improvements, tests and new features are all welcome.

## Before you start

- Check the open [issues](https://github.com/KageRyo/discord-auto-role/issues)
  and comment before starting a larger change.
- Never commit bot tokens, `.env` files or other credentials. `.env` is ignored
  by default; only `.env.example` with placeholder values belongs in Git.

## Development setup

The project uses [uv](https://docs.astral.sh/uv/) with a committed `uv.lock`, so
everyone installs the same hash-verified dependency versions:

```bash
git clone https://github.com/KageRyo/discord-auto-role.git
cd discord-auto-role
uv sync --locked
cp .env.example .env
```

Run the same checks used by CI before opening a pull request:

```bash
uv run python -m compileall -q src tests
PYTHONPATH=src uv run python -m unittest discover -s tests -v
```

CI runs these checks on Python 3.11, 3.12 and 3.13. It installs only the locked
dependency wheels (`uv sync --locked --no-build --no-install-project`) and never
builds packages from source.

When you change dependencies in `pyproject.toml`, run `uv lock` and commit the
updated `uv.lock` in the same pull request. Dependabot proposes weekly
`uv.lock` and GitHub Actions updates; Actions are pinned to full commit SHAs
with a version comment, so update both together.

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

## Workflow: GitHub Flow

The project follows [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).
`main` is the only long-lived branch and must always be releasable.

1. **Branch from `main`.** Create a short-lived branch for one change:

   ```text
   <type>/<short-description>
   <type>/<issue-number>-<short-description>
   ```

   `<type>` is the Conventional Commits type of the main change, for example
   `feat/welcome-message`, `fix/12-pending-members` or `docs/github-flow`.

2. **Commit** small, focused Conventional Commits. Tests must pass at every
   commit.
3. **Open a pull request** against `main` early, and fill in the pull request
   template. Keep each pull request focused on one issue or one reviewable
   change. Add tests for behaviour changes, update both `README.md` and
   `README-zh.md` when user-facing behaviour changes, add an entry under
   `[Unreleased]` in `CHANGELOG.md`, and list the checks you ran.
4. **Pass the checks.** The `Tests` workflow (Python 3.11, 3.12 and 3.13) and
   SonarCloud Code Analysis must pass before merging.
5. **Merge with rebase** so the Conventional Commits history is kept on `main`,
   then delete the branch.
6. **Release from `main`** when the merged changes should ship (see below).

### Protected `main`

`main` accepts changes only through a pull request that passes the four
required checks: `test (3.11)`, `test (3.12)`, `test (3.13)` and
`SonarCloud Code Analysis`. The branch must be up to date with `main` before
merging, and history must stay linear, which is why pull requests are merged
with rebase. Direct pushes, force pushes and deleting `main` are blocked.
No approving review is required, but administrators are not exempt from these
rules.

## Releases

Releases are cut from `main` and follow [Semantic Versioning](https://semver.org/).
The version bump is the last commit of the pull request that ships the release:

1. Move the `[Unreleased]` entries in `CHANGELOG.md` to a new version section.
2. Bump `version` in `pyproject.toml` and `__version__` in
   `src/discord_auto_role/__init__.py`, run `uv lock` (the lock file records the
   project version), and commit all of it as
   `chore(release): bump version to X.Y.Z`.
3. After the pull request is merged, tag the resulting `main` commit as
   `vX.Y.Z` and publish a GitHub Release titled `AutoRole vX.Y.Z`.

Changes that do not need to ship on their own, such as documentation-only
updates, can stay under `[Unreleased]` until the next release.

## License

By contributing, you agree that your contribution is licensed under the
[MIT License](LICENSE). Your contribution is credited through Git history and
[CONTRIBUTORS.md](CONTRIBUTORS.md).
