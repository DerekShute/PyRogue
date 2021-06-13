import unittest
from item import Gold
from position import Pos


# ===== Testing Items =====================================

class TestGold(unittest.TestCase):
    """Test gold"""

    def test_gold(self):
        """Test Elementary stuff"""
        g = Gold(val=10)
        assert str(g) == 'Gold(@(0,0),10)'

        g = Gold(val=20, pos=Pos((20, 20)))
        assert str(g) == 'Gold(@(20,20),20)'
        assert str(g.pos) == '@(20,20)'
        assert g.name == 'gold'
        assert repr(g) == repr(eval(repr(g)))
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
