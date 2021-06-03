"""
    Position!
"""
from __future__ import annotations
from typing import Tuple


# ===== Pos ===============================================

class Pos:  # struct coord
    """
    A location or direction/distance
    Contains
        _x, _y : map coordinates
    """
    _x: int = 0
    _y: int = 0

    def __init__(self, pos: Tuple = None, x: int = None, y: int = None):
        """
        Params
            pos : tuple (x, y)
        """
        if pos is not None:
            self._x, self._y = tuple(pos)  # "unpack" is the magic word
        elif x is not None:
            self._x = x
        if y is not None:
            self._y = y

    def __eq__(self, other) -> bool:
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

    def __str__(self) -> str:
        return f'@({self._x},{self._y})'

    def __iter__(self):
        """
        This does the magic if you want tuple(Pos)
        """
        yield self._x
        yield self._y

    # ===== Interface Routines =====
    @property
    def x(self) -> int:
        """
        Return x coordinate of thing
        """
        return self._x

    @property
    def y(self,) -> int:
        """
        Return y coordinate of thing
        """
        return self._y

    @property
    def xy(self) -> Tuple[int, int]:
        """
        Return position of a thing as a tuple
        """
        return self._x, self._y


# ===== TESTING ===========================================

if __name__ == "__main__":
    p = Pos((10, 20))
    # print(p)
    assert str(p) == '@(10,20)'
    # print(Pos(p))
    # print(p.x)
    assert p.x == 10
    # print(p.y)
    assert p.y == 20
    # print(p.xy)
    assert p.xy == (10, 20)
    assert not Pos((1, 1)) == Pos((2, 2))
    assert Pos((1, 2)) == Pos(x=1, y=2)

    print('*** Tests passed ***')

# EOF
