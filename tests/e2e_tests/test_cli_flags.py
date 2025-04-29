"""Test behavior of specific CLI flags.

Some flags that focus on bugs are covered in test_basic_behavior.py,
and other test modules. This module is for more generic flags such as -v.
"""

import shutil
import shlex
import subprocess
import filecmp
import os
import sys


def test_verbose_flag_true(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError --verbose"""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_name_picker.name
    shutil.copyfile(e2e_config.path_name_picker, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()} --verbose"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout
    assert "name_picker.py" in stdout


def test_verbose_flag_false(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError"""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_name_picker.name
    shutil.copyfile(e2e_config.path_name_picker, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout
    assert "Added bug." in stdout
    assert "name_picker.py" not in stdout
