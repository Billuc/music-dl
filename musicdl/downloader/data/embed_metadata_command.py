from dataclasses import dataclass
from pathlib import Path

from musicdl.common import Song

@dataclass
class EmbedMetadataCommand:
    song: Song
    output_file: Path
    file_format: str
    