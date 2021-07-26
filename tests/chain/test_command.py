import unittest

from tests.chain.dummy import *


class TestCommand(unittest.TestCase):
    def test01(self) -> None:
        command = DummySuccessCommand()
        context = DummyContect()

        self.assertFalse(command.executed)
        self.assertTrue(command.execute(context))
        self.assertTrue(command.executed)

        self.assertEqual(CommandState.UNKNOWN, command.state)
        command.post_execute(context, CommandState.SUCCESS, None)
        self.assertEqual(CommandState.SUCCESS, command.state)

    def test02(self) -> None:
        command = DummyFailureCommand()
        context = DummyContect()

        self.assertFalse(command.executed)
        self.assertFalse(command.execute(context))
        self.assertTrue(command.executed)

        self.assertEqual(CommandState.UNKNOWN, command.state)
        command.post_execute(context, CommandState.FAILURE, None)
        self.assertEqual(CommandState.FAILURE, command.state)


    def test03(self) -> None:
        command = DummyErrorCommand()
        context = DummyContect()

        self.assertFalse(command.executed)
        with self.assertRaises(Exception):
            command.execute(context)
        self.assertTrue(command.executed)

        self.assertEqual(CommandState.UNKNOWN, command.state)
        exception = Exception("Dummy exception")
        command.post_execute(context, CommandState.ERROR, exception)
        self.assertEqual(CommandState.ERROR, command.state)


if __name__ == '__main__':
    unittest.main()
