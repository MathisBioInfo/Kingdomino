from random import shuffle
from sys import stderr

from src.lib.tiles import TILES


class Deck:
    def __init__(self):
        self.deck = TILES.copy()
        shuffle(self.deck)
        self.remain = len(TILES)

    def draw(self):
        if self.remain > 0:
            self.remain -= 1
            return self.deck.pop()
        else:
            print("Le deck est vide", file=stderr)

    def draw_n(self, n):
        doms = []
        for i in range(n):
            dom = self.draw()
            if dom is None:
                return doms
            doms.append(dom)
        return doms

    def reset(self):
        self.deck = TILES.copy()
        shuffle(self.deck)
        self.remain = len(TILES)
