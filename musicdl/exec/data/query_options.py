from dataclasses import dataclass
from typing import List, Optional


@dataclass
class QueryOptions:
    """
    QueryOptions class. Contains all the options set in the query.
    """

    operation: Optional[str]
    query: Optional[List[str]]
    audio_providers: List[str]
    lyrics_providers: List[str]
    no_config: bool
    search_query: str
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
    log_level: str
    simple_tui: bool
    headless: bool
    download_ffmpeg: bool
    generate_config: bool
    check_for_updates: bool
    profile: bool

    def __repr__(self) -> str:
        return f"""QueryOptions[
    operation : {self.operation},
    query : {self.query},
    audio_providers: {self.audio_providers},
    lyrics_providers: {self.lyrics_providers},
    no_config: {self.no_config},
    search_query: {self.search_query},
    filter_results: {self.filter_results},
    ffmpeg: {self.ffmpeg},
    threads: {self.threads},
    bitrate: {self.bitrate},
    ffmpeg_args: {self.ffmpeg_args},
    format: {self.format},
    save_file: {self.save_file},
    output: {self.output},
    m3u: {self.m3u},
    overwrite: {self.overwrite},
    restrict: {self.restrict},
    print_errors: {self.print_errors},
    sponsor_block: {self.sponsor_block},
    log_level: {self.log_level},
    simple_tui: {self.simple_tui},
    headless: {self.headless},
    download_ffmpeg: {self.download_ffmpeg},
    generate_config: {self.generate_config},
    check_for_updates: {self.check_for_updates},
    profile: {self.profile}
]"""
