from musicdl.common import BaseResponsibilityChain

from musicdl.downloader import Song


class BaseAudioProvider(BaseResponsibilityChain[Song]):
    def __init__(self) -> None:
        super().__init__()