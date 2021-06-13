"""
    Test of things in player module
"""

import unittest
from unittest.mock import patch
from player import roll, Player, Stats
from position import Pos


# ===== Service Routines ==================================

def randint_return_min(*args, **kwargs):
    """If asked to random.randint(x,y), return x"""
    # print(f'from {args[0]} to {args[1]}')
    assert args[0] < args[1]   # Check for stupid mistake
    return args[0]


def randint_return_max(*args, **kwargs):
    """If asked to random.randint(x,y), return y"""
    # print(f'from {args[0]} to {args[1]}')
    assert args[0] < args[1]   # Check for stupid mistake
    return args[1]


# ===== Tests =============================================

class TestPlayer(unittest.TestCase):
    """Test damage ('AxB') die rolls"""

    def test(self):
        """Smoke test"""
        p = Player.factory(pos=(10, 10))
        # print(str(p))
        assert str(p) == 'Player(@(10,10),Stats(Str=16,XP=0(0),AC=10,Dmg=\'1x4\',HP=12/12))'
        # print(repr(p))
        assert repr(p) == 'Player(pos=(10, 10),stats=Stats(stren=16, arm=10, dmg=\'1x4\', ' \
               'maxhp=12, hpt=12, exp=0, level=0), food_left=1300)'
        assert repr(eval(repr(p))) == repr(p)
        assert p.name == 'Player'
        self.assertTrue(True)

    # Mapping, leveling, Display

    def test_pos(self):
        """Test positioning and set-positioning"""
        p = Player.factory(pos=Pos(10, 10))
        assert p.pos == Pos(10, 10)
        p.set_pos(Pos(20, 20))
        assert p.pos == Pos(20, 20)
        self.assertTrue(True)

    def test_char(self):
        """Test map display"""
        p = Player.factory(pos=Pos(10, 10))
        pos, char, color = p.char
        assert pos == Pos(10, 10)
        assert char == '@'
        assert color == (255, 255, 255)
        self.assertTrue(True)

    # Combat interface

    def test_melee_dmg_adj(self):
        p = Player.factory()
        # print (p.melee_dmg_adj)
        assert p.melee_dmg_adj == 1

    def test_melee_hit_adj(self):
        p = Player.factory()
        # print (p.melee_hit_adj)
        assert p.melee_hit_adj == 0

    def test_ac(self):
        p = Player.factory()
        # print (p.ac)
        assert p.ac == 10  # TODO: armor

    @patch('random.randint')
    def test_melee_dmg(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        p = Player.factory()
        # print (p.melee_dmg())
        assert p.melee_dmg() == 2  # STR 16 -> +1, TODO: weapon


class TestRoll(unittest.TestCase):
    """Test damage ('AxB') die rolls"""

    @patch('random.randint')
    def test_lowest(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        dmg = roll('1x4')
        # print(dmg)
        assert dmg == 1
        self.assertTrue(True)

    @patch('random.randint')
    def test_highest(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        dmg = roll('1x4')
        # print(dmg)
        assert dmg == 4
        self.assertTrue(True)

    @patch('random.randint')
    def test_summation(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        dmg = roll('10x4')
        # print(dmg)
        assert mock_randint.call_count == 10
        assert dmg == 40
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
