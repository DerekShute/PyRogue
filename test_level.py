"""
    Testing the level
"""

import unittest
from level import Level
from position import Pos
from room import Room
from item import Gold
from monster import Monster


# ===== Test Level ========================================

class TestLevel(unittest.TestCase):

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
        gold = Gold(val=10, pos=Pos(5, 5), level=lvl)
        assert lvl.items_at(Pos(5, 5)) == [gold]
        lvl.remove_item(gold)
        assert lvl.items_at(Pos(5, 5)) == []
        gold.set_level(lvl)
        assert lvl.items_at(Pos(5, 5)) == [gold]
        gold.set_level(None)
        assert lvl.items_at(Pos(5, 5)) == []
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
        room = lvl.new_room(Pos(50, 50), None)
        assert room is None
        room = lvl.new_room(Pos(5, 5), None)
        assert room == room1
        assert room.found is True
        assert room2.found is False
        room = lvl.new_room(Pos(25, 25), room)
        assert room == room2

# TODO: activation of monsters


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
