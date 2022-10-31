import abc
from typing import List
from musicdl.common import BaseResponsibilityChain

from musicdl.commands.data import CommandOptions


class BaseM3UWriter(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'check_installed') and callable(subclass.check_installed) and 
            hasattr(subclass, 'get_local_path') and callable(subclass.get_local_path) and
            hasattr(subclass, 'download') and callable(subclass.download) or
            NotImplemented
        )


    @abc.abstractmethod
    def write(self, 
        file_name: str,
        song_list: List[Song],
        template: str,
        file_extension: str,
        short: bool = False
    ) -> str:
        raise NotImplementedError
