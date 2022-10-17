"""
Execution module, contains the console entry point and different subcommands.
"""

from .utils import init_app
from .classes import QueryExecuter
from .data import QueryOptions
from .entry_point import entry_point as console_entry_point