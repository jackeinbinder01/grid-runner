import random
from pathfinder.reward_aware_pathfinder import RewardAwarePathfinder
from core.grid import Grid
from enums.game_object import GameObject


class RewardRandomizedHillClimbingPathfinder(RewardAwarePathfinder):
    """
    Reward-aware Randomized Hill Climbing pathfinder.
    """
    def __init__(self, step_limit, coin_reward, trash_reward, heuristic=None):
        super().__init__(step_limit, coin_reward, trash_reward)
        self.heuristic = heuristic or self.manhattan

    @staticmethod
    def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
        """
        Returns Manhattan distance between a and b.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    def evaluate(self, pos: tuple[int, int], goal: tuple[int, int], state_space: Grid, collected: set) -> float:
        """
        Reward-aware evaluation function for determining the value of a candidate.
        """
        r, c = pos
        cell = state_space.get_cell_type(r, c)
        reward = 0
        if cell in (GameObject.COIN, GameObject.TRASH) and (r, c) not in collected:
            reward = self.get_reward(cell)
        distance = self.heuristic(pos, goal)
        return reward - distance  # Reward-aware evaluation function

    def search(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Compute a path from start to goal in the given state space.
        """
        current = start
        path = [current]
        steps = 0
        collected = set()
        while current != goal and steps < self.step_limit:
            self.states_explored += 1
            neighbors = state_space.get_adjacent(*current)
            random.shuffle(neighbors)  # Shuffle to explore neighbors in random order
            best_score = float('-inf')  # Track best score
            best_neighbor = None  # Track best neighbor
            for neighbor in neighbors:
                score = self.evaluate(neighbor, goal, state_space, collected)  # Evaluate neighbor
                if score > best_score:
                    best_score = score
                    best_neighbor = neighbor
            if (best_neighbor is None or self.evaluate(best_neighbor, goal, state_space, collected) <=
                    self.evaluate(current, goal, state_space, collected)):
                break  # Stop if no neighbor improves on current
            current = best_neighbor
            path.append(current)  # Append best neighbor to path
            steps += 1
            if state_space.get_cell_type(*current) in (GameObject.COIN, GameObject.TRASH):
                collected.add(current)  # Mark reward as collected
        if current == goal:  # Goal test
            self.final_path = path
            return path
        self.final_path = []
        return []

