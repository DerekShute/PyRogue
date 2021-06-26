"""
    Items
"""

from typing import Tuple
from position import Pos
# TODO: can't import Entity because recursion

# TODO: colors go somewhere
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BURNTSIENNA = (138,54,15)  # AKA "brown"

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
        self.parent = parent

    @property
    def quantity(self):
        return None
        # TODO: 'collective' objects with _quantity

    # ===== Item callbacks from Entity ====================

    def use(self, entity) -> bool:
        entity.add_msg('Can\'t do that with a {self.name}!')
        return False


# ===== Items with Quantity ===============================

class QuantityItem(Item):
   quantity: int = 0  # o_count

   def __init__(self, quantity: int = 0, **kwargs):
       self.quantity = quantity
       super().__init__(**kwargs)


# ===== Food ==============================================

class Food(Item):
    OKAY_FOOD = 1
    INTERESTING_FOOD = 0

    def __init__(self, which: int = -1, **kwargs):
        if which == -1:
            which = self.OKAY_FOOD
        self.which = which
        super().__init__(name='food', char=':', color=COLOR_BURNTSIENNA, **kwargs)

    def __str__(self) -> str:
        which = 'Okay' if self.which == Food.OKAY_FOOD else 'Interesting'
        return f'Food({self.pos},{which})'

    def __repr__(self) -> str:
        # TODO: does not handle parent
        return f'Food(pos={repr(self.pos)},which={self.which})'

    # ===== Item callbacks ================================

    def use(self, entity) -> bool:
        """Eat it.  You know you want to."""
        # Peculiar logic here: at level creation 'which' has a one in ten of being boring OKAY
        if self.which == self.OKAY_FOOD:
            entity.add_msg('Yum yum!')  # TODO: real messages
        else:
            entity.add_msg('BLECCCH!')  # TODO: 70% chance of +1 exp
        # TODO hunger appeasement
        return True


# ===== Gold ==============================================

class Gold(QuantityItem):
    def __init__(self, **kwargs):
        super().__init__(name='gold', char='*', color=COLOR_YELLOW, **kwargs)

    def __str__(self) -> str:
        return f'Gold({self.pos},{self.quantity})'

    def __repr__(self) -> str:
        # TODO: does not handle parent
        return f'Gold(pos={repr(self.pos)},quantity={self.quantity})'


# ===== TESTING ===========================================

# See test_items.py

# EOF
