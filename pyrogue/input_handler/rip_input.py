import tcod
from input_handler import InputHandler


# ===== RIP Input management ========================

class RIPInputHandler(InputHandler):
    """Input management for Main Menu: returns strings for Main Menu to juggle"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def ev_quit(self, event: tcod.event.Quit) -> str:
        return 'quit'

    def ev_keydown(self, event: tcod.event.KeyDown) -> str:
        return 'quit'

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> str:
        return ''

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> str:
        return ''

# EOF
