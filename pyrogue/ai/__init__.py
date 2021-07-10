"""
    AI Basics
"""
import random
from entity import Entity
from level import Level
from actions import Action, MovementAction


# ===== AI ================================================

class AI:
    """AI Superclass"""
    previous: 'AI'
    # TODO: turns_remaining

    def __init__(self, previous: 'AI' = None):
        self.previous = previous

    def activate(self) -> bool:
        """Does this entity come awake?"""
        return True  # TODO: chance of staying asleep?

# ===== ConfusedAI ========================================

class ConfusedAI(AI):
    """This is permanently or temporarily confused"""

    def get_action(self) -> Action:
        dx, dy = random.choice(
            [(-1, -1),  # Northwest
             (0, -1),   # North
             (1, -1),   # Northeast
             (-1, 0),   # West
             (1, 0),    # East
             (-1, 1),   # Southwest
             (0, 1),    # South
             (1, 1),]   # Southeast
        )
        return MovementAction(dx, dy)
        # TODO: countdown


# ===== HostileAI =========================================

class HostileAI(AI):
    """Hostile entities"""
    target: Entity = None  # TODO: or next position

    def __init__(self):
        self.target = None

    # TODO: perform() get player from level

# EOF
