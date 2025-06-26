from lib.players import GreedyCompactPlayer, GreedyPlayer
from lib.dominos import Decor
from lib.games import GamesTwoPlayers


def main():
    """Launch a very small two player game."""

    player_a = GreedyPlayer("P1")
    player_b = GreedyPlayer("P2")
    game = GamesTwoPlayers(player_a, player_b)

    scores = game.start_game()
    for p, _ in scores:
        print(p, end="\n\n")

    Decor.legend()

if __name__ == "__main__":
    main()
