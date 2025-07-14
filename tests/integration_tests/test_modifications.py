"""Test the modifications object."""

from pathlib import Path
import shutil
import os

import pytest

from py_bugger import py_bugger
from py_bugger.cli.config import pb_config
from py_bugger.cli import cli_utils
from py_bugger.utils.modification import modifications


def test_modifications_modulenotfounderror(tmp_path_factory, test_config):
    """Tests modifications after creating a ModuleNotFoundError."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "name_picker.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this directory.
    pb_config.exception_type = "ModuleNotFoundError"
    pb_config.target_file = path_dst
    cli_utils.validate_config()

    py_bugger.main()

    assert len(modifications) == 1
    assert modifications[0].exception_induced == ModuleNotFoundError


def test_7_random_bugs(tmp_path_factory, test_config):
    """Test equivalent of `py-bugger -n 7`.

    Look for modifications that match bugs_requested.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this directory.
    # With the current random seed, 7 seems to be the max number of bugs before
    # it can't add more.
    pb_config.target_file = path_dst
    pb_config.num_bugs = 7
    cli_utils.validate_config()

    requested_bugs = py_bugger.main()

    # Make sure one modification was made for each requested bug.
    assert len(modifications) == len(requested_bugs)

    # Make sure the correct kinds of exceptions were induced.
    exceptions_induced_str = [m.exception_induced.__name__ for m in modifications]
    assert sorted(exceptions_induced_str) == sorted(requested_bugs)


def test_8_random_bugs(tmp_path_factory, test_config):
    """Test equivalent of `py-bugger -n 8`.

    Look for modifications that match bugs_requested.
    Look for message that it can't add more bugs.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this directory.
    # With the current random seed, 8 seems to be the smallest number of bugs
    # where it can't finish adding bugs.
    pb_config.target_file = path_dst
    pb_config.num_bugs = 8
    cli_utils.validate_config()

    requested_bugs = py_bugger.main()

    # Make sure one requested bug was unable to be generated.
    assert len(modifications) == len(requested_bugs) - 1

    # Make sure all requested bugs except one are in modifications.
    exceptions_induced_str = [m.exception_induced.__name__ for m in modifications]
    while exceptions_induced_str:
        exception_induced = exceptions_induced_str.pop()
        requested_bugs.remove(exception_induced)

    assert len(requested_bugs) == 1

def test_indentationerror_multiple_trys(tmp_path_factory, test_config):
    """Test requesting a single IndentationError against a file with two try blocks.

    This is related to issue 65, where the bare try block that's being targeted matches
    every try block in the file. We should see just one modification.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "two_trys.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.num_bugs = 1
    pb_config.exception_type = "IndentationError"
    cli_utils.validate_config()

    requested_bugs = py_bugger.main()

    # Check that only one modification was made.
    assert len(modifications) == 1

def test_first_try_not_indented(tmp_path_factory, test_config):
    """Make sure a random try block is affected, not always the first one.

    This is related to issue 65, where the bare try block that's being targeted matches
    every try block in the file. We should see just one modification, and it should be
    a random one.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "five_trys.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.num_bugs = 1
    pb_config.exception_type = "IndentationError"
    cli_utils.validate_config()

    requested_bugs = py_bugger.main()

    # Check that only one modification was made.
    assert len(modifications) == 1

    # Read modified file. Make sure first try line hasn't changed. Make sure one
    # try has been indented.
    lines = path_dst.read_text().splitlines()
    assert lines[2] == "try:"
    assert lines.count("    try:") == 1

@pytest.mark.parametrize(
    "exception_type", ["IndentationError", "AttributeError", "ModuleNotFoundError"]
)
def test_linenums_recorded(tmp_path_factory, test_config, exception_type):
    """Test that a line number is recorded for each exception type."""
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = exception_type
    cli_utils.validate_config()

    requested_bugs = py_bugger.main()

    assert len(modifications) == 1
    assert modifications[0].line_num > 0

# --- Tests for --target-lines ---

def test_target_lines_block_indentation_error(tmp_path_factory, test_config):
    """Test that the modified line is in the targeted block.

    This test was first written without --target-lines. Then a block of
    lines was identifed that didn't contain the bug that was originally made.
    We're asserting that the change made is different than what would have been
    introduced without this target block.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "IndentationError"
    pb_config.target_lines = "19-22"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [19, 20, 21, 22]

    requested_bugs = py_bugger.main()

    # Without including --target-lines, line 12 was modified. Make sure the line that
    # was modified with --target-lines is in the target block.
    assert len(modifications) == 1
    assert modifications[0].line_num in pb_config.target_lines

def test_target_lines_block_attribute_error(tmp_path_factory, test_config):
    """Test that the modified line is in the targeted block.

    This test was first written without --target-lines. Then a block of
    lines was identifed that didn't contain the bug that was originally made.
    We're asserting that the change made is different than what would have been
    introduced without this target block.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "AttributeError"
    pb_config.target_lines = "12-22"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

    requested_bugs = py_bugger.main()

    # Without including --target-lines, line 26 was modified. Make sure the line that
    # was modified with --target-lines is in the target block.
    assert len(modifications) == 1
    assert modifications[0].line_num in pb_config.target_lines

def test_target_lines_block_modulenotfound_error(tmp_path_factory, test_config):
    """Test that the modified line is in the targeted block.

    This test was first written without --target-lines. Then a block of
    lines was identifed that didn't contain the bug that was originally made.
    We're asserting that the change made is different than what would have been
    introduced without this target block.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "ten_imports.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "ModuleNotFoundError"
    pb_config.target_lines = "1-3"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [1, 2, 3]

    requested_bugs = py_bugger.main()

    # Without including --target-lines, line 6 was modified. Make sure the line that
    # was modified with --target-lines is in the target block.
    assert len(modifications) == 1
    assert modifications[0].line_num in pb_config.target_lines

def test_single_target_line_indentation_error(tmp_path_factory, test_config):
    """Test that the modified line is the targeted line.

    This test was first written without --target-lines. Then a line
    was identifed that didn't contain the bug that was originally made.
    We're asserting that the change made is different than what would have been
    introduced without this target line.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "IndentationError"
    pb_config.target_lines = "16"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [16]

    requested_bugs = py_bugger.main()

    # Without including --target-lines, line 12 was modified. Make sure the line that
    # was modified with --target-lines is the target line.
    assert len(modifications) == 1
    assert modifications[0].line_num in pb_config.target_lines

def test_single_target_line_attribute_error(tmp_path_factory, test_config):
    """Test that the modified line is the targeted line.

    This test was first written without --target-lines. Then a line
    was identifed that didn't contain the bug that was originally made.
    We're asserting that the change made is different than what would have been
    introduced without this target line.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "AttributeError"
    pb_config.target_lines = "14"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [14]

    requested_bugs = py_bugger.main()

    # Without including --target-lines, line 26 was modified. Make sure the line that
    # was modified with --target-lines is the target line.
    assert len(modifications) == 1
    assert modifications[0].line_num in pb_config.target_lines

def test_target_lines_block_modulenotfound_error(tmp_path_factory, test_config):
    """Test that the modified line is the targeted line.

    This test was first written without --target-lines. Then a line
    was identifed that didn't contain the bug that was originally made.
    We're asserting that the change made is different than what would have been
    introduced without this target line.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "ten_imports.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "ModuleNotFoundError"
    pb_config.target_lines = "4"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [4]

    requested_bugs = py_bugger.main()

    # Without including --target-lines, line 6 was modified. Make sure the line that
    # was modified with --target-lines is the target line.
    assert len(modifications) == 1
    assert modifications[0].line_num in pb_config.target_lines







def test_single_target_line_indentation_error_not_possible(tmp_path_factory, test_config):
    """Test that a target line where the error can't be induced results in no modifications.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "IndentationError"
    pb_config.target_lines = "9"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [9]

    requested_bugs = py_bugger.main()

    assert not modifications

def test_single_target_line_attribute_error_not_possible(tmp_path_factory, test_config):
    """Test that a target line where the error can't be induced results in no modifications.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "AttributeError"
    pb_config.target_lines = "12"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [12]

    requested_bugs = py_bugger.main()

    assert not modifications

def test_target_lines_block_modulenotfound_error_not_possible(tmp_path_factory, test_config):
    """Test that a target line where the error can't be induced results in no modifications.
    """
    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this file.
    pb_config.target_file = path_dst
    pb_config.exception_type = "ModuleNotFoundError"
    pb_config.target_lines = "12"
    cli_utils.validate_config()

    # Check that the --target-lines arg was converted correctly.
    assert pb_config.target_lines == [12]

    requested_bugs = py_bugger.main()

    assert not modifications