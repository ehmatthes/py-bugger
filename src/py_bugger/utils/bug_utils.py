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
