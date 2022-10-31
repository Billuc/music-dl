from logging import Logger
from kink import inject

from musicdl.common import BaseResponsibilityChainLink
from musicdl.commands.data import CommandOptions, AllowedOperations


@inject
class CheckUpdatesCommand(BaseResponsibilityChainLink[CommandOptions]):
    """
    Check for updates
    """
    
    _logger: Logger
    
    def __init__(self, logger: Logger):
        self._logger = logger


    def exec(self, options: CommandOptions) -> bool:
        if not options.operation == AllowedOperations.CHECK_FOR_UPDATES:
            return False

        raise NotImplementedError
        return True
