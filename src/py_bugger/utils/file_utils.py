"""Utilities for working with the target project's files and directories."""

def get_py_files(target_dir):
    """Get all the .py files we can consider modifying when introducing bugs."""
    py_files = target_dir.glob("*.py")
    path = next(py_files)
    return [path]