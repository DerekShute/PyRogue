"""
    Position!
"""
from __future__ import annotations
from typing import Any


# ===== Pos ===============================================

class Pos:  # struct coord
    """
    A location or direction/distance
    Contains
        _x, _y : map coordinates
    """
    _x: int = 0
    _y: int = 0

    def __init__(self, x: Any = None, y: int = None):
        self._x = 0
        self._y = 0
        if x is None and y is None:
            self._x = 0
            self._y = 0
        elif type(x) is int:
            self._x = x
            if y is not None:
                self._y = y
        else:
            self._x, self._y = tuple(x)  # "unpack"

    def __eq__(self, other) -> bool:
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

    def __str__(self) -> str:
        return f'@({self._x},{self._y})'

    def __repr__(self) -> str:
        return f'Pos({self._x},{self._y})'

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

# Is in test_position.py

# EOF
