import logging
import os
import subprocess
import sys
import tempfile

from zenith import config
from zenith.command1 import Command
from zenith.models import Client


class ClientCommand(Command):
    def __init__(self):
        logger = logging.getLogger(__name__)
        logger.debug("__init__() - Start")
        super().__init__()
        logger.debug("__init__() - Finish")


    def active(self, name: str) -> None:
        """
        Activates a client.

        :param name: the name of the client
        """
        logger = logging.getLogger(__name__)
        logger.debug("active() - Start")
        session = self.create_session()
        # get client
        client = session.query(Client).filter(Client.client_name == name).one()
        # set all actives to false
        for active in session.query(Client).filter(Client.client_active == True):
            active.client_active = False
        # set client active
        client.client_active = True
        session.commit()
        logger.info(f"Activated: {client}")
        logger.debug("active() - Finish")

    def create(self, name: str) -> None:
        """
        Create a new client.

        :param name:  the name of the client
        """
        logger = logging.getLogger(__name__)
        logger.debug("create() - Start")
        client = Client(client_name=name)
        session = self.create_session()
        session.add(client)
        if session.query(Client).filter(Client.client_active == True).count() == 0:
            client.client_active = True
        session.commit()
        logger.info(f"Created: {client}")
        logger.debug("create() - Finish")

    def delete(self, name: str) -> None:
        """
        Deletes a client.

        :param name: the name of the client.
        """
        logger = logging.getLogger(__name__)
        logger.debug("delete() - Start")
        session = self.create_session()
        client = session.query(Client).filter(Client.client_name == name).one()
        session.delete(client)
        if session.query(Client).filter(Client.client_active == True).count() == 0:
            logger.warning(f"No active client")
        session.commit()
        logger.info(f"Deleted: {client}")
        logger.debug("delete() - Finish")

    def edit(self, name: str) -> None:
        """
        Edits a client.

        :param name: the name of the client
        """
        logger = logging.getLogger(__name__)
        logger.debug("edit() - Start")
        session = self.create_session()
        client = session.query(Client).filter(Client.client_name == name).one()

        with tempfile.TemporaryDirectory(dir=config["tmp_dir"]) as tmp:
            logger.debug(f"tmp: {tmp}")
            filename = os.path.join(tmp, f"{client.client_name}.txt")

            with open(filename, "wt") as o:
                o.write(f"Id: {client.client_id}\n")
                o.write(f"Uuid: {client.client_uuid}\n")
                o.write(f"Name: {client.client_name}\n")
                o.write(f"Active: {client.client_active}\n")
                o.write(f"Description: {client.client_description or ''}\n")
                o.write(f"\n{client.client_remark or ''}\n")

            subprocess.call(["/usr/bin/vim", filename])

        with open(filename, "rt") as i:
            remark = ""
            header = True

            for line in i.readlines():
                line = line.strip()

                if header:
                    if "" == line:
                        header = False
                    else:
                        key, value = line.split(":", 2)
                        if "Id" == key:
                            client.client_id = value.strip()
                        elif "Uuid" == key:
                            client.client_uuid = value.strip()
                        elif "Name" == key:
                            client.client_name = value.strip()
                        elif "Description" == key:
                            client.client_description = value.strip()
                else:
                    remark += line + "\n"

            client.client_remark = remark.strip()

        session.commit()
        logger.info(f"Edited: {client}")
        logger.debug("edit() - Finish")

    def help(self) -> None:
        """
        Displays a help messag.
        """
        logger = logging.getLogger(__name__)
        logger.debug("help() - Start")
        logger.info(f"""
zenith client, version {config['version']}

usage: zenith client [command] 

    active [name]  - Activates a client and deactivates all others
    create [name]  - Creates a client
    delete [name]  - Deletes a client
    edit [name]    - Edits the client
    help           - Display this help text
    info [name]    - Displays the client
    list           - Lists all clients
""")
        logger.debug("help() - Finish")

    def info(self, name: str) -> None:
        """
        Shows the details of a client.

        :param name: the name of the client
        """
        logger = logging.getLogger(__name__)
        logger.debug("info() - Start")
        session = self.create_session()
        client = session.query(Client).filter(Client.client_name == name).one()
        logger.info(f"""Info:
Id: {client.client_id}
Uuid: {client.client_uuid}
Name: {client.client_name}
Active: {client.client_active}
Description: {client.client_description or ''}

{client.client_remark or ''}
""")
        session.commit()
        logger.debug("info() - Finish")

    def list(self) -> None:
        logger = logging.getLogger(__name__)
        logger.debug("list() - Start")
        session = self.create_session()
        clients = session.query(Client).order_by(Client.client_name)
        logger.info(f" | NAME | UUID | DESCRIPTION")

        for client in clients:
            name = client.client_name or ""
            uuid = client.client_uuid or ""
            description = client.client_description or ""
            if client.client_active:
                active = "+"
            else:
                active = "-"
            logger.info(f" {active} {name} {active} {uuid} {active} {description}")

        session.commit()
        logger.debug("list() - Finish")

    def execute(self, args: list) -> None:
        """
        Executes the logic.

        :param args: commandline parameters
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"execute() - Start")

        try:
            if "active" == args[0]:
                name = args[1]
                self.active(name)
            elif "create" == args[0]:
                name = args[1]
                self.create(name)
            elif "delete" == args[0]:
                name = args[1]
                self.delete(name)
            elif "edit" == args[0]:
                name = args[1]
                self.edit(name)
            elif "help" == args[0]:
                self.help()
            elif "info" == args[0]:
                name = args[1]
                self.info(name)
            elif "list" == args[0]:
                self.list()
            else:
                logger.warning(f"args: {args}")
                self.help()
        except IndexError:
            logger.warning(f"args: {args}")
            self.help()

        logger.debug(f"execute() - Finish")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Zenith Command Client - Start")

        command = ClientCommand()
        command.execute(sys.argv[1:])

        logger.info(f"Zenith Command Client - Finish")
    except Exception as err:
        logger.fatal(err, exc_info=True)
