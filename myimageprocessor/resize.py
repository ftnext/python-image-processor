from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from PIL import Image


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


@dataclass
class ShrinkProcessor:
    _source_destination_pair: Tuple[Path, Path]
    _shrink_size: int

    def process(self):
        source_path, destination_path = self._source_destination_pair
        image = Image.open(source_path)
        shrink_size_calculator = create_shrink_size_calculator(
            image.size, self._shrink_size
        )
        if shrink_size_calculator.needs_shrink():
            shrinked_size = shrink_size_calculator.shrink_size()
            resized_image = image.resize(shrinked_size)
            resized_image.save(destination_path)
