from dataclasses import dataclass
from typing import List

from musicdl.common import Song


@dataclass
class DownloadSongCommand:
    song: Song
    search_query: str
    filter_results: bool
    audio_providers: List[str]
    