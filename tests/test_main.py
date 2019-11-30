from unittest import TestCase
from unittest.mock import call, MagicMock, patch

from myimageprocessor import main
import myimageprocessor.path_handler as ph


class MainTestCase(TestCase):
    @patch("myimageprocessor.resize.create_shrink_processor")
    @patch("myimageprocessor.path_handler.create_path_pair")
    @patch("myimageprocessor.parser.parse_args")
    def test(self, parse_args, create_path_pair, create_shrink_processor):
        shrink_size = MagicMock(spec=int)
        pair = MagicMock(spec=ph.SourceDestinationPair)
        args = parse_args.return_value
        path_pair = create_path_pair.return_value
        path_pair.list_targets.return_value = [pair]
        processor = create_shrink_processor.return_value

        main(shrink_size)

        self.assertEqual(parse_args.call_args_list, [call()])
        self.assertEqual(
            create_path_pair.call_args_list,
            [call(args.source, args.source.name)],
        )
        self.assertEqual(path_pair.list_targets.call_args_list, [call()])
        self.assertEqual(
            create_shrink_processor.call_args_list, [call(pair, shrink_size)],
        )
        self.assertEqual(processor.process.call_args_list, [call()])
