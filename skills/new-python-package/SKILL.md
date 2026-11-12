---
name: new-python-package
description: Start a new Python package, library or command line tool from jpsanders/python-package-template, with Python 3.15, strict typing, eight checks, CI, releases and a man page wired in. Use when the user asks to create, scaffold or bootstrap a Python package, a pip installable library or a Python CLI, or to add those conventions to a new repository.
---

# Start a new Python package from the template

The template gives a package that is green from its first commit: black, isort, editorconfig-checker, darglint,
flake8, mypy strict, bandit and pytest run with `make checks`, the same as CI. It also carries a man page built from
`docs/MANUAL.md`, a release workflow and an `AGENTS.md`.

## Steps

1. Pick two names with the user: the import name (`acme_widgets`, lowercase with underscores) and, if it should
   differ, the command and distribution name (default: the import name with hyphens, `acme-widgets`).

2. Create the repository from the template. With the GitHub CLI:

   ```sh
   gh repo create acme-widgets --template jpsanders/python-package-template --private --clone
   cd acme-widgets
   ```

   Without it, clone https://github.com/jpsanders/python-package-template and remove its `.git` folder first.

3. Rename everything in one go. This rewrites names in every tracked file, renames paths and the man page, and
   removes the files that only describe the template:

   ```sh
   python3 scripts/rename.py acme_widgets            # or: make rename NAME=acme_widgets
   ```

4. Install and prove it is green, in a virtual environment with Python 3.15 (3.14 also works):

   ```sh
   python3.15 -m venv .venv && . .venv/bin/activate
   make init-dev
   make man
   make checks
   ```

5. Replace the example. `src/<package>/python_pet.py` and its tests are a placeholder; write the real code, then
   rewrite `docs/MANUAL.md` for the real command and run `make man`. Rewrite `README.md` and `CHANGELOG.md`.

6. Commit, push, and let CI run. To release, tag the bare version (`git tag -s 1.0.0 -m 1.0.0`, never `v1.0.0`),
   push the tag and publish a GitHub release for it. The release workflow attaches the wheel and the sdist, and it
   fails unless the README's release badge names the same version.

## Rules to keep

- Run `make checks` before saying any change is done. Fix what it reports rather than silencing it.
- Keep `docs/MANUAL.md` the one source of the command's documentation; never edit the generated files in `data/`.
- Every command takes `--json`. Read `AGENTS.md` in the new repository for the rest.
