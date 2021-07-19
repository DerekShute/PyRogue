"""
    Drinking a potion
"""
import random
# TODO: can't import Entity here


SEEDURATION = 850


def roll(count: int, sides: int) -> int:
    """XdY die roll"""
    # TODO: goes elsewhere, combines with other things
    total = 0
    while count > 0:
        total = total + random.randint(1, sides)
        count = count - 1
    return total


# ===== Potion Effects ====================================

def do_blindness(entity) -> bool:
    entity.add_effect('blind', SEEDURATION)
    if 'hallucinating' in entity.effects:
        entity.add_msg('Oh, bummer!  Everything is dark!  Help!')
    else:
        entity.add_msg('A cloak of darkness falls around you')
    return True


def do_confusion(entity) -> bool:
    entity.add_effect('confusion', 20)  # HUHDURATION
    if 'hallucinating' in entity.effects:
        entity.add_msg('What a trippy feeling!')
    else:
        entity.add_msg('Wait, what\'s going on here?  Huh?  What?  Who?')
    # TODO: unconfuse at timeout --- callback?
    return True


def do_extra_healing(entity) -> bool:
    """(level)d8 points restored.  If max HP exceeded, add one to max"""
    entity.add_hp(roll(entity.lvl, 8))
    entity.add_msg('You begin to feel much better.')
    # TODO: sight()
    # TODO: come_down()
    return True


def do_gain_strength(entity) -> bool:
    entity.change_str(1)
    entity.add_msg('You feel stronger now.  What bulging muscles!')
    return True


def do_hallucination(entity) -> bool:  # AKA P_LSD
    entity.add_effect('hallucinating', SEEDURATION)
    entity.add_msg('Oh, wow!  Everything seems so cosmic!')
    return True


def do_haste_self(entity) -> bool:
    if 'haste' not in entity.effects:
        entity.add_msg('You feel yourself moving much faster.')
        entity.add_effect('haste', random.randint(0, 4) + 3)
    # TODO: else, 'you faint from exhaustion', deactivating haste and 'no_command' for 0-7 turns
    return True


def do_healing(entity) -> bool:
    """(level)d4 points restored.  If max hit points exceeded, add one to max hit points"""
    entity.add_hp(roll(entity.lvl, 4))
    entity.add_msg('You begin to feel better.')
    # TODO: sight() ?
    return True


def do_levitation(entity) -> bool:
    """Start floating off the ground.  Practicality is questionable."""
    entity.add_effect('levitating', 30)  # HEALTIME
    if 'hallucinating' in entity.effects:
        entity.add_msg('Oh, wow!  You\'re floating in the air!')
    else:
        entity.add_msg('You start to float in the air')
    return True


def do_magic_detection(entity) -> bool:   # P_TFIND
    """Oh my.  Find the magic items."""
    entity.add_effect('detect magic', 2)
    entity.add_msg('You sense the presence of magic on this level.')  # only if something revealed
    return True  # TODO: technically only if items are revealed


def do_monster_detection(entity) -> bool:  # P_MFIND
    """Monster detection"""
    entity.add_effect('monster detection', 20)  # HUHDURATION
    if 'blind' in entity.effects:
        entity.add_msg('You have a strange feeling for a moment, then it passes')
    return False  # Apparently not known, which seems strange.  Depends on if something is detected?


def do_poison(entity) -> bool:
    """Strength decreased by 1-3 points, unless wearing a ring of sustain strength"""
    entity.change_str(-random.randint(1, 3))
    entity.add_msg('You feel very sick now.')
    # TODO: come_down
    return True


def do_raise_level(entity) -> bool:
    """The good stuff.  Raise player level"""
    entity.raise_level()
    entity.add_msg('You suddenly feel much more skillful.')
    return True


def do_restore_strength(entity) -> bool:
    """Restore strength to maximum"""
    entity.restore_strength()
    entity.add_msg('Hey, this tastes great.  It make you feel warm all over!')
    return True  # That's right, it doesn't self-identify


def do_see_invisible(entity) -> bool:
    """See invisible creatures"""
    entity.add_msg('This potion tastes like slime-mold juice.')  # WONT-DO: do not feel like wrangling the fruit string
    entity.add_effect('see invisible', SEEDURATION)
    return False


# ===== Potion Effect starting point ======================

POTION_EFFECTS = {
    'blindness': do_blindness,
    'confusion': do_confusion,
    'extra healing': do_extra_healing,
    'gain strength': do_gain_strength,
    'hallucination': do_hallucination,
    'haste self': do_haste_self,
    'healing': do_healing,
    'levitation': do_levitation,
    'magic detection': do_magic_detection,
    'monster detection': do_monster_detection,
    'poison': do_poison,
    'raise level': do_raise_level,
    'restore strength': do_restore_strength,
    'see invisible': do_see_invisible,
}


def potion_effect(name: str, entity) -> bool:
    """Dispatch the potion name to the callback that implements the effect"""
    call = POTION_EFFECTS.get(name)
    if call is None:
        entity.add_msg(f'No idea what a {name} does')
        return
    return call(entity)
    # WONT-DO: If effect is not obvious, opportunity to slap a name on it

# EOF
