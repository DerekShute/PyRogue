"""
    Waving some kind of stick around
"""
# todo import position
# TODO targeting.  Always gets a direction...

# ===== Stick Effects =====================================

def do_nothing(entity) -> bool:
    return False

# ===== Stick Effect Starting Point ========================

STICK_EFFECTS = {
    # cancellation
    # cold
    # drain life
    # fire
    # haste monster
    # invisibility
    # light
    # lightning
    # magic missile
    'nothing': do_nothing,
    # polymorph
    # slow monster
    # teleport away
    # teleport to
}


def stick_effect(name: str, entity) -> bool:  # do_zap
    """Dispatch the stick name to the callback that implements the effect"""
    call = STICK_EFFECTS.get(name)
    if call is None:
        entity.add_msg(f'No idea what a {name} does')
        return
    return call(entity)
    # WONT-DO: If effect is not obvious, opportunity to slap a name on it

# EOF
    