"""A dog that barks. It's a class with an import.

This supports testing for:
- IndentationError
- AttributeError
- ModuleNotFoundError
"""

import random


class Dog:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print(f"Hi, I'm {self.name} the dog!")

    def bark(self):
        barks = ["woof", "ruff", "owooooo"]
        bark = random.choice(barks)
        print(f"{bark}!")


dog = Dog("Willie")
dog.bark()
dog.say_hi()

