from kink import di

from musicdl.common import ResponsibilityChainFactory, init_di as add_common

from musicdl.commands.data import CommandOptions
from musicdl.commands.interfaces import BaseCommandExecuter
from musicdl.commands.commands import GenerateConfigCommand, CheckUpdatesCommand, DownloadFFMPEGCommand


def init_di():
    add_common()

    di[BaseCommandExecuter] = lambda di: (
        ResponsibilityChainFactory[CommandOptions]()
            .add(di[DownloadFFMPEGCommand])
            .add(di[GenerateConfigCommand])
            .add(di[CheckUpdatesCommand])
            .build()
    )
    