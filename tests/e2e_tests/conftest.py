from pathlib import Path
import sys
import os

import pytest


# --- Fixtures ---


@pytest.fixture(autouse=True, scope="session")
def set_random_seed_env():
    """Make random selections repeatable."""
    # To verify a random action, set autouse to False and run one test.
    os.environ["PY_BUGGER_RANDOM_SEED"] = "10"


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
        path_system_info = path_sample_scripts / "system_info_script.py"
        path_ten_imports = path_sample_scripts / "ten_imports.py"
        path_zero_imports = path_sample_scripts / "zero_imports.py"
        path_dog = path_sample_scripts / "dog.py"
        path_identical_attributes = path_sample_scripts / "identical_attributes.py"

        # Python executable
        if sys.platform == "win32":
            python_cmd = path_root / ".venv" / "Scripts" / "python"
        else:
            python_cmd = path_root / ".venv" / "bin" / "python"

    return Config()
