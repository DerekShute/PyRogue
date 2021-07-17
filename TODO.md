IN PROGRESS

    Consumables
    
        * Potions, potion effects.  Need a better way than some enormous if/elif for effects.
            * Direct effect by name, attribute of some effects class?  That's skeevy
            * from consumables import effects as potion_effect
            
        * Potion types that become known... how to record it?  Against the player itself
            known[desc] = True -> stone, wood, inscription, color.  Is there a collection or set to make this easier?
            Then pickup or inventory resolves it at the item level, or at message time or something.
                description becomes a method and takes 'known' argument instead

        * Push food under consumables?

    Effects over time:
        * Turning off via timer, etc.
        * flag use: convention, adding and removing and testing correctly

BIG TODO:

    Wizard mode game (reveals map, identifies objects)

    Items and equipment
        * rings (new equipment type)
        * scrolls, sticks

    Monster AI

    Monster special powers

Gameplay

    Food effects, hunger,
        * Testing of effects, add to display, fainting, weakness, death -- see stomach()

Items in general

    Equip and un-equip : if replacing, this is technically two actions.  Requeue as such?

    o_count == quantity

    Treasure rooms

    player repr() for inventory

Messages

    * Relocated status line to bottom of display (+1 line)

    * currently assumes map coord == display coord

    * Might be able to replace the display slice, but this is nontrivial

    * TODO: history and display of history

AI
    * subsection and generalization.  Player AI is player input, and is a stack of handlers

SAVE GAMES

    * Potion description strings and so forth: must somehow attach to savegame...
    
monster.py
    AMULETLEVEL goes someplace else

    venus flytrap has odd damage declaration

    Monster
        * should this really be a dataclass?

    Monster.factory()
        * xeroc takes on a disguise
        * pack, chance of having an item
        * behavior change if ring of aggravation
        * destination position if aggressive or greedy

./rogue_level.py:68:1: C901 'connect_rooms' is too complex (11)
1     C901 'connect_rooms' is too complex (11)

rogue_level
    player.Stats is imported but unused (except by eval()

Display / Map / Level
    * Make level a part of GameMap, rather than the reverse
    * Consolidate colors into a set of manifest constants
    * Safe to place player: no monster at that square, maze wall, etc.
    * Render priority

Rogue Level
    * Traps
    * Maze rooms
    * Treasure rooms
    * put_things

Combat
    * Must take weapon / armor / rings / confusion effect / etc. into consideration
    
    * Projectile rules
    
    * helpless target?  Additional bonus
    
    * Combat turns off healing quiet time

Stats use

    * doctor daemon: pstats.lvl, pstats.hpt max_hp(?)
    * stat line: hpt, exp, str, lvl, cur_armor, s_arm
    * check level: exp, lvl, hpt
    * Strength change (chg_str)
    * Monsters: creation, etc., 
    * saving throws save_throw use lvl
