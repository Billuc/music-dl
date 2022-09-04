from logging import Logger

from musicdl.commands.interfaces import BaseCommand
from musicdl.commands.classes import CommandOptions



class DownloadFFMPEGCommand(BaseCommand):
    _logger: Logger
    
    def __init__(self, logger: Logger):
        self._logger = logger


    def exec(self, options: CommandOptions) -> None:
        """
        Executes a command : Download FFMpeg

        ### Arguments
        - options: The command options.
        """

        raise NotImplementedError
