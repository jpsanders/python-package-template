# Contributing

Issues and pull requests are welcome.

## Set up

```sh
git clone https://github.com/jpsanders/python-package-template && cd python-package-template
python3.15 -m venv .venv && . .venv/bin/activate
make init-dev
```

## Before a pull request

```sh
make format      # black and isort
make checks      # every check CI runs, in the same order
```

`make checks` runs isort, black, editorconfig-checker, darglint, flake8, mypy in strict mode, bandit, the man page
check and pytest with coverage. CI runs the same on Linux and macOS with Python 3.14 and 3.15, then renames the
package to `acme_widgets` and runs everything again, so a change that breaks a new repository fails here first.

## Changing things

- **The manual** is `docs/MANUAL.md`. `make man` rebuilds the packaged copy and the man page from it, and
  `make checks` fails while either is stale.
- **A file that only describes the template** (its plugin, its skill, its banners) belongs in `TEMPLATE_ONLY` in
  `scripts/rename.py`, so a new repository does not inherit it.
- **Commits** are signed. Tags carry the bare version, `1.2.0`, never `v1.2.0`.
