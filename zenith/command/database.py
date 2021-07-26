import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from zenith.chain import Command, CommandState, Context, ContextKeyException
from zenith.models import Base


class DatabaseContext(Context):
    session = None

    def get_session(self):
        return self.session

class DatabaseSetupCommand(Command):
    def __init__(self, db_filename: str) -> None:
        self.db_filename = db_filename

    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("setup.execute() - Start")

        context.engine = create_engine(f"sqlite:///{self.db_filename}")

        # does the database exist?
        if not os.path.isfile(self.db_filename):
            Base.metadata.create_all(context.engine)
            logger.info(f"Created db: {self.db_filename}")

        logger.debug("setup.execute() - Finish")
        return Command.SUCCESS


class DatabaseSessionCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        logger = logging.getLogger(__name__)
        logger.debug("session.execute() - Start")

        engine = context.engine
        Session = sessionmaker(engine)
        self.session = Session()
        context.session = self.session

        logger.debug("session.execute() - Finish")
        return Command.SUCCESS

    def post_execute(self, context: Context, state: CommandState, error: Exception = None) -> None:
        logger = logging.getLogger(__name__)
        logger.debug("session.post_execute() - Start")

        if state == CommandState.SUCCESS:
            self.session.commit()
            logger.debug("session.commit()")
        else:
            if self.session:
                self.session.rollback()
                logger.debug("session.rollback()")

        logger.debug("session.post_execute() - Finish")
