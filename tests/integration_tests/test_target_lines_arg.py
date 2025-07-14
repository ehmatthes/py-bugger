"""Test modifications made when --target-lines is set."""

from pathlib import Path
import shutil
import os

import pytest

from py_bugger import py_bugger
from py_bugger.cli.config import pb_config
from py_bugger.cli import cli_utils
from py_bugger.utils.modification import modifications


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
