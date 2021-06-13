"""
    Testing the level
"""

import unittest
from level import Level
from position import Pos
from room import Room


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


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
