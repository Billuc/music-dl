from argparse import Namespace
from musicdl.common.exceptions.MusicDLException import MusicDLException
from musicdl.exec import QueryParser

def entry_point():
    """
    Console entry point for ytm_dl. This is where the magic happens.
    """

    # Don't log too much
    set_loggers()
    #check_ffmpeg()

    parser = QueryParser()
    arguments = parser.parse_args()
    _check_arguments(arguments)

    