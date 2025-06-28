import os
import random

from py_bugger import buggers
from py_bugger.utils import file_utils

from py_bugger.cli.config import pb_config
from py_bugger.cli.config import SUPPORTED_EXCEPTION_TYPES
from py_bugger.cli import cli_messages


def main():
    set_random_seed()

    # Get a list of .py files we can consider modifying.
    py_files = file_utils.get_py_files(pb_config.target_dir, pb_config.target_file)

    # Make a list of bugs to introduce.
    if pb_config.exception_type:
        # User has requested a specific kind of bug.
        requested_bugs = [pb_config.exception_type for _ in range(pb_config.num_bugs)]
    else:
        # No -e arg passed; get a random sequence of bugs to introduce.
        # Reorder sequence so all regex parsing happens after CST parsing. CST parsing
        # will fail if it's attempted after introducing a bug that affects parsing.
        requested_bugs = random.choices(SUPPORTED_EXCEPTION_TYPES, k=pb_config.num_bugs)
        requested_bugs = sorted(requested_bugs, key=lambda b: b == "IndentationError")

    # Introduce bugs, one at a time.
    for bug in requested_bugs:
        if bug == "ModuleNotFoundError":
            buggers.module_not_found_bugger(py_files)
        elif bug == "AttributeError":
            buggers.attribute_error_bugger(py_files)
        elif bug == "IndentationError":
            buggers.indentation_error_bugger(py_files)

    # Show a final success/fail message.
    msg = cli_messages.success_msg()
    print(msg)

    # Returning requested_bugs helps with testing.
    return requested_bugs


# --- Helper functions ---


def set_random_seed():
    # Set a random seed when testing.
    if seed := os.environ.get("PY_BUGGER_RANDOM_SEED"):
        random.seed(int(seed))
