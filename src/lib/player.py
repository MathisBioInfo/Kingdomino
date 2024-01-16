from lib.board import GameBoard


class Player:
    def __init__(self, name):
        self.name = name
        self.board = GameBoard(5, 5)
        self.score = 0
        self.last_dom = None
        self.tour = 0

    def __repr__(self):
        return f"\nplayer {self.name} tour {self.tour}: score={self.score} domino={self.last_dom}\n{self.board}"


    def simul_placement(self, domino):
        places = self.board.get_places()
        if len(places) == 0:
            raise Exception("No move is possible, end game")

        simulations = []
        for pl in places:
            board_copy = self.board.copy()
            board_copy.add_domino(*pl, domino)
            simulations.append((pl, board_copy.alter_score()))

        return sorted(simulations, key=lambda x: x[1])


    def play_a_domino(self, pos_1, pos_2, domino):
        self.board.add_domino(pos_1, pos_2, domino)
        self.score = self.board.official_score()
        self.last_dom = domino
