from logging import Logger
from kink import inject

from musicdl.common import BaseResponsibilityChainLink
from musicdl.commands.classes import CommandOptions, AllowedOperations
from musicdl.common import is_ffmpeg_installed, get_local_ffmpeg, download_ffmpeg



@inject
class DownloadFFMPEGCommand(BaseResponsibilityChainLink[CommandOptions]):
    _logger: Logger
    
    def __init__(self, logger: Logger):
        self._logger = logger


    def exec(self, options: CommandOptions) -> bool:
        if (not options.operation == AllowedOperations.DOWNLOAD_FFMPEG):
            return False

        if is_ffmpeg_installed():
            self._logger.debug("FFmpeg already installed")
            overwrite_ffmpeg = input(
                "FFmpeg is already installed. Do you want to overwrite it? (y/N): "
            )

            if overwrite_ffmpeg.lower() != "y":
                return True
        
        self._download_and_check_ffmpeg()
        return True


    def _download_and_check_ffmpeg(self):
        self._logger.info("Downloading FFmpeg...")
        download_ffmpeg()

        if get_local_ffmpeg().is_file():
            self._logger.info(f"FFmpeg successfully downloaded to {get_local_ffmpeg().absolute()}")
        else:
            self._logger.error("FFmpeg download failed")




