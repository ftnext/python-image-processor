from unittest import TestCase
from unittest.mock import call, MagicMock, patch

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
        """Case of width > limit and height > limit"""
        size = (600, 400)
        resize_calculator = r.ResizeCalculator(size, self.limit)
        actual = resize_calculator.needs_resize()
        self.assertTrue(actual)

    def test_needs_resize_width_smaller(self):
        """Case of width < limit (< height)"""
        size = (299, 500)
        resize_calculator = r.ResizeCalculator(size, self.limit)
        actual = resize_calculator.needs_resize()
        self.assertFalse(actual)

    def test_needs_resize_height_smaller(self):
        """Case of height < limit (< width)"""
        size = (400, 250)
        resize_calculator = r.ResizeCalculator(size, self.limit)
        actual = resize_calculator.needs_resize()
        self.assertFalse(actual)

    def test_needs_resize_boundary(self):
        """Case of height == limit < width"""
        size = (301, 300)
        resize_calculator = r.ResizeCalculator(size, self.limit)
        actual = resize_calculator.needs_resize()
        self.assertFalse(actual)

    def test_shrink_size(self):
        size = (600, 400)
        limit = 300
        resize_calculator = r.ResizeCalculator(size, limit)
        actual = resize_calculator.shrink_size()
        self.assertEqual(actual, (300, 200))

    def test_shrink_size_check_int(self):
        """intで返っていることを確認する
        
        (400 / 700) * 500 = 285.71
        四捨五入でなく、intによる切り捨てで285となる
        """
        size = (500, 700)
        limit = 400
        resize_calculator = r.ResizeCalculator(size, limit)
        actual = resize_calculator.shrink_size()
        self.assertEqual(actual, (285, 400))


class CreateResizeCalculatorTestCase(TestCase):
    @patch(
        "myimageprocessor.resize.ResizeCalculator.__init__", return_value=None
    )
    def test(self, init_mock):
        size, limit = MagicMock(), MagicMock()
        actual = r.create_resize_calculator(size, limit)
        self.assertTrue(isinstance(actual, r.ResizeCalculator))
        self.assertEqual(init_mock.call_args_list, [call(size, limit)])
