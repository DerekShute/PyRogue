"""
    Items
"""

from typing import Tuple
from position import Pos
# TODO: can't import Entity because recursion

# TODO: colors go somewhere
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BURNTSIENNA = (138, 54, 15)  # AKA "brown"

FRUIT_NAME = 'slime-mold'
"""Traditional fruit name.  Settable in the original, but I can't be bothered"""


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
        entity.add_msg(f'Can\'t do that with a {self.name}!')
        return False

    @property
    def description(self) -> str:
        """Inventory description"""
        return self.name


# ===== Items with Quantity ===============================

class QuantityItem(Item):
    quantity: int = 0  # o_count

    def __init__(self, quantity: int = 0, **kwargs):
        self.quantity = quantity
        super().__init__(**kwargs)


# ===== Food ==============================================

class Food(Item):
    """Found food, because that's what one does in a dungeon."""
    # Originally, at 'new_thing': 1:10 of being 'which 1' -> fruit and 9:10 of being rations
    # Rations at eat have a 30% chance of being awful and giving you +1 exp, else being okay.
    #
    # I'm not going to give you the choose_str business for exclamations, and am working out the
    # odds elsewhere
    #
    which: int
    FRUIT = 0
    GOOD_RATION = 1
    BAD_RATION = 2

    def __init__(self, which: int, **kwargs):
        self.which = which
        super().__init__(name='food', char=':', color=COLOR_BURNTSIENNA, **kwargs)

    def __str__(self) -> str:
        if self.which == Food.FRUIT:
            which = 'fruit'
        elif self.which == Food.GOOD_RATION:
            which = 'good-ration'
        else:
            which = 'bad-ration'
        return f'Food({self.pos},{which})'

    def __repr__(self) -> str:
        # TODO: does not handle parent
        return f'Food(pos={repr(self.pos)},which={self.which})'

    # ===== Item callbacks ================================

    def use(self, entity) -> bool:
        """Eat it.  You know you want to."""
        if self.which == self.FRUIT:
            entity.add_msg(f'my, that was a yummy {FRUIT_NAME}')
        elif self.which == self.BAD_RATION:
            entity.add_msg('yuk, this food tastes awful')
            entity.add_exp(1)
        else:
            entity.add_msg('yum, that tasted good')
        entity.add_food()
        return True

    @property
    def description(self) -> str:
        # TODO: pluralization
        if self.which == self.FRUIT:
            return f'a {FRUIT_NAME}'
        return 'a food ration'


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
