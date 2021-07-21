"""
Setup Zenith in the current working directory.
"""

import logging
import os
import pathlib
import pprint
import sys


from zenith import config


def __init_directories(directory: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"__init_directories({directory}) - Start")

    db_dir = os.path.join(directory, "var", "db")
    log_dir = os.path.join(directory, "var", "log")
    tmp_dir = os.path.join(directory, "var", "tmp")

    if not os.path.isdir(directory):
        os.makedirs(directory)

        if not os.path.isdir(db_dir):
            os.makedirs(db_dir)

        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir)

        logger.info(f"Created Zenith directory: {directory}")

    logger.debug(f"__init_directories({directory}) - Finish")


def execute(directory: str) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"execute({directory}) - Start")

    zenith_dir = os.path.join(directory, ".zenith")
    __init_directories(zenith_dir)

    config["zenith_dir"] = zenith_dir
    config["db_dir"] = os.path.join(zenith_dir, "var", "db")
    config["log_dir"] = os.path.join(zenith_dir, "var", "log")
    config["tmp_dir"] = os.path.join(zenith_dir, "var", "tmp")

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