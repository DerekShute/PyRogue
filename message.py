"""
    Messages to the player at the top of the screen
"""
from position import Pos

class MessageBuffer:
    _message: str = None  # TODO: buffering and view

    def __init__(self):
        self._message = ''

    def add(self, text: str):
        self._message = text
        # TODO: multiline output (includes "--MORE--"), and buffering

    @property
    def msg(self) -> str:
        return self._message if self._message is not None else ''

# EOF
