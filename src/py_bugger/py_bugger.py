import os
import random

from py_bugger import buggers
from py_bugger.utils import file_utils

from py_bugger.cli.config import pb_config
from py_bugger.cli.config import SUPPORTED_EXCEPTION_TYPES
from py_bugger.cli import cli_messages


# Set a random seed when testing.
if seed := os.environ.get("PY_BUGGER_RANDOM_SEED"):
    random.seed(int(seed))


def main():
    # Get a list of .py files we can consider modifying.
    py_files = file_utils.get_py_files(pb_config.target_dir, pb_config.target_file)

    # If --exception-type not specified, choose one.
    if not pb_config.exception_type:
        pb_config.exception_type = random.choice(SUPPORTED_EXCEPTION_TYPES)

    # Currently, handles just one exception type per py-bugger call.
    # When multiple are supported, implement more complex logic for choosing which ones
    # to introduce, and tracking bugs. Also consider a more appropriate dispatch approach
    # as the project evolves.
    for _ in range(pb_config.num_bugs):
        if pb_config.exception_type == "ModuleNotFoundError":
            buggers.module_not_found_bugger(py_files)
        elif pb_config.exception_type == "AttributeError":
            buggers.attribute_error_bugger(py_files)
        elif pb_config.exception_type == "IndentationError":
            buggers.indentation_error_bugger(py_files)

    # Show a final success/fail message.
    msg = cli_messages.success_msg()
    print(msg)
