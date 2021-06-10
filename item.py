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
class Thing:  # union thing
    """
    Structure for monsters and player (superclass)
        (...and items, apparently --DS)
    """
    _pos: Pos = None
    _name: str = '<unknown>'
    _char: str = '&'  # No good default
    _color: Tuple[int, int, int] = COLOR_WHITE  # No good default

    def __init__(self, name: str, char: str, color: Tuple[int, int, int], pos: Pos = None):
        self._pos = Pos(pos)
        self._name = name
        self._char = char
        self._color = color

    # ===== Interface =====================================

    @property
    def xy(self) -> Tuple[int, int]:
        return self._pos.xy

    @property
    def pos(self):
        return Pos(self._pos)

    # TODO: setter of pos

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def char(self):
        return self._char


# ===== Item ==============================================

class Item (Thing):  # _o internal to union thing originally
    """Anything that can be picked up"""
    # TODO: _name ?
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# TODO: 'collective' objects with _quantity


# ===== Gold ==============================================

class Gold (Item):
    _val: int = 0

    def __init__(self, *args, val: int = 0, **kwargs):
        self._val = val
        super().__init__(*args, name='gold', char='*', color=COLOR_YELLOW, **kwargs)

    def __str__(self):
        return f'Gold({self._pos},{self._val})'


# ===== TESTING ===========================================

if __name__ == '__main__':
    # Note: see test_items
    g = Gold(val=10)
    assert str(g) == 'Gold(@(0,0),10)'
    g = Gold(val=20, pos=Pos((20, 20)))
    assert str(g) == 'Gold(@(20,20),20)'
    assert str(g.pos) == '@(20,20)'
    assert g.name == 'gold'
    assert g.char == '*'
    assert g.color == COLOR_YELLOW

    print('*** Tests passed ***')

# EOF
