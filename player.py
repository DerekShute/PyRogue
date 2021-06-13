"""
    Player
"""

import random
from dataclasses import dataclass
from item import Item
from position import Pos
from typing import Tuple

HUNGERTIME = 1300
"""Turns before hunger state change, I guess"""

INIT_STATS = {
    'stren': 16,
    'arm': 10,    # Unarmed
    'maxhp': 12,
    'dmg': '1x4'  # Unarmed damage
}


def strike(dmg_str: str) -> bool:
    """Make X attacks - the damage string denotes the number of attacks"""
    # TODO: goes elsewhere
    for attack in dmg_str.split('/'):
        # TODO make attack type
        dmg = roll(attack)  # TODO: THIS DOES NOT WORK
        assert dmg
    return True


def roll(die_roll: str) -> int:
    """dmg as string in format COUNTxSIDES"""
    # TODO: goes elsewhere
    # TODO: there's special rules for one of the dmg descriptors
    count, _, sides = die_roll.partition('x')
    total = 0
    count = int(count)  # No elegant way to do this with _ in the middle
    sides = int(sides)
    while count > 0:
        total = total + random.randint(1, sides)
        count = count - 1
    return total


ADD_DMG = (-7, -6, -5, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0-15
           1, 1, 2, 3, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6)
"""adjustments to damage done due to strength (0-31)"""


STR_PLUS = (-7, -6, -5, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0,  # 0-15
            0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3)
"""adjustments to hit probabilities due to strength"""

PLAYER_CHAR = '@'

PLAYER_COLOR = (255, 255, 255)  # White TODO: consolidate definitions


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

    @property
    def melee_hit_adj(self):
        """Attack damage just based on stats"""
        # TODO: effect of rings
        return STR_PLUS[self.stren]

    @property
    def melee_dmg_adj(self):
        """Attack damage just based on stats"""
        return ADD_DMG[self.stren]

    def melee_dmg(self):
        """Attack damage just based on stats"""
        return roll(self.dmg) + self.melee_dmg_adj

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

    def __init__(self, pos: Pos = None, stats: Stats = None, food_left: int = HUNGERTIME):
        self._stats = stats
        self._pos = pos
        self._food_left = food_left

    def __str__(self):
        return f'Player({Pos(self._pos)},{self._stats})'

    def __repr__(self):
        return f'Player(pos={repr(self._pos)},stats={repr(self._stats)}, food_left={self._food_left})'

    # TODO: methods to retrieve effective AC, hit points, etc.

    # ===== Display =======================================

    @property
    def char(self) -> Tuple[Pos, str, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self._pos, PLAYER_CHAR, PLAYER_COLOR

    # ===== Base Interface ================================

    def set_pos(self, pos: Pos):
        self._pos = pos

    @property
    def pos(self) -> Pos:
        return self._pos

    @property
    def name(self) -> str:
        return 'Player'

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
    def melee_hit_adj(self):
        """Attack damage just based on stats"""
        # TODO: effect of rings
        return self._stats.melee_hit_adj

    @property
    def melee_dmg_adj(self):
        """Attack damage just based on stats"""
        # TODO: effect of rings and weapon
        return self._stats.melee_dmg_adj

    def melee_dmg(self):
        """Melee attack damage"""
        # TODO: effect of weapons
        return self._stats.melee_dmg()

    @property
    def ac(self):
        """Armor class"""
        # TODO: account for armor, rings, whatever
        return self._stats.ac

    # ===== Constructor ===================================

    @staticmethod
    def factory(pos: Pos = None):   # init_player
        plr = Player(pos=pos, stats=Stats(**INIT_STATS))
        # cur_armor Armor: ring_mail, known, a_class = RING_MAIL
        # one food
        # cur_weapon Weapon: mace, known, hplus=1 dplus=1
        # weapon: BOW, hplus=1, known
        # to pack: 25 + rnd(15) arrows, known
        return plr


# ===== Unit Test =========================================
# TODO: goes elsewhere

if __name__ == '__main__':
    p = Player.factory(pos=Pos(3, 3))
    assert repr(eval(repr(p))) == repr(p)

    print('*** Tests Passed ***')
# EOF
