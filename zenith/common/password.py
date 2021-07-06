import logging
import os
import pathlib
import random
import string
import sys

from .logging import log_initialize


def generate(length: int = 64) -> str:
    logger = logging.getLogger(__name__)
    logger.debug(f'generate() - Start')

    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    password = "".join(random.choices(characters, k=length))

    logger.info(f'Generated password: {password}')
    logger.debug(f'generate() - Finish')

    return password


if __name__ == '__main__':
    log_initialize()
    logger = logging.getLogger(__name__)

    try:
        logger.debug('Zenith Common Password - Start')
        length = 64

        if len(sys.argv) == 2:
            length = int(sys.argv[1])

        generate(length)

        logger.debug('Zenith Common Password - Finish')
    except Exception as err:
        logger.fatal(err, exc_info=True)
