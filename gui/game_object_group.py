
import pygame
from enums.game_object import GameObject
from gui.button import Button
from gui.component import Component
from gui.layout import OBJ_GRP_PAD
from gui.colors import BLACK, WHITE, BUTTON_BG_COLOR, HOVER_COLOR, GREEN


class GameObjectGroup(Component):
    """
    Button group for selecting game objects.
    """
    def __init__(
            self,
            game_objects: list[GameObject],
            x: int, y: int,
            btn_width: int, btn_height: int,
            font: pygame.font.Font | None = None,
            text_color: tuple[int, int, int] = BLACK,
            bg_color: tuple[int, int, int] = BUTTON_BG_COLOR,
            hover_bg_color: tuple[int, int, int] = HOVER_COLOR,
            flash_color: tuple[int, int, int] = WHITE,
            flash_duration: int = 100,
            active_bg_color: tuple[int, int, int] = GREEN,
            on_select=None
    ):
        self.game_objects = game_objects
        self.x = x
        self.y = y
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.font = font or pygame.font.SysFont(None, 24)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.flash_color = flash_color
        self.flash_duration = flash_duration
        self.active_bg_color = active_bg_color
        self.on_select = on_select

        self.selected = None
        self.buttons: list[Button] = []
        self._build_buttons()

    def _build_buttons(self) -> None:
        """
        Build game object buttons.
        """
        self.buttons.clear()
        for i, obj in enumerate(self.game_objects):
            btn_x = self.x + i * (self.btn_width + OBJ_GRP_PAD)
            button = Button(
                text=obj.emoji,
                x=btn_x, y=self.y,
                width=self.btn_width, height=self.btn_height,
                callback=self._make_select_callback(obj),
                font=self.font,
                text_color=self.text_color,
                bg_color=self.bg_color,
                hover_bg_color=self.hover_bg_color,
                flash_color=self.flash_color,
                flash_duration=self.flash_duration,
                active_bg_color=self.active_bg_color,
                toggle=True,
                icon=obj.icon
            )
            if obj == self.selected:
                button.activate()
            self.buttons.append(button)

    def _make_select_callback(self, game_object: GameObject):
        """
        Make callbacks for game object buttons.
        """
        def callback():
            if self.selected == game_object:
                self.selected = None
            else:
                self.selected = game_object
            for i, obj in enumerate(self.game_objects):
                if obj == self.selected:
                    self.buttons[i].activate()
                else:
                    self.buttons[i].deactivate()
            if self.on_select:
                self.on_select(self.selected)
        return callback

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw button group.
        """
        for btn in self.buttons:
            btn.draw(surface)

    def update(self, event: pygame.event.Event) -> None:
        """
        Update button group.
        """
        for btn in self.buttons:
            btn.update(event)

    @property
    def selected_game_object(self) -> GameObject:
        """
        Get selected game object.
        """
        return self.selected

    @selected_game_object.setter
    def selected_game_object(self, game_object: GameObject | None) -> None:
        """
        Set selected game object.
        """
        if game_object in self.game_objects:
            self.selected = game_object
            for i, obj in enumerate(self.game_objects):
                if obj == self.selected:
                    self.buttons[i].activate()
                else:
                    self.buttons[i].deactivate()
