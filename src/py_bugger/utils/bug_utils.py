"""Resources for modifying code in ways that make it break."""

import random
import builtins

from py_bugger.utils import file_utils
from py_bugger.utils.modification import Modification, modifications


def make_typo(name):
    """Add a typo to the name of an identifier.

    Randomly decides which kind of change to make.
    """
    typo_fns = [remove_char, insert_char, modify_char]

    while True:
        typo_fn = random.choice(typo_fns)
        new_name = typo_fn(name)

        # Reject names that match builtins.
        if new_name in dir(builtins):
            continue

        return new_name


def remove_char(name):
    """Remove a character from the name."""
    chars = list(name)
    index_remove = random.randint(0, len(chars) - 1)
    del chars[index_remove]

    return "".join(chars)


def insert_char(name):
    """Insert a character into the name."""
    chars = list(name)
    new_char = random.choice("abcdefghijklmnopqrstuvwxyz")
    index = random.randint(0, len(chars))
    chars.insert(index, new_char)

    return "".join(chars)


def modify_char(name):
    """Modify a character in a name."""
    chars = list(name)
    index = random.randint(0, len(chars) - 1)

    # Make sure new_char does not match current char.
    while True:
        new_char = random.choice("abcdefghijklmnopqrstuvwxyz")
        if new_char != chars[index]:
            break
    chars[index] = new_char

    return "".join(chars)


def add_indentation(path, target_line):
    """Add one level of indentation (four spaces) to line."""
    indentation_added = False

    lines = path.read_text().splitlines(keepends=True)

    modified_lines = []
    for line in lines:
        # `line` contains leading whitespace and trailing newline.
        # `target_line` just contains code, so use `in` rather than `==`.
        if target_line in line:
            modified_line = f"    {line}"
            modified_lines.append(modified_line)
            indentation_added = True

            # Record this modification.
            modification = Modification(
                path,
                original_line=line,
                modified_line=modified_line,
                exception_induced=IndentationError,
            )
            modifications.append(modification)
        else:
            modified_lines.append(line)

    modified_source = "".join(modified_lines)
    path.write_text(modified_source)

    return indentation_added


def add_indentation_linenum(path, target_line_num):
    """Add one level of indentation (four spaces) to line at linenum."""
    indentation_added = False

    lines = path.read_text().splitlines(keepends=True)

    modified_lines = []
    for line_num, line in enumerate(lines, start=1):
        if line_num == target_line_num:
            modified_line = f"    {line}"
            modified_lines.append(modified_line)
            indentation_added = True

            # Record this modification.
            modification = Modification(
                path,
                original_line=line,
                modified_line=modified_line,
                exception_induced=IndentationError,
                line_num=line_num,
            )
            modifications.append(modification)
        else:
            modified_lines.append(line)

    modified_source = "".join(modified_lines)
    path.write_text(modified_source)

    return indentation_added