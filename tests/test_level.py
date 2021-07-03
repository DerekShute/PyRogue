"""
    Testing the level
"""

import unittest
from level import Level, lit_area
from position import Pos
from room import Room
from item import Gold
from monster import Monster
from player import Player


# ===== Test Level ========================================

class TestLevel(unittest.TestCase):

    def test_smoke(self):
        """Smoke test"""
        lvl = Level(1, 20, 20, None)
        _ = str(lvl)
        assert lvl.now == 0
        self.assertTrue(True)

    def test_can_enter(self):
        """Exercise 'can enter position' conditions"""
        lvl = Level(1, 20, 20, None)
        lvl.add_room(0, Room(Pos(0, 0), Pos(7, 7)))
        assert lvl.can_enter(Pos(3, 3))  # Inside
        assert lvl.can_enter(Pos(0, 0))
        assert lvl.can_enter(Pos(6, 6))
        assert not lvl.can_enter(Pos(7, 7))    # just outside
        assert not lvl.can_enter(Pos(30, 30))  # Way out there
        assert not lvl.can_enter(Pos(-1, -1))  # Way out there
        self.assertTrue(True)

    def test_item_at_location(self):
        """Exercise 'list of items at position' plus add and remove"""
        lvl = Level(1, 10, 10, None)
        lvl.add_room(0, Room(Pos(0, 0), Pos(7, 7)))
        assert lvl.items_at(Pos(5, 5)) == []
        gold = Gold(quantity=10, pos=Pos(5, 5), parent=lvl)
        lvl.add_item(gold)
        # Gold is present at level at (5, 5)
        assert gold.pos == Pos(5, 5)
        assert gold.parent == lvl
        print(lvl.items)
        assert lvl.items != []
        assert lvl.items_at(Pos(5, 5)) == [gold]
        assert gold.parent == lvl
        # Gold no longer present when removed
        lvl.remove_item(gold)
        gold.set_parent(None)
        assert lvl.items_at(Pos(5, 5)) == []
        assert gold.parent is None
        # Gold back again
        lvl.add_item(gold)
        gold.set_parent(lvl)
        assert lvl.items_at(Pos(5, 5)) == [gold]
        assert gold.parent == lvl
        # Not confused about other positions
        assert lvl.items_at(Pos(3, 3)) == []
        self.assertTrue(True)

    def test_stairs_at_location(self):
        """Exercise 'there are stairs here' """
        lvl = Level(1, 10, 10, None)
        lvl.add_room(0, Room(Pos(0, 0), Pos(7, 7)))
        lvl.add_stairs(Pos(5, 5))
        assert lvl.is_stairs(Pos(5, 5))
        assert not lvl.is_stairs(Pos(0, 0))
        self.assertTrue(True)

    def test_monsters_at_location(self):
        """Exercise 'there is monsters here' """
        lvl = Level(1, 10, 10, None)
        mon = Monster.factory(Pos(3, 3), 1, ord('A'))
        lvl.add_monster(mon)
        assert lvl.monsters_at(Pos(0, 0)) == []
        assert lvl.monsters_at(Pos(3, 3)) == [mon]
        self.assertTrue(True)

    def test_room_at_location(self):
        """Exercise 'what room is right here'"""
        lvl = Level(1, 50, 50, None)
        room1 = Room(Pos(0, 0), Pos(10, 10))
        lvl.add_room(0, room1)
        room2 = Room(Pos(20, 20), Pos(30, 30))
        lvl.add_room(1, room2)
        assert lvl.find_room(Pos(50, 50)) is None
        assert lvl.find_room(Pos(5, 5)) == room1
        self.assertTrue(True)

    def test_room_activation(self):
        """Are you in a new room?  Do you need to wake up the monsters inside?"""
        lvl = Level(1, 50, 50, None)
        room1 = Room(Pos(0, 0), Pos(10, 10))
        assert room1.found is False
        lvl.add_room(0, room1)
        room2 = Room(Pos(20, 20), Pos(30, 30))
        lvl.add_room(1, room2)
        room = lvl.new_room(Pos(25, 25), room2)  # No change
        assert room == room2
        room = lvl.new_room(Pos(50, 50), None)
        assert room is None
        room = lvl.new_room(Pos(5, 5), None)
        assert room == room1
        assert room.found is True
        assert room2.found is False
        room = lvl.new_room(Pos(25, 25), room)
        assert room == room2
        self.assertTrue(True)

    def test_fov_area(self):
        lvl = Level(1, 50, 50, None)
        room1 = Room(Pos(1, 1), Pos(10, 10))
        lvl.add_room(0, room1)
        entity = Player(pos=Pos(4, 4))
        entity.room = room1
        assert lit_area(entity) == (slice(0, 12, None), slice(0, 12, None))
        entity.pos = Pos(20, 25)
        entity.room = None
        assert lit_area(entity) == (slice(19, 22, None), slice(24, 27, None))
        self.assertTrue(True)

# TODO: activation of monsters

# TODO: run queue

# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
