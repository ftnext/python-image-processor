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
    _destination: Path  # ファイルまたはディレクトリを指す

    def list_targets(self):
        if self._destination.is_dir():
            dest_path = self._destination / self._source.name
            pair = create_source_destination_pair(self._source, dest_path)
            return create_source_destination_list([pair])
        pair = create_source_destination_pair(self._source, self._destination)
        return create_source_destination_list([pair])


def create_path_pair(source, destination=None):
    if not destination:
        destination = Path.cwd()
    # sourceがディレクトリ、destinationがファイルのとき、エラーを上げる
    return PathPair(source, destination)
