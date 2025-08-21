import pygame
from gui.colors import BLACK, WHITE


class DisplayRect:
    """
    Display window for metrics.
    """
    def __init__(
            self,
            label: str,
            value: str | tuple[int, ...],
            x: int, y: int,
            width: int, height: int,
            bg_color: tuple[int, int, int] = WHITE,
            text_color: tuple[int, int, int] = BLACK,
            font: pygame.font.Font | None = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = label
        self.value = value
        self.font = font or pygame.font.SysFont(None, 24)
        self.bg_color = bg_color
        self.text_color = text_color

    def set_value(self, new_value: str | tuple[int, ...]) -> None:
        """
        Set display value.
        """
        self.value = new_value

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw display.
        """
        pygame.draw.rect(screen, self.bg_color, self.rect)

        if isinstance(self.value, tuple):
            if len(self.value) == 2:
                value_str = f"{self.value[0]} / {self.value[1]}"
            elif len(self.value) == 1:
                value_str = str(self.value[0])
            else:
                value_str = "N/A"
        else:
            value_str = self.value

        text_surface = self.font.render(f"{self.label}: {value_str}", True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
