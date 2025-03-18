"""Test basic behavior.

- Copy sample code to a temp dir.
- Run py-bugger against that code.
- Verify correct exception is raised.
"""

from pathlib import Path
import shutil

import pytest


def test_modulenotfounderror(tmp_path_factory):
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

    

