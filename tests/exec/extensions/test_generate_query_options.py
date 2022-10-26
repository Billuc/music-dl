import pytest
from musicdl.exec.data.query_options import QueryOptions

from musicdl.exec.extensions.query_options_extensions import generate_query_options


@pytest.fixture
def dict_success():
    return {
        "audio_providers": ["youtube", "youtube-music"],
        "m3u": "something_m3u",
        "operation": "download",
        "query": ["some_url"]
    }

@pytest.fixture
def empty_dict():
    return {}

@pytest.fixture
def dict_other_keys():
    return {
        "bitrate": "test_bitrate",
        "threads": 2,
        "simple_tui": True,
        "other_key_1": "other_value_1",
        "other_key_2": "other_value_2",
    }



def test_from_dict_success(dict_success):
    options = generate_query_options(dict_success)

    assert ["youtube", "youtube-music"] == options.audio_providers
    assert "something_m3u" == options.m3u
    assert "download" == options.operation
    assert ["some_url"] == options.query
    assert None == options.ffmpeg
    assert None == options.bitrate
    assert None == options.overwrite


def test_from_empty_dict(empty_dict):
    options = generate_query_options(empty_dict)

    assert None == options.audio_providers
    assert None == options.operation
    assert None == options.check_for_updates
    assert None == options.download_ffmpeg
    assert None == options.filter_results
    assert None == options.format


def test_from_dict_with_other_keys(dict_other_keys):
    options = generate_query_options(dict_other_keys)

    assert "test_bitrate" == options.bitrate
    assert 2 == options.threads
    assert True == options.simple_tui
    assert None == options.download_ffmpeg
    assert None == options.filter_results
    assert None == options.format

