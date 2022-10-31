
from dataclasses import dataclass
from typing import List

from musicdl.common import LoggingLevel


@dataclass
class DownloaderSettings:
    """
    CommandOptions class. Contains all the options necessary to execute commands.
    """

    query: List[str]
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
    log_level: LoggingLevel
    simple_tui: bool
    headless: bool