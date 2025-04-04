"""Tests for utilities that generate actual bugs."""

from py_bugger.utils import bug_utils


def test_remove_char():
    """Test utility for removing a random character from a name.

    Take a short name. Call remove_char() 25 times. Should end up with all variations.
    """
    name = "event"
    new_names = set([bug_utils.remove_char(name) for _ in range(1000)])

    assert new_names == {"vent", "eent", "evnt", "evet", "even"}


def test_insert_char():
    """Test utility for inserting a random character into a name."""
    for _ in range(100):
        name = "event"
        new_name = bug_utils.insert_char(name)

        assert new_name != name
        assert len(new_name) == len(name) + 1


def test_modify_char():
    """Test utility for modifying a name."""
    for _ in range(100):
        name = "event"
        new_name = bug_utils.modify_char(name)

        assert new_name != name
        assert len(new_name) == len(name)


def test_make_typo():
    """Test utility for generating a typo."""
    for _ in range(100):
        name = "event"
        new_name = bug_utils.make_typo(name)

        assert new_name != name


def test_no_builtin_name():
    """Make sure we don't get a builtin name such as `min`."""
    for _ in range(100):
        name = "mine"
        new_name = bug_utils.make_typo(name)

        assert new_name != name
        assert new_name != "min"
