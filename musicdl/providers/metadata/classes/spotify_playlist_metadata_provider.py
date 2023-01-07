
from typing import Callable, Dict, Any
from spotipy import Spotify
from kink import inject

from musicdl.common import BasePipelineMiddleware, MusicDLException, BaseSpotifyClientProvider, SongList, Playlist
from musicdl.providers.metadata.utils import create_song


@inject
class SpotifyPlaylistMetadataProvider(BasePipelineMiddleware[str, SongList]):
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
        
        if "open.spotify.com" not in query or "playlist" not in query:
            return None

        playlist = self._get_playlist_metadata(query)
        return playlist
    
    
    def _get_playlist_metadata(self, url: str) -> Playlist:
        playlist_metadata = self._spotifyClient.playlist(url)
        if playlist_metadata is None:
            raise MusicDLException("Couldn't get metadata, check if you have passed correct playlist url")
        
        playlist_tracks = self._spotifyClient.playlist_items(url)
        if playlist_tracks is None:
            raise MusicDLException(f"Wrong playlist id: {url}")
        
        tracks = playlist_tracks["items"]
        
        # Get all tracks from playlist
        while playlist_tracks["next"]:
            playlist_tracks = self._spotifyClient.next(playlist_tracks)

            # Failed to get response, break the loop
            if playlist_tracks is None:
                break

            # Add tracks to the list
            tracks.extend(playlist_tracks["items"])
        
        urls = [
            track["track"]["external_urls"]["spotify"]
            for track in tracks
            if track is not None
            and track.get("track") is not None
            and track.get("track").get("id")
        ]
        
        songs = [create_song(self._spotifyClient, url) for url in urls]

        return Playlist(
            playlist_metadata["name"], 
            url, 
            urls, 
            songs, 
            playlist_metadata["description"],
            playlist_metadata["external_urls"]["spotify"],
            playlist_metadata["owner"]["display_name"]
        )
        