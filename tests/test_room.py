import unittest
from unittest.mock import patch
import pyrogue
from pyrogue.room import Room
from pyrogue.position import Pos


# ===== Service Routines ==================================

def randint_return_min(*args, **kwargs):
    """If asked to random.randint(x,y), return x"""
    assert args[0] < args[1]   # Check for stupid mistake
    return args[0]


def randint_return_max(*args, **kwargs):
    """If asked to random.randint(x,y), return y"""
    assert args[0] < args[1]   # Check for stupid mistake
    return args[1]


# ===== Testing Rooms =====================================

class TestRoom(unittest.TestCase):
    """Test the room constructions and expectations"""

    def test_room_basics(self):
        """Test Elementary stuff"""
        r = Room(Pos((0, 0)), Pos((10, 20)))
        assert r.center.x == 4
        assert r.center.y == 9
        assert str(r) == 'Room @(0,0)-@(10,20)'
        assert str(r.max_pos) == '@(10,20)'
        assert str(r.shadow()) == '(slice(0, 10, None), slice(0, 20, None))'
        self.assertTrue(True)

    @patch('random.randint')
    def test_rnd_pos_min(self, mock_randint):
        """Test boundaries of room random position: top left corner"""
        mock_randint.side_effect = randint_return_min
        r = Room(Pos((0, 0)), Pos((10, 20)))
        p = r.rnd_pos
        assert mock_randint.call_count == 2
        assert mock_randint.call_args_list == [((0, 9),), ((0, 19),)]  # No I don't know why
        assert p == Pos((0, 0))
        self.assertTrue(True)

    @patch('random.randint')
    def test_rnd_pos_max(self, mock_randint):
        """Test boundaries of room random position: bottom right corner"""
        mock_randint.side_effect = randint_return_max
        r = Room(Pos((0, 0)), Pos((10, 20)))
        p = r.rnd_pos
        assert mock_randint.call_count == 2
        assert mock_randint.call_args_list == [((0, 9),), ((0, 19),)]  # No I don't know why
        assert p == Pos((9, 19))
        self.assertTrue(True)


# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
