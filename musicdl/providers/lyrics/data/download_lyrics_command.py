from dataclasses import dataclass
from typing import List

from musicdl.common import Song


@dataclass
class DownloadLyricsCommand():
    song: Song
    lyrics_providers: List[str]
    