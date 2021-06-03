"""
Fundamentals of levels: rooms and corridors

Probably will be consolidated with other modules at some point
"""

from room import Room
from game_map import GameMap
from display import Display
from position import Pos
from typing import List, Tuple, Iterator
import tcod


# ===== Service Routines ==================================

def tunnel_between(start: Pos, end: Pos, going_south=bool) -> Iterator[Pos]:
    """Return an S-shaped tunnel between these two points."""
    # TODO: goes insane if less than 3 tiles distance.  Raise an exception?
    # TODO: specify 'midpoint' position, else get an L-bend?
    x1, y1 = start
    x2, y2 = end
    xmid = (x1 + x2) // 2  # TODO: one of these can be random
    ymid = (y1 + y2) // 2

    if going_south:    # vertically then horizontally.
        stop1 = Pos((x1, ymid))
        stop2 = Pos((x2, ymid))
    else:              # horizontally then vertically.
        stop1 = Pos((xmid, y1))
        stop2 = Pos((xmid, y2))

    # Generate the coordinates for this tunnel.

    for x, y in tcod.los.bresenham(start, stop1).tolist():
        yield Pos((x, y))
    for x, y in tcod.los.bresenham(stop1, stop2).tolist():
        yield Pos((x, y))
    for x, y in tcod.los.bresenham(stop2, end).tolist():
        yield Pos((x, y))


# ===== Level of dungeon ==================================

class Level:
    map: GameMap
    rooms: List[Room]

    def __init__(self, width: int, height: int, display: Display):
        """
        An empty level
        """
        self.map = GameMap(width, height, display)
        self.rooms = []

    def __str__(self):
        s = 'Level : '
        for r in self.rooms:
            s = s + str(r) + ','
        return s

    # ===== Interface =====================================

    def add_room(self, i: int, r: Room):
        self.rooms.insert(i, r)
        self.map.set_tiles(r.shadow(), GameMap.FLOOR)

    def add_passage(self, start_pos: Pos, end_pos: Pos, going_south: bool):
        """
        Create a double-bend passage between two points (which are included)

        Note: needs 3 spaces vertical or horizontal clearance in order to remain sane
        """
        for p in tunnel_between(start_pos, end_pos, going_south):
            self.map.set_tile(p, GameMap.FLOOR)

    def render(self):
        self.map.render()


# ===== TESTING ===========================================

if __name__ == '__main__':
    import time

    def rectangle(x1: int, y1: int, x2: int, y2: int) -> Tuple[slice, slice]:
        return slice(x1, x2), slice(y1, y2)

    with Display(80, 25, title='unit test Level') as d:
        lvl = Level(80, 25, d)
        lvl.map.lit(rectangle(0, 0, 80, 25))
        lvl.map.explore(rectangle(0, 0, 80, 25))

        lvl.add_room(0, Room(Pos((0, 0)), Pos((7, 7))))
        lvl.add_room(1, Room(Pos((1, 12)), Pos((5, 5))))
        lvl.add_room(2, Room(Pos((10, 12)), Pos((7, 7))))
        lvl.add_room(3, Room(Pos((40, 10)), Pos((0, 0))))    # "gone" room should not be drawn
        lvl.add_passage(Pos((3, 7)), Pos((4, 11)), True)     # 0 to 1
        lvl.map.set_tile(Pos((3, 7)), GameMap.DOOR)
        lvl.map.set_tile(Pos((4, 11)), GameMap.DOOR)
        lvl.add_passage(Pos((7, 3)), Pos((9, 15)), False)    # 0 to 2
        lvl.map.set_tile(Pos((7, 3)), GameMap.DOOR)
        lvl.map.set_tile(Pos((9, 15)), GameMap.DOOR)
        lvl.add_passage(Pos((11, 5)), Pos((15, 11)), True)   # (gone) to 1
        lvl.map.set_tile(Pos((15, 11)), GameMap.DOOR)
        lvl.add_passage(Pos((11, 5)), Pos((20, 5)), False)   # (gone) to (gone) straight line
        lvl.map.set_tile(Pos((20, 5)), GameMap.DOOR)

        lvl.render()
        d.present()   # TODO: not sure about this
        time.sleep(5)
        print(str(lvl))
        assert str(lvl) == 'Level : Room @(0,0)-@(7,7),Room @(1,12)-@(5,5),Room @(10,12)-@(7,7),Room @(40,10)-@(0,0),'

    print('*** Tests Passed ***')

# EOF
