import unittest

from tests.chain.dummy import *
from zenith.chain import Chain


class TestChain(unittest.TestCase):
    def test01(self):
        aap = DummySuccessCommand()
        noot = DummySuccessCommand()
        mies = DummySuccessCommand()

        chain = Chain()
        chain.append(aap)
        chain.append(noot)
        chain.append(mies)

        context = DummyContect()
        success = False
        exception = None

        try:
            success = chain.execute(context)
        except Exception as err:
            success = False
            exception = err
        finally:
            if exception:
                state = CommandState.ERROR
            elif success == Command.FAILURE:
                state = CommandState.FAILURE
            elif success == Command.SUCCESS:
                state = CommandState.SUCCESS
            else:
                state = CommandState.UNKNOWN

            chain.post_execute(context, state, exception)

        self.assertTrue(aap.executed)
        self.assertTrue(noot.executed)
        self.assertTrue(mies.executed)

        self.assertEqual(CommandState.SUCCESS, mies.state)
        self.assertEqual(CommandState.SUCCESS, noot.state)
        self.assertEqual(CommandState.SUCCESS, aap.state)

    def test02(self):
        aap = DummySuccessCommand()
        noot = DummyFailureCommand()
        mies = DummySuccessCommand()

        chain = Chain()
        chain.append(aap)
        chain.append(noot)
        chain.append(mies)

        context = DummyContect()
        success = False
        exception = None

        try:
            success = chain.execute(context)
        except Exception as err:
            success = False
            exception = err
        finally:
            if exception:
                state = CommandState.ERROR
            elif success == Command.FAILURE:
                state = CommandState.FAILURE
            elif success == Command.SUCCESS:
                state = CommandState.SUCCESS
            else:
                state = CommandState.UNKNOWN

            chain.post_execute(context, state, exception)

        self.assertTrue(aap.executed)
        self.assertTrue(noot.executed)
        self.assertFalse(mies.executed)

        self.assertEqual(CommandState.FAILURE, mies.state)
        self.assertEqual(CommandState.FAILURE, noot.state)
        self.assertEqual(CommandState.FAILURE, aap.state)

    def test03(self):
        aap = DummySuccessCommand()
        noot = DummyErrorCommand()
        mies = DummyFailureCommand()

        chain = Chain()
        chain.append(aap)
        chain.append(noot)
        chain.append(mies)

        context = DummyContect()
        success = False
        exception = None

        try:
            success = chain.execute(context)
        except Exception as err:
            success = False
            exception = err
        finally:
            if exception:
                state = CommandState.ERROR
            elif success == Command.FAILURE:
                state = CommandState.FAILURE
            elif success == Command.SUCCESS:
                state = CommandState.SUCCESS
            else:
                state = CommandState.UNKNOWN

            chain.post_execute(context, state, exception)

        self.assertTrue(aap.executed)
        self.assertTrue(noot.executed)
        self.assertFalse(mies.executed)

        self.assertEqual(CommandState.ERROR, mies.state)
        self.assertEqual(CommandState.ERROR, noot.state)
        self.assertEqual(CommandState.ERROR, aap.state)

    def test04(self):
        commands = list()

        chain0 = Chain()
        chain1 = Chain()
        chain2 = Chain()

        main = Chain()
        main.append(chain0)
        main.append(chain1)
        main.append(chain2)

        for n in range(0, 30):
            commands.append(DummySuccessCommand())
        for n in range(0, 10):
            chain0.append(commands[n])
        for n in range(10, 20):
            chain1.append(commands[n])
        for n in range(20, 30):
            chain2.append(commands[n])

        context = DummyContect()
        success = False
        exception = None

        try:
            success = main.execute(context)
        except Exception as err:
            success = False
            exception = err
        finally:
            if exception:
                state = CommandState.ERROR
            elif success == Command.FAILURE:
                state = CommandState.FAILURE
            elif success == Command.SUCCESS:
                state = CommandState.SUCCESS
            else:
                state = CommandState.UNKNOWN

            main.post_execute(context, state, exception)

        self.assertEqual(30, len(commands))

        for n in range(30):
            self.assertTrue(commands[n].executed)
            self.assertEqual(CommandState.SUCCESS, commands[n].state)
            self.assertEqual(n + 1, commands[n].counter)
            self.assertEqual(30 - n, commands[n].post_counter)

    def test05(self):
        commands = list()

        chain0 = Chain()
        chain1 = Chain()
        chain2 = Chain()

        main = Chain()
        main.append(chain0)
        main.append(chain1)
        main.append(chain2)

        for n in range(0, 30):
            commands.append(DummySuccessCommand())

        commands[19] = DummyFailureCommand()

        for n in range(0, 10):
            chain0.append(commands[n])
        for n in range(10, 20):
            chain1.append(commands[n])
        for n in range(20, 30):
            chain2.append(commands[n])

        context = DummyContect()
        success = False
        exception = None

        try:
            success = main.execute(context)
        except Exception as err:
            success = False
            exception = err
        finally:
            if exception:
                state = CommandState.ERROR
            elif success == Command.FAILURE:
                state = CommandState.FAILURE
            elif success == Command.SUCCESS:
                state = CommandState.SUCCESS
            else:
                state = CommandState.UNKNOWN

            main.post_execute(context, state, exception)

        self.assertEqual(30, len(commands))

        for n in range(1, 20):
            self.assertTrue(commands[n].executed)
            self.assertEqual(CommandState.FAILURE, commands[n].state)
            self.assertEqual(n + 1, commands[n].counter)
            self.assertEqual(30 - n, commands[n].post_counter)

        for n in range(20, 30):
            self.assertFalse(commands[n].executed)
            self.assertEqual(CommandState.FAILURE, commands[n].state)
            self.assertEqual(0, commands[n].counter)  # not executed
            self.assertEqual(30 - n, commands[n].post_counter)

    def test06(self):
        commands = list()

        chain0 = Chain()
        chain1 = Chain()
        chain2 = Chain()

        main = Chain()
        main.append(chain0)
        main.append(chain1)
        main.append(chain2)

        for n in range(0, 30):
            commands.append(DummySuccessCommand())

        commands[19] = DummyErrorCommand()

        for n in range(0, 10):
            chain0.append(commands[n])
        for n in range(10, 20):
            chain1.append(commands[n])
        for n in range(20, 30):
            chain2.append(commands[n])

        context = DummyContect()
        success = False
        exception = None

        try:
            success = main.execute(context)
        except Exception as err:
            success = False
            exception = err
        finally:
            if exception:
                state = CommandState.ERROR
            elif success == Command.FAILURE:
                state = CommandState.FAILURE
            elif success == Command.SUCCESS:
                state = CommandState.SUCCESS
            else:
                state = CommandState.UNKNOWN

            main.post_execute(context, state, exception)

        self.assertEqual(30, len(commands))

        for n in range(1, 20):
            self.assertTrue(commands[n].executed)
            self.assertEqual(CommandState.ERROR, commands[n].state)
            self.assertEqual(n + 1, commands[n].counter)
            self.assertEqual(30 - n, commands[n].post_counter)

        for n in range(20, 30):
            self.assertFalse(commands[n].executed)
            self.assertEqual(CommandState.ERROR, commands[n].state)
            self.assertEqual(0, commands[n].counter)  # not executed
            self.assertEqual(30 - n, commands[n].post_counter)


if __name__ == '__main__':
    unittest.main()
