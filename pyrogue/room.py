"""
Simple rooms
"""
from position import Pos
import random
from typing import Tuple


def rectangle(p1: Pos, p2: Pos) -> Tuple[slice, slice]:
    """Simple rectangle inclusive of p1 and p2"""
    return slice(p1.x, p2.x), slice(p1.y, p2.y)


# ===== Room ==============================================

class Room:  # struct room
    """
    Room Structure
    """
    # TODO maybe a dataclass
    _pos: Pos = None  # Upper left
    _max: Pos = None  # Size TODO lower right?
    found: bool = False

    def __init__(self, pos=None, size=None):
        self._pos = Pos(pos)
        self._max = Pos(size)
        self.found = False

    def __str__(self):
        return 'Room {}-{}'.format(self._pos, self._max)

    # ===== Interface routines ============================

    @property
    def x(self) -> int:
        return self._pos.x

    @property
    def max_x(self) -> int:
        if self._max.x == 0:
            return self._pos.x  # Math becomes weird
        return self._pos.x + self._max.x - 1

    @property
    def y(self) -> int:
        return self._pos.y

    @property
    def max_y(self) -> int:
        if self._max.y == 0:
            return self._pos.y  # Math becomes weird
        return self._pos.y + self._max.y - 1

    @property
    def xy(self) -> Tuple[int, int]:
        return self._pos.xy

    @property
    def center(self) -> Pos:
        """Stolen from tutorial"""
        center_x = (self.x + self.max_x) // 2
        center_y = (self.y + self.max_y) // 2
        return Pos(center_x, center_y)

    @property
    def pos(self) -> Pos:
        return Pos(self._pos)

    @property
    def max_pos(self) -> Pos:
        return Pos((self._pos.x + self._max.x, self._pos.y + self._max.y))

    @property
    def rnd_pos(self) -> Pos:
        """
        Pick a random spot in a room.  Inclusive of border edges
        """
        return Pos((random.randint(self.x, self.max_x), random.randint(self.y, self.max_y)))

    def shadow(self):
        """Return the inner area of this room as a 2D array index."""
        return rectangle(self._pos, self.max_pos)

    def inside(self, pos: Pos) -> bool:
        """Is this position inside the room?"""
        return pos.x >= self.x and pos.x <= self.max_x and pos.y >= self.y and pos.y <= self.max_y


# ===== UNIT TEST =========================================

# See test_player.py

# EOF
