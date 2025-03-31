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
import sys


# --- Test functions ---


def test_no_exception_type(tmp_path_factory, e2e_config):
    """Test output for not passing --exception-type."""

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
    path = e2e_config.path_reference_files / "no_exception_type.txt"
    assert stdout.replace("\r\n", "\n") == path.read_text().replace("\r\n", "\n")

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
    assert 'system_info_script.py", line ' in stderr
    assert "ModuleNotFoundError: No module named " in stderr

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
    assert "ModuleNotFoundError: No module named " in stderr

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
    assert 'ten_imports.py", line ' in stderr
    assert "ModuleNotFoundError: No module named " in stderr

    # Read modified file; should have changed one import statement.
    modified_source = path_dst.read_text()
    pkgs = [
        "os",
        "sys",
        "re",
        "random",
        "difflib",
        "calendar",
        "zoneinfo",
        "array",
        "pprint",
        "enum",
    ]
    assert sum([p in modified_source for p in pkgs]) == 9


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
    assert 'ten_imports.py", line ' in stderr
    assert "ModuleNotFoundError: No module named " in stderr

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


def test_target_dir_and_file(tmp_path_factory, e2e_config):
    """Test an invalid call including --target-dir and --target-file."""
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_zero_imports.name
    shutil.copyfile(e2e_config.path_zero_imports, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-dir {tmp_path.as_posix()} --target-file {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert (
        "Target file overrides target dir. Please only pass one of these args."
        in stdout
    )


def test_target_file(tmp_path_factory, e2e_config):
    """Test for passing --target-file."""
    # Copy two sample scripts to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst_ten_imports = tmp_path / e2e_config.path_ten_imports.name
    shutil.copyfile(e2e_config.path_ten_imports, path_dst_ten_imports)

    path_dst_system_info = tmp_path / e2e_config.path_system_info.name
    shutil.copyfile(e2e_config.path_system_info, path_dst_system_info)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type ModuleNotFoundError --target-file {path_dst_system_info.as_posix()}"
    print(cmd)
    cmd_parts = shlex.split(cmd)
    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise ModuleNotFoundError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst_system_info.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'system_info_script.py", line ' in stderr
    assert "ModuleNotFoundError: No module named " in stderr

    # Other file should not be changed.
    assert filecmp.cmp(e2e_config.path_ten_imports, path_dst_ten_imports)


def test_attribute_error(tmp_path_factory, e2e_config):
    """py-bugger --exception-type AttributeError"""

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_name_picker.name
    shutil.copyfile(e2e_config.path_name_picker, path_dst)

    # Run py-bugger against directory.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-dir {tmp_path.as_posix()}"
    )
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise AttributeError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'name_picker.py", line ' in stderr
    assert "AttributeError: " in stderr
    assert "Did you mean: " in stderr


def test_one_node_changed(tmp_path_factory, e2e_config):
    """Test that only one node in a file is modified for identical nodes."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_dog.name
    shutil.copyfile(e2e_config.path_dog, path_dst)

    # Run py-bugger against directory.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-dir {tmp_path.as_posix()}"
    )
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise AttributeError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'dog.py", line 10, in <module>' in stderr
    assert "AttributeError: 'Dog' object has no attribute " in stderr
    assert "Did you mean: " in stderr

    # Make sure only one attribute was affected.
    modified_source = path_dst.read_text()
    assert "self.name" in modified_source
    assert "self.nam" in modified_source


def test_random_node_changed(tmp_path_factory, e2e_config):
    """Test that a random node in a file is modified if it has numerous identical nodes."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_identical_attributes.name
    shutil.copyfile(e2e_config.path_identical_attributes, path_dst)

    # Run py-bugger against directory.
    cmd = (
        f"py-bugger --exception-type AttributeError --target-dir {tmp_path.as_posix()}"
    )
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise AttributeError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "Traceback (most recent call last)" in stderr
    assert 'identical_attributes.py", line ' in stderr
    assert "AttributeError: module 'random' has no attribute " in stderr
    assert "Did you mean: " in stderr

    # Make sure only one attribute was affected.
    modified_source = path_dst.read_text()
    assert modified_source.count("random.choice(") == 19


def test_indentation_error_simple(tmp_path_factory, e2e_config):
    """py-bugger --exception-type IndentationError

    Run against a file with a single indented block.
    """

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_simple_indent.name
    shutil.copyfile(e2e_config.path_simple_indent, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type IndentationError --target-dir {tmp_path.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise IndentationError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "IndentationError: unexpected indent" in stderr
    assert 'simple_indent.py", line 1' in stderr


def test_indentation_error_complex(tmp_path_factory, e2e_config):
    """py-bugger --exception-type IndentationError

    Run against a file with multiple indented blocks of different kinds.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_many_dogs.name
    shutil.copyfile(e2e_config.path_many_dogs, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type IndentationError --target-dir {tmp_path.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise IndentationError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "IndentationError: unexpected indent" in stderr
    assert 'many_dogs.py", line 1' in stderr


def test_all_indentation_blocks(tmp_path_factory, e2e_config):
    """Test that all kinds of indented blocks can be modified.

    Note: There are a couple blocks that aren't currently in all_indentation_blocks.py
        match, case, finally
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_dst = tmp_path / e2e_config.path_all_indentation_blocks.name
    shutil.copyfile(e2e_config.path_all_indentation_blocks, path_dst)

    # Run py-bugger against directory.
    cmd = f"py-bugger --exception-type IndentationError --num-bugs 12 --target-dir {tmp_path.as_posix()}"
    print("cmd:", cmd)
    cmd_parts = shlex.split(cmd)

    stdout = subprocess.run(cmd_parts, capture_output=True).stdout.decode()

    assert "All requested bugs inserted." in stdout

    # Run file, should raise IndentationError.
    cmd = f"{e2e_config.python_cmd.as_posix()} {path_dst.as_posix()}"
    cmd_parts = shlex.split(cmd)
    stderr = subprocess.run(cmd_parts, capture_output=True).stderr.decode()
    assert "IndentationError: unexpected indent" in stderr
    assert 'all_indentation_blocks.py", line 1' in stderr
