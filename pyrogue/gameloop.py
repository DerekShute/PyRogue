"""
    Input-Handler loops: Main Menu, Gameplay, etc.

    Concept stolen shamelessly from https://github.com/HexDecimal/roguelike-tutorial
"""

from display import Display
from player import Player
from input_handler import InputHandler, CancelHandler
from input_handler.player_input import PlayerInputHandler
from input_handler.mainmenu_input import MainMenuInputHandler
from rogue_level import RogueLevel

# TODO: These are everywhere
NUMCOLS = 80
NUMLINES = 25

# ===== Game Loop Superclass ==============================

class Gameloop:
    _display: Display = None
    _previous: 'Gameloop' = None
    _input_handler: InputHandler = None

    def __init__(self, display: Display, previous: 'Gameloop' = None):
        self._display = display
        self._previous = previous

    def run(self) -> 'Gameloop':  # Quotes: 'forward declaration'
        assert self
        raise NotImplementedError('Cannot use Gameloop raw')


# ===== Main Game Loop ====================================

class MainGameloop(Gameloop):
    """Main gameplay loop: moving around and doing things"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_handler = PlayerInputHandler()
        self.level = None
        self.level_no = 0
        self.player = None

    def run(self) -> Gameloop:
        if self.player is None:
            self.player = Player.factory()
            self.player.add_msg('Welcome to the dungeon!')
        if self.player.level is None:
            del self.level
            self.level_no = self.level_no + 1
            self.level = RogueLevel(self.level_no, *self._display.size, self._display, player=self.player)

        self.player.level.render()
        self._display.present(self.player)
        if self.player.input_handler is None:  # New to here
            self.player.input_handler = self.input_handler
        self.player.input_handler = self._display.dispatch_event(self.player.input_handler)
        if isinstance(self.player.input_handler, CancelHandler):
            del self.player
            del self.level
            return self._previous
        self.player.level.run_queue()
        # TODO: if we're doing a submenu, then override this and return to this.  Capture _prevous
        return self


# ===== Main Menu State ====================================

class MainMenuState(Gameloop):
    """Main gameplay loop: moving around and doing things"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_handler = MainMenuInputHandler()

    def run(self) -> Gameloop:
        self._display.clear()
        self._display.centered_msg(y=9, string='WELCOME TO THE DUNGEON OF DOOM', fg=(255, 255, 255), bg=(100, 100, 100))
        self._display.centered_msg(y=11, string="(N)ew Game  ", fg=(255, 255, 255), bg=(100, 100, 100))
        self._display.centered_msg(y=13, string="(Q)uit      ", fg=(255, 255, 255), bg=(100, 100, 100))
        self._display.present()
        result = self._display.dispatch_event(self.input_handler)
        if result == 'new':  # New Game
            return MainGameloop(display=self._display, previous=self)
        if result == 'quit':  # Exit
            return None
        # TODO: continue
        return self

# EOF
