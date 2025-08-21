from core.grid import Grid
from core.search_planner import SearchPlanner
from collections import deque


class Agent:
    """
    Grid-based Agent that uses a SearchPlanner to travel from a starting position to a goal.
    """
    def __init__(self, planner: SearchPlanner):
        self.planner = planner
        self.position = None
        self.path = deque()

    def set_position(self, position: tuple[int, int]) -> None:
        """
        Set the agent's current position.
        """
        self.position = position

    def plan_path(self, state_space: Grid, goal: tuple[int, int]) -> None:
        """
        Find a path from the agent's position to the goal using its planner.

        :param state_space: The state space (grid)
        :param goal: (row, col) goal position
        """
        if self.position is None:
            raise ValueError("Agent's position has not been set.")
        self.path = deque(self.planner.plan(state_space, self.position, goal))

    def has_path(self) -> bool:
        """
        Return true if the agent still has nodes remaining in its path.
        """
        return bool(self.path)

    def step(self) -> None:
        """
        Traverse the agent's path to its next position.
        """
        if self.path:
            self.position = self.path.popleft()
