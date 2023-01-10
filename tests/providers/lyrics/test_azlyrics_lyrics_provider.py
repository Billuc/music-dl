import pytest

from musicdl.common import Song
from musicdl.providers.lyrics import DownloadLyricsCommand
from musicdl.providers.lyrics.classes import AZLyricsLyricsProvider


def test_azlyrics_not_in_providers_should_call_next():
    provider = AZLyricsLyricsProvider()
    song = Song("foo", ["bar"])
    options = DownloadLyricsCommand(song, ["some", "random", "shxt", "just", "not", "azlxrics"])
    next_lyrics = "lorem ipsum"
    next = lambda opts: next_lyrics
    
    lyrics = provider.exec(options, next)
    
    assert lyrics == next_lyrics


@pytest.mark.vcr()
def test_azlyrics_basic_get_lyrics():
    provider = AZLyricsLyricsProvider()
    song = Song("In the end", ["Linkin Park"])
    options = DownloadLyricsCommand(song, ["azlyrics"])
    song_prefix = "It starts with one"
    next = lambda opts: None
    
    lyrics = provider.exec(options, next)
    
    assert song_prefix in lyrics
    
    
@pytest.mark.vcr()
def test_azlyrics_song_with_different_versions():
    provider = AZLyricsLyricsProvider()
    song = Song("Summer Paradise (French Version)", ["Simple Plan"])
    options = DownloadLyricsCommand(song, ["azlyrics"])
    lyrics_extract = "Cet avion qui m'emmène loin de toi"
    next = lambda opts: None
    
    lyrics = provider.exec(options, next)
    
    assert lyrics_extract in lyrics