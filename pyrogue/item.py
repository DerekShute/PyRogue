"""
    Items
"""

from typing import Tuple, Set
from position import Pos
from factories import unpack_template
from potions import potion_effect
from scrolls import scroll_effect
# TODO: can't import Entity because recursion

# TODO: colors go somewhere
COLOR_BLACK = (0, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_BURNTSIENNA = (138, 54, 15)  # AKA "brown"
COLOR_CHOCOLATE4 = (139, 69, 19)   # AKA "brown"
COLOR_DEEPSKYBLUE = (0, 191, 255)
COLOR_PURPLE = (128, 0, 128)
COLOR_SILVER = (192, 192, 192)

FRUIT_NAME = 'slime-mold'
"""Traditional fruit name.  WONT-DO: Settable in the original, but I can't be bothered"""


# ===== Item ==============================================

class Item:  # union thing
    """
    Superclass for all items
    Thing (originally): Superclass structure for monsters / player / items
    """
    pos: Pos = None
    name: str = '<unknown>'
    _char: int = ord('&')  # No good default
    _color: Tuple[int, int, int] = COLOR_WHITE  # No good default
    parent = None  # Inventory or floor
    desc: str = ''

    def __init__(self, name: str, char: str, color: Tuple[int, int, int], desc: str = None, pos: Pos = None, parent=None):
        self.pos = pos
        self.name = name
        self._char = ord(char)
        self._color = color
        self.parent = parent
        self.desc = desc

    # ===== Display =======================================

    @property
    def char(self) -> Tuple[Pos, int, Tuple[int, int, int]]:
        """Return map display information"""
        # TODO: render priority
        return self.pos, self._char, self._color

    @property
    def magic(self) -> bool:
        """Map display 'detect magic'"""
        return False

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

    # ===== Item callbacks from Entity ====================

    def use(self, entity) -> bool:
        entity.add_msg(f'Can\'t do that with a {self.description(entity.known)}!')
        return False

    def description(self, known: Set[str]) -> str:
        """Words used in inventory and dialog: resolve with 'known' and so forth"""
        return self.name


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
        if self.which == Food.FRUIT:
            kwargs['desc'] = FRUIT_NAME
        else:
            kwargs['desc'] = 'food ration'
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
            entity.add_msg(f'my, that was a yummy {self.desc}')
        elif self.which == self.BAD_RATION:
            entity.add_msg('yuk, this food tastes awful')
            entity.add_exp(1)
        else:
            entity.add_msg('yum, that tasted good')
        entity.add_food()
        return True

    def description(self, known: Set[str]) -> str:
        return self.desc


# ===== Gold ==============================================

class Gold(Item):
    quantity: int = 0

    def __init__(self, quantity: int = 0, **kwargs):
        self.quantity = quantity
        super().__init__(name='gold', char='*', color=COLOR_YELLOW, **kwargs)

    def __str__(self) -> str:
        return f'Gold({self.pos},{self.quantity})'

    def __repr__(self) -> str:
        # TODO: does not handle parent
        return f'Gold(pos={repr(self.pos)},quantity={self.quantity})'


# ===== Equipment =========================================

class Equipment(Item):
    """
    Equippable object (Armor, Weapon, Ring, Shield, etc.)
    """
    etype: int = 0  # ARMOR / WEAPON / etc
    worth: int = 0  # Score calculation at player demise
    dmg: str = None
    hurl: str = None
    launch: str = None
    state: Set[str] = set()
    hplus: int = 0
    dplus: int = 0
    known: bool = False  # TODO: Do you know exactly what it does/is?

    # Types
    ARMOR = 0
    WEAPON = 1
    RING = 2

    def __init__(self, etype: int, value: int = 0, worth: int = 0,
                 dam: str = None, hurl: str = None, launch: str = None, flags: str = '', **kwargs):
        self.etype = etype
        self.value = value
        self.worth = worth
        self.dam = dam
        self.hurl = hurl
        self.launch = launch
        self.state = set(flags.split(' '))
        super().__init__(**kwargs)

    @property
    def magic(self):
        return True if self.etype == Equipment.RING or self.hplus != 0 or self.dplus != 0 else False

    def description(self, known: Set[str]) -> str:
        def describe_ring() -> str:
            # TODO: bonuses
            if self.desc in known:
                return f'{self.desc} ring of {self.name}'
            return f'{self.desc} ring'

        def describe_other() -> str:
            if not self.known:
                return f'{self.name}'
            cursed_str = 'cursed ' if 'cursed' in self.state else ''
            if self.hplus != 0:
                return f'{cursed_str}{self.hplus:+} {self.name}'
            return f'{cursed_str}normal {self.name}'

        if self.etype == Equipment.RING:
            return describe_ring()
        return describe_other()

    @staticmethod
    def factory(etype: int, template: str, desc: str = None) -> 'Equipment':
        """Convert from the readable format"""
        kwargs = unpack_template(template, ('prob'))
        if etype == Equipment.ARMOR:
            kwargs['char'] = ']'
            kwargs['color'] = COLOR_CHOCOLATE4
        elif etype == Equipment.WEAPON:
            kwargs['char'] = ')'
            kwargs['color'] = COLOR_DEEPSKYBLUE
        elif etype == Equipment.RING:
            desc_kwargs = unpack_template(desc, '')
            kwargs['char'] = '='
            kwargs['color'] = COLOR_SILVER
            kwargs['worth'] += desc_kwargs['worth']
            kwargs['desc'] = desc_kwargs['desc']
        return Equipment(etype, **kwargs)


# ===== CONSUMABLES =======================================

class Consumable(Item):
    """
    Consumable items: potions, scrolls, and 'sticks'
    """
    etype: int         # POTION / etc
    worth: int         # score calculation at player demise
    # TODO: charges

    # TYPES
    POTION = 0
    SCROLL = 1

    def __init__(self, etype: int, worth: int, **kwargs):
        self.etype = etype
        self.worth = worth
        super().__init__(**kwargs)

    @property
    def magic(self):
        return True

    def description(self, known: Set[str]):
        if self.etype == Consumable.POTION:
            if self.desc in known:
                return f'potion of {self.name}'
            return f'{self.desc} potion'
        # Scroll
        if self.desc in known:
            return f'scroll of {self.name}'
        return f'scroll titled "{self.desc}"'

    @staticmethod
    def factory(etype: int, template: str, desc: str):
        kwargs = unpack_template(template, ('prob'))
        if etype == Consumable.POTION:
            kwargs['char'] = '!'
            kwargs['color'] = COLOR_PURPLE
        elif etype == Consumable.SCROLL:
            kwargs['char'] = '?'
            kwargs['color'] = COLOR_BLACK
        kwargs['desc'] = desc
        return Consumable(etype, **kwargs)

    def use(self, entity) -> bool:
        """Drink the mystery fluid found in a dungeon, etc.  What could go wrong?"""
        now_known = False
        if self.etype == Consumable.POTION:
            now_known = potion_effect(self.name, entity)
        elif self.etype == Consumable.SCROLL:
            now_known = scroll_effect(self.name, entity)
        if now_known:
            entity.known.add(self.desc)
        return True

# ===== TESTING ===========================================

# See test_items.py

# EOF
