import logging
import os
import subprocess

from zenith.chain import Command, ContextKeyException
from zenith.command.database import DatabaseContext
from zenith.models import Project


class ProjectActivateCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("activate.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("project_name")

        project_name = context["project_name"]

        for project in context.session.query(Project).filter(Project.project_active is True).all():
            project.project_active = False

        project = context.session.query(Project).filter(Project.project_name == project_name).one()
        project.project_active = True

        logger.info(f"Project[project_name = {project_name}] - activated")
        logger.debug("activate.execute() - Finish")
        return Command.SUCCESS


class ProjectActiveCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("active.execute() - Start")

        project = context.session.query(Project).filter(Project.project_active is True).first()
        if project:
            context["project"] = project
            found = True
        else:
            logger.warning("No active project found")
            found = False

        logger.debug("active.execute() - Finish")
        return found


class ProjectCreateCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("create.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("client_name")

        if "client" not in context:
            raise ContextKeyException("client")

        project_name = context["project_name"]
        client = context["client"]

        project = Project(client_id=client.client_id, project_name=project_name)
        context.session.add(project)

        logger.info(f"Project[project_name = {project_name}] - created")
        logger.debug("create.execute() - Finish")
        return Command.SUCCESS


class ProjectReadCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("read.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("project_name")

        if "client" not in context:
            raise ContextKeyException("client")

        project_name = context["project_name"]
        client = context["client"]

        project = context.session.query(Project).filter(Project.client_id == client.client_id,
                                                        Project.project_name == project_name).one()

        context["project"] = project

        logger.debug("read.execute() - Finish")
        return Command.SUCCESS


class ProjectUpdateCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("update.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("project_name")

        if "client" not in context:
            raise ContextKeyException("client")

        updated = False
        project_name = context["project_name"]
        client = context["client"]

        project = context.session.query(Project).filter(Project.client_id == client.client_id,
                                                        Project.project_name == project_name).one()

        if "project_active" in context:
            project.project_active = context["project_active"]
            updated = True

        if "project_description" in context:
            project.project_description = context["project_description"]
            updated = True

        if "project_remark" in context:
            project.project_remark = context["project_remark"]
            updated = True

        if updated:
            logger.info(f"Project[project_name = {project_name}] - updated")
        else:
            logger.warning(f"Project[project_name = {project_name}] - not updated")

        logger.debug("update.execute() - Finish")
        return updated


class ProjectDeleteCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("delete.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("project_name")

        if "client" not in context:
            raise ContextKeyException("client")

        project_name = context["project_name"]
        client = context["client"]

        project = context.session.query(Project).filter(Project.client_id == client.client_id,
                                                        Project.project_name == project_name).one()
        context.session.delete(project)

        logger.info(f"Project[project_name = {project_name}] - deleted")
        logger.debug("delete.execute() - Finish")
        return Command.SUCCESS


class ProjectListCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("list.execute() - Start")

        if "client" not in context:
            raise ContextKeyException("client")

        client = context["client"]

        projects = context.session.query(Project).filter(Project.client_id == client.client_id).order_by(
            Project.project_name).all()
        context["projects"] = projects

        logger.debug("list.execute() - Finish")
        return Command.SUCCESS


class ProjectExistCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("exist.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("project_name")

        if "client" not in context:
            raise ContextKeyException("client")

        exist = True
        project_name = context["project_name"]
        client = context["client"]

        if context.session.query(Project).filter(Project.client_id == client.client_id,
                                                 Project.project_name == project_name).count() == 0:
            exist = False
            logger.warning(f"Project[project_name = {project_name}] - does not exist")

        logger.debug("exist.execute() - Finish")
        return exist


class ProjectNotExistCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("not_exist.execute() - Start")

        if "project_name" not in context:
            raise ContextKeyException("project_name")

        if "client" not in context:
            raise ContextKeyException("client")

        not_exist = True
        project_name = context["project_name"]
        client = context["client"]

        if context.session.query(Project).filter(Project.client_id == client.client_id,
                                                 Project.project_name == project_name).count() > 0:
            not_exist = False
            logger.warning(f"Project[project_name = {project_name}] - does exist")

        logger.debug("not_exist.execute() - Finish")
        return not_exist


class ProjectDisplayCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("display.execute() - Start")

        if "client" not in context:
            raise ContextKeyException("client")

        client = context["client"]

        if "project" in context:
            project = context["project"]
            logger.info(f"""Project[project_name = {project.project_name}]:
Client:      {project.client.client_name}
ID:          {project.project_id}
UUID:        {project.project_uuid}
Name:        {project.project_name}
Active:      {project.project_active}
Description: {project.project_description or ''}
Remark:      {project.project_remark or ''}""")
        elif "projects" in context:
            projects = context["projects"]
            logger.info(f"Client: {client.client_name}")
            for project in projects:
                if project.project_active:
                    msg = f"+ {project.project_id} + {project.project_name} + {project.project_uuid}"
                else:
                    msg = f"- {project.project_id} - {project.project_name} - {project.project_uuid}"
                logger.info(msg)
        logger.debug("display.execute() - finish")
        return Command.SUCCESS


class ProjectEditCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("edit.execute() - Start")

        if "project" not in context:
            raise ContextKeyException("project")

        changed = False
        project = context["project"]
        filename = os.path.join(context["tmp_dir"], f"{project.project_name}.txt")
        with open(filename, "wt") as txt:
            txt.write(f"Client: {project.client.client_name} (ReadOnly)\n")
            txt.write(f"ID: {project.project_id} (ReadOnly)\n")
            txt.write(f"UUID: {project.project_uuid} (ReadOnly)\n")
            txt.write(f"Name: {project.project_name} (ReadOnly)\n")
            txt.write(f"Active: {project.project_active}\n")
            txt.write(f"Description: {project.project_description or ''}\n")
            txt.write(f"\n{project.project_remark or ''}\n")

        subprocess.call(["/usr/bin/vim", filename])

        with open(filename, "rt") as txt:
            header = True
            remark = ""

            for line in txt.readlines():
                if line == "\n":
                    header = False

                if header:
                    key, value = line.split(":")

                    if key in ["Client", "ID", "UUID", "Name"]:
                        pass
                    elif key in "Active":
                        project_active = value.strip().lower() == "true"
                        if project_active != project.project_active:
                            context["project_active"] = project_active
                            changed = True
                    elif key in "Description":
                        project_description = value.strip()
                        if project_description != project.project_description:
                            context["project_description"] = value.strip()
                            changed = True
                else:
                    remark += line

            # ToDo - Remove extra empty lines
            if len(remark):
                if remark != project.project_remark:
                    context["project_remark"] = remark
                    changed = True

        if os.path.isfile(filename):
            os.remove(filename)

        logger.debug("edit.execute() - finish")
        return changed
