from lib.deck import Deck
from lib.players import BasePlayer
import random

class GamesTwoPlayers:
    def __init__(self,player_A,player_B) -> None:
        self.player_A = player_A
        self.player_B = player_B
        self.deck = Deck()
        self.n_round = 0
        self.reserved = {self.player_A:[],self.player_B:[]}
        self.reserved = []
    
    def start_game(self):
        if random('A','B') == 'A':
            first = self.player_A
            second = self.player_B
            third = self.player_B
            fourth = self.player_A
        else :
            first = self.player_B
            second = self.player_A
            third = self.player_A
            fourth = self.player_B
        
        self.first_round(first,second,third,fourth)
        self.n_round += 1
        for i in range(11):
            self.other_round()
            self.n_round +=1
        self.last_round()
        self.final_score()

    def first_round(self,first,second,third,fourth):
        shop = self.deck.draw_n(4)
        self.reserved = []
        self.reserved.append((first, first.pick_domino(shop)))
        self.reserved.append((second, second.pick_domino(shop)))
        self.reserved.append((third, third.pick_domino(shop)))
        self.reserved.append((fourth, fourth.pick_domino(shop)))

    def other_round(self):
        shop = self.deck.draw_n(4)
        for player, domino in self.define_running_order():
            self.reserved.append((player,player.pick_domino(shop)))
            player.play(domino)
    
    def last_round(self):
        for player, domino in self.define_running_order():
            player.play(domino)


    def define_running_order(self):
        running_order = sorted(self.reserved, lambda x: x[1][0].dom_id)
        self.reserved = []
        return running_order
    
    def final_score(self):
        raise NotImplementedError("à faire")

        




    



