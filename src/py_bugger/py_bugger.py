import os
import random

from py_bugger import buggers
from py_bugger.utils import file_utils


def main(config):

    # Set a random seed when testing.
    if seed := os.environ.get("PY_BUGGER_RANDOM_SEED"):
        random.seed(int(seed))

    # Get a list of .py files we can consider modifying.
    if config.target_file:
        # User requested a single target file.
        py_files = [config.target_file]
    else:
        py_files = file_utils.get_py_files(config.target_dir)

    # Track how many bugs have been added.
    bugs_added = 0

    # Currently, just one exception type. When multiple are supported, implement
    # more complex logic for choosing which ones to introduce, and tracking bugs.
    if config.exception_type == "ModuleNotFoundError":
        new_bugs_made = buggers.module_not_found_bugger(py_files, config.num_bugs)
        bugs_added += new_bugs_made
    elif config.exception_type == "AttributeError":
        new_bugs_made = buggers.attribute_error_bugger(py_files, config.num_bugs)
        bugs_added += new_bugs_made
    elif config.exception_type == "IndentationError":
        new_bugs_made = buggers.indentation_error_bugger(py_files, config.num_bugs)
        bugs_added += new_bugs_made

    # Show a final success/fail message.
    if bugs_added == config.num_bugs:
        print("All requested bugs inserted.")
    elif bugs_added == 0:
        print("Unable to introduce any of the requested bugs.")
    else:
        msg = f"Inserted {bugs_added} bugs."
        msg += "\nUnable to introduce additional bugs of the requested type."
        print(msg)
