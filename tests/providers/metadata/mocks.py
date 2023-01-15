from spotipy import Spotify
from typing import Optional
from musicdl.common import BaseSpotifyClientProvider

class MockSpotify(Spotify):
    MOCK_TRACK = {
        "artists": [
            { "id": "artist_1_id", "name": "Artist 1" },    
            { "id": "artist_2_id", "name": "Artist 2" },    
        ],
        "album": { "id": "album_id" },
        "name": "song_name",
        "disc_number": 2,
        "duration_ms": 40000,
        "track_number": 8,
        "id": "song_id",
        "explicit": False,
        "external_urls": { "spotify": "spotify_song_url" }
    }
    
    MOCK_ALBUM = {
        "name": "album_name",
        "artists": [
            { "name": "Artist 1" }
        ],
        "copyrights": [
            { "text": "copyright_text" }
        ],
        "genres": ["genre_1"],
        "release_date": "2000-01-01",
        "total_tracks": 15,
        "label": "album_label",
        "images": [
            { "width": 120, "height": 120, "url": "image_url_120_x_120" },
            { "width": 240, "height": 240, "url": "image_url_240_x_240" },
            { "width": 360, "height": 360, "url": "image_url_360_x_360" },
            { "width": 480, "height": 480, "url": "image_url_480_x_480" }
        ],
        "tracks": {
            "items": [
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 1 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
                { "disc_number": 2 },
            ]
        }
    }
    
    MOCK_ARTIST = {
        "genres": [ "genre_1", "genre_2" ]
    }
    
    def artist(self, artist_id):
        return self.MOCK_ARTIST
    
    def album(self, album_id):
        return self.MOCK_ALBUM
    
    def track(self, track_id, market=None):
        return self.MOCK_TRACK
    
class MockSpotifyClientProvider(BaseSpotifyClientProvider):
    def init(self, client_id: str, client_secret: str, user_auth: bool = False, cache_path: Optional[str] = None, no_cache: bool = False, open_browser: bool = True) -> None:
        pass
    
    def get_client(self) -> Spotify:
        return MockSpotify()