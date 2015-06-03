import random

from collections import OrderedDict


class LineOrder(object):
    def __init__(self, key, max_lines):
        random.seed(key)
        self._used_numbers = OrderedDict()
        self._max_lines = max_lines

    def next(self):
        while True:
            number = random.randint(0, self._max_lines-1)
            if not number in self._used_numbers:
                self._used_numbers[number] = 1
                return number
