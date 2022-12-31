from typing import List
from dataclasses import dataclass


@dataclass
class YoutubeMusicResult:
    name: str
    type: str
    link: str
    album: str
    duration: int
    artists: str
    artist_list: List[str]