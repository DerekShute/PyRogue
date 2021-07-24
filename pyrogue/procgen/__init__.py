"""
    Procedural Generation
"""
import random
from typing import List
from item import Item, Food, Equipment, Consumable
from factories import (calc_probability, ITEM_PROB_TEMPLATES, ARMOR_TEMPLATES, WEAPON_TEMPLATES,
                       POTION_TEMPLATES, POTION_RAINBOW, RING_TEMPLATES, RING_STONES,
                       SCROLL_TEMPLATES, SCROLL_SYLLABLES, STICK_TEMPLATES, WOOD_NAMES, METAL_NAMES)


# TODO: randmonster

ITEM_PROBABILITIES: List[int] = calc_probability(ITEM_PROB_TEMPLATES)
"""Initialized weighted probability list"""

ARMOR_PROBABILITIES: List[int] = calc_probability(ARMOR_TEMPLATES)
"""Initialized weighted probablility list"""

WEAPON_PROBABILITIES: List[int] = calc_probability(WEAPON_TEMPLATES)
"""Initialized weighted probability list"""

POTION_PROBABILITIES: List[int] = calc_probability(POTION_TEMPLATES)
"""Initialized weighted probability list"""

POTION_DESCRIPTIONS: List[str] = []
"""Initialized potion colors, scrambled per game"""
# TODO: this totally will not work for save games

RING_PROBABILITIES: List[int] = calc_probability(RING_TEMPLATES)
"""Initialized weighted probability list"""

RING_DESCRIPTIONS: List[str] = []
"""Initialized ring stones (with value add), scrambled per game"""
# TODO: this totally will not work for save games

SCROLL_PROBABILITIES: List[int] = calc_probability(SCROLL_TEMPLATES)
"""Initialized weighted probability list"""

SCROLL_DESCRIPTIONS: List[str] = []
"""Initialized scroll inscriptions, scrambled per game"""
# TODO: this totally will not work for save games

STICK_PROBABILITIES: List[int] = calc_probability(STICK_TEMPLATES)
"""Initialized weighted probability list"""

STICK_DESCRIPTIONS: List[str] = []
"""Initialized wand/staff descriptions, scrambled per game"""
# TODO: This totally will not work for save games

STICK_IS_WAND: List[bool] = []
"""Initialized wand/staff type, scrambled per game"""


# ===== Service Routines ==================================

def plus_value() -> int:
    """+1 -> +3 determination.  Or minus, for cursed objects.  Also good for monkeypatching"""
    # Should probably be weighted
    return random.randint(1, 3)


def new_armor(which: int = None) -> Equipment:
    """Fabricate a random armor"""
    if which is None:
        numlist = random.choices(list(range(0, len(ARMOR_TEMPLATES))), weights=ARMOR_PROBABILITIES, k=1)
        which = numlist[0]
    elif which >= len(ARMOR_TEMPLATES):
        return None
    armor = Equipment.factory(etype=Equipment.ARMOR, template=ARMOR_TEMPLATES[which])
    r = random.randint(0, 99)
    if r < 20:    # cursed
        armor.hplus -= plus_value()  # Minuses always _worsen_
        armor.state.add('cursed')
    elif r < 28:  # 8% magic
        armor.hplus += plus_value()  # Pluses always _improve_
    return armor


def new_food(which: int = None) -> Food:
    """Make some food"""
    if which is None:
        if random.randint(0, 100) < 10:
            which = Food.FRUIT
        elif random.randint(0, 100) > 70:
            which = Food.BAD_RATION
        else:
            which = Food.GOOD_RATION
    return Food(which=which)


def new_potion(which: int = None) -> Consumable:
    """Fabricate a random potion"""
    if which is None:
        numlist = random.choices(list(range(0, len(POTION_TEMPLATES))), weights=POTION_PROBABILITIES, k=1)
        which = numlist[0]
    elif which >= len(POTION_TEMPLATES):
        return None
    return Consumable.factory(
        etype=Consumable.POTION, template=POTION_TEMPLATES[which], desc=POTION_DESCRIPTIONS[which]
        )


def new_ring(which: int = None) -> Equipment:
    """Fabricate a random ring"""
    if which is None:
        numlist = random.choices(list(range(0, len(RING_TEMPLATES))), weights=RING_PROBABILITIES, k=1)
        which = numlist[0]
    elif which >= len(RING_TEMPLATES):
        return None
    ring = Equipment.factory(etype=Equipment.RING, template=RING_TEMPLATES[which], desc=RING_DESCRIPTIONS[which])
    if ring.name in ('add strength', 'protection', 'dexterity', 'increase damage'):
        ring.hplus = plus_value() - 1
        if ring.hplus < 1:
            ring.hplus = -1
            ring.state.add('cursed')
    return ring


def new_scroll(which: int = None) -> Consumable:
    """Fabricate a random scroll"""
    if which is None:
        numlist = random.choices(list(range(0, len(SCROLL_TEMPLATES))), weights=SCROLL_PROBABILITIES, k=1)
        which = numlist[0]
    elif which >= len(SCROLL_TEMPLATES):
        return None
    return Consumable.factory(
        etype=Consumable.SCROLL, template=SCROLL_TEMPLATES[which], desc=SCROLL_DESCRIPTIONS[which]
        )


def new_stick(which: int = None) -> Consumable:
    """Fabricate a random stick"""
    if which is None:
        numlist = random.choices(list(range(0, len(STICK_TEMPLATES))), weights=STICK_PROBABILITIES, k=1)
        which = numlist[0]
    elif which >= len(STICK_TEMPLATES):
        return None
    etype = Consumable.WAND if STICK_IS_WAND[which] else Consumable.STAFF
    stick = Consumable.factory(etype=etype, template=STICK_TEMPLATES[which], desc=STICK_DESCRIPTIONS[which])
    if stick.name == 'light':
        stick.charges = random.randint(10, 19)
    else:
        stick.charges = random.randint(3, 7)
    # TODO: if staff, damage = '2x3' else '1x1' and hurldmg = '1x1'
    stick.known = True
    return stick


def new_weapon(which: int = None) -> Equipment:
    """Fabricate a random weapon"""
    if which is None:
        numlist = random.choices(list(range(0, len(WEAPON_TEMPLATES))), weights=WEAPON_PROBABILITIES, k=1)
        which = numlist[0]
    elif which >= len(WEAPON_TEMPLATES):
        return None
    weapon = Equipment.factory(etype=Equipment.WEAPON, template=WEAPON_TEMPLATES[which])
    r = random.randint(0, 100)
    if r < 10:  # 10% cursed
        weapon.state.add('cursed')
        weapon.hplus -= plus_value()
        # Note not dplus...interesting (though the initial mace is +1/+1, and dplus _is_ taken into consideration)
    elif r < 15:  # 5% bonus
        weapon.hplus += plus_value()
        # Note not dplus
    # else 85% normal
    return weapon


# ===== New Thing =========================================

def new_thing() -> Item:  # new_thing
    """Return a new thing (item)"""

    # Decide what kind of object it will be
    # - If we haven't had food for a while, let it be food
    i = random.randint(0, 20)  # TODO This is baloney
    if i == 0:
        # TODO: putting down food resets 'no_food' count
        return new_food()
    if i == 1:
        return new_weapon()
    if i == 2:
        return new_armor()
    if i == 3:
        return new_potion()
    if i == 4:
        return new_ring()
    if i == 5:
        return new_scroll()
    return new_stick()

# ==== Initialization for a new game ======================

def game_init():
    """Scramble the description strings for the new game"""
    # NOTE: need to hook it into save game
    global POTION_DESCRIPTIONS
    global RING_DESCRIPTIONS
    global SCROLL_DESCRIPTIONS
    global STICK_DESCRIPTIONS
    global STICK_IS_WAND

    POTION_DESCRIPTIONS = list(POTION_RAINBOW)
    random.shuffle(POTION_DESCRIPTIONS)

    RING_DESCRIPTIONS = list(RING_STONES)
    random.shuffle(RING_DESCRIPTIONS)

    wand_descriptions = list(METAL_NAMES)
    random.shuffle(wand_descriptions)
    
    staff_descriptions = list(WOOD_NAMES)
    random.shuffle(staff_descriptions)
    
    SCROLL_DESCRIPTIONS = []
    i = 0
    while i < len(SCROLL_TEMPLATES):
        words = None
        nwords = random.randint(2, 4)
        while nwords > 0:
            word = ''
            nsyl = random.randint(1, 3)
            while nsyl > 0:
                word = word + random.choice(SCROLL_SYLLABLES)
                nsyl -= 1
            words = word if words is None else f'{words} {word}'
            nwords -= 1
        SCROLL_DESCRIPTIONS.append(words)
        i += 1

    STICK_IS_WAND = []
    STICK_DESCRIPTIONS = []
    i = 0
    while i < len(STICK_TEMPLATES):
        STICK_IS_WAND.append(random.choice([True, False]))
        if STICK_IS_WAND[i]:
            STICK_DESCRIPTIONS.append(wand_descriptions[i])
        else:
            STICK_DESCRIPTIONS.append(staff_descriptions[i])
        i += 1
# EOF
