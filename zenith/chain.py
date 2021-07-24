"""
Chain of Command
"""
import enum


class CommandState(enum.Enum):
    UNKNOWN = 0
    ERROR = 1
    FAILURE = 2
    SUCCESS = 3


class Command(object):
    FAILURE = False
    SUCCESS = True

    def execute(self, context: dict) -> bool:
        return Command.SUCCESS

    def post_execute(self, context: dict, state: CommandState, error: Exception = None) -> None:
        pass


class Chain(Command):
    def __init__(self):
        self.commands = list()

    def append(self, command: Command) -> None:
        self.commands.append(command)

    def execute(self, context: dict) -> bool:
        success = True
        for command in self.commands:
            success = command.execute(context)
            if not success:
                break

        return success

    def post_execute(self, context: dict, state: CommandState, error: Exception = None) -> None:
        for command in self.commands[::-1]:
            command.post_execute(context, state, error)


class Runner(Chain):
    def execute(self, context: dict) -> bool:
        exception = Exception("No exception")
        state = CommandState.UNKNOWN

        try:
            if super().execute(context):
                state = CommandState.SUCCESS
            else:
                state = CommandState.FAILURE
        except Exception as err:
            exception = err
            state = CommandState.ERROR
        finally:
            super().post_execute(context, state, exception)

        if state == CommandState.ERROR:
            raise exception
        elif state == CommandState.FAILURE:
            return Command.FAILURE
        elif state == CommandState.SUCCESS:
            return Command.SUCCESS
        else:
            # Huh, How did this happen?
            return Command.FAILURE
