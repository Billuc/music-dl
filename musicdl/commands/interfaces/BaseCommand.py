import abc
from typing import List



class BaseCommand(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'exec') and 
                callable(subclass.exec) or 
                NotImplemented)

    @abc.abstractmethod
    def exec(self, query: List[str]) -> None:
        """
        Executes a command

        ### Arguments
        - query: The queried arguments.
        """

        raise NotImplementedError
