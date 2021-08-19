import logging

from zenith.chain import Processor
from zenith.command.common import ReportCommand, ZenithCommand, ZenithDirectoryCommand, LoggingCommand, \
    AuthenticationCommand, ReadlineCommand
from zenith.command.database import DatabaseSetupCommand, DatabaseSessionCommand
from zenith.command.node import NodeUUIDCommand


class DefaultFactory(object):
    log_level = logging.INFO

    @classmethod
    def create_default(cls, level) -> Processor:
        default = Processor()

        default.reporting.append(ReportCommand())

        default.initialization.append(ZenithCommand())
        default.initialization.append(ZenithDirectoryCommand())
        default.initialization.append(LoggingCommand(level))
        default.initialization.append(DatabaseSetupCommand())
        default.initialization.append(DatabaseSessionCommand())
        default.initialization.append(NodeUUIDCommand())
        default.initialization.append(ReadlineCommand())

        default.authentication.append(AuthenticationCommand())

        return default
