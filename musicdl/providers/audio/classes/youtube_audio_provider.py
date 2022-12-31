"""
Youtube module for downloading and searching songs.
"""

from typing import Any, Dict, List, Optional, Tuple
from kink import inject
from pytube import YouTube as PyTube, Search
from rapidfuzz import fuzz
from slugify import slugify

from typing import Dict, Callable
from yt_dlp import YoutubeDL

from musicdl.common import BasePipelineMiddleware, BaseFormatHelper, BaseYoutubeDLClientProvider, MusicDLException, Song
from musicdl.providers.audio.data import DownloadSongCommand


@inject
class YoutubeAudioProvider(BasePipelineMiddleware[DownloadSongCommand, Dict]):
    _format_helper: BaseFormatHelper
    _youtube_dl_client: YoutubeDL
    
    
    def __init__(
        self, 
        format_helper: BaseFormatHelper,
        ytdl_client_provider: BaseYoutubeDLClientProvider
    ):
        self._format_helper = format_helper
        self._youtube_dl_client = ytdl_client_provider.get_client()
        
        
    def exec(self, query: DownloadSongCommand, next: Callable[[DownloadSongCommand], Dict]) -> Dict:
        if "youtube" not in query.audio_providers:
            return next(query)
        
        download_url = self._get_download_url(query.song, query.search_query, query.filter_results)
        
        if download_url is None:
            return next(query)
        
        return self._get_download_metadata(download_url, True)
    
    
    def _get_download_url(self, song: Song, search_query: str, filter_results: bool):
        if search_query is None and song.isrc is not None:
            isrc_result = self._get_isrc_result(song)
            if isrc_result is not None:
                return isrc_result
            
        if search_query is not None:
            search = self._format_helper.create_search_query(
                song, search_query, False, None, True
            )
        else:
            search = self._format_helper.create_song_title(song.name, song.artists).lower()
            
        results = Search(search).results
        
        if results is None:
            return None
        
        return self._get_best_result(results, song, search, filter_results)
        
        
    def _get_isrc_result(self, song: Song) -> Optional[str]:
        isrc_results: Optional[List[PyTube]] = Search(song.isrc).results

        if isrc_results is None or len(isrc_results) != 1:
            return None
        
        isrc_result = isrc_results[0]
        return isrc_result.watch_url if isrc_result is not None else None
        
                
    def _get_best_result(self, results: List[PyTube], song: Song, search: str, filter_results: bool) -> str:
        if not filter_results:
            return results[0].watch_url
        
        results_score_dict: Dict[PyTube, Tuple[float, int]] = {}
        for result in results:
            video_id_score = self._get_video_id_score(result)
            words_in_common_score = self._get_words_in_common_score(result, song)
            artist_match_score = self._get_artist_match_score(result, song)
            name_match_score = self._get_name_match_score(result, song, search)
            time_match_score = self._get_time_match_score(result, song)
            
            score = 0
            if not (
                video_id_score < 1 or
                words_in_common_score < 1 or
                artist_match_score < 70 or
                name_match_score < 50 or
                time_match_score < 50
            ):
                score = (artist_match_score + name_match_score + time_match_score) / 3
                
            results_score_dict[result.watch_url] = (score, result.views)
            
        ordered_results = sorted(list(results_score_dict.items()), key=lambda el: el[1], reverse=True)
        return ordered_results[0][0] if ordered_results[0][1][0] > 0 else None
    
          
    def _get_video_id_score(self, result: PyTube) -> float:
        return 0.0 if result.video_id is None else 1.0
    
    
    def _get_words_in_common_score(self, result: PyTube, song: Song) -> float:
        slug_result_name = slugify(result.title)
        slug_song_name = slugify(song.name, separator=" ").split(" ")
        return 1.0 if any(
            word != "" and word in slug_result_name for word in slug_song_name
        ) else 0.0
        
        
    def _get_artist_match_score(self, result: PyTube, song: Song) -> float:
        slug_result_name = slugify(result.title)
        artist_match_number = 0.0
        
        for artist in song.artists:
            artist_match_number += fuzz.partial_token_sort_ratio(
                slugify(artist), slug_result_name
            )
        
        return artist_match_number / len(song.artists)
    
    
    def _get_name_match_score(self, result: PyTube, song: Song, search: str) -> float:
        slug_result_name = slugify(result.title)
        slug_song_title = slugify(search)

        return fuzz.partial_token_sort_ratio(
            slug_result_name, slug_song_title
        )
        
        
    def _get_time_match_score(self, result: PyTube, song: Song) -> float:
        return 100 - abs(result.length - song.duration) / song.duration * 100
            
    
    def _get_download_metadata(self, url: str, download: bool = False) -> Dict:
        """
        Get metadata for a download using yt-dlp.

        ### Arguments
        - url: The url to get metadata for.

        ### Returns
        - A dictionary containing the metadata.
        """

        try:
            data = self._youtube_dl_client.extract_info(url, download=download)

            if data:
                return data
        except Exception as exception:
            raise MusicDLException(f"YT-DLP download error - {url}") from exception

        raise MusicDLException(f"No metadata found for the provided url {url}")


