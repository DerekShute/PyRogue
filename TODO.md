Test directory

try this

in test/test_whatnot.py

import sys
sys.path.insert(0, './peer_directory/')
(imports)

empty __init__.py

Messages

    * Relocated status line to bottom of display (+1 line)

    * currently assumes map coord == display coord

    * Might be able to replace the display slice, but this is nontrivial

    * TODO: history and display of history

    * TODO: Multiline and --more--

Main state machine -> Main menu, gameplay, menus, endgame

    * Need a generalization of InputHandler distinguishing player game input versus menu input
        * Then can create MainMenu and submenus

AI
    * subsection and generalization.  Player AI is player input, and is a stack of handlers

    * Then monster actions

Engine

    * Everything hangs off of Engine
    
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

Thing
    * superclass of Item, theoretically superclass of Monster and Player

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
    
    * HEALING EFFECTS