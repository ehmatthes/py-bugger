"""Tests for behavior not specifically related to making bugs.
"""

import shutil
import shlex
import subprocess
import filecmp
import os
import sys

import pytest


# Skip this test until resuming work on #39.
@pytest.mark.skip
@pytest.mark.parametrize("exception_type", ["IndentationError", "AttributeError"])
def test_preserve_file_ending_trailing_newline(tmp_path_factory, e2e_config, exception_type):
    """Test that trailing newlines are preserved when present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_simple_indent.name
    shutil.copyfile(e2e_config.path_dog, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is blank.
    lines = path_dst.read_text().splitlines()
    assert lines[-1] == ""


@pytest.mark.parametrize("exception_type", ["IndentationError", "AttributeError"])
def test_preserve_file_ending_no_trailing_newline(tmp_path_factory, e2e_config, exception_type):
    """Test that trailing newlines are not introduced when not originally present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog_no_trailing_newline.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is not blank.
    lines = path_dst.read_text().splitlines()
    assert lines[-1] != ""