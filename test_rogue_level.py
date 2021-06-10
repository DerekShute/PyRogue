"""
    Unit test of Rogue Level generation
"""

import unittest
from unittest.mock import patch
import rogue_level


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


# ===== Testing Rogue Level ===============================

class TestRandmonster(unittest.TestCase):
    """Test random monster selection in rooms"""

    @patch('random.randint')
    def test_min(self, mock_randint):
        mock_randint.side_effect = randint_return_min
        r = chr(rogue_level.randmonster(1, False))
        # print(f'min 1: {r}')
        assert r == 'K'

        r = chr(rogue_level.randmonster(7, False))
        # print(f'min 7: {r}')
        assert r == 'E'

        r = chr(rogue_level.randmonster(26, False))
        # print(f'min 26: {r}')
        assert r == 'U'

        r = chr(rogue_level.randmonster(100, False))
        # print(f'min 100: {r}')
        assert r == 'M'

        self.assertTrue(True)

    @patch('random.randint')
    def test_max(self, mock_randint):
        mock_randint.side_effect = randint_return_max
        r = chr(rogue_level.randmonster(1, False))
        # print(f'max 1: {r}')
        assert r == 'H'

        r = chr(rogue_level.randmonster(7, False))
        # print(f'max 7: {r}')
        assert r == 'C'

        r = chr(rogue_level.randmonster(26, False))
        # print(f'max 26: {r}')
        assert r == 'D'

        r = chr(rogue_level.randmonster(100, False))
        # print(f'max 100: {r}')
        assert r == 'D'

        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
