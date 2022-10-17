from argparse import ArgumentError, ArgumentParser
import sys
import pytest
from musicdl.common.exceptions import MusicDLException
from musicdl.exec.classes import QueryParser
from musicdl.exec.data import QueryOptions

from mocks import MockLogger


class TestQueryExecuter:
    @pytest.fixture
    def arguments_success(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ["musicdl", "download", "test_uri", "--audio", "youtube"])

    @pytest.fixture
    def arguments_no_operation(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ["musicdl", "--download-ffmpeg"])

    @pytest.fixture
    def arguments_missing_query(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ["musicdl", "download"])

    @pytest.fixture
    def arguments_wrong_operation(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ["musicdl", "test"])

    @pytest.fixture
    def arguments_no_arguments(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', [])

    @pytest.fixture
    def arguments_wrong_save_file(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ["musicdl", "download", "test_uri", "--save-file", "test_file.txt"])

    @pytest.fixture
    def argument_parser(self):
        return ArgumentParser(prog="tests", description="parser for tests")


    def test_print_help(self, argument_parser, capsys):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        query_parser.print_help()
        captured_out = capsys.readouterr().out

        assert argument_parser.prog in captured_out
        assert argument_parser.description in captured_out
        assert "query" in captured_out
        assert "--audio" in captured_out


    def test_parse_arguments_success(self, arguments_success, argument_parser):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        options = query_parser.parse_arguments()

        assert options.operation == "download"
        assert options.query == ["test_uri"]
        assert options.audio_providers == ["youtube"]
        assert options.no_config == False


    def test_parse_arguments_no_operation(self, arguments_no_operation, argument_parser):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        options = query_parser.parse_arguments()

        assert options.operation == None
        assert options.query == []
        assert options.audio_providers == None # Still wondering why this one is None and query is '[]'
        assert options.no_config == False
        assert options.download_ffmpeg == True


    def test_parse_arguments_missing_query(self, arguments_missing_query, argument_parser):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        try:
            options = query_parser.parse_arguments()
            assert False
        except MusicDLException as mdlex:
            assert "Invalid arguments" == mdlex.args[0]


    def test_parse_arguments_wrong_operation(self, arguments_wrong_operation, argument_parser):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        try:
            options = query_parser.parse_arguments()
            assert False
        except ArgumentError:
            assert True
        except SystemExit:
            assert True


    def test_parse_arguments_no_arguments(self, arguments_no_arguments, argument_parser):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        try:
            options = query_parser.parse_arguments()
            assert False
        except MusicDLException as mdlex:
            assert "Invalid arguments" == mdlex.args[0]


    def test_parse_arguments_wrong_save_file(self, arguments_wrong_save_file, argument_parser):
        logger = MockLogger()
        query_parser = QueryParser(logger, argument_parser)

        try:
            options = query_parser.parse_arguments()
            assert False
        except MusicDLException as mdlex:
            assert "Save file has to end with .musicdl" == mdlex.args[0]
