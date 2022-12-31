from typing import Any, Dict, List, Optional, Tuple
from kink import inject
from rapidfuzz import fuzz
from slugify import slugify

from typing import Dict, Callable
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

from musicdl.common import BasePipelineMiddleware, BaseFormatHelper, BaseYoutubeDLClientProvider, MusicDLException, Song
from musicdl.providers.audio.data import DownloadSongCommand, YoutubeMusicResult


@inject
class YoutubeMusicAudioProvider(BasePipelineMiddleware[DownloadSongCommand, Dict]):
    _format_helper: BaseFormatHelper
    _youtube_music_client: YTMusic
    _youtube_dl_client: YoutubeDL
    
    
    def __init__(
        self, 
        format_helper: BaseFormatHelper,
        ytdl_client_provider: BaseYoutubeDLClientProvider
    ):
        self._format_helper = format_helper
        self._youtube_music_client = YTMusic() # TODO : maybe have a provider (to handle sessions or have a singleton)
        self._youtube_dl_client = ytdl_client_provider.get_client()
        
        
    def exec(self, query: DownloadSongCommand, next: Callable[[DownloadSongCommand], Dict]) -> Dict:
        if "ytmusic" not in query.audio_providers:
            return next(query)
        
        download_url = self._get_download_url(query.song, query.search_query, query.filter_results)
        
        if download_url is None:
            return next(query)
        
        return self._get_download_metadata(download_url, True)
    
    
    def _get_download_url(self, song: Song, search_query: str, filter_results: bool) -> str:
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
            
        song_results = self._get_results(search, filter="songs")
        song_result = self._get_best_result(song_results, song, search, filter_results)

        if song_result is not None and song_result[1][0] > 80:
            return song_result[0].link
        
        video_results = self._get_results(search, filter="videos")
        video_result = self._get_best_result(video_results, song, search, filter_results)
        
        if video_result is None:
            return song_result[0].link if song_result is not None else None
        if song_result is None:
            return video_result[0].link if video_result is not None else None
        
        return max([song_result, video_result], key=lambda x: x[1])[0].link
        
        
    def _get_results(self, search: str, filter: str) -> List[YoutubeMusicResult]:
        ytm_results = self._youtube_music_client.search(search, filter=filter)
        
        results = []
        for result in ytm_results:
            if result is None or result.get("videoId") is None:
                continue
            
            results.append(YoutubeMusicResult(
                result["title"],
                result["resultType"],
                f"https://youtube.com/watch?v={result['videoId']}",
                result.get("album", {}).get("name", None),
                0, # TODO
                ", ".join(map(lambda a: a["name"], result["artists"])),
                list(map(lambda a: a["name"], result["artists"]))
            ))
            
        return results
        
        
    def _get_isrc_result(self, song: Song) -> Optional[str]:
        isrc_results = self._get_results(song.isrc, filter="songs")

        if isrc_results is None or len(isrc_results) != 1:
            return None
        
        isrc_result = self._get_best_result([isrc_results[0]], song, song.isrc, True)
        return isrc_result[0] if isrc_result[1][0] > 90 else None
        
                
    def _get_best_result(self, results: List[YoutubeMusicResult], song: Song, search: str, filter_results: bool) -> Tuple[YoutubeMusicResult, Tuple[float, int]]:
        if results is None or len(results) == 0:
            return None
        
        if not filter_results:
            return results[0].link
        
        results_score_dict: Dict[YoutubeMusicResult, Tuple[float, int]] = {}
        for result in results:
            words_in_common_score = self._get_words_in_common_score(result, song)
            artist_match_score = self._get_artist_match_score(result, song)
            name_match_score = self._get_name_match_score(result, song, search)
            album_match_score = self._get_album_match_score(result, song)
            time_match_score = self._get_time_match_score(result, song)
            
            score = 0
            if not (
                words_in_common_score < 1 or
                artist_match_score < 70 or
                name_match_score < 50 or
                album_match_score < 50 or
                time_match_score < 50
            ):
                score = (artist_match_score + name_match_score + album_match_score + time_match_score) / 4
                
            results_score_dict[result.watch_url] = (score, result.views)
            
        best_result = max(list(results_score_dict.items()), key=lambda el: el[1])
        return best_result if best_result[1][0] > 0 else None
    
    
    def _get_words_in_common_score(self, result: YoutubeMusicResult, song: Song) -> float:
        slug_result_name = slugify(result.name)
        slug_song_name = slugify(song.name, separator=" ").split(" ")
        return 1.0 if any(
            word != "" and word in slug_result_name for word in slug_song_name
        ) else 0.0
        
        
    def _get_artist_match_score(self, result: YoutubeMusicResult, song: Song) -> float:
        slug_result_name = slugify(result.name)
        slug_result_artists = slugify(result.artists)
        artist_match_number = 0.0
        
        for artist in song.artists:
            artist_match_number += fuzz.partial_token_sort_ratio(
                slugify(artist), slug_result_artists
            )
            artist_match_number += fuzz.partial_token_sort_ratio(
                slugify(artist), slug_result_name
            )
        
        return artist_match_number / len(song.artists)
    
    
    def _get_name_match_score(self, result: YoutubeMusicResult, song: Song, search: str) -> float:
        slug_result_name = slugify(result.name)
        slug_song_title = slugify(search)

        return fuzz.partial_token_sort_ratio(
            slug_result_name, slug_song_title
        )
        
        
    def _get_album_match_score(self, result: YoutubeMusicResult, song: Song) -> float:
        if result.album is None:
            return 50.0
        
        slug_result_album = slugify(result.album)
        slug_song_album = slugify(song.album)
        
        return fuzz.partial_token_sort_ratio(
            slug_result_album, slug_song_album
        )
        
        
    def _get_time_match_score(self, result: YoutubeMusicResult, song: Song) -> float:
        return 100 - abs(result.duration - song.duration) / song.duration * 100
            
    
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


