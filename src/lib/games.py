from lib.deck import Deck
from lib.players import BasePlayer
import random

class GamesTwoPlayers:
    def __init__(self,player_A,player_B) -> None:
        self.player_A = player_A
        self.player_B = player_B
        self.players = [self.player_A, self.player_B]
        self.deck = Deck()
        self.n_round = 0
        self.reserved = []
    
    def start_game(self):
        #turn_order = self.determine_turn_order()
        turn_order = self.define_running_order(self.n_round)
        self.first_round(turn_order)
        self.n_round += 1

        for i in range(11):
            self.other_round()
            self.n_round +=1
        self.last_round()
        self.final_score()

    #def determine_turn_order(self): #determine running order for first_round
    #    random.shuffle(self.players)
    #    return self.players + self.players[::-1]  # [first, second, second, first]

    def first_round(self,turn_order):
        print("start first round: \n")
        shop = self.deck.draw_n(2)
        self.reserved = []
        for player in turn_order:
            self.reserved.append((player, player.pick_domino(shop)))
        print("end first round \n")

    def other_round(self):
        print("start other round: \n")
        shop = self.deck.draw_n(2)
        order = self.define_running_order(self.n_round)
        print(f'len order: {len(order)}')
        print(f'order: {order}')
        for player, domino in order:
            self.reserved.append((player,player.pick_domino(shop)))
            player.play(domino)
        print("end other round: \n")
    
    def last_round(self):
        for player, domino in self.define_running_order(self.n_round):
            player.play(domino)


    #def define_running_order(self): #determine the running order for other_round and last_round
    #    running_order = sorted(self.reserved, key=lambda x: x[1][0].dom_id)
    #    self.reserved = []
    #    return running_order
    
    def final_score(self):
        score_list = []
        for player in self.players:
            score_list.append((player,player.score))
        sorted(score_list, key=lambda x: x[1])
        return score_list
    
    def define_running_order(self,n_round):
        if n_round == 0:
            random.shuffle(self.players)
            running_order = self.players #+ self.players[::-1]
        else :
            running_order = sorted(self.reserved, key=lambda x: x[1][0].dom_id)
            self.reserved = []
        return running_order


        




    



