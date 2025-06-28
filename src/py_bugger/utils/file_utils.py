"""Utilities for working with the target project's files and directories."""

import subprocess
import shlex
from pathlib import Path
import sys

from py_bugger.utils.modification import modifications


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
    """Get all lines from all files matching targets, if they haven't already
    been modified.
    """
    paths_lines = []
    for path in py_files:
        lines = path.read_text().splitlines()
        _remove_modified_lines(path, lines)

        for line in lines:
            stripped_line = line.strip()
            if any([stripped_line.startswith(target) for target in targets]):
                paths_lines.append((path, line))

    return paths_lines


def check_unmodified(candidate_path, candidate_node=None, candidate_line=None):
    """Check if it's safe to modify a node or line.

    If the node or line has not already been modified, return True. Otherwise,
    return False.
    """
    # Only look at modifications in the candidate path.
    relevant_modifications = [m for m in modifications if m.path == candidate_path]

    if not relevant_modifications:
        return True

    modified_nodes = [m.modified_node for m in relevant_modifications]
    modified_lines = [m.modified_line for m in relevant_modifications]

    # Need to use deep_equals for node comparisons.
    for modified_node in modified_nodes:
        if modified_node.deep_equals(candidate_node):
            return False

    if candidate_line in modified_lines:
        return False

    # The candidate node or line has not been modified during this run of py-bugger.
    return True


# --- Helper functions ---


def _get_py_files_git(target_dir):
    """Get all relevant .py files from a directory managed by Git."""
    cmd = f'git -C {target_dir.as_posix()} ls-files "*.py"'
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

    # Build full paths.
    py_files = [target_dir / pf for pf in py_files]

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


def _remove_modified_lines(path, lines):
    """Remove lines from the list that have already been modified."""
    for modification in modifications:
        if modification.path != path:
            continue
        if not modification.modified_line:
            continue

        # This path has been modified. Check line.
        modified_line = modification.modified_line.rstrip()
        if modified_line in lines:
            # DEV: We may want to look at line numbers. For now, remove all occurrences
            # of this line.
            while modified_line in lines:
                lines.remove(modified_line)
