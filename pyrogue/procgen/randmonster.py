"""
    Monster creation
"""
import random
from position import Pos
from entity import Entity
from factories import MONSTER_TEMPLATES, unpack_template
from monster import Monster
from typing import Dict, Any


AMULETLEVEL = 26
"""Per rogue.h : this goes somewhere"""


# ===== Service Routines ===================================

def roll(count: int, sides: int) -> int:
    """XdY, if you know the reference"""
    # TODO: This goes elsewhere
    total = 0
    while count > 0:
        total = total + random.randint(1, sides)
        count = count - 1
    return total


def exp_add(mon: Dict[str, Any]) -> int:
    """Experience to add for this monster's level/hit points"""
    mod = 0
    if mon['lvl'] == 1:
        mod = mon['maxhp'] // 8
    else:
        mod = mon['maxhp'] // 6
    if mon['lvl'] > 9:
        mod = mod * 20
    elif mon['lvl'] > 6:
        mod = mod * 4
    return mod


# ===== NEW MONSTER =======================================

def new_monster(pos: Pos = None, levelno: int = 1, code:int = 0) -> Entity:
    """Cough up a new monster"""
    # TODO: randmonster here?

    lev_add = 0 if levelno < AMULETLEVEL else levelno - AMULETLEVEL
    index = code - ord('A')
    if index > len(MONSTER_TEMPLATES) or index < 0:
        raise ValueError(f'code {code} ({index}) out of range')
    arglist = unpack_template(MONSTER_TEMPLATES[index], (''))
    arglist['armor'] = arglist['armor'] - lev_add  # Long live AD&D AC
    arglist['lvl'] = arglist['lvl'] + lev_add
    arglist['maxhp'] = roll(arglist['lvl'], 8)  # Long live AD&D hit dice
    arglist['exp'] = arglist['exp'] + lev_add * 10 + exp_add(arglist)
    arglist.pop('carry', None)  # TODO: % chance of item in pack
    monster = Monster(pos=pos, mtype=code, **arglist)
    # TODO: if code == ord('X') then this is in disguise=random_thing()
    if levelno > 29:
        monster.state.add('haste')
    # TODO: monster carry is % that it has an item, attached to monster.pack
    return monster

# EOF
