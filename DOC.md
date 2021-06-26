Combat

    Instead of inheritance, polymorphism.  Monsters and Players support certain properties
    and methods:
        * melee_attack() -> level, strength, damage
        * take_damage
        * ac
        * add_hit_msg
        * add_was_hit_msg
        * add_miss_msg
        * add_was_missed_msg
        * death
        * kill
        * xp_value

    (Which may or may not use Stats behind the scenes and which may or may not make sense for someone).
    
    Player.melee_attack() is responsible for figuring out the weapon in use and the effects of rings and other considerations
    
    Likewise Monster.melee_attack()

FOOD

    Weird logic around what it does: 1 in 10 chance of being boring, else (9 in 10) has an additional 70% chance of giving a point of experience due to awfulness.
    would it really be too hard to figure out the whole business ahead of time?

Oh Holy Crap

When you see this in C code:

    switch (no_food > 3 ? 2 : pick_one(things, NUMTHINGS))
    {
	case 0:
	    cur->o_type = POTION;
	    cur->o_which = pick_one(pot_info, MAXPOTIONS);
	when 1:
	    cur->o_type = SCROLL;
	    cur->o_which = pick_one(scr_info, MAXSCROLLS);

(wait...what the Hell is a 'when'?)

#define when		break;case

OH HOLY FRACK

Basic Stuff

    We do have the Entity superclass to both Monster and Player that does the basics

Map Display / Level

    Same polymorphism for Monsters, Players, and Items.  Support:
        * char -> Tuple[Pos, display-character str, color Tuple[int, int, int]]
        * set_pos
        
    Right now each has a method to add to the level
        * level.add/remove_player
        * level.add/remove_monster
        * level.add/remove_item
