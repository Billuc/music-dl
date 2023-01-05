from kink import inject
from typing import Callable, List, Tuple
from requests import Session, Response
from bs4 import BeautifulSoup

from musicdl.common import BasePipelineMiddleware, Song
from musicdl.providers.lyrics.data import DownloadLyricsCommand
from musicdl.providers.lyrics.consts import LYRICS_HEADERS


SEARCH_URL = "https://api.genius.com/search"


@inject
class GeniusLyricsProvider(BasePipelineMiddleware[DownloadLyricsCommand, str]):
    _session: Session

    def __init__(self):
        self._session = Session()
        self._session.headers.update(LYRICS_HEADERS)
        self._session.headers.update(
            {
                "Authorization": "Bearer alXXDbPZtK1m2RrZ8I4k2Hn8Ahsd0Gh_o076HYvcdlBvmc0ULL1H8Z8xRlew5qaG"
            }
        )

    def exec(
        self,
        options: DownloadLyricsCommand,
        next: Callable[[DownloadLyricsCommand], str],
    ) -> str:
        """
        Try to get lyrics from genius

        ### Arguments
        - name: The name of the song.
        - artists: The artists of the song.

        ### Returns
        - The lyrics of the song or None if no lyrics were found.
        """

        search_results = self._get_search_results(options.song)
        links = self._get_links(search_results)
        lyrics_link = self._get_best_link(links)
        lyrics = self._get_lyrics(lyrics_link)

        return lyrics

    def _get_search_results(self, song: Song) -> Response:
        params = {
            "q": f"{song.name} {', '.join(artist for artist in song.artists if artist)}"
        }

        return self._session.get(SEARCH_URL, params=params, timeout=10)

    def _get_links(self, response: Response) -> List[Tuple[str, str, str]]:
        list_items = response.json()["response"]["hits"]

        results = []
        for list_item in list_items:
            if list_item["result"]["url"] is None:
                continue

            results.append(
                (
                    list_item["result"]["url"],
                    list_item["result"]["title_with_featured"],
                    list_item["result"]["artist_names"],
                )
            )

        return results

    def _get_best_link(self, links: List[Tuple[str, str, str]]) -> str:
        return links[0][0]  # TODO

    def _get_lyrics(self, link: str) -> str:
        lyrics_response = self._session.get(link, timeout=10)
        soup = BeautifulSoup(lyrics_response.text.replace("<br/>", "\n"), "html.parser")

        lyrics_div = soup.select_one("div.lyrics")
        if lyrics_div is not None:
            return lyrics_div.get_text().strip()

        lyrics_divs = soup.select("div[class^=Lyrics__Container]")
        return "\n".join(div.get_text() for div in lyrics_divs).strip()
