"""Tests for utilities that generate actual bugs."""

from py_bugger.utils import bug_utils


def test_remove_char():
    """Test utility for removing a random character from a name.

    Take a short name. Call remove_char() 25 times. Should end up with all variations.
    """
    name = "part"
    new_names = [bug_utils.remove_char(name) for _ in range(25)]
    print(sorted(new_names))

    expected_names = ["art", "prt", "pat", "par"]
    assert all(en in new_names for en in expected_names)