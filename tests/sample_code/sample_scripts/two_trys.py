"""Simple file with two try-except blocks."""

try:
    5/0
except ZeroDivisionError:
    print("Can't divide by zero!")

try:
    10/0
except ZeroDivisionError:
    print("That doesn't work either!")
