"""
    Drinking a potion
"""
import random
# TODO: can't import Entity here

def roll(count: int, sides: int) -> int:
    """XdY die roll"""
    # TODO: goes elsewhere, combines with other things
    total = 0
    while count > 0:
        total = total + random.randint(1, sides)
        count = count - 1
    return total

# ===== Potion Effects ====================================

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

def do_healing(entity):
    """(level)d4 points restored.  If max hit points exceeded, add one to max hit points"""
    entity.add_hp(roll(entity.lvl, 4))
    entity.add_msg('You begin to feel better.')
    # TODO: known
    # TODO: sight() ?

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

# ===== Potion Effect starting point ======================

POTION_EFFECTS = {
    'extra healing' : do_extra_healing,
    'gain strength' : do_gain_strength,
    'healing' : do_healing,
    'poison' : do_poison,
    'raise level' : do_raise_level,
    'restore strength' : do_restore_strength,
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
