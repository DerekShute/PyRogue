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

Basic Stuff

    Items, Monsters, and Player must respond to:
        * pos property
        * set_pos() method
        * name

Map Display / Level

    Same polymorphism for Monsters, Players, and Items.  Support:
        * char -> Tuple[Pos, display-character str, color Tuple[int, int, int]]
        * set_pos
        
    Right now each has a method to add to the level
        * level.add/remove_player
        * level.add/remove_monster
        * level.add/remove_item
