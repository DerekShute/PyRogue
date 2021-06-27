"""
    Need a simple response from the player - ['a'..'d'], ['y','n'], etc.

    TODO: does this become an Action, or just return the character with the InputHandler?
"""

import tcod
from typing import List
from actions import Action
from input_handler import InputHandler


# ===== ResponseInputHandler ================================

class ResponseInputHandler(InputHandler):
    """Need a one-character response from player"""
    responses: str
    action: Action  # Action to modify

    def __init__(self, responses: str, action: Action = None, **kwargs):
        super().__init__(**kwargs)
        self.responses = responses
        self.action = action

    def ev_quit(self, event: tcod.event.Quit) -> (InputHandler, None):
        return self.previous, None  # TODO this is not easy

    def ev_keydown(self, event: tcod.event.KeyDown) -> (InputHandler, Action):
        key = event.sym
        
        # TODO: special meaning escape key
        if chr(key) in self.responses:  # Condition met
            action = self.action.incorporate(key)
            return self.previous, action
        return self, None

# EOF
