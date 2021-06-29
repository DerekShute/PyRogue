"""
    Messages to the player at the top of the screen
"""
from typing import List

# TODO: buffering and history


# ===== MessageBuffer =====================================

class MessageBuffer:
    _message: List[str] = None  # TODO: buffering and view

    def __init__(self):
        self._message = []

    def add(self, text: str):
        self._message.append(text)

    @property
    def msg(self) -> str:
        return self._message[0] if self.count > 0 else ''

    @property
    def count(self) -> int:
        return len(self._message)

    def advance(self):
        if self.count > 0:
            self._message.pop(0)
# EOF
