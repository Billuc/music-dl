from musicdl.common import BaseResponsibilityChain

from musicdl.commands.classes import CommandOptions


class BaseCommandExecuter(BaseResponsibilityChain[CommandOptions]):
    def __init__(self) -> None:
        super().__init__()
