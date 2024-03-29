from random import shuffle
from copy import deepcopy

from lib.dominos import DOMINOS


class Deck:
    def __init__(self):
        self.deck = deepcopy(DOMINOS)
        shuffle(self.deck)
        self.remain = len(DOMINOS)


    def __repr__(self):
        return f"Deck with {self.remain} dominos"


    def draw(self):
        if self.remain > 0:
            self.remain -= 1
            return self.deck.pop()
        else:
            raise Exception("Deck is empty!")


    def draw_n(self, n):
        if n <= self.remain:
            return sorted([self.draw() for _ in range(n)], key=lambda x: x[0].dom_id)
        else:
            raise Exception("Deck does not have enough dominos")
