"""Codies Memory Lite v2 — file-based two-tier memory for AI agents."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("codies-memory")
except PackageNotFoundError:  # imported from a source checkout without installation
    __version__ = "0+unknown"
