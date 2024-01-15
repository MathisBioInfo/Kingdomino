from sys import stderr
from typing import NamedTuple

from src.lib.utilsfunc import cartesian_product


class Box(NamedTuple):
    max_x: int
    min_x: int
    max_y: int
    min_y: int


class Grid:
    def __init__(self, limit_x, limit_y):
        self.init_limits = Box(limit_x, -limit_x, limit_y, -limit_y)
        self.limits = Box(limit_x, -limit_x, limit_y, -limit_y)
        self.grid = {(0, 0)}
        #self.tiles_grid ?

    def __repr__(self):
        return self._pretty_repr()

    def _adj_repr(self):
        repr = []
        for node in self.grid:
            neighbors = [k for k, v in self.get_neighbors(*node).items() if v]
            repr.append(f"{node}\t->\t{neighbors.__str__().rstrip(']').lstrip('[')}")
        return "\n".join(repr)

    def _pretty_repr(self):
        repr = ["\n"]
        x_range = range(self.limits.min_x, self.limits.max_x+1)
        x_range_2 = range(self.limits.min_x, self.limits.max_x+1)
        y_range = range(self.limits.max_y, self.limits.min_y-1, -1)
        for iy in y_range:
            repr.append(f"{iy:^3}   ")
            for ix in x_range:
                if self._is_not_overbounded_node(ix, iy):
                    if ix == 0 and iy == 0:
                        repr.append(" O ")
                    elif (ix, iy) in self.grid:
                        repr.append(" # ")
                    else:
                        repr.append(" . ")
                else:
                    repr.append(" X ")
            repr.append("\n")
        repr.append("\n      ")
        repr.extend([f"{x:^3}" for x in x_range_2])
        repr.append("\n")
        return "".join(repr)
    
    def _pretty_repr_domino(self):
        ...
    
    def _pretty_repr_content(self):
        ...

    def _max_x(self):
        return max([x for x, _ in self.grid])

    def _min_x(self):
        return min([x for x, _ in self.grid])

    def _max_y(self):
        return max([y for _, y in self.grid])

    def _min_y(self):
        return min([y for _, y in self.grid])

    def _update_limits(self):
        self.limits = Box(
            self.init_limits.max_x + self._min_x(),
            self.init_limits.min_x + self._max_x(),
            self.init_limits.max_y + self._min_y(),
            self.init_limits.min_y + self._max_y(),
        )

    def _add_node(self, x, y):
        if self._is_not_overbounded_node(x, y) and (x, y) not in self.grid:
            self.grid.add((x, y))
            self._update_limits()
        else:
            print("Le noeud n\'a pas été ajouté", file=stderr)

    def _is_not_overbounded_node(self, x, y):
        return (
            x > self.limits.min_x and
            x < self.limits.max_x and
            y > self.limits.min_y and
            y < self.limits.max_y
        )

    def get_neighbors(self, x, y):
        return {
            (x+1, y): True if (x+1, y) in self.grid else False,
            (x, y+1): True if (x, y+1) in self.grid else False,
            (x-1, y): True if (x-1, y) in self.grid else False,
            (x, y-1): True if (x, y-1) in self.grid else False
        }

    def _find_free_places(self):
        places = set()
        for node in self.grid:
            for coord, exist in self.get_neighbors(*node).items():
                if not exist:
                    places.add(coord)
        return list(places)

    def _extend_free_places(self, places):
        extended = []
        for p in places:
            ext = self.get_neighbors(*p)
            valid_ext = [k for k, v in ext.items() if not v]
            extended.append((p, valid_ext))
        return extended

    def _build_node_pairs(self, ext_places):
        pairs = []
        for p, ext_p in ext_places:
            pairs.extend(cartesian_product([p], ext_p))
        return pairs

    def _remove_overbounded_pairs(self, flipped_pairs):
        passed = []
        for nd1, nd2 in flipped_pairs:
           if self._is_not_overbounded_node(*nd1) and self._is_not_overbounded_node(*nd2):
               passed.append((nd1, nd2))
        return passed

    def _add_flipped_nodes_pairs(self, pairs):
        flipped_pairs = []
        for nd1, nd2 in pairs:
            flipped_pairs.append((nd1, nd2))
            flipped_pairs.append((nd2, nd1))
        return list(set(flipped_pairs))

    def get_candidates(self):
        places = self._find_free_places()
        ext_places = self._extend_free_places(places)
        pairs = self._build_node_pairs(ext_places)
        valid_pairs = self._remove_overbounded_pairs(pairs)
        candidates = self._add_flipped_nodes_pairs(valid_pairs)
        return candidates
    
    def _score(self, grid): #return score of "grid"
        ...
    
    def score(self): #return score interface
        return self._score(self.grid)
