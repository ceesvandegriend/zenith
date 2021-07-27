import os
import pathlib
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.exc import IntegrityError

from zenith.models import *

class TestModels(unittest.TestCase):
    engine = None
    Session = None

    @classmethod
    def setUpClass(cls) -> None:
        base_dir = pathlib.Path(__file__).parent.parent.parent.absolute()
        db_dir = os.path.join(base_dir, "var", "db")
        db_filename = os.path.join(db_dir, "zenith-test.db")

        if not os.path.isdir(db_dir):
            os.makedirs(db_dir)

        cls.engine = create_engine(f"sqlite:///{db_filename}")
        cls.Session = sessionmaker(cls.engine)

    def setUp(self) -> None:
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def test_client01(self):
        """ Assert an empty list. """
        session0 = self.Session()
        clients = session0.query(Client).all()
        self.assertEqual(0, len(clients))
        session0.commit()

    def test_client02(self):
        """ Assert a single item. """
        session0 = self.Session()
        aap0 = Client(client_name="aap", client_description="Een aap", client_remark="Een opmerking")
        session0.add(aap0)
        session0.commit()

        session1 = self.Session()
        clients = session1.query(Client).all()
        self.assertEqual(1, len(clients))
        aap1 = clients[0]

        self.assertEqual(aap0.client_id, aap1.client_id)
        self.assertEqual(aap0.client_uuid, aap1.client_uuid)
        self.assertEqual(aap0.client_name, aap1.client_name)
        self.assertEqual(aap0.client_description, aap1.client_description)
        self.assertEqual(aap0.client_remark, aap1.client_remark)
        self.assertEqual(aap0.created_on, aap1.created_on)
        self.assertEqual(aap0.updated_on, aap1.updated_on)

        session1.commit()

    def test_client03(self):
        """ Assert name is unique. """
        aap0 = Client(client_name="aap", client_description="Een aap", client_remark="Een opmerking")
        aap1 = Client(client_name="aap", client_description="Een aap", client_remark="Een opmerking")

        session0 = self.Session()
        session0.add(aap0)
        session0.commit()

        with self.assertRaises(IntegrityError):
            session1 = self.Session()
            session1.add(aap1)
            session1.commit()

    def test_client04(self):
        """ Assert name is not null. """
        aap0 = Client(client_name="aap", client_description="Een aap", client_remark="Een opmerking")

        session0 = self.Session()
        session0.add(aap0)
        session0.commit()

        with self.assertRaises(IntegrityError):
            session1 = self.Session()
            aap1 = session1.query(Client).filter_by(client_name = "aap").one()
            aap1.client_name = None
            session1.commit()

    def test_client05(self):
        """ Assert three items. """
        session0 = self.Session()
        aap0 = Client(client_name="aap", client_description="Een aap", client_remark="Een opmerking")
        noot0 = Client(client_name="noot", client_description="Een noot", client_remark="Een opmerking")
        mies0 = Client(client_name="mies", client_description="Een mies", client_remark="Een opmerking")
        session0.add(aap0)
        session0.add(noot0)
        session0.add(mies0)
        session0.commit()

        session1 = self.Session()
        clients = session1.query(Client).all()
        self.assertEqual(3, len(clients))
        aap1 = clients[0]
        noot1 = clients[1]
        mies1 = clients[2]

        self.assertEqual(aap0.client_name, aap1.client_name)
        self.assertEqual(aap0.client_uuid, aap1.client_uuid)
        self.assertEqual(noot0.client_name, noot1.client_name)
        self.assertEqual(noot0.client_uuid, noot1.client_uuid)
        self.assertEqual(mies0.client_name, mies1.client_name)
        self.assertEqual(mies0.client_uuid, mies1.client_uuid)


if __name__ == '__main__':
    unittest.main()
