from musicdl.commands.data import CommandOptions
from musicdl.downloader import DownloaderSettings


def build_download_settings(commandOpts: CommandOptions) -> DownloaderSettings:
    settings = DownloaderSettings(
        commandOpts.query,
        commandOpts.search_query,
        commandOpts.filter_results,
        commandOpts.ffmpeg,
        commandOpts.threads,
        commandOpts.bitrate,
        commandOpts.ffmpeg_args,
        commandOpts.format,
        commandOpts.save_file,
        commandOpts.output,
        commandOpts.m3u,
        commandOpts.overwrite,
        commandOpts.restrict,
        commandOpts.print_errors,
        commandOpts.sponsor_block,
        commandOpts.log_level,
        commandOpts.simple_tui,
        commandOpts.client_id,
        commandOpts.client_secret,
        commandOpts.cache_path,
        commandOpts.user_auth,
        commandOpts.no_cache,
        commandOpts.headless
    )

    return settings