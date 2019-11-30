from pathlib import Path
import sys
from unittest import TestCase

import myimageprocessor.parser as p


class ParseArgsTestCase(TestCase):
    def test(self):
        sys.argv = [
            "myimageprocessor/main.py",
            "picture/test.jpg",
        ]
        actual = p.parse_args()
        self.assertIsInstance(actual.source, Path)
        self.assertEqual(str(actual.source), "picture/test.jpg")
