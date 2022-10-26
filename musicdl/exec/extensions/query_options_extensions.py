from typing import Any, Dict

from musicdl.commands import CommandOptions, AllowedOperations
from musicdl.common import LoggingLevel
from musicdl.common.consts.logging import DEFAULT_LOGGING_LEVEL
from musicdl.exec.data import QueryOptions


def generate_query_options(args_dict: Dict[str, Any]) -> QueryOptions:
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
        operation,  # type: ignore
        query,  # type: ignore
        audio_providers,  # type: ignore
        lyrics_providers,  # type: ignore
        no_config,  # type: ignore
        search_query,  # type: ignore
        filter_results,  # type: ignore
        ffmpeg,  # type: ignore
        threads,  # type: ignore
        bitrate,  # type: ignore
        ffmpeg_args,  # type: ignore
        format,  # type: ignore
        save_file,  # type: ignore
        output,  # type: ignore
        m3u,  # type: ignore
        overwrite,  # type: ignore
        restrict,  # type: ignore
        print_errors,  # type: ignore
        sponsor_block,  # type: ignore
        log_level,  # type: ignore
        simple_tui,  # type: ignore
        headless,  # type: ignore
        download_ffmpeg,  # type: ignore
        generate_config,  # type: ignore
        check_for_updates,  # type: ignore
        profile,  # type: ignore
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
    log_level = (
        LoggingLevel[opts.log_level]
        if opts.log_level in LoggingLevel.level_names()
        else DEFAULT_LOGGING_LEVEL
    )
    lyrics_providers = opts.lyrics_providers
    m3u = opts.m3u
    output = opts.output
    overwrite = opts.overwrite
    print_errors = opts.print_errors
    query = opts.query if opts.query is not None else []
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
