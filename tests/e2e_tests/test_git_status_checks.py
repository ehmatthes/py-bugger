"""Tests for all the checks related to Git status.

This is handled in cli_utils.py.
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
from py_bugger.cli.config import PBConfig


def test_git_not_available(tmp_path_factory, e2e_config, on_windows):
    """Check appropriate message shown when Git not available."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file. We're emptying PATH in order to make sure Git is not
    # available for this run, so we need the direct path to the py-bugger command.
    py_bugger_exe = Path(sys.executable).parent / "py-bugger"
    cmd = f"{py_bugger_exe} --exception-type IndentationError --target-file {path_dst.as_posix()}"
    print("\ncmd:", cmd)
    cmd_parts = shlex.split(cmd)

    env = os.environ.copy()
    env["PATH"] = ""
    # stdout = subprocess.run(cmd_parts, capture_output=True, env=env).stdout.decode()
    stdout = subprocess.run(cmd_parts, capture_output=True, env=env, text=True, shell=on_windows).stdout
    return
    msg_expected = cli_messages.msg_git_not_available
    assert msg_expected in stdout

def test_git_not_used(tmp_path_factory, e2e_config):
    """Check appropriate message shown when Git not being used."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file. This is one of the few e2e tests where --ignore-git-status
    # is not passed, because we want to verify appropriate behavior without a clean Git status.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    pb_config = PBConfig()
    pb_config.target_file = path_dst
    msg_expected = cli_messages.msg_git_not_used(pb_config)
    assert msg_expected in stdout


def test_unclean_git_status(tmp_path_factory, e2e_config):
    """Check appropriate message shown when Git status is not clean."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run git init, but don't make a commit. This is enough to create an unclean status.
    cmd = "git init"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts, cwd=tmp_path)

    # Run py-bugger against file. This is one of the few e2e tests where --ignore-git-status
    # is not passed, because we want to verify appropriate behavior without a clean Git status.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True, text=True).stdout

    msg_expected = cli_messages.msg_unclean_git_status
    assert msg_expected in stdout


def test_clean_git_status(tmp_path_factory, e2e_config):
    """Run py-bugger against a tiny repo with a clean status, without passing
    --ignore-git-status.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make an initial commit with a clean status.
    cmd = "git init"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts, cwd=tmp_path)

    cmd = "git add ."
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts, cwd=tmp_path)

    cmd = 'git commit -m "Initial state."'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts, cwd=tmp_path)

    # Run py-bugger against file. This is one of the few e2e tests where --ignore-git-status
    # is not passed, because we want to verify appropriate behavior with a clean Git status.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True, text=True).stdout

    assert "All requested bugs inserted." in stdout

    # Run file, should raise AttributeError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'dog.py", line ' in stderr
    assert "AttributeError: " in stderr
    assert "Did you mean: " in stderr


def test_ignore_git_status(tmp_path_factory, e2e_config):
    """Test that py-bugger runs when --ignore-git-status is passed.

    This is the test for Git not being used, with a different assertion.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = e2e_config.path_sample_scripts / "dog.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Run py-bugger against file, passing --ignore-git-status.
    cmd = f"py-bugger --exception-type AttributeError --target-file {path_dst.as_posix()} --ignore-git-status"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise AttributeError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'dog.py", line ' in stderr
    assert "AttributeError: " in stderr
    assert "Did you mean: " in stderr