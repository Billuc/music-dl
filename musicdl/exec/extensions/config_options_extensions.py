from typing import Any, Dict

from musicdl.exec.data import ConfigOptions


def generate_config_options(dict: Dict[str, Any]) -> ConfigOptions:
    audio_providers = dict.get("audio_providers")
    bitrate = dict.get("bitrate")
    cache_path = dict.get("cache_path")
    client_id = dict.get("client_id")
    client_secret = dict.get("client_secret")
    cookie_file = dict.get("cookie_file")
    ffmpeg = dict.get("ffmpeg")
    ffmpeg_args = dict.get("ffmpeg_args")
    filter_results = dict.get("filter_results")
    format = dict.get("format")
    headless = dict.get("headless")
    load_config = dict.get("load_config")
    log_level = dict.get("log_level")
    lyrics_providers = dict.get("lyrics_providers")
    m3u = dict.get("m3u")
    no_cache = dict.get("no_cache")
    output = dict.get("output")
    overwrite = dict.get("overwrite")
    preload = dict.get("preload")
    print_errors = dict.get("print_errors")
    restrict = dict.get("restrict")
    save_file = dict.get("save_file")
    search_query = dict.get("search_query")
    simple_tui = dict.get("simple_tui")
    sponsor_block = dict.get("sponsor_block")
    threads = dict.get("threads")
    user_auth = dict.get("user_auth")

    options = ConfigOptions(
        load_config,  # type: ignore
        log_level,  # type: ignore
        simple_tui,  # type: ignore
        cache_path,  # type: ignore
        audio_providers,  # type: ignore
        lyrics_providers,  # type: ignore
        ffmpeg,  # type: ignore
        bitrate,  # type: ignore
        ffmpeg_args,  # type: ignore
        format,  # type: ignore
        save_file,  # type: ignore
        m3u,  # type: ignore
        output,  # type: ignore
        overwrite,  # type: ignore
        client_id,  # type: ignore
        client_secret,  # type: ignore
        user_auth,  # type: ignore
        search_query,  # type: ignore
        filter_results,  # type: ignore
        threads,  # type: ignore
        no_cache,  # type: ignore
        cookie_file,  # type: ignore
        headless,  # type: ignore
        restrict,  # type: ignore
        print_errors,  # type: ignore
        sponsor_block,  # type: ignore
        preload,  # type: ignore
    )

    return options
