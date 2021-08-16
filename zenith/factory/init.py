import logging

from zenith.chain import Processor
from zenith.command.common import ReportCommand, ZenithCommand, ZenithDirectoryCommand, LoggingCommand, \
    AuthenticationCommand
from zenith.command.database import DatabaseSetupCommand, DatabaseSessionCommand, DatabaseCreateCommand
from zenith.command.node import NodeUUIDCommand
from zenith.factory.default import DefaultFactory


class InitFactory(DefaultFactory):
    log_level = logging.INFO

    @classmethod
    def create_init(cls, level = logging.ERROR) -> Processor:
        client = cls.create_default(level)
        client.processing.append(DatabaseCreateCommand())

        return client
