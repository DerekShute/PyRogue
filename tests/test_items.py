"""
    Unit test of Items
"""

from parameterized import parameterized
import unittest
from item import Gold, Food, Item
from position import Pos
from player import Player

COLOR_YELLOW = (255, 255, 0)

# ===== Testing Items =====================================
class TestItem(unittest.TestCase):
    """Test general item behavior"""

    # TODO: test force keyword arguments

    def test_basics(self):
        i = Item(pos=Pos(3, 4), name='frotz', char='?', color=COLOR_YELLOW)
        assert i.name == 'frotz'
        assert i.pos == Pos(3, 4)
        assert i.xy == (3, 4)
        assert i.char == (Pos(3, 4), ord('?'), COLOR_YELLOW)
        i.set_pos(Pos(1, 1))
        assert i.pos == Pos(1, 1)
        i.set_pos(None)
        assert i.pos == None
        self.assertTrue(True)

    def test_failure_cases(self):
        i = Item(pos=Pos(3, 4), name='frotz', char='?', color=COLOR_YELLOW)
        p = Player.factory()
        i.use(p)
        assert p.curr_msg == 'Can\'t do that with a frotz!'
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

    def test_smoke(self):
        """Test Elementary Stuff"""
        f = Food(pos=Pos(20, 20), which=Food.FRUIT)
        assert str(f) == 'Food(@(20,20),fruit)'
        assert f.name == 'food'
        assert f.quantity == None
        assert repr(f) == repr(eval(repr(f)))
        self.assertTrue(True)

    @parameterized.expand([(Food.FRUIT, 'fruit'),
                           (Food.GOOD_RATION, 'good-ration'),
                           (Food.BAD_RATION, 'bad-ration')])
    def test_food_names(self, input, expected):
        """Test food names"""
        f = Food(which=input)
        assert f.which == input
        assert str(f) == f'Food(None,{expected})'
        assert repr(f) == repr(eval(repr(f)))
        self.assertTrue(True)

    @parameterized.expand([(Food.FRUIT, 'my, that was a yummy slime-mold'),
                           (Food.GOOD_RATION, 'yum, that tasted good'),
                           (Food.BAD_RATION, 'yuk, this food tastes awful')])
    def test_eat(self, input, expected):
        f = Food(which=input)
        p = Player.factory()
        f.use(p)
        assert p.curr_msg == expected
        if input == Food.BAD_RATION:
            assert p.exp == 1
        else:
            assert p.exp == 0
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
