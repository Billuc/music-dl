from argparse import ArgumentParser
from kink import di

from musicdl.commands import init_di as add_commands
from musicdl.common import init_di as add_common, ResponsibilityChainFactory

from musicdl.exec.classes import ConfigLoader, CheckFFMpegHandler, CheckSavedHandler, HasSpecialArgsHandler
from musicdl.exec.data import QueryOptions
from musicdl.exec.interfaces import BaseConfigLoader, BaseQueryOptionsChecker

def init_di():
    add_common()
    add_commands()

    di[ArgumentParser] = ArgumentParser(
        prog="musicdl",
        description="Download your playlists and songs along with album art and metadata",
    )

    di[BaseConfigLoader] = ConfigLoader()

    di[BaseQueryOptionsChecker] = lambda di: (
        ResponsibilityChainFactory[QueryOptions]()
            .add(di[HasSpecialArgsHandler])
            .add(di[CheckFFMpegHandler])
            .add(di[CheckSavedHandler])
            .build()
    )
