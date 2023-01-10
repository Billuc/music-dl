import pytest

from musicdl.common import Song
from musicdl.providers.lyrics import DownloadLyricsCommand
from musicdl.providers.lyrics.classes import MusixmatchLyricsProvider


def test_genius_not_in_providers_should_call_next():
    provider = MusixmatchLyricsProvider()
    song = Song("foo", ["bar"])
    options = DownloadLyricsCommand(song, ["some", "random", "shxt", "just", "not", "mxsixmatch"])
    next_lyrics = "lorem ipsum"
    next = lambda opts: next_lyrics
    
    lyrics = provider.exec(options, next)
    
    assert lyrics == next_lyrics


@pytest.mark.vcr()
def test_basic_get_lyrics():
    provider = MusixmatchLyricsProvider()
    song = Song("In the end", ["Linkin Park"])
    options = DownloadLyricsCommand(song, ["musixmatch"])
    song_prefix = "It doesn't even matter how hard you try"
    next = lambda opts: None
    
    lyrics = provider.exec(options, next)
    
    assert song_prefix in lyrics
    
    
@pytest.mark.vcr()
def test_song_with_different_versions():
    provider = MusixmatchLyricsProvider()
    song = Song("Summer Paradise (French Version)", ["Simple Plan"])
    options = DownloadLyricsCommand(song, ["musixmatch"])
    lyrics_extract = "Et j'ai du mal a croire qu'on se quitte"
    
    lyrics = provider.exec(options, next)
    
    assert lyrics_extract in lyrics