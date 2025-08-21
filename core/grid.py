import numpy as np
from enums.game_object import GameObject
from collections import Counter


class Grid:
    """
    Game grid.
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows, cols), GameObject.EMPTY)
        self.agent_x_y = None
        self.goal_x_y = None

    def in_bounds(self, row: int, col: int) -> bool:
        """
        Determines if a position lies within the grid.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, row: int, col: int) -> bool:
        """
        Makes walled cells impassible.
        """
        return self.in_bounds(row, col) and self.grid[row, col] != GameObject.WALL

    def set_agent(self, row: int, col: int) -> None:
        """
        Set agent position in grid.
        """
        if self.agent_x_y:
            self.grid[self.agent_x_y] = GameObject.EMPTY
        self.agent_x_y = (row, col)
        self.grid[row, col] = GameObject.AGENT

    def set_goal(self, row: int, col: int) -> None:
        """
        Set goal position in grid.
        """
        if self.goal_x_y:
            self.grid[self.goal_x_y] = GameObject.EMPTY
        self.goal_x_y = (row, col)
        self.grid[self.goal_x_y] = GameObject.GOAL

    def get_cell_type(self, row: int, col: int) -> GameObject:
        """
        Get game object from cell.
        """
        return self.grid[row, col]

    def set_cell_type(self, row: int, col: int, game_object: GameObject) -> None:
        """
        Set game object in cell.
        """
        self.grid[row, col] = game_object

    def get_adjacent(self, row: int, col: int) -> list[tuple[int, int]]:
        """
        Get neighbors to passed cell.
        """
        adjacent = []
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            ar, ac = row + dr, col + dc
            if self.is_walkable(ar, ac):
                adjacent.append((ar, ac))
        return adjacent

    def clear(self) -> None:
        """
        Remove all game object from grid.
        """
        self.grid[:] = GameObject.EMPTY
        self.agent_x_y = None
        self.goal_x_y = None

    def count_game_objects(self) -> dict[GameObject, int]:
        """
        Get count of game objects on the grid.
        """
        counter = Counter()
        for row in self.grid:
            for cell in row:
                if cell in GameObject:
                    counter[cell] += 1
        return counter
