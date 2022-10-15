import logging
from logging import Logger
from kink import di

from musicdl.common.classes import ProcessExecutor
from musicdl.common.interfaces import BaseProcessExecutor

def init_di():
    di[Logger] = logging.getLogger("musicdl")
    di[BaseProcessExecutor] = ProcessExecutor()
