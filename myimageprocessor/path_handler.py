from dataclasses import dataclass
from pathlib import Path


@dataclass
class SourceDestinationPair:
    _source: Path
    _destination: Path
