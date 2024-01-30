import gymnasium
from gymnasium import spaces
import numpy as np
from lib.deck import Deck

class MonJeuEnv(gymnasium.Env):
    def __init__(self,deck):
        self.deck = deck # MonJeuEnv(Deck())
        self.action_space = ... # Définir l'espace d'action. Soit pickdomino donc numéro domino à prendre dans la pioche soit play donc coordonné.
        self.pick_action_space = spaces.Discrete(4)  # 4 dominos in the shop
        self.play_space = spaces.Tuple((
            spaces.Discrete(5),  # x coordinate
            spaces.Discrete(5),  # y coordinate
            spaces.Discrete(4)   # orientation
        ))

        self.observation_space = gymnasium.spaces.Box(low=np.array([0, 0]), 
                                        high=np.array([6, 3]), 
                                        shape=(5, 5, 2), 
                                        dtype=np.int32) # Définir l'espace d'observation
        self.observation_space = gymnasium.spaces.Dict({
            "shop": gymnasium.spaces.Box(low=np.array([0,0]), high=np.array([6,3]),shape=(2,4,2)), #peut être sequence ?
            "board_hero": gymnasium.spaces.Box(low=np.array([0,0]), high=np.array([6,3]),shape=(5,5,2)),
            "board_vilain": gymnasium.spaces.Sequence(gymnasium.spaces.Box(low=np.array([0,0]), high=np.array([6,3]),shape=(5,5,2)))

        })

    def step(self, action):
        ... # Appliquer l'action et retourner le résultat
        return observation, reward, done, info

    def reset(self):
        ... # Réinitialiser l'état de l'environnement
        return observation

    def render(self, mode='human'):
        ... # Afficher l'état de l'environnement

    def close(self):
        ... # Nettoyer les ressources
