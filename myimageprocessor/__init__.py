import myimageprocessor.parser as p
import myimageprocessor.path_handler as ph
import myimageprocessor.resize as r

SHRINK_SIZE = 300


def main(shrink_size=SHRINK_SIZE):
    args = p.parse_args()
    path_pair = ph.create_path_pair(args.source, args.source.name)
    targets = path_pair.list_targets()
    for target_pair in targets:
        processor = r.create_shrink_processor(target_pair, shrink_size)
        processor.process()


if __name__ == "__main__":
    main()
