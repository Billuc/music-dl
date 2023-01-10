import pytest

from musicdl.common import Song
from musicdl.providers.lyrics import DownloadLyricsCommand
from musicdl.providers.lyrics.classes import GeniusLyricsProvider


def test_genius_not_in_providers_should_call_next():
    provider = GeniusLyricsProvider()
    song = Song("foo", ["bar"])
    options = DownloadLyricsCommand(song, ["some", "random", "shxt", "just", "not", "gxnius"])
    next_lyrics = "lorem ipsum"
    next = lambda opts: next_lyrics
    
    lyrics = provider.exec(options, next)
    
    assert lyrics == next_lyrics


@pytest.mark.vcr()
def test_genius_basic_get_lyrics():
    provider = GeniusLyricsProvider()
    song = Song("In the end", ["Linkin Park"])
    options = DownloadLyricsCommand(song, ["genius"])
    song_prefix = "It starts with one"
    next = lambda opts: None
    
    lyrics = provider.exec(options, next)
    
    assert song_prefix in lyrics
    
    
@pytest.mark.vcr()
def test_genius_song_with_different_versions():
    provider = GeniusLyricsProvider()
    song = Song("Summer Paradise (French Version)", ["Simple Plan"])
    options = DownloadLyricsCommand(song, ["genius"])
    lyrics_extract = "Cet avion qui m'emmene loin de toi"
    next = lambda opts: None
    
    lyrics = provider.exec(options, next)
    
    assert lyrics_extract in lyrics