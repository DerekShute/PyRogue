"""
    Abstraction layer for Player and Monster
"""
from __future__ import annotations

from typing import Tuple, TYPE_CHECKING
from position import Pos

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
    
    # ===== Private etc ===================================

    def __init__(self, pos: Pos = None, level = None, key: int = 0, name: str = '',
                 mtype: int = ord('?'), color: Tuple[int, int, int] = COLOR_WHITE):
        self.pos = pos
        self.level = level
        self.key = key  # TurnQueue key initialize with random.randint(0, TIMER_COST-1)
        self.name = name
        self.mtype = mtype
        self._color = color

    def __lt__(self, other: 'Entity') -> bool:
        """Comparison for TurnQueue bisect operation"""
        return self.key < other.key

    # ===== Base Interface ================================


    # ===== Display and Maps ==============================

    @property
    def char(self) -> Tuple[Pos, int, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self.pos, self.mtype, self._color

    # Attach / detach done by derived classes

    def set_pos(self, pos: Pos):  # TODO: side effect, or just do the assignment?
        self.pos = pos

    # ===== Combat ========================================

    # Derived classes must implement:
    #   ac property
    #   melee_attack tuple
    #   death (this entity dead)
    #   kill  (this entity kills something else)
    #   take_damage
    #   xp_value property
    #   add_hit_msg
    #   add_was_hit_msg
    #   add_miss_msg
    #   add_was_missed_msg

    # ===== Action Callbacks ==============================

    # Derived classes must implement:
    #   bump
    #   descend
    #   fight
    #   move
    #   pick_up
    
# ===== Testing ===========================================

# See test_entity.py

# EOF
