"""
    Reading a scroll
"""
import random
# TODO: can't import Entity here


def do_enchant_armor(entity) -> bool:
    """Enchant armor, remove curse"""
    if entity.armor is not None:
        entity.armor.flags = ''  # TODO: remove 'cursed' specifically
        entity.armor.value -= 1  # Note AD&D rules
        entity.add_msg('Your armor glows silver for a moment')  # WONT-DO: other colors pick_color
    return False  # Really, not set known


def do_enchant_weapon(entity) -> bool:
    """Enchant weapon hit _or_ damage, and remove curses"""
    if entity.weapon is None:
        entity.add_msg('You feel a strange sense of loss.')
        return False
    entity.weapons.flags = ''  # TODO: remove 'cursed' specifically
    if random.randint(0, 1) == 0:
        entity.weapon.hplus += 1
    else:
        entity.weapon.dplus += 1
    entity.add_msg('Your {entity.weapon.description(entity.known)} glows blue for a moment')  # WONT-DO pick_color
    return False  # Really, not set known


def do_protect_armor(entity) -> bool:
    """Prevent armor from taking damage"""
    if entity.armor is None:
        entity.add_msg('You feel a strange sense of loss.')
        return False
    entity.add_msg('Your amor is covered by a shimmering gold shield.')  # WONT-DO pick_color
    entity.armor.flags = 'protected'  # TODO: real flags
    return False


def do_remove_curse(entity) -> bool:
    """Remove curses from all equipped items"""
    if entity.armor is not None:
        entity.armor.flags = ''  # TODO: real flags
    if entity.weapon is not None:
        entity.weapon.flags = ''  # TODO: real flags
    for ring in entity.rings:
        ring.flags = ''  # TODO: real flags
    entity.add_msg('You feel as if somebody is watching over you')  # TODO: choose_str
    return False


def do_scare_monster(entity) -> bool:
    """Not actually how you use it!"""
    entity.add_msg('You hear maniacal laughter in the distance!')
    return False


# ===== Scroll Effect starting point ======================

SCROLL_EFFECTS = {
    # TODO: aggravate monsters
    # TODO: create monster
    'enchant armor': do_enchant_armor,
    'enchant weapon': do_enchant_weapon,
    # TODO: food detection
    # TODO: hold monster
    # TODO: identify potion
    # TODO: identify scroll
    # TODO: identify weapon
    # TODO: identify armor
    # TODO: identify ring staff or wand
    # TODO: magic mapping
    # TODO: monster confusion
    'protect armor': do_protect_armor,
    'remove curse': do_remove_curse,
    'scare monster': do_scare_monster,
    # TODO: sleep
    # TODO: teleportation
}


def scroll_effect(name: str, entity) -> bool:
    """Dispatch the scroll name to the callback that implements the effect"""
    call = SCROLL_EFFECTS.get(name)
    if call is None:
        entity.add_msg(f'No idea what a {name} does')
        return
    return call(entity)
    # WONT-DO: If effect is not obvious, opportunity to slap a name on it

# EOF
