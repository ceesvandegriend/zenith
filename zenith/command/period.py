import logging
import os
import subprocess
import sys
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zenith import config
from zenith.models import Client, Project


def _find_active_client(session) -> Client:
    return session.query(Client).filter(Client.client_active == True).one()


def active(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("active() - Start")
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    # get client
    client = _find_active_client(session)
    project = session.query(Project).filter(Project.client_id == client.client_id, Project.project_name == name).one()
    # set all actives to false
    for active in session.query(Project).filter(Project.project_active == True):
        active.project_active = False
    # set client active
    project.project_active = True
    session.commit()
    logger.info(f"Activated: {project}")
    logger.debug("active() - Finish")


def create(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("create() - Start")
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()

    client = _find_active_client(session)
    project = Project(client_id=client.client_id, project_name=name)
    session.add(project)
    if session.query(Project).filter(Project.project_active == True).count() == 0:
        project.project_active = True
    session.commit()
    logger.info(f"Created: {project}")
    logger.debug("create() - Finish")


def delete(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("delete() - Start")
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = _find_active_client(session)
    project = session.query(Project).filter(Project.client_id == client.client_id, Project.project_name == name).one()
    session.delete(project)
    if session.query(Project).filter(Project.project_active == True).count() == 0:
        logger.warning(f"No active project")
    session.commit()
    logger.info(f"Deleted: {project}")
    logger.debug("delete() - Finish")


def edit(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("edit() - Start")
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = _find_active_client(session)
    project = session.query(Project).filter(Project.client_id == client.client_id, Project.project_name == name).one()

    with tempfile.TemporaryDirectory(dir=config["tmp_dir"]) as tmp:
        logger.debug(f"tmp: {tmp}")
        filename = os.path.join(tmp, f"{project.project_name}.txt")

        with open(filename, "wt") as o:
            o.write(f"Id: {project.project_id}\n")
            o.write(f"Uuid: {project.project_uuid}\n")
            o.write(f"Client: {project.client.client_name}\n")
            o.write(f"Name: {project.project_name}\n")
            o.write(f"Active: {project.project_active}\n")
            o.write(f"Description: {project.project_description  or ''}\n")
            o.write(f"\n{project.project_remark or ''}\n")

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
                            project.project_id = value.strip()
                        elif "Uuid" == key:
                            project.project_uuid = value.strip()
                        elif "Name" == key:
                            project.project_name = value.strip()
                        elif "Description" == key:
                            project.project_description = value.strip()
                else:
                    remark += line + "\n"

            project.project_remark = remark.strip()

    session.commit()
    logger.info(f"Edited: {project}")
    logger.debug("edit() - Finish")



def help() -> None:
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


def info(name: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug("info() - Start")
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = _find_active_client(session)
    project = session.query(Project).filter(Project.client_id == client.client_id, Project.project_name == name).one()
    logger.info(f"""Info:
Id: {project.client_id}
Uuid: {project.project_uuid}
Client: {project.client.client_name}
Name: {project.project_name}
Active: {project.project_active}
Description: {project.project_description  or ''}

{project.project_remark or ''}
""")
    session.commit()
    logger.debug("info() - Finish")


def list() -> None:
    logger = logging.getLogger(__name__)
    logger.debug("list() - Start")
    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Session = sessionmaker(engine)
    session = Session()
    client = _find_active_client(session)
    projects = session.query(Project).filter(Project.client_id == client.client_id).order_by(Project.project_name)
    logger.info(f" | CLIENT | NAME | UUID | DESCRIPTION")

    for project in projects:
        client = project.client.client_name or ""
        name = project.project_name or ""
        uuid = project.project_uuid or ""
        description = project.project_description or ""
        if project.project_active:
            active = "+"
        else:
            active = "-"
        logger.info(f" {active} {client} {active} {name} {active} {uuid} {active} {description}")

    session.commit()
    logger.debug("list() - Finish")


def execute(args: list) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"execute() - Start")

    try:
        if "active" == args[0]:
            name = args[1]
            active(name)
        elif "create" == args[0]:
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
            logger.warning(f"args: {args}")
            help()
    except IndexError:
        logger.warning(f"args: {args}")
        help()

    logger.debug(f"execute() - Finish")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Zenith Command Project - Start")
        execute(sys.argv[1:])
        logger.info(f"Zenith Command Project - Finish")
    except Exception as err:
        logger.fatal(err, exc_info=True)