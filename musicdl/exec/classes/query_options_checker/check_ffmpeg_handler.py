from kink import inject
from musicdl.common import MusicDLException, BaseFfmpegHelper, BaseResponsibilityChainLink
from musicdl.exec.data import QueryOptions

@inject
class CheckFFMpegHandler(BaseResponsibilityChainLink[QueryOptions]):
    _ffmpegHelper: BaseFfmpegHelper

    def __init__(self, ffmpegHelper: BaseFfmpegHelper) -> None:
        self._ffmpegHelper = ffmpegHelper

    
    def exec(self, options: QueryOptions) -> bool:
        if not self._ffmpegHelper.check_installed(options.ffmpeg):
            raise MusicDLException(
                "FFmpeg not found. Please run `musicdl --download-ffmpeg` to install it, "
                "or `musicdl --ffmpeg /path/to/ffmpeg` to specify the path to ffmpeg."
            )

        return False