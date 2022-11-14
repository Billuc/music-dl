import abc
from typing import Generic, TypeVar, Callable


T = TypeVar("T")
U = TypeVar("U")


class BasePipelineMiddleware(Generic[T, U], metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'exec') and callable(subclass.exec) or 
            NotImplemented
        )


    @abc.abstractmethod
    def exec(self, options: T, next: Callable[[T], U]) -> U:
        raise NotImplementedError



class BasePipeline(BasePipelineMiddleware[T, U], metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'add') and callable(subclass.add) and 
            super().__subclasshook__(subclass)
        )


    @abc.abstractmethod
    def _add(self, link: BasePipelineMiddleware[T, U]) -> None:
        raise NotImplementedError
        
        
