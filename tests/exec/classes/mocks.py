from logging import Logger

from musicdl.commands.interfaces import BaseCommandExecuter


class MockLogger(Logger):
    def __init__(self):
        super().__init__("mock")
        self.logs = []

    def debug(self, msg):
        self.logs.append(("debug", msg))

    def info(self, msg):
        self.logs.append(("info", msg))

    def warning(self, msg):
        self.logs.append(("warning", msg))

    def error(self, msg):
        self.logs.append(("error", msg))


class MockSuccessCommandExecuter(BaseCommandExecuter):
    def _add(self, link):
        pass

    def exec(self, opts):
        return True


class MockFailureCommandExecuter(BaseCommandExecuter):
    def _add(self, link):
        pass

    def exec(self, opts):
        return False