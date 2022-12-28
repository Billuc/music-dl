
from typing import Callable, Dict, Any
from spotipy import Spotify
from kink import inject

from musicdl.common import BasePipelineMiddleware, MusicDLException
from musicdl.common.classes import SpotifyClientProvider
from musicdl.common.data import SongList, Song, Album
from musicdl.providers.metadata.utils import create_song


@inject
class SpotifyAlbumMetadataProvider(BasePipelineMiddleware[str, SongList]):
    _spotifyClient: Spotify
    
    def __init__(
        self,
        spotify_client_provider: SpotifyClientProvider
    ):
        self._spotifyClient = spotify_client_provider.get_client()
        
    
    def exec(self, query: str, next: Callable[[str], SongList]) -> SongList:
        songlist = next(query)
        if songlist is not None:
            return songlist
        
        if "open.spotify.com" not in query or "album" not in query:
            return None

        album = self._get_album_metadata(query)
        return album
    
    
    def _get_album_metadata(self, url: str) -> Album:
        album_metadata = self._spotifyClient.album(url)
        if album_metadata is None:
            raise MusicDLException("Couldn't get metadata, check if you have passed correct album id")
        
        album_tracks = self._spotifyClient.album_tracks(url)
        if album_tracks is None:
            raise MusicDLException("Couldn't get metadata, check if you have passed correct album id")

        tracks = album_tracks["items"]

        # Get all tracks from album
        while album_tracks["next"]:
            # If there is a next page, go to next page
            album_tracks = self._spotifyClient.next(album_tracks)

            # Failed to get response, break the loop
            if album_tracks is None:
                break

            tracks.extend(album_tracks["items"])

        if album_tracks is None:
            raise MusicDLException(f"Failed to get album response: {url}")
        
        urls = [
            track["external_urls"]["spotify"]
            for track in tracks
            if track is not None and track.get("id")
        ]
        
        songs = [create_song(self._spotifyClient, url) for url in urls]

        return Album(album_metadata["name"], url, urls, songs, album_metadata["artist"][0])
        