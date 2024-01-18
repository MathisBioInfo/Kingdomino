from lib.deck import Deck
import random

class GamesTwoPlayers:
    def __init__(self,player_A,player_B) -> None:
        self.player_A = player_A
        self.player_B = player_B
        self.deck = Deck()
        self.n_round = 0
        self.reserved = {self.player_A:[],self.player_B:[]}
    
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
        for i in range(12):
            self.other_round()
            self.n_round +=1

    def first_round(self,first,second,third,fourth):
        shop = Deck.draw_n(4)
        self.reserved[first].append(first.pick_domino(shop))
        self.reserved[second].append(second.pick_domino(shop))
        self.reserved[third].append(third.pick_domino(shop))
        self.reserved[fourth].append(fourth.pick_domino(shop))




    



