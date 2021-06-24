"""
    Unit test of TurnQueue
"""

import unittest
from turn_queue import TurnQueue


# ===== QueueItem ==========================================
# A synthetic class only for testing the TurnQueue

class QueueItem:
    key: int = 0

    def __init__(self, key: int):
        self.key = key

    def __lt__(self, other: 'QueueItem') -> bool:
        return self.key < other.key

    def __str__(self) -> str:
        return f'({self.key})'


# ===== Testing TurnQueue =====================================

class TestTurnQueue(unittest.TestCase):
    """Use fabricated things to shake it out"""

    def test_insertion(self):
        tq = TurnQueue()
        assert tq.now == 0
        tq.add(QueueItem(4))
        assert tq.now == 0
        _ = tq.pop()
        assert tq.now == 4
        _ = tq.pop()
        assert tq.now == 4
        self.assertTrue(True)

    def test_reordering(self):
        tq = TurnQueue()
        tq.add(QueueItem(4))
        tq.add(QueueItem(0))
        tq.add(QueueItem(2))
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
        assert tq.pop() is None
        self.assertTrue(True)


# ===== Invocation ========================================

# See 'run_tests.py' in parent directory

# EOF
