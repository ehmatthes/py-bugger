"""Test the modifications object."""

from pathlib import Path
import shutil

from py_bugger.cli import cli_utils



def test_modifications_modulenotfounderror(tmp_path_factory):
    """Tests modifications after creating a ModuleNotFoundError."""
    path_root = Path(__file__).parents[2]
    path_tests = path_root / "tests"
    path_reference_files = path_tests / "e2e_tests" / "reference_files"
    path_sample_code = path_tests / "sample_code"
    path_sample_scripts = path_sample_code / "sample_scripts"

    from py_bugger.cli.config import pb_config

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
    