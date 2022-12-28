from distutils.command.config import config
from typing import Any, Dict

from musicdl.commands import CommandOptions, AllowedOperations
from musicdl.common import LoggingLevel, DEFAULT_LOGGING_LEVEL, MusicDLException
from musicdl.exec.data import QueryOptions, ConfigOptions, ExecOptions


def generate_exec_options(
    query_opts: QueryOptions, config_opts: ConfigOptions
) -> ExecOptions:
    if config_opts is None:
        raise MusicDLException(
            "Config options should not be None ! If you don't have a config file, generate one using the --generate-config flag"
        )

    options = ExecOptions(
        query_opts.operation,
        query_opts.query,
        query_opts.audio_providers or config_opts.audio_providers,
        query_opts.lyrics_providers or config_opts.lyrics_providers,
        query_opts.no_config,
        query_opts.search_query or config_opts.search_query,
        query_opts.filter_results or config_opts.filter_results,
        query_opts.ffmpeg or config_opts.ffmpeg,
        query_opts.threads or config_opts.threads,
        query_opts.bitrate or config_opts.threads,
        query_opts.ffmpeg_args or config_opts.ffmpeg_args,
        query_opts.format or config_opts.format,
        query_opts.save_file or config_opts.format,
        query_opts.output or config_opts.output,
        query_opts.m3u or config_opts.m3u,
        query_opts.overwrite or config_opts.overwrite,
        query_opts.restrict or config_opts.restrict,
        query_opts.print_errors or config_opts.print_errors,
        query_opts.sponsor_block or config_opts.sponsor_block,
        query_opts.log_level or config_opts.log_level,
        query_opts.simple_tui or config_opts.simple_tui,
        query_opts.headless or config_opts.headless,
        query_opts.download_ffmpeg,
        query_opts.generate_config,
        query_opts.check_for_updates,
        query_opts.profile,
        config_opts.load_config,
        config_opts.cache_path,
        config_opts.client_id,
        config_opts.client_secret,
        config_opts.user_auth,
        config_opts.no_cache,
        config_opts.cookie_file,
        config_opts.preload,
    )

    return options


def to_command_options(opts: ExecOptions) -> CommandOptions:
    operation = _to_allowed_operation(opts)
    audio_providers = opts.audio_providers
    bitrate = opts.bitrate
    ffmpeg = opts.ffmpeg
    ffmpeg_args = opts.ffmpeg_args
    filter_results = opts.filter_results
    format = opts.format
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

    client_id = opts.client_id
    client_secret = opts.client_secret
    cache_path = opts.cache_path
    user_auth = opts.user_auth
    no_cache = opts.no_cache
    headless = opts.headless

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
        client_id,
        client_secret,
        cache_path,
        user_auth,
        no_cache,
        headless,
    )

    return command_opts


def _to_allowed_operation(options: ExecOptions) -> AllowedOperations:
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
