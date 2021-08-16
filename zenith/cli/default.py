import logging
import readline

from zenith.factory.default import DefaultFactory


class DefaultProcessor(object):
    def __init__(self, level = logging.ERROR):
        self.log_level = level

        # Setup GNU readline
        # ToDo: read history
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')

    def input(self, prompt: str, value: str = "") -> str:
        readline.set_startup_hook(lambda: readline.insert_text(value))

        try:
            line = input(prompt)
        finally:
            readline.set_startup_hook()

        return line