from abc import ABC, abstractmethod
from random import shuffle

from lib.board import GameBoard


class NoMorePlace(Exception):
    pass


class DominoNotPlayable(Exception):
    pass


class BasePlayer(ABC):
    def __init__(self, name):
        self.name = name
        self.board = GameBoard(5, 5)
        self.score = 0
        self.last_dom = None
        self.tour = 0


    def __repr__(self):
        return f"\nplayer:{self.name} tour:{self.tour} score:{self.score} domino:{self.last_dom}\n{self.board}"


    @abstractmethod
    def _best_move(self, domino):
        pass


    @abstractmethod
    def _strategy_score(self, board):
        pass


    def _domino_checker(self, domino):
        if len(self.board._playable_dominos) == 0:
            raise NoMorePlace("Plus de place :(")

        if len(self.board.get_places(domino)) == 0:
            raise DominoNotPlayable("Pas compatible")
        
    def pick_domino(self, shop):
        raise NotImplementedError("mécanique choix domino dans le shop à stocker dans reserved, voir dans games.py")


    def play(self, domino):
        self.tour += 1
        self.last_dom = domino
        best = self._best_move(domino)
        self.board.add_domino(*best, domino)
        self.score = self.board.score()



class GreedyPlayer(BasePlayer):
    def _best_move(self, domino):
        self._domino_checker(domino)

        places = self.board.get_places(domino)

        simulations = []
        for pl in places:
            board_copy = self.board.copy()
            board_copy.add_domino(*pl, domino)
            simulations.append((pl, self._strategy_score(board_copy)))
        simulations.sort(key=lambda x: x[1]["domains"])

        return simulations[0][0]


    def _strategy_score(self, board):
        return {"domains": len(board._find_domains())}



class GreedyCompactPlayer(BasePlayer):
    def _best_move(self, domino):
        self._domino_checker(domino)

        places = self.board.get_places(domino)

        simulations = []
        for pl in places:
            board_copy = self.board.copy()
            board_copy.add_domino(*pl, domino)
            simulations.append((pl, self._strategy_score(board_copy)))
        simulations.sort(key=lambda x: (x[1]["domains"], x[1]["area"]))

        return simulations[0][0]


    def _strategy_score(self, board: GameBoard):
        return {
            "domains": len(board._find_domains()),
            "area": (
                (board._get_max_x() - board._get_min_x() + 1)
                * (board._get_max_y() - board._get_min_y() + 1)
            )
        }


class GreedyPerimeterPlayer(BasePlayer):
    def _best_move(self, domino):
        self._domino_checker(domino)

        places = self.board.get_places(domino)

        simulations = []
        for pl in places:
            board_copy = self.board.copy()
            board_copy.add_domino(*pl, domino)
            simulations.append((pl, self._strategy_score(board_copy)))
        simulations.sort(key=lambda x: (x[1]["domains"], x[1]["perimeter"]))

        return simulations[0][0]


    def _strategy_score(self, board: GameBoard):
        return {
            "domains": len(board._find_domains()),
            "perimeter": board._get_perimeter()
        }


class StupidPlayer(BasePlayer):
    def _best_move(self, domino):
        self._domino_checker(domino)

        places = self.board.get_places(domino)

        shuffle(places)
        return places[0]


    def _strategy_score(self, board):
        pass