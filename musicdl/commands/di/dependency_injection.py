from kink import di, Container

from musicdl.commands.classes import CommandOptions
from musicdl.commands.consts.allowed_commands import AllowedCommands
from musicdl.commands.interfaces import BaseCommand
from musicdl.commands.commands import GenerateConfigCommand, CheckUpdatesCommand, DownloadFFMPEGCommand


def init_di(operation: AllowedCommands, options: CommandOptions):
    _set_command_implementation(di, operation)


def _set_command_implementation(di: Container, operation: AllowedCommands):
    if (operation == AllowedCommands.CHECK_FOR_UPDATES):
        di[BaseCommand] = di[CheckUpdatesCommand]
    elif (operation == AllowedCommands.DOWNLOAD_FFMPEG):
        di[BaseCommand] = di[DownloadFFMPEGCommand]
    elif (operation == AllowedCommands.GENERATE_CONFIG):
        di[BaseCommand] = di[GenerateConfigCommand] 
    