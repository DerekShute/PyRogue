import tcod
from typing import Any, Tuple
from entity import Entity
from position import Pos

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
    mouse: Pos = None
    mousedown: bool = False

    def __init__(self, entity: Entity = None, previous: 'InputHandler' = None):
        super().__init__()
        self.previous = previous
        self.entity = entity

    def get_action(self):
        """Pull out an action for the Player"""
        raise NotImplementedError()

    def render_layer(self, display):
        """Display extra stuff needed for this InputHandler"""
        return None

    def ev_mousemotion(self, event: tcod.event.MouseMotion):
        """Mouse has moved"""
        self.mouse = Pos(event.tile.x, event.tile.y)

    def ev_mousebuttonup(self, event: tcod.event.MouseButtonUp):
        self.mouse = Pos(event.tile.x, event.tile.y)
        self.mousedown = False

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown):
        self.mouse = Pos(event.tile.x, event.tile.y)
        self.mousedown = True

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
