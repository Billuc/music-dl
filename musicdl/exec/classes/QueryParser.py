import sys

from argparse import _ArgumentGroup, ArgumentParser, Namespace

from musicdl import _version
from musicdl.common.exceptions import MusicDLException
from musicdl.common.options.QueryOptions import QueryOptions
from musicdl.utils.ffmpeg import FFMPEG_FORMATS
from musicdl.utils.config import DEFAULT_CONFIG
from musicdl.utils.formatter import VARS
from musicdl.classes.downloader import (
    AUDIO_PROVIDERS,
    LYRICS_PROVIDERS,
    NAME_TO_LEVEL
)


OPERATIONS = ["download", "save", "preload", "sync"]


class QueryParser():
    """
    Query Parser class that handles the command line arguments.
    """

    parser: ArgumentParser

    def __init__(self):
        self.parser = ArgumentParser(
            prog="musicdl",
            description="Download your playlists and songs along with album art and metadata",
        )

        # Parse main options
        main_options = self.parser.add_argument_group("Main options")
        self._parse_main_options(main_options)

        # Parse ffmpeg options
        ffmpeg_options = self.parser.add_argument_group("FFmpeg options")
        self._parse_ffmpeg_options(ffmpeg_options)

        # Parse output options
        output_options = self.parser.add_argument_group("Output options")
        self._parse_output_options(output_options)

        # Parse misc options
        misc_options = self.parser.add_argument_group("Misc options")
        self._parse_misc_options(misc_options)

        # Parse other options
        other_options = self.parser.add_argument_group("Other options")
        self._parse_other_options(other_options)


    def parse_arguments(self):
        arguments = self.parser.parse_args()
        queryOptions = QueryOptions()
    
    
    # "Private" methods (do not import those)

    def _check_arguments(args: Namespace):
        if args is None:
            raise MusicDLException("No arguments passed")

        if (
            (args.get("operation") is None or args.get("query") is None) and
            _has_special_args(args) is False
        ):
            raise MusicDLException("Invalid arguments")

        save_file_arg = args["save_file"]
        if isinstance(save_file_arg, str) and not save_file_arg.endswith(".musicdl"):
            raise MusicDLException("Save file has to end with .musicdl")


    def _parse_main_options(parser: _ArgumentGroup):
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

        is_frozen = getattr(sys, "frozen", False)

        # If the program is frozen or we and user didn't pass any arguments,
        # we don't need to parse the query
        if (is_frozen and len(sys.argv) < 2):
            # If we are in the frozen env, don't remove the operation from the arg parser
            # parser._remove_action(operation)  # pylint: disable=protected-access
            parser._remove_action(query)  # pylint: disable=protected-access

        # Audio provider argument
        parser.add_argument(
            "--audio",
            dest="audio_providers",
            nargs="*",
            choices=AUDIO_PROVIDERS,
            default=DEFAULT_CONFIG["audio_providers"],
            help="The audio provider to use. You can provide more than one for fallback.",
        )

        # Lyrics provider argument
        parser.add_argument(
            "--lyrics",
            dest="lyrics_providers",
            nargs="*",
            choices=LYRICS_PROVIDERS.keys(),
            default=DEFAULT_CONFIG["lyrics_providers"],
            help="The lyrics provider to use. You can provide more than one for fallback.",
        )

        # Add config argument
        parser.add_argument(
            "--config",
            action="store_true",
            help=(
                "Use the config file to download songs. "
                "It's located under `C:\\Users\\user\\.ytm_dl\\config.json` "
                "or `~/.ytm_dl/config.json` under linux"
            ),
        )

        # Add search query argument
        parser.add_argument(
            "--search-query",
            default=DEFAULT_CONFIG["search_query"],
            help=f"The search query to use, available variables: {', '.join(VARS)}",
        )

        # Add don't filter results argument
        parser.add_argument(
            "--dont-filter-results",
            action="store_false",
            dest="filter_results",
            default=DEFAULT_CONFIG["filter_results"],
            help="Disable filtering results.",
        )


    def _parse_ffmpeg_options(parser: _ArgumentGroup):
        """
        Parse ffmpeg options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        # Add ffmpeg executable argument
        parser.add_argument(
            "--ffmpeg",
            default=DEFAULT_CONFIG["ffmpeg"],
            help="The ffmpeg executable to use.",
        )

        # Add search threads argument
        parser.add_argument(
            "--threads",
            default=DEFAULT_CONFIG["threads"],
            type=int,
            help="The number of threads to use when downloading songs.",
        )
        # Add constant bit rate argument
        parser.add_argument(
            "--bitrate",
            choices=[
                "8k",
                "16k",
                "24k",
                "32k",
                "40k",
                "48k",
                "64k",
                "80k",
                "96k",
                "112k",
                "128k",
                "160k",
                "192k",
                "224k",
                "256k",
                "320k",
            ],
            default=DEFAULT_CONFIG["bitrate"],
            type=str.lower,
            help="The constant bitrate to use for the output file.",
        )

        # Additional ffmpeg arguments
        parser.add_argument(
            "--ffmpeg-args",
            type=str,
            default=DEFAULT_CONFIG["ffmpeg_args"],
            help="Additional ffmpeg arguments passed as a string.",
        )


    def _parse_output_options(parser: _ArgumentGroup):
        """
        Parse output options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        # Add output format argument
        parser.add_argument(
            "--format",
            choices=FFMPEG_FORMATS.keys(),
            default=DEFAULT_CONFIG["format"],
            help="The format to download the song in.",
        )

        # Add save file argument
        parser.add_argument(
            "--save-file",
            type=str,
            default=DEFAULT_CONFIG["save_file"],
            help=(
                "The file to save/load the songs data from/to. "
                "It has to end with .ytmdl. "
                "If combined with the download operation, it will save the songs data to the file. "
                "Required for save/preload/sync"
            ),
            required=len(sys.argv) > 1 and sys.argv[1] in ["save", "preload", "sync"],
        )

        # Add name format argument
        parser.add_argument(
            "--output",
            type=str,
            default=DEFAULT_CONFIG["output"],
            help=f"Specify the downloaded file name format, available variables: {', '.join(VARS)}",
        )

        # Add m3u argument
        parser.add_argument(
            "--m3u",
            type=str,
            default=DEFAULT_CONFIG["m3u"],
            help="Name of the m3u file to save the songs to.",
        )

        # Add overwrite argument
        parser.add_argument(
            "--overwrite",
            choices={"force", "skip"},
            default=DEFAULT_CONFIG["overwrite"],
            help="Overwrite existing files.",
        )

        # Option to restrict filenames for easier handling in the shell
        parser.add_argument(
            "--restrict",
            default=DEFAULT_CONFIG["restrict"],
            help="Restrict filenames to ASCII only",
            action="store_true",
        )

        # Option to print errors on exit, useful for long playlist
        parser.add_argument(
            "--print-errors",
            default=DEFAULT_CONFIG["print_errors"],
            help="Print errors (wrong songs, failed downloads etc) on exit, useful for long playlist",
            action="store_true",
        )

        # Option to use sponsor block
        parser.add_argument(
            "--sponsor-block",
            default=DEFAULT_CONFIG["sponsor_block"],
            help="Use the sponsor block to download songs from yt/ytm.",
            action="store_true",
        )


    def _parse_misc_options(parser: _ArgumentGroup):
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
            default=DEFAULT_CONFIG["simple_tui"],
            help="Use a simple tui.",
        )

        # Add headless argument
        parser.add_argument(
            "--headless",
            action="store_true",
            default=DEFAULT_CONFIG["headless"],
            help="Run in headless mode.",
        )


    def _parse_other_options(parser: _ArgumentGroup):
        """
        Parse other options from the command line.

        ### Arguments
        - parser: The argument parser to add the options to.
        """

        parser.add_argument(
            "--download-ffmpeg",
            action="store_true",
            help="Download ffmpeg to ytm_dl directory.",
        )

        parser.add_argument(
            "--generate-config",
            action="store_true",
            help="Generate a config file. This will overwrite current config if present.",
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

