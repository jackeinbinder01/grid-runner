from abc import ABC, abstractmethod
from core.grid import Grid


class BasePathfinder(ABC):
    """
    Abstract base class for all pathfinding algorithms.
    """
    def __init__(self, step_limit: int, coin_reward: int, trash_reward: int):
        self.step_limit = step_limit
        self.coin_reward = coin_reward
        self.trash_reward = trash_reward
        self.states_explored = 0
        self.final_path: list[tuple[int, int]] = []

    @abstractmethod
    def search(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Compute a path from start to goal in the given state space.

        :param state_space: The state space (Grid)
        :param start: (row, col) start position
        :param goal: (row, col) goal position
        :return: List of (row, col) steps from start to goal, or [] if no path
        """
        pass
