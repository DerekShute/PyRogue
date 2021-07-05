"""
    Unit Test Combat Formulae
"""

from parameterized import parameterized

import unittest
from unittest.mock import patch
import combat
from player import Player
from monster import Monster


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


def choice_return_first(*args, **kwargs):
    """If asked to random.choice([things]), return first"""
    return args[0][0]

# ===== Test Basics =======================================


class TestRoll(unittest.TestCase):
    """Test damage ('AxB') die rolls"""

    @patch('random.randint')
    def test_lowest(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        dmg = combat.roll('1x4')
        # print(dmg)
        assert dmg == 1
        self.assertTrue(True)

    @patch('random.randint')
    def test_highest(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        dmg = combat.roll('1x4')
        # print(dmg)
        assert dmg == 4
        self.assertTrue(True)

    @patch('random.randint')
    def test_summation(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        dmg = combat.roll('10x4')
        # print(dmg)
        assert mock_randint.call_count == 10
        assert dmg == 40
        self.assertTrue(True)


class TestCombatBasics(unittest.TestCase):
    """Test Basic Formulae"""

    @patch('random.randint')
    def test_swing_miss(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        result = combat.swing(1, 6, 0)  # Level 1 player, Armor 6 orc
        assert result is False
        self.assertTrue(True)

    @patch('random.randint')
    def test_swing_hit(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        result = combat.swing(1, 6, 0)  # Level 1 player, Armor 6 orc
        assert result is True
        self.assertTrue(True)

    @patch('random.randint')
    def test_swing_odds(self, mock_randint):
        success_count = 0
        for i in range(0, 19):
            mock_randint.return_value = i
            result = combat.swing(1, 9, 0)  # Level 1 player, AC 9, no bonuses
            if result is True:
                success_count = success_count + 1
        assert success_count == 9  # 9 hits out of 20 attempts
        self.assertTrue(True)

    @patch('random.randint')
    def test_roll_em_miss(self, mock_randint):
        mock_randint.return_value = 16  # Needs 17 to hit
        p = Player.factory()
        m = Monster.factory(None, 1, ord('G'))
        result = combat.roll_em(p, m)
        assert result == 0
        self.assertTrue(True)

    @patch('random.randint')
    def test_roll_em_hit(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        p = Player.factory()
        m = Monster.factory(None, 1, ord('G'))
        result = combat.roll_em(p, m)
        assert result == 5  # Damage done - max of 1..4 + 1
        self.assertTrue(True)

    @patch('random.randint')
    @patch('player.Player.melee_attack')
    def test_roll_em_hit_dplus(self, mock_melee, mock_randint):
        """dplus figures into damage returned by roll_em"""
        mock_randint.side_effect = randint_return_max
        mock_melee.return_value = (1, 16, '1x4', 5)
        p = Player.factory()
        m = Monster.factory(None, 1, ord('G'))
        result = combat.roll_em(p, m)
        assert result == 10  # Damage done - max of 1..4 + 1 + 5
        self.assertTrue(True)

# TODO: roll_em multiple attacks, but need monster to attack player

    @patch('random.randint')
    @patch('random.choice')
    def test_fight_miss(self, mock_choice, mock_randint):
        mock_choice.side_effect = choice_return_first
        mock_randint.return_value = 10
        p = Player.factory()
        m = Monster.factory(None, 1, ord('G'))
        assert m.hpt == 130
        combat.fight(p, m)
        assert m.hpt == 130  # Swing and a miss
        assert p.curr_msg == 'You miss the griffin'
        self.assertTrue(True)

    @patch('random.randint')
    @patch('random.choice')
    def test_fight_hit(self, mock_choice, mock_randint):
        mock_choice.side_effect = choice_return_first
        mock_randint.side_effect = randint_return_max
        p = Player.factory()
        m = Monster.factory(None, 1, ord('G'))
        assert m.hpt == 104
        combat.fight(p, m)
        assert m.hpt == 99  # 5 points - max(1, 4) + 1
        assert p.curr_msg == 'You scored an excellent hit on the griffin'
        self.assertTrue(True)

    @patch('random.randint')
    @patch('random.choice')
    def test_fight_kill(self, mock_choice, mock_randint):
        mock_choice.side_effect = choice_return_first
        mock_randint.side_effect = randint_return_max
        p = Player.factory()
        m = Monster.factory(None, 1, ord('H'))
        assert p.exp == 0  # Buck private
        assert m.hpt == 8
        combat.fight(p, m)
        assert m.hpt == 3  # 5 points - max(1, 4) + 1
        assert p.curr_msg == 'You scored an excellent hit on the hobgoblin'
        p.advance_msg()
        combat.fight(p, m)
        assert p.exp == 4  # exp=3 + 1 for 8 hit points
        assert p.curr_msg == 'You scored an excellent hit on the hobgoblin --MORE--'
        p.advance_msg()
        assert p.curr_msg == 'You killed the hobgoblin!'
        self.assertTrue(True)

# TODO: test effects of magic/cursed weapon on hit chance

# TODO: test effects of magic/cursed armor on defense

# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
