import datetime
import logging
import logging.handlers
import os
import pathlib
import sys

__log_dir: str = '/tmp'
__app_name: str = 'dummy'


def __daily_log_filename():
    now = datetime.datetime.now()
    name = f'{__app_name}-{now.strftime("%Y%m%d")}.log'
    filename = os.path.join(__log_dir, name)
    return filename


def log_initialize(app_name: str = 'zenith', log_dir: str = os.path.join(pathlib.Path.home(), 'var', 'log')):
    global __log_dir
    global __app_name

    __log_dir = log_dir
    __app_name = app_name

    if not os.path.isdir(__log_dir):
        os.makedirs(__log_dir)

    format = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')

    fh = logging.handlers.TimedRotatingFileHandler(filename=__daily_log_filename(), when="d", backupCount=15)
    fh.rotation_filename = __daily_log_filename
    fh.setFormatter(format)
    fh.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(format)

    if sys.stdout.isatty():
        console.setLevel(logging.INFO)
    else:
        console.setLevel(logging.FATAL)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(console)


if __name__ == '__main__':
    log_initialize()

    logger = logging.getLogger(__name__)

    try:
        logger.info('Zenith Common Logging - Start')

        logger.info('Zenith Common Logging - Finish')
    except Exception as err:
        logger.fatal(err, exc_info=True)
