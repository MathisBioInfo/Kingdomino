from lib.deck import Deck
from lib.players import BasePlayer
from lib.games import GamesTwoPlayers
from lib.players import GreedyCompactPlayer, GreedyPlayer, DominoNotPlayable, NoMorePlace
from lib.dominos import Decor
import random

def main():
    deck = Deck()
    player_A = GreedyPlayer("P1")
    player_B = GreedyPlayer("P2")
    # Instantiate the game
    game = GamesTwoPlayers(player_A, player_B)
    # Start the game
    game.start_game()
    Decor.legend()

if __name__ == "__main__":
    main()
