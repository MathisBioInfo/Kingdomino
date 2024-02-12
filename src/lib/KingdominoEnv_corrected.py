import gymnasium as gym
from gymnasium import spaces
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import random


class BasicTilePlacementEnv(gym.Env):
    def __init__(self):
        super(BasicTilePlacementEnv, self).__init__()
        self.board_size = 9
        self.domino_set = self.generate_dominos()  # Example predefined set of dominos
        self.min_x = self.max_x = self.min_y = self.max_y = None  # Initialize boundaries

        self.action_space = spaces.Tuple((
            spaces.Discrete(len(self.domino_set)),  # Domino selection
            spaces.Discrete(self.board_size),       # x1 coordinate
            spaces.Discrete(self.board_size),       # y1 coordinate
            spaces.Discrete(self.board_size),       # x2 coordinate
            spaces.Discrete(self.board_size)        # y2 coordinate
        ))

        # Define the observation space (the state of the board)
        self.observation_space = spaces.Box(low=0, high=7,
                                    shape=(self.board_size, self.board_size),
                                    dtype=int)

        self.state = None  # To keep track of the board state
        
    def generate_dominos(self):
            # Example logic to generate a diverse set of 24 dominos
            # Adjust this logic based on how you want your dominos to be generated
            all_possible_dominos = [(i, j) for i in range(1, 7) for j in range(1, 7)]  # Example domino values
            selected_dominos = random.sample(all_possible_dominos, 12)  # Randomly select 12
            return selected_dominos

    def is_valid_placement(self, start: tuple, start_color: int, end: tuple, end_color: int) -> bool:
        """
        Check if a given domino placement is valid on the game board.

        Args:
            start (tuple): The coordinates of the starting cell for the domino.
            start_color (int): The color of the starting cell.
            end (tuple): The coordinates of the ending cell for the domino.
            end_color (int): The color of the ending cell.

        Returns:
            bool: True if the domino placement is valid, False otherwise.
        """
        allowable_min_x, allowable_max_x, allowable_min_y, allowable_max_y = self.calculate_allowable_area()

        # Check if start and end positions are within the allowable 5x5 area
        if not (allowable_min_x <= start[0] <= allowable_max_x and allowable_min_y <= start[1] <= allowable_max_y and
                allowable_min_x <= end[0] <= allowable_max_x and allowable_min_y <= end[1] <= allowable_max_y):
            return False
    
        # Check for out-of-bounds
        if not (0 <= start[0] < self.board_size and 0 <= start[1] < self.board_size and
                0 <= end[0] < self.board_size and 0 <= end[1] < self.board_size):
            return False

        # Check if either end is already occupied
        if self.state[start[0]][start[1]] != 0 or self.state[end[0]][end[1]] != 0:
            return False

        # Ensure the domino is placed either horizontally or vertically adjacent
        if not (start[0] == end[0] and abs(start[1] - end[1]) == 1 or
                start[1] == end[1] and abs(start[0] - end[0]) == 1):
            return False

        def check_adjacent_matching_color(position: tuple, color: int) -> bool:
            """
            Check if any adjacent cell matches the given color.

            Args:
                position (tuple): The coordinates of the cell to check.
                color (int): The color to match.

            Returns:
                bool: True if an adjacent cell matches the color, False otherwise.
            """
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_x, adj_y = position[0] + dx, position[1] + dy
                if 0 <= adj_x < self.board_size and 0 <= adj_y < self.board_size:
                    # Check if the adjacent cell matches the color
                    if self.state[adj_x][adj_y] == color or self.state[adj_x][adj_y] == 7:
                        return True
            return False

        start_matching = check_adjacent_matching_color(start, start_color)
        end_matching = check_adjacent_matching_color(end, end_color)

        # At least one end of the domino must match an adjacent color
        if not start_matching and not end_matching:
            return False  # Neither end has a matching adjacent color

        return True
    
    def get_valid_moves(self, domino_index: int) -> List[Tuple[int, int, int, int]]:
        """
        Calculate all valid moves for the given domino.

        Args:
            domino_index (int): Index of the domino to check.

        Returns:
            List of tuples representing valid moves (x1, y1, x2, y2).
        """
        valid_moves = []
        start_color, end_color = self.domino_set[domino_index]
        for x1 in range(self.board_size):
            for y1 in range(self.board_size):
                for (dx, dy) in [(0, 1), (1, 0)]:  # Horizontal or vertical placement
                    x2, y2 = x1 + dx, y1 + dy
                    if self.is_valid_placement((x1, y1), start_color, (x2, y2), end_color):
                        valid_moves.append((x1, y1, x2, y2))
        return valid_moves


    def check_game_over(self) -> bool:
        """
        Check if the game is over by determining if there valid moves remaining.

        Returns:
            A boolean value indicating whether the game is over or not.
        """
        print(self.domino_set)
        if not self.domino_set:  # Check if the domino set is empty
            return True
        
        # Check if there are any valid moves remaining
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] == 0:
                    # Check the adjacent cells (above, below, left, right)
                    if any(self.state[x][y] == 0 for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if 0 <= x < len(self.state) and 0 <= y < len(self.state[0])):
                        return False

        # If there are no empty spaces and no valid moves, the game is over
        return True
    def update_extremities(self, x: int, y: int) -> None:
        """
        Update the minimum and maximum x and y coordinates of the game board based on the given x and y values.

        Args:
            x (int): The x coordinate of a cell on the game board.
            y (int): The y coordinate of a cell on the game board.

        Returns:
            None. The method updates the minimum and maximum x and y coordinates of the game board.
        """
        if self.min_x is None or x < self.min_x:
            self.min_x = x
        if self.max_x is None or x > self.max_x:
            self.max_x = x
        if self.min_y is None or y < self.min_y:
            self.min_y = y
        if self.max_y is None or y > self.max_y:
            self.max_y = y
            
    def calculate_allowable_area(self) -> Tuple[int, int, int, int]:
        """
        Calculates the allowable area on the game board where the next domino can be placed based on the current state of the board.

        Returns:
            Tuple[int, int, int, int]: The potential minimum and maximum x and y coordinates that define the allowable area on the game board.
        """
        if self.min_x is None:
            return 2, 6, 2, 6

        potential_min_x = max(0, self.min_x - (4 - (self.max_x - self.min_x)))
        potential_max_x = min(8, self.max_x + (4 - (self.max_x - self.min_x)))
        potential_min_y = max(0, self.min_y - (4 - (self.max_y - self.min_y)))
        potential_max_y = min(8, self.max_y + (4 - (self.max_y - self.min_y)))

        potential_min_x = min(potential_min_x, potential_max_x - 4)
        potential_min_y = min(potential_min_y, potential_max_y - 4)
        potential_max_x = max(potential_max_x, potential_min_x + 4)
        potential_max_y = max(potential_max_y, potential_min_y + 4)

        return potential_min_x, potential_max_x, potential_min_y, potential_max_y


    
    def step(self, action):
        """
        Takes an action and updates the state of the environment accordingly.

        Args:
            action (tuple): A tuple representing the action to be taken. It consists of the index of the selected domino, and the coordinates of the two cells where the domino will be placed.

        Returns:
            tuple: The updated state of the environment after taking the action, the reward obtained from taking the action, a boolean flag indicating whether the game is done, and additional information about the step.
        """
        if not self.domino_set:
            # If there are no dominos left, the game is over.
            return self.state, 0, True, {"reason": "No more dominos to place"}
        
        domino_index = random.randint(0, len(self.domino_set) - 1)
        if domino_index >= len(self.domino_set):
            return self.state, -1, False, {"reason": "Invalid domino selection"}

        selected_domino = self.domino_set[domino_index]
        valid_moves = self.get_valid_moves(domino_index)

        if not valid_moves:
            self.domino_set.pop(domino_index)
            return self.state, 0, False, {"reason": "No valid moves, passing to the next domino"}

        selected_move = random.choice(valid_moves)
        x1, y1, x2, y2 = selected_move
        self.update_extremities(x1, y1)
        self.update_extremities(x2, y2)
        self.state[x1][y1], self.state[x2][y2] = selected_domino
        self.domino_set.pop(domino_index)

        done = len(self.domino_set) == 0
        reward = 1
        info = {}

        return self.state, reward, done, info

    def reset(self) -> List[List[int]]:
        """
        Reset the environment to its initial state.

        Returns:
            The initial state of the environment, represented as a 2D list of integers.
        """
        self.state = [[0] * self.board_size for _ in range(self.board_size)]
        center = self.board_size // 2
        self.state[center][center] = 7
        return self.state

    

    def render(self, mode: str = 'human') -> None:
        """
        Visualizes the current state of the game board using matplotlib.

        Args:
            mode (str, optional): The rendering mode. Default is 'human'.

        Returns:
            None
        """
        fig, ax = plt.subplots()
        ax.set_xlim(0, self.board_size)
        ax.set_ylim(0, self.board_size)
        ax.set_xticks(np.arange(0, self.board_size, 1))
        ax.set_yticks(np.arange(0, self.board_size, 1))

        # Draw gridlines
        ax.grid(which='both', color='k', linestyle='-', linewidth=1)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Define a color map for the tiles, including the special tile
        color_map = {
            0: 'white',  # Empty
            1: 'red',    # Color 1
            2: 'green',  # Color 2
            3: 'blue',   # Color 3
            4: 'yellow', # Color 4
            5: 'purple', # Color 5
            6: 'orange', # Color 6
            7: 'pink',   # Color 7
        }
        # Fill in tiles with corresponding colors
        for x in range(self.board_size):
            for y in range(self.board_size):
                tile_value = self.state[x][y]
                tile_color = color_map.get(tile_value, 'white')
                ax.add_patch(plt.Rectangle((y, self.board_size - x - 1), 1, 1, fill=True, color=tile_color))

        plt.show()

def test_environment(env_class, number_of_episodes):
    """
    Test the given environment by running a specified number of episodes.
    
    Parameters:
    - env_class: The environment class to be tested.
    - number_of_episodes: The number of episodes to run.
    """
    for episode in range(number_of_episodes):
        print(f"Starting episode {episode+1}")
        env = env_class()  # Initialize the environment
        env.reset()
        done = False
        number_of_steps = 0
        while not done:
            action = env.action_space.sample()  # Randomly sample an action
            state, reward, done, info = env.step(action)
            number_of_steps += 1
            if done:
                print(f"Board filled or game over in episode {episode+1}, resetting after {number_of_steps} steps.")
        env.render()  # Render the final state of the environment

# Example usage
test_environment(BasicTilePlacementEnv, 2)