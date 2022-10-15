from dataclasses import dataclass
from typing import List


@dataclass
class ProcessExecutionResult:
    returnCode: int
    logs: List[str]
    command: str
    arguments: List[str]