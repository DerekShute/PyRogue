"""
Fundamentals of levels: rooms and corridors

Probably will be consolidated with other modules at some point
"""

from room import Room
from game_map import GameMap
from display import Display
from position import Pos
from entity import Entity
from item import Item
from typing import Dict, Tuple, Iterator, List
from turn_queue import TurnQueue
import tcod


# ===== Service Routines ==================================

def lit_area(player: Entity) -> Tuple[slice, slice]:
    """The section of the map that is guaranteed to be lit by the player"""
    # TODO: blindness, complete darkness
    if player is None:
        return None
    room = player.room
    if room is not None and room.max_pos.x > room.pos.x:  # Not a gone room
        p1 = room.pos
        p2 = room.max_pos  # TODO: gone rooms
    else:
        p1 = player.pos
        p2 = Pos(player.pos.x + 1, player.pos.y + 1)  # Slices are weird
    return slice(p1.x - 1, p2.x + 1), slice(p1.y - 1, p2.y + 1)


def tunnel_between(start: Pos, end: Pos, going_south=bool) -> Iterator[Pos]:
    """Return an S-shaped tunnel between these two points."""
    # TODO: goes insane if less than 3 tiles distance.  Raise an exception?
    # TODO: specify 'midpoint' position, else get an L-bend?
    x1, y1 = start
    x2, y2 = end
    xmid = (x1 + x2) // 2  # TODO: one of these can be random
    ymid = (y1 + y2) // 2

    if going_south:    # vertically then horizontally.
        stop1 = Pos(x1, ymid)
        stop2 = Pos(x2, ymid)
    else:              # horizontally then vertically.
        stop1 = Pos(xmid, y1)
        stop2 = Pos(xmid, y2)

    # Generate the coordinates for this tunnel.

    for x, y in tcod.los.bresenham(start, stop1).tolist():
        yield Pos(x, y)
    for x, y in tcod.los.bresenham(stop1, stop2).tolist():
        yield Pos(x, y)
    for x, y in tcod.los.bresenham(stop2, end).tolist():
        yield Pos(x, y)


# ===== Level of dungeon ==================================

class Level:
    levelno: int = 0
    map: GameMap
    rooms: Dict[int, Room]
    stairs: List[Pos]  # TODO (eventually) "features" ?
    doors: List[Pos]
    items: List[Item]
    monsters: List[Entity]
    player: Entity
    queue: TurnQueue

    def __init__(self, levelno: int, width: int, height: int, display: Display):
        """
        An empty level
        """
        self.levelno = levelno
        self.map = GameMap(width, height, display)
        self.rooms = {}  # So we can insert exactly.  Just easier this way
        self.stairs = []
        self.doors = []
        self.items = []
        self.monsters = []
        self.player = None
        self.queue = TurnQueue()

    def __str__(self):
        s = 'Level : Rooms('
        rs = ''
        for i, r in self.rooms.items():
            rs = rs + f'({i} : {r}),'
        s = s + rs + '),Stairs('
        ss = ''
        for stair in self.stairs:
            ss = ss + f'{stair},'
        s = s + ss + '),Doors('
        ds = ''
        for door in self.doors:
            ds = ds + f'{door},'
        s = s + ds + '),Items('  # Closes Doors(...)
        i_s = ''
        for item in self.items:
            i_s = i_s + f'{item},'
        s = s + i_s + '),Monsters('  # Items(...)

        m_s = ''
        for monster in self.monsters:
            m_s = m_s + f'{monster},'  # TODO: Pos conversion won't work right.  need __repr__?
        s = s + m_s + '),'  # Monsters

        if self.player is not None:
            s = s + f'{self.player},'

        s = s + ')'
        return s

    # ===== Interface =====================================

    def add_room(self, i: int, r: Room):
        self.rooms[i] = r
        self.map.set_tiles(r.shadow(), GameMap.FLOOR)

    def add_stairs(self, pos: Pos):
        self.stairs.append(pos)
        self.map.set_tile(pos, GameMap.STAIRS)

    def add_door(self, pos: Pos):
        self.doors.append(pos)
        self.map.set_tile(pos, GameMap.DOOR)

    def add_passage(self, start_pos: Pos, end_pos: Pos, going_south: bool):
        """
        Create a double-bend passage between two points (which are included)

        Note: needs 3 spaces vertical or horizontal clearance in order to remain sane
        """
        for p in tunnel_between(start_pos, end_pos, going_south):
            self.map.set_tile(p, GameMap.FLOOR)

    def add_item(self, item: Item):
        """Add an item to the level/map"""
        self.items.append(item)
        # TODO: render?

    def remove_item(self, item: Item):
        self.items.remove(item)
        # TODO: render

    def add_monster(self, monster: Entity):
        """Add a monster to the level/map"""
        self.monsters.append(monster)
        # TODO: append monster to TurnQueue

    def remove_monster(self, monster: Entity):
        """Remove monster from the level/map"""
        self.monsters.remove(monster)
        # TODO: remove monster from TurnQueue

    def add_player(self, player: Entity):
        """Add the player to the level/map"""
        self.player = player
        player.attach_level(self)
        self.queue.add(player)

    def remove_player(self):
        """Remove the player from the level/map"""
        self.player.attach_level(None)
        self.player = None

    def can_enter(self, pos: Pos) -> bool:
        if self.map.can_enter(pos) and not any(m.pos == pos for m in self.monsters):
            return True
        return False

    def render(self):
        self.map.render(lit_area(self.player))

        # TODO: tutorial attaches this to GameMap and adds the clause for visibility
        # TODO: ordering - entity, item, tile
        for item in self.items:
            self.map.set_char(*item.char)
        for monster in self.monsters:
            self.map.set_char(*monster.char)
        if self.player is not None:
            self.map.set_char(*self.player.char)

    def items_at(self, pos: Pos) -> List[Item]:
        """A list of items at this location"""
        return [item for item in self.items if item.pos == pos]

    def monsters_at(self, pos: Pos) -> List[Entity]:
        return [monster for monster in self.monsters if monster.pos == pos]

    def is_stairs(self, pos: Pos) -> bool:
        """Is this the stairs?"""
        return any(stair for stair in self.stairs if stair == pos)

    def find_room(self, pos: Pos) -> Room:
        """Is this in a room?"""
        # There is almost certainly a better way
        results = [room for room in self.rooms.values() if room.inside(pos)]  # TODO: not a gone room
        # Assuming non-overlapping rooms
        return None if results == [] else results[0]

    # ===== Timer Run Queue and Activity ==================

    @property
    def now(self):
        return self.queue.now

    def run_queue(self):
        """Run one element from the timer queue"""
        element = self.queue.pop()
        if element is not None:
            # Not keen on this interface, but we'll see
            reschedule = element.perform()
            if reschedule:
                self.queue.add(element)

    def new_room(self, pos: Pos, curr_room: Room) -> Room:
        """Are you in a new room?  Have you left a room?"""
        if curr_room is None or not curr_room.inside(pos):
            # New room
            curr_room = self.find_room(pos)
            if curr_room is not None and not curr_room.found:
                curr_room.found = True
                for monster in [monster for monster in self.monsters if curr_room.inside(monster.pos)]:
                    print(f'Activating {monster.name} at {monster.pos}')
                    # self.queue.add(monster.activate(self.queue.now))  TODO something like that
        return curr_room


# ===== TESTING ===========================================

if __name__ == '__main__':
    import time

    def rectangle(x1: int, y1: int, x2: int, y2: int) -> Tuple[slice, slice]:
        return slice(x1, x2), slice(y1, y2)

    with Display(80, 25, title='unit test Level') as d:
        lvl = Level(1, 80, 25, d)
        lvl.map.lit(rectangle(0, 0, 80, 25))
        lvl.map.explore(rectangle(0, 0, 80, 25))

        lvl.add_room(0, Room(Pos(0, 0), Pos(7, 7)))
        lvl.add_room(1, Room(Pos(1, 12), Pos(5, 5)))
        lvl.add_room(2, Room(Pos(10, 12), Pos(7, 7)))
        lvl.add_room(3, Room(Pos(40, 10), Pos(0, 0)))    # "gone" room should not be drawn
        lvl.add_passage(Pos(3, 7), Pos(4, 11), True)     # 0 to 1
        lvl.add_door(Pos(3, 7))
        lvl.add_door(Pos(4, 11))
        lvl.add_passage(Pos(7, 3), Pos(9, 15), False)    # 0 to 2
        lvl.add_door(Pos(7, 3))
        lvl.add_door(Pos(9, 15))
        lvl.add_passage(Pos(11, 5), Pos(15, 11), True)   # (gone) to 1
        lvl.add_door(Pos(15, 11))
        lvl.add_passage(Pos(11, 5), Pos(20, 5), False)   # (gone) to (gone) straight line
        lvl.add_door(Pos(20, 5))
        lvl.add_stairs(Pos(5, 5))
        # TODO: items
        lvl.render()
        d.present()   # TODO: not sure about this
        time.sleep(5)
        # print(str(lvl))
        assert str(lvl) == 'Level : Rooms(' \
               '(0 : Room @(0,0)-@(7,7)),' \
               '(1 : Room @(1,12)-@(5,5)),' \
               '(2 : Room @(10,12)-@(7,7)),' \
               '(3 : Room @(40,10)-@(0,0)),' \
               '),' \
               'Stairs(@(5,5),),' \
               'Doors(@(3,7),@(4,11),@(7,3),@(9,15),@(15,11),@(20,5),),' \
               'Items(),' \
               'Monsters(),' \
               ')'
    print('*** Tests Passed ***')

# EOF
