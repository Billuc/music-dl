"""
Downloader module, this is where all the downloading pre/post processing happens etc.
"""

import json
import datetime
import asyncio
import shutil
import sys
import concurrent.futures
import traceback

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type

from yt_dlp.postprocessor.sponsorblock import SponsorBlockPP
from yt_dlp.postprocessor.modify_chapters import ModifyChaptersPP

from musicdl.utils.ffmpeg import FFmpegError, convert, get_ffmpeg_path
from musicdl.utils.metadata import embed_metadata, MetadataError
from musicdl.utils.formatter import create_file_name, restrict_filename
from musicdl.providers.audio.base import AudioProvider
from musicdl.providers.lyrics import Genius, MusixMatch, AzLyrics
from musicdl.providers.lyrics.base import LyricsProvider
from musicdl.providers.audio import YouTube, YouTubeMusic
from musicdl.downloader.progress_handler_old import NAME_TO_LEVEL, ProgressHandler
from musicdl.utils.config import get_errors_path, get_temp_path


from musicdl.downloader.classes import Song, DownloaderSettings
from musicdl.downloader.interfaces import BaseAudioProvider, BaseLyricsProvider, BaseProgressLogger
from musicdl.common import MusicDLException




class Downloader:
    """
    Downloader class, this is where all the downloading pre/post processing happens etc.
    It handles the downloading/moving songs, multthreading, metadata embedding etc.
    """

    _initialized: bool
    _audio_provider: BaseAudioProvider
    _lyrics_provider: BaseLyricsProvider
    _progress_logger: BaseProgressLogger
    _loop: asyncio.AbstractEventLoop
    _semaphore: asyncio.Semaphore
    _thread_executor: concurrent.futures.ThreadPoolExecutor


    def __init__(
        self,
        audio_provider: BaseAudioProvider,
        lyrics_provider: BaseLyricsProvider,
        progress_logger: BaseProgressLogger,
        loop: asyncio.AbstractEventLoop
    ):
        self._initialized = False
        self._audio_provider = audio_provider
        self._lyrics_provider = lyrics_provider
        self._progress_logger = progress_logger
        self._loop = loop


    def update_settings(self, settings: DownloaderSettings) -> None:
        # semaphore is required to limit concurrent asyncio executions
        self._semaphore = asyncio.Semaphore(settings.threads)

        # thread pool executor is used to run blocking (CPU-bound) code from a thread
        self._thread_executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=settings.threads
        )


    def download_song(self, song: Song) -> Tuple[Song, Optional[Path]]:
        results = self.download_multiple_songs([song])
        return results[0]


    def download_multiple_songs(
        self, songs: List[Song]
    ) -> List[Tuple[Song, Optional[Path]]]:
        self.progress_handler.set_song_count(len(songs))

        tasks = [self.pool_download(song) for song in songs]

        # call all task asynchronously, and wait until all are finished
        results = list(self.loop.run_until_complete(self._aggregate_tasks(tasks)))

        if self.print_errors:
            for error in self.errors:
                self.progress_handler.error(error)

        if self.save_file:
            with open(self.save_file, "w", encoding="utf-8") as save_file:
                json.dump([song.json for song, _ in results], save_file, indent=4)

        return results


    async def pool_download(self, song: Song) -> Tuple[Song, Optional[Path]]:
        """
        Run asynchronous task in a pool to make sure that all processes.

        ### Arguments
        - song: The song to download.

        ### Returns
        - tuple with the song and the path to the downloaded file if successful.

        ### Notes
        - This method calls `self.search_and_download` in a new thread.
        """

        # tasks that cannot acquire semaphore will wait here until it's free
        # only certain amount of tasks can acquire the semaphore at the same time
        async with self.semaphore:
            # The following function calls blocking code, which would block whole event loop.
            # Therefore it has to be called in a separate thread via ThreadPoolExecutor. This
            # is not a problem, since GIL is released for the I/O operations, so it shouldn't
            # hurt performance.
            return await self.loop.run_in_executor(
                self.thread_executor, self.search_and_download, song
            )

    def search(self, song: Song) -> str:
        """
        Search for a song using all available providers.

        ### Arguments
        - song: The song to search for.

        ### Returns
        - tuple with download url and audio provider if successful.
        """

        result = self._audio_provider.search(song)

        if result is None:
            raise MusicDLException(f"No results found for song: {song.display_name}")

        return result


    def search_lyrics(self, song: Song) -> str:
        """
        Search for lyrics using all available providers.

        ### Arguments
        - song: The song to search for.

        ### Returns
        - lyrics if successful.
        """

        for lyrics_provider in self.lyrics_providers:
            lyrics = lyrics_provider.get_lyrics(song.name, song.artists)
            if lyrics:
                self.progress_handler.debug(
                    f"Found lyrics for {song.display_name} on {lyrics_provider.name}"
                )
                return lyrics

            self.progress_handler.debug(
                f"{lyrics_provider.name} failed to find lyrics "
                f"for {song.display_name}"
            )

        raise LookupError(f"No lyrics found for song: {song.display_name}")

    def search_and_download(self, song: Song) -> Tuple[Song, Optional[Path]]:
        """
        Search for the song and download it.

        ### Arguments
        - song: The song to download.

        ### Returns
        - tuple with the song and the path to the downloaded file if successful.

        ### Notes
        - This function is synchronous.
        """

        # Check if we have all the metadata
        # and that the song object is not a placeholder
        # If it's None extract the current metadata
        # And reinitialize the song object
        if song.name is None and song.url:
            data = song.json
            new_data = Song.from_url(data["url"]).json
            data.update((k, v) for k, v in new_data.items() if v is not None)

            if data.get("song_list"):
                # Reinitialize the correct song list object
                data["song_list"] = song.song_list.__class__(**data["song_list"])

            # Reinitialize the song object
            song = Song(**data)

        # Create the output file path
        output_file = create_file_name(song, self.output, self.output_format)
        temp_folder = get_temp_path()

        # Restrict the filename if needed
        if self.restrict is True:
            output_file = restrict_filename(output_file)

        # If the file already exists and we don't want to overwrite it,
        # we can skip the download
        if output_file.exists() and self.overwrite == "skip":
            self.progress_handler.log(f"Skipping {song.display_name}")
            self.progress_handler.overall_completed_tasks += 1
            self.progress_handler.update_overall()
            return song, None

        # Don't skip if the file exists and overwrite is set to force
        if output_file.exists() and self.overwrite == "force":
            self.progress_handler.debug(f"Overwriting {song.display_name}")

        # Initalize the progress tracker
        display_progress_tracker = self.progress_handler.get_new_tracker(song)

        # Create the output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            if song.download_url is None:
                url, audio_provider = self.search(song)
            else:
                url = song.download_url
                audio_provider = AudioProvider(
                    output_format=self.output_format,
                    cookie_file=self.cookie_file,
                    search_query=self.search_query,
                    filter_results=self.filter_results,
                )

            self.progress_handler.debug(
                f"Downloading {song.display_name} using {url}, "
                f"audio provider: {audio_provider.name}"
            )

            # Add progress hook to the audio provider
            audio_provider.audio_handler.add_progress_hook(
                display_progress_tracker.yt_dlp_progress_hook
            )

            # Download the song using yt-dlp
            download_info = audio_provider.get_download_metadata(url, download=True)
            temp_file = Path(
                temp_folder / f"{download_info['id']}.{download_info['ext']}"
            )

            if download_info is None:
                self.progress_handler.debug(
                    f"No download info found for {song.display_name}, url: {url}"
                )

                raise LookupError(
                    f"yt-dlp failed to get metadata for: {song.name} - {song.artist}"
                )

            display_progress_tracker.notify_download_complete()

            success, result = convert(
                temp_file,
                output_file,
                self.ffmpeg,
                self.output_format,
                self.bitrate,
                self.ffmpeg_args,
                display_progress_tracker.ffmpeg_progress_hook,
            )

            # Remove the temp file
            if temp_file.exists():
                temp_file.unlink()

            if not success and result:
                # If the conversion failed and there is an error message
                # create a file with the error message
                # and save it in the errors directory
                # raise an exception with file path
                file_name = (
                    get_errors_path()
                    / f"ffmpeg_error_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt"
                )

                error_message = ""
                for key, value in result.items():
                    error_message += f"### {key}:\n{str(value).strip()}\n\n"

                with open(file_name, "w", encoding="utf-8") as error_path:
                    error_path.write(error_message)

                # Remove the file that failed to convert
                if output_file.exists():
                    output_file.unlink()

                raise FFmpegError(
                    f"Failed to convert {song.display_name}, "
                    f"you can find error here: {str(file_name.absolute())}"
                )

            download_info["filepath"] = str(output_file)

            # Set the song's download url
            if song.download_url is None:
                song.download_url = download_info["webpage_url"]

            display_progress_tracker.notify_conversion_complete()

            if self.sponsor_block:
                post_processor = SponsorBlockPP(
                    audio_provider.audio_handler, SPONSOR_BLOCK_CATEGORIES
                )

                _, download_info = post_processor.run(download_info)
                chapters = download_info["sponsorblock_chapters"]
                if len(chapters) > 0:
                    self.progress_handler.log(
                        f"Removing {len(chapters)} sponsor segments for {song.display_name}"
                    )

                    modify_chapters = ModifyChaptersPP(
                        audio_provider.audio_handler,
                        remove_sponsor_segments=SPONSOR_BLOCK_CATEGORIES,
                    )

                    files_to_delete, download_info = modify_chapters.run(download_info)

                    for file_to_delete in files_to_delete:
                        Path(file_to_delete).unlink()

            try:
                song.lyrics = self.search_lyrics(song)
            except LookupError:
                self.progress_handler.debug(
                    f"No lyrics found for {song.display_name}, "
                    "lyrics providers: "
                    f"{', '.join([lprovider.name for lprovider in self.lyrics_providers])}"
                )

            try:
                embed_metadata(output_file, song, self.output_format)
            except Exception as exception:
                raise MetadataError(
                    "Failed to embed metadata to the song"
                ) from exception

            display_progress_tracker.notify_complete()

            self.progress_handler.log(
                f'Downloaded "{song.display_name}": {song.download_url}'
            )

            return song, output_file
        except Exception as exception:
            display_progress_tracker.notify_error(traceback.format_exc(), exception)
            self.errors.append(
                f"{song.url} - {exception.__class__.__name__}: {exception}"
            )
            return song, None

    @staticmethod
    async def _aggregate_tasks(tasks):
        """
        Aggregate the futures and return the results
        """

        return await asyncio.gather(*(task for task in tasks))
