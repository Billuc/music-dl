from musicdl.common import BaseResponsibilityChain

from musicdl.commands.data import CommandOptions


class BaseCommandExecuter(BaseResponsibilityChain[CommandOptions]):
    def __init__(self) -> None:
        super().__init__()
