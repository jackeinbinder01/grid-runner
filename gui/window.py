import pygame
from core.agent import Agent
from core.grid import Grid
from gui.grid_view import GridView
from gui.algorithm_selector import AlgorithmSelector
from gui.button import Button
from gui.dialogue_window import DialogueWindow
from gui.display_rect import DisplayRect
from gui.game_object_group import GameObjectGroup
from gui.layout import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    S_BUTTON_HEIGHT, S_BUTTON_WIDTH,
    PAUSE_X, PAUSE_Y,
    RESET_X, RESET_Y,
    TITLE_X, TITLE_Y, TITLE_WIDTH, TITLE_HEIGHT,
    SCORE_X, SCORE_Y, SCORE_WIDTH, SCORE_HEIGHT,
    STEPS_X, STEPS_Y,
    COINS_X, COINS_Y, COINS_WIDTH, COINS_HEIGHT,
    TRASH_X, TRASH_Y, TRASH_WIDTH, TRASH_HEIGHT,
    STEP_BTN_WIDTH, STEP_BTN_HEIGHT,
    STEP_GRP_X, STEP_GRP_Y, STEP_GRP_WIDTH, STEP_GRP_HEIGHT,
    COIN_GRP_X, COIN_GRP_Y, COIN_GRP_WIDTH, COIN_GRP_HEIGHT,
    TRASH_GRP_X, TRASH_GRP_Y, TRASH_GRP_WIDTH, TRASH_GRP_HEIGHT,
    OBJ_GRP_X, OBJ_GRP_Y, OBJ_GRP_WIDTH, OBJ_GRP_HEIGHT,
    ALGO_GRP_X, ALGO_GRP_Y, ALGO_GRP_WIDTH, ALGO_GRP_HEIGHT,
    DW_X, DW_Y, DW_WIDTH, DW_HEIGHT
)
from gui.stepper_group import StepperGroup
from gui.title import Title
from enums.algorithm import Algorithm
from enums.game_object import GameObject
from core.config import DEFAULT_STEP_LIMIT
from enums.run_state import RunState
from gui.colors import BLACK, GREEN, RED, GUI_BG_COLOR, BUTTON_BG_COLOR, DARK_BUTTON_BG_COLOR, TEXT_GREEN


class Window:
    """
    Grid Runner GUI.
    """
    def __init__(
            self,
            grid: Grid,
            agent: Agent,
            on_change=None,
            on_step_limit_change=None,
            on_reward_change=None,
            on_algorithm_change=None,
            on_toggle_pause=None,
            on_reset=None,
    ):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Grid Runner")

        self.on_change = on_change
        self.on_step_limit_change = on_step_limit_change
        self.on_reward_change = on_reward_change
        self.on_algorithm_change = on_algorithm_change
        self.on_toggle_pause = on_toggle_pause
        self.on_reset = on_reset

        self.grid = grid
        self.agent = agent
        self.grid_view = GridView(grid, agent, surface=self.screen, on_change=self.on_change)

        # Basic components
        self.title = Title("Grid Runner", TITLE_X, TITLE_Y, TITLE_WIDTH, TITLE_HEIGHT)
        self.pause_btn = Button("Go", PAUSE_X, PAUSE_Y, S_BUTTON_WIDTH, S_BUTTON_HEIGHT, self.toggle_pause)
        self.reset_btn = Button("Reset", RESET_X, RESET_Y, S_BUTTON_WIDTH, S_BUTTON_HEIGHT, self.on_reset)

        # DisplayRects
        self.score_display = DisplayRect("Score", (0,), SCORE_X, SCORE_Y, SCORE_WIDTH, SCORE_HEIGHT)
        self.steps_display = DisplayRect("Steps", (0, DEFAULT_STEP_LIMIT), STEPS_X, STEPS_Y, SCORE_WIDTH, SCORE_HEIGHT)
        self.coins_display = DisplayRect("Coins", (0,), COINS_X, COINS_Y, COINS_WIDTH, COINS_HEIGHT)
        self.trash_display = DisplayRect("Trash", (0,), TRASH_X, TRASH_Y, TRASH_WIDTH, TRASH_HEIGHT)
        self.step_lim_grp_display = DisplayRect("Step Limit", (DEFAULT_STEP_LIMIT,), STEP_GRP_X, STEP_GRP_Y,
                                                STEP_GRP_WIDTH, STEP_GRP_HEIGHT)
        self.coin_grp_display = DisplayRect("Coin Reward", (0,), COIN_GRP_X, COIN_GRP_Y, COIN_GRP_WIDTH,
                                            COIN_GRP_HEIGHT)
        self.trash_grp_display = DisplayRect("Trash Reward", (0,), TRASH_GRP_X, TRASH_GRP_Y, TRASH_GRP_WIDTH,
                                             TRASH_GRP_HEIGHT)

        # StepperGroups
        self.step_limit_grp = StepperGroup(self.step_lim_grp_display, STEP_BTN_WIDTH, STEP_BTN_HEIGHT,
                                           callback=self.on_step_limit_change, initial=DEFAULT_STEP_LIMIT)
        self.coin_grp = StepperGroup(self.coin_grp_display, STEP_BTN_WIDTH, STEP_BTN_HEIGHT,
                                     callback=self.on_reward_change)
        self.trash_grp = StepperGroup(self.trash_grp_display, STEP_BTN_WIDTH, STEP_BTN_HEIGHT,
                                      callback=self.on_reward_change)

        # GameObjectGroups
        game_objects: list[GameObject] = [GameObject.COIN, GameObject.WALL, GameObject.TRASH]
        self.game_object_group = GameObjectGroup(
            game_objects,
            OBJ_GRP_X,
            OBJ_GRP_Y,
            OBJ_GRP_WIDTH,
            OBJ_GRP_HEIGHT,
            on_select=self.on_game_object_selected
        )
        # Algorithms list
        algorithms: list[Algorithm] = [
            Algorithm.ASTAR,
            Algorithm.UCS,
            Algorithm.GREEDY_SEARCH,
            Algorithm.BFS,
            Algorithm.RANDOMIZED_HILL_CLIMBING,
            Algorithm.SIMULATED_ANNEALING
        ]
        # Algorithms selector group
        self.algorithms_selector = AlgorithmSelector(
            algorithms,
            ALGO_GRP_X,
            ALGO_GRP_Y,
            ALGO_GRP_WIDTH,
            ALGO_GRP_HEIGHT,
            on_select=self.on_algo_selected
        )
        # Dialogue window
        self.dialogue_window = DialogueWindow(
            DW_X,
            DW_Y,
            DW_WIDTH,
            DW_HEIGHT,
        )

        self.displays: list[DisplayRect] = [
            self.score_display,
            self.steps_display,
            self.coins_display,
            self.trash_display,
            self.step_lim_grp_display,
            self.coin_grp_display,
            self.trash_grp_display,
        ]
        self.step_button_groups: list[StepperGroup] = [
            self.step_limit_grp, self.coin_grp, self.trash_grp
        ]

        self.components = [
            self.title,
            self.grid_view,
            self.pause_btn,
            self.reset_btn,
            *self.displays,
            *self.step_button_groups,
            self.game_object_group,
            self.algorithms_selector,
            self.dialogue_window
        ]

        # Track window values
        self.game_object_counts = self.grid.count_game_objects()
        self.collected = {
            GameObject.COIN: 0,
            GameObject.TRASH: 0
        }

        self.run_state = RunState.GO

    def draw(self) -> None:
        """
        Draw GUI window.
        """
        self.screen.fill(GUI_BG_COLOR)

        for component in self.components:
            component.draw(self.screen)

    @staticmethod
    def update() -> None:
        """
        Update GUI window.
        """
        pygame.display.flip()

    def handle_event(self, event) -> None:
        """
        GUI event handler.
        """
        for component in self.components:
            if hasattr(component, 'update'):
                component.update(event)

    def toggle_pause(self) -> None:
        """
        Pause button handler.
        """
        if not self.on_toggle_pause:
            return
        if self.run_state == RunState.GO:
            self.on_toggle_pause(RunState.GO)
            self.set_run_state(RunState.PLAY)
        elif self.run_state == RunState.PLAY:
            self.on_toggle_pause(RunState.PAUSE)
            self.set_run_state(RunState.PAUSE)
        elif self.run_state == RunState.PAUSE:
            self.on_toggle_pause(RunState.PLAY)
            self.set_run_state(RunState.PLAY)
        elif self.run_state == RunState.FINISHED:
            self.set_run_state(RunState.FINISHED)

    def set_run_state(self, run_state: RunState) -> None:
        """
        Set runstate.
        """
        self.run_state = run_state
        if run_state == RunState.GO:
            self.set_pause_button_text("Go")
            self.set_pause_button_bg_color(GREEN)
        elif run_state == RunState.PLAY:
            self.set_pause_button_text("Pause")
            self.set_pause_button_bg_color(BUTTON_BG_COLOR)
        elif run_state == RunState.PAUSE:
            self.set_pause_button_text("Play")
            self.set_pause_button_bg_color(BUTTON_BG_COLOR)
        elif run_state == RunState.FINISHED:
            self.set_pause_button_text("Goal Reached!")
            self.set_pause_button_bg_color(DARK_BUTTON_BG_COLOR)  # darker button bg
        elif run_state == RunState.HALTED:
            self.set_pause_button_text("Agent Halted")
            self.set_pause_button_bg_color(DARK_BUTTON_BG_COLOR)

    def set_pause_button_text(self, text: str) -> None:
        """
        Set pause button text.
        """
        self.pause_btn.text = text

    def set_pause_button_bg_color(self, color: tuple[int, int, int]) -> None:
        """
        Change pause button color.
        """
        self.pause_btn.bg_color = color

    def on_game_object_selected(self, selected: GameObject | None) -> None:
        """
        Handle game object selection.
        """
        self.grid_view.selected_object = selected

    def on_algo_selected(self, selected: Algorithm | None) -> None:
        """
        Handle algorithm selection.
        """
        if selected is not None:
            if self.on_algorithm_change:
                self.on_algorithm_change(selected)

    def update_game_object_displays(self) -> None:
        """
        Update game object counters.
        """
        counter = self.grid.count_game_objects()
        self.game_object_counts = counter

        self.coins_display.set_value(
            (self.collected.get(GameObject.COIN, 0),)
        )

        self.trash_display.set_value(
            (self.collected.get(GameObject.TRASH, 0),)
        )

    def update_step_counter(self, step_count: int, step_limit: int) -> None:
        """
        Update step counter.
        """
        self.steps_display.set_value((step_count, step_limit))

    def update_collected(self, collected: dict[GameObject, int]) -> None:
        """
        Update collected rewards.
        """
        self.collected = collected
        self.update_game_object_displays()

    def update_score(self, score: int) -> None:
        """
        Update score display value.
        """
        self.score_display.set_value((score,))

    def clear_dialogue_window(self) -> None:
        """
        Clear dialogue window
        """
        self.dialogue_window.clear()

    def set_dialogue_window(
            self,
            text: str = None,
            text_color: tuple[int, int, int] = None,
            sub_text: str = None,
            sub_text_color: tuple[int, int, int] = None
    ) -> None:
        """
        Set dialogue window text and/or subtext
        """
        self.dialogue_window.clear()
        if text:
            self.dialogue_window.set_text(text, text_color)
        if sub_text:
            self.dialogue_window.set_sub_text(sub_text, sub_text_color)

    def dialogue_window_prompt_go(self) -> None:
        """
        Prompt user to click Go via dialogue window.
        """
        self.set_dialogue_window(
            text="Click 'Go' to activate the agent.", text_color=BLACK,
            sub_text="Drag and drop to move the agent or the goal.", sub_text_color=BLACK
        )

    def dialogue_window_step_limit_reached(self) -> None:
        """
        Inform user that step limit is reached via dialogue window.
        """
        self.set_dialogue_window(
            text="Step limit reached!", text_color=RED,
            sub_text="Try increasing the step limit.", sub_text_color=BLACK
        )

    def dialogue_window_goal_reached(self) -> None:
        """
        Inform user that goal is reached via dialogue window.
        """
        self.set_dialogue_window(
            text="Goal has been reached!", text_color=TEXT_GREEN,
            sub_text="Click 'Reset' to play again.", sub_text_color=BLACK
        )

    def dialogue_window_agent_stuck(self) -> None:
        """
        Inform user that the agent cannot find a path to the goal.
        """
        self.set_dialogue_window(
            text="Agent is stuck!",
            text_color=RED,
            sub_text="Remove walls, change the pathfinder or move the goal.",
            sub_text_color=BLACK
        )

    def dialogue_window_prompt_set_pathfinder(self) -> None:
        """
        Prompt user to select a pathfinder via algorithm selector.
        """
        self.set_dialogue_window(
            text="Select a pathfinder algorithm",
            text_color=BLACK
        )
