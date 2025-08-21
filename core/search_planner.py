from core.grid import Grid
from pathfinder.base_pathfinder import BasePathfinder
import time


class SearchPlanner:
    """
    Computes paths from start to goal using a configured pathfinder algorithm.
    """
    def __init__(self, pathfinder: BasePathfinder):
        self.pathfinder = pathfinder
        self.last_compute_time = None

    def plan(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Plan a path from start to goal using the instance's pathfinder.

        :param state_space: The state space (Grid)
        :param start: (row, col) start position
        :param goal: (row, col) goal position
        :return: List of (row, col) steps from start to goal, or [] if no path is found
        """
        start_time = time.perf_counter()
        path = self.pathfinder.search(state_space, start, goal)
        end_time = time.perf_counter()
        self.last_compute_time = end_time - start_time
        return path

    def set_pathfinder(self, pathfinder: BasePathfinder) -> None:
        self.pathfinder = pathfinder
