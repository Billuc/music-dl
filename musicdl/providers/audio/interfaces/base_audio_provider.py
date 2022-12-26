from musicdl.common import BasePipeline

from musicdl.downloader import Song


class BaseAudioProvider(BasePipeline[Song, Dict]):
    def __init__(self) -> None:
        super().__init__()