"""Resources for modifying code in ways that make it break."""

import random


def make_typo(name):
    """Add a typo to the name of an identifier.

    Randomly decides which kind of change to make.
    """
    return remove_char(name)


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

def modify_char(name): ...
