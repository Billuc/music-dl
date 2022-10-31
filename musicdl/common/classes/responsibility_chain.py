from typing import Generic, TypeVar, List

from musicdl.common.interfaces import BaseResponsibilityChain, BaseResponsibilityChainLink


T = TypeVar("T")

class ResponsibilityChain(BaseResponsibilityChain[T]):
    _links: List[BaseResponsibilityChainLink[T]]

    def __init__(self):
        self._links = []


    def _add(self, link: BaseResponsibilityChainLink[T]):
        self._links.append(link)


    def exec(self, options: T) -> bool:
        for link in self._links:
            if link.exec(options):
                return True

        return False


class ResponsibilityChainFactory(Generic[T]):
    _chain: BaseResponsibilityChain[T]

    def __init__(self):
        self._chain = ResponsibilityChain()

    
    def add(self, link: BaseResponsibilityChainLink[T]):
        self._chain._add(link)
        return self


    def build(self) -> BaseResponsibilityChain[T]:
        return self._chain