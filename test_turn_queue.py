import unittest
from turn_queue import TurnQueue

class TestItem:
    key: int = 0

    def __init__(self, key: int):
        self.key = key

    def __lt__(self, other: 'TestItem') -> bool:
        return self.key < other.key

    def __str__(self) -> str:
        return f'({self.key})'


# ===== Testing Rooms =====================================

class TestTurnQueue(unittest.TestCase):
    """Use fabricated things to shake it out"""

    def test_insertion(self):
        tq = TurnQueue()
        assert tq.now == 0
        tq.add(TestItem(4))
        assert tq.now == 0
        _ = tq.pop()
        assert tq.now == 4
        _ = tq.pop()
        assert tq.now == 4
        self.assertTrue(True)

    def test_reordering(self):
        tq = TurnQueue()
        tq.add(TestItem(4))
        tq.add(TestItem(0))
        tq.add(TestItem(2))
        assert tq.now == 0
        assert tq.pop().key == 0
        assert tq.now == 0
        assert tq.pop().key == 2
        assert tq.now == 2
        assert tq.pop().key == 4
        assert tq.now == 4
        self.assertTrue(True)

    def test_empty(self):
        tq = TurnQueue()
        assert tq.pop() == None
        self.assertTrue(True)

# ===== Invocation ========================================

if __name__ == '__main__':
    unittest.main()

# EOF
