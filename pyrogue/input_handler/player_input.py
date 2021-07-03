import tcod
from actions import Action, QuitAction, DescendAction, MovementAction, PickupAction, UseAction, DropAction, EquipAction
from input_handler import InputHandler, CancelHandler, MOVE_KEYS
from input_handler.response_input import ResponseInputHandler
from input_handler.inventory_input import InventoryInputHandler


# ===== PlayerInputHandler ================================

class PlayerInputHandler(InputHandler):
    """Base input handler for ordinary game input"""

    def ev_quit(self, event: tcod.event.Quit) -> (InputHandler, Action):
        return CancelHandler(), None  # Out the door immediately

    def ev_keydown(self, event: tcod.event.KeyDown) -> (InputHandler, Action):
        key = event.sym
        modifier = event.mod

        if self.entity.msg_count > 1:
            self.entity.advance_msg()
            return self, None

        if key == tcod.event.K_PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            return self, DescendAction()
        elif key == tcod.event.K_ESCAPE:
            return (ResponseInputHandler(previous=self,
                                         responses='YyNn',
                                         string='Really quit? (y/N)',
                                         action=QuitAction()),
                    None)
        elif key == tcod.event.K_d:
            return self, DropAction()  # TODO: query involved
        elif key == tcod.event.K_e:
            return (InventoryInputHandler(usage='equip',
                                          previous=self,
                                          entity=self.entity,
                                          action=EquipAction(),
                                          msg='Equip which item?'),
                    None)
        elif key == tcod.event.K_g:
            return self, PickupAction()
        elif key == tcod.event.K_i:
            return InventoryInputHandler(previous=self, entity=self.entity), None
        elif key == tcod.event.K_u:
            return (InventoryInputHandler(usage='use',
                                          previous=self,
                                          entity=self.entity,
                                          action=UseAction(),
                                          msg='Use which item?'),
                    None)
        elif key in MOVE_KEYS:
            return self, MovementAction(*MOVE_KEYS[key])
        return self, None

    def render_layer(self, display):
        # Note: original uses line 0, this uses last line
        if self.entity is not None:
            xsize, ysize = display.size
            display.msg(x=0, y=ysize - 1, string=self.entity.curr_msg.ljust(xsize))

# EOF
