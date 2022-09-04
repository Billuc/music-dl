from kink import inject
from logging import Logger

from musicdl.commands import BaseCommand, CommandOptions


@inject
class QueryExecuter:
    """
    Query Parser class that handles the command line arguments.
    """

    _logger: Logger
    _command: BaseCommand

    def __init__(self, logger: Logger, command: BaseCommand):
        self._logger = logger
        self._command = command

    
    def exec(self, options: CommandOptions):
        self._command.exec(options)