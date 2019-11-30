from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import myimageprocessor.resize as r


class ShrinkSizeCalculatorTestCase(TestCase):
    def setUp(self):
        self.limit = 300

    def test_init(self):
        size = (400, 600)
        actual = r.ShrinkSizeCalculator(size, self.limit)
        self.assertEqual(actual._now, (400, 600))
        self.assertEqual(actual._limit, 300)

    def test_needs_shrink(self):
        """Case of width > limit and height > limit"""
        size = (600, 400)
        shrink_size_calculator = r.ShrinkSizeCalculator(size, self.limit)
        actual = shrink_size_calculator.needs_shrink()
        self.assertTrue(actual)

    def test_needs_shrink_width_smaller(self):
        """Case of width < limit (< height)"""
        size = (299, 500)
        shrink_size_calculator = r.ShrinkSizeCalculator(size, self.limit)
        actual = shrink_size_calculator.needs_shrink()
        self.assertFalse(actual)

    def test_needs_shrink_height_smaller(self):
        """Case of height < limit (< width)"""
        size = (400, 250)
        shrink_size_calculator = r.ShrinkSizeCalculator(size, self.limit)
        actual = shrink_size_calculator.needs_shrink()
        self.assertFalse(actual)

    def test_needs_shrink_boundary(self):
        """Case of height == limit < width"""
        size = (301, 300)
        shrink_size_calculator = r.ShrinkSizeCalculator(size, self.limit)
        actual = shrink_size_calculator.needs_shrink()
        self.assertFalse(actual)

    def test_shrink_size(self):
        size = (600, 400)
        limit = 300
        shrink_size_calculator = r.ShrinkSizeCalculator(size, limit)
        actual = shrink_size_calculator.shrink_size()
        self.assertEqual(actual, (300, 200))

    def test_shrink_size_check_int(self):
        """intで返っていることを確認する

        (400 / 700) * 500 = 285.71
        四捨五入でなく、intによる切り捨てで285となる
        """
        size = (500, 700)
        limit = 400
        shrink_size_calculator = r.ShrinkSizeCalculator(size, limit)
        actual = shrink_size_calculator.shrink_size()
        self.assertEqual(actual, (285, 400))


class CreateShrinkSizeCalculatorTestCase(TestCase):
    @patch(
        "myimageprocessor.resize.ShrinkSizeCalculator.__init__",
        return_value=None,
    )
    def test(self, init_mock):
        size, limit = MagicMock(spec=tuple), MagicMock(spec=int)
        actual = r.create_shrink_size_calculator(size, limit)
        self.assertIsInstance(actual, r.ShrinkSizeCalculator)
        self.assertEqual(init_mock.call_args_list, [call(size, limit)])


class ShrinkProcessorTestCase(TestCase):
    def setUp(self):
        self.shrink_size = MagicMock(spec=int)

    def test_init(self):
        source_destination_file_pair = MagicMock(spec=tuple)
        actual = r.ShrinkProcessor(
            source_destination_file_pair, self.shrink_size
        )
        self.assertEqual(
            actual._source_destination_pair, source_destination_file_pair
        )
        self.assertEqual(actual._shrink_size, self.shrink_size)

    @patch("myimageprocessor.resize.create_shrink_size_calculator")
    @patch("myimageprocessor.resize.Image.open")
    def test_process(self, image_open, create_shrink_size_calculator):
        source_file_path = MagicMock(spec=Path)
        destination_file_path = MagicMock(spec=Path)
        source_destination_file_pair = (
            source_file_path,
            destination_file_path,
        )
        image = image_open.return_value
        shrink_size_calculator = create_shrink_size_calculator.return_value
        shrink_size_calculator.needs_shrink.return_value = True
        shrinked_size = shrink_size_calculator.shrink_size.return_value
        resized_image = image.resize.return_value

        shrink_processor = r.ShrinkProcessor(
            source_destination_file_pair, self.shrink_size
        )
        shrink_processor.process()

        self.assertEqual(image_open.call_args_list, [call(source_file_path)])
        self.assertEqual(
            create_shrink_size_calculator.call_args_list,
            [call(image.size, self.shrink_size)],
        )
        self.assertEqual(
            shrink_size_calculator.needs_shrink.call_args_list, [call()]
        )
        self.assertEqual(
            shrink_size_calculator.shrink_size.call_args_list, [call()]
        )
        self.assertEqual(image.resize.call_args_list, [call(shrinked_size)])
        self.assertEqual(
            resized_image.save.call_args_list, [call(destination_file_path)]
        )


class CreateShrinkProcessor(TestCase):
    @patch(
        "myimageprocessor.resize.ShrinkProcessor.__init__", return_value=None
    )
    def test_init(self, init_mock):
        source_destination_pair = MagicMock(spec=tuple)
        shrink_size = MagicMock(spec=int)
        actual = r.create_shrink_processor(
            source_destination_pair, shrink_size
        )
        self.assertIsInstance(actual, r.ShrinkProcessor)
        self.assertEqual(
            init_mock.call_args_list,
            [call(source_destination_pair, shrink_size)],
        )
