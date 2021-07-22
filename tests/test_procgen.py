"""
    Test random generating elements
"""

from parameterized import parameterized
import unittest
from unittest.mock import patch
from procgen import new_food, new_armor, new_weapon, ITEM_PROBABILITIES, ARMOR_PROBABILITIES


# TODO: new_thing()


# ==== Test Item Probabilities ============================

class TestItemProbs(unittest.TestCase):
    """Test Proc Gen probability breakout"""

    def test_breakout(self):
        """How do the root probabilities look?"""
        assert ITEM_PROBABILITIES[0] == 26  # Potion
        assert ITEM_PROBABILITIES[4] == 7   # Armor
        self.assertTrue(True)

    def test_armor_breakout(self):
        """How does the list of armors look?"""
        assert ARMOR_PROBABILITIES[0] == 20  # Leather
        assert ARMOR_PROBABILITIES[6] == 10  # Banded
        self.assertTrue(True)


# ===== Testing Items =====================================

class TestProcgenItem(unittest.TestCase):
    """Create items"""

    @parameterized.expand([(0, 'slime-mold'),
                           (10, 'food ration'),
                           (90, 'food ration')])
    @patch('random.randint')
    def test_food(self, input, expected, mock_randint):
        mock_randint.return_value = input
        food = new_food()
        assert food.description(set()) == expected
        self.assertTrue(True)

    @parameterized.expand([(0, -1),    # cursed -1
                           (25, 1),   # magic +1
                           (90, 0)])  # absolutely normal
    @patch('random.choices')
    @patch('random.randint')
    @patch('procgen.plus_value')
    def test_armor(self, input, expected, mock_plus, mock_randint, mock_choices):
        mock_plus.return_value = 1
        mock_randint.return_value = input
        mock_choices.return_value = [5]  # peg on splint mail
        armor = new_armor()
        assert armor.description(set()) == 'splint mail'
        assert armor.hplus == expected
        if input == 0:
            assert 'cursed' in armor.state
        else:
            assert 'cursed' not in armor.state
        assert armor.worth == 80
        self.assertTrue(True)

    @parameterized.expand([(5, -1),   # cursed -1
                           (12, 1),   # magic +1
                           (90, 0)])  # absolutely normal
    @patch('random.choices')
    @patch('random.randint')
    @patch('procgen.plus_value')
    def test_weapon(self, input, expected, mock_plus, mock_randint, mock_choices):
        mock_plus.return_value = 1
        mock_randint.return_value = input
        mock_choices.return_value = [6]  # peg on dart
        weapon = new_weapon()
        assert weapon.description(set()) == 'dart'
        assert weapon.dam == '1x1'
        assert weapon.hplus == expected
        if input == 5:
            assert 'cursed' in weapon.state
        else:
            assert 'cursed' not in weapon.state
        self.assertTrue(True)

# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
