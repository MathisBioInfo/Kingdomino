from lib.deck import Deck
from lib.players import BasePlayer
import random

class GamesTwoPlayers:
    def __init__(self,player_A,player_B) -> None:
        self.player_A = player_A
        self.player_B = player_B
        self.deck = Deck()
        self.n_round = 0
        self.reserved = []
    
    def start_game(self):
        players = [self.player_A, self.player_B]
        random.shuffle(players)
        turn_order = players + players[::-1]  # [first, second, second, first]
        
        self.first_round(turn_order)
        self.n_round += 1
        for i in range(11):
            self.other_round()
            self.n_round +=1
        self.last_round()
        self.final_score()

    def first_round(self,turn_order):
        shop = self.deck.draw_n(4)
        self.reserved = []
        for player in turn_order:
            self.reserved.append((player, player.pick_domino(shop)))

    def other_round(self):
        shop = self.deck.draw_n(4)
        for player, domino in self.define_running_order():
            self.reserved.append((player,player.pick_domino(shop)))
            player.play(domino)
    
    def last_round(self):
        for player, domino in self.define_running_order():
            player.play(domino)


    def define_running_order(self):
        running_order = sorted(self.reserved, key=lambda x: x[1][0].dom_id)
        self.reserved = []
        return running_order
    
    def final_score(self):
        raise NotImplementedError("à faire")

        




    



