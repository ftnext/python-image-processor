from dataclasses import dataclass
from typing import Tuple


@dataclass
class ResizeCalculator:
    _now: Tuple[int, int]
    _limit: int

    def needs_resize(self):
        width, _ = self._now
        return width > self._limit
