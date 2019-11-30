from unittest import TestCase

import myimageprocessor.resize as r


class ResizeCalculatorTestCase(TestCase):
    def test_init(self):
        size = (400, 600)
        limit = 300
        actual = r.ResizeCalculator(size, limit)
        self.assertEqual(actual._now, (400, 600))
        self.assertEqual(actual._limit, 300)
