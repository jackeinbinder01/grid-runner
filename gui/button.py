from collections.abc import Callable
import pygame
import time
from gui.component import Component
from gui.colors import BLACK, HOVER_COLOR, WHITE, GREEN, BUTTON_BG_COLOR


class Button(Component):
    """
    Button class.
    """
    def __init__(
            self,
            text: str,
            x: int, y: int,
            width: int, height: int,
            callback: Callable[[], None] | None = None,
            toggle: bool = False,
            font: pygame.font.Font = None,
            text_color: tuple[int, int, int] = BLACK,
            bg_color: tuple[int, int, int] = BUTTON_BG_COLOR,
            hover_bg_color: tuple[int, int, int] = HOVER_COLOR,
            flash_color: tuple[int, int, int] = WHITE,
            flash_duration: int = 100,
            active_bg_color: tuple[int, int, int] = GREEN,
            icon: pygame.Surface | None = None
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback
        self.toggle = toggle
        self.font = font or pygame.font.SysFont(None, 24)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color or bg_color
        self.active_bg_color = active_bg_color or bg_color
        self.flash_color = flash_color
        self.flash_duration = flash_duration
        self.icon = icon

        self.hovered = False
        self._is_active = False
        self._flash_start_time = None

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw button.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        now = time.time() * 1000  # For flashing clicked buttons

        if self._flash_start_time and (now - self._flash_start_time < self.flash_duration):
            color = self.flash_color
        elif self.is_active:
            color = self.active_bg_color
        elif self.hovered:
            color = self.hover_bg_color
        else:
            color = self.bg_color

        pygame.draw.rect(screen, color, self.rect)

        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            screen.blit(self.icon, icon_rect)
        elif self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def flash(self) -> None:
        """
        Flash clicked button.
        """
        self._flash_start_time = time.time() * 1000

    def click(self) -> None:
        """
        On click.
        """
        if self.toggle:
            self._is_active = not self._is_active

        if self.callback:
            self.callback()

        self.flash()

    def update(self, event: pygame.event.Event) -> None:
        """
        Register click.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click()

    def activate(self) -> None:
        """
        Activate button.
        """
        self._is_active = True

    def deactivate(self) -> None:
        """
        Deactivate button.
        """
        self._is_active = False

    @property
    def is_active(self) -> bool:
        """
        Get active status.
        """
        return self._is_active
