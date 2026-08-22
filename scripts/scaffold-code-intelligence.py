#!/usr/bin/env python3
"""Portable entrypoint for the code-intelligence capability scaffold."""

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_intelligence_scaffold.cli import main  # noqa: E402


if __name__ == "__main__":
    sys.exit(main())
