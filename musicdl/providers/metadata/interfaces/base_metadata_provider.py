import abc
from typing import Optional

from musicdl.common import SongList, BasePipeline



class BaseMetadataProvider(BasePipeline[str, SongList]):
    def __init__(self) -> None:
        super().__init__()
