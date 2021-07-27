import logging
import os
import pathlib
import unittest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import sessionmaker

from zenith.chain import Runner
from zenith.command.client import *
from zenith.command.database import DatabaseContext, DatabaseCreateCommand, DatabaseDropCommand, DatabaseSetupCommand, DatabaseSessionCommand
from zenith.models import Base

# Reduce logging
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.ERROR)

class SuccessCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        return Command.SUCCESS

class FailureCommand(Command):
    def execute(self, context: DatabaseContext) -> bool:
        return Command.FAILURE

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        base_dir = pathlib.Path(__file__).parent.parent.parent.parent.absolute()
        db_dir = os.path.join(base_dir, "var", "db")
        db_filename = os.path.join(db_dir, "zenith-test.db")

        if not os.path.isdir(db_dir):
            os.makedirs(db_dir)

        cls.engine = create_engine(f"sqlite:///{db_filename}")
        cls.db_filename = db_filename

    def setUp(self) -> None:
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseDropCommand())
        runner.append(DatabaseCreateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        runner.execute(context)

    def test_create01(self):
        """ Create aap. """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientCreateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

    def test_create02(self):
        """ Missing client_name """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientCreateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        with self.assertRaises(ContextKeyException):
            runner.execute(context)

    def test_create03(self):
        """ Missing key """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientCreateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        with self.assertRaises(ContextKeyException):
            runner.execute(context)

    def test_create04(self):
        """ client_name exists """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()

        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientCreateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        with self.assertRaises(IntegrityError):
            runner.execute(context)

    def test_create05(self):
        """ Success: commit() """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientCreateCommand())
        runner.append(SuccessCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        count = tmp.query(Client).filter(Client.client_name == "aap").count()
        tmp.commit()

        self.assertEqual(1, count)

    def test_create06(self):
        """ Failure: rollback() """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientCreateCommand())
        runner.append(FailureCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertFalse(runner.execute(context))

        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        count = tmp.query(Client).filter(Client.client_name == "aap").count()
        tmp.commit()

        self.assertEqual(0, count)

    def test_read01(self):
        """ client_name exists """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()


        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientReadCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

        self.assertTrue("client" in context)
        self.assertEqual(aap.client_id, context["client"].client_id)
        self.assertEqual(aap.client_uuid, context["client"].client_uuid)
        self.assertEqual(aap.client_name, context["client"].client_name)
        self.assertEqual(aap.client_active, context["client"].client_active)
        self.assertEqual(aap.client_description, context["client"].client_description)
        self.assertEqual(aap.client_remark, context["client"].client_remark)
        self.assertEqual(aap.created_on, context["client"].created_on)
        self.assertEqual(aap.updated_on, context["client"].updated_on)

    def test_read02(self):
        """ client_name does not exists """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientReadCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        with self.assertRaises(NoResultFound):
            runner.execute(context)

        self.assertFalse("client" in context)

    def test_read03(self):
        """ client_name does not exists """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientReadCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        with self.assertRaises(ContextKeyException):
            runner.execute(context)

        self.assertFalse("client" in context)

    def test_update01(self):
        """ client_name does not exists """
        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientUpdateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"
        context["client_description"] = "Een aap"

        with self.assertRaises(NoResultFound):
            runner.execute(context)

    def test_update02(self):
        """ client_name does exists """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()

        runner = Runner()
        runner.append(DatabaseSetupCommand())
        runner.append(DatabaseSessionCommand())
        runner.append(ClientUpdateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"
        context["client_active"] = True
        context["client_description"] = "Een aap beschrijving"
        context["client_remark"] = "Een aap opmerking"

        self.assertTrue(runner.execute(context))

        tmp = Session()
        aap = tmp.query(Client).filter(Client.client_name == "aap").one()
        tmp.commit()

        self.assertEqual("aap", aap.client_name)
        self.assertEqual(True, aap.client_active)
        self.assertEqual("Een aap beschrijving", aap.client_description)
        self.assertEqual("Een aap opmerking", aap.client_remark)


    def test_update03(self):
        """ client_name does exists """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()
        updated_on = aap.updated_on

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientUpdateCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertFalse(runner.execute(context))

        tmp = Session()
        aap = tmp.query(Client).filter(Client.client_name == "aap").one()
        tmp.commit()

        self.assertEqual("aap", aap.client_name)
        self.assertEqual(updated_on, aap.updated_on)

    def test_update04(self):
        """ Success: commit """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()
        updated_on = aap.updated_on

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientUpdateCommand())
        runner.append(SuccessCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"
        context["client_active"] = True

        self.assertTrue(runner.execute(context))

        tmp = Session()
        aap = tmp.query(Client).filter(Client.client_name == "aap").one()
        tmp.commit()

        self.assertEqual("aap", aap.client_name)
        self.assertEqual(True, aap.client_active)

    def test_update05(self):
        """ Failure: rollback """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()
        updated_on = aap.updated_on

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientUpdateCommand())
        runner.append(FailureCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"
        context["client_active"] = True

        self.assertFalse(runner.execute(context))

        tmp = Session()
        aap = tmp.query(Client).filter(Client.client_name == "aap").one()
        tmp.commit()

        self.assertEqual("aap", aap.client_name)
        self.assertEqual(False, aap.client_active)

    def test_delete01(self):
        """ client does not exist """
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientDeleteCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        with self.assertRaises(NoResultFound):
            runner.execute(context)

    def test_delete02(self):
        """ client exists """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()

        tmp = Session()
        self.assertEqual(1, tmp.query(Client).filter(Client.client_name == "aap").count())
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientDeleteCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

        tmp = Session()
        self.assertEqual(0, tmp.query(Client).filter(Client.client_name == "aap").count())
        tmp.commit()

    def test_delete03(self):
        """ client_name key does not exist """
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientDeleteCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        with self.assertRaises(ContextKeyException):
            runner.execute(context)

    def test_delete04(self):
        """ Success: commit """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()

        tmp = Session()
        self.assertEqual(1, tmp.query(Client).filter(Client.client_name == "aap").count())
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientDeleteCommand())
        runner.append(SuccessCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

        tmp = Session()
        self.assertEqual(0, tmp.query(Client).filter(Client.client_name == "aap").count())
        tmp.commit()

    def test_delete05(self):
        """ Failure: rollback """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        aap = Client(client_name="aap")
        tmp.add(aap)
        tmp.commit()

        tmp = Session()
        self.assertEqual(1, tmp.query(Client).filter(Client.client_name == "aap").count())
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientDeleteCommand())
        runner.append(FailureCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertFalse(runner.execute(context))

        tmp = Session()
        self.assertEqual(1, tmp.query(Client).filter(Client.client_name == "aap").count())
        tmp.commit()

    def test_list01(self):
        """ Empty list """
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientListCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        self.assertTrue(runner.execute(context))
        self.assertTrue("clients" in context)

        clients = context["clients"]

        self.assertEqual(0, len(clients))

    def test_list02(self):
        """ list ordered by client_name """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        client0 = Client(client_name="aap")
        client1 = Client(client_name="noot")
        client2 = Client(client_name="mies")
        tmp.add(client0)
        tmp.add(client1)
        tmp.add(client2)
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientListCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        self.assertTrue(runner.execute(context))
        self.assertTrue("clients" in context)

        clients = context["clients"]

        self.assertEqual(3, len(clients))
        self.assertEqual(client0.client_id, clients[0].client_id)
        self.assertEqual(client0.client_uuid, clients[0].client_uuid)
        self.assertEqual(client0.client_name, clients[0].client_name)
        self.assertEqual(client2.client_id, clients[1].client_id)
        self.assertEqual(client2.client_uuid, clients[1].client_uuid)
        self.assertEqual(client2.client_name, clients[1].client_name)
        self.assertEqual(client1.client_id, clients[2].client_id)
        self.assertEqual(client1.client_uuid, clients[2].client_uuid)
        self.assertEqual(client1.client_name, clients[2].client_name)

    def test_list03(self):
        """ Success """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        client0 = Client(client_name="aap")
        client1 = Client(client_name="noot")
        client2 = Client(client_name="mies")
        tmp.add(client0)
        tmp.add(client1)
        tmp.add(client2)
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientListCommand())
        runner.append(SuccessCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        self.assertTrue(runner.execute(context))
        self.assertTrue("clients" in context)

        clients = context["clients"]

        self.assertEqual(3, len(clients))
        self.assertEqual(client0.client_id, clients[0].client_id)
        self.assertEqual(client0.client_uuid, clients[0].client_uuid)
        self.assertEqual(client0.client_name, clients[0].client_name)
        self.assertEqual(client2.client_id, clients[1].client_id)
        self.assertEqual(client2.client_uuid, clients[1].client_uuid)
        self.assertEqual(client2.client_name, clients[1].client_name)
        self.assertEqual(client1.client_id, clients[2].client_id)
        self.assertEqual(client1.client_uuid, clients[2].client_uuid)
        self.assertEqual(client1.client_name, clients[2].client_name)

    def test_list04(self):
        """ Failure """
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        client0 = Client(client_name="aap")
        client1 = Client(client_name="noot")
        client2 = Client(client_name="mies")
        tmp.add(client0)
        tmp.add(client1)
        tmp.add(client2)
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientListCommand())
        runner.append(FailureCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        self.assertFalse(runner.execute(context))
        self.assertTrue("clients" in context)

        clients = context["clients"]

        self.assertEqual(3, len(clients))
        self.assertEqual(client0.client_id, clients[0].client_id)
        self.assertEqual(client0.client_uuid, clients[0].client_uuid)
        self.assertEqual(client0.client_name, clients[0].client_name)
        self.assertEqual(client2.client_id, clients[1].client_id)
        self.assertEqual(client2.client_uuid, clients[1].client_uuid)
        self.assertEqual(client2.client_name, clients[1].client_name)
        self.assertEqual(client1.client_id, clients[2].client_id)
        self.assertEqual(client1.client_uuid, clients[2].client_uuid)
        self.assertEqual(client1.client_name, clients[2].client_name)

    def test_exist01(self):
        """ Empty list """
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientExistCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        with self.assertRaises(ContextKeyException):
            self.assertTrue(runner.execute(context))

    def test_exist02(self):
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        client0 = Client(client_name="aap")
        tmp.add(client0)
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientExistCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

    def test_exist03(self):
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientExistCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertFalse(runner.execute(context))

    def test_notexist01(self):
        """ Empty list """
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientNotExistCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename

        with self.assertRaises(ContextKeyException):
            self.assertTrue(runner.execute(context))

    def test_notexist02(self):
        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientNotExistCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertTrue(runner.execute(context))

    def test_notexist03(self):
        engine = create_engine(f"sqlite:///{self.db_filename}")
        Session = sessionmaker(engine)
        tmp = Session()
        client0 = Client(client_name="aap")
        tmp.add(client0)
        tmp.commit()

        runner = Runner()
        runner.append((DatabaseSetupCommand()))
        runner.append(DatabaseSessionCommand())
        runner.append(ClientNotExistCommand())

        context = DatabaseContext()
        context["db_filename"] = self.db_filename
        context["client_name"] = "aap"

        self.assertFalse(runner.execute(context))

if __name__ == '__main__':
    unittest.main()
