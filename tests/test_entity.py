"""
    Test of things in entity module
"""

import unittest
from entity import Entity


# ===== Test Basics ================================

class TestEntity(unittest.TestCase):
    """Test Entity Basics"""

    def test_comparisons(self):
        """Key testing for comparisons"""
        e1 = Entity(key=4)
        e2 = Entity(key=5)
        assert e1 < e2
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
