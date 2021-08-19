import logging

from zenith.chain import Processor
from zenith.command.database import DatabaseCreateCommand
from zenith.factory.default import DefaultFactory


class InitFactory(DefaultFactory):
    log_level = logging.INFO

    @classmethod
    def create_init(cls, level) -> Processor:
        client = cls.create_default(level)
        client.processing.append(DatabaseCreateCommand())

        return client
