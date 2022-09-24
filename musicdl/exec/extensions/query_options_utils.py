from argparse import Namespace

from musicdl.commands import CommandOptions
from musicdl.exec.classes import QueryOptions

def from_namespace(args: Namespace) -> QueryOptions:
    options = QueryOptions()
    args_dict = args.__dict__

    options.audio_providers = args_dict.get("audio_providers")
    options.bitrate = args_dict.get("bitrate")
    options.check_for_updates = args_dict.get("check_for_updates")
    options.no_config = args_dict.get("no_config")
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


def to_command_options(opts: QueryOptions) -> CommandOptions:
    command_opts = CommandOptions()

    command_opts.audio_providers = opts.audio_providers
    command_opts.bitrate = opts.bitrate
    command_opts.ffmpeg = opts.ffmpeg
    command_opts.ffmpeg_args = opts.ffmpeg_args
    command_opts.filter_results = opts.filter_results
    command_opts.format = opts.format
    command_opts.headless = opts.headless
    command_opts.log_level = opts.log_level
    command_opts.lyrics_providers = opts.lyrics_providers
    command_opts.m3u = opts.m3u
    command_opts.output = opts.output
    command_opts.overwrite = opts.overwrite
    command_opts.print_errors = opts.print_errors
    command_opts.query = opts.query
    command_opts.restrict = opts.restrict
    command_opts.search_query = opts.search_query
    command_opts.simple_tui = opts.simple_tui
    command_opts.sponsor_block = opts.sponsor_block
    command_opts.threads = opts.threads

    return command_opts


def has_special_args(opts: QueryOptions) -> bool:
    return (
        opts.download_ffmpeg is True
        or opts.generate_config is True
        or opts.check_for_updates is True
    )


