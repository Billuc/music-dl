"""
Youtube module for downloading and searching songs.
"""

from typing import Dict
from kink import inject
from typing import Dict, Callable
from yt_dlp import YoutubeDL

from musicdl.common import BasePipelineMiddleware, BaseFormatHelper, MusicDLException, BaseYoutubeDLClientProvider
from musicdl.providers.audio.data import DownloadSongCommand


@inject
class SavedSongAudioProvider(BasePipelineMiddleware[DownloadSongCommand, Dict]):
    _format_helper: BaseFormatHelper
    _youtube_dl_client: YoutubeDL
    
    def __init__(
        self, 
        format_helper: BaseFormatHelper,
        ytdl_client_provider: BaseYoutubeDLClientProvider
    ):
        self._format_helper = format_helper
        self._youtube_dl_client = ytdl_client_provider.get_client()
        
        
    def exec(self, query: DownloadSongCommand, next: Callable[[DownloadSongCommand], Dict]) -> Dict:
        if query.download_url is None:
            return next(query)

        try:
            data = self._youtube_dl_client.extract_info(query.download_url, download=True)
            
            if data:
                return data
        except Exception as exception:
            raise MusicDLException(f"YT-DLP download error - {query.download_url}") from exception
        
        raise MusicDLException(f"No metadata found for the url {query.download_url}")

