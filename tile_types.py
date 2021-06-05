"""
From tcod_tutorial_v2
"""

from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

def darken_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return [sum(x) for x in zip(color, (-100, -100, -100))]

# TODO: BLACK / WHITE

# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

# TODO: floor light background / dark background as constant
# TODO: wall light background / dark background as constant
# TODO: darken()
FEATURE_LIGHT = (255, 255, 255)  # White
FEATURE_DARK = darken_color(FEATURE_LIGHT)  # Gray
FLOOR_LIGHT = (200, 180, 50)
WALL_LIGHT = (130, 100, 50)

DOOR_CHAR = ord("+")
STAIR_CHAR = ord(">")
SPACE_CHAR = ord(" ")

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(SPACE_CHAR, (255, 255, 255), darken_color(FLOOR_LIGHT)),
    light=(SPACE_CHAR, (255, 255, 255), FLOOR_LIGHT),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(SPACE_CHAR, (255, 255, 255), darken_color(WALL_LIGHT)),
    light=(SPACE_CHAR, (255, 255, 255), WALL_LIGHT),
)

door = new_tile(
    walkable=False,
    transparent=False,
    dark=(DOOR_CHAR, FEATURE_DARK, darken_color(WALL_LIGHT)),
    light=(DOOR_CHAR, FEATURE_LIGHT, WALL_LIGHT),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(STAIR_CHAR, FEATURE_DARK, darken_color(FLOOR_LIGHT)),
    light=(STAIR_CHAR, FEATURE_LIGHT, FLOOR_LIGHT),
)
# EOF
