import tcod
from typing import List
from actions import Action, QuitAction, DescendAction, MovementAction, PickupAction, UseAction, DropAction
from input_handler import InputHandler, CancelHandler, MOVE_KEYS
from input_handler.response_input import ResponseInputHandler
from entity import Entity


# ===== PlayerInputHandler ================================

class PlayerInputHandler(InputHandler):
    """Base input handler for ordinary game input"""
    entity: Entity = None

    def __init__(self, entity: Entity = None, **kwargs):
        self.entity = entity
        super().__init__(**kwargs)

    def ev_quit(self, event: tcod.event.Quit) -> InputHandler:
        return CancelHandler()  # Out the door immediately

    def ev_keydown(self, event: tcod.event.KeyDown) -> InputHandler:
        key = event.sym
        modifier = event.mod
        if key == tcod.event.K_PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            return self, DescendAction()
        elif key == tcod.event.K_ESCAPE:
            self.entity.advance_msg()
            self.entity.add_msg('Really quit? (Y/N)')
            return ResponseInputHandler('YyNn', QuitAction()), None
        elif key == tcod.event.K_d:
            return self, DropAction()  # TODO: query involved
        elif key == tcod.event.K_g:
            return self, PickupAction()
        elif key == tcod.event.K_u:
            return self, UseAction()  # TODO: query involved, submenu, etc.
        elif key in MOVE_KEYS:
            return self, MovementAction(*MOVE_KEYS[key])
        return self, None

# EOF
