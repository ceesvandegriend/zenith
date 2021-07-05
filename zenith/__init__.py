
import os
import pathlib

config = {
    'base_dir': pathlib.Path(__file__).parent.parent,
    'log_dir': os.path.join(pathlib.Path.home(), 'var', 'log'),
}



