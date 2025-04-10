"""Tests for utils/file_utils.py.

This module does not use pb_config directly. That makes unit testing easier. To use
pb_config here, update tests to create an appropriate pb_config object.
"""

from pathlib import Path

import pytest

from py_bugger.utils import file_utils


def test_get_py_files_git():
    # This takes more setup. Need to actually initialize a Git dir. Could point it
    # at this project directory and just test a few files that should show up, and
    # some that should be excluded.
    root_dir = Path(__file__).parents[2]
    py_files = file_utils.get_py_files(root_dir, target_file="")
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
    # Build a tmp dir with some files that should be gathered, and some that
    # should not.
    tmp_path = tmp_path_factory.mktemp("sample_non_git_dir")

    path_tests = Path(tmp_path) / "tests"
    path_tests.mkdir()

    files = ["hello.py", "goodbye.py", "conftest.py", "tests/test_project.py"]
    for file in files:
        path = tmp_path / file
        path.touch()

    py_files = file_utils.get_py_files(tmp_path, target_file="")
    filenames = [pf.name for pf in py_files]

    assert "hello.py" in filenames
    assert "goodbye.py" in filenames

    assert "conftest.py" not in filenames
    assert "test_project.py" not in filenames


def test_get_py_files_target_file(tmp_path_factory):
    """Test function for getting .py files when target_file is set."""
    # Build a tmp dir with some files that should be gathered, and some that
    # should not.
    tmp_path = tmp_path_factory.mktemp("sample_non_git_dir")

    path_tests = Path(tmp_path) / "tests"
    path_tests.mkdir()

    files = ["hello.py", "goodbye.py", "conftest.py", "tests/test_project.py"]
    for file in files:
        path = tmp_path / file
        path.touch()

        # Set goodbye.py as the target file.
        if file == "goodbye.py":
            target_file = path

    py_files = file_utils.get_py_files(tmp_path, target_file)
    assert py_files == [target_file]
