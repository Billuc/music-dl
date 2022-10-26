import pytest
from musicdl.commands.classes.AllowedOperations import AllowedOperations
from musicdl.common.consts.logging import DEFAULT_LOGGING_LEVEL, LoggingLevel
from musicdl.exec.data.query_options import QueryOptions

from musicdl.exec.extensions.query_options_extensions import to_command_options


@pytest.fixture
def options_download_command():
    return QueryOptions(
        "download", ["test"], None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None
    )

@pytest.fixture
def options_config_command():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
        True,
        None, None
    )

@pytest.fixture
def options_unknown_command():
    return QueryOptions(
        "zbleu", None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None
    )

@pytest.fixture
def options_none_command():
    return QueryOptions(
        "zbleu", None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None
    )

@pytest.fixture
def options_valid_log_level():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, "WARNING", None, None, None, None, None, None
    )

@pytest.fixture
def options_lowercase_log_level():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, "critical", None, None, None, None, None, None
    )

@pytest.fixture
def options_unknown_log_level():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, "blip", None, None, None, None, None, None
    )

@pytest.fixture
def options_none_log_level():
    return QueryOptions(
        None, None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None, None, None, None
    )

@pytest.fixture
def options_other_arguments():
    return QueryOptions(
        None, None, ["youtube"], None, None, None, None, None, 4, None, None, "my_test_format", None,
        None, "test.m3u", None, None, None, None, None, False, None, None, None, None, None
    )


def test_to_command_options_download(options_download_command):
    cOpts = to_command_options(options_download_command)
    assert AllowedOperations.DOWNLOAD == cOpts.operation

def test_to_command_options_config(options_config_command):
    cOpts = to_command_options(options_config_command)
    assert AllowedOperations.GENERATE_CONFIG == cOpts.operation

def test_to_command_options_unknown(options_unknown_command):
    cOpts = to_command_options(options_unknown_command)
    assert AllowedOperations.UNKNOWN == cOpts.operation

def test_to_command_options_none(options_none_command):
    cOpts = to_command_options(options_none_command)
    assert AllowedOperations.UNKNOWN == cOpts.operation

def test_valid_log_level(options_valid_log_level):
    cOpts = to_command_options(options_valid_log_level)
    assert LoggingLevel.WARNING == cOpts.log_level

def test_lowercase_log_level(options_lowercase_log_level):
    cOpts = to_command_options(options_lowercase_log_level)
    assert DEFAULT_LOGGING_LEVEL == cOpts.log_level

def test_unknown_log_level(options_unknown_log_level):
    cOpts = to_command_options(options_unknown_log_level)
    assert DEFAULT_LOGGING_LEVEL == cOpts.log_level

def test_none_log_level(options_none_log_level):
    cOpts = to_command_options(options_none_log_level)
    assert DEFAULT_LOGGING_LEVEL == cOpts.log_level

def test_other_arguments(options_other_arguments):
    cOpts = to_command_options(options_other_arguments)
    
    assert ["youtube"] == cOpts.audio_providers
    assert 4 == cOpts.threads
    assert "my_test_format" == cOpts.format
    assert "test.m3u" == cOpts.m3u
    assert False == cOpts.simple_tui
