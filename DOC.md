Combat

    Instead of inheritance, polymorphism.  Monsters and Players support certain properties
    and methods:
        * melee_dmg()
        * melee_dmg_adj
        * melee_hit_adj
        * ac

    (Which may or may not use Stats behind the scenes).
    
    Player.melee_dmg() is responsible for figuring out the weapon in use and the effects of rings and other considerations
    
    Likewise Monster.melee_dmg()

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
        * level.add_player
        * level.add_monster
        * level.add_item
