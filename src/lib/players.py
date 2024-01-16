from abc import ABC, abstractmethod
from random import shuffle

from lib.board import GameBoard


class BasePlayer(ABC):
    def __init__(self, name):
        self.name = name
        self.board = GameBoard(5, 5)
        self.score = 0
        self.last_dom = None
        self.tour = 0


    def __repr__(self):
        return f"\nplayer {self.name} tour {self.tour}: score={self.score} domino={self.last_dom}\n{self.board}"


    @abstractmethod
    def _simulation(self, domino):
        pass


    @abstractmethod
    def _strategy_score(self, board):
        pass


    def play(self, domino):
        simulations = self._simulation(domino)
        self.board.add_domino(*simulations[0][0], domino)
        self.score = self.board.score()
        self.last_dom = domino
        self.tour += 1



class GreedyPlayer(BasePlayer):
    def _simulation(self, domino):
        places = self.board.get_places()
        if len(places) == 0:
            raise Exception("No move is possible, end game")

        simulations = []
        for pl in places:
            board_copy = self.board.copy()
            board_copy.add_domino(*pl, domino)
            simulations.append((pl, self._strategy_score(board_copy)))

        return sorted(simulations, key=lambda x: x[1])


    def _strategy_score(self, board):
        return len(board._find_domains())
    


# class GreedyPlayer2(BasePlayer):
#     def _simulation(self, domino):
#         places = self.board.get_places()
#         if len(places) == 0:
#             raise Exception("No move is possible, end game")

#         simulations = []
#         for pl in places:
#             board_copy = self.board.copy()
#             board_copy.add_domino(*pl, domino)
#             simulations.append((pl, self._strategy_score(board_copy)))

#         return sorted(simulations, key=lambda x: x[1])


#     def _strategy_score(self, board):
#         return len(board._find_domains())



class StupidPlayer(BasePlayer):
    def _simulation(self, domino):
        places = list(self.board.get_places())
        if len(places) == 0:
            raise Exception("No move is possible, end game")

        shuffle(places)
        simulations = []
        for pl in places:
            simulations.append((pl, 0))

        return simulations


    def _strategy_score(self, board):
        return 0