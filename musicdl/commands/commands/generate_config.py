import json
from kink import inject
from logging import Logger

from musicdl.commands.classes import CommandOptions
from musicdl.commands.interfaces import BaseCommand
from musicdl.common.consts import CONFIG_PATH
from musicdl.common.consts.config import DEFAULT_CONFIG


@inject
class GenerateConfigCommand(BaseCommand):
    _logger: Logger

    def __init__(self, logger: Logger):
        super().__init__()
        self._logger = logger

        
    def exec(self, options: CommandOptions) -> None:
        """
        Executes a command : Generate a default config for MusicDL

        ### Arguments
        - options: The command options.
        """
        
        if CONFIG_PATH.exists():
            self._logger.debug("Config file already existing")
            overwrite = input("Config file already exists. Overwrite ? (y/n): ")

            if overwrite.lower() != "y":
                self._logger.info("Exiting...")
                return None

        with open(CONFIG_PATH, "w", encoding="utf8") as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)

        self._logger.info(f"Config file generated at {CONFIG_PATH}")


    