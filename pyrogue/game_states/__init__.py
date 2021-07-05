import tcod
from typing import Any
from entity import Entity


MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
}


# ===== InputHandler Base Class ===========================

class InputHandler(tcod.event.EventDispatch[Any]):
    previous: 'InputHandler' = None

    def __init__(self, entity: Entity = None, previous: 'InputHandler' = None):
        super().__init__()
        self.previous = previous
        self.entity = entity

    def get_action(self):
        """Pull out an action for the Player"""
        raise NotImplementedError()

    def render_layer(self, display):
        """Display extra stuff needed for this InputHandler"""
        raise NotImplementedError()


# ===== CancelHandler derived class =======================

class CancelHandler(InputHandler):
    """A sentinel value to catch Cancel/Quit because not every event handler is implemented"""
    pass


# ===== Game Loop Superclass ==============================

class Gameloop:
    _display = None
    _previous: 'Gameloop' = None
    _input_handler: InputHandler = None

    def __init__(self, display=None, previous: 'Gameloop' = None):
        self._display = display
        self._previous = previous

    def run(self) -> 'Gameloop':  # Quotes: 'forward declaration'
        assert self
        raise NotImplementedError('Cannot use Gameloop raw')

# EOF
