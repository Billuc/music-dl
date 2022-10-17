from argparse import Namespace

from musicdl.commands import CommandOptions, AllowedOperations
from musicdl.exec.data import QueryOptions


def from_namespace(args: Namespace) -> QueryOptions:
    args_dict = args.__dict__

    audio_providers = args_dict.get("audio_providers")
    bitrate = args_dict.get("bitrate")
    check_for_updates = args_dict.get("check_for_updates")
    no_config = args_dict.get("no_config")
    download_ffmpeg = args_dict.get("download_ffmpeg")
    ffmpeg = args_dict.get("ffmpeg")
    ffmpeg_args = args_dict.get("ffmpeg_args")
    filter_results = args_dict.get("filter_results")
    format = args_dict.get("format")
    generate_config = args_dict.get("generate_config")
    headless = args_dict.get("headless")
    log_level = args_dict.get("log_level")
    lyrics_providers = args_dict.get("lyrics_providers")
    m3u = args_dict.get("m3u")
    operation = args_dict.get("operation")
    output = args_dict.get("output")
    overwrite = args_dict.get("overwrite")
    print_errors = args_dict.get("print_errors")
    profile = args_dict.get("profile")
    query = args_dict.get("query")
    restrict = args_dict.get("restrict")
    save_file = args_dict.get("save_file")
    search_query = args_dict.get("search_query")
    simple_tui = args_dict.get("simple_tui")
    sponsor_block = args_dict.get("sponsor_block")
    threads = args_dict.get("threads")

    options = QueryOptions(
        operation,
        query,
        audio_providers,
        lyrics_providers,
        no_config,
        search_query,
        filter_results,
        ffmpeg,
        threads,
        bitrate,
        ffmpeg_args,
        format,
        save_file,
        output,
        m3u,
        overwrite,
        restrict,
        print_errors,
        sponsor_block,
        log_level,
        simple_tui,
        headless,
        download_ffmpeg,
        generate_config,
        check_for_updates,
        profile
    )

    return options


def to_command_options(opts: QueryOptions) -> CommandOptions:
    operation = _to_allowed_operation(opts)
    audio_providers = opts.audio_providers
    bitrate = opts.bitrate
    ffmpeg = opts.ffmpeg
    ffmpeg_args = opts.ffmpeg_args
    filter_results = opts.filter_results
    format = opts.format
    headless = opts.headless
    log_level = opts.log_level
    lyrics_providers = opts.lyrics_providers
    m3u = opts.m3u
    output = opts.output
    overwrite = opts.overwrite
    print_errors = opts.print_errors
    query = opts.query
    restrict = opts.restrict
    save_file = opts.save_file
    search_query = opts.search_query
    simple_tui = opts.simple_tui
    sponsor_block = opts.sponsor_block
    threads = opts.threads

    command_opts = CommandOptions(
        operation,
        query,
        audio_providers,
        lyrics_providers,
        search_query,
        filter_results,
        ffmpeg,
        threads,
        bitrate,
        ffmpeg_args,
        format,
        save_file,
        output,
        m3u,
        overwrite,
        restrict,
        print_errors,
        sponsor_block,
        log_level,
        simple_tui,
        headless,
    )

    return command_opts


def has_special_args(opts: QueryOptions) -> bool:
    return (
        opts.download_ffmpeg is True
        or opts.generate_config is True
        or opts.check_for_updates is True
    )


def _to_allowed_operation(options: QueryOptions) -> AllowedOperations:
    if options.check_for_updates:
        return AllowedOperations.CHECK_FOR_UPDATES
    elif options.download_ffmpeg:
        return AllowedOperations.DOWNLOAD_FFMPEG
    elif options.generate_config:
        return AllowedOperations.GENERATE_CONFIG
    else:
        if options.operation == "download":
            return AllowedOperations.DOWNLOAD
        elif options.operation == "save":
            return AllowedOperations.SAVE
        elif options.operation == "sync":
            return AllowedOperations.SYNC
        elif options.operation == "web":
            return AllowedOperations.WEB

    return AllowedOperations.UNKNOWN
