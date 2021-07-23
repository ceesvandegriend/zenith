import logging
import sys

from zenith import config

import zenith.command.client
import zenith.command.init
import zenith.command.project



def help() -> None:
    logger = logging.getLogger(__name__)
    logger.debug("help() - Start")
    logger.info(f"""
zenith, version {config['version']}

usage: zenith [command] 

    client  - Client commands
    help    - Display this help text
    init    - Init commands
    project - Project commands
""")
    logger.debug("help() - Finish")


def execute(args: list) -> None:
    logger = logging.getLogger(__name__)
    logger.debug(f"execute() - Start")

    try:
        if "client" == args[0]:
            zenith.command.client.execute(args[1:])
        elif "init" == args[0]:
            zenith.command.init.execute(args[1:])
        elif "project" == args[0]:
            zenith.command.project.execute(args[1:])
        else:
            help()
    except IndexError:
        help()

    logger.debug(f"execute() - Finish")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Zenith - Start")
        execute(sys.argv[1:])
        logger.info(f"Zenith - Finish")
    except Exception as err:
        logger.fatal(err, exc_info=True)
