from enum import Enum
from typing import NamedTuple


class Decor(Enum):
    FOREST = "FOREST"
    FIELD = "FIELD"
    LAKE = "LAKE"
    MEADOW = "MEADOW"
    MINE = "MINE"
    SWAMP = "SWAMP"
    CAPITAL = "CAPITAL"


class Tile(NamedTuple):
    dom_id: int
    decor: Decor
    crown: int


TILES = [
    (Tile(1, Decor.FIELD, 0), Tile(1, Decor.FIELD, 0)),
    (Tile(2, Decor.FIELD, 0), Tile(2, Decor.FIELD, 0)),
    (Tile(3, Decor.FOREST, 0), Tile(3, Decor.FOREST, 0)),
    (Tile(4, Decor.FOREST, 0), Tile(4, Decor.FOREST, 0)),
    (Tile(5, Decor.FOREST, 0), Tile(5, Decor.FOREST, 0)),
    (Tile(6, Decor.FOREST, 0), Tile(6, Decor.FOREST, 0)),
    (Tile(7, Decor.LAKE, 0), Tile(7, Decor.LAKE, 0)),
    (Tile(8, Decor.LAKE, 0), Tile(8, Decor.LAKE, 0)),
    (Tile(9, Decor.LAKE, 0), Tile(9, Decor.LAKE, 0)),
    (Tile(10, Decor.MEADOW, 0), Tile(10, Decor.MEADOW, 0)),
    (Tile(11, Decor.MEADOW, 0), Tile(11, Decor.MEADOW, 0)),
    (Tile(12, Decor.SWAMP, 0), Tile(12, Decor.SWAMP, 0)),
    (Tile(13, Decor.FOREST, 0), Tile(13, Decor.FIELD, 0)),
    (Tile(14, Decor.LAKE, 0), Tile(14, Decor.FIELD, 0)),
    (Tile(15, Decor.MEADOW, 0), Tile(15, Decor.FIELD, 0)),
    (Tile(16, Decor.SWAMP, 0), Tile(16, Decor.MEADOW, 0)),
    (Tile(17, Decor.LAKE, 0), Tile(17, Decor.FOREST, 0)),
    (Tile(18, Decor.MEADOW, 0), Tile(18, Decor.FOREST, 0)),
    (Tile(19, Decor.FOREST, 0), Tile(19, Decor.FIELD, 1)),
    (Tile(20, Decor.LAKE, 0), Tile(20, Decor.FIELD, 1)),
    (Tile(21, Decor.MEADOW, 0), Tile(21, Decor.FIELD, 1)),
    (Tile(22, Decor.SWAMP, 0), Tile(22, Decor.FIELD, 1)),
    (Tile(23, Decor.MINE, 0), Tile(23, Decor.FIELD, 1)),
    (Tile(24, Decor.FIELD, 0), Tile(24, Decor.FOREST, 1)),
    (Tile(25, Decor.FIELD, 0), Tile(25, Decor.FOREST, 1)),
    (Tile(26, Decor.FIELD, 0), Tile(26, Decor.FOREST, 1)),
    (Tile(27, Decor.FIELD, 0), Tile(27, Decor.FOREST, 1)),
    (Tile(28, Decor.LAKE, 0), Tile(28, Decor.FOREST, 1)),
    (Tile(29, Decor.MEADOW, 0), Tile(29, Decor.FOREST, 1)),
    (Tile(30, Decor.FIELD, 0), Tile(30, Decor.LAKE, 1)),
    (Tile(31, Decor.FIELD, 0), Tile(31, Decor.LAKE, 1)),
    (Tile(32, Decor.FOREST, 0), Tile(32, Decor.LAKE, 1)),
    (Tile(33, Decor.FOREST, 0), Tile(33, Decor.LAKE, 1)),
    (Tile(34, Decor.FOREST, 0), Tile(34, Decor.LAKE, 1)),
    (Tile(35, Decor.FOREST, 0), Tile(35, Decor.LAKE, 1)),
    (Tile(36, Decor.MEADOW, 1), Tile(36, Decor.FIELD, 0)),
    (Tile(37, Decor.MEADOW, 1), Tile(37, Decor.LAKE, 0)),
    (Tile(38, Decor.SWAMP, 0), Tile(38, Decor.FIELD, 1)),
    (Tile(39, Decor.SWAMP, 0), Tile(39, Decor.MEADOW, 0)),
    (Tile(40, Decor.FIELD, 0), Tile(40, Decor.MINE, 1)),
    (Tile(41, Decor.MEADOW, 2), Tile(41, Decor.FIELD, 0)),
    (Tile(42, Decor.MEADOW, 2), Tile(42, Decor.LAKE, 0)),
    (Tile(43, Decor.SWAMP, 2), Tile(43, Decor.FIELD, 0)),
    (Tile(44, Decor.SWAMP, 2), Tile(44, Decor.MEADOW, 0)),
    (Tile(45, Decor.FIELD, 0), Tile(45, Decor.MINE, 2)),
    (Tile(46, Decor.MINE, 2), Tile(46, Decor.SWAMP, 0)),
    (Tile(47, Decor.MINE, 2), Tile(47, Decor.SWAMP, 0)),
    (Tile(48, Decor.MINE, 3), Tile(48, Decor.FIELD, 0))
]
