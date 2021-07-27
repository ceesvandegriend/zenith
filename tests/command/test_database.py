import os
import pathlib
import tempfile
import unittest

from sqlalchemy import create_engine

from zenith.chain import Context, ContextKeyException, Runner

from zenith.command.database import DatabaseContext, DatabaseCreateCommand, DatabaseSetupCommand

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        base_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        db_dir = os.path.join(base_dir, "var", "db")
        db_filename = os.path.join(db_dir, "zenith-test.db")

        if not os.path.isdir(db_dir):
            os.makedirs(db_dir)

        cls.engine = create_engine(f"sqlite:///{db_filename}")
        cls.db_filename = db_filename

    def test_setup01(self):
        """ db_filename does not exist in the context """

        if os.path.isfile(self.db_filename):
            os.remove(self.db_filename)

        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseCreateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        self.assertTrue(runner.execute(context))
        self.assertTrue(os.path.isfile(self.db_filename))

if __name__ == '__main__':
    unittest.main()
