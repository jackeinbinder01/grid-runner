from enums.algorithm import Algorithm

"""
Grid
"""
GRID_ROWS = 10
GRID_COLS = 10
GRID_SIZE = GRID_ROWS, GRID_COLS


"""
Agent and goal position
"""
ORIGIN = (0, 0)
AGENT_ORIGIN = (0, 0)
GOAL_ORIGIN = (-1, -1)

GRIDLINE_COLOR = (200, 200, 200)

"""
Icons
"""
ICON_SIZE = (30, 30)

"""
Defaults
"""
DEFAULT_STEP_LIMIT = 20
DEFAULT_ALGO = Algorithm.ASTAR
