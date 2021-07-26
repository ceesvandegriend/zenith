from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zenith import config

class Command(ABC):
    """ Abstract class which is the base of all commands. """

    def __init__(self):
        self.engine = create_engine(f"sqlite:///{config['db_filename']}")
        self.Session = sessionmaker(self.engine)


    def create_session(self):
        """
        Creates a session.

        Initializes SQLAlchemy once, when needed.
        """

        return self.Session()


    @abstractmethod
    def execute(self, args: list) -> None:
        pass
