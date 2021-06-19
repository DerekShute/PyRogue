"""
Item basics

Derives from Thing
"""

from typing import Tuple
from position import Pos

# TODO: colors go somewhere
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)


# TODO: Thing goes in pyrogue
# ===== Thing =============================================
# TODO: dataclass?
# TODO: not sure what to do with this.
class Thing:  # union thing
    """
    Structure for monsters and player (superclass)
        (...and items, apparently --DS)
    """
    _pos: Pos = None
    _name: str = '<unknown>'
    _char: int = ord('&')  # No good default
    _color: Tuple[int, int, int] = COLOR_WHITE  # No good default
    _level = None  # TODO: 'parent'

    def __init__(self, name: str, char: str, color: Tuple[int, int, int], pos: Pos = None, level = None):
        self._pos = Pos(pos)
        self._name = name
        self._char = ord(char)
        self._color = color
        self._level = level
        if level is not None:
            level.add_item(self)

    # ===== Display =======================================

    @property
    def char(self) -> Tuple[Pos, int, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self._pos, self._char, self._color

    # ===== Interface =====================================

    @property
    def xy(self) -> Tuple[int, int]:
        return self._pos.xy

    @property
    def pos(self) -> Pos:
        return Pos(self._pos)

    def set_pos(self, pos: Pos):
        self._pos = pos

    def set_level(self, level):
        """Put the Thing on the map, or remove it from the map"""
        if level is None:
            self._level.remove_item(self)
        self._level = level
        if level is not None:
            self._level.add_item(self)

    @property
    def name(self):
        return self._name


# ===== Item ==============================================

class Item (Thing):  # _o internal to union thing originally
    """Anything that can be picked up"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # ===== Interface =====================================
    
    @property
    def quantity(self):
        return None

# TODO: 'collective' objects with _quantity


# ===== Gold ==============================================

class Gold (Item):
    _val: int = 0

    def __init__(self, *args, val: int = 0, **kwargs):
        self._val = val
        super().__init__(*args, name='gold', char='*', color=COLOR_YELLOW, **kwargs)

    def __str__(self) -> str:
        return f'Gold({self._pos},{self._val})'

    def __repr__(self) -> str:
        return f'Gold(pos={repr(self._pos)},val={self._val})'

    # ===== Interface =====================================

    @property
    def quantity(self) -> int:
        return self._val

# ===== TESTING ===========================================

# See test_items.py

# EOF
