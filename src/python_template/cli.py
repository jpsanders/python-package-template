"""
The command line: ``python-template``.

Every command takes ``--json``, so scripts and AI agents read the same facts people do. ``guide`` prints the full
manual and ``man`` shows, or installs, the man page built from it.
"""

import argparse
import json
import os
import shutil
import subprocess  # nosec B404: runs man with fixed arguments only
import sys
from collections.abc import Callable, Sequence
from importlib import resources
from pathlib import Path

from python_template import __version__
from python_template.python_pet import PythonPet

PROG = "python-template"


def _data(name: str) -> str:
    """
    Read a file shipped in the package's data folder.

    :param name: File name inside ``data``
    :returns: Its text
    """
    return (resources.files("python_template") / "data" / name).read_text(encoding="utf-8")


def _emit(pet: PythonPet, as_json: bool) -> int:
    """
    Print the pet for people or as JSON.

    :param pet: The pet to show
    :param as_json: Print JSON instead of a sentence
    :returns: Exit code
    """
    print(json.dumps(pet.as_dict()) if as_json else pet.get_status())
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """
    Show the pet as it starts.

    :param args: Parsed arguments
    :returns: Exit code
    """
    return _emit(PythonPet(args.name), args.json)


def cmd_feed(args: argparse.Namespace) -> int:
    """
    Feed the pet the given number of times, then show it.

    :param args: Parsed arguments
    :returns: Exit code
    """
    pet = PythonPet(args.name)
    for _ in range(args.times):
        pet.feed()
    return _emit(pet, args.json)


def cmd_play(args: argparse.Namespace) -> int:
    """
    Play with the pet the given number of times, then show it.

    :param args: Parsed arguments
    :returns: Exit code
    """
    pet = PythonPet(args.name)
    for _ in range(args.times):
        pet.play()
    return _emit(pet, args.json)


def cmd_guide(args: argparse.Namespace) -> int:
    """
    Print the full manual as Markdown, written for people and agents alike.

    :param args: Parsed arguments
    :returns: Exit code
    """
    print(_data("MANUAL.md"), end="")
    return 0


def man_folder() -> Path:
    """
    Find the per user man folder that ``man`` searches without any setup.

    :returns: ``$XDG_DATA_HOME/man/man1``, or ``~/.local/share/man/man1``
    """
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "man" / "man1"


def cmd_man(args: argparse.Namespace) -> int:
    """
    Show the man page, print it as roff, or install it so ``man python-template`` works.

    :param args: Parsed arguments
    :returns: Exit code
    """
    page = _data(f"{PROG}.1")
    if args.install:
        target = man_folder() / f"{PROG}.1"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        print(f"installed {target}; open it with: man {PROG}")
        return 0
    man = shutil.which("man")
    if man and sys.stdout.isatty() and not args.raw:
        with resources.as_file(resources.files("python_template") / "data" / f"{PROG}.1") as path:
            return subprocess.call([man, "-l", str(path)])  # nosec B603: man, fixed arguments
    print(page, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """
    Build the argument parser with every command.

    :returns: The parser
    """
    parser = argparse.ArgumentParser(prog=PROG, description="An example command: a pet you can feed and play with.")
    parser.add_argument("--version", action="version", version=f"{PROG} {__version__}")
    sub = parser.add_subparsers(dest="command", metavar="command")

    def add(
        name: str, func: Callable[[argparse.Namespace], int], about: str, pet: bool = True
    ) -> argparse.ArgumentParser:
        p = sub.add_parser(name, help=about, description=about)
        if pet:
            p.add_argument("--name", default="Baby Python", help="the pet's name (default: Baby Python)")
            p.add_argument("--json", action="store_true", help="print JSON")
        p.set_defaults(func=func)
        return p

    add("status", cmd_status, "show the pet")
    for name, func, verb in (("feed", cmd_feed, "feed"), ("play", cmd_play, "play with")):
        p = add(name, func, f"{verb} the pet, then show it")
        p.add_argument("--times", type=int, default=1, choices=range(1, 11), metavar="N", help="1 to 10 (default 1)")
    add("guide", cmd_guide, "print the full manual, for people and agents", pet=False)
    man = add("man", cmd_man, "show the man page", pet=False)
    man.add_argument("--install", action="store_true", help=f"install it so `man {PROG}` works")
    man.add_argument("--raw", action="store_true", help="print the roff source")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """
    Run the command line.

    :param argv: Arguments, without the program name; ``sys.argv`` when omitted
    :returns: Exit code
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        args = parser.parse_args(["status", *(argv or [])])
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
