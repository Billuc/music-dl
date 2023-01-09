import base64
from urllib.request import urlopen

from kink import inject
from mutagen.flac import Picture
from mutagen.oggvorbis import OggVorbis

from musicdl.common import BaseResponsibilityChainLink, Song
from musicdl.downloader.data import EmbedMetadataCommand

OGG_TAG_PRESET = {
    "album": "album",
    "artist": "artist",
    "date": "date",
    "title": "title",
    "year": "year",
    "originaldate": "originaldate",
    "comment": "comment",
    "group": "group",
    "writer": "writer",
    "genre": "genre",
    "tracknumber": "tracknumber",
    "albumartist": "albumartist",
    "discnumber": "discnumber",
    "cpil": "cpil",
    "albumart": "albumart",
    "encodedby": "encodedby",
    "copyright": "copyright",
    "tempo": "tempo",
    "lyrics": "lyrics",
    "explicit": "explicit",
}


@inject
class OGGMetadataEmbedder(BaseResponsibilityChainLink[EmbedMetadataCommand]):
    def exec(self, options: EmbedMetadataCommand) -> bool:
        if options.file_format is not "ogg":
            return False

        audio_file = OggVorbis(str(options.output_file.resolve()))
        self._embed_basic_metadata(audio_file, options.song)
        self._embed_advanced_metadata(audio_file, options.song)
        self._embed_cover(audio_file, options.song)
        audio_file.save()

        return True

    def _embed_basic_metadata(self, audio_file: OggVorbis, song: Song) -> None:
        album_name = song.album_name
        if album_name:
            audio_file[OGG_TAG_PRESET["album"]] = album_name

        audio_file[OGG_TAG_PRESET["artist"]] = song.artist
        audio_file[OGG_TAG_PRESET["albumartist"]] = song.artist
        audio_file[OGG_TAG_PRESET["title"]] = song.name
        audio_file[OGG_TAG_PRESET["date"]] = song.date
        audio_file[OGG_TAG_PRESET["originaldate"]] = song.date

        if len(song.genres) > 0:
            audio_file[OGG_TAG_PRESET["genre"]] = song.genres[0]

        if song.copyright_text:
            audio_file[OGG_TAG_PRESET["copyright"]] = song.copyright_text

        audio_file[OGG_TAG_PRESET["discnumber"]] = str(song.disc_number).zfill(
            len(str(song.disc_count))
        )
        audio_file[OGG_TAG_PRESET["tracknumber"]] = str(song.track_number).zfill(
            len(str(song.tracks_count))
        )

    def _embed_advanced_metadata(self, audio_file: OggVorbis, song: Song) -> Song:
        audio_file[OGG_TAG_PRESET["year"]] = str(song.year)

        if song.lyrics:
            audio_file[OGG_TAG_PRESET["lyrics"]] = song.lyrics

        if song.download_url:
            audio_file[OGG_TAG_PRESET["comment"]] = song.download_url

    def _embed_cover(self, audio_file: OggVorbis, song: Song) -> None:
        if song.cover_url is None:
            return

        image = Picture()
        image.type = 3
        image.desc = "Cover"
        image.mime = "image/jpeg"

        with urlopen(song.cover_url) as raw_album_art:
            image.data = raw_album_art.read()

        image_data = image.write()
        encoded_data = base64.b64encode(image_data)
        vcomment_value = encoded_data.decode("ascii")
        audio_file["metadata_block_picture"] = [vcomment_value]
