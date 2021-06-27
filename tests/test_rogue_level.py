"""
    Unit test of Rogue Level generation
"""

import unittest
from unittest.mock import patch
import rogue_level
from level import Level
from player import Player


# ===== Service Routines ==================================

def randint_return_min(*args, **kwargs):
    """If asked to random.randint(x,y), return x"""
    print(f'from {args[0]} to {args[1]}')
    assert args[0] <= args[1]   # Check for stupid mistake
    return args[0]


def randint_return_max(*args, **kwargs):
    """If asked to random.randint(x,y), return y"""
    print(f'from {args[0]} to {args[1]}')
    assert args[0] <= args[1]   # Check for stupid mistake
    return args[1]


# ===== Testing Rogue Level ===============================

class TestBasics(unittest.TestCase):
    """Service routines and whatnot"""

    def test_roomxy(self):
        """Room numbers on 3x3 grid"""
        assert rogue_level.room_xy(0) == (0, 0)
        assert rogue_level.room_xy(1) == (1, 0)
        assert rogue_level.room_xy(2) == (2, 0)
        assert rogue_level.room_xy(3) == (0, 1)
        assert rogue_level.room_xy(4) == (1, 1)
        assert rogue_level.room_xy(8) == (2, 2)
        self.assertTrue(True)

    def test_adjacent(self):
        """Adjacency test of room numbers"""
        assert rogue_level.adjacent(0, 1)
        assert not rogue_level.adjacent(0, 2)
        assert rogue_level.adjacent(1, 2)
        assert rogue_level.adjacent(2, 1)
        assert rogue_level.adjacent(0, 3)
        assert not rogue_level.adjacent(0, 4)
        assert not rogue_level.adjacent(0, 8)
        self.assertTrue(True)


# ===== Testing Random Monsters ===========================

class TestRandmonster(unittest.TestCase):
    """Test random monster selection in rooms"""

    # TODO: test wandering monster and weird '0' clause

    @patch('random.randint')
    def test_min(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        r = chr(rogue_level.randmonster(1, False))
        # print(f'min 1: {r}')
        assert r == 'K'

        r = chr(rogue_level.randmonster(7, False))
        # print(f'min 7: {r}')
        assert r == 'E'

        r = chr(rogue_level.randmonster(26, False))
        # print(f'min 26: {r}')
        assert r == 'U'

        r = chr(rogue_level.randmonster(100, False))
        # print(f'min 100: {r}')
        assert r == 'M'

        self.assertTrue(True)

    @patch('random.randint')
    def test_max(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        r = chr(rogue_level.randmonster(1, False))
        # print(f'max 1: {r}')
        assert r == 'H'

        r = chr(rogue_level.randmonster(7, False))
        # print(f'max 7: {r}')
        assert r == 'C'

        r = chr(rogue_level.randmonster(26, False))
        # print(f'max 26: {r}')
        assert r == 'D'

        r = chr(rogue_level.randmonster(100, False))
        # print(f'max 100: {r}')
        assert r == 'D'

        self.assertTrue(True)


class TestGeneration(unittest.TestCase):
    """Smoke test the whole darn thing"""

    def test_smoke(self):
        """Absolute basics"""
        lvl = rogue_level.RogueLevel(1, 80, 25, None, player=None)
        _ = str(lvl)
        assert lvl
        self.assertTrue(True)

    # TODO: random.choice
    @patch('random.shuffle')  # Room number
    @patch('random.randint')
    def test_mingen(self, mock_randint, random_shuffle):
        assert random_shuffle
        mock_randint.side_effect = randint_return_min
        p = Player()
        lvl = rogue_level.RogueLevel(1, 80, 25, None, player=p)
        assert lvl
        _ = str(lvl)
        self.assertTrue(True)

    # TODO: random.choice
    @patch('random.shuffle')  # Room number
    @patch('random.randint')
    def test_maxgen(self, mock_randint, random_shuffle):
        assert random_shuffle
        mock_randint.side_effect = randint_return_max
        p = Player()
        lvl = rogue_level.RogueLevel(1, 80, 25, None, player=p)
        assert lvl
        _ = str(lvl)
        self.assertTrue(True)

    def test_room_factory(self):
        """Basic room factory splatting"""
        lvl = Level(1, 20, 20, None)
        _ = rogue_level.room_factory(lvl, 1, 0, True)   # Gone room
        _ = rogue_level.room_factory(lvl, 1, 1, False)  # Not a gone room
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
