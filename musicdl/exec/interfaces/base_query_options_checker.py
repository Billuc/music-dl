import abc

from musicdl.common import BaseResponsibilityChain
from musicdl.exec.data import QueryOptions


class BaseQueryOptionsChecker(BaseResponsibilityChain[QueryOptions]):
    def __init__(self) -> None:
        super().__init__()