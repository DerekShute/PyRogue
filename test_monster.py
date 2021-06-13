"""
    Unit test of monster generation
"""

import unittest
from unittest.mock import patch
from monster import Monster
from position import Pos


# ===== Service Routines ==================================

def randint_return_min(*args, **kwargs):
    """If asked to random.randint(x,y), return x"""
    # print(f'from {args[0]} to {args[1]}')
    assert args[0] < args[1]   # Check for stupid mistake
    return args[0]


# ===== TestMonster =======================================

class TestMonster(unittest.TestCase):
    """Test random monster factory (less cool than it sounds)"""

    @patch('random.randint')
    def test(self, mock_randint):
        """Smoke Test"""
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 1, ord('A'))
        # print(str(mon))
        assert str(mon) == 'Monster(aquator:@(0,0),HP=5/5,AC=2,dmg=\'0x0/0x0\',flags=\'mean\')'
        # print(repr(mon))
        assert mon == eval(repr(mon))
        assert mon.name == 'aquator'
        self.assertTrue(True)

    @patch('random.randint')
    def test_lowest(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 1, ord('A'))
        # print(mon)
        assert repr(mon) == 'Monster(pos=None, name=\'aquator\', carry=0, ' \
               'flags=\'mean\', exp=20, lvl=5, armor=2, hpt=5, maxhp=5, ' \
               'dmg=\'0x0/0x0\', mtype=65, disguise=0, dest=None)'
        self.assertTrue(True)

    @patch('random.randint')
    def test_negative_armor(self, mock_randint):
        """Black unicorn armor is negative.  Did parse do that right?"""
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 1, ord('U'))
        # print(mon)
        assert mon.armor == -2
        self.assertTrue(True)

    @patch('random.randint')
    def test_flags(self, mock_randint):
        """Griffin has many flags"""
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 1, ord('G'))
        # print(mon)
        assert mon.flags == 'mean fly regenerate'
        self.assertTrue(True)

    def test_oob_high(self):
        """Out of bounds monster index"""
        try:
            _ = Monster.factory(None, 1, 100)
            assert False
        except ValueError:
            pass
        self.assertTrue(True)

    def test_oob_low(self):
        """Out of bounds low"""
        try:
            _ = Monster.factory(None, 1, ord('A') - 1)
            assert False
        except ValueError:
            pass
        self.assertTrue(True)

    @patch('random.randint')
    def test_leveladd(self, mock_randint):
        """At high dungeon levels, additional benefits (to be a monster)"""
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 27, ord('A'))
        # print(mon)
        assert mon.lvl == 6 and mon.armor == 1 and mon.hpt == 6 and mon.maxhp == 6
        self.assertTrue(True)

    @patch('random.randint')
    def test_haste(self, mock_randint):
        """At dungeon level > 29, monsters get hasted"""
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 31, ord('A'))
        # print(mon)
        assert mon.flags == 'mean haste'
        self.assertTrue(True)

    # Mapping, leveling, Display

    def test_pos(self):
        """Test positioning and set-positioning"""
        mon = Monster.factory(Pos(10, 10), 1, ord('G'))
        assert mon.pos == Pos(10, 10)
        mon.set_pos(Pos(20, 20))
        assert mon.pos == Pos(20, 20)
        self.assertTrue(True)

    def test_char(self):
        """Test map display"""
        mon = Monster.factory(Pos(10, 10), 1, ord('G'))
        pos, char, color = mon.char
        assert pos == Pos(10, 10)
        assert char == 'G'
        assert color == (63, 127, 63)
        self.assertTrue(True)

# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
