from argparse import ArgumentParser
import logging
from logging import Logger
from kink import di
from rich.console import Console

from musicdl.commands import init_di as add_commands
from musicdl.common import init_di as add_common

def init_di():
    add_common()
    add_commands()

    di[ArgumentParser] = ArgumentParser(
        prog="musicdl",
        description="Download your playlists and songs along with album art and metadata",
    )
