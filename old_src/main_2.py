from lib.deck import Deck
from lib.players import BasePlayer
#from lib.games import GamesTwoPlayers
from lib.games_2 import KingdominoGame
from lib.players_2 import GreedyCompactPlayer, GreedyPlayer, DominoNotPlayable, NoMorePlace
from lib.dominos import Decor
import random

def main():
    deck = Deck()
    player_A = GreedyPlayer("P1")
    player_B = GreedyPlayer("P2")
    player_C = GreedyPlayer("P3")
    player_D = GreedyPlayer("P4")
    players = [player_A,player_B,player_C,player_D]
    # Instantiate the game
    game = KingdominoGame(players)
    # Start the game
    game.start_game()
    Decor.legend()

if __name__ == "__main__":
    main()
