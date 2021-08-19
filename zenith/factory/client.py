import logging

from zenith.chain import Processor
from zenith.command.client import ClientActivateCommand, ClientExistCommand, ClientNotExistCommand, ClientCreateCommand, \
    ClientReadCommand, ClientUpdateCommand, ClientDeleteCommand, ClientListCommand
from zenith.factory.default import DefaultFactory


class ClientFactory(DefaultFactory):
    log_level = logging.INFO

    @classmethod
    def create_activate(cls, level) -> Processor:
        client = cls.create_default(level)
        client.validating.append(ClientExistCommand())
        client.processing.append(ClientActivateCommand())

        return client

    @classmethod
    def create_create(cls, level) -> Processor:
        client = cls.create_default(level)
        client.validating.append(ClientNotExistCommand())
        client.processing.append(ClientCreateCommand())

        return client

    @classmethod
    def create_read(cls, level) -> Processor:
        client = cls.create_default(level)
        client.validating.append(ClientExistCommand())
        client.processing.append(ClientReadCommand())

        return client

    @classmethod
    def create_update(cls, level) -> Processor:
        client = cls.create_default(level)
        client.validating.append(ClientExistCommand())
        client.processing.append(ClientUpdateCommand())

        return client

    @classmethod
    def create_delete(cls, level) -> Processor:
        client = cls.create_default(level)
        client.validating.append(ClientExistCommand())
        client.processing.append(ClientDeleteCommand())

        return client

    @classmethod
    def create_list(cls, level) -> Processor:
        client = cls.create_default(level)
        client.processing.append(ClientListCommand())

        return client
