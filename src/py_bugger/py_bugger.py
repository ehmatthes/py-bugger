import os
import random

from py_bugger.utils import file_utils
from py_bugger.utils import buggers


def main(exception_type, target_dir, num_bugs):

    # Set a random seed when testing.
    if seed := os.environ.get("PY_BUGGER_RANDOM_SEED"):
        random.seed(int(seed))

    # Get a list of .py files we can consider modifying.
    py_files = file_utils.get_py_files(target_dir)

    # Currently, just one exception type. When multiple are supported, implement
    # more complex logic for choosing which ones to introduce, and tracking bugs.
    if exception_type == "ModuleNotFoundError":
        new_bugs_made = buggers.module_not_found_bugger(py_files, num_bugs)

        assert new_bugs_made == num_bugs
