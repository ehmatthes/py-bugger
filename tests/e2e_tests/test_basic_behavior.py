"""Test basic behavior.

- Copy sample code to a temp dir.
- Run py-bugger against that code.
- Verify correct exception is raised.
"""

import shutil
import shlex
import subprocess
import filecmp
import os


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
    assert stdout.replace("\r\n", "\n") == path_bare_output.read_text().replace(
        "\r\n", "\n"
    )

    # Check that .py file is unchanged.
    assert filecmp.cmp(e2e_config.path_name_picker, path_dst)


def test_help(e2e_config):
    """Test output of `py-bugger --help`."""
    # Set an explicit column width, so output is consistent across systems.
    env = os.environ.copy()
    env["COLUMNS"] = "80"

    cmd = "py-bugger --help"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True, env=env).stdout.decode()

    path_help_output = e2e_config.path_reference_files / "help.txt"
    assert stdout.replace("\r\n", "\n") == path_help_output.read_text().replace(
        "\r\n", "\n"
    )


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
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'name_picker.py", line 1, in <module>' in stderr
    assert "ModuleNotFoundError: No module named" in stderr


def test_default_one_error(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError

    Test that only one import statement is modified.
    """

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_system_info.name
    shutil.copyfile(e2e_config.path_system_info, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'system_info_script.py", line 4, in <module>' in stderr
    assert "ModuleNotFoundError: No module named 'o'" in stderr

    # Read modified file; should have changed only one import statement.
    modified_source = path_dst.read_text()
    assert "import sys" in modified_source or "import os" in modified_source


def test_two_bugs(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError --num-bugs 2

    Test that both import statements are modified.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_system_info.name
    shutil.copyfile(e2e_config.path_system_info, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --num-bugs 2 --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'system_info_script.py", line 3, in <module>' in stderr
    assert "ModuleNotFoundError: No module named 'ys'" in stderr

    # Read modified file; should have changed both import statements.
    modified_source = path_dst.read_text()
    assert "import sys" not in modified_source
    assert "import os" not in modified_source


def test_random_import_affected(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError

    Test that a random import statement is modified.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_ten_imports.name
    shutil.copyfile(e2e_config.path_ten_imports, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    print(cmd)
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'ten_imports.py", line 6, in <module>' in stderr
    assert "ModuleNotFoundError: No module named 'clendar'" in stderr

    # Read modified file; should have changed import statement.
    modified_source = path_dst.read_text()
    assert "import clendar" in modified_source


def test_random_py_file_affected(tmp_path_factory, e2e_config):
    """py-bugger --exception-type ModuleNotFoundError

    Test that a random .py file is modified.
    """
    # Copy two sample scripts to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst_ten_imports = tmp_path / e2e_config.path_ten_imports.name
    shutil.copyfile(e2e_config.path_ten_imports, path_dst_ten_imports)

    path_dst_system_info = tmp_path / e2e_config.path_system_info.name
    shutil.copyfile(e2e_config.path_system_info, path_dst_system_info)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    print(cmd)
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst_ten_imports.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'ten_imports.py", line 7, in <module>' in stderr
    assert "ModuleNotFoundError: No module named 'zoneino'" in stderr

    # Other file should not be changed.
    assert filecmp.cmp(e2e_config.path_system_info, path_dst_system_info)


def test_unable_insert_all_bugs(tmp_path_factory, e2e_config):
    """Test for appropriate message when unable to generate all requested bugs."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_system_info.name
    shutil.copyfile(e2e_config.path_system_info, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError -n 3 --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "Inserted 2 bugs." in stdout
    assert "Unable to introduce additional bugs of the requested type." in stdout


def test_no_bugs(tmp_path_factory, e2e_config):
    """Test for appropriate message when unable to introduce any requested bugs."""
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_zero_imports.name
    shutil.copyfile(e2e_config.path_zero_imports, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "Unable to introduce any of the requested bugs." in stdout
