"""
    Unit test of monster generation
"""

import unittest
from unittest.mock import patch
from procgen.randmonster import new_monster
from position import Pos
from level import Level


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
        mon = new_monster(Pos(3, 2), 1, ord('A'))
        # print(str(mon))
        assert str(mon) == 'Monster(aquator:@(3,2),HP=5/5,AC=2,dmg=\'0x0/0x0\',state={\'mean\'})'
        assert mon.name == 'aquator'
        assert mon.pos == Pos(3, 2)
        pos, mtype, color = mon.char
        assert pos == Pos(3, 2)
        assert mtype == ord('A')
        assert color == (63, 127, 63)
        # TODO : representation sufficient that eval(repr(mon)) == mon
        self.assertTrue(True)

    @patch('random.randint')
    def test_lowest(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        mon = new_monster(None, 1, ord('A'))
        # print(mon)
        assert str(mon) == 'Monster(aquator:@(0,0),HP=5/5,AC=2,dmg=\'0x0/0x0\',state={\'mean\'})'
        self.assertTrue(True)

    @patch('random.randint')
    def test_negative_armor(self, mock_randint):
        """Black unicorn armor is negative.  Did parse do that right?"""
        mock_randint.side_effect = randint_return_min
        mon = new_monster(None, 1, ord('U'))
        # print(mon)
        assert mon.armor == -2
        self.assertTrue(True)

    @patch('random.randint')
    def test_flags(self, mock_randint):
        """Griffin has many flags"""
        mock_randint.side_effect = randint_return_min
        mon = new_monster(None, 1, ord('G'))
        # print(mon)
        assert mon.state == set(('mean', 'fly', 'regenerate'))
        self.assertTrue(True)

    def test_oob_high(self):
        """Out of bounds monster index"""
        try:
            _ = new_monster(None, 1, 100)
            assert False
        except ValueError:
            pass
        self.assertTrue(True)

    def test_oob_low(self):
        """Out of bounds low"""
        try:
            _ = new_monster(None, 1, ord('A') - 1)
            assert False
        except ValueError:
            pass
        self.assertTrue(True)

    @patch('random.randint')
    def test_leveladd(self, mock_randint):
        """At high dungeon levels, additional benefits (to be a monster)"""
        mock_randint.side_effect = randint_return_min
        mon = new_monster(None, 27, ord('A'))
        # print(mon)
        assert mon.lvl == 6 and mon.armor == 1 and mon.hpt == 6 and mon.maxhp == 6
        self.assertTrue(True)

    @patch('random.randint')
    def test_haste(self, mock_randint):
        """At dungeon level > 29, monsters get hasted"""
        mock_randint.side_effect = randint_return_min
        mon = new_monster(None, 31, ord('A'))
        # print(mon)
        assert mon.state == set(('mean', 'haste'))
        self.assertTrue(True)


class TestMonsterMapLevel(unittest.TestCase):
    """Monster on maps"""

    def test_pos(self):
        """Test positioning and set-positioning"""
        mon = new_monster(Pos(10, 10), 1, ord('G'))
        assert mon.pos == Pos(10, 10)
        mon.set_pos(Pos(20, 20))
        assert mon.pos == Pos(20, 20)
        self.assertTrue(True)

    def test_char(self):
        """Test map display"""
        mon = new_monster(Pos(10, 10), 1, ord('G'))
        pos, char, color = mon.char
        assert pos == Pos(10, 10)
        assert char == ord('G')
        assert color == (63, 127, 63)
        self.assertTrue(True)

    def test_level(self):
        """Monster attachment to level"""
        mon = new_monster(Pos(10, 10), 1, ord('G'))
        lvl = Level(1, 80, 25, None)
        mon.attach_level(lvl)
        assert mon.level == lvl  # Test point in neighborhood
        assert lvl.monsters_at(Pos(10, 10)) == [mon]
        mon.detach_level()
        assert mon.level is None
        assert lvl.monsters_at(Pos(10, 10)) == []
        self.assertTrue(True)


# ===== Combat Interface ==================================

class TestMonsterCombat(unittest.TestCase):
    """Test monster combat"""

    @patch('random.randint')
    def test_xp_value(self, mock_randint):
        """Test xp_value returned for killing the darn thing"""
        mock_randint.side_effect = randint_return_min
        mon = new_monster(Pos(10, 10), 1, ord('A'))
        assert mon.xp_value == 20  # 20 in listing plus zero for 5 HP
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
