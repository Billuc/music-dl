
import os
from pathlib import Path
import platform
import shutil
from typing import Optional

from musicdl.common.consts.config import MUSICDL_PATH


DEFAULT_FFMPEG_COMMAND = "ffmpeg"


def is_ffmpeg_installed(ffmpeg: str = DEFAULT_FFMPEG_COMMAND) -> bool:
    """
    Check if ffmpeg is installed.

    ### Arguments
    - ffmpeg: ffmpeg executable to check

    ### Returns
    - True if ffmpeg is installed, False otherwise.
    """

    if ffmpeg != DEFAULT_FFMPEG_COMMAND:
        ffmpeg_path = Path(ffmpeg)
    else:
        global_ffmpeg = shutil.which(DEFAULT_FFMPEG_COMMAND)
            
        if global_ffmpeg is not None:
            ffmpeg_path = Path(global_ffmpeg)
        else:
            ffmpeg_path = get_local_ffmpeg()

    # else check if path to ffmpeg is valid
    # and if ffmpeg has the correct access rights
    return ffmpeg_path.is_file() and os.access(ffmpeg_path, os.X_OK)


def get_local_ffmpeg() -> Optional[Path]:
    """
    Get local ffmpeg binary path.

    ### Returns
    - Path to ffmpeg binary or None if not found.
    """

    return Path(
        MUSICDL_PATH, "ffmpeg" + ".exe" if platform.system() == "Windows" else ""
    )