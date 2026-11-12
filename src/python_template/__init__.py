"""A small example package. Rename it with ``make rename NAME=your_package`` and replace the code."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("python-template")
except PackageNotFoundError:  # running from a source tree that was never installed
    __version__ = "0.0.0"
