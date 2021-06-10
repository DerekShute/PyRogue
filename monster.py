"""
    Monsters, monsters
"""

import random
from dataclasses import dataclass
from typing import Dict, Any
from position import Pos


AMULETLEVEL = 26
"""Per rogue.h : this goes somewhere"""

MONSTER_TEMPLATES = (
    'name=aquator flags=mean exp=20 lvl=5 armor=2 dmg=0x0/0x0',
    'name=bat flags=fly exp=1 lvl=1 armor=2 dmg=1x2',
    'name=centaur carry=15 exp=17 lvl=4 armor=4 dmg=1x2/1x5/1x5',
    'name=dragon carry=100 flags=mean exp=5000 lvl=10 armor=-1 dmg=1x8/1x8/3x10',
    'name=emu flags=mean exp=2 lvl=1 armor=7 dmg=1x2',
    'name=venus_flytrap flags=mean exp=80 lvl=8 armor=3 dmg=%%%x0',  # TODO xstr in comment?
    'name=griffin carry=20 flags=mean_fly_regenerate exp=2000 lvl=13 armor=2 dmg=4x3/3x5',
    'name=hobgoblin flags=mean exp=3 lvl=1 armor=1 dmg=1x8',
    'name=ice_monster exp=5 lvl=1 armor=8 dmg=0x0',
    'name=jabberwock carry=70 exp=3000 lvl=15 armor=6 dmg=2x12/2x4',
    'name=kestrel flags=mean_fly exp=1 lvl=1 armor=7 dmg=1x4',
    'name=leprechaun exp=10 lvl=3 armor=8 dmg=1x1',
    'name=medusa carry=40 flags=mean exp=200 lvl=8 armor=2 dmg=3x4/3x4/2x5',
    'name=nymph carry=100 exp=37 lvl=3 armor=9 dmg=0x0',
    'name=orc carry=15 flags=greedy exp=5 lvl=1 armor=6 dmg=1x8',
    'name=phantom flags=invis exp=120 lvl=8 armor=3 dmg=4x4',
    'name=quagga flags=mean exp=15 lvl=3 armor=3 dmg=1x5/1x5',
    'name=rattlesnake flags=mean exp=9 lvl=2 armor=3 dmg=1x6',
    'name=snake flags=mean exp=2 lvl=1 armor=5 dmg=1x3',
    'name=troll carry=50 flags=regenerate_mean exp=120 lvl=6 armor=4 dmg=1x8/1x8/2x6',
    'name=black_unicorn flags=mean exp=190 lvl=7 armor=-2 dmg=1x9/1x9/2x9',
    'name=vampire carry=20 flags=regenerate_mean exp=350 lvl=8 armor=1 dmg=1x10',
    'name=wraith exp=55 lvl=5 armor=4 dmg=1x6',
    'name=xeroc carry=30 exp=100 lvl=7 armor=7 dmg=4x4',
    'name=yeti carry=30 exp=50 lvl=4 armor=6 dmg=1x6/1x6',
    'name=zombie flags=mean exp=6 lvl=2 armor=8 dmg=1x8',
)


# ===== Service Routines ===================================

def roll(count: int, sides: int) -> int:
    """XdY, if you know the reference"""
    # TODO: This goes elsewhere
    total = 0
    while count > 0:
        total = total + random.randint(1, sides)
        count = count - 1
    return total


def unpack(template: str) -> Dict[str, str]:
    """
    Convert from the string descriptor into a list of values and
    a dict of key-value pairs.

    Caller then ships the resulting tuple as *args, **kwargs to a factory

    Key value pairs will replace underbar with a space
    Returns:
        args (list of strings)
        kwargs (dict of strings)
    """
    as_dict = {}
    for x in template.split(' '):
        p = x.partition('=')
        if p[2].isdigit():
            as_dict[p[0]] = int(p[2])
        elif p[2][0] == '-' and p[2][1:].isdigit():
            as_dict[p[0]] = 0 - int(p[2][1:])
        else:
            as_dict[p[0]] = p[2].replace('_', ' ')  # XXX=yyy format
    return as_dict


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


# ===== Monster ===========================================

@dataclass
class Monster:  # struct monster
    """
    The fundamentals of 'monster'
    """
    pos: Pos = None
    name: str = '<Unknown Monster>'
    carry: int = 0
    flags: str = ''
    exp: int = 0
    lvl: int = 0
    armor: int = 0
    hpt: int = 0       # Hit points, subject to change
    maxhp: int = 0     # Max hit points
    dmg: str = ''
    mtype: int = 0
    disguise: int = 0  # For xeroc in disguise
    dest: Pos = None   # AI: where it is going.  Player location, room gold (see room->r_gold)
    # pack: Item = None   # What the monster is holding and drops
    # TODO: t_room = room it is in (why?)
    # t_turn = TRUE
    # if player is wearing ring of aggrevation runto(cp)
    #

    @property
    def char(self) -> str:
        return self.disguise if self.disguise != 0 else chr(self.mtype)

    # ===== Interface =====================================

    @staticmethod
    def factory(pos: Pos, levelno: int, code: int):
        """Convert the given MONSTER_TEMPLATES entry into a Monster"""
        lev_add = 0 if levelno < AMULETLEVEL else levelno - AMULETLEVEL

        index = code - ord('A')
        if index > len(MONSTER_TEMPLATES) or index < 0:
            raise ValueError(f'code {code} ({index}) out of range')
        kwargs = unpack(MONSTER_TEMPLATES[index])
        # TODO: if code == ord('X') then this is in disguise=random_thing()
        # TODO: monster carry is % that it has an item, attached to monster.pack

        kwargs['armor'] = kwargs['armor'] - lev_add  # Long live AD&D AC
        kwargs['lvl'] = kwargs['lvl'] + lev_add
        kwargs['maxhp'] = roll(kwargs['lvl'], 8)  # Long live AD&D hit dice
        kwargs['hpt'] = kwargs['maxhp']
        kwargs['exp'] = kwargs['exp'] + lev_add * 10 + exp_add(kwargs)

        if levelno > 29:
            kwargs['flags'] = kwargs['flags'] + ' haste'
        return Monster(pos=pos, mtype=code, **kwargs)


# ===== Unit Testing ======================================

# is in test_monster.py, elsewhere
