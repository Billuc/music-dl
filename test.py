from musicdl.providers.lyrics.classes import GeniusLyricsProvider
from musicdl.common import Song
from musicdl.providers.lyrics.data import DownloadLyricsCommand

song = Song(
    "Arrow of Love",
    ["Electric Callboy"],
    "Electric Callboy",
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None
)

command = DownloadLyricsCommand(song, ["genius"])

provider = GeniusLyricsProvider()
lyrics = provider.exec(command, None)

print(lyrics)
