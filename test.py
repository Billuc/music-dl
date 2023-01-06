from musicdl.providers.lyrics.classes import GeniusLyricsProvider
from musicdl.common import Song
from musicdl.providers.lyrics.data import DownloadLyricsCommand

song = Song(
    "Save Yourself",
    ["ONE OK ROCK"],
    "ONE OK ROCK",
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
