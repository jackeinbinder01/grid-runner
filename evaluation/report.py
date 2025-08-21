import json
import os
from datetime import datetime
from core.grid import Grid
from enums.game_object import GameObject

GAME_OBJECT_CODE = {
    GameObject.EMPTY: "_",
    GameObject.WALL: "W",
    GameObject.COIN: "C",
    GameObject.TRASH: "T",
    GameObject.AGENT: "A",
    GameObject.GOAL: "G",
}


class Report:
    """
    Report class for performance metrics.
    """
    def __init__(self, output_dir="evaluation/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.runs = []

    def add_run(
            self,
            grid,
            algorithm_name,
            success,
            steps_taken,
            step_limit,
            score,
            collected,
            states_explored,
            compute_time,
            final_path
    ) -> None:
        """
        Add recent run to report.
        """
        run = {
            'timestamp': datetime.now().isoformat(),
            'algorithm': algorithm_name,
            'success': success,
            'steps_taken': steps_taken,
            'step_limit': step_limit,
            'score': score,
            'collected': {k.name: v for k, v in collected.items()},
            'states_explored': states_explored,
            'compute_time': compute_time,
            'final_path': final_path,
            'grid': self._serialize_grid(grid)
        }
        self.runs.append(run)

    @staticmethod
    def _serialize_grid(grid: Grid) -> list[list[str]]:
        """
        Serialize grid for writing to json.
        """
        return [
            [GAME_OBJECT_CODE.get(cell, "?") for cell in row]
            for row in grid.grid
        ]

    def save_json(self, filename: str = "report.json") -> None:
        """
        Save report to json file.
        """
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w') as f:
            json.dump(self.runs, f, indent=4)

    def print_report(self) -> None:
        """
        Print report summary.
        """
        if not self.runs:
            print("[EMPTY]")
            return

        print("Report Summary\n")
        for i, run in enumerate(self.runs, start=1):
            print(f"Run: {i}")
            print(f"Timestamp: {run['timestamp']}")
            print(f"Algorithm: {run['algorithm']}")
            print(f"Success: {run['success']}")
            print(f"Steps Taken: {run['steps_taken']} / {run['step_limit']}")
            print(f"Score: {run['score']}")
            print(f"Collected: {run['collected']}")
            print(f"States Explored: {run['states_explored']}")
            print(f"Compute Time (seconds): {run['compute_time']}")
            print(f"Final Path: {run['final_path']}\n")
