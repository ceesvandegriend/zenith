from zenith.command.client import *
from zenith.command.database import DatabaseContext
from zenith.process.default import DefaultProcessor


class ClientProcessor(DefaultProcessor):
    def create(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientNotExistCommand())
        self.processing.append(ClientCreateCommand())
        self.execute(context)

    def read(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())
        self.processing.append(ClientReadCommand())
        self.processing.append(ClientDisplayCommand())
        self.execute(context)

    def update(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())
        self.processing.append(ClientReadCommand())
        self.processing.append(ClientEditCommand())
        self.processing.append(ClientUpdateCommand())
        self.processing.append(ClientDisplayCommand())
        self.execute(context)

    def delete(self, name: str) -> None:
        context = DatabaseContext()
        context["client_name"] = name

        self.validating.append(ClientExistCommand())
        self.processing.append(ClientDeleteCommand())
        self.execute(context)

    def list(self) -> None:
        context = DatabaseContext()

        self.processing.append(ClientListCommand())
        self.processing.append(ClientDisplayCommand())
        self.execute(context)
