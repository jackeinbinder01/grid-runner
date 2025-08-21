from enum import Enum
from pathfinder.reward_astar_pathfinder import RewardAStarPathfinder
from pathfinder.reward_greedy_best_first_pathfinder import RewardGreedyBestFirstPathfinder
from pathfinder.ucs_pathfinder import UCSPathfinder
from pathfinder.bfs_pathfinder import BFSPathfinder
from pathfinder.reward_randomized_hill_climbing_pathfinder import RewardRandomizedHillClimbingPathfinder
from pathfinder.reward_simulated_annealing_pathfinder import RewardSimulatedAnnealingPathfinder


class Algorithm(Enum):
    """
    Supported pathfinder algorithms.
    """
    ASTAR = "A* Search"
    UCS = "Uniform Cost Search"
    GREEDY_SEARCH = "Greedy Best-First Search"
    BFS = "Breadth-First Search"
    RANDOMIZED_HILL_CLIMBING = "Randomized Hill Climbing"
    SIMULATED_ANNEALING = "Simulated Annealing"

    def __init__(self, pretty_name: str):
        self._pretty_name = pretty_name

    @property
    def pretty(self) -> str:
        """
        Get pretty name.
        """
        return self._pretty_name

    def get_pathfinder(self):
        """
        Get pathfinder from enum.
        """
        return {
            Algorithm.ASTAR: RewardAStarPathfinder,
            Algorithm.GREEDY_SEARCH: RewardGreedyBestFirstPathfinder,
            Algorithm.UCS: UCSPathfinder,
            Algorithm.BFS: BFSPathfinder,
            Algorithm.RANDOMIZED_HILL_CLIMBING: RewardRandomizedHillClimbingPathfinder,
            Algorithm.SIMULATED_ANNEALING: RewardSimulatedAnnealingPathfinder
        }[self]

    def __str__(self) -> str:
        """
        Get enum name.
        """
        return self.name
