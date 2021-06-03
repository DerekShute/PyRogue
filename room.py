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

    def __init__(self, pos=None, size=None):
        self._pos = Pos(pos)
        self._max = Pos(size)

    def __str__(self):
        return 'Room {}-{}'.format(self._pos, self._max)

    # ===== Interface routines ============================

    @property
    def x(self) -> int:
        return self._pos.x

    @property
    def max_x(self) -> int:
        return self._pos.x + self._max.x - 1

    @property
    def y(self) -> int:
        return self._pos.y

    @property
    def max_y(self) -> int:
        return self._pos.y + self._max.y - 1

    @property
    def xy(self) -> Tuple[int, int]:
        return self._pos.xy

    @property
    def center(self) -> Pos:
        """Stolen from tutorial"""
        center_x = (self.x + self.max_x) // 2
        center_y = (self.y + self.max_y) // 2
        return Pos((center_x, center_y))

    @property
    def pos(self) -> Pos:
        return Pos(self._pos)

    @property
    def max_pos(self) -> Pos:
        return Pos((self._pos.x + self._max.x, self._pos.y + self._max.y))

    @property
    def rnd_pos(self) -> Pos:
        """
        Pick a random spot in a room
        """
        return Pos((random.randint(self.x, self.max_x - 2) + 1,
                    random.randint(self.y, self.max_y - 2) + 1))

    def shadow(self):
        """Return the inner area of this room as a 2D array index."""
        return rectangle(self._pos, self.max_pos)


# ===== UNIT TEST =========================================
if __name__ == '__main__':
    r = Room(Pos((0, 0)), Pos((10, 20)))
    # print(r.center.x)
    assert r.center.x == 4
    # print(r.center.y)
    assert r.center.y == 9
    assert str(r) == 'Room @(0,0)-@(10,20)'
    p = r.rnd_pos
    # print(p)
    assert str(r.max_pos) == '@(10,20)'
    assert p.x > r.x
    assert p.x < r.max_x
    assert p.y > r.y
    assert p.y < r.max_y
    assert str(r.shadow()) == '(slice(0, 10, None), slice(0, 20, None))'

    print('*** Tests passed ***')
# EOF
