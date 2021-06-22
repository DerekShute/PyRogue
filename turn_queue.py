"""
    The turn queue: clock and action queue for entities
"""
import bisect
from typing import List


# ===== TurnQueue =========================================

class TurnQueue:
    _queue: List = []
    _now: int = 0

    def __init__(self):
        self._queue = []
        self._now = 0

    def __str__(self) -> str:
        s = 'TurnQueue('
        for i in self._queue:
            s = f'{s} {i.key}'
        return s + ')'

    @property
    def now(self) -> int:
        """Return the key of the thing that was popped most recently"""
        return self._now

    def add(self, new):
        # This has weird effects if you push something in the 'past' but I need to
        # see how it shakes out
        bisect.insort(self._queue, new)
        self._now = new.key if new.key < self._now else self._now

    def pop(self):
        """Return the thing at the top of the queue and update .now"""
        if len(self._queue) == 0:
            return None
        ret = self._queue.pop(0)
        self._now = ret.key
        return ret


# ===== Testing ===========================================

# See test_turn_queue.py

# EOF
