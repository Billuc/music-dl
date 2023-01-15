import pytest

from musicdl.common import SongList, Song
from musicdl.providers.metadata.classes import SpotifyTrackMetadataProvider
from mocks import MockSpotify, MockSpotifyClientProvider

@pytest.fixture
def client_provider():
    return MockSpotifyClientProvider()


def test_spotify_not_in_query_should_return_none(client_provider):
    provider = SpotifyTrackMetadataProvider(client_provider)
    query = "https://music.youtube.com/watch?v=fF_SekY0zQs&feature=share"
    next = lambda query: None
    
    metadata = provider.exec(query, next)
    
    assert metadata is None
    
    
def test_track_not_in_query_should_return_none(client_provider):
    provider = SpotifyTrackMetadataProvider(client_provider)
    query = "https://open.spotify.com/playlist/3pAkXh4EPX5xxU9KtXbONY?si=a109474d022d4a99"
    next = lambda query: None
    
    metadata = provider.exec(query, next)
    
    assert metadata is None
    
    
def test_skip_if_next_returns_list(client_provider):
    provider = SpotifyTrackMetadataProvider(client_provider)
    query = "https://open.spotify.com/track/4Nqn5k7rifapbS2Kt15g8h?si=5497c31b65a8463b"
    result = SongList(None, None, [query], [Song("Fall", ["Neck Deep"])])
    next = lambda query: result
    
    metadata = provider.exec(query, next)
    
    assert metadata == result


def test_basic_get_metadata(client_provider):
    provider = SpotifyTrackMetadataProvider(client_provider)
    query = "https://open.spotify.com/track/4Nqn5k7rifapbS2Kt15g8h?si=5497c31b65a8463b"
    next = lambda query: None
    
    metadata = provider.exec(query, next)
    
    assert len(metadata.songs) == 1
    assert metadata.songs[0].name == MockSpotify.MOCK_TRACK["name"]
    assert metadata.songs[0].cover_url == MockSpotify.MOCK_ALBUM["images"][-1]["url"]
    assert len(metadata.urls) == 1
    assert metadata.urls[0] == query
