"""
    Waving some kind of stick around
"""
from position import Pos


# ===== Stick Effects =====================================

def do_light(entity, pos: Pos, target) -> bool:
    """Light the room"""
    if entity.room:
        entity.room.dark = False
    return True


def do_nothing(entity, pos: Pos, target) -> bool:
    return False

# ===== Stick Effect Starting Point ========================


STICK_EFFECTS = {
    # cancellation
    # cold
    # drain life
    # fire
    # haste monster
    # invisibility
    'light': do_light,
    # lightning
    # magic missile
    'nothing': do_nothing,
    # polymorph
    # slow monster
    # teleport away
    # teleport to
}


def stick_effect(name: str, entity, pos: Pos, target) -> bool:  # do_zap
    """Dispatch the stick name to the callback that implements the effect"""
    call = STICK_EFFECTS.get(name)
    if call is None:
        entity.add_msg(f'No idea what a {name} does')
        print(f'...to a {pos} or {target}')
        return
    return call(entity, pos, target)
    # WONT-DO: If effect is not obvious, opportunity to slap a name on it

# EOF
