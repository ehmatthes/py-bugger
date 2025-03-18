"""Test basic behavior.

- Copy sample code to a temp dir.
- Run py-bugger against that code.
- Verify correct exception is raised.
"""

from pathlib import Path
import shutil
import shlex
import subprocess
import filecmp

import pytest


# --- Fixtures ---

@pytest.fixture(scope="session")
def python_cmd():
    """Return path to Python executable."""
    path_root = Path(__file__).parents[2]
    return path_root / ".venv" / "bin" / "python"


# --- Test functions ---


def test_bare_call(tmp_path_factory, python_cmd):
    """Test that bare py-bugger call does not modify file."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_root = Path(__file__).parents[2]
    path_sample_code = path_root / "tests"/ "sample_code" / "sample_scripts"
    path_name_picker = path_sample_code / "name_picker.py"
    assert path_name_picker.exists()

    path_dst = tmp_path / path_name_picker.name
    shutil.copyfile(path_name_picker, path_dst)

    # Run file, should raise no issues.
    cmd = f"{python_cmd} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts, check=True)

    # Make bare py-bugger call.
    cmd = f"py-bugger"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()
    msg = "A bare py-bugger call makes no changes to your project.\nYou must be explicit about what kinds of errors you want to induce in the project."
    assert msg in stdout    

    # Check that file is unchanged.
    assert filecmp.cmp(path_name_picker, path_dst)


def test_help(python_cmd):
    """Test output of `py-bugger --help`."""
    path_root = Path(__file__).parents[2]
    cmd = "py-bugger --help"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    path_reference_files = path_root / "tests" / "e2e_tests" / "reference_files"
    path_help_output = path_reference_files / "help.txt"
    help_txt = path_help_output.read_text()

    assert stdout == help_txt


def test_modulenotfounderror(tmp_path_factory, python_cmd):
    """py-bugger --exception-type ModuleNotFoundError"""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_root = Path(__file__).parents[2]
    path_sample_code = path_root / "tests"/ "sample_code" / "sample_scripts"
    path_name_picker = path_sample_code / "name_picker.py"
    assert path_name_picker.exists()

    path_dst = tmp_path / path_name_picker.name
    shutil.copyfile(path_name_picker, path_dst)

    # Run file, should raise no issues.
    cmd = f"{python_cmd} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts, check=True)

    # Run py-bugger against file.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    # Run file again, should raise ModuleNotFoundError.
    cmd = f"{python_cmd} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'name_picker.py", line 1, in <module>' in stderr
    assert "ModuleNotFoundError: No module named" in stderr
