from argparse import Namespace
from .. import QueryOptions

def fromNamespace(args: Namespace) -> QueryOptions:
    options = QueryOptions()
    args_dict = args.__dict__

    options.audio_providers = args_dict.get("audio_providers")
    options.bitrate = args_dict.get("bitrate")
    options.check_for_updates = args_dict.get("check_for_updates")
    options.config = args_dict.get("config")
    options.download_ffmpeg = args_dict.get("download_ffmpeg")
    options.ffmpeg = args_dict.get("ffmpeg")
    options.ffmpeg_args = args_dict.get("ffmpeg_args")
    options.filter_results = args_dict.get("filter_results")
    options.format = args_dict.get("format")
    options.generate_config = args_dict.get("generate_config")
    options.headless = args_dict.get("headless")
    options.log_level = args_dict.get("log_level")
    options.lyrics_providers = args_dict.get("lyrics_providers")
    options.m3u = args_dict.get("m3u")
    options.operation = args_dict.get("operation")
    options.output = args_dict.get("output")
    options.overwrite = args_dict.get("overwrite")
    options.print_errors = args_dict.get("print_errors")
    options.profile = args_dict.get("profile")
    options.query = args_dict.get("query")
    options.restrict = args_dict.get("restrict")
    options.save_file = args_dict.get("save_file")
    options.search_query = args_dict.get("search_query")
    options.simple_tui = args_dict.get("simple_tui")
    options.sponsor_block = args_dict.get("sponsor_block")
    options.threads = args_dict.get("threads")

    return options