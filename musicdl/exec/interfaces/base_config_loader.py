import abc

from musicdl.exec.data import ConfigOptions


class BaseConfigLoader(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'load') and callable(subclass.load) or
            NotImplemented
        )

    @abc.abstractmethod
    def load(self) -> ConfigOptions:
        raise NotImplementedError
    
