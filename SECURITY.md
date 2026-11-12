# Security

## Reporting a vulnerability

Please report security problems privately, through GitHub's
[private vulnerability reporting](https://github.com/jpsanders/python-package-template/security/advisories/new),
not in a public issue. You will get an answer within a week.

## What the template does on your machine

Nothing runs until you run it. `make init-dev` installs the development tools from PyPI into your active environment.
`make rename` rewrites tracked files in the repository it lives in, and nothing outside it. The example command reads
nothing and sends nothing; `python-template man --install` writes one file to your per user man folder.

## What it checks for you

bandit runs on every push and flags shell injection, unsafe deserialisation, weak cryptography and hardcoded
passwords. Dependabot opens monthly updates for the GitHub Actions and the Python tools.
