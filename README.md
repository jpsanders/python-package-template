# Python Package Template

This repository is an example and can be used as a repository template.

## Setup

### Requirements

* `python3.12`
* A corresponding virtual environment created and activated using your favourite venv tool (`virtualenv`, `pyenv`,
  `pipenv`, `direnv` etc).

### Install

For a non-development version, install the required dependencies only with the following command:

```bash
make init
```

## Development

For an editable development version (will install required and development dependencies). Inside your virtual env run
the following command:

```bash
make init-dev
```

### Tests, linting and formatting checks

```bash
make checks
```

**Note:** *That `make checks` will only **report** formatting changes.*
To auto format (`ruff`) run:

```bash
make format
```

### Docker

```bash
make build-docker
```

### Per-user dotfiles vs repository `.gitignore`

The `.gitignore` in this repository mostly contains just artifacts that would be produced by the code in the repository.
As a developer, there may be other files you need to ignore (e.g. `.envrc`, `.python-version`, etc) - since those should
be ignored *in general*, it is recommended to add them to your global user ignore file, at `~/.gitignore` rather than
adding to the repository `.gitignore`.
