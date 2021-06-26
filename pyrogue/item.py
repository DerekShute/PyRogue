"""
    Items
"""

from typing import Tuple
from position import Pos

# TODO: colors go somewhere
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)


# ===== Item =============================================
class Item:  # union thing
    """
    Superclass for all items
    Thing (originally): Superclass structure for monsters / player / items
    """
    pos: Pos
    name: str
    _char: int  # Note: No good default
    _color: Tuple[int, int, int]  # No good default
    parent = None  # Level or Monster or Player (inventories)

    def __init__(self, name: str = '<unknown>', char: str = '&', color: Tuple[int, int, int] = COLOR_WHITE,
                 pos: Pos = None, parent=None):
        self.pos = pos
        self.name = name
        self._char = ord(char)
        self._color = color
        self.parent = parent
        if parent is not None:
            parent.add_item(self)

    # ===== Display =======================================

    @property
    def char(self) -> Tuple[Pos, int, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self.pos, self._char, self._color

    # ===== Interface =====================================

    @property
    def xy(self) -> Tuple[int, int]:
        return self.pos.xy

    def set_pos(self, pos: Pos):
        self.pos = pos

    def set_parent(self, parent):
        """Move Item between map and some inventory"""
        if parent is None and self.parent is not None:
            self.parent.remove_item(self)
        self.parent = parent
        if parent is not None:
            self.parent.add_item(self)

    @property
    def quantity(self):
        return None
        # TODO: 'collective' objects with _quantity


# ===== Items with Quantity ===============================

class QuantityItem(Item):
   quantity: int = 0

   def __init__(self, quantity: int = 0, **kwargs):
       self.quantity = quantity
       super().__init__(**kwargs)


# ===== Gold ==============================================

class Gold(QuantityItem):
    def __init__(self, **kwargs):
        super().__init__(name='gold', char='*', color=COLOR_YELLOW, **kwargs)

    def __str__(self) -> str:
        return f'Gold({self.pos},{self.quantity})'

    def __repr__(self) -> str:
        return f'Gold(pos={repr(self.pos)},quantity={self.quantity})'


# ===== TESTING ===========================================

# See test_items.py

# EOF
