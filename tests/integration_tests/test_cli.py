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
    "actual_expected",
    [
        ("IndentationErrorr", "IndentationError"),
        ("AttributeErrorr", "AttributeError"),
        ("ModuleNotFoundErrorr", "ModuleNotFoundError"),
    ],
)
def test_exception_type_typo(actual_expected):
    """Test appropriate handling of a typo in the exception type."""
    # Run py-bugger against file.
    exception_type, correction = actual_expected
    cmd = f"py-bugger --exception-type {exception_type} --target-file nonexistent_python_file.py --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True, text=True).stdout

    msg_expected = cli_messages.msg_apparent_typo(exception_type, correction)
    assert msg_expected in stdout


def test_exception_type_unsupported():
    """Test appropriate handling of an unsupported exception type."""
    # Run py-bugger against file.
    exception_type = "CompletelyUnsupportedExceptionType"
    cmd = f"py-bugger --exception-type {exception_type} --target-file nonexistent_python_file.py --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True, text=True).stdout

    msg_expected = cli_messages.msg_unsupported_exception_type(exception_type)
    assert msg_expected in stdout
