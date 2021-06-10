position.py
    Pos
        * __repr__ -> eval(repr(x)) == x
        * Cases where we want to represent it so we can factory it, save game pickling (?)
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
        