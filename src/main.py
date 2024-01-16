from lib.deck import Deck
from lib.player import Player
from lib.dominos import Decor


def main():
    deck = Deck()
    ply_1 = Player("P1")

    while True:
        domino = deck.draw()
        try:
            simul = ply_1.simul_placement(domino)
        except Exception:
            print("Plus de place! Fin du Jeu")
            break
        else:
            ply_1.play_a_domino(*simul[0][0], domino)
            print(ply_1, end="\n\n")

    Decor.legend()


if __name__ == "__main__":
    main()
