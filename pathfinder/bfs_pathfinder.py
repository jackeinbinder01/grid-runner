from collections import deque
from pathfinder.base_pathfinder import BasePathfinder
from core.grid import Grid


class BFSPathfinder(BasePathfinder):
    """
    Breadth-First Search pathfinder
    """
    def __init__(self, step_limit: int, coin_reward: int, trash_reward: int):
        super().__init__(step_limit, coin_reward, trash_reward)

    def search(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Compute a path from start to goal in the given state space.
        """
        frontier = deque()
        frontier.append((start, [start]))
        visited = set()
        while frontier:
            current, path = frontier.popleft()  # Pop node from frontier
            self.states_explored += 1
            if len(path) - 1 > self.step_limit or current in visited:  # Skip invalid or visited nodes
                continue
            visited.add(current)  # Add node to visited set
            if current == goal:  # Goal test
                self.final_path = path
                return path
            for neighbor in state_space.get_adjacent(*current):  # Enqueue neighbors
                if neighbor not in visited:
                    frontier.append((neighbor, path + [neighbor]))
        self.final_path = []
        return []
