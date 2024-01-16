from typing import NamedTuple
from copy import deepcopy

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


def flat_n_uniq(list):
    return set([elmt for sublist in list for elmt in sublist])


class GameBoard:
    def __init__(self, width, height):
        self.initial_bounds = Bounds(-width, width, -height, height)
        self.bounds = Bounds(-width, width, -height, height)
        self.nodes = {(0, 0): Tile(0, Decor.CAPITAL, 0)}
        self._playable_nodes = set()
        self._playable_dominos = set()

        self._update_playable_nodes(0, 0)
        self._update_playable_dominos()


    def __repr__(self):
        playables = flat_n_uniq(self._playable_dominos)
        repr = []
        for y in range(self.bounds.max_y, self.bounds.min_y-1, -1):
            repr.append(f"{y:^3}" + " " * 1)
            for x in range(self.bounds.min_x, self.bounds.max_x+1):
                if not self._is_not_overbounded_node(x, y):
                    repr.append(" X ")
                elif (x, y) in self.nodes:
                    repr.append(self.nodes[(x, y)].__repr__())
                elif (x, y) in playables:
                    repr.append(" p ")
                else:
                    repr.append(" . ")
            repr.append("\n")
        repr.append("\n" + " " * 4)
        repr.extend([f"{x:^3}" for x in range(self.bounds.min_x, self.bounds.max_x+1)])
        return "".join(repr)
    

    def copy(self):
        return deepcopy(self)


    def _get_max_x(self):
        return max([x for x, _ in self.nodes])


    def _get_min_x(self):
        return min([x for x, _ in self.nodes])


    def _get_max_y(self):
        return max([y for _, y in self.nodes])


    def _get_min_y(self):
        return min([y for _, y in self.nodes])


    def _update_bounds(self):
        self.bounds = Bounds(
            self.initial_bounds.min_x + self._get_max_x(),
            self.initial_bounds.max_x + self._get_min_x(),
            self.initial_bounds.min_y + self._get_max_y(),
            self.initial_bounds.max_y + self._get_min_y(),
        )


    def _update_playable_nodes(self, x, y):
        playables = (self._playable_nodes | set(self._get_free_neighbors_coords(x, y))) - {(x, y)}
        self._playable_nodes = {p for p in playables if self._is_not_overbounded_node(*p)}


    def _update_playable_dominos(self):
        res = []
        for p in self._playable_nodes:
            playables = cartesian_product([p], self._get_free_neighbors_coords(*p))
            valid_playables = [d for d in playables if self._is_not_overbounded_domino(*d)]
            rotated_playables = [(pos_2, pos_1) for (pos_1, pos_2) in valid_playables]
            res.extend(valid_playables)
            res.extend(rotated_playables)

        self._playable_dominos = set(res)


    def _is_not_overbounded_node(self, x, y):
        return (
            x > self.bounds.min_x and
            x < self.bounds.max_x and
            y > self.bounds.min_y and
            y < self.bounds.max_y
        )


    def _is_not_overbounded_domino(self, pos_1, pos_2):
        return (
            self._is_not_overbounded_node(*pos_1) and
            self._is_not_overbounded_node(*pos_2)
        )


    def _add_node(self, x, y, tile):
        self.nodes[(x, y)] = tile
        self._update_bounds()
        self._update_playable_nodes(x, y)


    def _add_domino(self, pos_1, pos_2, tiles):
        self._add_node(*pos_1, tiles[0])
        self._add_node(*pos_2, tiles[1])
        self._update_playable_dominos()


    def to_matrix(self):
        mat = []
        for x in range(self.bounds.min_x+1, self.bounds.max_x):
            sub_mat = []
            for y in range(self.bounds.min_y+1, self.bounds.max_y):
                sub_mat.append(self.nodes.get((x, y), None))
            mat.append(sub_mat)
        return mat


    def _get_neighbors_coords(self, x, y):
        return [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]


    def _get_free_neighbors_coords(self, x, y):
        return [pos for pos in self._get_neighbors_coords(x, y) if pos not in self.nodes]


    def _get_existing_neighbors_coords(self, x, y):
        return [pos for pos in self._get_neighbors_coords(x, y) if pos in self.nodes]
    

    def get_places(self):
        return self._playable_dominos


    def add_domino(self, pos_1, pos_2, tiles):
        if pos_1 not in self._get_neighbors_coords(*pos_2):
            raise Exception("invalid domino definition, tiles must be adjacent")
        elif pos_1 in self.nodes or pos_2 in self.nodes:
            raise Exception(f"this place {(pos_1, pos_2)} is already taken")
        elif not self._is_not_overbounded_domino(pos_1, pos_2):
            raise Exception(f"this place {(pos_1, pos_2)} is overbounded")
        elif (pos_1, pos_2) not in self._playable_dominos:
            raise Exception(f"this place {(pos_1, pos_2)} is not connected to an existing domino")
        else:
            self._add_domino(pos_1, pos_2, tiles)


    def _dfs_domain(self, node, visited):
        visited.add(node)
        for neighbor in self._get_existing_neighbors_coords(*node):
            if neighbor not in visited and self.nodes[node].decor == self.nodes[neighbor].decor:
                self._dfs_domain(neighbor, visited)
        return visited
    

    def _find_domains(self):
        to_visit = set(self.nodes)
        domains = []
        while len(to_visit) != 0:
            node = to_visit.pop()
            visited = self._dfs_domain(node, set())
            domain = [self.nodes[n] for n in visited]
            domains.append(domain)
            to_visit -= visited
        return domains
    

    def score(self):
        score = 0 
        for d in self._find_domains():
            score += len(d) * sum([i.crown for i in d])
        return score
        


