"""
    This stolen wholesale from tcod_tutorial
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from position import Pos

if TYPE_CHECKING:
    from level import Level
    from player import Player


class Action:
    def perform(self, entity: Player, level: Level) -> None:
        """Perform this action with the objects needed to determine its scope.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, entity: Player, level: Level) -> None:
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx  # TODO: Pos
        self.dy = dy

    def perform(self, entity: Player, level: Level) -> None:
        dest = Pos(entity.pos.x + self.dx, entity.pos.y + self.dy)
        if level.can_enter(dest):
            entity.move(self.dx, self.dy)
        else:
            entity.add_msg('Ouch!')
            # TODO: update display for the two positions involved

# EOF
