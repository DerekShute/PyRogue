"""
    Wizardry
"""
from procgen import new_weapon, new_armor, new_food, new_scroll, new_potion, new_ring


# ===== Service Routines ==================================
def convert_plus(player, plus: str) -> int:
    negative = False
    if plus[0] == '-':
        negative = True
    value = plus.lstrip('+-')
    if not value.isdigit():
        player.add_msg('Plusval must be positive integer or negative integer')
        return None
    return -int(value) if negative else int(value)


def ready_item(player, item, plus: int = None):
    if item is None:
        player.add_msg('You utterly fail to conjure an impossible item')
        return
    if plus is not None:
        item.hplus = int(plus)
        if item.hplus < 0:
            item.flags = 'cursed'
    item.known = True
    item.set_parent(player)
    player.add_item(item)
    player.add_msg(f'You mystically conjure a new {item.name}')


# ===== Making Things =====================================

def make_armor(player, cmd):
    """Format: armor <#> <plusval, cursed if < 0>"""
    plus = None
    if len(cmd) > 2:
        plus = convert_plus(player, cmd[2])
        if plus is None:
            return
    ready_item(player, new_armor(int(cmd[1])), plus)


def make_food(player, cmd):
    """Format: food <#>"""
    ready_item(player, new_food(int(cmd[1])))


def make_potion(player, cmd):
    """Format: potion <#>"""
    ready_item(player, new_potion(int(cmd[1])))


def make_ring(player, cmd):
    """Format: ring <#> <plusval, cursed if < 0>"""
    plus = None
    if len(cmd) > 2:
        plus = convert_plus(player, cmd[2])
        if plus is None:
            return
    ready_item(player, new_ring(int(cmd[1])), plus)


def make_scroll(player, cmd):
    """Format: scroll <#>"""
    ready_item(player, new_scroll(int(cmd[1])))


def make_weapon(player, cmd):
    """Format: weapon <#> <plusval, cursed if < 0>"""
    plus = None
    if len(cmd) > 2:
        plus = convert_plus(player, cmd[2])
        if plus is None:
            return
    ready_item(player, new_weapon(int(cmd[1])), plus)


# ===== Parse the chat line ===============================

GIVERS = {
    'armor': make_armor,
    'food': make_food,
    'potion': make_potion,
    'ring': make_ring,
    'scroll': make_scroll,
    'weapon': make_weapon,
}


def wizard_request(player, text: str):
    """Turn the text into a request and handle it"""
    cmd = text.split(' ')
    if len(cmd) < 2 or not cmd[1].isdigit():
        player.add_msg('Must give object type and index')
        return

    call = GIVERS.get(cmd[0])
    if call is None:
        player.add_msg(f'Do not know how to make a {cmd[0]}')
        return
    call(player, cmd)

# EOF
