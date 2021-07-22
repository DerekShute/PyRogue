IN PROGRESS

    Wizard Mode
    
        * Text "chat" interface : - "/" enters chat mode
          * InputHandler to add text to thing

BUGS:
    * Still ways to get multiple actions in the player action queue and that means an offset.
    * "Turn off effect" message appears to not be seen very much, probably based on how it is being rendered

BIG TODO:

    Wizard mode / Chat
        * shift-key ('+') needs special decode.  Not sure how to deal with that
        * identify sequence -> subsequent InputHandler
        * wizard mode always gets scorecard

    Curses:
        * Cannot remove equipped item  (dropped item?)

    Hallucination:
        * many user messages have alternate output if you're LSDing.  Some second argument to add_msg?

    Haste / Monster Haste
        * Don't have a good model for this.  Adjusting ACTION_COST causes problems when the user action queue gets empty.
            * Do not reschedule if no action in queue, adding action adds to queue?  This is general rework

    * Push food under consumables?

    Conditions as set (cursed, hasted monsters, etc)
        * Player: confuse monster effect via scroll

    Inventory:
        * Consolidate count of items in listing

    Items and equipment
        * sticks -> targeting

    Monster AI

    Monster special powers

    Potions:
        Detect Magic

    Rings:
        Teleportation
        monster aggrevation
        haste
        sustain hunger
        invisibility
        detect invisibility
        regeneration
        searching

    Scrolls:
        monster confusion -> state, magic mapping, hold monster, sleep, identify potion,
        identify scroll, identify weapon, identify armor, identify ring staff or wand, 
        food detection, teleportation, create monster, remove curse, aggravate monsters

    Traps
    
    Amulet and stairs up

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
    * Maze rooms
    * Treasure rooms

Combat    
    * Projectile rules
    
    * helpless target?  Additional bonus
    
    * Combat turns off healing quiet time

Stats use

    * doctor daemon: pstats.lvl, pstats.hpt max_hp(?)
    * saving throws save_throw use lvl
