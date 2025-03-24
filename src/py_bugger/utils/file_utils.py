"""Utilities for working with the target project's files and directories."""

import subprocess
import shlex
from pathlib import Path
import sys


def get_py_files(target_dir):
    """Get all the .py files we can consider modifying when introducing bugs."""
    path = target_dir / ".git"
    using_git = path.exists()

    # if using_git:
    #     cmd = 'git ls-files "*.py"'
    #     cmd_parts = shlex.split(cmd)
    #     py_files = subprocess.run(cmd_parts, capture_output=True).stdout.decode().strip().splitlines()

    #     # Don't modify any test-related files.
    #     py_files = [Path(f) for f in py_files]
    #     py_files = [pf for pf in py_files if "tests/" not in pf.as_posix()]

    #     return py_files

    # Project does not seem to be using Git. Return all .py files not in .venv, and
    # outside of any tests/ dir, build/ dir, or dist/ dir.

    py_files = target_dir.rglob("*.py")
    py_files = [pf for pf in py_files if ".venv/" not in pf.as_posix()]
    py_files = [pf for pf in py_files if "tests/" not in pf.as_posix()]
    py_files = [pf for pf in py_files if "build/" not in pf.as_posix()]
    py_files = [pf for pf in py_files if "dist/" not in pf.as_posix()]
    breakpoint()


    sys.exit()

    return py_files