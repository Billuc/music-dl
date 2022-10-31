import json
from typing import Any, Dict
from kink import inject

from musicdl.common import CONFIG_PATH, MusicDLException

from musicdl.exec.data import ConfigOptions
from musicdl.exec.extensions import generate_config_options
from musicdl.exec.interfaces import BaseConfigLoader


class ConfigLoader(BaseConfigLoader):
    def load(self) -> ConfigOptions:
        config_dict = self._load_file()
        options = generate_config_options(config_dict)
        return options


    def _load_file(self) -> Dict[str, Any]:
        if not CONFIG_PATH.exists():
            raise MusicDLException(
                "Config file not found."
                "Run `musicdl --generate-config` to create a default config file"
            )

        with open(CONFIG_PATH, "r", encoding="utf8") as config_file:
            return json.load(config_file)

