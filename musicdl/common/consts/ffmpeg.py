
from typing import Dict, List


FFMPEG_URLS: Dict[str, Dict[str, str]] = {
    "windows": {
        "amd64": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/win32-x64",
        "i686": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/win32-ia32",
    },
    "linux": {
        "x86_64": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-x64",
        "x86": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-ia32",
        "arm32": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-arm",
        "aarch64": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/linux-arm64",
    },
    "darwin": {
        "x86_64": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/darwin-x64",
        "arm": "https://github.com/eugeneware/ffmpeg-static/releases/download/b4.4/darwin-arm64",
    },
}

FFMPEG_FORMATS: Dict[str, List[str]] = {
    "mp3": ["-codec:a", "libmp3lame"],
    "flac": ["-codec:a", "flac"],
    "ogg": ["-codec:a", "libvorbis"],
    "opus": ["-codec:a", "libopus"],
    "m4a": ["-codec:a", "aac"],
}