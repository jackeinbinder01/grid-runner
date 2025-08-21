import heapq
from pathfinder.reward_aware_pathfinder import RewardAwarePathfinder
from core.grid import Grid
from enums.game_object import GameObject
from itertools import count


class RewardGreedyBestFirstPathfinder(RewardAwarePathfinder):
    """
    Reward-aware Greedy Best-First Search pathfinder.
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

    @staticmethod
    def pos_to_bit(row: int, col: int, cols: int) -> int:
        """
        Return bitmask for grid position.
        """
        return 1 << (row * cols + col)

    def search(self, state_space: Grid, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Compute a path from start to goal in the given state space.
        """
        initial = {
            'pos': start,
            'score': 0,
            'steps': 0,
            'collected_mask': 0,
            'parent': None
        }
        frontier = []
        counter = count()
        # Priority queue is frontier
        heapq.heappush(frontier, (self.heuristic(start, goal), next(counter), initial))
        visited = {}
        best_goal_score = float('-inf')  # Track best score
        best_goal_node = None  # Track best node
        while frontier:
            self.states_explored += 1
            _, _, node = heapq.heappop(frontier)  # Pop node from frontier
            pos = node['pos']
            score = node['score']
            steps = node['steps']
            collected_mask = node['collected_mask']
            if pos == goal and steps <= self.step_limit:  # Goal test
                if score > best_goal_score:  # Skip state if no improvement
                    best_goal_score = score
                    best_goal_node = node
                continue
            if steps > self.step_limit:  # Skip invalid nodes
                continue
            state_key = (pos, collected_mask)
            if state_key in visited:  # Skip state if no improvement
                prev_score, prev_steps = visited[state_key]
                if score <= prev_score and steps >= prev_steps:
                    continue
            visited[state_key] = (score, steps)
            for neighbor in state_space.get_adjacent(*pos):
                r, c = neighbor
                cell_type = state_space.get_cell_type(r, c)
                bit = self.pos_to_bit(r, c, state_space.cols)  # Use bit masking to quickly check and modify grid
                reward = 0
                new_mask = collected_mask
                if cell_type in (GameObject.COIN, GameObject.TRASH) and not (collected_mask & bit):
                    reward = self.get_reward(cell_type)  # Add reward if not yet collected
                    new_mask |= bit  # Mark item as collected
                new_node = {
                    'pos': neighbor,
                    'score': score + reward,
                    'steps': steps + 1,
                    'collected_mask': new_mask,
                    'parent': node
                }
                h = self.heuristic(neighbor, goal) - new_node['score']  # Reward aware heuristic function
                heapq.heappush(frontier, (h, next(counter), new_node))  # Push neighbors to pqueue
        if best_goal_node:
            self.final_path = self.reconstruct_path(best_goal_node)
            return self.final_path
        self.final_path = []
        return []
