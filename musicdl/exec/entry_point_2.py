from musicdl.common.exceptions.MusicDLException import MusicDLException
from .app_init import init_app
from . import QueryParser

def entry_point():
    """
    Console entry point for ytm_dl. This is where the magic happens.
    """

    init_app()

    parser = QueryParser()

    try:
        options = parser.parse_arguments()
        print(options)
    except MusicDLException as ex:
        parser.print_help()
    