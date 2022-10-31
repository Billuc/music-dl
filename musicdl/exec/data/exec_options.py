from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ExecOptions:
    """
    ExecOptions class. Contains all the options set in both the query and the config file.
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

    load_config: bool
    cache_path: str
    client_id: str
    client_secret: str
    user_auth: bool
    no_cache: bool
    cookie_file: str
    preload: bool
