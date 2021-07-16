import tcod
from actions import Action
from game_states import InputHandler, CancelHandler
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

    def ev_quit(self, event: tcod.event.Quit):
        return CancelHandler()

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        if self.usage != '':
            if key >= ord('a') and key <= ord('z'):
                return self.action.incorporate(key - ord('a'))
        return self.previous

    def render_layer(self, display):
        self.inventory = self.entity.render_inventory(self.usage)
        display.draw_menu(self.entity.pos.x, self.inventory)
        xsize, ysize = display.size
        display.msg(x=0, y=ysize - 1, string=self.msg.ljust(xsize))  # TODO: all messages appear to go here

# EOF
