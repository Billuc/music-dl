from kink import inject
from mutagen.easyid3 import EasyID3, ID3
from mutagen.id3 import APIC as AlbumCover, USLT, COMM as Comment
from urllib.request import urlopen

from musicdl.common import BaseResponsibilityChainLink, Song
from musicdl.downloader.data import EmbedMetadataCommand


@inject
class MP3MetadataEmbedder(BaseResponsibilityChainLink[EmbedMetadataCommand]):
    def exec(self, options: EmbedMetadataCommand) -> bool:
        if options.file_format is not "mp3":
            return False

        audio_file = EasyID3(str(options.output_file.resolve()))
        audio_file.delete()
        self._embed_basic_metadata(audio_file, options.song)
        audio_file.save(v2_version=3)

        audio_file = ID3(str(options.output_file.resolve()))
        self._embed_advanced_metadata(audio_file, options.song)
        audio_file.save(v2_version=3)
        
        return True

    def _embed_basic_metadata(self, audio_file: EasyID3, song: Song) -> None:
        audio_file["title"] = song.name
        audio_file["titlesort"] = song.name
        audio_file["tracknumber"] = [song.track_number, song.tracks_count]
        audio_file["discnumber"] = [song.disc_number, song.disc_count]
        audio_file["artist"] = song.artists
        audio_file["album"] = song.album_name
        audio_file["albumartist"] = song.album_artist
        audio_file["date"] = song.date
        audio_file["originaldate"] = song.date
        audio_file["encodedby"] = song.publisher

        if song.copyright_text:
            audio_file["copyright"] = song.copyright_text

        genres = song.genres
        if len(genres) > 0:
            audio_file["genre"] = genres[0]

    def _embed_advanced_metadata(self, audio_file: ID3, song: Song) -> None:
        if song.cover_url:
            with urlopen(song.cover_url) as raw_album_art:
                audio_file["APIC"] = AlbumCover(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=raw_album_art.read(),
                )

        if song.lyrics:
            audio_file["USLT::'eng'"] = USLT(
                encoding=3, lang="eng", desc="desc", text=song.lyrics
            )

        if song.download_url:
            audio_file.add(Comment(encoding=3, text=song.download_url))
