from musicdl.commands.data import CommandOptions
from musicdl.downloader import DownloaderSettings


def build_download_settings(command_opts: CommandOptions) -> DownloaderSettings:
    settings = DownloaderSettings(
        command_opts.query,
        command_opts.search_query,
        command_opts.filter_results,
        command_opts.ffmpeg,
        command_opts.threads,
        command_opts.bitrate,
        command_opts.ffmpeg_args,
        command_opts.format,
        command_opts.save_file,
        command_opts.output,
        command_opts.m3u,
        command_opts.overwrite,
        command_opts.restrict,
        command_opts.print_errors,
        command_opts.sponsor_block,
        command_opts.log_level,
        command_opts.simple_tui,
        command_opts.client_id,
        command_opts.client_secret,
        command_opts.cache_path,
        command_opts.user_auth,
        command_opts.no_cache,
        command_opts.headless,
        command_opts.cookie_file,
        command_opts.audio_providers,
        command_opts.lyrics_providers
    )

    return settings