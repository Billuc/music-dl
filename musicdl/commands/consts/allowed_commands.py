from enum import Enum

class AllowedCommands(Enum):
    UNKNOWN = 0
    CHECK_FOR_UPDATES = 1
    DOWNLOAD_FFMPEG = 2
    GENERATE_CONFIG = 3
    DOWNLOAD = 4
    SAVE = 5
    SYNC = 6
    WEB = 7


