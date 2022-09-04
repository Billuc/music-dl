import sys

from argparse import _ArgumentGroup, ArgumentParser
from kink import inject
from logging import Logger

from musicdl import _version
from musicdl.common import (
    AUDIO_PROVIDERS,
    LYRICS_PROVIDERS,
    OPERATIONS,
    BITRATES,
    NAME_TO_LEVEL,
    FFMPEG_FORMATS,
    FORMAT_VARIABLES,
    MusicDLException,
)
from . import QueryOptions
from musicdl.exec.utils import fromNamespace


@inject
class QueryParser:
    """
    Query Parser class that handles the command line arguments.
    """

    _logger: Logger
    _parser: ArgumentParser

    def __init__(self, logger: Logger, parser: ArgumentParser):
        self._parser = parser
        self._logger = logger

        # Parse main options
        main_options = self._parser.add_argument_group("Main options")
        self._parse_main_options(main_options)

        # Parse ffmpeg options
        ffmpeg_options = self._parser.add_argument_group("FFmpeg options")
        self._parse_ffmpeg_options(ffmpeg_options)

        # Parse output options
        output_options = self._parser.add_argument_group("Output options")
        self._parse_output_options(output_options)

        # Parse misc options
        misc_options = self._parser.add_argument_group("Misc options")
        self._parse_misc_options(misc_options)

        # Parse other options
        other_options = self._parser.add_argument_group("Other options")
        self._parse_other_options(other_options)

        self._logger.debug("QueryParser initialized")


    def parse_arguments(self) -> QueryOptions:
        self._logger.debug("Parsing...")

        arguments = self._parser.parse_args()
        options = fromNamespace(arguments)
        self._check_options(options)

        self._logger.debug("Parsed !")
        return options


    def print_help(self) -> None:
        self._parser.print_help()


    # "Private" methods (do not import those)

    def _check_options(self, opts: QueryOptions):
        if opts is None:
            self._logger.error("Error : no arguments parsed !")
            raise MusicDLException("No arguments parsed")

        if (
            opts.operation is None or opts.query is None
        ) and opts.has_special_args() is False:
            self._logger.error("Error in query : Invalid arguments !")
            raise MusicDLException("Invalid arguments")

        save_file_arg = opts.save_file
        if isinstance(save_file_arg, str) and not save_file_arg.endswith(".musicdl"):
            self._logger.error("Error in query : Save file has to end with .musicdl")
            raise MusicDLException("Save file has to end with .musicdl")

    # Parse options : configure parser

    def _parse_main_options(self, parser: _ArgumentGroup):
        """
        Parse main options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        # Add operation argument
        operation = parser.add_argument(
            "operation",
            nargs="?",
            choices=OPERATIONS,
            help="The operation to perform.",
        )

        # Add query argument
        query = parser.add_argument(
            "query",
            nargs="*",
            type=str,
            help=(
                "Youtube Music URL for a song/playlist/album/artist/etc. to download."
            ),
        )

        # If the program is frozen (to an executable) or we and user didn't pass any arguments,
        # we don't need to parse the query
        if getattr(sys, "frozen", False) and len(sys.argv) < 2:
            # If we are in the frozen env, don't remove the operation from the arg parser
            # parser._remove_action(operation)  # pylint: disable=protected-access
            parser._remove_action(query)  # pylint: disable=protected-access

        # Audio provider argument
        parser.add_argument(
            "--audio",
            dest="audio_providers",
            nargs="*",
            choices=AUDIO_PROVIDERS,
            help="The audio provider to use. You can provide more than one for fallback.",
        )

        # Lyrics provider argument
        parser.add_argument(
            "--lyrics",
            dest="lyrics_providers",
            nargs="*",
            choices=LYRICS_PROVIDERS,
            help="The lyrics provider to use. You can provide more than one for fallback.",
        )

        # Add config argument
        parser.add_argument(
            "--no-config",
            action="store_true",
            help=(
                "Do not use the config file to download songs. "
                "It's located under `C:\\Users\\user\\.musicdl\\config.json` "
                "or `~/.musicdl/config.json` under linux"
            ),
        )

        # Add search query argument
        parser.add_argument(
            "--search-query",
            help=f"The search query to use, available variables: {', '.join(FORMAT_VARIABLES)}",
        )

        # Add don't filter results argument
        parser.add_argument(
            "--dont-filter-results",
            action="store_false",
            dest="filter_results",
            help="Disable filtering results.",
        )

    def _parse_ffmpeg_options(self, parser: _ArgumentGroup):
        """
        Parse ffmpeg options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        # Add ffmpeg executable argument
        parser.add_argument(
            "--ffmpeg",
            help="The ffmpeg executable to use.",
        )

        # Add search threads argument
        parser.add_argument(
            "--threads",
            type=int,
            help="The number of threads to use when downloading songs.",
        )
        # Add constant bit rate argument
        parser.add_argument(
            "--bitrate",
            choices=BITRATES,
            type=str.lower,
            help="The constant bitrate to use for the output file.",
        )

        # Additional ffmpeg arguments
        parser.add_argument(
            "--ffmpeg-args",
            type=str,
            help="Additional ffmpeg arguments passed as a string.",
        )

    def _parse_output_options(self, parser: _ArgumentGroup):
        """
        Parse output options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        # Add output format argument
        parser.add_argument(
            "--format",
            choices=FFMPEG_FORMATS.keys(),
            help="The format to download the song in.",
        )

        # Add save file argument
        parser.add_argument(
            "--save-file",
            type=str,
            help=(
                "The file to save/load the songs data from/to. "
                "It has to end with .musicdl. "
                "If combined with the download operation, it will save the songs data to the file. "
                "Required for save/preload/sync"
            ),
            required=len(sys.argv) > 1 and sys.argv[1] in ["save", "preload", "sync"],
        )

        # Add name format argument
        parser.add_argument(
            "--output",
            type=str,
            help=f"Specify the downloaded file name format, available variables: {', '.join(FORMAT_VARIABLES)}",
        )

        # Add m3u argument
        parser.add_argument(
            "--m3u",
            type=str,
            help="Name of the m3u file to save the songs to.",
        )

        # Add overwrite argument
        parser.add_argument(
            "--overwrite",
            choices={"force", "skip"},
            help="Overwrite existing files.",
        )

        # Option to restrict filenames for easier handling in the shell
        parser.add_argument(
            "--restrict",
            help="Restrict filenames to ASCII only",
            action="store_true",
        )

        # Option to print errors on exit, useful for long playlist
        parser.add_argument(
            "--print-errors",
            help="Print errors (wrong songs, failed downloads etc) on exit, useful for long playlist",
            action="store_true",
        )

        # Option to use sponsor block
        parser.add_argument(
            "--sponsor-block",
            help="Use the sponsor block to download songs from yt/ytm.",
            action="store_true",
        )

    def _parse_misc_options(self, parser: _ArgumentGroup):
        """
        Parse misc options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        # Add verbose argument
        parser.add_argument(
            "--log-level",
            choices=NAME_TO_LEVEL.keys(),
            help="Select log level.",
        )

        # Add simple tui argument
        parser.add_argument(
            "--simple-tui",
            action="store_true",
            help="Use a simple tui.",
        )

        # Add headless argument
        parser.add_argument(
            "--headless",
            action="store_true",
            help="Run in headless mode.",
        )

    def _parse_other_options(self, parser: _ArgumentGroup):
        """
        Parse other options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        parser.add_argument(
            "--download-ffmpeg",
            action="store_true",
            help="Download ffmpeg to musicdl directory.",
        )

        parser.add_argument(
            "--generate-config",
            action="store_true",
            help="Generate a config file. This will ask if you want to overwrite current config if present.",
        )

        parser.add_argument(
            "--check-for-updates", action="store_true", help="Check for new version."
        )

        parser.add_argument(
            "--profile",
            action="store_true",
            help="Run in profile mode. Useful for debugging.",
        )

        parser.add_argument(
            "--version",
            "-v",
            action="version",
            help="Show the version number and exit.",
            version=_version.__version__,
        )
