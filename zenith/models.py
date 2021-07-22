import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def generate_uuid() -> str:
    """
    Generates a random UUID.

    :return: UUID as string
    """
    return str(uuid.uuid4())


class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer(), primary_key=True, nullable=False)
    client_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    client_name = Column(String(128), index=True, nullable=False, unique=True)
    client_description = Column(String(255), nullable=True)
    client_remark = Column(String(1024), nullable=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self) -> str:
        return f"Client<client_id: {self.client_id}, client_uuid: {self.client_uuid}, client_name: {self.client_name}>"

class Contact(Base):
    __tablename__ = "contacts"

    client_id = Column(Integer(), ForeignKey("clients.client_id"), nullable=False)
    contact_id = Column(Integer(), primary_key=True, nullable=False)
    contact_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    contact_name = Column(String(128), index=True, nullable=False, unique=True)
    contact_description = Column(String(255), nullable=True)
    contact_remark = Column(String(1024), nullable=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    client_id = Column(Integer(), ForeignKey("clients.client_id"), nullable=False)
    project_id = Column(Integer(), primary_key=True, nullable=False)
    project_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    project_name = Column(String(128), index=True, nullable=False, unique=True)
    project_description = Column(String(255), nullable=True)
    project_remark = Column(String(1024), nullable=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Period(Base):
    __tablename__ = "periods"

    project_id = Column(Integer(), ForeignKey("projects.project_id"), nullable=False)
    period_id = Column(Integer(), primary_key=True, nullable=False)
    period_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Asset(Base):
    __tablename__ = "assets"

    period_id = Column(Integer(), ForeignKey("projects.project_id"), nullable=False)
    asset_id = Column(Integer(), primary_key=True, nullable=False)
    asset_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Event(Base):
    __tablename__ = "events"

    period_id = Column(Integer(), ForeignKey("projects.project_id"), nullable=False)
    event_id = Column(Integer(), primary_key=True, nullable=False)
    event_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now, nullable=False)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now, nullable=False)


class Note(Base):
    __tablename__ = "notes"

    period_id = Column(Integer(), ForeignKey("projects.project_id"), nullable=False)
    note_id = Column(Integer(), primary_key=True, nullable=False)
    note_uuid = Column(String(128), index=True, default=generate_uuid, nullable=False, unique=True)
    note_description = Column(String(255), nullable=True)
    note_remark = Column(String(1024), nullable=True)
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
