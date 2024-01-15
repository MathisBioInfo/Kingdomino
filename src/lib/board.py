from typing import NamedTuple

from src.lib.dominos import Tile, Decor


class Bounds(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int


def cartesian_product(list_1, list_2):
    prod = []
    for i in list_1:
        prod.extend([(i, j) for j in list_2])
    return prod


class GameBoard:
    def __init__(self, width, height):
        self.initial_bounds = Bounds(-width, width, -height, height)
        self.current_bounds = Bounds(-width, width, -height, height)
        self.nodes = {(0, 0): Tile(0, Decor.CAPITAL, 0)}
        self.places = {*self.get_neighbors_coords(0, 0)} #Not Used

    def __repr__(self):
        repr = []
        for y in range(self.initial_bounds.max_y, self.initial_bounds.min_y-1, -1):
            repr.append(f"{y:^3}" + " " * 1)
            for x in range(self.initial_bounds.min_x, self.initial_bounds.max_x+1):
                if self._is_not_overbounded_node(x, y):
                    tile = self.nodes.get((x, y), Tile())
                    repr.append(tile.__repr__())
                else:
                    repr.append(" X ")
            repr.append("\n")
        repr.append("\n" + " " * 4)
        repr.extend([f"{x:^3}" for x in range(self.initial_bounds.min_x, self.initial_bounds.max_x+1)])
        repr.append("\n")
        return "".join(repr)

    def _get_max_x(self):
        return max([x for x, _ in self.nodes])

    def _get_min_x(self):
        return min([x for x, _ in self.nodes])

    def _get_max_y(self):
        return max([y for _, y in self.nodes])

    def _get_min_y(self):
        return min([y for _, y in self.nodes])

    def _update_bounds(self):
        self.current_bounds = Bounds(
            self.initial_bounds.min_x + self._get_max_x(),
            self.initial_bounds.max_x + self._get_min_x(),
            self.initial_bounds.min_y + self._get_max_y(),
            self.initial_bounds.max_y + self._get_min_y(),
        )

    def _is_not_overbounded_node(self, x, y):
        return (
            x > self.current_bounds.min_x and
            x < self.current_bounds.max_x and
            y > self.current_bounds.min_y and
            y < self.current_bounds.max_y
        )

    def _is_not_overbounded_domino(self, pos1, pos2):
        return (
            self._is_not_overbounded_node(*pos1) and
            self._is_not_overbounded_node(*pos2)
        )

    def _add_node(self, x, y, tile):
        self.nodes[(x, y)] = tile
        self._update_bounds()

    def _add_domino(self, pos1, pos2, domino):
        self.nodes[pos1] = domino[0]
        self.nodes[pos2] = domino[1]
        self._update_bounds()

    def _to_matrix(self):
        mat = []
        for x in range(self.current_bounds.min_x+1, self.current_bounds.max_x):
            sub_mat = []
            for y in range(self.current_bounds.min_y+1, self.current_bounds.max_y):
                sub_mat.append(self.nodes.get((x, y), Tile()))
            mat.append(sub_mat)
        return mat

    def _to_adjacency_matrix(self):
        raise NotImplementedError

    def _to_adjacency_list(self):
        raise NotImplementedError

    def get_neighbors_coords(self, x, y):
        return [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

    def get_neighbors(self, x, y):
        return {coord: self.nodes.get(coord, Tile()) for coord in self.get_neighbors_coords()}

    def add_node(self, x, y, tile):
        raise NotImplementedError

    def add_domino(sefl, pos1, pos2, domino):
        raise NotImplementedError



