import abc
from typing import Generic, TypeVar


T = TypeVar("T")


class BaseResponsibilityChainLink(Generic[T], metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'exec') and callable(subclass.exec) or 
            NotImplemented
        )


    @abc.abstractmethod
    def exec(self, options: T) -> bool:
        raise NotImplementedError



class BaseResponsibilityChain(BaseResponsibilityChainLink[T], metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'add') and callable(subclass.add) and 
            super().__subclasshook__(subclass)
        )


    @abc.abstractmethod
    def _add(self, link: BaseResponsibilityChainLink[T]) -> None:
        raise NotImplementedError
        
        
