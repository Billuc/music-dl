from logging import Logger
from kink import inject

from musicdl.commands.interfaces import BaseCommand
from musicdl.commands.classes import CommandOptions


@inject
class CheckUpdatesCommand(BaseCommand):
    _logger: Logger
    
    def __init__(self, logger: Logger):
        self._logger = logger


    def exec(self, options: CommandOptions) -> None:
        """
        Executes a command : Checks for updates

        ### Arguments
        - options: The command options.
        """

        raise NotImplementedError
