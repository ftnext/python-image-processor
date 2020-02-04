from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SourceDestinationPair:
    _source: Path
    _destination: Path

    @property
    def source(self):
        return self._source

    @property
    def destination(self):
        return self._destination


def create_source_destination_pair(source, destination):
    return SourceDestinationPair(source, destination)


@dataclass
class SourceDestinationList:
    _pairs: List[SourceDestinationPair]

    def __iter__(self):
        return iter(self._pairs)


def create_source_destination_list(pairs):
    return SourceDestinationList(pairs)


@dataclass
class PathPair:
    _source: Path  # ファイルまたはディレクトリを指す
    _destination: Path  # ディレクトリを指す（現時点ではカレントディレクトリ）

    def list_targets(self):
        assert self._destination.is_dir()
        if self._source.is_file():
            dest_path = self._destination / self._source.name
            pair = create_source_destination_pair(self._source, dest_path)
            return create_source_destination_list([pair])
        pairs = []
        dest_directory = self._destination / self._source.name
        dest_directory.mkdir(exist_ok=True)
        for source_path in self._source.iterdir():
            if not source_path.name.endswith((".jpg", ".png")):
                continue
            destination_path = dest_directory / source_path.name
            pair = create_source_destination_pair(
                source_path, destination_path
            )
            pairs.append(pair)
        return create_source_destination_list(pairs)


def create_path_pair(source, destination=None):
    if not destination:
        destination = Path.cwd()
    # sourceがディレクトリ、destinationがファイルのとき、エラーを上げる
    return PathPair(source, destination)
