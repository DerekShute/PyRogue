"""
    Input-Handler loops: Main Menu, Gameplay, etc.

    Concept stolen shamelessly from https://github.com/HexDecimal/roguelike-tutorial
"""

from player import Player
from game_states import Gameloop
from game_states.player_input import PlayerInputHandler
from game_states.rip_input import RIPInputHandler
from game_states.mainmenu_input import MainMenuInputHandler
from procgen.rogue_level import RogueLevel


TEXT_COLOR = {'fg': (255, 255, 255), 'bg': (75, 75, 75)}
"""White on gray"""


# ===== RIP State ====================================

class RIPGameState(Gameloop):
    """RIP: Player has died or quit"""
    # TODO: or won

    def __init__(self, player: Player = None, situation: str = '', **kwargs):
        super().__init__(**kwargs)
        self.input_handler = RIPInputHandler()
        self.player = player
        self.situation = situation

    def run(self) -> Gameloop:
        """I don't feel like drawing out a tombstone"""
        self._display.clear()
        # Killed by
        if self.player.demise == 'quit':
            self._display.centered_msg(y=8, string='A COWARDLY ESCAPE BY', **TEXT_COLOR)
        else:
            self._display.centered_msg(y=8, string='REST IN PEACE', **TEXT_COLOR)
        self._display.centered_msg(y=10, string=f'A level {self.player.lvl} adventurer', **TEXT_COLOR)
        self._display.centered_msg(y=12, string=f'On level {self.player.levelno} of The Dungeon of Doom', **TEXT_COLOR)
        self._display.centered_msg(y=14, string=f'Clutching {self.player.purse} gold pieces', **TEXT_COLOR)
        self._display.present()
        # TODO: have amulet?  Total winner?
        # TODO: Top scores?
        while True:
            result = self._display.dispatch_event(self.input_handler)
            if result == 'quit':
                break
        del self.player
        return self._previous


# ===== Main Game Loop ====================================

class MainGameloop(Gameloop):
    """Main gameplay loop: moving around and doing things"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = None
        self.level_no = 0
        self.player = None

    def run(self) -> Gameloop:
        if self.player is None:
            self.player = Player.factory()
            self.input_handler = PlayerInputHandler(entity=self.player)
            self.player.add_msg('Welcome to the dungeon!')
        if self.player.level is None:
            del self.level
            self.level_no = self.level_no + 1
            self.level = RogueLevel(self.level_no, *self._display.size, self._display, player=self.player)

        self.player.level.render()
        self.input_handler = self._display.display(self.input_handler)
        self.player.level.run_queue()
        if self.player.demise is not None:
            del self.level
            return RIPGameState(display=self._display, previous=self._previous, player=self.player)
        return self


# ===== Main Menu State ====================================

class MainMenuState(Gameloop):
    """Main gameplay loop: moving around and doing things"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_handler = MainMenuInputHandler()

    def run(self) -> Gameloop:
        self._display.clear()
        self._display.centered_msg(y=9, string='WELCOME TO THE DUNGEON OF DOOM', **TEXT_COLOR)
        self._display.centered_msg(y=11, string="(N)ew Game  ", **TEXT_COLOR)
        self._display.centered_msg(y=13, string="(Q)uit      ", **TEXT_COLOR)
        self._display.present()
        result = self._display.dispatch_event(self.input_handler)
        if result == 'new':  # New Game
            return MainGameloop(display=self._display, previous=self)
        if result == 'quit':  # Exit
            return None
        # TODO: continue
        return self

# EOF
