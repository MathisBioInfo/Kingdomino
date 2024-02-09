import gymnasium as gym
from gymnasium import spaces
import matplotlib.pyplot as plt
import numpy as np

class BasicTilePlacementEnv(gym.Env):
    def __init__(self):
        super(BasicTilePlacementEnv, self).__init__()
        self.board_size = 5
        self.domino_set = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,3)]  # Example predefined set of dominos

        self.action_space = spaces.Tuple((
            spaces.Discrete(len(self.domino_set)),  # Domino selection
            spaces.Discrete(self.board_size),       # x1 coordinate
            spaces.Discrete(self.board_size),       # y1 coordinate
            spaces.Discrete(self.board_size),       # x2 coordinate
            spaces.Discrete(self.board_size)        # y2 coordinate
        ))

        # Define the observation space (the state of the board)
        self.observation_space = spaces.Box(low=0, high=5,
                                    shape=(self.board_size, self.board_size),
                                    dtype=int)

        self.state = None  # To keep track of the board state

    def is_valid_placement(self, start, start_color, end, end_color):
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
        
        def check_adjacent_matching_color(position, color):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                adj_x, adj_y = position[0] + dx, position[1] + dy
                if 0 <= adj_x < self.board_size and 0 <= adj_y < self.board_size:
                    # Check if the adjacent cell matches the color
                    if self.state[adj_x][adj_y] == color or self.state[adj_x][adj_y] == 5:
                        return True
            return False
        
        start_matching = check_adjacent_matching_color(start, start_color)
        end_matching = check_adjacent_matching_color(end, end_color)

         # At least one end of the domino must match an adjacent color
        if not start_matching and not end_matching:
            return False  # Neither end has a matching adjacent color

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
        domino_index, x1, y1, x2, y2 = action
        
        # Check if the selected domino is valid (not already placed)
        if domino_index >= len(self.domino_set):
            return self.state, -1, False, {"reason": "Invalid domino selection"}

        selected_domino = self.domino_set[domino_index]
        start_color = selected_domino[0]
        end_color = selected_domino[0]

        # Check if the placement is valid with the added tile color
        if not self.is_valid_placement((x1, y1), start_color, (x2, y2), end_color):
            # Penalize invalid moves to discourage them
            return self.state, -1, False, {"reason": "Invalid placement"}
        
        # Place the domino on the board with its color
        self.state[x1][y1] = selected_domino[0] #(1,selected_domino[0])
        self.state[x2][y2] = selected_domino[1] #(1,selected_domino[1])

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
        #self.state = [[(0, 0) for _ in range(self.board_size)] for _ in range(self.board_size)]
        
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