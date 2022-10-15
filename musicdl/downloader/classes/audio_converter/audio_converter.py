from pathlib import Path
import shlex
from typing import List

from musicdl.common import MusicDLException, FFMPEG_FORMATS, BaseProcessExecutor
from musicdl.common.data.process_execution_result import ProcessExecutionResult
from musicdl.downloader.classes import DownloaderSettings
from musicdl.downloader.interfaces import BaseAudioConverter, BaseProgressLogger
from musicdl.downloader.consts import TIME_REGEX, DUR_REGEX
from musicdl.utils.ffmpeg import get_ffmpeg_version


class AudioConverter(BaseAudioConverter):
    _progress_logger: BaseProgressLogger
    _process_executor: BaseProcessExecutor

    _ffmpeg_exec: str
    _output_format: str
    _bitrate: str
    _ffmpeg_args: str

    _configured: bool

    def __init__(
        self,
        progress_logger: BaseProgressLogger,
        process_executor: BaseProcessExecutor
    ):
        self._configured = False
        self._progress_logger = progress_logger
        self._process_executor = process_executor

    
    def configure(self, settings: DownloaderSettings) -> None:
        self._ffmpeg_exec = settings.ffmpeg
        self._output_format = settings.output
        self._bitrate = settings.bitrate
        self._ffmpeg_args = settings.ffmpeg_args
        self._configured = True

    
    def convert(self, src_file: Path, output_file: Path) -> None:
        if not self._configured:
            raise MusicDLException("Call to convert when AudioConverter wasn't configured")

        ffmpeg_arguments = self._build_arguments(src_file, output_file)
        try:
            self._execute_conversion(ffmpeg_arguments)
        except:
            output_file.unlink(missing_ok=True)
            raise

    
    def _build_arguments(self, src_file: Path, output_file: Path) -> List[str]:
        arguments: List[str] = [
            "-nostdin",
            "-y",
            "-i",
            str(src_file.resolve()),
            "-movflags",
            "+faststart",
            "-v",
            "debug",
            "-progress",
            "-",
            "-nostats"
        ]

        src_format = src_file.suffix[1:]
        format_related_arguments = self._build_format_related_arguments(src_format)
        bitrate_arguments = self._build_bitrate_arguments()
        user_ffmpeg_arguments = self._build_user_ffmpeg_arguments()

        arguments.extend(format_related_arguments)
        arguments.extend(bitrate_arguments)
        arguments.extend(user_ffmpeg_arguments)
        arguments.append(str(output_file.resolve()))

        return arguments
        

    def _build_format_related_arguments(self, src_format: str) -> List[str]:
        if self._output_format == "opus" and src_format != "webm":
            return ["-c:a", "libopus"]
        
        # TODO : check this part in the original code for opus to opus
        if (
            self._output_format == "m4a" and src_format == "m4a"
            and not self._bitrate and not self._ffmpeg_args
        ):
            return ["-vn", "-c:a", "copy"]

        return FFMPEG_FORMATS.get(self._output_format, [])

    
    def _build_bitrate_arguments(self):
        if not self._bitrate:
            return []

        return ["-b:a", self._bitrate]


    def _build_user_ffmpeg_arguments(self):
        if not self._ffmpeg_args:
            return []

        return shlex.split(self._ffmpeg_args)



    def _execute_conversion(self, ffmpeg_arguments: List[str], tracker) -> None:
        tracker.set(0)

        result = self._process_executor.exec(
            [self._ffmpeg_exec, *ffmpeg_arguments],
            lambda msg: self._update_tracker(msg, tracker)
        )
        self._handle_convert_result(result)

        tracker.set(100)


    def _update_tracker(self, msg: str, tracker) -> None:
        total_dur_match = DUR_REGEX.search(msg)

        if total_dur_match:
            total_dur = to_ms(**total_dur_match.groupdict())  # type: ignore
            tracker.set_duration(total_dur)
            return

        progress_time = TIME_REGEX.search(msg)

        if progress_time:
            elapsed_time = to_ms(**progress_time.groupdict())  # type: ignore
            tracker.set_progress(elapsed_time)


    def _handle_convert_result(self, result: ProcessExecutionResult) -> None:
        if result.returnCode == 0:
            return None

        version = get_ffmpeg_version(result.command)
        raise MusicDLException(f"""
            Error during conversion : 
            Command: {result.command},
            Arguments: {", ".join(result.arguments)},
            Version: {version.version},
            BuildYear: {version.build_year},
            Logs: {"\n".join(result.logs)}
        """)


    