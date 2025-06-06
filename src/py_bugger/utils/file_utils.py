"""Utilities for working with the target project's files and directories."""

import subprocess
import shlex
from pathlib import Path
import sys


# --- Public functions ---


def get_py_files(target_dir, target_file):
    """Get all the .py files we can consider modifying when introducing bugs."""
    # Check if user requested a single target file.
    if target_file:
        return [target_file]

    # Use .gitignore if possible.
    path_git = target_dir / ".git"
    if path_git.exists():
        return _get_py_files_git(target_dir)
    else:
        return _get_py_files_non_git(target_dir)


def get_paths_lines(py_files, targets):
    """Get all lines from all files matching targets."""
    paths_lines = []
    for path in py_files:
        lines = path.read_text().splitlines()
        for line in lines:
            stripped_line = line.strip()
            if any([stripped_line.startswith(target) for target in targets]):
                paths_lines.append((path, line))

    return paths_lines


# --- Helper functions ---


def _get_py_files_git(target_dir):
    """Get all relevant .py files from a directory manage.py by Git."""
    cmd = 'git ls-files "*.py"'
    cmd_parts = shlex.split(cmd)
    output = subprocess.run(cmd_parts, capture_output=True)
    py_files = output.stdout.decode().strip().splitlines()

    # Convert to path objects. Filter out any test-related files.
    py_files = [Path(f) for f in py_files]
    py_files = [pf for pf in py_files if "tests/" not in pf.as_posix()]
    py_files = [pf for pf in py_files if "Tests/" not in pf.as_posix()]
    py_files = [pf for pf in py_files if "test_code/" not in pf.as_posix()]
    py_files = [pf for pf in py_files if pf.name != "conftest.py"]
    py_files = [pf for pf in py_files if not pf.name.startswith("test_")]

    return py_files


def _get_py_files_non_git(target_dir):
    """Get all relevant .py files from a directory not managed by Git."""
    py_files = target_dir.rglob("*.py")

    exclude_dirs = [
        ".venv/",
        "venv/",
        "tests/",
        "Tests/",
        "test_code/",
        "build/",
        "dist/",
    ]
    py_files = [
        pf
        for pf in py_files
        if not any(ex_dir in pf.as_posix() for ex_dir in exclude_dirs)
    ]
    py_files = [pf for pf in py_files if pf.name != "conftest.py"]
    py_files = [pf for pf in py_files if not pf.name.startswith("test_")]

    return py_files
