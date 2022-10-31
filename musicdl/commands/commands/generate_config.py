import json
from kink import inject
from logging import Logger

from musicdl.common import BaseResponsibilityChainLink

from musicdl.commands.data import CommandOptions, AllowedOperations
from musicdl.common.consts import CONFIG_PATH
from musicdl.common.consts.config import DEFAULT_CONFIG


@inject
class GenerateConfigCommand(BaseResponsibilityChainLink[CommandOptions]):
    """
    Generate a default config if it doesn't exist.
    Otherwise, asks if the user wants to overwrite current config.
    """
    
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

        
    def exec(self, options: CommandOptions) -> bool:
        if not options.operation == AllowedOperations.GENERATE_CONFIG:
            return False
        
        if CONFIG_PATH.exists():
            self._logger.debug("Config file already existing")
            overwrite = input("Config file already exists. Overwrite ? (y/n): ")

            if overwrite.lower() != "y":
                self._logger.info("Exiting...")
                return None

        with open(CONFIG_PATH, "w", encoding="utf8") as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)

        self._logger.info(f"Config file generated at {CONFIG_PATH}")

        return True


    