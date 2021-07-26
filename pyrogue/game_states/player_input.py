import tcod
from actions import QuitAction, DescendAction, BumpAction, PickupAction, UseAction, DropAction, EquipAction, ZapAction
from game_states import InputHandler, CancelHandler, MOVE_KEYS
from game_states.chat_input import ChatInputHandler
from game_states.response_input import ResponseInputHandler
from game_states.inventory_input import InventoryInputHandler


# ===== PlayerInputHandler ================================

class PlayerInputHandler(InputHandler):
    """Base input handler for ordinary game input"""

    def ev_quit(self, event: tcod.event.Quit):
        return CancelHandler()  # Out the door immediately

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        modifier = event.mod

        if self.entity.msg_count > 1:
            self.entity.advance_msg()
            return self

        if key == tcod.event.K_SLASH:
            return ChatInputHandler(previous=self)

        if key == tcod.event.K_PERIOD and modifier & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
            return DescendAction()

        if key == tcod.event.K_ESCAPE:
            return ResponseInputHandler(previous=self,
                                        responses='YyNn',
                                        entity=self.entity,
                                        string='Really quit? (y/N)',
                                        action=QuitAction())
        if key == tcod.event.K_d:
            return InventoryInputHandler(usage='drop',
                                         previous=self,
                                         entity=self.entity,
                                         action=DropAction(),
                                         msg='Drop which item?')

        if key == tcod.event.K_e:
            return InventoryInputHandler(usage='equip',
                                         previous=self,
                                         entity=self.entity,
                                         action=EquipAction(),
                                         msg='Equip which item?')

        if key == tcod.event.K_g:
            return PickupAction()

        if key == tcod.event.K_i:
            return InventoryInputHandler(previous=self, entity=self.entity)

        elif key == tcod.event.K_u:
            return InventoryInputHandler(usage='use',
                                         previous=self,
                                         entity=self.entity,
                                         action=UseAction(),
                                         msg='Use which item?')

        elif key == tcod.event.K_z:
            return InventoryInputHandler(usage='zap',
                                        previous=self,
                                        entity=self.entity,
                                        action=ZapAction(),
                                        msg='Zap which item?')

        if key in MOVE_KEYS:
            return BumpAction(*MOVE_KEYS[key])

        return self

    def render_layer(self, display):
        # Note: original uses line 0, this uses last line
        if self.entity is not None:
            xsize, ysize = display.size
            display.msg(x=0, y=ysize - 1, string=self.entity.curr_msg.ljust(xsize))

# EOF
