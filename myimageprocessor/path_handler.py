from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SourceDestinationPair:
    _source: Path
    _destination: Path


@dataclass
class SourceDestinationList:
    _pairs: List[SourceDestinationPair]
