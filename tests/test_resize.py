from unittest import TestCase

import myimageprocessor.resize as r


class ResizeCalculatorTestCase(TestCase):
    def setUp(self):
        self.limit = 300

    def test_init(self):
        size = (400, 600)
        actual = r.ResizeCalculator(size, self.limit)
        self.assertEqual(actual._now, (400, 600))
        self.assertEqual(actual._limit, 300)

    def test_needs_resize(self):
        size = (600, 400)
        resize_calculator = r.ResizeCalculator(size, self.limit)
        actual = resize_calculator.needs_resize()
        self.assertTrue(actual)
