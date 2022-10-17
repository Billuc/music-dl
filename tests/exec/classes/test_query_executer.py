import pytest
from musicdl.exec.classes import QueryExecuter
from musicdl.exec.data import QueryOptions

from mocks import MockLogger, MockFailureCommandExecuter, MockSuccessCommandExecuter


class TestQueryExecuter:
    @pytest.fixture
    def options(self):
        return QueryOptions(
            "download",
            "test_uri",
            [],
            [],
            False, 
            False, 
            False, 
            "ffmpeg",
            4,
            "test_bitrate",
            "",
            "test_format",
            "test_save_file",
            "test_output",
            "test_m3u",
            "skip",
            False, 
            True, 
            False, 
            "DEBUG",
            False, 
            False, 
            False, 
            False, 
            False, 
            False
        )


    def test_exec_success(self, options):
        logger = MockLogger()
        command_executer = MockSuccessCommandExecuter()
        query_executer = QueryExecuter(logger, command_executer)

        query_executer.exec(options)

        assert len(logger.logs) == 0 


    def test_exec_failure(self, options):
        logger = MockLogger()
        command_executer = MockFailureCommandExecuter()
        query_executer = QueryExecuter(logger, command_executer)

        query_executer.exec(options)

        assert len(logger.logs) == 1
        assert logger.logs[0][0] == "error"