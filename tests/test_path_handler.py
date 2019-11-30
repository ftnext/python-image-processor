from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock

import myimageprocessor.path_handler as ph


class SourceDestinationPairTestCase(TestCase):
    def test_init(self):
        source_path = MagicMock(spec=Path)
        destination_path = MagicMock(spec=Path)
        actual = ph.SourceDestinationPair(source_path, destination_path)
        self.assertEqual(actual._source, source_path)
        self.assertEqual(actual._destination, destination_path)
