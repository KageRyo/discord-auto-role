## Summary

<!-- What changed and why? Link the issue with `Closes #123` where applicable. -->

## Validation

- [ ] `python -m compileall -q src tests`
- [ ] `PYTHONPATH=src python -m unittest discover -s tests -v`
- [ ] Tested against a Discord test server (if behaviour changed)

## Checklist

- [ ] Branch is based on the latest `main` and named `<type>/<short-description>`.
- [ ] Commits follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
- [ ] No bot tokens, `.env` files or other credentials were committed.
- [ ] `README.md` and `README-zh.md` are aligned when relevant.
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]` for user-facing changes.
