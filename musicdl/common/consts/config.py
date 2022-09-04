import os
from pathlib import Path


MUSICDL_PATH: Path = Path(os.path.expanduser("~"), ".musicdl")
CONFIG_PATH: Path = MUSICDL_PATH / "config.json"
CACHE_PATH: Path = MUSICDL_PATH / ".spotipy"
TEMP_PATH: Path = MUSICDL_PATH / "temp"
ERRORS_PATH: Path = MUSICDL_PATH / "errors"
LOG_PATH: Path = MUSICDL_PATH / "debug.log"


DEFAULT_CONFIG = {
    "load_config": True,
    "log_level": "INFO",
    "simple_tui": False,
    "cache_path": str(CACHE_PATH),
    "audio_providers": ["youtube-music"],
    "lyrics_providers": ["musixmatch", "genius"],
    "ffmpeg": "ffmpeg",
    "bitrate": None,
    "ffmpeg_args": None,
    "format": "mp3",
    "save_file": None,
    "m3u": None,
    "output": "{artists} - {title}.{output-ext}",
    "overwrite": "skip",
    "client_id": "5f573c9620494bae87890c0f08a60293",
    "client_secret": "212476d9b0f3472eaa762d90b19b0ba8",
    "user_auth": False,
    "search_query": None,
    "filter_results": True,
    "threads": 4,
    "no_cache": False,
    "cookie_file": None,
    "headless": False,
    "restrict": False,
    "print_errors": False,
    "sponsor_block": False,
    "preload": False,
}