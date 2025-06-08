"""Tests for behavior not specifically related to making bugs.

- How trailing newlines are handled.
- How incorret target types are handled.
"""

import shutil
import shlex
import subprocess
import filecmp
import os
import sys

import pytest


@pytest.mark.parametrize("exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"])
def test_preserve_file_ending_trailing_newline(tmp_path_factory, e2e_config, exception_type):
    """Test that trailing newlines are preserved when present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_dog_bark.name
    shutil.copyfile(e2e_config.path_dog_bark, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line has a trailing newline.
    lines = path_dst.read_text().splitlines(keepends=True)
    if exception_type == "AttributeError":
        # Random seed causes a bug in the last line, but we're just checking the line ending.
        assert lines[-1] == "dog.sayhi()\n"
    else:
        assert lines[-1] == "dog.say_hi()\n"


@pytest.mark.parametrize("exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"])
def test_preserve_file_ending_no_trailing_newline(tmp_path_factory, e2e_config, exception_type):
    """Test that trailing newlines are not introduced when not originally present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog_bark_no_trailing_newline.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is not blank.
    lines = path_dst.read_text().splitlines(keepends=True)
    if exception_type == "AttributeError":
        # Random seed causes a bug in the last line, but we're just checking the line ending.
        assert lines[-1] == "dog.sayhi()"
    else:
        assert lines[-1] == "dog.say_hi()"

@pytest.mark.parametrize("exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"])
def test_preserve_file_ending_two_trailing_newline(tmp_path_factory, e2e_config, exception_type):
    """Test that two trailing newlines are preserved when present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog_bark_two_trailing_newlines.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is not blank.
    lines = path_dst.read_text().splitlines(keepends=True)
    assert lines[-1] == "\n"

@pytest.mark.parametrize("exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"])
def test_blank_file_behavior(tmp_path_factory, e2e_config, exception_type):
    """Make sure py-bugger handles a blank file correctly."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "blank_file.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "Unable to introduce any of the requested bugs." in stdout

    # Check that file is still blank.
    contents = path_dst.read_text()
    assert contents == ""


def test_file_passed_to_targetdir(tmp_path_factory, e2e_config):
    """Make sure passing a file to --target-dir fails appropriately."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type AttributeError --target-dir {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = f"You specified --target-dir, but {path_dst.name} is a file. Did you mean to use --target-file?"
    assert msg_expected in stdout
