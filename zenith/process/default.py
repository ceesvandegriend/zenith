
from zenith.chain import Processor

from zenith.command.common import ZenithCommand, LoggingCommand, ReportCommand, AuthenticationCommand, ZenithDirectoryCommand
from zenith.command.database import DatabaseSetupCommand, DatabaseSessionCommand


class DefaultProcessor(Processor):
    def __init__(self):
        super().__init__()

        self.reporting.append(ReportCommand())

        self.initialization.append(ZenithCommand())
        self.initialization.append(ZenithDirectoryCommand())
        self.initialization.append(LoggingCommand())
        self.initialization.append(DatabaseSetupCommand())
        self.initialization.append(DatabaseSessionCommand())

        self.authentication.append(AuthenticationCommand())
