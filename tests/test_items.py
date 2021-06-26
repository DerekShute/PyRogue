"""
    Unit test of Items
"""

import unittest
from item import Gold, Food, Item
from position import Pos


# ===== Testing Items =====================================
class TestItem(unittest.TestCase):
    """Test general item behavior"""

    # TODO: test force keyword arguments

    def test_basics(self):
        COLOR_YELLOW = (255, 255, 0)
        i = Item(pos=Pos(3, 4), name='frotz', char='?', color=COLOR_YELLOW)
        assert i.name == 'frotz'
        assert i.pos == Pos(3, 4)
        assert i.char == (Pos(3, 4), ord('?'), COLOR_YELLOW)
        i.set_pos(Pos(1, 1))
        assert i.pos == Pos(1, 1)
        i.set_pos(None)
        assert i.pos == None
        self.assertTrue(True)


# ===== Test Gold =========================================
class TestGold(unittest.TestCase):
    """Test gold"""

    def test_gold(self):
        """Test Elementary stuff"""
        g = Gold(quantity=10)
        assert str(g) == 'Gold(None,10)'
        g = Gold(quantity=20, pos=Pos((20, 20)))
        assert str(g) == 'Gold(@(20,20),20)'
        assert g.name == 'gold'
        assert g.quantity == 20
        assert repr(g) == repr(eval(repr(g)))
        self.assertTrue(True)


# ===== Test Food =========================================

class TestFood(unittest.TestCase):
    """Test food"""

    def test_food(self):
        """Test Elementary stuff"""
        g = Food(which=Food.OKAY_FOOD)
        assert str(g) == 'Food(None,Okay)'
        g = Food(which=Food.INTERESTING_FOOD)
        assert str(g) == 'Food(None,Interesting)'
        g = Food(pos=Pos(20, 20), which=Food.OKAY_FOOD)
        assert str(g) == 'Food(@(20,20),Okay)'
        assert g.name == 'food'
        assert g.quantity == None
        assert repr(g) == repr(eval(repr(g)))
        self.assertTrue(True)

# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
