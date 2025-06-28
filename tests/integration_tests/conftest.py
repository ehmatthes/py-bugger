"""Config for integration tests.

Any test that's more than a unit test, but doesn't require running py-bugger against
actual code should probably be an integration test.
"""

import pytest

from py_bugger.utils.modification import modifications
from py_bugger.cli.config import pb_config


@pytest.fixture(autouse=True, scope="function")
def reset_pbconfig():
    """Reset the pb_config object for each test."""
    # Cleanup.
    pb_config.target_dir = None
    modifications.clear()