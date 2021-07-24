"""
    The tuples of strings to feed into factory constructors
"""
from typing import Dict, List, Tuple, Any


# ===== MONSTERS ==========================================

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


# ===== ITEM PROBABILITIES ================================

#
# 'worth' : value that gets added to score calculation
# 'prob' : Weighted probability for placing that object during level generation
#

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


# ===== SCROLL TEMPLATES ==================================

SCROLL_SYLLABLES = (
    "a", "ab", "ag", "aks", "ala", "an", "app", "arg", "arze", "ash",
    "bek", "bie", "bit", "bjor", "blu", "bot", "bu", "byt", "comp",
    "con", "cos", "cre", "dalf", "dan", "den", "do", "e", "eep", "el",
    "eng", "er", "ere", "erk", "esh", "evs", "fa", "fid", "fri", "fu",
    "gan", "gar", "glen", "gop", "gre", "ha", "hyd", "i", "ing", "ip",
    "ish", "it", "ite", "iv", "jo", "kho", "kli", "klis", "la", "lech",
    "mar", "me", "mi", "mic", "mik", "mon", "mung", "mur", "nej",
    "nelg", "nep", "ner", "nes", "nes", "nih", "nin", "o", "od", "ood",
    "org", "orn", "ox", "oxy", "pay", "ple", "plu", "po", "pot",
    "prok", "re", "rea", "rhov", "ri", "ro", "rog", "rok", "rol", "sa",
    "san", "sat", "sef", "seh", "shu", "ski", "sna", "sne", "snik",
    "sno", "so", "sol", "sri", "sta", "sun", "ta", "tab", "tem",
    "ther", "ti", "tox", "trol", "tue", "turs", "u", "ulk", "um", "un",
    "uni", "ur", "val", "viv", "vly", "vom", "wah", "wed", "werg",
    "wex", "whon", "wun", "xo", "y", "yot", "yu", "zant", "zeb", "zim",
    "zok", "zon", "zum",
)


SCROLL_TEMPLATES = (
    'name=monster_confusion prob=7 worth=140',
    'name=magic_mapping prob=4 worth=150',
    'name=hold_monster prob=2 worth=180',
    'name=sleep prob=3 worth=5',
    'name=enchant_armor prob=7 worth=160',
    'name=identify_potion prob=10 worth=80',
    'name=identify_scroll prob=10 worth=80',
    'name=identify_weapon prob=6 worth=80',
    'name=identify_armor prob=7 worth=100',
    'name=identify_ring_wand_or_staff prob=10 worth=115',  # TODO: we'll see if that name sticks
    'name=scare_monster prob=3 worth=200',
    'name=food_detection prob=2 worth=60',
    'name=teleportation prob=5 worth=165',
    'name=enchant_weapon prob=8 worth=150',
    'name=create_monster prob=4 worth=75',
    'name=remove_curse prob=7 worth=105',
    'name=aggravate_monsters prob=3 worth=20',
    'name=protect_armor prob=2 worth=250',
)


# ===== WAND / STAFF ======================================

WOOD_NAMES = (
    'avacado wood', 'balsa', 'bamboo', 'banyan', 'birch',
    'cedar', 'cherry', 'cinnibar', 'cypress',
    'dogwood', 'driftwood', 'ebony', 'elm', 'eucalyptus',
    'fall', 'hemlock', 'holly', 'ironwood', 'kikui wood',
    'mahogany', 'manzanita', 'maple', 'oaken',
    'persimmon wood', 'pecan', 'pine', 'poplar',
    'redwood', 'rosewood', 'spruce', 'teak', 'walnut', 'zebrawood',
)


METAL_NAMES = (
    'aluminum', 'beryllium', 'bone', 'brass', 'bronze',
    'copper', 'electrum', 'gold', 'iron', 'lead', 'magnesium',
    'mercury', 'nickel', 'pewter', 'platinum', 'steel', 'silver',
    'silicon', 'tin', 'titanium', 'tungsten', 'zinc',
)


STICK_TEMPLATES = (
    'name=light prob=12 worth=250',
    'name=invisibility prob=6 worth=5',
    'name=lightning prob=3 worth=330',
    'name=fire prob=3 worth=330',
    'name=cold prob=3 worth=330',
    'name=polymorph prob=15 worth=310',
    'name=magic_missile prob=10 worth=170',
    'name=haste_monster prob=10 worth=5',
    'name=slow_monster prob=11 worth=350',
    'name=drain_life prob=9 worth=300',
    'name=nothing prob=1 worth=5',
    'name=teleport_away prob=6 worth=340',
    'name=teleport_to prob=6 worth=50',
    'name=cancellation prob=5 worth=280',
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
            if p[2][0] == '-' and p[2][1:].isdigit():
                as_dict[p[0]] = - int(p[2][1:])
            elif p[2].isdigit():
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
