from typing import Optional
from spotipy import Spotify
from spotipy.cache_handler import CacheFileHandler, MemoryCacheHandler
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from musicdl.common.consts import CACHE_PATH
from musicdl.common.exceptions import MusicDLException
from musicdl.common.interfaces import BaseSpotifyClientProvider

# TODO : maybe handle cache (didn't understand it for now)
class SpotifyClientProvider(BaseSpotifyClientProvider):
    _spotify: Spotify
    
    
    def __init__(self) -> None:
        self._spotify = None
    
    
    def init(
        self,
        client_id: str,
        client_secret: str,
        user_auth: bool = False,
        cache_path: Optional[str] = None,
        no_cache: bool = False,
        open_browser: bool = True
    ) -> None:
        cache_handler = (
            CacheFileHandler(cache_path or CACHE_PATH)
            if not no_cache
            else MemoryCacheHandler()
        )
        
        # Use SpotifyOAuth as auth manager
        if user_auth:
            credential_manager = SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri="http://127.0.0.1:8080/",
                scope="user-library-read",
                cache_handler=cache_handler,
                open_browser=open_browser,
            )
        # Use SpotifyClientCredentials as auth manager
        else:
            credential_manager = SpotifyClientCredentials(
                client_id=client_id,
                client_secret=client_secret,
                cache_handler=cache_handler,
            )
            
        self._spotify = Spotify(
            auth_manager=credential_manager,
            status_forcelist=(429, 500, 502, 503, 504, 404),
        )
        
        
    def get_client(self):
        if self._spotify is None:
            raise MusicDLException("Client has not been initialized. Use SpotifyClientProvider.init first !")
        
        return self._spotify
        
    