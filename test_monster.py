"""
    Unit test of monster generation
"""

import unittest
from unittest.mock import patch
from monster import Monster


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
    def test_lowest(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        mon = Monster.factory(None, 1, ord('A'))
        # print(mon)
        assert str(mon) == 'Monster(pos=None, name=\'aquator\', carry=0, ' \
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


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
