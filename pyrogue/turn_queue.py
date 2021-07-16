"""
    The turn queue: clock and action queue for entities
"""
import bisect
from typing import List


# ===== TurnQueue =========================================

class TurnQueue:
    _queue: List = []

    def __init__(self):
        self._queue = []

    def __str__(self) -> str:
        s = 'TurnQueue('
        for i in self._queue:
            s = f'{s} {i.key}'
        return s + ')'

    @property
    def now(self) -> int:
        """Return the key of the first thing in the queue"""
        return 0 if len(self._queue) == 0 else self._queue[0].key

    @property
    def end(self) -> int:
        """Return the key of the last thing in the queue"""
        return 0 if len(self._queue) == 0 else self._queue[-1].key

    def add(self, new):
        # This has weird effects if you push something in the 'past' but I need to
        # see how it shakes out
        bisect.insort(self._queue, new)

    def pop(self):
        """Return the thing at the top of the queue and update .now"""
        if len(self._queue) == 0:
            return None
        ret = self._queue.pop(0)
        return ret

    def remove(self, rid):
        if rid in self._queue:
            self._queue.remove(rid)


# ===== Testing ===========================================

# See test_turn_queue.py

# EOF
