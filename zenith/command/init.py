"""
Setup Zenith in the current working directory.
"""

import logging
import os
import pathlib
import pprint
import sys

from sqlalchemy import create_engine

from zenith import config
from zenith.models import Base


def __init_directories(config: dict) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"__init_directories() - Start")

    if not os.path.isdir(config["zenith_dir"]):
        os.makedirs(config["zenith_dir"])

        if not os.path.isdir(config["db_dir"]):
            os.makedirs(config["db_dir"])

        if not os.path.isdir(config["log_dir"]):
            os.makedirs(config["log_dir"])

        if not os.path.isdir(config["tmp_dir"]):
            os.makedirs(config["tmp_dir"])

        logger.info(f"Created Zenith directory: {config['zenith_dir']}")

    logger.debug(f"__init_directories() - Finish")


def __init_database(config: dict) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"__init_database() - Start")

    db_filename = config["db_filename"] or None

    print(db_filename)

    if not os.path.isfile(db_filename):
        engine = create_engine(f"sqlite:///{db_filename}")
        Base.metadata.create_all(engine)

        logger.info(f"Created Zenith database: {db_filename}")

    logger.debug(f"__init_database() - Finish")


def execute(directory: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"execute({directory}) - Start")

    zenith_dir = os.path.join(directory, ".zenith")

    config["zenith_dir"] = zenith_dir
    config["db_dir"] = os.path.join(zenith_dir, "var", "db")
    config["db_filename"] = os.path.join(zenith_dir, "var", "db", "zenith.db")
    config["log_dir"] = os.path.join(zenith_dir, "var", "log")
    config["tmp_dir"] = os.path.join(zenith_dir, "var", "tmp")

    __init_directories(config)
    __init_database(config)

    logger.debug(f"execute({zenith_dir}) - Finish")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Zenith Command Init - Start")
        if len(sys.argv) == 2:
            directory = str(pathlib.Path(sys.argv[1]).absolute())
        else:
            directory = str(pathlib.Path(os.getcwd()).absolute())

        execute(directory)

        pprint.pprint(config)

        logger.info(f"Zenith Command Init - Finish")
    except Exception as err:
        logger.fatal(err, exc_info=True)