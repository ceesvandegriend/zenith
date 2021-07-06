'''
Usage: python3 -m zenith.common.hash

Generates a BCrypt and Sha512 hash from a password.
'''

import getpass
import logging
import passlib

from .logging import log_initialize


def bcrypthash(password: str) -> str:
    logger = logging.getLogger(__name__)
    logger.debug(f'bcrypthash() - Start')

    hash = passlib.hash.bcrypt.using(rounds=10).hash(password)
    hash = hash.replace("$2b$", "$2a$")
    logger.info(f'bcrypt hash: {hash}')

    logger.debug(f'bcrypthash() - Finish')
    return hash


def sha512hash(password: str) -> str:
    '''
    per the official specification, when the rounds parameter is set to 5000, it may be omitted from the hash string
    '''
    logger = logging.getLogger(__name__)
    logger.debug(f'sha512hash() - Start')

    hash = passlib.hash.sha512_crypt.hash(password, rounds=5000)
    logger.info(f'sha512 hash: {hash}')

    logger.debug(f'sha512hash() - Finish')
    return hash


if __name__ == '__main__':
    log_initialize()
    logger = logging.getLogger(__name__)

    try:
        logger.debug('Zenith Common Hash - Start')

        password = getpass.getpass('Password: ')
        bcrypthash(password)
        sha512hash(password)

        logger.debug('Zenith Common Hash - Finish')
    except Exception as err:
        logger.fatal(err, exc_info=True)
