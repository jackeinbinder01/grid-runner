import heapq
from pathfinder.base_pathfinder import BasePathfinder
from core.grid import Grid


class UCSPathfinder(BasePathfinder):
    """
    Uniform Cost Search pathfinder.
    """
    def __init__(self, step_limit: int, coin_reward: int, trash_reward: int):
        super().__init__(step_limit, coin_reward, trash_reward)

    def search(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Compute a path from start to goal in the given state space.
        """
        frontier = []
        heapq.heappush(frontier, (0, start, [start]))  # Priority queue is frontier
        visited = {}
        while frontier:
            self.states_explored += 1
            cost_so_far, current, path = heapq.heappop(frontier)  # Pop node from frontier
            if len(path) - 1 > self.step_limit:  # Skip invalid nodes
                continue
            if current in visited and cost_so_far >= visited[current]:  # Skip if state is not improvement
                continue
            visited[current] = cost_so_far  # Add node to visited dict
            if current == goal:  # Goal test
                self.final_path = path
                return path
            for neighbor in state_space.get_adjacent(*current):  # Push neighbors to pqueue
                total_cost = cost_so_far + 1
                new_path = path + [neighbor]
                heapq.heappush(frontier, (total_cost, neighbor, new_path))
        self.final_path = []
        return []
