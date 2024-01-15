


def cartesian_product(l1, l2):
    prod = []
    for i in l1:
        prod.extend([(i, j) for j in l2])
    return prod

class Grid: 
    def __init__(self, limit_x, limit_y):
        self.limit_x = limit_x
        self.limit_y = limit_y
        self.grid = {(0, 0)}
        #self.grid = {(0, 0), (0, -1), (1, 0)}

    def __repr__(self):
        repr = []
        for node in self.grid:
            neighbors = [k for k, v in self.get_neighbors(*node).items() if v]
            repr.append(f'{node}\t->\t{neighbors.__str__().rstrip("]").lstrip("[")}')
        return '\n'.join(repr)

    # A refaire: je veux une fonction qui à l'ajout d'un node dans la grid, 
    # la place 
    #
    # def _add_node(self, nd):
    #     if self._check_not_overbounded_node(*nd):
    #         x, y = nd

    # a refaire : je veux une fonction qui retourne les contraines

    # def _calc_constraint(self):
    #     return {
    #         'min_x': 
    #     }


    
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
    


    # a refaire : appelle la fonction qui calcul les nouvelles contraines 
    #               et verifie que le nd passé en parametre ne les dépassent pas ! 
    # def _check_not_overbounded_node(self, x, y):   
    #     return x < self.limit_x and x > (-self.limit_x) and \
    #             y < self.limit_y and y > (-self.limit_y) 
    
    def _remove_overbounded_pairs(self, flipped_pairs): 
        passed = []
        for nd1, nd2 in flipped_pairs:
           if self._check_not_overbounded_node(*nd1) and self._check_not_overbounded_node(*nd2):
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
