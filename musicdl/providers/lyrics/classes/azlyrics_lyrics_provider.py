from kink import inject
from typing import Callable, List, Tuple
from requests import Session, Response
from bs4 import BeautifulSoup

from musicdl.common import BasePipelineMiddleware, Song
from musicdl.providers.lyrics.data import DownloadLyricsCommand
from musicdl.providers.lyrics.consts import LYRICS_HEADERS


GEO_JS_URL = "https://www.azlyrics.com/geo.js"
SEARCH_URL = "https://search.azlyrics.com/search.php"


@inject
class AZLyricsLyricsProvider(BasePipelineMiddleware[DownloadLyricsCommand, str]):
    _session: Session
    _x_code: str

    def __init__(self):
        self._session = Session()
        self._session.headers.update(LYRICS_HEADERS)

        self._get_x_code()

    def _get_x_code(self):
        geo_js = self._session.get(GEO_JS_URL)
        js_code = geo_js.text

        start_index = js_code.find('"value"') + 10  # len('"value", "')
        end_index = js_code[start_index:].find('");')

        self._x_code = js_code[start_index : start_index + end_index]

    def exec(
        self,
        options: DownloadLyricsCommand,
        next: Callable[[DownloadLyricsCommand], str],
    ) -> str:
        if not "azlyrics" in options.lyrics_providers:
            return next(options)

        search_results = self._get_search_results(options.song)
        links = self._get_links_in_html(search_results)
        lyrics_link = self._get_best_link(links)
        lyrics = self._get_lyrics(lyrics_link)

        return lyrics

    def _get_search_results(self, song: Song) -> Response:
        params = {
            "q": f"{', '.join(artist for artist in song.artists if artist)} - {song.name}",
            "x": self._x_code,
        }

        return self._session.get(SEARCH_URL, params=params)

    def _get_links_in_html(self, response: Response) -> List[Tuple[str, str, str]]:
        soup = BeautifulSoup(response.content, "html.parser")
        list_item = soup.find("td")

        results = []
        while list_item is not None:
            link = list_item.find("a", href=True)

            if link is None or link["href"].strip() == "":
                list_item = list_item.find_next("td")
                continue

            infos = link.find_all("b")

            if len(infos) < 2:
                list_item = list_item.find_next("td")
                continue

            results.append(
                (link["href"].strip(), str(infos[0].string), str(infos[1].string))
            )
            list_item = list_item.find_next("td")

        return results

    def _get_best_link(self, links: List[Tuple[str, str, str]]) -> str:
        return links[0][0]  # TODO

    def _get_lyrics(self, link: str) -> str:
        lyrics_response = self._session.get(link)
        soup = BeautifulSoup(lyrics_response.content, "html.parser")

        divs = soup.find_all("div", class_=False, id_=False)
        lyrics_div = max(divs, key=lambda div: len(div.text))

        return lyrics_div.get_text().strip()
