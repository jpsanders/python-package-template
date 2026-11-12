# Changelog

Versions follow [semantic versioning](https://semver.org). Tags carry the bare version, such as `1.0.0`.

## 1.0.0 (2026-11-12)

The first release.

- Python 3.15 first: packages require 3.14 or later, CI tests 3.14 and 3.15 on Linux and macOS, and the Docker image
  is `python:3.15-slim`.
- Eight checks wired in from the first commit: black, isort, editorconfig-checker, darglint, flake8 with pydocstyle
  and tidy imports, mypy in strict mode, bandit and pytest with coverage. `make checks` runs exactly what CI runs.
- A man page from the first commit: `docs/MANUAL.md` is the one source for `<command> guide`, `<command> man` and
  `man <command>`, and a ninth check fails when they drift apart.
- An example command that shows the conventions: `--json` on every command, `guide` for people and agents, exit
  codes that mean something.
- Releases: publishing a GitHub release builds the wheel and the sdist and attaches them.
- `make rename` renames the package, its command, its paths and its man page in one go, and drops the files that only
  describe the template. CI proves a renamed copy starts green.
- Agent ready: an `AGENTS.md` for coding agents, and a Claude Code plugin with a skill that starts a new package
  from the template.
- Fixed: installing straight from git failed because `setup.cfg` sent egg metadata to a folder that does not exist
  in a fresh clone.
