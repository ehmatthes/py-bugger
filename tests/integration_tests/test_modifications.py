"""Test the modifications object."""

from pathlib import Path
import shutil
import os


def test_modifications_modulenotfounderror(tmp_path_factory):
    """Tests modifications after creating a ModuleNotFoundError."""
    path_root = Path(__file__).parents[2]
    path_tests = path_root / "tests"
    path_reference_files = path_tests / "e2e_tests" / "reference_files"
    path_sample_code = path_tests / "sample_code"
    path_sample_scripts = path_sample_code / "sample_scripts"

    from py_bugger.cli.config import pb_config
    from py_bugger.cli import cli_utils

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = path_sample_scripts / "name_picker.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this directory.
    pb_config.exception_type = "ModuleNotFoundError"
    pb_config.target_file = path_dst
    pb_config.ignore_git_status = True

    cli_utils.validate_config()

    from py_bugger import py_bugger
    py_bugger.main()

    from py_bugger.utils.modification import modifications
    assert len(modifications) == 1
    assert modifications[0].exception_induced == ModuleNotFoundError

    # Cleanup.
    pb_config.target_dir = None
    modifications.clear()

def test_5_random_bugs(tmp_path_factory, test_config):
    """Test equivalent of `py-bugger -n 5`.

    Look for modifications that match bugs_requested.
    """
    from py_bugger.cli.config import pb_config
    from py_bugger.cli import cli_utils

    # Copy sample code to tmp dir.
    tmp_path = tmp_path_factory.mktemp("sample_code")
    print(f"\nCopying code to: {tmp_path.as_posix()}")

    path_src = test_config.path_sample_scripts / "dog_bark.py"
    path_dst = tmp_path / path_src.name
    shutil.copyfile(path_src, path_dst)

    # Make modifications against this directory.
    pb_config.exception_type = ""
    pb_config.target_file = path_dst
    pb_config.ignore_git_status = True
    pb_config.num_bugs = 5

    cli_utils.validate_config()

    from py_bugger import py_bugger
    from py_bugger.utils.modification import modifications

    requested_bugs = py_bugger.main()
    breakpoint()

    assert len(modifications) == len(requested_bugs)

    exceptions_induced_str = [m.exception_induced.__name__ for m in modifications]
    assert sorted(exceptions_induced_str) == sorted(requested_bugs)

    # Cleanup.
    pb_config.target_dir = None
    modifications.clear()