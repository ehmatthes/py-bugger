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
    char_remove = random.choice(chars)
    chars.remove(char_remove)
    new_name = "".join(chars)

    return new_name

def insert_char(name):
    ...

def modify_char(name):
    ...