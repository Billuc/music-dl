import subprocess
from typing import Callable, List
from musicdl.common.data import ProcessExecutionResult
from musicdl.common.interfaces import BaseProcessExecutor
from musicdl.common.exceptions import MusicDLException


class ProcessExecutor(BaseProcessExecutor):
    def exec(self, command: List[str], output_callback: Callable[[str], None]) -> ProcessExecutionResult:
        if len(command) == 0:
            raise MusicDLException("Command is empty")

        with subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=False
        ) as process:
            logs: List[str] = []

            while True:
                if process.stdout is None:
                    continue

                stdout_current_line = (
                    process.stdout.readline().decode("utf-8", errors="replace").strip()
                )

                is_finished = stdout_current_line == "" and process.poll() is not None
                if is_finished:
                    break

                logs.append(stdout_current_line)
                output_callback(stdout_current_line)

            return ProcessExecutionResult(
                process.returncode,
                logs,
                command[0],
                command[1:] if len(command) >= 1 else []
            )