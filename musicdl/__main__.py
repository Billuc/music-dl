"""
Main module for spotdl. Exports version and main function.
"""

from musicdl.exec import console_entry_point
from ._version import __version__

if __name__ == "__main__":
    console_entry_point()
