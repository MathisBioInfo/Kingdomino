from lib.deck import Deck
from lib.players import BasePlayer,  DominoNotPlayable, NoMorePlace
import random

class KingdominoGame:
    def __init__(self, players) -> None:

        if len(players) < 2 or len(players) > 4:

            raise ValueError("Number of players must be between 2 and 4.")

        self.players = players

        self.deck = Deck()

        self.n_round = 0

        self.reserved = []

    
    def start_game(self):

        self.first_round()
        self.n_round += 1

        for i in range(1,11):
            self.other_round()
            self.n_round +=1
        self.last_round()
        self.n_round +=1
        score = self.final_score()
        print(score)

    def first_round(self):
        print("start first round: \n")
        turn_order = self.define_running_order(self.n_round)
        shop = self.deck.draw_n(len(turn_order))
        self.reserved = []
        for player in turn_order:
            self.reserved.append((player, player.pick_domino(shop)))
        print("end first round \n")

    def other_round(self):
        print("start other round: \n")
        turn_order = self.define_running_order(self.n_round)
        shop = self.deck.draw_n(len(turn_order))
        print(turn_order[1][1])
        for player, domino in turn_order:
            self.reserved.append((player,player.pick_domino(shop)))
            player.play(domino)
            print('TEST')
        print("end other round: \n")
    
    def last_round(self):
        turn_order = self.define_running_order(self.n_round)
        for player, domino in turn_order:
            player.play(domino)
        print("end last_round: \n")
    
    def final_score(self):
        score_list = []
        for player in self.players:
            score_list.append((player,player.score))
        sorted(score_list, key=lambda x: x[1])
        return score_list
    
    def define_running_order(self,n_round):
        if n_round == 0:
            random.shuffle(self.players)
            if len(self.players) == 2:
                running_order = self.players + self.players[::-1]
            else :
                running_order = self.players
        else :
            running_order = sorted(self.reserved, key=lambda x: x[1][0].dom_id)
            self.reserved = []
        return running_order


        




    



