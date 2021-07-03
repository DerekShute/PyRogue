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
    'name=leather_armor prob=20 worth=20 value=8',  # AC 8
    'name=ring_mail prob=15 worth=25 value=7',      # AC 7
    'name=studded_leather_armor prob=15 worth=20 value=7', # AC 7
    'name=scale_mail prob=13 worth=30 value=6',  # AC 6
    'name=chain_mail prob=12 worth=75 value=5',  # AC 5
    'name=splint_mail prob=10 worth=80 value=4',  # AC 4
    'name=banded_mail prob=10 worth=90 value=4',  # AC 4
    'name=plate_mail prob=5 worth=150 value=3',   # AC 3
)

# TODO: - Need three generators here: value calculation at RIP/END, probability for level generation, and the
# factory for items.

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
                as_dict[p[0]] = p[2].replace('_',' ')  # XXX=yyy format
    return as_dict



def calc_probability(factory: Tuple[str]) -> (List[str], List[int]):
    """pulls out the 'name' and 'prob' fields and readies it for the weighted probability tuples"""
    names = []
    probs = []
    for entry in factory:
        dict_of = unpack_template(entry, [])
        names.append(dict_of['name'])
        probs.append(dict_of['prob'])
    return (names, probs)        


# ===== Module Initialization =============================

# TODO: random.choices(names, weights=probs, k=1)

ITEM_PROBABILITIES: Tuple[List[str], List[int]] = calc_probability(ITEM_PROB_TEMPLATES)

ARMOR_PROBABILITIES: Tuple[List[str], List[int]] = calc_probability(ARMOR_TEMPLATES)