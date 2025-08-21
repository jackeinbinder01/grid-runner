import pygame
from core.grid import Grid
from core.agent import Agent
from enums.game_object import GameObject
from gui.layout import CELL_SIZE, GRID_ML, GRID_MT
from gui.colors import GRIDLINE_COLOR, WHITE


class GridView:
    """
    GUI window that displays the game grid.
    """
    def __init__(self, grid: Grid, agent: Agent, surface: pygame.surface, on_change=None):
        pygame.init()

        self.grid = grid
        self.agent = agent

        self.margin_top = GRID_MT
        self.margin_left = GRID_ML

        self.cell_size = CELL_SIZE
        self.width = grid.cols * self.cell_size
        self.height = grid.rows * self.cell_size
        self.screen = surface
        self.on_change = on_change

        self.selected_object: GameObject | None = None
        self.dragging_object = None
        self.dragging = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw grid.
        """
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                game_object = self.grid.get_cell_type(row, col)

                x = self.margin_left + col * self.cell_size
                y = self.margin_top + row * self.cell_size
                pygame.draw.rect(surface, WHITE, (x, y, self.cell_size, self.cell_size))

                if game_object not in [GameObject.EMPTY, GameObject.AGENT]:
                    icon = game_object.icon
                    if icon:
                        icon_rect = icon.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        surface.blit(icon, icon_rect)
                    else:
                        pygame.draw.rect(surface, game_object.color, (x, y, self.cell_size, self.cell_size))

                pygame.draw.rect(surface, GRIDLINE_COLOR, (x, y, self.cell_size, self.cell_size), width=1)

        if self.agent.position and not (self.dragging and self.dragging_object == GameObject.AGENT):
            r, c = self.agent.position
            x = self.margin_left + c * self.cell_size
            y = self.margin_top + r * self.cell_size

            icon = GameObject.AGENT.icon
            if icon:
                icon_rect = icon.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                surface.blit(icon, icon_rect)
            else:
                pygame.draw.circle(
                    surface,
                    GameObject.AGENT.color,
                    (x + self.cell_size // 2, y + self.cell_size // 2),
                    self.cell_size // 3
                )

        if self.dragging and self.dragging_object in {GameObject.AGENT, GameObject.GOAL}:
            icon = self.dragging_object.icon
            if icon:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                icon_rect = icon.get_rect(center=(mouse_x, mouse_y))
                self.screen.blit(icon, icon_rect)

    def handle_click(self, pos: tuple[int, int], button: int = 1):
        """
        Handle click on game grid.
        """
        x, y = pos
        row = (y - self.margin_top) // self.cell_size
        col = (x - self.margin_left) // self.cell_size

        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            if button == 1 and self.selected_object is not None:
                occupant = self.grid.get_cell_type(row, col)
                if occupant != self.selected_object and occupant not in (GameObject.AGENT, GameObject.GOAL):
                    self.grid.set_cell_type(row, col, self.selected_object)  # Place object on game board
                    if self.on_change:
                        self.on_change()

            elif button == 3:
                occupant = self.grid.get_cell_type(row, col)
                if occupant not in (GameObject.AGENT, GameObject.GOAL, GameObject.EMPTY):
                    self.grid.set_cell_type(row, col, GameObject.EMPTY)  # Remove object from game board
                    if self.on_change:
                        self.on_change()

    def _get_cell_from_mouse(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        """
        Convert click position into grid cell.
        """
        x, y = pos
        x -= self.margin_left
        y -= self.margin_top
        row = y // self.cell_size
        col = x // self.cell_size
        if 0 <= row < self.grid.rows and 0 <= col < self.grid.cols:
            return row, col
        return None

    def update(self, event: pygame.event.Event):
        """
        Update grid on click.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos, event.button)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                result = self._get_cell_from_mouse(event.pos)
                if result:
                    row, col = result
                    obj = self.grid.get_cell_type(row, col)
                    if obj in {GameObject.AGENT, GameObject.GOAL}:
                        self.dragging_object = obj
                        self.dragging = True
                        self.grid.set_cell_type(row, col, GameObject.EMPTY)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                result = self._get_cell_from_mouse(event.pos)
                if result:
                    row, col = result
                    if self.dragging_object == GameObject.AGENT:
                        self.agent.set_position((row, col))
                        self.grid.set_agent(row, col)
                    elif self.dragging_object == GameObject.GOAL:
                        self.grid.set_goal(row, col)
                self.dragging = False
                self.dragging_object = None
                if self.on_change:
                    self.on_change()
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            pass
