"""
Downloader module, this is where all the downloading pre/post processing happens etc.
"""

import json

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type
from kink import inject

from musicdl.downloader.data import Song, DownloaderSettings
from musicdl.downloader.interfaces import (
    BaseLyricsProvider, 
    BaseProgressLogger,
    BaseDownloadCoordinator,
    BaseAudioConverter,
    BaseParallelExecutor
)
from musicdl.providers.audio import BaseAudioProvider, DownloadSongCommand
from musicdl.providers.metadata import BaseMetadataProvider
from musicdl.common import MusicDLException, BaseSpotifyClientProvider, BaseYoutubeDLClientProvider, TEMP_PATH, Song, BaseFormatHelper



@inject
class DownloadCoordinator(BaseDownloadCoordinator):
    """
    Downloader class, this is where all the downloading pre/post processing happens etc.
    It handles the downloading/moving songs, multthreading, metadata embedding etc.
    """

    _initialized: bool
    _settings: DownloaderSettings

    _spotify_client_provider: BaseSpotifyClientProvider
    _youtube_dl_client_provider: BaseYoutubeDLClientProvider
    _format_helper: BaseFormatHelper
    
    _metadata_provider: BaseMetadataProvider
    _audio_provider: BaseAudioProvider
    _lyrics_provider: BaseLyricsProvider
    _audio_converter: BaseAudioConverter

    _progress_logger: BaseProgressLogger
    _parallel_executor: BaseParallelExecutor



    def __init__(
        self,
        spotify_client_provider: BaseSpotifyClientProvider,
        youtube_dl_client_provider: BaseYoutubeDLClientProvider,
        format_helper: BaseFormatHelper,
        metadata_provider: BaseMetadataProvider,
        audio_provider: BaseAudioProvider,
        lyrics_provider: BaseLyricsProvider,
        progress_logger: BaseProgressLogger,
        parallel_executor: BaseParallelExecutor,
        audio_converter: BaseAudioConverter
    ):
        self._initialized = False
        self._spotify_client_provider = spotify_client_provider
        self._youtube_dl_client_provider = youtube_dl_client_provider
        self._format_helper = format_helper
        self._metadata_provider = metadata_provider
        self._audio_provider = audio_provider
        self._lyrics_provider = lyrics_provider
        self._progress_logger = progress_logger
        self._parallel_executor = parallel_executor
        self._audio_converter = audio_converter


    def download(self, options: DownloaderSettings) -> List[Tuple[Song, Optional[Path]]]:
        self._update_settings(options)
        results = self._search_and_download(options.query)
        
        if self.print_errors:
            for error in self.errors:
                self.progress_handler.error(error)

        if self.save_file:
            with open(self.save_file, "w", encoding="utf-8") as save_file:
                json.dump([song.json for song, _ in results], save_file, indent=4)

        return results


    def _update_settings(self, settings: DownloaderSettings) -> None:
        self._settings = settings
        self._spotify_client_provider.init(
            settings.client_id,
            settings.client_secret,
            settings.user_auth,
            settings.cache_path,
            settings.no_cache,
            not settings.headless
        )
        self._youtube_dl_client_provider.init(
            settings.output,
            settings.cookie_file,
        )
        self._progress_logger.update_settings(settings)
        self._parallel_executor.configure(settings.threads)
        self._audio_converter.configure(settings)
        self._initialized = True


    def _search_and_download(self, query: List[str]) -> List[Tuple[Song, Optional[Path]]]:
        results = list()

        for query_item in query:
            songs = self._metadata_provider.search(query_item)
            self._progress_logger.set_count(len(songs))
            
            partial_results = list(self._parallel_executor.execute_function(self._download, songs, return_exceptions=True))
            results.concat(partial_results)

        return results


    def _download(self, song: Song) -> Tuple[Song, Optional[Path]]:
        output_file = self._format_helper.create_file_name(
            song, self._settings.output, self._settings.format, self._settings.restrict
        )
        
        if not self._should_skip(song, output_file):
            self._prepare(song, output_file)
            
            download_info = self._audio_provider.exec(
                DownloadSongCommand(
                    song, 
                    self._settings.search_query, 
                    self._settings.filter_results,
                    self._settings.audio_providers
                )
            )
            
            temp_file = Path(TEMP_PATH / f"{download_info['id']}.{download_info['ext']}")
            self._audio_converter.convert(temp_file, output_file)
            
            # sponsor block
            lyrics = self._lyrics_provider.get_lyrics(song)
            # embed metadata
            # TODO : update song.download_url ?
            
            self._clean(temp_file)
            
        # TODO : update logger
        
        return (song, output_file)
        
    
    def _should_skip(self, song: Song, output_file: Path) -> bool:
        if not output_file.exists():
            return False
        
        if self._settings.overwrite == "force":
            self._progress_logger.debug(f"Overwriting {song.display_name}")
            return False
        
        self._progress_logger.log(f"Skipping {song.display_name}")
        # self._progress_logger.overall_completed_tasks += 1
        # self._progress_logger.update_overall()
        return True
    
    
    def _prepare(self, song: Song, output_file: Path):
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
    
    def _clean(self, temp_file: Path):
        if temp_file.exists():
            temp_file.unlink()
        
