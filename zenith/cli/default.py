import logging
import readline

from zenith.chain import Processor

from zenith.command.common import ZenithCommand, LoggingCommand, ReportCommand, AuthenticationCommand, ZenithDirectoryCommand
from zenith.command.database import DatabaseSetupCommand, DatabaseSessionCommand
from zenith.command.node import NodeUUIDCommand

class DefaultProcessor(Processor):
    def __init__(self, level):
        super().__init__()

        self.reporting.append(ReportCommand())

        self.initialization.append(ZenithCommand())
        self.initialization.append(ZenithDirectoryCommand())
        self.initialization.append(LoggingCommand(level))
        self.initialization.append(DatabaseSetupCommand())
        self.initialization.append(DatabaseSessionCommand())
        self.initialization.append(NodeUUIDCommand())

        self.authentication.append(AuthenticationCommand())

        # Setup GNU readline
        # ToDo: read history
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')

    def input(self, prompt: str, value: str = "") -> str:
        readline.set_startup_hook(lambda: readline.insert_text(value))

        try:
            line = input(prompt)
        finally:
            readline.set_startup_hook()

        return line