from typing import Any, Dict

from musicdl.exec.classes import ConfigOptions


def from_dict(dict: Dict[str, Any]) -> ConfigOptions:
    options = ConfigOptions()

    options.audio_providers = dict.get("audio_providers")
    options.bitrate = dict.get("bitrate")
    options.cache_path = dict.get("cache_path")
    options.client_id = dict.get("client_id")
    options.client_secret = dict.get("client_secret")
    options.cookie_file = dict.get("cookie_file")
    options.ffmpeg = dict.get("ffmpeg")
    options.ffmpeg_args = dict.get("ffmpeg_args")
    options.filter_results = dict.get("filter_results")
    options.format = dict.get("format")
    options.headless = dict.get("headless")
    options.load_config = dict.get("load_config")
    options.log_level = dict.get("log_level")
    options.lyrics_providers = dict.get("lyrics_providers")
    options.m3u = dict.get("m3u")
    options.no_cache = dict.get("no_cache")
    options.output = dict.get("output")
    options.overwrite = dict.get("overwrite")
    options.preload = dict.get("preload")
    options.print_errors = dict.get("print_errors")
    options.restrict = dict.get("restrict")
    options.save_file = dict.get("save_file")
    options.search_query = dict.get("search_query")
    options.simple_tui = dict.get("simple_tui")
    options.sponsor_block = dict.get("sponsor_block")
    options.threads = dict.get("threads")
    options.user_auth = dict.get("user_auth")

    return options