"""
    Test random generating elements
"""

from parameterized import parameterized
import unittest
from unittest.mock import patch
from procgen import new_food, new_armor, ITEM_PROBABILITIES, ARMOR_PROBABILITIES


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

    @parameterized.expand([(0, 'a slime-mold'),
                           (10, 'a food ration'),
                           (90, 'a food ration')])
    @patch('random.randint')
    def test_food(self, input, expected, mock_randint):
        mock_randint.return_value = input
        food = new_food()
        assert food.description == expected
        self.assertTrue(True)

    @patch('random.choices')
    def test_armor(self, mock_randint):
        mock_randint.return_value = [5]
        armor = new_armor()
        assert armor.description == 'splint mail'
        assert armor.value == 4
        assert armor.worth == 80
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
