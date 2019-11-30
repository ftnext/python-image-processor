from pathlib import Path
from unittest import TestCase
from unittest.mock import call, MagicMock, patch

import myimageprocessor.path_handler as ph


class SourceDestinationPairTestCase(TestCase):
    def test_init(self):
        source_path = MagicMock(spec=Path)
        destination_path = MagicMock(spec=Path)
        actual = ph.SourceDestinationPair(source_path, destination_path)
        self.assertEqual(actual._source, source_path)
        self.assertEqual(actual._destination, destination_path)


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
    def test_init(self):
        source_destination_pairs = [
            MagicMock(spec=ph.SourceDestinationPair),
            MagicMock(spec=ph.SourceDestinationPair),
        ]
        actual = ph.SourceDestinationList(source_destination_pairs)
        self.assertEqual(actual._pairs, source_destination_pairs)


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
    def test_init(self):
        source, destination = MagicMock(spec=Path), MagicMock(spec=Path)
        actual = ph.PathPair(source, destination)
        self.assertEqual(actual._source, source)
        self.assertEqual(actual._destination, destination)
