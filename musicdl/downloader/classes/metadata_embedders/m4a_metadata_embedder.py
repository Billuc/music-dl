from kink import inject
from mutagen.mp4 import MP4, MP4Cover
from urllib.request import urlopen

from musicdl.common import BaseResponsibilityChainLink, Song
from musicdl.downloader.data import EmbedMetadataCommand

# Apple has specific tags - see mutagen docs -
# http://mutagen.readthedocs.io/en/latest/api/mp4.html
M4A_TAG_PRESET = {
    "album": "\xa9alb",
    "artist": "\xa9ART",
    "date": "\xa9day",
    "title": "\xa9nam",
    "year": "\xa9day",
    "originaldate": "purd",
    "comment": "\xa9cmt",
    "group": "\xa9grp",
    "writer": "\xa9wrt",
    "genre": "\xa9gen",
    "tracknumber": "trkn",
    "albumartist": "aART",
    "discnumber": "disk",
    "cpil": "cpil",
    "albumart": "covr",
    "encodedby": "\xa9too",
    "copyright": "cprt",
    "tempo": "tmpo",
    "lyrics": "\xa9lyr",
    "explicit": "rtng",
}


@inject
class M4AMetadataEmbedder(BaseResponsibilityChainLink[EmbedMetadataCommand]):
    def exec(self, options: EmbedMetadataCommand) -> bool:
        if options.file_format is not "m4a":
            return False

        audio_file = MP4(str(options.output_file.resolve()))
        self._embed_basic_metadata(audio_file, options.song)
        self._embed_advanced_metadata(audio_file, options.song)
        audio_file.save()

        return True

    def _embed_basic_metadata(self, audio_file: MP4, song: Song) -> None:
        album_name = song.album_name
        if album_name:
            audio_file[M4A_TAG_PRESET["album"]] = album_name

        audio_file[M4A_TAG_PRESET["artist"]] = song.artist
        audio_file[M4A_TAG_PRESET["albumartist"]] = song.artist
        audio_file[M4A_TAG_PRESET["title"]] = song.name
        audio_file[M4A_TAG_PRESET["date"]] = song.date
        audio_file[M4A_TAG_PRESET["originaldate"]] = song.date

        if len(song.genres) > 0:
            audio_file[M4A_TAG_PRESET["genre"]] = song.genres[0]

        if song.copyright_text:
            audio_file[M4A_TAG_PRESET["copyright"]] = song.copyright_text

        audio_file[M4A_TAG_PRESET["discnumber"]] = [(song.disc_number, song.disc_count)]
        audio_file[M4A_TAG_PRESET["tracknumber"]] = [(song.track_number, song.tracks_count)]
        audio_file[M4A_TAG_PRESET["encodedby"]] = song.publisher

    def _embed_advanced_metadata(self, audio_file: MP4, song: Song) -> Song:
        audio_file[M4A_TAG_PRESET["year"]] = str(song.year)
        audio_file[M4A_TAG_PRESET["explicit"]] = (4 if song.explicit is True else 2,)

        if song.lyrics:
            audio_file[M4A_TAG_PRESET["lyrics"]] = song.lyrics

        if song.cover_url:
            try:
                with urlopen(song.cover_url) as raw_album_art:
                    audio_file[M4A_TAG_PRESET["albumart"]] = [
                        MP4Cover(
                            raw_album_art.read(),
                            imageformat=MP4Cover.FORMAT_JPEG,
                        )
                    ]
            except IndexError:
                pass

        if song.download_url:
            audio_file[M4A_TAG_PRESET["comment"]] = song.download_url
