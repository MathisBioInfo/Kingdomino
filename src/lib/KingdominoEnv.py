import gymnasium as gym
from gymnasium import spaces
import matplotlib.pyplot as plt
import numpy as np

class BasicTilePlacementEnv(gym.Env):
    def __init__(self):
        super(BasicTilePlacementEnv, self).__init__()
        self.board_size = 5  # Define the board size
        self.domino_set = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,3)]  # Example predefined set of dominos
        # Define the action space (x, y coordinates for tile placement)
        # Update the action space to include tile color (1-4)
        self.action_space = spaces.Tuple((
            spaces.Discrete(len(self.domino_set)),  # Selecting a domino
            spaces.Discrete(self.board_size),  # x coordinate
            spaces.Discrete(self.board_size),  # y coordinate
            spaces.Discrete(4),                # orientation (up, down, left, right)
        ))

        # Define the observation space (the state of the board)
        self.observation_space = spaces.Box(low=0, high=5,
                                    shape=(self.board_size, self.board_size),
                                    dtype=int)

        self.state = None  # To keep track of the board state

    def is_valid_placement(self, start, direction, tile_color):
        # Assume tile_color parameter is passed, indicating the color of the domino being placed.
        # Calculate the second tile's position based on direction
        if direction == 'up':
            end = (start[0] - 1, start[1])
        elif direction == 'down':
            end = (start[0] + 1, start[1])
        elif direction == 'left':
            end = (start[0], start[1] - 1)
        elif direction == 'right':
            end = (start[0], start[1] + 1)
        else:
            return False  # Invalid direction

        # Check for out-of-bounds or overlapping tiles
        if not (0 <= end[0] < self.board_size and 0 <= end[1] < self.board_size):
            return False
        if self.state[start[0]][start[1]] != 0 or self.state[end[0]][end[1]] != 0:
            return False

        # Adjust the touching check for color or special tile
        touching = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_cell = (start[0] + dx, start[1] + dy)
            if 0 <= adj_cell[0] < self.board_size and 0 <= adj_cell[1] < self.board_size:
                if self.state[adj_cell[0]][adj_cell[1]] == tile_color or self.state[adj_cell[0]][adj_cell[1]] == 5:
                    touching = True
        if not touching:
            return False

        return True


    def check_game_over(self):
    # Vérifie s'il reste des cases vides
    #for row in self.state:
        #if 0 in row:
            #return False

        # Vérifie s'il existe encore des mouvements valides
        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if self.state[i][j] == 0:
                    # Vérifie les cases adjacentes (haut, bas, gauche, droite)
                    if (i > 0 and self.state[i - 1][j] == 0) or \
                       (i < len(self.state) - 1 and self.state[i + 1][j] == 0) or \
                       (j > 0 and self.state[i][j - 1] == 0) or \
                       (j < len(self.state[0]) - 1 and self.state[i][j + 1] == 0):
                        return False

        # Si aucune case vide n'est trouvée et aucun mouvement valide n'est possible, le jeu est terminé
        return True
    
    def step(self, action):
        # Decode the action into position (x, y), orientation, and tile color
        domino_index, x, y, orientation = action
        directions = ['up', 'down', 'left', 'right']
        direction = directions[orientation]
        
        # Check if the selected domino is valid (not already placed)
        if domino_index >= len(self.domino_set):
            return self.state, -1, False, {"reason": "Invalid domino selection"}

        selected_domino = self.domino_set[domino_index]
        tile_color = selected_domino[0]

        # Check if the placement is valid with the added tile color
        if not self.is_valid_placement((x, y), direction, tile_color):
            # Penalize invalid moves to discourage them
            return self.state, -1, False, {"reason": "Invalid placement"}

        # Calculate the second tile's position based on the direction
        second_tile = {
            'up': (x - 1, y),
            'down': (x + 1, y),
            'left': (x, y - 1),
            'right': (x, y + 1)
        }[direction]

        # Place the domino on the board with its color
        self.state[x][y] = selected_domino[0]
        self.state[second_tile[0]][second_tile[1]] = selected_domino[1]

        # Check if the game is done
        done = self.check_game_over()

        # Define the reward mechanism; simple example: +1 for each successful move
        reward = 1

        # Optionally, provide additional info about the step
        info = {}

        return self.state, reward, done, info




    def reset(self):
        # Reset the environment to an initial state
        self.state = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Set the center position to 1
        center_row = self.board_size // 2
        center_col = self.board_size // 2
        self.state[center_row][center_col] = 5

        return self.state  # Return the initial state

    

    def render(self, mode='human'):
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
            5: 'purple'  # Special tile
        }

        # Fill in tiles with corresponding colors
        for x in range(self.board_size):
            for y in range(self.board_size):
                tile_value = self.state[x][y]
                tile_color = color_map[tile_value]
                ax.add_patch(plt.Rectangle((y, self.board_size - x - 1), 1, 1, fill=True, color=tile_color))

        plt.show()

