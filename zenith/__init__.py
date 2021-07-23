import datetime
import logging
import logging.handlers
import os
import pathlib
import sys

__licence = """
Zenith - a time tracker

Copyright (C) 2021 Cees van de Griend <c.vande.griend@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

config = {}

config["base_dir"] = str(pathlib.Path(__file__).parent.parent.absolute())
config["version"] = "v0.1"
config["app_name"] = "zenith"

__current_dir = os.getcwd()
__zenith_dir = None

while __zenith_dir is None:
    tmp = os.path.join(__current_dir, '.zenith')

    if os.path.isdir(tmp):
        __zenith_dir = tmp
    else:
        if __current_dir == pathlib.Path(__current_dir).parent:
            break
        else:
            __current_dir = pathlib.Path(__current_dir).parent


def __daily_log_filename():
    now = datetime.datetime.now()
    name = f"{config['app_name']}-{now.strftime('%Y%m%d')}.log"
    filename = os.path.join(config['log_dir'], name)
    return filename


def log_initialize(logfile: bool = True):
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    format = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    console = logging.StreamHandler()
    console.setFormatter(format)
    rootLogger.addHandler(console)

    if sys.stdout.isatty():
        console.setLevel(logging.INFO)
    else:
        console.setLevel(logging.FATAL)

    if logfile:
        format = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s - %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')
        fh = logging.handlers.TimedRotatingFileHandler(filename=__daily_log_filename(), when="d")
        fh.rotation_filename = __daily_log_filename
        fh.setFormatter(format)
        fh.setLevel(logging.DEBUG)
        rootLogger.addHandler(fh)


if __zenith_dir:
    config["zenith_dir"] = __zenith_dir
    config["db_dir"] = os.path.join(__zenith_dir, "var", "db")
    config["db_filename"] = os.path.join(__zenith_dir, "var", "db", "zenith.db")
    config["log_dir"] = os.path.join(__zenith_dir, "var", "log")
    config["tmp_dir"] = os.path.join(__zenith_dir, "var", "tmp")
    log_initialize(logfile=True)
else:
    log_initialize(logfile=False)
