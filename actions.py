"""
    This stolen wholesale from tcod_tutorial
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from position import Pos

if TYPE_CHECKING:
    from entity import Entity


class Action:
    def perform(self, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class DescendAction(Action):
    """Go down"""
    def perform(self, entity: Entity) -> None:
        if entity.level.is_stairs(entity.pos):
            entity.descend()
        else:
            entity.add_msg('No stairs here!')  # TODO real message


class EscapeAction(Action):
    def perform(self, entity: Entity) -> None:
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx  # TODO: Pos
        self.dy = dy

    def perform(self, entity: Entity) -> None:
        dest = Pos(entity.pos.x + self.dx, entity.pos.y + self.dy)
        monsters = entity.level.monsters_at(dest)
        if len(monsters) > 0:
            # TODO: other games verify if monster nonhostile.  Not Rogue.
            entity.fight(monsters[0])
        elif entity.level.can_enter(dest):  # TODO: might depend on 'can entity enter square'
            entity.move(self.dx, self.dy)
            # TODO: update display for the two positions involved
            # TODO: consequences of entering square
        else:
            entity.bump(pos=dest)  # TODO: thing you're bonking against
            # TODO: BumpAction as first level, and if can-enter then MoveAction.perform()


class PickupAction(Action):
    def perform(self, entity: Player) -> None:
        items = entity.level.items_at(entity.pos)
        entity.pick_up(None if items == [] else items[0])
        # TODO: top of stack vs menu to select

# EOF
