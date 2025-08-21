import math
import random
from pathfinder.reward_aware_pathfinder import RewardAwarePathfinder
from core.grid import Grid
from enums.game_object import GameObject


class RewardSimulatedAnnealingPathfinder(RewardAwarePathfinder):
    """
    Reward-aware Simulated Annealing pathfinder.
    """
    def __init__(self, step_limit, coin_reward, trash_reward, heuristic=None):
        super().__init__(step_limit, coin_reward, trash_reward)
        self.heuristic = heuristic or self.manhattan

    @staticmethod
    def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
        """
        Returns Manhattan distance between a and b.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

    @staticmethod
    def acceptance_probability(old_score: float, new_score: float, temperature: float) -> float:
        """
        Acceptance probability for new move.
        """
        if new_score > old_score:
            return 1.0
        return math.exp((new_score - old_score) / temperature)

    def search(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Compute a path from start to goal in the given state space.
        """
        current = start
        path = [current]
        collected = set()
        steps = 0
        temperature = 1.0
        cooling_rate = 0.97
        while current != goal and steps < self.step_limit:
            self.states_explored += 1
            neighbors = state_space.get_adjacent(*current)
            if not neighbors:
                break  # Break if no valid moves
            candidate = random.choice(neighbors)  # Randomly choose neighbor to evaluate
            old_score = self.evaluate(current, goal, state_space, collected)
            new_score = self.evaluate(candidate, goal, state_space, collected)
            steps += 1
            # Accept worse move with probability based on temperature
            if random.random() < self.acceptance_probability(old_score, new_score, temperature):
                current = candidate
                path.append(current)  # Append accepted neighbor to path
                if state_space.get_cell_type(*current) in (GameObject.COIN, GameObject.TRASH):
                    collected.add(current)  # Mark reward as collected
            temperature = max(temperature * cooling_rate, 1e-6)  # Decrease temperature
        if current == goal:  # Goal test
            self.final_path = path
            return path
        self.final_path = []
        return []


