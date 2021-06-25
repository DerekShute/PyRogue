import tcod
from typing import List
from actions import Action, DescendAction, MovementAction, PickupAction
from input_handler import InputHandler, CancelHandler, MOVE_KEYS


# ===== PlayerInputHandler ================================

class PlayerInputHandler(InputHandler):
    """Base input handler for ordinary game input"""

    _inputq: List[Action] = []
    """Queued Actions on behalf of the Player AI"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._inputq = []

    def ev_quit(self, event: tcod.event.Quit) -> InputHandler:
        return CancelHandler()

    def ev_keydown(self, event: tcod.event.KeyDown) -> InputHandler:
        key = event.sym
        modifier = event.mod
        if key == tcod.event.K_PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            self._inputq.append(DescendAction())
        elif key == tcod.event.K_ESCAPE:
            return CancelHandler()
        elif key == tcod.event.K_g:
            self._inputq.append(PickupAction())
        elif key in MOVE_KEYS:
            self._inputq.append(MovementAction(*MOVE_KEYS[key]))
        return self

    def get_action(self) -> Action:
        if len(self._inputq) == 0:
            return None
        return self._inputq.pop(0)
