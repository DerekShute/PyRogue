"""
    Test of things in player module
"""

import unittest
from unittest.mock import patch
from player import roll, Player, Stats
from position import Pos
from actions import MovementAction, PickupAction
from level import Level
from item import Gold


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


# ===== Test Player Basics ================================

class TestPlayer(unittest.TestCase):
    """Test Player"""

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
        assert p.display == 'HP:12/12 Level:0(0) STR:16 GP:0'
        self.assertTrue(True)

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
        assert char == ord('@')
        assert color == (255, 255, 255)
        self.assertTrue(True)


# ===== Test Action =======================================

class TestPlayerActionCallback(unittest.TestCase):

    def test_move(self):
        """Move action moves the player"""
        p = Player.factory(pos=Pos(10, 10))
        p.move(-1, -1)
        assert p.pos == Pos(9, 9)
        self.assertTrue(True)


# ===== Test AI Callback ==================================

class TestPlayerAI(unittest.TestCase):

    @patch('player_input.PlayerInputHandler.get_action')
    def test_perform_move_allowed(self, mock_get_action):
        """Player was allowed to move"""
        mock_get_action.return_value = MovementAction(-1, -1)
        p = Player.factory(pos=Pos(10, 10))
        with patch.object(Level, 'can_enter', return_value=True) as patched_level:
            p.attach_level(Level(80, 25, None))
            p.perform()
            patched_level.assert_called_once()
        mock_get_action.assert_called_once()
        assert p.pos == Pos(9, 9)
        self.assertTrue(True)

    @patch('player_input.PlayerInputHandler.get_action')
    def test_perform_move_denied(self, mock_get_action):
        """Player was not allowed to move"""
        mock_get_action.return_value = MovementAction(-1, -1)
        p = Player.factory(pos=Pos(10, 10))
        with patch.object(Level, 'can_enter', return_value=False) as patched_level:
            p.attach_level(Level(80, 25, None))
            p.perform()
            patched_level.assert_called_once()
        mock_get_action.assert_called_once()
        assert p.pos == Pos(10, 10)
        self.assertTrue(True)

    @patch('player_input.PlayerInputHandler.get_action')
    def test_perform_pickup_gold(self, mock_get_action):
        """Pick up an Item"""
        mock_get_action.return_value = PickupAction()
        p = Player.factory(pos=Pos(10, 10))
        level = Level(80, 25, None)
        _ = Gold(val=10, pos=Pos(10, 10), level=level)
        p.attach_level(level)
        p.perform()
        mock_get_action.assert_called_once()
        assert level.items == []  # Gone from map
        assert p.display == 'HP:12/12 Level:0(0) STR:16 GP:10'
        self.assertTrue(True)

    # TODO: bump actions, take actions, etc.


# ===== Test Combat Interface =============================

class TestPlayerCombat(unittest.TestCase):
    """Player Combat Interface"""

    def test_melee_dmg_adj(self):
        p = Player.factory()
        # print (p.melee_dmg_adj)
        assert p.melee_dmg_adj == 1
        self.assertTrue(True)

    def test_melee_hit_adj(self):
        p = Player.factory()
        # print (p.melee_hit_adj)
        assert p.melee_hit_adj == 0
        self.assertTrue(True)

    def test_ac(self):
        p = Player.factory()
        # print (p.ac)
        assert p.ac == 10  # TODO: armor
        self.assertTrue(True)

    @patch('random.randint')
    def test_melee_dmg(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        p = Player.factory()
        # print (p.melee_dmg())
        assert p.melee_dmg() == 2  # STR 16 -> +1, TODO: weapon
        self.assertTrue(True)


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
