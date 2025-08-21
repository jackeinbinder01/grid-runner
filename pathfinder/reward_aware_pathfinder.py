from abc import abstractmethod
from pathfinder.base_pathfinder import BasePathfinder
from core.grid import Grid
from enums.game_object import GameObject


class RewardAwarePathfinder(BasePathfinder):
    """
    Base class for reward-aware pathfinding algorithms that consider both step limits and game object collection.
    """
    def get_reward(self, game_object: GameObject) -> int:
        """
        :param game_object: GameObject within a cell.
        :return: reward value of GameObject.
        """
        if game_object == GameObject.COIN:
            return self.coin_reward
        elif game_object == GameObject.TRASH:
            return self.trash_reward
        return 0

    @staticmethod
    def build_initial_node(start: tuple[int, int]) -> dict:
        """
        :param start: start state.
        :return: initial search node.
        """
        return {
            'pos': start,
            'score': 0,
            'steps': 0,
            'collected': frozenset(),
            'parent': None
        }

    def reconstruct_path(self, node: dict) -> list[tuple[int, int]]:
        """
        Reconstructs a path from a terminal node.

        :param node: terminal node to reconstruct path from.
        :return: path from terminal node.
        """
        path = []
        while node:
            path.append(node['pos'])
            node = node['parent']
        return list(reversed(path))

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
