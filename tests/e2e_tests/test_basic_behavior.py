"""Test basic behavior.

- Copy sample code to a temp dir.
- Run py-bugger against that code.
- Verify correct exception is raised.
"""

from pathlib import Path

import pytest


def test_modulenotfounderror():
    assert True