import tcod
from typing import Any, Optional, List


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
    
    def __init__(self, previous: 'InputHandler' = None):
        super().__init__()
        self.previous = previous

    def get_action(self):
        return None


# ===== CancelHandler derived class =======================

class CancelHandler(InputHandler):
    """A sentinel value to catch Cancel/Quit because not every event handler is implemented"""
    pass

# EOF
