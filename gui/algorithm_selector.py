import pygame
from enums.algorithm import Algorithm
from gui.button import Button
from gui.component import Component
from gui.layout import ALGO_GRP_PAD
from gui.colors import BLACK, HOVER_COLOR, WHITE, GREEN, BUTTON_BG_COLOR

DEFAULT = Algorithm.ASTAR


class AlgorithmSelector(Component):
    """
    Button group enabling user to select a valid pathfinding algorithm.
    """
    def __init__(
            self,
            algorithms: list[Algorithm],
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
        self.algorithms = algorithms
        self.x = x
        self.y = y
        self.btn_width = btn_width
        self.btn_height = btn_height
        self.font = font or pygame.font.SysFont(None, 16)
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_bg_color = hover_bg_color
        self.flash_color = flash_color
        self.flash_duration = flash_duration
        self.active_bg_color = active_bg_color
        self.on_select = on_select

        self.selected = DEFAULT
        self.buttons: list[Button] = []
        self._build_buttons()

    def _build_buttons(self):
        """
        Construct algorithm selector.
        """
        self.buttons.clear()
        col_pad = ALGO_GRP_PAD
        row_pad = 10

        for i, algo in enumerate(self.algorithms):
            col = i % 2
            row = i // 2

            btn_x = self.x + col * (self.btn_width + col_pad)
            btn_y = self.y + row * (self.btn_height + row_pad)

            button = Button(
                text=algo.pretty,
                x=btn_x, y=btn_y,
                width=self.btn_width, height=self.btn_height,
                callback=self._make_select_callback(algo),
                toggle=True,
                font=self.font,
                text_color=self.text_color,
                bg_color=self.bg_color,
                hover_bg_color=self.hover_bg_color,
                flash_color=self.flash_color,
                flash_duration=self.flash_duration,
                active_bg_color=self.active_bg_color
            )
            if algo == self.selected:
                button.activate()
            self.buttons.append(button)

    def _make_select_callback(self, algo: Algorithm):
        """
        Make callback for buttons.
        """
        def callback():
            if self.selected == algo:
                return
            self.selected = algo
            for i, a in enumerate(self.algorithms):
                if a == algo:
                    self.buttons[i].activate()
                else:
                    self.buttons[i].deactivate()
            if self.on_select:
                self.on_select(self.selected)
        return callback

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw algorithm selector.
        """
        for btn in self.buttons:
            btn.draw(surface)

    def update(self, event: pygame.event.Event) -> None:
        """
        Update algorithm selector.
        """
        for btn in self.buttons:
            btn.update(event)

    @property
    def selected_algo(self) -> Algorithm:
        """
        get selected algorithm.
        """
        return self.selected

    @selected_algo.setter
    def selected_algo(self, algo: Algorithm) -> None:
        """
        set selected algorithm.
        """
        if algo in self.algorithms:
            self.selected = algo
            for i, a in enumerate(self.algorithms):
                if a == algo:
                    self.buttons[i].activate()
                else:
                    self.buttons[i].deactivate()
