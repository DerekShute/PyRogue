"""
    Testing the level
"""

import unittest
from level import Level
from position import Pos
from room import Room
from item import Gold


# ===== Test Level ========================================

class TestLevel(unittest.TestCase):

    def test_can_enter(self):
        """Exercise 'can enter position' conditions"""
        lvl = Level(20, 20, None)
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
        lvl = Level(10, 10, None)
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
        self.assertTrue(True)

    def test_stairs_at_location(self):
        """Exercise 'there are stairs here' """
        lvl = Level(10, 10, None)
        lvl.add_room(0, Room(Pos(0, 0), Pos(7, 7)))
        lvl.add_stairs(Pos(5, 5))
        assert lvl.is_stairs(Pos(5, 5))
        assert not lvl.is_stairs(Pos(0, 0))
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
