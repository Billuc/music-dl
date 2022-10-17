import json
from typing import Any, Dict

from musicdl.common import MusicDLException, is_ffmpeg_installed, CONFIG_PATH
from musicdl.exec.classes import QueryExecuter
from musicdl.exec.data import QueryOptions
from musicdl.exec.extensions import has_special_args


def exec_command(options: QueryOptions) -> None:
    if not has_special_args(options):
        options = _merge_with_config_file(options)
        _check_ffmpeg(options)
        _check_saved(options)

    executer = QueryExecuter()
    executer.exec(options)


def _merge_with_config_file(options: QueryOptions) -> QueryOptions:
    if options.no_config:
        return options

    config = _load_config()

    if not vars(config).get("load_config"):
        return options

    # maybe return a new type with all the properties
    return _merge(options, config)


def _load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise MusicDLException(
            "Config file not found."
            "Run `musicdl --generate-config` to create a default config file"
        )

    with open(CONFIG_PATH, "r", encoding="utf8") as config_file:
        return json.load(config_file) # maybe use object_hook to load into a typed object


def _merge(options: QueryOptions, config: Dict[str, Any]):
    for key in vars(options):
        option_val = vars(options).get(key)
        config_val = config.get(key)

        if option_val is None and config_val is not None:
            vars(options)[key] = config_val

    return options


def _check_ffmpeg(options: QueryOptions):
    if not is_ffmpeg_installed(options.ffmpeg):
        raise MusicDLException(
            "FFmpeg not found. Please run `musicdl --download-ffmpeg` to install it, "
            "or `musicdl --ffmpeg /path/to/ffmpeg` to specify the path to ffmpeg."
        )


def _check_saved(options: QueryOptions):
    if options.query and "saved" in options.query and not options.user_auth:
        raise MusicDLException(
            "You must be logged in to use the saved query. \
Log in by adding the --user-auth flag"
        )

