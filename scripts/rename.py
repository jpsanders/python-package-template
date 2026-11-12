"""
Rename the template's package in place.

Run once, right after creating a repository from the template::

    python scripts/rename.py acme_widgets

It replaces the import name ``python_template`` and the distribution, command and image name ``python-template`` in
every tracked text file, renames every tracked path that carries either name, and removes the files that only describe
the template itself (its agent plugin, its skill, its llms.txt and its banner images). Nothing else is touched.
"""

import argparse
import re
import shutil
import subprocess  # nosec B404: runs git with fixed arguments only
import sys
from pathlib import Path

OLD_IMPORT = "python_template"
OLD_DIST = "python-template"
ROOT = Path(__file__).resolve().parent.parent
# These describe the template repository, not the package made from it.
TEMPLATE_ONLY = [".claude-plugin", "skills/new-python-package", "llms.txt", "docs/images"]


def tracked_files() -> list[Path]:
    """
    List the files git tracks, so build output and virtual envs are skipped.

    :returns: Absolute paths of tracked files
    """
    out = subprocess.run(  # nosec B603 B607: fixed git command, no shell
        ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    return [ROOT / p for p in out.decode().split("\0") if p]


def rename(import_name: str, dist_name: str) -> list[str]:
    """
    Replace the template names in file contents and paths, and drop the template only files.

    :param import_name: New import name, such as ``acme_widgets``
    :param dist_name: New distribution and command name, such as ``acme-widgets``
    :returns: What changed, relative to the repository root
    :raises SystemExit: When the template was already renamed
    """
    if not (ROOT / "src" / OLD_IMPORT).is_dir():
        raise SystemExit(f"src/{OLD_IMPORT} not found: this repository was already renamed")
    changed = []
    for item in TEMPLATE_ONLY:
        gone = ROOT / item
        if gone.is_dir():
            shutil.rmtree(gone)
        elif gone.exists():
            gone.unlink()
        else:
            continue
        changed.append(f"removed {item}")
    me = Path(__file__).resolve()
    for path in tracked_files():
        if path.resolve() == me or not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = text.replace(OLD_IMPORT, import_name).replace(OLD_DIST, dist_name)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    # Paths: deepest first, so a renamed folder never strands a file inside it.
    rels: set[Path] = set()
    for path in tracked_files():
        if path.exists():
            rel = path.relative_to(ROOT)
            rels.add(rel)
            rels.update(p for p in rel.parents if p != Path("."))
    for rel in sorted(rels, key=lambda p: -len(p.parts)):
        name = rel.name
        if OLD_IMPORT not in name and OLD_DIST not in name:
            continue
        source = ROOT / rel
        if not source.exists():
            continue
        target = source.with_name(name.replace(OLD_IMPORT, import_name).replace(OLD_DIST, dist_name))
        source.rename(target)
        changed.append(f"{rel} -> {target.relative_to(ROOT)}")
    return changed


def main() -> None:
    """Parse the arguments and rename."""
    parser = argparse.ArgumentParser(description="Rename the template package.")
    parser.add_argument("import_name", help="new import name, lowercase with underscores")
    parser.add_argument("--dist", help="distribution and command name (default: import name with hyphens)")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.import_name):
        sys.exit("import name must be lowercase letters, digits and underscores, starting with a letter")
    dist_name = args.dist or args.import_name.replace("_", "-")
    for line in rename(args.import_name, dist_name):
        print(line)
    print("Next: make man, then write your own docs/MANUAL.md, README.md and CHANGELOG.md.")


if __name__ == "__main__":
    main()
