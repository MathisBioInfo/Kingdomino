import itertools
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
                                    shape=(self.board_size, self.board_size, 2),
                                    dtype=np.int32)

        self.state = np.zeros((self.board_size, self.board_size, 2), dtype=np.uint8)
        center = self.board_size // 2
        self.state[center][center] = (7, 0)

    def generate_dominos(self) -> List[Tuple[int, int, int, int]]:
        colors = range(1, 7)
        crown_values = range(2)
        all_possible_dominos = list(itertools.product(colors, crown_values, repeat=2))
        selected_dominos = random.sample(all_possible_dominos, 12)
        return selected_dominos

    def is_valid_placement(self, start: tuple, start_color: int, end: tuple, end_color: int) -> bool:
        (allowable_min_x, allowable_max_x, allowable_min_y, allowable_max_y) = self.calculate_allowable_area()
        if not self._is_within_allowable_area(start, end, allowable_min_x, allowable_max_x, allowable_min_y, allowable_max_y):
            return False
        if not self._is_within_board(start, end):
            return False
        if not self._is_empty_tile(start, end):
            return False
        if not self._is_adjacent(start, end):
            return False
        if not self._has_matching_color(start, start_color) and not self._has_matching_color(end, end_color):
            return False
        return True

    def _is_within_allowable_area(self, start: tuple, end: tuple, min_x: int, max_x: int, min_y: int, max_y: int) -> bool:
        return min_x <= start[0] <= max_x and min_y <= start[1] <= max_y and min_x <= end[0] <= max_x and min_y <= end[1] <= max_y

    def _is_within_board(self, start: tuple, end: tuple) -> bool:
        return 0 <= start[0] < self.board_size and 0 <= start[1] < self.board_size and 0 <= end[0] < self.board_size and 0 <= end[1] < self.board_size

    def _is_empty_tile(self, start: tuple, end: tuple) -> bool:
        return self.state[start[0]][start[1]][0] == 0 and self.state[end[0]][end[1]][0] == 0

    def _is_adjacent(self, start: tuple, end: tuple) -> bool:
        return start[0] == end[0] and abs(start[1] - end[1]) == 1 or start[1] == end[1] and abs(start[0] - end[0]) == 1

    def _has_matching_color(self, position: tuple, color: int) -> bool:
        for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            (adj_x, adj_y) = (position[0] + dx, position[1] + dy)
            if 0 <= adj_x < self.board_size and 0 <= adj_y < self.board_size:
                (adj_tile_color, _) = self.state[adj_x][adj_y]
                if adj_tile_color == color or adj_tile_color == 7:
                    return True
        return False

    def get_valid_moves(self, domino_index: int) -> List[Tuple[int, int, int, int]]:
        valid_moves = []
        start_color, start_crowns, end_color, end_crowns = self.domino_set[domino_index]

        for x1 in range(self.board_size):
            for y1 in range(self.board_size):
                for dx, dy in [(0, 1), (1, 0)]:
                    x2, y2 = x1 + dx, y1 + dy
                    if self.is_valid_placement((x1, y1), start_color, (x2, y2), end_color):
                        valid_moves.append((x1, y1, x2, y2))

        return valid_moves

    def check_game_over(self) -> bool:
        if not self.domino_set:
            return True

        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j][0] == 0:
                    if any(self.state[x][y][0] == 0 for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)] if 0 <= x < len(self.state) and 0 <= y < len(self.state[0])):
                        return False

        return True

    def update_extremities(self, x: int, y: int) -> None:
        if self.min_x is None or x < self.min_x:
            self.min_x = x
        if self.max_x is None or x > self.max_x:
            self.max_x = x
        if self.min_y is None or y < self.min_y:
            self.min_y = y
        if self.max_y is None or y > self.max_y:
            self.max_y = y

    def calculate_allowable_area(self) -> Tuple[int, int, int, int]:
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
    
    def calculate_score(self):
        visited = np.zeros_like(self.state[...,0], dtype=bool)  # Track visited tiles
        score = 0
        for x in range(self.board_size):
            for y in range(self.board_size):
                if not visited[x, y] and self.state[x, y, 0] > 0:  # Tile has color and is not visited
                    domain_score, domain_size = self._explore_domain(x, y, visited)
                    score += domain_score * domain_size

        # Apply bonus points for Middle Kingdom and Harmony rules if applicable
        if self._is_middle_kingdom():
            score += 10
            print("This board respect the middle kingdom !")
        if self._is_harmony():
            score += 5
            print("This board respect the harmony !")

        return score

    def _explore_domain(self, x, y, visited):
        """
        Explore connected tiles of the same color to calculate the domain's score.

        Args:
            x, y (int): Coordinates of the starting tile for the domain.
            visited (2D array): A boolean array indicating whether a tile has been visited.

        Returns:
            tuple: The total score for the domain and the number of tiles in the domain.
        """
        # Stack for DFS
        stack = [(x, y)]
        domain_score = 0
        domain_size = 0
        color = self.state[x, y, 0]

        while stack:
            x, y = stack.pop()
            if visited[x, y]:
                continue

            visited[x, y] = True
            domain_size += 1
            domain_score += self.state[x, y, 1]  # Add the number of crowns in the tile to the domain score

            # Check adjacent tiles (N, S, E, W) for the same color and if they are part of the domain
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size and not visited[nx, ny] and self.state[nx, ny, 0] == color:
                    stack.append((nx, ny))

        return domain_score, domain_size

    def _is_middle_kingdom(self):
        if self.calculate_allowable_area() == (2, 6, 2, 6):
            return True
        # Assuming the castle or special tile is marked with a specific color/code, e.g., 7
        # and that the central tile having this specific tile indicates Middle Kingdom rule satisfaction
        return False


    def _is_harmony(self):
        # Assuming self.state indicates tile presence with a color code > 0
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                if self.state[x][y][0] == 0:  # If any tile within the boundaries is empty
                    return False
        return True

    def step(self, action):
        if not self.domino_set:
            return self.state, 0, True, {"reason": "No more dominos to place"}

        domino_index = np.random.randint(0, len(self.domino_set))
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
        color1, crowns1, color2, crowns2 = selected_domino
        self.state[x1][y1] = (color1, crowns1)
        self.state[x2][y2] = (color2, crowns2)
        self.domino_set.pop(domino_index)

        observation = self.state

        done = len(self.domino_set) == 0
        reward = 1
        info = {}

        return observation, reward, done, info

    def reset(self) -> List[List[int]]:
        self.state = np.zeros((self.board_size, self.board_size, 2), dtype=np.uint8)
        center = self.board_size // 2
        self.state[center][center] = (7, 0)
        return self.state

    def render(self, mode='human'):
        color_map = {
            0: 'white',
            1: 'red',
            2: 'green',
            3: 'blue',
            4: 'yellow',
            5: 'purple',
            6: 'orange',
            7: 'pink',
        }

        crown_text_map = {0: '', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '0'}

        fig, ax = plt.subplots()
        ax.set_xlim(0, self.board_size)
        ax.set_ylim(0, self.board_size)
        ax.grid(which='both', color='k', linestyle='-', linewidth=1)
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        for x in range(self.board_size):
            for y in range(self.board_size):
                (tile_value, crown_value) = self.state[x][y]
                tile_color = color_map.get(tile_value, 'white')
                ax.add_patch(plt.Rectangle((y, self.board_size - x - 1), 1, 1, fill=True, color=tile_color))
                if tile_value > 0:
                    ax.text(y + 0.5, self.board_size - x - 0.5, crown_text_map[crown_value], ha='center', va='center')

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
        score = env.calculate_score()
        print(f"Calculated Score = {score}")
    #return env.state

# Example usage
test_environment(BasicTilePlacementEnv, 10)