from zenith.chain import Context, Command, CommandState

class DummyContect(Context):
    def __init__(self):
        self.counter = 0
        self.post_counter = 0


class DummySuccessCommand(Command):
    counter = 0
    post_counter = 0
    executed = False
    state = CommandState.UNKNOWN

    def execute(self, context: DummyContect) -> bool:
        context.counter += 1
        self.executed = True
        self.counter = context.counter
        return Command.SUCCESS


    def post_execute(self, context: DummyContect, state: CommandState, error: Exception = None) -> None:
        context.post_counter += 1
        self.state = state
        self.post_counter = context.post_counter


class DummyFailureCommand(DummySuccessCommand):
    def execute(self, context: DummyContect) -> bool:
        super().execute(context)
        return Command.FAILURE

class DummyException(Exception):
    pass

class DummyErrorCommand(DummySuccessCommand):
    def execute(self, context: DummyContect) -> bool:
        super().execute(context)
        raise DummyException("Dummy exception")
