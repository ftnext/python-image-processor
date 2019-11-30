from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SourceDestinationPair:
    _source: Path
    _destination: Path


def create_source_destination_pair(source, destination):
    return SourceDestinationPair(source, destination)


@dataclass
class SourceDestinationList:
    _pairs: List[SourceDestinationPair]


def create_source_destination_list(pairs):
    return SourceDestinationList(pairs)


@dataclass
class PathPair:
    _source: Path  # ファイルまたはディレクトリを指す
    _destination: Path  # ファイルまたはディレクトリを指す

    def list_targets(self):
        pair = create_source_destination_pair(self._source, self._destination)
        return create_source_destination_list([pair])
