"""
    Need a simple response from the player - ['a'..'d'], ['y','n'], etc.

    TODO: does this become an Action, or just return the character with the InputHandler?
"""

import tcod
from actions import Action
from game_states import InputHandler


# ===== ResponseInputHandler ================================

class ResponseInputHandler(InputHandler):
    """Need a one-character response from player"""
    responses: str
    action: Action  # Action to modify
    string: str

    def __init__(self, responses: str = None, string: str = '', action: Action = None, **kwargs):
        super().__init__(**kwargs)
        self.responses = responses
        self.action = action
        self.string = string

    def ev_quit(self, event: tcod.event.Quit) -> InputHandler:
        return self.previous

    def ev_keydown(self, event: tcod.event.KeyDown) -> InputHandler:
        key = event.sym

        # TODO: special meaning escape key
        if key < 257 and chr(key) in self.responses:  # Condition met.  Don't feed large numbers into chr()
            if self.entity is not None and self.action is not None:
                self.entity.queue_action(self.action.incorporate(key))
            return self.previous
        return self

    def render_layer(self, display):
        if len(self.string) > 0:
            xsize, ysize = display.size
            display.msg(x=0, y=ysize - 1, string=self.string.ljust(xsize))

# EOF
