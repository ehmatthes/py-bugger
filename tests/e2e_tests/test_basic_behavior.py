"""Test basic behavior.

- Copy sample code to a temp dir.
- Run py-bugger against that code.
- Verify correct exception is raised.
"""

import shutil
import shlex
import subprocess
import filecmp


# --- Test functions ---

def test_bare_call(tmp_path_factory, e2e_config):
    """Test that bare py-bugger call does not modify file."""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_name_picker.name
    shutil.copyfile(e2e_config.path_name_picker, path_dst)

    # Make bare py-bugger call.
    cmd = f"py-bugger"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    # Verify output.
    path_bare_output = e2e_config.path_reference_files / "bare.txt"
    assert stdout == path_bare_output.read_text()

    # Check that .py file is unchanged.
    assert filecmp.cmp(e2e_config.path_name_picker, path_dst)


def test_help(e2e_config):
    """Test output of `py-bugger --help`."""
    cmd = "py-bugger --help"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    path_help_output = e2e_config.path_reference_files / "help.txt"
    assert stdout == path_help_output.read_text()


def test_modulenotfounderror(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError"""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_name_picker.name
    shutil.copyfile(e2e_config.path_name_picker, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'name_picker.py", line 1, in <module>' in stderr
    assert "ModuleNotFoundError: No module named" in stderr
