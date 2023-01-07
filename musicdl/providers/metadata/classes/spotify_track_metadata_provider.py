
from typing import Callable, Dict, Any
from spotipy import Spotify
from kink import inject

from musicdl.common import BasePipelineMiddleware, BaseSpotifyClientProvider, SongList
from musicdl.providers.metadata.utils import create_song


@inject
class SpotifyTrackMetadataProvider(BasePipelineMiddleware[str, SongList]):
    _spotifyClient: Spotify
    
    def __init__(
        self,
        spotify_client_provider: BaseSpotifyClientProvider
    ):
        self._spotifyClient = spotify_client_provider.get_client()
        
    
    def exec(self, query: str, next: Callable[[str], SongList]) -> SongList:
        songlist = next(query)
        if songlist is not None:
            return songlist
        
        if "open.spotify.com" not in query or "track" not in query:
            return None

        song = create_song(self._spotifyClient, query)
        return SongList(None, None, [query], [song])
    