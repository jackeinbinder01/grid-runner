import pygame
from gui.colors import BLACK, GUI_BG_COLOR


class DialogueWindow:
    """
    Window for communicating with the user.
    """

    def __init__(
            self,
            x: int, y: int,
            width: int, height: int,
            text: str = None,
            sub_text: str = None,
            bg_color: tuple[int, int, int] = GUI_BG_COLOR,
            text_color: tuple[int, int, int] = BLACK,
            sub_text_color: tuple[int, int, int] = BLACK,
            font: pygame.font.Font | None = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.sub_text = sub_text
        self.font = font or pygame.font.SysFont(None, 24)
        self.sub_text_font = pygame.font.SysFont(None, 16)
        self.bg_color = bg_color
        self.text_color = text_color
        self.sub_text_color = sub_text_color

    def set_text(self, text: str, text_color=None) -> None:
        """
        Set main text in dialogue window
        """
        if text_color:
            self.text_color = text_color
        self.text = text

    def set_sub_text(self, sub_text: str, sub_text_color=None) -> None:
        """
        Set sub-text in dialogue window
        """
        if sub_text_color:
            self.sub_text_color = sub_text_color
        self.sub_text = sub_text

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw dialogue window.
        """
        if not (self.text or self.sub_text):
            return

        pygame.draw.rect(screen, self.bg_color, self.rect)

        # Main text
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.top = self.rect.top + 10
            screen.blit(text_surface, text_rect)

        # Subtext
        if self.sub_text:
            sub_surface = self.sub_text_font.render(self.sub_text, True, self.sub_text_color)
            sub_rect = sub_surface.get_rect()
            sub_rect.centerx = self.rect.centerx
            sub_rect.top = self.rect.centery + 4
            screen.blit(sub_surface, sub_rect)

    def clear(self) -> None:
        """
        Clear dialogue window.
        """
        self.text = None
        self.sub_text = None
