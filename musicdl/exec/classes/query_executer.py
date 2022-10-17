from kink import inject
from logging import Logger

from musicdl.commands import BaseCommandExecuter

from musicdl.exec.data import QueryOptions
from musicdl.exec.extensions import to_command_options


@inject
class QueryExecuter:
    """
    Query Parser class that handles the command line arguments.
    """

    _logger: Logger
    _commandExecuter: BaseCommandExecuter

    def __init__(self, logger: Logger, commandExecuter: BaseCommandExecuter):
        self._logger = logger
        self._commandExecuter = commandExecuter

    
    def exec(self, options: QueryOptions):
        command_options = to_command_options(options)

        has_executed = self._commandExecuter.exec(command_options)

        if not has_executed:
            self._logger.error("Something went wrong : Command not found !")


