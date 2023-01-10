import pytest
from musicdl.providers.audio.classes import YoutubeAudioProvider
from musicdl.common import Song

@pytest.mark.vcr()
def test_yt_not_in_providers_should_call_next():
    provider = YoutubeAudioProvider()