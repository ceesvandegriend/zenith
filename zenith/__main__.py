import datetime
import logging
import logging.handlers
import os
import sys

import paramiko

from . import config


def __daily_log_filename():
    now = datetime.datetime.now()
    log_dir = config['log_dir']
    filename = f'zenith-{now.strftime("%Y%m%d")}.log'
    return os.path.join(log_dir, filename)


def initialize():
    log_dir = config['log_dir']

    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    format = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')

    fh = logging.handlers.TimedRotatingFileHandler(filename=__daily_log_filename(), when="d", backupCount=15)
    fh.rotation_filename = __daily_log_filename
    fh.setFormatter(format)
    fh.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(format)

    if sys.stdout.isatty():
        console.setLevel(logging.INFO)
    else:
        console.setLevel(logging.ERROR)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(console)


def __execute(channel, command):
    logger.info(f'Cmd: {command}')

    f = channel.makefile()
    channel.exec_command(command)
    logger.debug(f.read())


def execute():
    logger = logging.getLogger(__name__)

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect('asrv0000019.griend.eu', 3351)
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.set_combine_stderr(True)
        channel.get_pty()

        __execute(channel, 'whoami')
        __execute(channel, 'id')
        __execute(channel, 'sudo whoami')
        __execute(channel, 'sudo id')



if __name__ == '__main__':
    initialize()

    logger = logging.getLogger(__name__)

    try:
        logger.info(f'base_dir: {config["base_dir"]}')
        logger.info(f'log_dir: {config["log_dir"]}')

        execute()
    except Exception as err:
        logger.fatal(err, exc_info=True)
