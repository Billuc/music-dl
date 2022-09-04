import json

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

from musicdl.downloader.classes.SongList import SongList



@dataclass()
class CommandOptions:
    """
    CommandOptions class. Contains all the options necessary to execute commands.
    """

    query: List[str]
    audio_providers: List[str]
    lyrics_providers: List[str]
    config: bool
    search_query: bool
    filter_results: bool
    ffmpeg: str
    threads: int
    bitrate: str
    ffmpeg_args: str
    format: str
    save_file: str
    output: str
    m3u: str
    overwrite: str
    restrict: bool
    print_errors: bool
    sponsor_block: bool
    log_level: bool
    simple_tui: bool
    headless: bool

