"""
    Abstraction layer for Player and Monster
"""
from __future__ import annotations

from typing import List, Tuple, Set, TYPE_CHECKING
from position import Pos
from item import Item
from combat import fight


if TYPE_CHECKING:
    from level import Level


COLOR_WHITE = (255, 255, 255)


# ===== Entity ============================================

class Entity:
    key: int = 0
    level: Level = None
    name: str = ''
    pos: Pos = None
    mtype: int = ord('?')
    _color: Tuple[int, int, int] = COLOR_WHITE
    pack: List[Item] = None
    state: Set[str] = set()

    # ===== Private etc ===================================

    def __init__(self, pos: Pos = None, level=None, key: int = 0, name: str = '',
                 mtype: int = ord('?'), color: Tuple[int, int, int] = COLOR_WHITE):
        self.pos = pos
        self.level = level
        self.key = key  # TurnQueue key initialize with random.randint(0, TIMER_COST-1)
        self.name = name
        self.mtype = mtype
        self._color = color
        self.pack = []
        self.state = set()

    def __lt__(self, other: 'Entity') -> bool:
        """Comparison for TurnQueue bisect operation"""
        return self.key < other.key

    # ===== Display and Maps ==============================

    @property
    def char(self) -> Tuple[Pos, int, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self.pos, self.mtype, self._color

    # Attach / detach done by derived classes

    def set_pos(self, pos: Pos):  # TODO: side effect, or just do the assignment?
        self.pos = pos

    # ===== Items =========================================

    def add_item(self, item: Item):
        """Add item to inventory"""
        # TODO: pos
        self.pack.append(item)
        # item.set_parent(self)  # TODO: weight and capacity

    def remove_item(self, item: Item):
        """Remove item from inventory"""
        self.pack.remove(item)

    # ===== Combat ========================================

    # Derived classes must implement:
    #   ac property
    #   melee_attack tuple
    #   death (this entity dead)
    #   take_damage
    #   xp_value property
    #   add_hit_msg
    #   add_was_hit_msg
    #   add_miss_msg
    #   add_was_missed_msg

    def add_hit_msg(self, entity):
        # TODO: worth a message if monster brawl
        pass

    def add_was_hit_msg(self, entity):
        pass

    def add_miss_msg(self, entity):
        pass

    def add_was_missed_msg(self, entity):
        pass

    def kill(self, entity: Entity):
        """This entity killed something else"""
        # TODO: worth a message if monster brawl
        pass

    def fight(self, entity: Entity):
        fight(self, entity)

    # ===== Action Callbacks ==============================

    # Derived classes must implement:
    #   descend
    #   fight
    #   pick_up

    def move(self, dx: int, dy: int):
        self.pos = Pos(self.pos.x + dx, self.pos.y + dy)

    def bump(self, pos: Pos):
        assert pos

# ===== Testing ===========================================

# See test_entity.py

# EOF
