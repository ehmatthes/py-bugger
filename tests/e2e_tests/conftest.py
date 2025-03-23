from pathlib import Path
import sys

import pytest


# --- Fixtures ---


@pytest.fixture(scope="session")
def e2e_config():
    """Resources useful to most tests."""

    class Config:
        # Paths
        path_root = Path(__file__).parents[2]

        path_tests = path_root / "tests"

        path_reference_files = path_tests / "e2e_tests" / "reference_files"

        path_sample_code = path_tests / "sample_code"
        path_sample_scripts = path_sample_code / "sample_scripts"
        path_name_picker = path_sample_scripts / "name_picker.py"

        # Python executable
        if sys.platform == "win32":
            python_cmd = path_root / ".venv" / "Scripts" / "python"
        else:
            python_cmd = path_root / ".venv" / "bin" / "python"

    return Config()
