import numpy as np

class StupidPlayer:
    def __init__(self, action_space):
        """
        Initializes the StupidPlayer with the environment's action space.

        Args:
            action_space: The action space of the environment, which allows the agent
                          to know the range of possible actions it can take.
        """
        self.action_space = action_space

    def get_action(self, obs):
        """
        Returns a random action from the action space regardless of the observation.

        Args:
            obs: The current state observation. Note that for this agent, the observation
                 is ignored, and the decision is made randomly.

        Returns:
            int: A randomly chosen action.
        """
        return self.action_space.sample()
