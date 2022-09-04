from argparse import ArgumentParser
from logging import Logger
import logging
from kink import di
from rich.console import Console

def init_di():
    di[ArgumentParser] = ArgumentParser(
        prog="musicdl",
        description="Download your playlists and songs along with album art and metadata",
    )

    di[Logger] = logging.getLogger("musicdl")
    di[Console] = Console()
