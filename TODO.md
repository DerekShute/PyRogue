IN PROGRESS

    Targeting
        * Rework of 'inventory' menu generation and contents

BUGS:
    * Wizard chat backspace at empty string
    * Still ways to get multiple actions in the player action queue and that means an offset.
    * "Turn off effect" message appears to not be seen very much, probably based on how it is being rendered
        * Countdown on a single message: remains for 3 moves or something
    * QuantityItem exists

BIG TODO:

    "Bravely bravely bravely run away" suggests my son

    invoke pylint programmatically

    roll() and friends go in one place

    Sticks: light -> room darkness, invisibility, lightning, fire, cold, polymorph, magic missile,
        haste monster, slow monster, drain life, nothing, teleport away, teleport to, cancellation
        * have 'dmg' and 'hurldmg'

    Potions:
        Duration of effects is probably wrong
        Haste: if already hasted, faint
        see invisible

    Items:
        set parent, set level can be consolidated

    Wizard mode / Chat
        * shift-key ('+') needs special decode.  Not sure how to deal with that
        * identify sequence -> subsequent InputHandler
        * wizard mode always gets scorecard
        * summon monster

    Hallucination:
        * many user messages have alternate output if you're LSDing.  Some second argument to add_msg?

    Haste / Monster Haste
        * Don't have a good model for this.  Adjusting ACTION_COST causes problems when the user action queue gets empty.
            * Do not reschedule if no action in queue, adding action adds to queue?  This is general rework

    UI:
        Inventory:
            * Consolidate count of items in listing
        Status screen
        help screen

    Monster AI

    Monster special powers

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

    Rooms:
        darkness
        treasure room
        lair
        maze room

    Traps
    
    Amulet and stairs up

Gameplay

    Food effects, hunger,
        * Testing of effects, add to display, fainting, weakness, death -- see stomach()

Items in general

    Equip and un-equip : if replacing, this is technically two actions.  Requeue as such?

    o_count == quantity

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

./pyrogue/player/__init__.py:182:5: C901 'Player.render_inventory' is too complex (13)
./pyrogue/player/__init__.py:284:5: C901 'Player.equip' is too complex (17)
./pyrogue/procgen/rogue_level.py:75:1: C901 'connect_rooms' is too complex (13)
./pyrogue/game_states/player_input.py:17:5: C901 'PlayerInputHandler.ev_keydown' is too complex (11)

rogue_level
    player.Stats is imported but unused (except by eval()

Display / Map / Level
    * Make level a part of GameMap, rather than the reverse
    * Consolidate colors into a set of manifest constants
    * Safe to place player: no monster at that square, maze wall, etc.
    * Render priority

Combat    
    * Projectile rules
    
    * helpless target?  Additional bonus
    
    * Combat turns off healing quiet time

Stats use

    * doctor daemon: pstats.lvl, pstats.hpt max_hp(?)
    * saving throws save_throw use lvl
