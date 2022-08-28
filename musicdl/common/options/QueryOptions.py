from dataclasses import dataclass
from typing import List, Optional


@dataclass()
class QueryOptions:
    """
    QueryOptions class. Contains all the options set in the query.
    """

    operation: Optional[str]
    query: Optional[List[str]]
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
    download_ffmpeg: bool
    generate_config: bool
    check_for_updates: bool
    profile: bool
    version: bool


    def has_special_args(self):
        return (
            self.download_ffmpeg is True or 
            self.generate_config is True or
            self.check_for_updates is True or
            self.version is True
        )

