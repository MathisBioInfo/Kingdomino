from lib.deck import Deck
from lib.players import GreedyCompactPlayer, GreedyPlayer, DominoNotPlayable, NoMorePlace
from lib.dominos import Decor


def main():
    deck = Deck()
    ply_1 = GreedyPlayer("P1")

    for i in range(1, 14):
        domino = deck.draw()
        try:
            ply_1.play(domino)
        except NoMorePlace:
            print(f"Plus de place! tour:{i}")
            continue
        except DominoNotPlayable:
            print(f"Pass your turn! tour:{i} {domino}")
            continue
        else:
            print(ply_1, end="\n\n")

    Decor.legend()

if __name__ == "__main__":
    main()
