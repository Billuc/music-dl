from typing import Callable, Generic, TypeVar, List

from musicdl.common.interfaces import BaseResponsibilityChain, BaseResponsibilityChainLink, BasePipeline, BasePipelineMiddleware
from musicdl.common.exceptions import MusicDLException


T = TypeVar("T")
U = TypeVar("U")

class Pipeline(BasePipeline[T, U]):
    _middlewares: List[BasePipelineMiddleware[T, U]]
    _nexts: List[Callable[[T], U]]

    def __init__(self):
        self._middlewares = []
        self._nexts = []


    def _add(self, link: BasePipelineMiddleware[T, U]):
        self._middlewares.append(link)


    def exec(self, options: T, next: Callable[[T], U]) -> U:
        if len(self._middlewares) == 0:
            raise MusicDLException("No middleware configured")

        return self._middlewares[0].exec(options, self._gen_next(0))


    def _gen_next(self, index: int) -> Callable[[T], U]:
        if index >= len(self._middlewares) - 1:
            return lambda t: None

        return lambda t: self._middlewares[index + 1].exec(t, self._gen_next(index + 1))
        


class PipelineFactory(Generic[T, U]):
    _pipeline: BasePipeline[T, U]

    def __init__(self):
        self._pipeline = Pipeline()

    
    def add(self, middleware: BasePipelineMiddleware[T, U]):
        self._pipeline._add(middleware)
        return self


    def build(self) -> BasePipeline[T, U]:
        return self._pipeline