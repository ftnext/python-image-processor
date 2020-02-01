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
    def test_list_targets_source_and_destination_are_file(
        self, create_source_destination_pair, create_source_destination_list
    ):
        self.source.is_file.return_value = True
        self.destination.is_dir.return_value = False
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

    @patch("myimageprocessor.path_handler.create_source_destination_list")
    @patch("myimageprocessor.path_handler.create_source_destination_pair")
    def test_list_targets_source_file_destination_directory(
        self, create_source_destination_pair, create_source_destination_list
    ):
        self.source.is_file.return_value = True
        self.destination.is_dir.return_value = True
        path_pair = ph.PathPair(self.source, self.destination)
        source_destination_pair = create_source_destination_pair.return_value

        actual = path_pair.list_targets()

        self.assertEqual(
            create_source_destination_pair.call_args_list,
            [call(self.source, self.destination / self.source.name)],
        )
        self.assertEqual(
            create_source_destination_list.call_args_list,
            [call([source_destination_pair])],
        )
        self.assertEqual(actual, create_source_destination_list.return_value)

    @patch("myimageprocessor.path_handler.create_source_destination_list")
    @patch("myimageprocessor.path_handler.create_source_destination_pair")
    def test_list_targets_source_directory_destination_current_directory(
        self, create_source_destination_pair, create_source_destination_list
    ):
        self.source.is_file.return_value = False
        self.destination.is_dir.return_value = True
        file1, file2, file3 = (
            MagicMock(spec=Path),
            MagicMock(spec=Path),
            MagicMock(spec=Path),
        )
        file2.name.endswith.return_value = False
        self.source.iterdir.return_value = (
            item for item in [file1, file2, file3]
        )
        path_pair = ph.PathPair(self.source, self.destination)

        actual = path_pair.list_targets()

        # TODO: チェックを別の関数に切り出す
        image_extensions = (".jpg", ".png")
        self.assertEqual(
            file1.name.endswith.call_args_list, [call(image_extensions)]
        )
        self.assertEqual(
            file2.name.endswith.call_args_list, [call(image_extensions)]
        )
        self.assertEqual(
            file3.name.endswith.call_args_list, [call(image_extensions)]
        )
        self.assertEqual(
            create_source_destination_pair.call_args_list,
            [
                call(file1, self.destination / file1.name),
                call(file3, self.destination / file3.name),
            ],
        )
        self.assertEqual(
            create_source_destination_list.call_args_list,
            [
                call(
                    [
                        create_source_destination_pair.return_value,
                        create_source_destination_pair.return_value,
                    ]
                )
            ],
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

    @patch("myimageprocessor.path_handler.Path.cwd")
    @patch(
        "myimageprocessor.path_handler.PathPair.__init__", return_value=None
    )
    def test_not_specified_destination(self, init_mock, path_cwd_mock):
        source = MagicMock(spec=Path)
        cwd_path = path_cwd_mock.return_value

        actual = ph.create_path_pair(source)

        self.assertEqual(init_mock.call_args_list, [call(source, cwd_path)])
        self.assertIsInstance(actual, ph.PathPair)
