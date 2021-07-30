import logging
import os
import subprocess

from zenith.chain import Command, ContextKeyException
from zenith.command.database import DatabaseContext
from zenith.models import Client


class ClientActivateCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("activate.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        client_name = context["client_name"]

        for client in context.session.query(Client).filter_by(client_active = True).all():
            client.client_active = False

        client = context.session.query(Client).filter(Client.client_name == client_name).one()
        client.client_active = True

        logger.info(f"Client[client_name = {client_name}] - activated")
        logger.debug("activate.execute() - Finish")
        return Command.SUCCESS


class ClientActiveCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("active.execute() - Start")

        client = context.session.query(Client).filter(Client.client_active == True).first()

        if client.client_active:
            context["client"] = client
            found = True
        else:
            logger.warning("No active client found")
            found = False

        logger.debug("active.execute() - Finish")
        return found


class ClientCreateCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("create.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        client_name = context["client_name"]

        client = Client(client_name=client_name)
        context.session.add(client)

        logger.info(f"Client[client_name = {client_name}] - created")
        logger.debug("create.execute() - Finish")
        return Command.SUCCESS


class ClientReadCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("read.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        client_name = context["client_name"]

        client = context.session.query(Client).filter(Client.client_name == client_name).one()

        context["client"] = client

        logger.debug("read.execute() - Finish")
        return Command.SUCCESS


class ClientUpdateCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("update.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        updated = False
        client_name = context["client_name"]

        client = context.session.query(Client).filter(Client.client_name == client_name).one()

        if "client_active" in context:
            client.client_active = context["client_active"]
            updated = True

        if "client_description" in context:
            client.client_description = context["client_description"]
            updated = True

        if "client_remark" in context:
            client.client_remark = context["client_remark"]
            updated = True

        if updated:
            logger.info(f"Client[client_name = {client_name}] - updated")
        else:
            logger.warning(f"Client[client_name = {client_name}] - not updated")

        logger.debug("update.execute() - Finish")
        return updated


class ClientDeleteCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("delete.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        client_name = context["client_name"]

        client = context.session.query(Client).filter(Client.client_name == client_name).one()
        context.session.delete(client)

        logger.info(f"Client[client_name = {client_name}] - deleted")
        logger.debug("delete.execute() - Finish")
        return Command.SUCCESS


class ClientListCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("list.execute() - Start")

        clients = context.session.query(Client).order_by(Client.client_name).all()
        context["clients"] = clients

        logger.debug("list.execute() - Finish")
        return Command.SUCCESS


class ClientExistCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("exist.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        exists = True
        client_name = context["client_name"]

        if context.session.query(Client).filter(Client.client_name == client_name).count() == 0:
            exists = False
            logger.warning(f"Client[client_name = {client_name}] - does not exist")

        logger.debug("exist.execute() - Finish")
        return exists


class ClientNotExistCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("not_exist.execute() - Start")

        if "client_name" not in context:
            raise ContextKeyException("client_name")

        not_exist = True
        client_name = context["client_name"]

        if context.session.query(Client).filter(Client.client_name == client_name).count() > 0:
            not_exist = False
            logger.warning(f"Client[client_name = {client_name}] - does exist")

        logger.debug("not_exist.execute() - Finish")
        return not_exist


class ClientEditCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("edit.execute() - Start")

        if "client" not in context:
            raise ContextKeyException("client")

        changed = False
        client = context["client"]
        filename = os.path.join(context["tmp_dir"], f"{client.client_name}.txt")
        with open(filename, "wt") as txt:
            txt.write(f"ID: {client.client_id} (ReadOnly)\n")
            txt.write(f"UUID: {client.client_uuid} (ReadOnly)\n")
            txt.write(f"Name: {client.client_name} (ReadOnly)\n")
            txt.write(f"Active: {client.client_active}\n")
            txt.write(f"Description: {client.client_description or ''}\n")
            txt.write(f"\n{client.client_remark or ''}\n")

        subprocess.call(["/usr/bin/vim", filename])

        with open(filename, "rt") as txt:
            header = True
            remark = ""

            for line in txt.readlines():
                if line == "\n":
                    header = False

                if header:
                    key, value = line.split(":")

                    if key in "ID":
                        pass
                    elif key in "UUID":
                        pass
                    elif key in "Name":
                        pass
                    elif key in "Active":
                        client_active = value.strip().lower() == "true"
                        if client_active != client.client_active:
                            context["client_active"] = client_active
                            changed = True
                    elif key in "Description":
                        client_description = value.strip()
                        if client_description != client.client_description:
                            context["client_description"] = value.strip()
                            changed = True
                else:
                    remark += line

            # ToDo - Remove extra empty lines
            if len(remark):
                if remark != client.client_remark:
                    context["client_remark"] = remark
                    changed = True

        if os.path.isfile(filename):
            os.remove(filename)

        logger.debug("edit.execute() - finish")
        return changed
