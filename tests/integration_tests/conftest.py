"""Config for integration tests.

Any test that's more than a unit test, but doesn't require running py-bugger against
actual code should probably be an integration test.
"""

import pytest

from py_bugger.utils.modification import modifications
from py_bugger.cli.config import pb_config


@pytest.fixture(autouse=True, scope="function")
def reset_state():
    """Reset the shared state objects for each test."""

    # Reset pb_config.
    pb_config.exception_type = ""
    pb_config.target_dir = ""
    pb_config.target_file = ""
    pb_config.num_bugs = 1
    pb_config.ignore_git_status = False
    pb_config.verbose = True

    # Reset list of modifications.
    modifications.clear()

    # Customize some state. For some tests, you may need to override
    # these customizations in specific test functions.

    # For most integration tests, we're targeting a sample file or directory
    # that has not been set up as a Git repo.
    pb_config.ignore_git_status = True
