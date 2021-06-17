"""
    Let's see if this all hangs together
"""
import random
from typing import Tuple
from display import Display
from player import Player
from gameloop import MainGameloop
from rogue_level import RogueLevel

NUMCOLS = 80
NUMLINES = 25


def main():

    def rectangle(x1: int, y1: int, x2: int, y2: int) -> Tuple[slice, slice]:
        return slice(x1, x2), slice(y1, y2)

    random.seed()

    with Display(NUMCOLS, NUMLINES, title='PyRogue') as d:
        p = Player.factory()
        lvl = RogueLevel(1, NUMCOLS, NUMLINES, d, player=p)
        lvl.map.lit(rectangle(0, 0, NUMCOLS, NUMLINES - 1))   # TODO
        lvl.map.explore(rectangle(0, 0, NUMCOLS, NUMLINES - 1))  # TODO
        loop = MainGameloop(level=lvl, player=p, display=d)
        while True:
            loop = loop.run()
            if loop is None:
                break


# ===== NOT TESTING =======================================

if __name__ == '__main__':
    main()

# EOF
