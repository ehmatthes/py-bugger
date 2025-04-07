for num in [1, 2, 3]:
    print(num)

while True:
    print("one iteration")
    break


def add_two(x):
    return x + 2


print(add_two(5))


class Dog:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print(f"Hi, I'm {self.name} the dog!")


dog = Dog("Willie")
dog.say_hi()

try:
    5 / 0
except ZeroDivisionError:
    print("my bad!")

import random

roll = random.randint(1, 6)
if roll > 3:
    print("Yes!")
elif roll > 4:
    print("Yes yes!")
elif roll == 6:
    print("Yes yes yes!")
else:
    print("oh no")
