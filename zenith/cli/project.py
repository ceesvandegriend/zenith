from zenith.cli.default import DefaultProcessor
from zenith.command.client import ClientActiveCommand
from zenith.command.project import *


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

        self.execute(context)
        self.display(context)

    def update(self, name: str) -> None:
        context = DatabaseContext()
        context["project_name"] = name

        self.validating.append(ClientActiveCommand())
        self.validating.append(ProjectExistCommand())

        self.processing.append(ProjectReadCommand())
        self.processing.append(ProjectEditCommand())
        self.processing.append(ProjectUpdateCommand())

        self.execute(context)
        self.display(context)

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

        self.execute(context)
        self.display(context)

    def display(self, context: DatabaseContext) -> None:
        if "project" in context:
            project = context["project"]
            if project:
                print(f"""\
Client:      {project.client.client_name}
ID:          {project.project_id}
UUID:        {project.project_uuid}
Name:        {project.project_name}
Active:      {project.project_active}
Description: {project.project_description or ''}

{project.project_remark or ''}""")
        elif "projects" in context:
            projects = context["projects"]
            if len(projects):
                print(f"Client: {projects[0].client.client_name}")
            for project in projects:
                if project.project_active:
                    msg = f"+ {project.project_id} + {project.project_name} + {project.project_uuid}"
                else:
                    msg = f"- {project.project_id} - {project.project_name} - {project.project_uuid}"
                print(msg)
