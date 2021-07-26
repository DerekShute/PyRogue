"""
    Player inventory dialogs
"""
from menu import Menu
from item import Item, Equipment, Consumable, Food


"""
TODO:
    Consumables and Food consolidate entries by quantity - "4 food rations", etc

    Equipment reports quantity of ammunition

    Menu becomes List of Tuple (<description> <Item of topmost identical thing>)
        Where ordinal 'a'..'z' is figured out by InputHandler display of it (?)
        
    Technically wands and staves can be equipped as weapons

    ...then we can say use item X -> need a directional or targeting specifier
"""

def describe_item(player, item: Item) -> str:
    """Describe item in ten words or less"""
    if item == player.weapon:
        worn_str = ' (wielded)'
    else:
        worn_str = ' (being worn)' if item in (*player.rings, player.armor) else ''
    return f'{item.description(player.known)}{worn_str}'


# ===== Inventory root ====================================

def do_inventory(player, usage: str) -> Menu:
    """Start here for displaying/generating user inventory for situations"""
    inventory = []
    title = 'inventory' if usage == '' else usage

    listing = ord('a')
    for item in player.pack:
        if usage == '':
            inventory.append(describe_item(player, item))
            listing += 1
            continue
        inv = set()
        inv.add('drop')
        if isinstance(item, Equipment):
            inv.add('equip')
        if isinstance(item, Food):
            inv.add('use')
        if isinstance(item, Consumable):
            if item.etype in (Consumable.WAND, Consumable.STAFF):
                inv.add('zap')
            else:
                inv.add('use')
        if usage not in inv:
            listing += 1
            continue
        inventory.append(f'{chr(listing)}: {describe_item(player, item)}')
        listing += 1
    return Menu(title=title, text=inventory)

# EOF
