import pytest

from musicdl.exec.extensions.config_options_extensions import generate_config_options


@pytest.fixture
def dict_success():
    return {
        "load_config": True,
        "audio_providers": ["youtube", "youtube-music"]
    }

@pytest.fixture
def empty_dict():
    return {}

@pytest.fixture
def dict_other_keys():
    return {
        "bitrate": "test_bitrate",
        "threads": 2,
        "other_key_1": "other_value_1",
        "other_key_2": "other_value_2",
    }


def test_from_dict_success(dict_success):
    config = generate_config_options(dict_success)

    assert True == config.load_config
    assert ["youtube", "youtube-music"] == config.audio_providers
    assert None == config.bitrate
    assert None == config.threads


def test_from_dict_empty(empty_dict):
    config = generate_config_options(empty_dict)

    assert None == config.load_config
    assert None == config.client_id
    assert None == config.filter_results
    assert None == config.threads


def test_from_dict_other_keys(dict_other_keys):
    config = generate_config_options(dict_other_keys)

    assert "test_bitrate" == config.bitrate
    assert 2 == config.threads
    assert None == config.client_id
    assert None == config.no_cache