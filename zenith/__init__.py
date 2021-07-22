import os
import pathlib

config = {}

config["base_dir"] = str(pathlib.Path(__file__).parent.parent.absolute())
config["version"] = "v0.1"

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


if __zenith_dir:
    config["zenith_dir"] = __zenith_dir
    config["db_dir"] = os.path.join(__zenith_dir, "var", "db")
    config["db_filename"] = os.path.join(__zenith_dir, "var", "db", "zenith.db")
    config["log_dir"] = os.path.join(__zenith_dir, "var", "log")
    config["tmp_dir"] = os.path.join(__zenith_dir, "var", "tmp")