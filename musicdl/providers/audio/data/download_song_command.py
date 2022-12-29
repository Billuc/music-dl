from dataclasses import dataclass

from musicdl.common import Song


@dataclass
class DownloadSongCommand:
    song: Song
    search_query: str
    filter_results: bool
    