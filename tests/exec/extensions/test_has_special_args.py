import pytest
from musicdl.exec.data.query_options import QueryOptions

from musicdl.exec.extensions.query_options_extensions import has_special_args


@pytest.fixture
def options_without_special_args():
    return QueryOptions(
        "download", ["test"], [], [], True, None, False, None, 6, None, None, None, "test.musicdl",
        None, None, True, None, False, None, "debug", True, None, None, None, None, True
    )

@pytest.fixture
def options_with_ffmpeg_special_args():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, 
        True,
        None, None, None
    )

@pytest.fixture
def options_with_config_special_args():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
        True,
        None, None
    )

@pytest.fixture
def options_with_updates_special_args():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None,
        True,
        None
    )

@pytest.fixture
def options_with_multiple_special_args():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None,
        True, False, True,
        None
    )

@pytest.fixture
def options_with_special_args_and_others():
    return QueryOptions(
        "download", ["test"], None, None, None, "plop", True, None, None, "16k", "", None, None,
        "{artist} - {album}", "playlist.m3u", None, True, None, True, None, None, None, None,
        True, 
        None, None
    )


def test_has_special_args_false(options_without_special_args):
    assert False == has_special_args(options_without_special_args)


def test_has_special_args_ffmpeg(options_with_ffmpeg_special_args):
    assert True == has_special_args(options_with_ffmpeg_special_args)


def test_has_special_args_config(options_with_config_special_args):
    assert True == has_special_args(options_with_config_special_args)


def test_has_special_args_updates(options_with_updates_special_args):
    assert True == has_special_args(options_with_updates_special_args)


def test_has_special_args_multiple(options_with_multiple_special_args):
    assert True == has_special_args(options_with_multiple_special_args)


def test_has_special_args_and_others(options_with_special_args_and_others):
    assert True == has_special_args(options_with_special_args_and_others)
