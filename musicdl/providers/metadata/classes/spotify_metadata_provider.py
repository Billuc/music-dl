
from typing import Callable
from musicdl.common import BasePipelineMiddleware
from musicdl.common.data.song_list import SongList


class SpotifyMetadataProvider(BasePipelineMiddleware[str, SongList]):
    def exec(self, query: str, next: Callable[[str], SongList]) -> SongList:
        if (notSpotify):
            if (next is None):
                return SongList("", "", [], [])

            return next(query)

        # build SongList
        return None