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
import platform
from pathlib import Path

import pytest

from py_bugger.cli import cli_messages


# --- Tests for handling of line endings. ---


@pytest.mark.parametrize(
    "exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"]
)
def test_preserve_file_ending_trailing_newline(
    tmp_path_factory, test_config, exception_type
):
    """Test that trailing newlines are preserved when present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / test_config.path_dog_bark.name
    shutil.copyfile(test_config.path_dog_bark, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()} --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line has a trailing newline.
    lines = path_dst.read_text().splitlines(keepends=True)

    assert lines[-1] == "dog.say_hi()\n"


@pytest.mark.parametrize(
    "exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"]
)
def test_preserve_file_ending_no_trailing_newline(
    tmp_path_factory, test_config, exception_type
):
    """Test that trailing newlines are not introduced when not originally present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark_no_trailing_newline.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()} --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is not blank.
    lines = path_dst.read_text().splitlines(keepends=True)

    assert lines[-1] == "dog.say_hi()"


@pytest.mark.parametrize(
    "exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"]
)
def test_preserve_file_ending_two_trailing_newline(
    tmp_path_factory, test_config, exception_type
):
    """Test that two trailing newlines are preserved when present."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark_two_trailing_newlines.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()} --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Check that last line is not blank.
    lines = path_dst.read_text().splitlines(keepends=True)
    assert lines[-1] == "\n"


### --- Test for handling of blank files ---


@pytest.mark.parametrize(
    "exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"]
)
def test_blank_file_behavior(tmp_path_factory, test_config, exception_type):
    """Make sure py-bugger handles a blank file correctly."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "blank_file.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type {exception_type} --target-file {path_dst.as_posix()} --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "Unable to introduce any of the requested bugs." in stdout

    # Check that file is still blank.
    contents = path_dst.read_text()
    assert contents == ""


### --- Tests for invalid --target-dir calls ---


def test_file_passed_to_targetdir(tmp_path_factory, test_config):
    """Make sure passing a file to --target-dir fails appropriately."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-dir {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_file_not_dir(path_dst)
    assert msg_expected in stdout


def test_nonexistent_dir_passed_to_targetdir():
    """Make sure passing a nonexistent dir to --target-dir fails appropriately."""

    # Make a dir path that doesn't exist. If this assertion fails, something weird happened.
    path_dst = Path("nonsense_name")
    assert not path_dst.exists()

    # Run py-bugger against nonexistent dir.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-dir {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_nonexistent_dir(path_dst)
    assert msg_expected in stdout


@pytest.mark.skipif(
    platform.system() == "Windows", reason="Can't use /dev/null on Windows."
)
def test_targetdir_exists_not_dir():
    """Passed something that exists, but is not a file or dir.."""

    # /dev/null is neither a file or a dir, but exists.
    path_dst = Path("/dev/null")
    assert path_dst.exists()
    assert not path_dst.is_file()
    assert not path_dst.is_dir()

    # Run py-bugger.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-dir {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_not_dir(path_dst)
    assert msg_expected in stdout


### --- Tests for invalid --target-file calls ---


def test_dir_passed_to_targetfile(tmp_path_factory):
    """Make sure passing a dir to --target-file fails appropriately."""
    path_dst = tmp_path_factory.mktemp("sample_code")

    # Run py-bugger.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_dir_not_file(path_dst)
    assert msg_expected in stdout


def test_nonexistent_file_passed_to_targetfile():
    """Make sure passing a nonexistent file to --target-file fails appropriately."""

    # Make a file path that doesn't exist. If this assertion fails, something weird happened.
    path_dst = Path("nonsense_python_file.py")
    assert not path_dst.exists()

    # Run py-bugger.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_nonexistent_file(path_dst)
    assert msg_expected in stdout


@pytest.mark.skipif(
    platform.system() == "Windows", reason="Can't use /dev/null on Windows."
)
def test_targetfile_exists_not_file():
    """Passed something that exists, but is not a file or dir.."""

    # /dev/null is neither a file or a dir, but exists.
    path_dst = Path("/dev/null")
    assert path_dst.exists()
    assert not path_dst.is_file()
    assert not path_dst.is_dir()

    # Run py-bugger.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_not_file(path_dst)
    assert msg_expected in stdout


def test_targetfile_py_file(tmp_path_factory, test_config):
    """Test for appropriate message when passed a non-.py file."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "hello.txt"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    msg_expected = cli_messages.msg_file_not_py(path_dst)
    assert msg_expected in stdout
