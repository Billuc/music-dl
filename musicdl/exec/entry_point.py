import cProfile
import pstats
from kink import di

from musicdl.common.exceptions.MusicDLException import MusicDLException

from .utils import init_app
from .classes import QueryParser, QueryExecuter
from .data import QueryOptions


def entry_point():
    """
    Console entry point for musicdl. This is where the magic happens.
    """

    init_app()
    
    parser: QueryParser = di[QueryParser]
    executer: QueryExecuter = di[QueryExecuter]

    try:
        options = parser.parse_arguments()
    except MusicDLException as ex:
        parser.print_help()
        return None

    if options.profile:
        _execute_with_profile(executer, options)
    else:
        executer.exec(options)


def _execute_with_profile(executer: QueryExecuter, options: QueryOptions) -> None:
    with cProfile.Profile() as profile:
        executer.exec(options)

    # Get profile's stats. They can be visualized using snakeviz
    stats = pstats.Stats(profile)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats("musicdl.profile")
