import numpy as np
import gymnasium as gym
from gymnasium.spaces import Tuple, Box, Discrete

# Define the low and high bounds for a single tile
tile_low = np.array([0, 0])  # Lower bound for a single tile (type, crowns)
tile_high = np.array([6, 3])  # Upper bound for a single tile (type, crowns)

# Function to create a board space
def create_board_space():
    board_low = np.tile(tile_low, (9, 9, 1), dtype=np.uint8)
    board_high = np.tile(tile_high, (9, 9, 1), dtype=np.uint8)
    return Box(low=board_low, high=board_high, dtype=np.uint8)

# Create spaces for your board and opponent boards
your_board_space = create_board_space()

# Create the shop space: 4 dominos, each with 2 tiles, each tile with 2 features
shop_space = Box(low=np.tile(tile_low, (4, 2, 1)), high=np.tile(tile_high, (4, 2, 1)),dtype=np.uint8)

playable_space = Box(low=0,high=1,shape=(9, 9),dtype=np.uint8)

# Combine all spaces into a single observation space
observation_space = Tuple((your_board_space, shop_space, playable_space))

# Define the discrete spaces for each coordinate
position_x1 = Discrete(9)  # X coordinate for tile 1
position_y1 = Discrete(9)  # Y coordinate for tile 1
position_x2 = Discrete(9)  # X coordinate for tile 2
position_y2 = Discrete(9)  # Y coordinate for tile 2
orientation = Discrete(2)

# Define the action space as a tuple of these discrete spaces
play_space = Tuple((position_x1, position_y1, position_x2, position_y2,orientation))

# Example usage in your environment
class KingdominoEnv(gym.Env):
    def __init__(self):
        self.observation_space = observation_space
        self.action_space = play_space
        # ...
    def step(self, action):
        action = self.action_space.sample()
        # ...
        pass

    def reset(self):
        # ...
        pass