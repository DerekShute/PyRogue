import tcod
from input_handler import InputHandler


# ===== Main Menu Input management ========================

class MainMenuInputHandler(InputHandler):
    """Input management for Main Menu: returns strings for Main Menu to juggle"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def ev_quit(self, event: tcod.event.Quit) -> str:
        return 'quit'

    def ev_keydown(self, event: tcod.event.KeyDown) -> str:
        key = event.sym
        if key == tcod.event.K_n:  # New Game
            return 'new'
        if key == tcod.event.K_ESCAPE or key == tcod.event.K_q:
            return 'quit'
        if key == tcod.event.K_c:
            return 'continue'
        return ''  # Nonsense

    # We implement these to cut down on the event chatter

    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> None:
        return ''

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> None:
        return ''

# EOF
