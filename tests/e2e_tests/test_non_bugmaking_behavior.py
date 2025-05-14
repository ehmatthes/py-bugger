"""Tests for behavior not specifically related to making bugs.
"""

import shutil
import shlex
import subprocess
import filecmp
import os
import sys


def test_preserve_file_ending_trailing_newline(tmp_path_factory, e2e_config):
    """Test that trailing newlines are preserved when present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_simple_indent.name
    shutil.copyfile(e2e_config.path_simple_indent, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type IndentationError --target-file {path_dst.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is blank.
    lines = path_dst.read_text().splitlines()
    breakpoint()
    assert lines[-1] == ""