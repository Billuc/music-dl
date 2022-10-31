"""
Download module for the console.
"""

from logging import Logger
from kink import inject

from musicdl.common import BaseResponsibilityChainLink
from musicdl.downloader import BaseDownloadCoordinator

from musicdl.commands.extensions import build_download_settings
from musicdl.commands.data import CommandOptions, AllowedOperations


@inject
class DownloadCommand(BaseResponsibilityChainLink[CommandOptions]):
    _logger: Logger
    _downloader: BaseDownloadCoordinator

    def __init__(self, logger: Logger, downloader: BaseDownloadCoordinator):
        self._logger = logger
        self._downloader = downloader


    def exec(self, options: CommandOptions) -> bool:
        if (not options.operation == AllowedOperations.DOWNLOAD):
            return False
            
        settings = build_download_settings(options)
        self._downloader.download(settings)

        self._logger.info("Downloaded")

        return True
