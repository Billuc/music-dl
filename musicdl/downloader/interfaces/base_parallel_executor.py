import abc
from typing import Any, Callable, Coroutine, List, Tuple


class BaseParallelExecutor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'configure') and 
            callable(subclass.configure) and 
            hasattr(subclass, 'execute_function') and 
            callable(subclass.execute_function) and 
            hasattr(subclass, 'execute_tasks') and 
            callable(subclass.execute_tasks) or 
            NotImplemented
        )

    @abc.abstractmethod
    def configure(self, threads: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def execute_function(self, function: Callable, *args: List[Any], return_exceptions: bool) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def execute_tasks(self, tasks: List[Coroutine]) -> Any:
        raise NotImplementedError
