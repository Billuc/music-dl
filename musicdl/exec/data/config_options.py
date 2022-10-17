
from dataclasses import dataclass
from typing import List


@dataclass
class ConfigOptions:
    """
    ConfigOptions class. Contains all the options that could be set in the config file.
    """

    load_config: bool
    log_level: str
    simple_tui: bool
    cache_path: str
    audio_providers: List[str]
    lyrics_providers: List[str]
    ffmpeg: str
    bitrate: bool
    ffmpeg_args: str
    format: str
    save_file: str
    m3u: None
    output: str
    overwrite: str
    client_id: str
    client_secret: str
    user_auth: bool
    search_query: str
    filter_results: bool
    threads: int
    no_cache: bool
    cookie_file: str
    headless: bool
    restrict: bool
    print_errors: bool
    sponsor_block: bool
    preload: bool
    