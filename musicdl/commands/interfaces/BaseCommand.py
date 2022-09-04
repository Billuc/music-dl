import abc
from typing import List

from musicdl.commands.classes import CommandOptions



class BaseCommand(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'exec') and 
                callable(subclass.exec) or 
                NotImplemented)

    @abc.abstractmethod
    def exec(self, options: CommandOptions) -> None:
        """
        Executes a command

        ### Arguments
        - options: The command options.
        """

        raise NotImplementedError
