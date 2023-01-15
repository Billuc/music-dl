from musicdl.common import BaseResponsibilityChain
from musicdl.downloader.data import EmbedMetadataCommand


class BaseMetadataEmbedder(BaseResponsibilityChain[EmbedMetadataCommand]):
    def __init__(self) -> None:
        super().__init__()
