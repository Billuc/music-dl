from logging import Logger
from kink import inject

from musicdl.commands.interfaces import BaseCommand
from musicdl.commands.classes import CommandOptions
from musicdl.common import is_ffmpeg_installed, get_local_ffmpeg, download_ffmpeg



@inject
class DownloadFFMPEGCommand(BaseCommand):
    _logger: Logger
    
    def __init__(self, logger: Logger):
        self._logger = logger


    def exec(self, options: CommandOptions) -> None:
        """
        Executes a command : Download FFMpeg

        ### Arguments
        - options: The command options.
        """

        if is_ffmpeg_installed():
            self._logger.debug("FFmpeg already installed")
            overwrite_ffmpeg = input(
                "FFmpeg is already installed. Do you want to overwrite it? (y/N): "
            )

            if overwrite_ffmpeg.lower() != "y":
                return None
        
        self._download_and_check_ffmpeg()
        return None


    def _download_and_check_ffmpeg(self):
        self._logger.info("Downloading FFmpeg...")
        download_ffmpeg()

        if get_local_ffmpeg().is_file():
            self._logger.info(f"FFmpeg successfully downloaded to {get_local_ffmpeg().absolute()}")
        else:
            self._logger.error("FFmpeg download failed")




