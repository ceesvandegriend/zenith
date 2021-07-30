import os
import pathlib
import sys

from zenith.command.database import DatabaseContext, DatabaseCreateCommand
from zenith.cli.default import DefaultProcessor


class InitProcessor(DefaultProcessor):
    def init(self, direcory: str) -> None:
        if not direcory:
            zenith_dir = os.path.join(pathlib.Path(os.getcwd()).absolute(), ".zenith")
        elif ".zenith" == pathlib.Path(direcory).name:
            zenith_dir = pathlib.Path(direcory).absolute()
        else:
            zenith_dir = os.path.join(pathlib.Path(direcory).absolute(), ".zenith")

        context = DatabaseContext()
        context["zenith_dir"] = zenith_dir
        context["logfile"] = False

        self.processing.append(DatabaseCreateCommand())

        self.execute(context)
