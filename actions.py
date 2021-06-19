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
        if level.can_enter(dest):  # TODO: might depend on 'can entity enter square'
            entity.move(self.dx, self.dy)
            # TODO: update display for the two positions involved
            # TODO: consequences of entering square
        # TODO: elif entity here then MeleeAction(attacker, defender).perform()
        else:
            entity.bump(self.dx, self.dy)  # TODO: thing you're bonking against
            # TODO: BumpAction as first level, and if can-enter then MoveAction.perform()


class PickupAction(Action):
    def perform(self, entity: Player, level: Level) -> None:
        items = level.items_at(entity.pos)
        if items == []:
            entity.pick_up(None)
        else:
            entity.pick_up(items[0])  # TODO: top of stack vs menu to select

# EOF
