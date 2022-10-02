import logging
from logging import Logger
from kink import di
from rich.console import Console

def init_di():
    di[Logger] = logging.getLogger("musicdl")
    di[Console] = Console()
