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

def do_blindness(entity):
    entity.add_effect('blind', SEEDURATION)
    if 'hallucinating' in entity.effects:
        entity.add_msg('Oh, bummer!  Everything is dark!  Help!')
    else:
        entity.add_msg('A cloak of darkness falls around you')

def do_confusion(entity):
    entity.add_effect('confusion', 20)  # HUHDURATION
    if 'hallucinating' in entity.effects:
        entity.add_msg('What a trippy feeling!')
    else:
        entity.add_msg('Wait, what\'s going on here?  Huh?  What?  Who?')
    # TODO: known
    # TODO: unconfuse at timeout --- callback?

def do_extra_healing(entity):
    """(level)d8 points restored.  If max HP exceeded, add one to max"""
    entity.add_hp(roll(entity.lvl, 8))
    entity.add_msg('You begin to feel much better.')
    # TODO: known
    # TODO: sight()
    # TODO: come_down()

def do_gain_strength(entity):
    entity.change_str(1)
    entity.add_msg('You feel stronger now.  What bulging muscles!')
    # TODO: known

def do_hallucination(entity):  # AKA P_LSD   
    entity.add_effect('hallucinating', SEEDURATION)
    entity.add_msg('Oh, wow!  Everything seems so cosmic!')
    # TODO: known
    # TODO: come_down() at timeout

def do_haste_self(entity):
    if 'haste' not in entity.effects:
        entity.add_msg('You feel yourself moving much faster.')
        entity.add_effect('haste', random.randint(0, 4) + 3)
    # TODO: else, 'you faint from exhaustion', deactivating haste and 'no_command' for 0-7 turns
    # TODO: known

def do_healing(entity):
    """(level)d4 points restored.  If max hit points exceeded, add one to max hit points"""
    entity.add_hp(roll(entity.lvl, 4))
    entity.add_msg('You begin to feel better.')
    # TODO: known
    # TODO: sight() ?

def do_levitation(entity):
    """Start floating off the ground.  Practicality is questionable."""
    entity.add_effect('levitating', 30)  # HEALTIME
    if 'hallucinating' in entity.effects:
        entity.add_msg('Oh, wow!  You\'re floating in the air!')
    else:
        entity.add_msg('You start to float in the air')

def do_magic_detection(entity):   # P_TFIND
    """Oh my.  Find the magic items."""
    # TODO: not sure how to do this.  As is, it'll be shown in the display update
    entity.add_effect('detect magic', 2)
    entity.add_msg('You sense the presence of magic on this level.')
    # TODO: known
    # TODO: technically, only if items are revealed

def do_monster_detection(entity):  # P_MFIND
    """Monster detection"""
    entity.add_effect('monster detection', 20)  # HUHDURATION
    if 'blind' in entity.effects:
        entity.add_msg('You have a strange feeling for a moment, then it passes')  # Technically a choice here, but who cares
    # Apparently not 'known' after this

def do_poison(entity):
    """Strength decreased by 1-3 points, unless wearing a ring of sustain strength"""
    entity.change_str(-random.randint(1, 3))
    entity.add_msg('You feel very sick now.')
    # TODO: known
    # TODO: come_down

def do_raise_level(entity):
    """The good stuff.  Raise player level"""
    entity.raise_level()
    entity.add_msg('You suddenly feel much more skillful.')
    # TODO: known

def do_restore_strength(entity):
    """Restore strength to maximum"""
    entity.restore_strength()
    entity.add_msg('Hey, this tastes great.  It make you feel warm all over!')
    # TODO: NOT known

def do_see_invisible(entity):
    """See invisible creatures"""
    entity.add_effect('see invisible', SEEDURATION)
    
# ===== Potion Effect starting point ======================

POTION_EFFECTS = {
    'blindness' : do_blindness,
    'confusion' : do_confusion,
    'extra healing' : do_extra_healing,
    'gain strength' : do_gain_strength,
    'hallucination' : do_hallucination,
    'haste self' : do_haste_self,
    'healing' : do_healing,
    'levitation' : do_levitation,
    'magic detection' : do_magic_detection,
    'monster detection' : do_monster_detection,
    'poison' : do_poison,
    'raise level' : do_raise_level,
    'restore strength' : do_restore_strength,
    'see invisible' : do_see_invisible,
}

def potion_effect(name: str, entity):
    """Dispatch the potion name to the callback that implements the effect"""
    call = POTION_EFFECTS.get(name)
    if call is None:
        entity.add_msg(f'No idea what a {name} does')
        return
    call(entity)
    # TODO: unknown? call it something

# EOF
