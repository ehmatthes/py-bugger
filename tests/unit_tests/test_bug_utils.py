"""Tests for utilities that generate actual bugs."""

from py_bugger.utils import bug_utils


def test_remove_char():
    """Test utility for removing a random character from a name.

    Take a short name. Call remove_char() 25 times. Should end up with all variations.
    """
    name = "part"
    new_names = set([bug_utils.remove_char(name) for _ in range(25)])

    assert new_names == {"art", "prt", "pat", "par"}
