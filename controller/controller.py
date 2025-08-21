import pygame
from core.grid import Grid
from core.agent import Agent
from core.search_planner import SearchPlanner
from gui.window import Window
from gui.gui_utils import init_pygame
from enums.game_object import GameObject
from enums.algorithm import Algorithm
from core.config import GRID_ROWS, GRID_COLS
from core.config import AGENT_ORIGIN, DEFAULT_STEP_LIMIT, DEFAULT_ALGO
from enums.run_state import RunState
from evaluation.report import Report


class Controller:
    """
    Game controller.
    """
    def __init__(self):
        init_pygame()

        self.path = []
        self.step_idx = 0
        self.steps_taken = 0
        self.step_limit = DEFAULT_STEP_LIMIT
        self.collected = {  # Track reward collection
            GameObject.COIN: 0,
            GameObject.TRASH: 0
        }
        self.score = 0
        self.coin_reward = 0
        self.trash_reward = 0
        self.selected_algo = DEFAULT_ALGO
        self.pathfinder = DEFAULT_ALGO.get_pathfinder()
        self.grid = Grid(GRID_ROWS, GRID_COLS)
        self.search_planner = SearchPlanner(self.pathfinder(self.step_limit, self.coin_reward, self.trash_reward))
        self.agent = Agent(self.search_planner)

        self.grid.set_agent(*AGENT_ORIGIN)  # Top left corner
        self.agent.set_position(AGENT_ORIGIN)
        self.grid.set_goal(GRID_ROWS - 1, GRID_COLS - 1)  # Bottom right corner

        self.window = Window(
            self.grid,
            self.agent,
            on_change=self._handle_change,
            on_step_limit_change=self._handle_step_limit_change,
            on_reward_change=self._update_rewards,
            on_algorithm_change=self._update_algo,
            on_toggle_pause=self._handle_toggle_pause,
            on_reset=self._handle_reset,
        )

        self.run_state = RunState.GO
        self.window.set_run_state(self.run_state)

        self._handle_reset()
        self.report = Report()

    def _handle_toggle_pause(self, run_state: RunState) -> None:
        """
        Handle pause button interaction.
        """
        if self.run_state == RunState.GO:
            self.window.clear_dialogue_window()
            self.run_state = run_state.PLAY
            self.window.set_run_state(RunState.PLAY)
            self._run_pathfinding()
            return
        if self.run_state == RunState.PLAY:
            self.window.clear_dialogue_window()
            self.run_state = RunState.PAUSE
        elif self.run_state == RunState.PAUSE:
            self.window.clear_dialogue_window()
            self.run_state = RunState.PLAY
            self._run_pathfinding()
        self.window.set_run_state(self.run_state)

    def _handle_reset(self):
        """
        Handle reset button interaction.
        """
        self.window.dialogue_window_prompt_go()
        self.path = []
        self.step_idx = 0
        self.steps_taken = 0
        self.collected = {
            GameObject.COIN: 0,
            GameObject.TRASH: 0
        }
        self.score = 0

        self.grid.set_agent(*AGENT_ORIGIN)  # Top left corner
        self.agent.set_position(AGENT_ORIGIN)
        self.grid.set_goal(GRID_ROWS - 1, GRID_COLS - 1)  # Bottom right corner

        self.window.update_step_counter(self.steps_taken, self.step_limit)
        self.window.update_score(self.score)
        self.window.update_collected(self.collected)

        self.run_state = RunState.GO
        self.window.set_run_state(RunState.GO)

    def _handle_step_limit_change(self, new_limit: int) -> None:
        """
        Update on step limit changes.
        """
        self.step_limit = new_limit
        self.window.update_step_counter(self.steps_taken, self.step_limit)

        pathfinder = self.selected_algo.get_pathfinder()
        pathfinder = pathfinder(self.step_limit, self.coin_reward, self.trash_reward)
        self.search_planner.set_pathfinder(pathfinder)

        if self.run_state == RunState.HALTED and self.step_idx < len(self.path):
            self.run_state = RunState.PAUSE
            self.window.set_run_state(RunState.PAUSE)

        self._handle_change()

    def set_scoring_rules(self, coin_reward: int | str, trash_reward: int | str):
        """
        Set reward values.
        """
        self.coin_reward = int(coin_reward)
        self.trash_reward = int(trash_reward)

    def _update_rewards(self, *_):
        """
        Update reward values.
        """
        self.coin_reward = int(self.window.coin_grp_display.value or 0)
        self.trash_reward = int(self.window.trash_grp_display.value or 0)

        pathfinder = self.selected_algo.get_pathfinder()  # New pathfinder to account for change in reward values
        pathfinder = pathfinder(self.step_limit, self.coin_reward, self.trash_reward)
        self.search_planner.set_pathfinder(pathfinder)
        self._handle_change()

    def _update_algo(self, selected_algo: Algorithm) -> None:
        """
        Set algorithm selection.
        """
        if self.selected_algo is None:
            self.window.dialogue_window_prompt_set_pathfinder()

        if self.run_state != RunState.GO:
            self.window.clear_dialogue_window()
        self.selected_algo = selected_algo

        pathfinder = selected_algo.get_pathfinder()  # New pathfinder with updated algo
        pathfinder = pathfinder(self.step_limit, self.coin_reward, self.trash_reward)
        self.search_planner.set_pathfinder(pathfinder)

        if self.run_state != RunState.GO:
            self.window.clear_dialogue_window()

        self._handle_change()

    def _handle_change(self):
        """
        Handle changes within the GUI
        """
        self._run_pathfinding()
        self.window.update_game_object_displays()

    def _goal_reached(self):
        """
        Update runstate, dialogue window and record run when goal reached.
        """
        self.run_state = RunState.FINISHED
        self.window.set_run_state(RunState.FINISHED)
        self.window.dialogue_window_goal_reached()
        self._record_run()

    def _run_pathfinding(self):
        """
        Plan new path.
        """
        if self.grid.agent_x_y and self.grid.goal_x_y:
            self.path = self.search_planner.plan(self.grid, self.grid.agent_x_y, self.grid.goal_x_y)
            self.step_idx = 0
            self.finished = False

        # Agent is stuck
        if not self.path and self.run_state == RunState.PLAY:
            self.window.dialogue_window_agent_stuck()
            self._record_run()

    def _record_run(self):
        """
        Generate report for performance measurement.
        """
        self.report.add_run(
            grid=self.grid,
            algorithm_name=self.selected_algo.pretty,
            success=self.grid.agent_x_y == self.grid.goal_x_y,
            steps_taken=self.steps_taken,
            step_limit=self.step_limit,
            score=self.score,
            collected=self.collected,
            states_explored=self.search_planner.pathfinder.states_explored,
            compute_time=self.search_planner.last_compute_time,
            final_path=self.search_planner.pathfinder.final_path
        )

    def run(self) -> None:
        """
        Main event loop.
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.report.save_json('report.json')  # Generate report on quit
                    running = False
                else:
                    self.window.handle_event(event)

            if self.run_state == RunState.PLAY and self.step_idx < len(self.path):
                if self.steps_taken >= self.step_limit:
                    self.run_state = RunState.HALTED
                    self.window.set_run_state(RunState.HALTED)
                    self.window.dialogue_window_step_limit_reached()
                    self._record_run()
                else:
                    r, c = self.path[self.step_idx]
                    obj = self.grid.get_cell_type(r, c)

                    if (r, c) != self.grid.agent_x_y:
                        self.agent.set_position((r, c))
                        self.grid.set_agent(r, c)
                        self.steps_taken += 1

                    if obj == GameObject.COIN:
                        self.collected[GameObject.COIN] += 1
                        self.score += self.coin_reward
                        self.grid.set_cell_type(r, c, GameObject.EMPTY)
                        self.window.update_score(self.score)

                    elif obj == GameObject.TRASH:
                        self.collected[GameObject.TRASH] += 1
                        self.score += self.trash_reward
                        self.grid.set_cell_type(r, c, GameObject.EMPTY)
                        self.window.update_score(self.score)

                    self.window.update_step_counter(self.steps_taken, self.step_limit)
                    self.window.update_collected(self.collected)

                    self.step_idx += 1
                    if self.step_idx >= len(self.path):
                        if self.grid.agent_x_y == self.grid.goal_x_y:
                            self._goal_reached()

            self.window.draw()
            self.window.update()
            clock.tick(5)

        pygame.quit()
