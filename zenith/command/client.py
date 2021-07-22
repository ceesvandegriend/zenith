import logging
import os
import subprocess
import sys
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zenith import config
from zenith.models import Client


def create(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("create() - Start")

    client = Client(client_name=name)
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    session.add(client)
    session.commit()
    logger.info(f"Created: {client}")

    logger.debug("create() - Finish")


def delete(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("delete() - Start")

    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = session.query(Client).filter(Client.client_name == name).one()
    session.delete(client)
    session.commit()

    logger.info(f"Edited: {client}")
    logger.debug("delete() - Finish")


def edit(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("edit() - Start")

    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = session.query(Client).filter(Client.client_name == name).one()

    with tempfile.TemporaryDirectory(dir=config["tmp_dir"]) as tmp:
        logger.info(f"tmp: {tmp}")
        filename = os.path.join(tmp, f"{client.client_name}.txt")

        with open(filename, "wt") as o:
            o.write(f"Id: {client.client_id}\n")
            o.write(f"Uuid: {client.client_uuid}\n")
            o.write(f"Name: {client.client_name}\n")
            o.write(f"Description: {client.client_description  or ''}\n")
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



def help() -> None:
    logger = logging.getLogger(__name__)
    logger.debug("help() - Start")
    logger.info(f"""
zenith client, version {config['version']}

usage: zenith client [command] 

    create [name]  - Creates a client
    delete [name]  - Deletes a client
    edit [name]    - Edits the client
    help           - Display this help text
    info [name]    - Displays the client
    list           - Lists all clients
""")
    logger.debug("help() - Finish")


def info(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("info() - Start")

    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = session.query(Client).filter(Client.client_name == name).one()

    logger.info(f"""Info:
Id: {client.client_id}
Uuid: {client.client_uuid}
Name: {client.client_name}
Description: {client.client_description  or ''}

{client.client_remark or ''}
""")
    session.commit()
    logger.debug("info() - Finish")

def list() -> None:
    logger = logging.getLogger(__name__)
    logger.debug("list() - Start")

    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    clients = session.query(Client).order_by(Client.client_name)

    logger.info(f" * NAME - UUID DESCRIPTION")

    for client in clients:
        name = client.client_name or ""
        uuid = client.client_uuid or ""
        description = client.client_description or ""
        logger.info(f" - {name} - {uuid} {description}")

    session.commit()

    logger.debug("list() - Finish")


def execute(args: list) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"execute() - Start")

    try:
        if "create" == args[0]:
            name = args[1]
            create(name)
        elif "delete" == args[0]:
            name = args[1]
            delete(name)
        elif "edit" == args[0]:
            name = args[1]
            edit(name)
        elif "help" == args[0]:
            help()
        elif "info" == args[0]:
            name = args[1]
            info(name)
        elif "list" == args[0]:
            list()
        else:
            help()
    except IndexError:
        help()

    logger.debug(f"execute() - Finish")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Zenith Command Client - Start")
        execute(sys.argv[1:])
        logger.info(f"Zenith Command Client - Finish")
    except Exception as err:
        logger.fatal(err, exc_info=True)