import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer(), primary_key=True, nullable=False)
    project_name = Column(String(128), index=True, nullable=False, unique=True)
    project_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Session(Base):
    __tablename__ = "sessions"

    project_id = Column(Integer(), ForeignKey("projects.project_id"), nullable=False)
    session_id = Column(Integer(), primary_key=True, nullable=False)
    session_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from zenith import config

    engine = create_engine(f"sqlite:///{config['db_filename']}")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    aap = Project(project_name="aap")
    noot = Project(project_name="noot")
    mies = Project(project_name="mies")

    session = Session()
    session.add(aap)
    session.add(noot)
    session.add(mies)
    session.commit()
