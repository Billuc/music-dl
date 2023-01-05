from logging import Logger
from typing import Optional
from yt_dlp import YoutubeDL
from kink import inject

from musicdl.common.consts import TEMP_PATH
from musicdl.common.exceptions import MusicDLException
from musicdl.common.interfaces import BaseYoutubeDLClientProvider


@inject
class YoutubeDLClientProvider(BaseYoutubeDLClientProvider):
    _youtubedl: YoutubeDL
    _logger: Logger
    
    
    def __init__(
        self,
        logger: Logger    
    ) -> None:
        self._youtubedl = None
    
    
    def init(
        self,
        output_format: str = "mp3",
        cookie_file: Optional[str] = None
    ) -> None:
        if output_format == "m4a":
            ytdl_format = "bestaudio[ext=m4a]/bestaudio/best"
        elif output_format == "opus":
            ytdl_format = "bestaudio[ext=webm]/bestaudio/best"
        else:
            ytdl_format = "bestaudio"

        self.audio_handler = YoutubeDL(
            {
                "format": ytdl_format,
                "quiet": True,
                "no_warnings": True,
                "encoding": "UTF-8",
                "logger": self._logger,
                "cookiefile": cookie_file,
                "outtmpl": f"{TEMP_PATH}/%(id)s.%(ext)s",
                "retries": 5,
            }
        )
        
        
    def get_client(self):
        if self._youtubedl is None:
            raise MusicDLException("Client has not been initialized. Use YoutubeDLClientProvider.init first !")
        
        return self._youtubedl
        
    