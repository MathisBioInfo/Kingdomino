from lib.deck import Deck
from lib.players import GreedyCompactPlayer, GameIsEnd
from lib.dominos import Decor


def main():
    deck = Deck()
    ply_1 = GreedyCompactPlayer("P1")

    while True:
        domino = deck.draw()
        try:
            ply_1.play(domino)
        except GameIsEnd:
            print("Plus de place! Fin du Jeu")
            break
        else:
            print(ply_1, end="\n\n")

    Decor.legend()

if __name__ == "__main__":
    main()
