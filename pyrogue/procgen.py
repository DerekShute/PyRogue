"""
    Procedural Generation
"""
import random
from typing import List
from item import Item, Food, Equipment
from factories import calc_probability, ITEM_PROB_TEMPLATES, ARMOR_TEMPLATES


# TODO: randmonster

ITEM_PROBABILITIES: List[int] = calc_probability(ITEM_PROB_TEMPLATES)
"""Initialized weighted probability list"""

ARMOR_PROBABILITIES: List[int] = calc_probability(ARMOR_TEMPLATES)
"""Initialized weighted probablility list"""


# ===== Service Routines ==================================

def new_food() -> Food:
    if random.randint(0, 100) < 10:
        which = Food.FRUIT
    elif random.randint(0, 100) > 70:
        which = Food.BAD_RATION
    else:
        which = Food.GOOD_RATION
    return Food(which=which)


def new_armor() -> Equipment:
    """Fabricate a random armor"""
    numlist = random.choices(list(range(0, len(ARMOR_TEMPLATES))), weights=ARMOR_PROBABILITIES, k=1)
    return Equipment.factory(etype=Equipment.ARMOR, template=ARMOR_TEMPLATES[numlist[0]])


# ===== New Thing =========================================

def new_thing() -> Item:  # new_thing
    """Return a new thing (item)"""

    # Decide what kind of object it will be
    # - If we haven't had food for a while, let it be food
    if random.randint(0, 10) < 3:  # TODO this is baloney
        # TODO: putting down food resets 'no_food' count
        return new_food()
    return new_armor()

# EOF
