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
