"""Resources for modifying code in ways that make it break."""

import random
import builtins


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

    lines = path.read_text().splitlines()

    modified_lines = []
    for line in lines:
        if line == target_line:
            line = f"    {line}"
            modified_lines.append(line)
            indentation_added = True
        else:
            modified_lines.append(line)

    modified_source = "\n".join(modified_lines)
    path.write_text(modified_source)

    return indentation_added


def mess_up_indentation(path, target_line):
    """
    Randomly mess with indentation of the target line.
    Options: indent, dedent, or bad-indent.
    """
    lines = path.read_text().splitlines()
    modified_lines = []
    modified = False

    for line in lines:
        if line == target_line and not modified:
            leading_spaces = len(line) - len(line.lstrip(" "))
            indent_unit = 4 if leading_spaces % 4 == 0 else 2
            action = random.choice(["indent", "dedent", "bad-indent"])

            if action == "indent":
                line = " " * indent_unit + line
            elif action == "dedent" and leading_spaces >= indent_unit:
                line = line[indent_unit:]
            elif action == "bad-indent":
                line = " " * (indent_unit + 1) + line.lstrip(" ")

            modified = True

        modified_lines.append(line)

    if modified:
        path.write_text("\n".join(modified_lines))
        return True
        
    return False