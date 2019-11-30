from dataclasses import dataclass
from typing import Tuple


@dataclass
class ShrinkSizeCalculator:
    _now: Tuple[int, int]
    _limit: int

    def needs_shrink(self):
        width, height = self._now
        return width > self._limit and height > self._limit

    def shrink_size(self):
        width, height = self._now
        if width > height:
            new_width = self._limit
            new_height = int((self._limit / width) * height)
            return (new_width, new_height)
        new_width = int((self._limit / height) * width)
        new_height = self._limit
        return (new_width, new_height)


def create_shrink_size_calculator(size, limit):
    return ShrinkSizeCalculator(size, limit)
