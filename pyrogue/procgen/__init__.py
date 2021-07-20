"""
    Procedural Generation
"""
import random
from typing import List
from item import Item, Food, Equipment, Consumable
from factories import (calc_probability, ITEM_PROB_TEMPLATES, ARMOR_TEMPLATES, WEAPON_TEMPLATES,
                       POTION_TEMPLATES, POTION_RAINBOW, RING_TEMPLATES, RING_STONES)


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


# ===== Service Routines ==================================

def plus_value() -> int:
    """+1 -> +3 determination.  Or minus, for cursed objects.  Also good for monkeypatching"""
    # Should probably be weighted
    return random.randint(1, 3)


def new_armor() -> Equipment:
    """Fabricate a random armor"""
    numlist = random.choices(list(range(0, len(ARMOR_TEMPLATES))), weights=ARMOR_PROBABILITIES, k=1)
    armor = Equipment.factory(etype=Equipment.ARMOR, template=ARMOR_TEMPLATES[numlist[0]])
    r = random.randint(0, 99)
    if r < 20:    # cursed
        armor.value += plus_value()  # AD&D -> this worsens, remember?
        armor.flags = f'{armor.flags} cursed'
    elif r < 28:  # 8% magic
        armor.value -= plus_value()  # AD&D -> this improves, remember?
    return armor


def new_food() -> Food:
    if random.randint(0, 100) < 10:
        which = Food.FRUIT
    elif random.randint(0, 100) > 70:
        which = Food.BAD_RATION
    else:
        which = Food.GOOD_RATION
    return Food(which=which)


def new_potion() -> Consumable:
    """Fabricate a random potion"""
    numlist = random.choices(list(range(0, len(POTION_TEMPLATES))), weights=POTION_PROBABILITIES, k=1)
    return Consumable.factory(
        etype=Consumable.POTION, template=POTION_TEMPLATES[numlist[0]], desc=POTION_DESCRIPTIONS[numlist[0]]
        )


def new_ring() -> Equipment:
    """Fabricate a random ring"""
    numlist = random.choices(list(range(0, len(RING_TEMPLATES))), weights=RING_PROBABILITIES, k=1)
    ring = Equipment.factory(
        etype=Equipment.RING, template=RING_TEMPLATES[numlist[0]], desc=RING_DESCRIPTIONS[numlist[0]]
        )
    if ring.name in ('add strength', 'protection', 'dexterity', 'increase damage'):
        ring.hplus = plus_value() - 1
        if ring.hplus < 1:
            ring.hplus = -1
            ring.flags = 'cursed'
    return ring


def new_weapon() -> Equipment:
    """Fabricate a random weapon"""
    numlist = random.choices(list(range(0, len(WEAPON_TEMPLATES))), weights=WEAPON_PROBABILITIES, k=1)
    weapon = Equipment.factory(etype=Equipment.WEAPON, template=WEAPON_TEMPLATES[numlist[0]])
    r = random.randint(0, 100)
    if r < 10:  # 10% cursed
        weapon.flags = f'{weapon.flags} cursed'
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
    return new_ring()


# ==== Initialization for a new game ======================

def game_init():
    """Scramble the description strings for the new game"""
    # NOTE: need to hook it into save game
    global POTION_DESCRIPTIONS
    global RING_DESCRIPTIONS

    POTION_DESCRIPTIONS = list(POTION_RAINBOW)
    random.shuffle(POTION_DESCRIPTIONS)

    RING_DESCRIPTIONS = list(RING_STONES)
    random.shuffle(RING_DESCRIPTIONS)
# EOF
