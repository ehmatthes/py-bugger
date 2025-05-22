"""Tests for utilities that generate actual bugs."""

from py_bugger.utils import bug_utils
from unittest import mock
from pathlib import Path
import tempfile

def _write_temp_file(content: str) -> Path:
    """Create a temporary .py file with the given content and return its path."""
    tmp = tempfile.NamedTemporaryFile("w+", delete=False, suffix=".py")
    path = Path(tmp.name)
    path.write_text(content)
    return path

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

@mock.patch("random.choice", return_value="indent")
def test_mess_up_indentation_indent(mock_choice):
    # Should add one indentation level to the target line.
    path = _write_temp_file("def hello():\n    pass\n")
    bug_utils.mess_up_indentation(path, "def hello():")
    new_lines = path.read_text().splitlines()
    assert new_lines[0].startswith("    def hello():")
    path.unlink()


@mock.patch("random.choice", return_value="dedent")
def test_mess_up_indentation_dedent(mock_choice):
    # Should remove one indentation level from the target line.
    path = _write_temp_file("    def hello():\n    pass\n")
    bug_utils.mess_up_indentation(path, "    def hello():")
    new_lines = path.read_text().splitlines()
    assert new_lines[0].startswith("def hello():")
    path.unlink()


@mock.patch("random.choice", return_value="bad-indent")
def test_mess_up_indentation_bad_indent(mock_choice):
    # Should apply incorrect indentation (like 5 spaces) to the target line.
    path = _write_temp_file("    def hello():\n    pass\n")
    bug_utils.mess_up_indentation(path, "    def hello():")
    new_lines = path.read_text().splitlines()
    assert new_lines[0].startswith("     def hello():")  # 5 spaces
    path.unlink()


@mock.patch("random.choice", return_value="indent")
def test_mess_up_indentation_modifies_target_line(mock_choice):
    # Should modify the line if it matches the target line.
    path = _write_temp_file("def hello():\n    print('hi')\n")
    modified = bug_utils.mess_up_indentation(path, "def hello():")
    new_lines = path.read_text().splitlines()
    assert modified is True
    assert new_lines[0] != "def hello():"
    assert new_lines[1] == "    print('hi')"
    path.unlink()

def test_mess_up_indentation_returns_false_if_line_not_found():
    # Should return False if the target line is not present in the file.
    path = _write_temp_file("def hello():\n    print('hi')\n")
    modified = bug_utils.mess_up_indentation(path, "def missing():")
    assert modified is False
    path.unlink()