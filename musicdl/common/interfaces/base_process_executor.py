import abc
from typing import Callable, List

from musicdl.common.data import ProcessExecutionResult


class BaseProcessExecutor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'exec') and callable(subclass.exec) or 
            NotImplemented
        )


    @abc.abstractmethod
    def exec(self, command: List[str], output_callback: Callable[[str], None]) -> ProcessExecutionResult:
        raise NotImplementedError