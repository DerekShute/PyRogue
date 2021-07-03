"""
    Test of factory conversion
"""

import unittest
from factories import ITEM_PROBABILITIES, ARMOR_PROBABILITIES

class TestItemProbs(unittest.TestCase):
    """Test Proc Gen probability breakout"""

    def test_breakout(self):
        """How do the root probabilities look?"""
        names = ITEM_PROBABILITIES[0]
        probs = ITEM_PROBABILITIES[1]
        assert names[0] == 'potion'
        assert probs[0] == 26
        assert names[4] == 'armor'
        assert probs[4] == 7
        self.assertTrue(True)


# ===== Test Armor ================================

class TestArmor(unittest.TestCase):
    """Test Entity Basics"""

    def test_armor_breakout(self):
        """How does the list of armors look?"""
        names = ARMOR_PROBABILITIES[0]
        probs = ARMOR_PROBABILITIES[1]
        assert names[0] == 'leather armor'
        assert probs[0] == 20
        assert names[6] == 'banded mail'
        assert probs[6] == 10
        self.assertTrue(True)

