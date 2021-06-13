"""
    Input-Handler loops: Main Menu, Gameplay, etc.
    
    Concept stolen shamelessly from https://github.com/HexDecimal/roguelike-tutorial
"""

from typing import Tuple, Any, Optional
from display import Display
from level import Level
from player import Player

# ===== Game Loop Superclass ==============================

class Gameloop:
    _display: Display = None
    _previous: 'Gameloop' = None

    def __init__(self, display: Display, previous: 'Gameloop' = None):
        self._display = display
        self._previous = previous

    def run(self) -> 'Gameloop':  # Quotes: 'forward declaration'
        assert self
        raise NotImplementedError('Cannot use Gameloop raw')


# ===== Main Game Loop ====================================

class MainGameloop (Gameloop):
    """Main gameplay loop: moving around and doing things"""

    _player: Player = None
    _level: Level = None  # TODO: generalization into Engine or something

    def __init__(self, level: Level, player: Player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._level = level
        self._player = player

    def run(self) -> Gameloop:
        self._level.render()
        self._display.present()
        self._display.dispatch_events(self._player.input_handler)
        # TODO: escape action reverts to _previous (return value?)
        self._player.perform()  # TODO: this actually hooks into timer logic
        
        # TODO: if we're doing a submenu, then override this and return to this.  Capture _prevous
        return self

# ===== Main Menu Loop ====================================

# TODO: Need input handler for it

# EOF
