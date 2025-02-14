from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import myimageprocessor.path_handler as ph


class SourceDestinationPairTestCase(TestCase):
    def setUp(self):
        self.source_path = MagicMock(spec=Path)
        self.destination_path = MagicMock(spec=Path)
        self.pair = ph.SourceDestinationPair(
            self.source_path, self.destination_path
        )

    def test_init(self):
        actual = ph.SourceDestinationPair(
            self.source_path, self.destination_path
        )
        self.assertEqual(actual._source, self.source_path)
        self.assertEqual(actual._destination, self.destination_path)

    def test_source_property(self):
        actual = self.pair.source
        self.assertEqual(actual, self.source_path)

    def test_destination_property(self):
        actual = self.pair.destination
        self.assertEqual(actual, self.destination_path)


class CreateSourceDestinationPairTestCase(TestCase):
    @patch(
        "myimageprocessor.path_handler.SourceDestinationPair.__init__",
        return_value=None,
    )
    def test(self, init_mock):
        source, destination = MagicMock(spec=Path), MagicMock(spec=Path)
        actual = ph.create_source_destination_pair(source, destination)
        self.assertEqual(init_mock.call_args_list, [call(source, destination)])
        self.assertIsInstance(actual, ph.SourceDestinationPair)


class SourceDestinationListTestCase(TestCase):
    def setUp(self):
        self.pair0 = MagicMock(spec=ph.SourceDestinationPair)
        self.pair1 = MagicMock(spec=ph.SourceDestinationPair)
        self.source_destination_pairs = [self.pair0, self.pair1]

    def test_init(self):
        actual = ph.SourceDestinationList(self.source_destination_pairs)
        self.assertEqual(actual._pairs, self.source_destination_pairs)

    def test_iter(self):
        source_destination_list = ph.SourceDestinationList(
            self.source_destination_pairs
        )
        actual = [pair for pair in source_destination_list]
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0], self.pair0)
        self.assertEqual(actual[1], self.pair1)


class CreateSourceDestinationListTestCase(TestCase):
    @patch(
        "myimageprocessor.path_handler.SourceDestinationList.__init__",
        return_value=None,
    )
    def test(self, init_mock):
        source_destination_pairs = [
            MagicMock(spec=ph.SourceDestinationPair),
            MagicMock(spec=ph.SourceDestinationPair),
        ]
        actual = ph.create_source_destination_list(source_destination_pairs)
        self.assertEqual(
            init_mock.call_args_list, [call(source_destination_pairs)]
        )
        self.assertIsInstance(actual, ph.SourceDestinationList)


class PathPairTestCase(TestCase):
    def setUp(self):
        self.source, self.destination = (
            MagicMock(spec=Path),
            MagicMock(spec=Path),
        )

    def test_init(self):
        actual = ph.PathPair(self.source, self.destination)
        self.assertEqual(actual._source, self.source)
        self.assertEqual(actual._destination, self.destination)

    @patch("myimageprocessor.path_handler.create_source_destination_list")
    @patch("myimageprocessor.path_handler.create_source_destination_pair")
    def test_list_targets(
        self, create_source_destination_pair, create_source_destination_list
    ):
        path_pair = ph.PathPair(self.source, self.destination)
        source_destination_pair = create_source_destination_pair.return_value

        actual = path_pair.list_targets()
        self.assertEqual(
            create_source_destination_pair.call_args_list,
            [call(self.source, self.destination)],
        )
        self.assertEqual(
            create_source_destination_list.call_args_list,
            [call([source_destination_pair])],
        )
        self.assertEqual(actual, create_source_destination_list.return_value)


class CreatePathPairTestCase(TestCase):
    @patch(
        "myimageprocessor.path_handler.PathPair.__init__", return_value=None
    )
    def test(self, init_mock):
        source, destination = MagicMock(spec=Path), MagicMock(spec=Path)
        actual = ph.create_path_pair(source, destination)
        self.assertEqual(init_mock.call_args_list, [call(source, destination)])
        self.assertIsInstance(actual, ph.PathPair)
