from logging import Logger
from kink import inject

from musicdl.commands.data import CommandOptions, AllowedOperations
from musicdl.common import BaseFfmpegHelper, BaseResponsibilityChainLink



@inject
class DownloadFFMPEGCommand(BaseResponsibilityChainLink[CommandOptions]):
    _logger: Logger
    _ffmpeg_helper: BaseFfmpegHelper
    
    def __init__(self, logger: Logger, ffmpeg_helper: BaseFfmpegHelper):
        self._logger = logger
        self._ffmpeg_helper = ffmpeg_helper


    def exec(self, options: CommandOptions) -> bool:
        if (not options.operation == AllowedOperations.DOWNLOAD_FFMPEG):
            return False

        if self._ffmpeg_helper.check_installed():
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
        self._ffmpeg_helper.download()

        if self._ffmpeg_helper.get_local_path().is_file():
            self._logger.info(f"FFmpeg successfully downloaded to {self._ffmpeg_helper.get_local_path().absolute()}")
        else:
            self._logger.error("FFmpeg download failed")




