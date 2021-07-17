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

    def incorporate(self, key: int) -> None:
        """Gotten some additional information to meld into this Action"""
        raise NotImplementedError()


class QuitAction(Action):
    def incorporate(self, key: int) -> Action:
        if chr(key) == 'Y' or chr(key) == 'y':
            return self
        return None

    def perform(self, entity: Entity) -> None:
        entity.quit_action('quit')


class BumpAction(Action):
    """Bonk into something, or move"""

    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, entity: Entity) -> None:
        dest = Pos(entity.pos.x + self.dx, entity.pos.y + self.dy)
        if not entity.level.can_enter(dest):
            entity.bump(pos=dest)
            return
        if entity.level.player is not None and entity.level.player.pos == dest:
            entity.fight(entity.level.player)
            return
        monsters = entity.level.monsters_at(dest)
        if len(monsters) > 0:
            entity.fight(monsters[0])
            return
        MovementAction(self.dx, self.dy).perform(entity)


class DescendAction(Action):
    """Go down"""
    def perform(self, entity: Entity) -> None:
        if entity.level.is_stairs(entity.pos):
            entity.descend()
        else:
            entity.add_msg('No stairs here!')


class DropAction(Action):
    """Drop an item in entity inventory"""
    index: int = 0

    def perform(self, entity: Entity) -> None:
        if self.index >= len(entity.pack):
            entity.add_msg('No such item to drop!')
            return
        entity.drop(entity.pack[self.index])

    def incorporate(self, index: int = 0):
        self.index = index
        return self


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
        if entity.level.can_enter(dest):
            entity.move(self.dx, self.dy)
        # TODO: not sure 'else'


class PickupAction(Action):
    """Pick up item at feet (or at other location if that makes sense)"""
    def perform(self, entity: Entity) -> None:
        items = entity.level.items_at(entity.pos)
        entity.pick_up(None if items == [] else items[0])
        # TODO: top of stack vs menu to select


class UseAction(Action):
    """Use an item in entity inventory"""
    index: int = 0

    def perform(self, entity: Entity) -> None:
        if self.index >= len(entity.pack):
            entity.add_msg('No such item to use!')
            return
        entity.use(entity.pack[self.index])

    def incorporate(self, index: int = 0):
        self.index = index
        return self


class EquipAction(Action):
    """Equip an item in entity inventory"""
    index: int = 0

    def perform(self, entity: Entity) -> None:
        if self.index >= len(entity.pack):
            entity.add_msg('No such item to equip!')
            return
        entity.equip(entity.pack[self.index])

    def incorporate(self, index: int = 0):
        self.index = index
        return self

# EOF
