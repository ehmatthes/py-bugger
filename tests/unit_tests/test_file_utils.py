"""Tests for utils/file_utils.py."""

from pathlib import Path

import pytest

from py_bugger.utils import file_utils


def test_get_py_files_git():
    # This takes more setup. Need to actually initialize a Git dir. Could point it
    # at this project directory and just test a few files that should show up, and
    # some that should be excluded.
    root_dir = Path(__file__).parents[2]
    py_files = file_utils.get_py_files(root_dir)
    filenames = [pf.name for pf in py_files]
    assert "__init__.py" in filenames
    assert "cli.py" in filenames
    assert "cli_messages.py" in filenames
    assert "py_bugger.py" in filenames
    assert "file_utils.py" in filenames

    assert "test_file_utils.py" not in filenames
    assert "test_basic_behavior.py" not in filenames
    assert "conftest.py" not in filenames

def test_get_py_files_non_git(tmp_path_factory):
    """Test function for getting .py files from a dir not managed by Git."""
    ...
