"""
    Pop up a menu for the player(human) to choose from
"""
from typing import List


class Menu:
    title: str
    text: List[str] = None

    def __init__(self, title: str, text: List[str]):
        self.title = title
        self.text = text

    # TODO: add by index
    # TODO: item reference for selection
# EOF
