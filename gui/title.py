import pygame
from gui.colors import TITLE_COLOR, BLACK

class Title:
    """
    Grid Runner title rect
    """
    def __init__(self, text, x, y, width, height, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font or pygame.font.SysFont(None, 24)
        self.color = TITLE_COLOR

    def draw(self, screen: pygame.surface) -> None:
        """
        Draw title rect.
        """
        pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
