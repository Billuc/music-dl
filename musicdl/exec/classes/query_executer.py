from kink import inject
from logging import Logger

from musicdl.common import MusicDLException
from musicdl.commands import BaseCommandExecuter, CommandOptions

from musicdl.exec.data import QueryOptions
from musicdl.exec.extensions import to_command_options, generate_exec_options, has_special_args, to_exec_options
from musicdl.exec.interfaces import BaseConfigLoader, BaseQueryOptionsChecker


@inject
class QueryExecuter:
    """
    Query Parser class that handles the command line arguments.
    """

    _logger: Logger
    _configLoader: BaseConfigLoader
    _queryOptionsChecker: BaseQueryOptionsChecker
    _commandExecuter: BaseCommandExecuter

    def __init__(
        self, 
        logger: Logger, 
        configLoader: BaseConfigLoader,
        queryOptionsChecker: BaseQueryOptionsChecker,
        commandExecuter: BaseCommandExecuter,
    ):
        self._logger = logger
        self._configLoader = configLoader
        self._queryOptionsChecker = queryOptionsChecker
        self._commandExecuter = commandExecuter

    
    def exec(self, options: QueryOptions):
        self._check_options(options)
        commandOptions = self._build_command_options(options)

        has_executed = self._commandExecuter.exec(commandOptions)

        if not has_executed:
            self._logger.error("Something went wrong : Command not found !")


    def _check_options(self, queryOpts: QueryOptions):
        try:
            self._queryOptionsChecker.exec(queryOpts)
        except MusicDLException as e:
            self._logger.error(e)

    
    def _build_command_options(self, queryOpts: QueryOptions) -> CommandOptions:
        if (has_special_args(queryOpts)):
            execOpts = to_exec_options(queryOpts)
            return to_command_options(execOpts)

        configOpts = self._configLoader.load()

        if (queryOpts.no_config or not configOpts.load_config):
            execOpts = to_exec_options(queryOpts)
            return to_command_options(execOpts)
        else:
            execOpts = generate_exec_options(queryOpts, configOpts)
            return to_command_options(execOpts)
       
        
