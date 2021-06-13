monster.py
    AMULETLEVEL goes somemplace else

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

Display / Map / Level
    * Consolidate colors into a set of manifest constants
    * Monster should return a color
    * Safe to place player: no monster at that square, maze wall, etc.
    * Render priority

Basic Stuff
    * Everyone responds to .pos , .set_pos(), .name

Thing
    * superclass of Item, theoretically superclass of Monster and Player

Rogue Level
    * Traps
    * Maze rooms
    * Treasure rooms
    * put_things

stats mechanism / combat
    see roll_em for several attacks : specifies thatt (attacker thing) thdef (defender) weapon, and 'hurl'
    
    if no weapon, stats->dmg, dplus = hplus = 0, cp = att->s_dmg
    else:
        hplus = weap->hplus, dplus = weap->dplus
    
        if weap == cur_weapon (held, so must be player, unless monster can make you hit yourself)
    
           if a ADD_DAM ring (on either hand)
               dplus += cur_ring->o_arm  (the ring plus, I think)
           if a ADD_HIT ring (on either hand)
               hplus += cur_ring->o_arm
        cp = weap->damage
        if hurl
            thrown/shot rules, hurldmg, hplus+=cur_weap->hplus, dplus+=cur_weapon->dplus
            else other stuff
    
    helpless target?  Additional bonus
    
    def_arm = def->s_arm
    if defender is player (pstats)
        def_arm += cur_armor value
        ring of protection? def_arm += ring->o_arm
    
    Strikes are noted in damage string: 1x4/1x4/1x8 -> three strikes, two are 1d4, last is 1d8
    for each strike
        convert damage string: DICExSIDES
        if swing (level, armor, hplus + str_plus[att->s_str])
            proll = roll(ndice, nsides)
            damage = dplus + proll + add_dam[att->s_str)
            defender->hpt -= max(0, damage)
            did_hit = TRUE
            
     return did_hit
     
Stats use

    * doctor daemon: pstats.lvl, pstats.hpt max_hp(?)
    * stat line: hpt, exp, str, lvl, cur_armor, s_arm
    * check level: exp, lvl, hpt
    * Strength change (chg_str)
    * Monsters: creation, etc., 
    * saving throws save_throw use lvl
    
    * HEALING EFFECTS