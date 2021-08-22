"""
    Input-Handler loops: Main Menu, Gameplay, etc.

    Concept stolen shamelessly from https://github.com/HexDecimal/roguelike-tutorial
"""

from player import Player
from game_states import Gameloop, PlayerDemise
from game_states.player_input import PlayerInputHandler
from game_states.rip_input import RIPInputHandler
from game_states.mainmenu_input import MainMenuInputHandler
from actions import Action
from procgen.rogue_level import RogueLevel
from procgen import game_init


TEXT_COLOR = {'fg': (255, 255, 255), 'bg': (75, 75, 75)}
"""White on gray"""


# ===== RIP State ====================================

class RIPGameState(Gameloop):
    """RIP: Player has died or quit"""
    # TODO: or won

    def __init__(self, player: Player = None, situation: str = '', text: str = '', **kwargs):
        super().__init__(**kwargs)
        self.input_handler = RIPInputHandler()
        self.player = player
        self.situation = situation
        self.text = text

    def run(self) -> Gameloop:
        """I don't feel like drawing out a tombstone"""
        self._display.clear()
        pname = 'wizard' if 'wizard' in self.player.state else 'adventurer'
        if 'wizard' in self.player.state:
            self._display.centered_msg(y=8, string='A DIGNIFIED STRATEGIC WITHDRAWAL BY', **TEXT_COLOR)
        elif self.text == 'quitted':
            self._display.centered_msg(y=8, string='A COWARDLY ESCAPE BY', **TEXT_COLOR)
        else:
            self._display.centered_msg(y=8, string='REST IN PEACE', **TEXT_COLOR)
        self._display.centered_msg(y=10, string=f'A level {self.player.lvl} {pname}', **TEXT_COLOR)
        if self.text != 'quitted':
            self._display.centered_msg(y=12, string=f'Killed by {self.text}', **TEXT_COLOR)  # Note expect 'a XXX'
        self._display.centered_msg(y=14, string=f'On level {self.player.levelno} of The Dungeon of Doom', **TEXT_COLOR)
        self._display.centered_msg(y=16, string=f'Clutching {self.player.purse} gold pieces', **TEXT_COLOR)
        self._display.present()

        # TODO: scorecard if wizard or died: have amulet?  Total winner?
        # TODO: Top scores?

        while True:
            result = self._display.dispatch_event(self.input_handler)
            if result == 'quit':
                break
        del self.player
        return self._previous


# ===== Main Game Loop ====================================

class RunGame(Gameloop):
    """Main gameplay loop: moving around and doing things"""

    def __init__(self, *args, wizard: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = None
        self.level_no = 0
        self.player = None
        self.wizard = wizard

    def run(self) -> Gameloop:
        if self.player is None:
            self.player = Player.factory(wizard=self.wizard)
            self.player.input_handler = PlayerInputHandler(entity=self.player, display=self._display)
            self.player.add_msg('Welcome to the dungeon!')
        if self.player.level is None:
            del self.level
            self.level_no = self.level_no + 1
            self.level = RogueLevel(self.level_no, *self._display.size, self._display, player=self.player)
            if 'wizard' in self.player.state:
                self.player.add_effect('monster detection', 20)
                self.player.add_effect('detect magic', 20)

        # TODO: Cancellation is an exception, player death an exception
        self.player.level.render()
        try:
            self.player.level.run_queue()
        except PlayerDemise as ex:
            del self.level
            return RIPGameState(display=self._display, previous=self._previous, player=self.player, text=str(ex))
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
        self._display.centered_msg(y=11, string="(N)ew Game     ", **TEXT_COLOR)
        self._display.centered_msg(y=12, string='  (w)izard mode', **TEXT_COLOR)
        self._display.centered_msg(y=14, string="(Q)uit         ", **TEXT_COLOR)
        self._display.present()
        result = self._display.dispatch_event(self.input_handler)
        if result == 'new' or result == 'wizard':  # New Game
            game_init()
            return RunGame(display=self._display, previous=self, wizard=True if result == 'wizard' else False)
        if result == 'quit':  # Exit
            return None
        # TODO: continue
        return self

# EOF
