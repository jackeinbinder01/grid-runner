from collections.abc import Callable
import pygame

from gui.button import Button
from gui.component import Component
from gui.display_rect import DisplayRect
from gui.colors import BUTTON_BG_COLOR, WHITE, BLACK, HOVER_COLOR


class StepperGroup(Component):
    """
    Button group with +/- buttons for inputting values.
    """
    def __init__(
            self,
            display_rect: DisplayRect,
            btn_width: int, btn_height: int,
            callback: Callable[[int], None] | None = None,
            min_value: int = 0,
            max_value: int = 100,
            step: int = 1,
            initial: int = 0,
            font: pygame.font.Font | None = None,
            text_color: tuple[int, int, int] = BLACK,
            bg_color: tuple[int, int, int] = BUTTON_BG_COLOR,
            hover_bg_color: tuple[int, int, int] | None = HOVER_COLOR,
            flash_color: tuple[int, int, int] = WHITE,
            flash_duration: int = 100,
    ):
        self.display_rect = display_rect
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.callback = callback
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

        self.value = initial
        self.update_display()

        self.font = font or pygame.font.SysFont(None, 24)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color or bg_color
        self.flash_color = flash_color or bg_color
        self.flash_duration = flash_duration

        self.inc_btn = Button(
            text='+',
            x=self.display_rect.rect.right + 20,
            y=self.display_rect.rect.y,
            width=self.btn_width, height=self.btn_height,
            callback=self._increment,
            font=self.font,
            text_color=self.text_color,
            bg_color=self.bg_color,
            hover_bg_color=self.hover_bg_color,
            flash_color=self.flash_color,
            flash_duration=self.flash_duration
        )

        self.dec_btn = Button(
            text='-',
            x=self.inc_btn.x + btn_width + 10, y=self.display_rect.rect.y,
            width=self.btn_width, height=self.btn_height,
            callback=self._decrement,
            font=self.font,
            text_color=self.text_color,
            bg_color=self.bg_color,
            hover_bg_color=self.hover_bg_color,
            flash_color=self.flash_color,
            flash_duration=self.flash_duration
        )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw button group.
        """
        self.display_rect.draw(surface)
        self.inc_btn.draw(surface)
        self.dec_btn.draw(surface)

    def update(self, event: pygame.event.Event) -> None:
        """
        Update button group.
        """
        self.inc_btn.update(event)
        self.dec_btn.update(event)

    def update_display(self) -> None:
        """
        Update display value.
        """
        self.display_rect.set_value(str(self.value))

    def _increment(self) -> None:
        """
        Increment display value.
        """
        if self.value + self.step <= self.max_value:
            self.value += self.step
            self.update_display()
            if self.callback:
                self.callback(self.value)

    def _decrement(self) -> None:
        """
        Decrement display value.
        """
        if self.value - self.step >= self.min_value:
            self.value -= self.step
            self.update_display()
            if self.callback:
                self.callback(self.value)
