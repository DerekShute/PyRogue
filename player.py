"""
    Player
"""

import random
from dataclasses import dataclass
from item import Item
from position import Pos
from typing import Tuple
from player_input import PlayerInputHandler
from message import MessageBuffer
from combat import fight


HUNGERTIME = 1300
"""Turns before hunger state change, I guess"""

INIT_STATS = {
    'level': 1,
    'stren': 16,
    'arm': 10,    # Unarmed
    'maxhp': 12,
    'dmg': '1x4'  # Unarmed damage
}

PLAYER_CHAR = ord('@')

PLAYER_COLOR = (255, 255, 255)  # White TODO: consolidate definitions

HIT_NAMES = (
    "scored an excellent hit on",
    "hit",
    "have injured",
    "swing and hit",
    "scored an excellent hit on",
    "hit",
    "has injured",
    "swings and hits"
)

PLAYER_MISS = (
    "miss",
    "swing and miss",
    "barely miss",
    "don't hit"
)

MONSTER_MISS = (
    "misses",
    "swings and misses",
    "barely misses",
    "doesn't hit",
)


# ===== Stats =============================================

@dataclass
class Stats:  # struct stats
    """
    Structure describing a fighting being
    """
    stren: int
    arm: int   # TODO: base AC 10
    dmg: str
    maxhp: int
    hpt: int = None
    exp: int = 0  # TODO: xp count for player, xp value for monsters
    level: int = 0

    def __post_init__(self):
        if self.hpt is None:
            self.hpt = self.maxhp

    def __str__(self):
        return f'Stats(Str={self.stren},XP={self.exp}({self.level}),AC={self.arm},' \
               f'Dmg=\'{self.dmg}\',HP={self.hpt}/{self.maxhp})'

    # ===== Combat ========================================

    def melee_attack(self):
        """Attack components just based on stats"""
        return self.level, self.stren, self.dmg

    @property
    def ac(self):
        """Armor class"""
        return self.arm


# ===== Player ============================================

class Player:
    _pos: Pos = None
    _food_left: int
    _stats: Stats = None
    _cur_armor: Item = None
    _level = None
    _input: PlayerInputHandler = None
    _msg: MessageBuffer = None
    _purse: int = 0  # Gold collected, an infinitely large pocket
    levelno: int = 0  # How deep in the dungeon? (May disconnect from _level, so keep here)

    def __init__(self, pos: Pos = None, stats: Stats = None, food_left: int = HUNGERTIME,
                 msg: MessageBuffer = None):
        self._stats = stats
        self._pos = pos
        self._food_left = food_left
        self._input = PlayerInputHandler()
        self._msg = msg
        self.levelno = 0

    def __str__(self):
        return f'Player({Pos(self._pos)},{self._stats})'

    def __repr__(self):
        # TODO: self._input not reconstructable
        return f'Player(pos={repr(self._pos)},stats={repr(self._stats)}, food_left={self._food_left})'

    # TODO: methods to retrieve effective AC, hit points, etc.

    # ===== Display =======================================

    @property
    def char(self) -> Tuple[Pos, str, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self._pos, PLAYER_CHAR, PLAYER_COLOR

    @property
    def display(self) -> str:
        """Status-line"""
        # TODO: originally 'Level: <dungeon level> Gold: %d Hp: %d/%d Str:%d(%d) Arm: %d Exp:%lvl/%xp <status>'
        return f'Level: {self.levelno} Gold: {self._purse} Hp:{self._stats.hpt}/{self._stats.maxhp} ' \
               f'Str:{self._stats.stren}({self._stats.stren}) Arm: ? Exp:{self._stats.level}({self._stats.exp})'

    # ===== Base Interface ================================

    def set_pos(self, pos: Pos):
        self._pos = pos

    @property
    def pos(self) -> Pos:
        return self._pos

    @property
    def name(self) -> str:
        return 'Player'

    @property
    def level(self):
        return self._level

    def attach_level(self, level):
        self._level = level
        self.levelno = level.levelno if level is not None else self.levelno

    def add_msg(self, text: str):
        if self._msg is not None:
            self._msg.add(text)  # TODO: censor message for visibility of source, etc.

    @property
    def curr_msg(self):
        return self._msg.msg if self._msg.msg else f'{self.display}'

    # ===== Action callbacks ==============================

    def fight(self, entity):
        fight(self, entity)

    def bump(self, pos: Pos):
        self.add_msg('Ouch!')

    def descend(self):
        self.add_msg('You stumble down the stairs.')  # TODO: real message?
        self._level.remove_player()
        self.levelno = self.levelno + 1
        # Once not on the level, the game main loop takes care of it

    def move(self, dx: int, dy: int):
        self._pos = Pos(self._pos.x + dx, self._pos.y + dy)  # TODO: Pos addition
        # TODO : returns timer tick cost

    def pick_up(self, item: Item):
        if item is None:
            self.add_msg('No item there to pick up!')
            return
        if item.name == 'gold':
            # AD&D would award XP for treasure, but not Rogue apparently
            self.add_msg(f'You pick up {item.quantity} gold pieces!')
            self._purse = self._purse + item.quantity
            item.set_level(None)
            del item  # Poof
        else:
            self.add_msg(f'You pick up the {item.name}')
            # TODO: remove from level, add to inventory
            # TODO: after verifying you can

    @property
    def input_handler(self):
        """Gameloop needs input handler so it can collect actions"""
        return self._input

    # ===== Timer / AI / Action Interface ==========================

    def perform(self):
        # TODO: returns timer tick cost
        action = self._input.get_action()
        if action is not None:
            self.add_msg('')
            action.perform(self)

    # ===== Stat interface ================================
    # TODO: who cares?
    @property
    def lvl(self) -> int:
        return self._stats.level

    @property
    def hpt(self) -> int:
        return self._stats.hpt

    @property
    def exp(self) -> int:
        return self._stats.exp

    @property
    def stren(self) -> int:
        return self._stats.stren

    # ===== Combat Interface ==============================

    @property
    def ac(self):
        """Armor class"""
        # TODO: account for armor, rings, whatever
        return self._stats.ac

    def add_hit_msg(self, entity):
        self.add_msg(f'You {random.choice(HIT_NAMES)} the {entity.name}')

    def add_was_hit_msg(self, entity):
        self.add_msg(f'The {entity.name} {random.choice(HIT_NAMES)} you')

    def add_miss_msg(self, entity):
        self.add_msg(f'You {random.choice(PLAYER_MISS)} the {entity.name}')

    def add_was_missed_msg(self, entity):
        self.add_msg(f'The {entity.name} {random.choice(MONSTER_MISS)} you')

    def death(self, entity):
        self.msg(f'You were killed by the {entity.name}!')  # TODO traps?
        # TODO raise end-of-game

    def kill(self, entity):  # TODO: monster
        self.add_msg(f'You killed the {entity.name}!')
        self._stats.exp = self._stats.exp + entity.xp_value
        # TODO: level gain

    def melee_attack(self):
        """Melee attack (level, strength, dmg)"""
        # TODO: effect of weapons and objects.  I think it can add to level instead of an explicit bonus
        return self._stats.melee_attack()

    def take_damage(self, amount: int):
        """Took it on the chin"""
        self._stats.hpt = max(0, self._stats.hpt - amount)

    @property
    def xp_value(self) -> int:
        return 0  # TODO: how did we get here?

    # ===== Constructor ===================================

    @staticmethod
    def factory(pos: Pos = None, msg: MessageBuffer = None):   # init_player
        plr = Player(pos=pos, stats=Stats(**INIT_STATS), msg=msg)
        # cur_armor Armor: ring_mail, known, a_class = RING_MAIL
        # one food
        # cur_weapon Weapon: mace, known, hplus=1 dplus=1
        # weapon: BOW, hplus=1, known
        # to pack: 25 + rnd(15) arrows, known
        return plr


# ===== Unit Test =========================================

# See test_player.py

# EOF
