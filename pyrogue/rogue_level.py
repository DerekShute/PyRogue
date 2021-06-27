"""
Create a Rogue-style level
"""

import random
import math
from position import Pos
from room import Room
from level import Level
from monster import Monster
from item import Gold
from display import Display
from typing import Tuple
from player import Player


# ===== Constants =========================================

MAXROOMS = 9  # Magic number due to sqrt
NUMCOLS = 80
NUMLINES = 25
ROOM_DIVISOR = int(math.sqrt(MAXROOMS))
BLOCK_X_SIZE = NUMCOLS // ROOM_DIVISOR  # bsize, used as a vector
BLOCK_Y_SIZE = NUMLINES // ROOM_DIVISOR

MAXROOMNO = MAXROOMS - 1
_ROOMLIST = [i for i in range(MAXROOMS)]
random.shuffle(_ROOMLIST)
"""
Room numbers, which we scramble every level-generation to select disincluded rooms
"""


# ===== Service Routines ==================================

def rand(i1: int, i2: int) -> int:
    """random.randint really wants in increasing order.  Note: rnd(n) -> 0 .. n-1 inclusive"""
    _i1 = min(i1, i2)
    _i2 = max(i1, i2)
    return random.randint(_i1, _i2)


def room_xy(i: int) -> Tuple[int, int]:
    """Room coordinates in the 3x3 grid"""
    return i % ROOM_DIVISOR, i // ROOM_DIVISOR


def adjacent(room1: int, room2: int) -> bool:
    """Are these rooms next to one another?"""
    r1x, r1y = room_xy(room1)
    r2x, r2y = room_xy(room2)
    if abs(r1x - r2x) == 1 and r1y == r2y:
        return True
    if abs(r1y - r2y) == 1 and r1x == r2x:
        return True
    return False


def rectangle(x1: int, y1: int, x2: int, y2: int) -> Tuple[slice, slice]:
    return slice(x1, x2), slice(y1, y2)


def tunnel_south(r1: int, r2: int) -> bool:
    """Is the tunnel going south between these two rooms?"""
    if r1 < r2:
        if r1 + 1 == r2:
            return False
        return True
    if r2 + 1 == r1:
        return False
    return True


def connect_rooms(level: Level, r1: int, r2: int):
    """Hook rooms together taking into account Gone rooms and room number direction"""

    # We go from the lower number room to the higher, so either digging south or east

    if r2 < r1:
        temp = r1
        r1 = r2
        r2 = temp

    r1_gone = False
    r2_gone = False

    if level.rooms[r1].max_x == level.rooms[r1].x:
        start_pos = Pos(level.rooms[r1].pos)
        r1_gone = True
    if level.rooms[r2].max_x == level.rooms[r2].x:
        end_pos = Pos(level.rooms[r2].pos)
        r2_gone = True

    going_south = tunnel_south(r1, r2)
    if going_south:
        if not r1_gone:
            start_pos = Pos(rand(level.rooms[r1].x + 1, level.rooms[r1].max_x - 1),
                            level.rooms[r1].max_y + 1)
        if not r2_gone:
            end_pos = Pos(rand(level.rooms[r2].x + 1, level.rooms[r2].max_x - 1),
                          level.rooms[r2].y - 1)
    else:
        if not r1_gone:
            start_pos = Pos(level.rooms[r1].max_x + 1,
                            rand(level.rooms[r1].y + 1, level.rooms[r1].max_y - 1))
        if not r2_gone:
            end_pos = Pos(level.rooms[r2].x - 1,
                          rand(level.rooms[r2].y + 1, level.rooms[r2].max_y - 1))

    # Gone rooms don't get the dignification of having a door

    level.add_passage(start_pos, end_pos, going_south)
    if not r1_gone:
        level.add_door(start_pos)
    if not r2_gone:
        level.add_door(end_pos)


def randmonster(levelno: int, wander: bool) -> int:
    """
    Pick a monster to show up.  The lower (deeper) the level the meaner the monster.

    Returns the ord of the monster's character ID
    """

    LEVEL_MONS = 'KEBSHIROZLCQANYFTWPXUMVGJD'
    WAND_MONS = 'KEBSH0ROZ0CQA0Y0TWP0UMVGJ0'

    mlist = WAND_MONS if wander else LEVEL_MONS

    while True:
        mno = levelno + rand(-6, 3)  # rnd(10) - 6
        if mno < 0:  # Under the beginning
            mno = rand(0, 4)
        if mno >= len(mlist) - 1:  # Off the end
            mno = rand(21, len(mlist) - 1)  # rnd(5) + 21
        if mlist[mno] != '0':
            return ord(mlist[mno])


# ==== Manufactury ========================================

def room_factory(level: Level, levelno: int, roomno: int, gone: bool = False):  # do_rooms()
    """
    We divide the screen into a 3x3 box and the room number defines
    which box it fits into
    """
    pos: Pos = None  # room position, eventually

    # Find upper left corner of box that this room goes in
    rx, ry = room_xy(roomno)
    top = Pos(rx * BLOCK_X_SIZE, ry * BLOCK_Y_SIZE)  # Nothing goes on this horiz/vert

    # In order to fit a curvy passage, you need at least 3 spaces clearance along the
    # "dig direction".  This all takes into account.

    if gone:
        # The gone rooms hold everything together (as opposed to not placing
        # them): it only connects adjacent rooms and if you remove more than
        # one then something can be isolated in a corner or the map becomes
        # disjoint
        pos = Pos(top.x + rand(1, BLOCK_X_SIZE - 3),
                  top.y + rand(1, BLOCK_Y_SIZE - 3))
        return Room(pos, Pos(0, 0))

    # Set room type

    # TODO: Dark and maze

    # Find a place and size for a random room

    # else not maze...
    # figure out the size first, then work backwards and randomly pick an appropriate
    # position that legally fits
    size = Pos(rand(4, BLOCK_X_SIZE - 3), rand(4, BLOCK_Y_SIZE - 3))
    pos = Pos(top.x + rand(1, BLOCK_X_SIZE - size.x - 2),
              top.y + rand(1, BLOCK_Y_SIZE - size.y - 2))
    r = Room(pos, size)

    # Put the gold in
    # TODO: if not amulet and max_level calc

    gold = None
    if rand(0, 2) == 0:  # I think that rnd(2) is 0..2
        gold = Gold(pos=r.rnd_pos, val=rand(2, 50 + 10 * levelno), level=level)

    # Put the monster in

    if rand(0, 100) < 80 if gold else 25:
        monster = Monster.factory(r.rnd_pos, levelno, randmonster(levelno, False))
        monster.attach_level(level)

    return r


def do_passages(level):
    """Connect rooms with tunnels"""

    connected = [[False for i in range(MAXROOMS)] for j in range(MAXROOMS)]
    # connected[i][j] == True => connection exists from i to j
    ingraph = []

    # starting with one room, connect it to a random adjacent room and
    # then pick a new room to start with.

    r1 = random.choice([x for x in range(len(level.rooms))])
    ingraph.append(r1)

    while len(ingraph) < len(level.rooms):
        # find a room to connect with
        i = 0
        r2 = -1
        candidates = [
            x for x in range(len(level.rooms)) if adjacent(r1, x) if x not in ingraph
            ]
        if candidates == []:
            # if no adjacent rooms are outside the graph, pick a new room
            # to look from
            r1 = random.choice(ingraph)
            continue

        j = 0
        for i in candidates:
            # r2 will be set to the first thing we find, and if others exist
            # then it might be changed to some other success
            j = j + 1
            if r2 == -1:
                r2 = i
            elif random.randint(0, j) == 0:
                r2 = i

        # otherwise, connect new room to the graph, and draw a tunnel to it
        ingraph.append(r2)
        connected[r1][r2] = True
        connected[r2][r1] = True

        connect_rooms(level, r1, r2)

    # "attempt to add passages to the graph a random number of times so
    # that there isn't always just one unique passage through it."

    roomcount = rand(0, 4)
    while roomcount > 0:
        r1 = rand(0, MAXROOMS - 1)
        candidates = [x for x in range(len(level.rooms)) if adjacent(r1, x) if not connected[r1][x]]
        if candidates:
            r2 = random.choice(candidates)
            connect_rooms(level, r1, r2)
            connected[r1][r2] = True
            connected[r2][r1] = True

        roomcount = roomcount - 1


# ===== ROGUE LEVEL =======================================

def RogueLevel(levelno: int, width: int, height: int, display: Display, player: Player) -> Level:
    """
    Factory for Rogue-style levels
    """
    # "dig and populate all the rooms on this level"

    level = Level(levelno, width, height, display)

    # TODO: do_rooms()

    # Pick rooms to disinclude for this level
    random.shuffle(_ROOMLIST)
    limit = random.randint(0, 3)

    # Create the rooms, leaving out 0-3 of them (gone rooms)

    # Draw rooms (was 'do_rooms')

    i = 0
    while i < MAXROOMS:
        room = room_factory(level, levelno, _ROOMLIST[i], i < limit)
        level.add_room(_ROOMLIST[i], room)
        i = i + 1

    # Draw passages

    do_passages(level)

    # TODO: no_food++
    # TODO: put_things()

    # TODO: place the traps --- this is in passages?

    # Place the staircase down

    level.add_stairs(random.choice([x for _, x in level.rooms.items() if x.max_y != x.y]).rnd_pos)

    # pick a starting location

    if player is not None:
        starting_room = random.choice([x for _, x in level.rooms.items() if x.max_y != x.y])
        player.set_pos(starting_room.rnd_pos)
        # TODO: position has to be safe to be.
        level.add_player(player)
        player.room = level.new_room(player.pos, None)

    level.map.lit(rectangle(0, 0, NUMCOLS, NUMLINES))   # TODO wizard mode
    level.map.explore(rectangle(0, 0, NUMCOLS, NUMLINES))  # TODO wizard mode

    return level


# ===== TESTING ===========================================

if __name__ == '__main__':
    import time

    with Display(NUMCOLS, NUMLINES, title='unit test rogue_level') as d:
        p = Player.factory()
        lvl = RogueLevel(1, NUMCOLS, NUMLINES, d, player=p)
        print(str(lvl))
        lvl.map.lit(rectangle(0, 0, 80, 25))   # TODO
        lvl.map.explore(rectangle(0, 0, 80, 25))  # TODO
        lvl.render()
        d.present()
        time.sleep(10)

    print('*** Tests Passed ***')

# EOF
