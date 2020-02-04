from pathlib import Path

import myimageprocessor.parser as p
import myimageprocessor.path_handler as ph
import myimageprocessor.resize as r

SHRINK_SIZE = 300


def main(shrink_size=SHRINK_SIZE):
    args = p.parse_args()
    destination = Path.cwd()
    path_pair = ph.create_path_pair(args.source, destination)
    targets = path_pair.list_targets()
    processor = r.create_shrink_processor(shrink_size)
    processor.process(targets)


if __name__ == "__main__":
    main()
