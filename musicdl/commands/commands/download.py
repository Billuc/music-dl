"""
Download module for the console.
"""

from logging import Logger
from kink import inject
import json

from typing import List, Optional
from pathlib import Path

from musicdl.commands.interfaces import BaseCommand
from musicdl.commands.data import CommandOptions
from musicdl.downloader import BaseDownloader

from musicdl.downloader.downloader_old import Downloader
from musicdl.utils.m3u import create_m3u_file
from musicdl.utils.search import get_simple_songs


@inject
class DownloadCommand(BaseCommand):
    _logger: Logger
    _downloader: BaseDownloader

    def __init__(self, logger: Logger, downloader: BaseDownloader):
        self._logger = logger
        self._downloader = downloader


    def exec(self, options: CommandOptions) -> None:
        self._downloader.download_multiple_songs()
        # parse query to get songs or song searches
        # download musics accordingly
        # if m3u, create a m3u file
        # if save_path dump json

        return None


def download(
    query: List[str],
    downloader: Downloader,
    save_path: Optional[Path] = None,
    m3u_file: Optional[str] = None,
    **_
) -> None:
    """
    Find songs with the provided audio provider and save them to the disk.

    ### Arguments
    - query: list of strings to search for.
    - downloader: Already initialized downloader instance.
    - save_path: Path to save the songs to or None.
    - m3u_file: Path to the m3u file to save the songs to.
    """

    # Parse the query
    songs = get_simple_songs(query)

    results = downloader.download_multiple_songs(songs)

    if m3u_file:
        song_list = [song for (song, _) in results]
        create_m3u_file(
            m3u_file, song_list, downloader.output, downloader.output_format, False
        )

    if save_path:
        # Save the songs to a file
        with open(save_path, "w", encoding="utf-8") as save_file:
            json.dump(songs, save_file, indent=4, ensure_ascii=False)
