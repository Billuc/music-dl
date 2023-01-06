from urllib.parse import quote
from kink import inject
from typing import Callable, List, Tuple
from requests import Session, Response
from bs4 import BeautifulSoup

from musicdl.common import BasePipelineMiddleware, Song
from musicdl.providers.lyrics.data import DownloadLyricsCommand
from musicdl.providers.lyrics.consts import LYRICS_HEADERS


SEARCH_URL = "https://www.musixmatch.com/search"


@inject
class MusixmatchLyricsProvider(BasePipelineMiddleware[DownloadLyricsCommand, str]):
    _session: Session

    def __init__(self):
        self._session = Session()
        self._session.headers.update(LYRICS_HEADERS)

    def exec(
        self,
        options: DownloadLyricsCommand,
        next: Callable[[DownloadLyricsCommand], str],
    ) -> str:
        if not "musixmatch" in options.lyrics_providers:
            return next(options)

        search_results = self._get_search_results(options.song)
        links = self._get_links(search_results)
        lyrics_link = self._get_best_link(links)
        lyrics = self._get_lyrics(lyrics_link)

        return lyrics

    def _get_search_results(self, song: Song) -> Response:
        query = (
            f"{song.name} - {', '.join(artist for artist in song.artists if artist)}"
        )
        safe_query = f"{SEARCH_URL}/{quote(query, safe='')}"

        return self._session.get(safe_query, timeout=10)

    def _get_links(self, response: Response) -> List[Tuple[str, str, str]]:
        search_soup = BeautifulSoup(response.text, "html.parser")
        list_items = search_soup.select("div.media-card-text")

        results = []
        for list_item in list_items:
            lyrics_link = list_item.select_one("a.title[href^='/lyrics/']")
            artist_link = list_item.select_one("a.artist")

            if lyrics_link is None or lyrics_link.get("href", None) is None:
                continue

            results.append(
                (
                    lyrics_link.get("href", None),
                    lyrics_link.get_text(strip=True),
                    artist_link.get_text(strip=True) if artist_link else None,
                )
            )

        return results

    def _get_best_link(self, links: List[Tuple[str, str, str]]) -> str:
        return f"https://www.musixmatch.com{links[0][0]}"  # TODO

    def _get_lyrics(self, link: str) -> str:
        lyrics_response = self._session.get(link, timeout=10)
        lyrics_soup = BeautifulSoup(lyrics_response.text, "html.parser")

        lyrics_paragraphs = lyrics_soup.select("p.mxm-lyrics__content")
        return "\n".join(p.get_text() for p in lyrics_paragraphs).strip()
