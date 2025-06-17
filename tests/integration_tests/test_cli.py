"""Tests that focus on the CLI itself."""

import shutil
import shlex
import subprocess
import filecmp
import os
import sys
import platform
from pathlib import Path

import pytest

from py_bugger.cli import cli_messages


@pytest.mark.parametrize(
    "exception_type", ["IndentationErrorr", "AttributeErrorr", "ModuleNotFoundErrorr"]
)
def test_exception_type_typo(exception_type):
    """Test appropriate handling of a typo in the exception type."""
    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file nonexistent_python_file.py --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True, text=True).stdout

    assert "Did you mean" in stdout