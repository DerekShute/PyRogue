"""
    Monsters, monsters
"""

from typing import Tuple
from position import Pos
from entity import Entity
from level import Level
from ai import AI, ConfusedAI


ORC_GREEN = (63, 127, 63)  # TODO: color per monster somehow?  Subtype?


ACTION_COST = 8


# ===== Monster ===========================================

class Monster(Entity):  # struct monster
    """
    The fundamentals of 'monster'
    """
    exp: int = 0
    lvl: int = 0
    armor: int = 0
    hpt: int = 0       # Hit points, subject to change
    maxhp: int = 0     # Max hit points
    dmg: str = ''
    disguise: int = 0  # For xeroc in disguise
    dest: Pos = None   # AI: where it is going.  Player location, room gold (see room->r_gold)
    ai: AI = None      # TODO: to entity

    # TODO: t_room = room it is in (why?)
    # t_turn = TRUE
    # if player is wearing ring of aggrevation runto(cp)
    #

    def __init__(self, exp: int = 0, lvl: int = 0, armor: int = 0, maxhp: int = 0, dmg: str = '', flags: str = '', **kwargs):
        self.exp = exp
        self.lvl = lvl
        self.armor = armor
        self.maxhp = maxhp
        self.dmg = dmg
        self.hpt = self.maxhp
        self.ai = ConfusedAI()  # TODO: for now.  Also 'mean' does something here
        super().__init__(**kwargs)
        self.state = set(flags.split(' '))

    def __str__(self) -> str:
        return f'Monster({self.name}:{Pos(self.pos)},HP={self.hpt}/{self.maxhp},AC={self.armor},' \
               f'dmg=\'{self.dmg}\',state={self.state})'

    # ===== Display =======================================

    @property
    def char(self) -> Tuple[Pos, str, Tuple[int, int, int]]:
        """Return map display information"""
        return self.pos, self.disguise if self.disguise != 0 else self.mtype, ORC_GREEN

    # ===== Base Interface ================================

    def attach_level(self, level: Level):
        level.add_monster(self)
        self.level = level

    def detach_level(self):
        if self.level is not None:  # Test cases omit having one
            self.level.queue.remove(self)
            self.level.remove_monster(self)
            self.level = None

    # ===== Combat Interface ==============================

    @property
    def ac(self):
        return self.armor

    def death(self, entity: Entity):
        # TODO: certain monsters have consequences: Venus Flytrap, Leprechaun
        # TODO: drops everything in pack
        assert entity
        self.detach_level()

    def melee_attack(self):
        """Attack components just based on stats"""
        # Rogue pegs monster strength at 10 and I don't think it ever modifies
        return self.lvl, 10, self.dmg, 0

    def take_damage(self, amount):
        self.hpt = max(0, self.hpt - amount)

    @property
    def xp_value(self) -> int:
        return self.exp

    # ===== AI ============================================

    def perform(self) -> bool:
        action = self.ai.get_action()
        action.perform(self)
        self.key += ACTION_COST
        # TODO: possibly revert AI
        return True

    def activate(self, key: int) -> 'Monster':
        self.key = key + 5  # TODO: need a bit of noise here
        self.ai.activate()
        return self

    # ===== Action callback ===============================

    # None right now

# ===== Unit Testing ======================================

# is in test_monster.py, elsewhere
