import cProfile
import pstats
from musicdl.common.exceptions.MusicDLException import MusicDLException
from .utils import init_app, exec_command
from .classes import QueryParser, QueryOptions


def entry_point():
    """
    Console entry point for musicdl. This is where the magic happens.
    """

    init_app()
    parser = QueryParser()

    try:
        options = parser.parse_arguments()
    except MusicDLException as ex:
        parser.print_help()
        return None

    if options.profile:
        _execute_with_profile(options)
    else:
        exec_command(options)


def _execute_with_profile(options: QueryOptions) -> None:
    with cProfile.Profile() as profile:
        exec_command(options)

    # Get profile's stats. They can be visualized using snakeviz
    stats = pstats.Stats(profile)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats("musicdl.profile")
