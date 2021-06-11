"""
    Unit test of position
"""

import unittest
from position import Pos


class TestPosition(unittest.TestCase):
    """Test position"""

    # Could actually be many tests, but why bother?
    def test(self):
        p = Pos((10, 20))
        assert str(p) == '@(10,20)'
        assert p.x == 10
        assert p.y == 20
        assert p.xy == (10, 20)

        p = Pos(15, 25)
        assert str(p) == '@(15,25)'
        assert eval(repr(p)) == p

        assert Pos(5, 15) == Pos(Pos(5, 15))
        
        assert not Pos(1, 1) == Pos(2, 2)
        assert Pos(1, 2) == Pos(x=1, y=2)

        
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
