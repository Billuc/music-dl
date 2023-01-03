import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional

from slugify import slugify
from yt_dlp.utils import sanitize_filename

from musicdl.common.consts import DEFAULT_TEMPLATE, FORMAT_VARIABLES
from musicdl.common.data import Song
from musicdl.common.exceptions import MusicDLException
from musicdl.common.interfaces import BaseFormatHelper


class FormatHelper(BaseFormatHelper):
    def create_song_title(self, song_name: str, song_artists: List[str]) -> str:
        """
        Create the song title.

        ### Arguments
        - song_name: the name of the song
        - song_artists: the list of artists of the song

        ### Returns
        - the song title

        ### Notes
        - Example: "Artist1, Artist2 - Song Name"

        """

        if len(song_artists) == 0:
            return song_name

        joined_artists = ", ".join(song_artists)
        return f"{joined_artists} - {song_name}"

    def create_search_query(
        self,
        song: Song,
        template: str,
        santitize: bool,
        file_extension: Optional[str] = None,
        short: bool = False,
    ) -> str:
        # If template does not contain any of the keys,
        # append {artist} - {title} at the beggining of the template
        if not any(key in template for key in FORMAT_VARIABLES):
            template = "{artist} - {title}" + template

        return self._format_query(
            song, template, santitize, file_extension, short=short
        )

    def create_file_name(
        self,
        song: Song,
        template: str,
        file_extension: str,
        restrict: bool,
        short: bool = False,
    ) -> Path:
        """
        Create the file name for the song, by replacing template variables with the actual values.

        ### Arguments
        - song: the song object
        - template: the template string
        - file_extension: the file extension to use
        - short: whether to use the short version of the template

        ### Returns
        - the formatted string as a Path object
        """

        if (
            not any(key in template for key in FORMAT_VARIABLES)
            or template.endswith("/")
            or template.endswith(r"\\")
            or template.endswith("\\\\")
        ):
            template += "/{artists} - {title}.{output-ext}"

        if not template.endswith(".{output-ext}"):
            template += ".{output-ext}"

        formatted_string = self._format_query(
            song, template, True, file_extension, short
        )
        file = Path(formatted_string)
        # TODO : sanitize (look what it actually does)

        if len(file.name) > 255:
            if short is True:
                warnings.warn(
                    f"{song.display_name}: File name is too long. Using the default template."
                )

                return self.create_file_name(
                    song, DEFAULT_TEMPLATE, file_extension, short
                )
                # TODO : i skipped a part here

            return self.create_file_name(song, template, file_extension, True)

        if restrict is True:
            filename = sanitize_filename(file.name, True, False) or "_"
            filename = filename.replace("_-_", "-")

            file = file.with_name(filename)

        return file

    def _format_query(
        self,
        song: Song,
        template: str,
        santitize: bool,
        file_extension: Optional[str] = None,
    ) -> str:
        if "{output-ext}" in template and file_extension is None:
            raise MusicDLException(
                "file_extension is None, but template contains {output-ext}"
            )

        artists = [
            artist
            for artist in song.artists
            if slugify(artist) not in slugify(song.name)
        ]

        if len(artists) == 0 or artists[0] != song.artists[0]:
            artists.insert(0, song.artists[0])

        if song.song_list:
            try:
                index = song.song_list.songs.index(song)
            except ValueError:
                index = song.song_list.urls.index(song.url)

        variable_values = {
            "{title}": song.name,
            "{artists}": song.artists[0] if short else ", ".join(artists),
            "{artist}": song.artists[0],
            "{album}": song.album_name,
            "{album-artist}": song.album_artist,
            "{genre}": song.genres[0] if len(song.genres) > 0 else "",
            "{disc-number}": song.disc_number,
            "{disc-count}": song.disc_count,
            "{duration}": song.duration,
            "{year}": song.year,
            "{original-date}": song.date,
            "{track-number}": song.track_number,
            "{tracks-count}": song.tracks_count,
            "{isrc}": song.isrc,
            "{track-id}": song.song_id,
            "{publisher}": song.publisher,
            "{output-ext}": file_extension,
            "{list-name}": song.song_list.name if song.song_list is not None else "",
            "{list-position}": str(index + 1).zfill(len(str(song.song_list.length)))
            if song.song_list is not None
            else "",
            "{list-length}": song.song_list.length
            if song.song_list is not None
            else "",
        }

        if santitize:
            variable_values = self._sanitize_values(variable_values)

        for key, value in variable_values.items():
            template = template.replace(key, str(value))

        template = template.replace(r"//", r"/")
        return template

    def _sanitize_values(self, values: Dict[str, Any]) -> Dict[str, Any]:
        newValues = {}

        for key, value in values.items():
            if value is None:
                continue

            newValue = "".join(char for char in value if char not in "/?\\*|<>")
            newValue = newValue.replace('"', "'").replace(":", "-")

            newValues[key] = newValue
