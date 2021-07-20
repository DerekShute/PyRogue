"""
    The tuples of strings to feed into factory constructors
"""
from typing import Dict, List, Tuple, Any

#
# 'worth' : value that gets added to score calculation
# 'prob' : Weighted probability for placing that object during level generation
#

# ===== ITEM PROBABILITIES ================================

ITEM_PROB_TEMPLATES = (
    'name=potion prob=26',
    'name=scroll prob=36',
    'name=food prob=16',
    'name=weapon prob=7',
    'name=armor prob=7',
    'name=ring prob=4',
    'name=stick prob=4',
)
"""Master probabilities-- start here"""


# ===== ARMOR TEMPLATES ===================================

ARMOR_TEMPLATES = (
    'name=leather_armor prob=20 worth=20 value=8',          # AC 8
    'name=ring_mail prob=15 worth=25 value=7',              # AC 7
    'name=studded_leather_armor prob=15 worth=20 value=7',  # AC 7
    'name=scale_mail prob=13 worth=30 value=6',             # AC 6
    'name=chain_mail prob=12 worth=75 value=5',             # AC 5
    'name=splint_mail prob=10 worth=80 value=4',            # AC 4
    'name=banded_mail prob=10 worth=90 value=4',            # AC 4
    'name=plate_mail prob=5 worth=150 value=3',             # AC 3
)


# ===== WEAPON TEMPLATES ==================================

# combines obj_info and init_weaps
# 'dam' - melee damage
# 'hurl' - missile/thrown damage
# 'launch' - launching weapon
# 'flags' - 'many': collective 'missile': missile weapon

WEAPON_TEMPLATES = (
    'name=mace prob=11 worth=8 dam=2x4 hurl=1x3',
    'name=long_sword prob=11 worth=15 dam=3x4 hurl=1x2',
    'name=short_bow prob=12 worth=15 dam=1x1 hurl=1x1',
    'name=arrow prob=12 worth=1 dam=1x1 hurl=2x3 launch=short_bow flags=many_missle',
    'name=dagger prob=8 worth=3 dam=1x6 hurl=1x4 flags=missile',
    'name=two_handed_sword prob=10 worth=75 dam=4x4 hurl=1x2',
    'name=dart prob=12 worth=2 dam=1x1 hurl=1x3 flags=many_missile',
    'name=shuriken prob=12 worth=5 dam=1x2 hurl=2x4 flags=many_missile',
    'name=spear prob=12 worth=5 dam=2x3 hurl=1x6 flags=missile',
)


# ===== POTION TEMPLATES ==================================

POTION_RAINBOW = (
    'amber',
    'aquamarine',
    'black',
    'blue',
    'brown',
    'clear',
    'crimson',
    'cyan',
    'ecru',
    'gold',
    'green',
    'grey',
    'magenta',
    'orange',
    'pink',
    'plaid',
    'purple',
    'red',
    'silver',
    'tan',
    'tangerine',
    'topaz',
    'turquoise',
    'vermilion',
    'violet',
    'white',
    'yellow',
)


POTION_TEMPLATES = (
    'name=confusion prob=7 worth=5',
    'name=hallucination prob=8 worth=5',
    'name=poison prob=8 worth=5',
    'name=gain_strength prob=13 worth=150',
    'name=see_invisible prob=3 worth=100',
    'name=healing prob=13 worth=150',
    'name=monster_detection prob=6 worth=130',
    'name=magic_detection prob=5 worth=105',
    'name=raise_level prob=2 worth=250',
    'name=extra_healing prob=5 worth=200',
    'name=haste_self prob=13 worth=130',
    'name=restore_strength prob=13 worth=130',
    'name=blindness prob=5 worth=5',
    'name=levitation prob=5 worth=75',
)


# ===== RING TEMPLATES ====================================

RING_STONES = (
    'desc=agate worth=25',
    'desc=alexandrite worth=40',
    'desc=amethyst worth=50',
    'desc=carnelian worth=40',
    'desc=diamond worth=300',
    'desc=emerald worth=300',
    'desc=germanium worth=225',
    'desc=granite worth=5',
    'desc=garnet worth=50',
    'desc=jade worth=150',
    'desc=kryptonite worth=300',
    'desc=lapis_lazuli worth=50',
    'desc=moonstone worth=50',
    'desc=obsidian worth=15',
    'desc=onyx worth=60',
    'desc=opal worth=200',
    'desc=pearl worth=220',
    'desc=peridot worth=63',  # That one is weirdly specific
    'desc=ruby worth=350',
    'desc=sapphire worth=285',
    'desc=stibiotantalite worth=200',  # (spelling corrected because of course I had to look it up)
    'desc=tiger_eye worth=50',
    'desc=topaz worth=60',
    'desc=turquoise worth=70',
    'desc=taaffeite worth=300',
    'desc=zircon worth=80',  # worth 80?  really?
)


RING_TEMPLATES = (
    'name=protection prob=9 worth=400',
    'name=add_strength prob=9 worth=400',
    'name=sustain_strength prob=5 worth=280',
    'name=searching prob=10 worth=420',
    'name=see_invisible prob=10 worth=310',
    'name=adornment prob=1 worth=10',
    'name=aggravate_monster prob=10 worth=10 flags=cursed',
    'name=dexterity prob=8 worth=440',
    'name=increase_damage prob=8 worth=400',
    'name=regeneration prob=4 worth=460',
    'name=slow_digestion prob=9 worth=240',
    'name=teleportation prob=5 worth=30 flags=cursed',
    'name=stealth prob=7 worth=470',
    'name=maintain_armor prob=5 worth=380',
)


# ===== Probability calculations and whatnot ==============

def unpack_template(template: str, omit: Tuple[str]) -> Dict[str, Any]:
    """
    Convert from the string descriptor into a dict of the key-value pairs

    Key value pairs will replace underbar with a space

    omit:
        Remove these keys from the resulting dict ('worth' and 'prob' are disinteresting for factory-ing items)
    """
    as_dict = {}
    for x in template.split(' '):
        p = x.partition('=')
        if p[0] not in omit:
            if p[2].isdigit():
                as_dict[p[0]] = int(p[2])
            else:
                as_dict[p[0]] = p[2].replace('_', ' ')  # XXX=yyy format
    return as_dict


def calc_probability(factory: Tuple[str]) -> List[int]:
    """pulls out the 'name' and 'prob' fields and readies it for the weighted probability tuples"""
    probs = []
    for entry in factory:
        dict_of = unpack_template(entry, (''))
        probs.append(dict_of['prob'])
    return probs

# EOF
