
import os
import platform
import requests
import shutil
import stat
from pathlib import Path
from typing import Optional

from musicdl.common.consts import MUSICDL_PATH, FFMPEG_URLS
from musicdl.common.exceptions import MusicDLException


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


def get_local_ffmpeg() -> Path:
    """
    Get path to local ffmpeg binary.
    """

    return Path(
        MUSICDL_PATH, "ffmpeg" + ".exe" if platform.system() == "Windows" else ""
    )


def download_ffmpeg() -> None:
    """
    Download ffmpeg binary to musicdl directory.

    ### Notes
    - ffmpeg is downloaded from github releases
        for current platform and architecture.
    - executable permission is set for ffmpeg binary.
    """

    ffmpeg_url = _get_ffmpeg_url()
    _download_ffmpeg_binary(ffmpeg_url)
    _set_ffmpeg_permissions()

    return None



def _get_ffmpeg_url() -> str:
    os_name = platform.system().lower()
    os_arch = platform.machine().lower()

    ffmpeg_url = FFMPEG_URLS.get(os_name, {}).get(os_arch)

    if ffmpeg_url is None:
        raise MusicDLException("FFmpeg binary is not available for your system.")

    return ffmpeg_url


def _download_ffmpeg_binary(ffmpeg_url: str) -> None:
    ffmpeg_path = get_local_ffmpeg()
    ffmpeg_binary = requests.get(ffmpeg_url, allow_redirects=True).content

    with open(ffmpeg_path, "wb") as ffmpeg_file:
        ffmpeg_file.write(ffmpeg_binary)

    return None



def _set_ffmpeg_permissions() -> None:
    os_name = platform.system().lower()
    ffmpeg_path = get_local_ffmpeg()

    if os_name in ["linux", "darwin"]:
        ffmpeg_path.chmod(ffmpeg_path.stat().st_mode | stat.S_IEXEC)

    return None


