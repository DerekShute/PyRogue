import tcod
from actions import Action
from input_handler import InputHandler, CancelHandler
from menu import Menu


# ===== InventoryInputHandler ================================

class InventoryInputHandler(InputHandler):
    """Base input handler for ordinary game input"""
    inventory: Menu = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inventory = None

    def ev_quit(self, event: tcod.event.Quit) -> (InputHandler, Action):
        return CancelHandler(), None

    def ev_keydown(self, event: tcod.event.KeyDown) -> (InputHandler, Action):
        return self.previous, None

    def render_layer(self, display):
        self.inventory = self.entity.render_inventory()
        display.draw_menu(self.entity.pos.x, self.inventory)

# EOF
