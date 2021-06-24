import tcod
from typing import Any, Optional, List
from actions import EscapeAction, MovementAction, Action, PickupAction, DescendAction


MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
}


class PlayerInputHandler(tcod.event.EventDispatch[Any]):
    """Base input handler right now: movement"""

    _inputq: List[Action] = []
    """Queued Actions on behalf of the Player AI"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._inputq = []

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Any]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        key = event.sym
        modifier = event.mod
        if key == tcod.event.K_PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            self._inputq.append(DescendAction())
        elif key == tcod.event.K_ESCAPE:
            self._inputq.append(EscapeAction())
        elif key == tcod.event.K_g:
            self._inputq.append(PickupAction())
        elif key in MOVE_KEYS:
            self._inputq.append(MovementAction(*MOVE_KEYS[key]))

    def get_action(self) -> Action:
        if len(self._inputq) == 0:
            return None
        return self._inputq.pop(0)
