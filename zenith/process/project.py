from zenith.command.database import DatabaseContext
from zenith.command.client import ClientActiveCommand
from zenith.command.project import *
from zenith.process.default import DefaultProcessor


class ProjectProcessor(DefaultProcessor):
    def activate(self, name: str) -> None:
        context = DatabaseContext()
        context["project_name"] = name

        self.validating.append(ClientActiveCommand())
        self.validating.append(ProjectExistCommand())

        self.processing.append(ProjectActivateCommand())

        self.execute(context)

    def create(self, name: str) -> None:
        context = DatabaseContext()
        context["project_name"] = name

        self.validating.append(ClientActiveCommand())
        self.validating.append(ProjectNotExistCommand())

        self.processing.append(ProjectCreateCommand())

        self.execute(context)

    def read(self, name: str) -> None:
        context = DatabaseContext()
        context["project_name"] = name

        self.validating.append(ClientActiveCommand())
        self.validating.append(ProjectExistCommand())

        self.processing.append(ProjectReadCommand())
        self.processing.append(ProjectDisplayCommand())

        self.execute(context)

    def update(self, name: str) -> None:
        context = DatabaseContext()
        context["project_name"] = name

        self.validating.append(ClientActiveCommand())
        self.validating.append(ProjectExistCommand())

        self.processing.append(ProjectReadCommand())
        self.processing.append(ProjectEditCommand())
        self.processing.append(ProjectUpdateCommand())
        self.processing.append(ProjectDisplayCommand())

        self.execute(context)

    def delete(self, name: str) -> None:
        context = DatabaseContext()
        context["project_name"] = name

        self.validating.append(ClientActiveCommand())
        self.validating.append(ProjectExistCommand())

        self.processing.append(ProjectDeleteCommand())

        self.execute(context)

    def list(self) -> None:
        context = DatabaseContext()

        self.validating.append(ClientActiveCommand())

        self.processing.append(ProjectListCommand())
        self.processing.append(ProjectDisplayCommand())

        self.execute(context)
