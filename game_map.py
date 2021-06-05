"""
The map is the grid that sits on top of the display.  Eventually we'd be able
to have a map larger than the display: You'd see only a fraction of it in the
display.

From tcod_tutorial_v2
"""

import numpy as np  # type: ignore
from position import Pos
from typing import Tuple
from display import Display

import tile_types

# This dodges around the chicken/egg of defining GameMap.FLOOR after TILES

_FLOOR = 0
_WALL = 1
_DOOR = 2
_STAIRS = 3

# Internal reference to equate GameMap.FLOOR with tile_types.floor, which needs be known by nobody

_TILES = {
    _FLOOR: tile_types.floor,
    _WALL: tile_types.wall,
    _DOOR: tile_types.door,
    _STAIRS: tile_types.down_stairs,
}


# ===== GameMap ===========================================

class GameMap:

    # References for export.  Outside clients use GameMap.FLOOR

    FLOOR: int = _FLOOR
    WALL: int = _WALL
    DOOR: int = _DOOR
    STAIRS: int = _STAIRS

    def __init__(self, width: int, height: int, display: Display):
        self._display = display
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=_TILES[GameMap.WALL], order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """

        # TODO: this needs to hold the topmost and hand the grid to the Display, which figures out colors and shapes

        self._display.rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )
        # TODO : Entities

    def set_tiles(self, inner: Tuple[slice, slice], tile: int):
        """
        Set the basics of the map: what is the underlying location?
        """
        t = _TILES[tile]
        self.tiles[inner] = t
        self._display.rgb[inner] = np.select(
            condlist=[self.visible[inner], self.explored[inner]],
            choicelist=[self.tiles[inner]["light"], self.tiles[inner]["dark"]],
            default=tile_types.SHROUD
        )

    def set_tile(self, p: Pos, tile: int):
        """
        Set a single tile
        """
        self.tiles[p.x, p.y] = _TILES[tile]
        t = tile_types.SHROUD
        if self.visible[p.x, p.y] and self.explored[p.x, p.y]:
            t = self.tiles[p.x, p.y]['light']
        else:
            t = self.tiles[p.x, p.y]['dark']
        self._display.rgb[p.x, p.y] = t

    def lit(self, inner: Tuple[slice, slice], lit: bool = True):
        """Set a region to lit / visible"""
        self.visible[inner] = lit
        self._display.rgb[inner] = np.select(
            condlist=[self.visible[inner], self.explored[inner]],
            choicelist=[self.tiles[inner]["light"], self.tiles[inner]["dark"]],
            default=tile_types.SHROUD
        )

    def lit_tile(self, p: Pos, lit: bool = True):
        self.visible[p.x, p.y] = lit
        # TODO: is it worth pushing it through?

    def explore(self, inner: Tuple[slice, slice], known: bool = True):
        """Mark a region as player-discovered"""
        self.explored[inner] = known
        self._display.rgb[inner] = np.select(
            condlist=[self.visible[inner], self.explored[inner]],
            choicelist=[self.tiles[inner]["light"], self.tiles[inner]["dark"]],
            default=tile_types.SHROUD
        )

    def explore_tile(self, p: Pos, known: bool = True):
        self.explored[p.x, p.y] = known
        # TODO: is it worth pushing it through?


# ===== TESTING ===========================================

if __name__ == '__main__':
    import time

    def rectangle(x1: int, y1: int, x2: int, y2: int) -> Tuple[slice, slice]:
        return slice(x1, x2), slice(y1, y2)

    with Display(80, 25, 'testing GameMap') as d:
        m = GameMap(80, 25, d)
        m.set_tiles(rectangle(5, 5, 20, 20), GameMap.FLOOR)
        m.set_tile(Pos((4, 5)), GameMap.DOOR)
        m.set_tile(Pos((6, 6)), GameMap.STAIRS)
        m.lit(rectangle(0, 0, 10, 25), True)
        # NOTE: lit but not explored is odd
        m.explore(rectangle(0, 0, 40, 10), True)
        d.present()
        time.sleep(2)
        m.lit(rectangle(0, 0, 10, 25), False)
        d.present()

        time.sleep(2)
        m.explore(rectangle(5, 5, 20, 20), False)
        d.present()
        time.sleep(2)

    print('*** Tests Passed ***')

# EOF
