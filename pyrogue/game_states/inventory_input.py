import tcod
from actions import Action, ZapAction
from game_states import InputHandler
from game_states.target_input import TargetInputHandler
from menu import Menu


# ===== InventoryInputHandler ================================

class InventoryInputHandler(InputHandler):
    """Base input handler for ordinary game input"""
    inventory: Menu = None
    usage: str
    msg: str
    action: Action

    def __init__(self, action: Action = None, msg: str = '', usage: str = '', **kwargs):
        super().__init__(**kwargs)
        self.inventory = None
        self.usage = usage
        self.msg = msg
        self.action = action

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        if self.usage != '':
            if key >= ord('a') and key <= ord('z'):
                self.action.incorporate(key - ord('a'))
                if isinstance(self.action, ZapAction):
                    return TargetInputHandler(usage='zap',
                                              previous=self.previous,
                                              entity=self.entity,
                                              action=self.action,
                                              msg='Zap where?')
                else:
                    return self.action
        return self.previous

    def render_layer(self):
        self.inventory = self.entity.render_inventory(self.usage)
        self.display.draw_menu(self.entity.pos.x, self.inventory)
        xsize, ysize = self.display.size
        self.display.msg(x=0, y=ysize - 1, string=self.msg.ljust(xsize))  # TODO: all messages appear to go here

# EOF
