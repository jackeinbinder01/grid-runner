import json
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

BASE_DIR = os.getcwd()
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def load_from_json(filepath: str) -> list[dict]:
    """
    Load json file into dict.
    """
    with open(filepath, 'r') as f:
        runs: list[dict] = json.load(f)
    return runs


def get_averages_from_dicts(dicts: list[dict]) -> dict:
    """
    Get metric averages from list of dicts.
    """
    if not dicts:
        return {}

    n = len(dicts)
    n_successful = 0

    total_success = 0
    total_steps = 0
    total_score = 0
    total_states_explored = 0
    total_compute_time = 0

    for d in dicts:
        success = int(d['success'])
        total_success += success
        total_states_explored += d['states_explored']
        total_compute_time += d['compute_time']

        if success:
            n_successful += 1
            total_steps += d['steps_taken']
            total_score += d['score']

    average = {
        'algorithm': dicts[0]['algorithm'],
        'avg_success': total_success / n,
        'avg_steps_taken': total_steps / n_successful if n_successful else 0,
        'avg_score': total_score / n_successful if n_successful else 0,
        'avg_states_explored': total_states_explored / n,
        'avg_compute_time': total_compute_time / n
    }

    return average


def plot_success_rate(avg_runs: list[dict], save_to_file: bool = False) -> None:
    """
    Visualize success rate.
    """
    algorithms = [run['algorithm'] for run in avg_runs]
    success_rates = [run['avg_success'] * 100 for run in avg_runs]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, success_rates, color="tab:blue")

    for bar, success_rate in zip(bars, success_rates):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f'{success_rate:.0f}%',
            ha='center', va='bottom'
        )

    plt.ylim(0, 110)
    plt.title('Success Rate by Algorithm', pad=15)
    plt.ylabel('Success Rate (%)', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.grid(False)
    plt.tight_layout()

    if save_to_file:
        path = os.path.join(REPORTS_DIR, "success_rate.png")
        plt.savefig(path)
    plt.show()


def plot_avg_steps(avg_runs: list[dict], save_to_file: bool = False) -> None:
    """
    Visualize average steps taken.
    """
    algorithms = [run['algorithm'] for run in avg_runs]
    avg_steps_taken = [run['avg_steps_taken'] for run in avg_runs]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, avg_steps_taken, color="tab:purple")

    for bar, avg_steps in zip(bars, avg_steps_taken):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f'{avg_steps:.0f}',
            ha='center', va='bottom'
        )

    plt.ylim(0, max(avg_steps_taken) + 3)
    plt.title('Average Steps Taken by Algorithm (Successful Runs Only)', pad=15)
    plt.ylabel('Average Steps Taken', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.grid(False)
    plt.tight_layout()

    if save_to_file:
        path = os.path.join(REPORTS_DIR, "avg_steps_taken.png")
        plt.savefig(path)
    plt.show()


def plot_avg_scores(avg_runs: list[dict], save_to_file: bool = False) -> None:
    """
    Visualize average score.
    """
    algorithms = [run['algorithm'] for run in avg_runs]
    avg_score = [run['avg_score'] for run in avg_runs]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, avg_score, color="tab:green")

    for bar, score in zip(bars, avg_score):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f'{score:.0f}',
            ha='center', va='bottom'
        )

    plt.ylim(0, max(avg_score) + 3)
    plt.title('Average Score by Algorithm (Successful Runs Only)', pad=15)
    plt.ylabel('Average Score', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.grid(False)
    plt.tight_layout()

    if save_to_file:
        path = os.path.join(REPORTS_DIR, "avg_score.png")
        plt.savefig(path)
    plt.show()


def plot_avg_states_explored(avg_runs: list[dict], save_to_file: bool = False) -> None:
    """
    Visualize avg states explored.
    """
    algorithms = [run['algorithm'] for run in avg_runs]
    avg_states_explored = [run['avg_states_explored'] for run in avg_runs]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, avg_states_explored, color="tab:red")

    for bar, avg_states in zip(bars, avg_states_explored):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.05,
            f'{avg_states:,.0f}',
            ha='center', va='bottom'
        )

    plt.yscale('log')
    plt.ylim(top=max(avg_states_explored) * 2)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))  # Add commas to y axis
    plt.ylabel('Average States Explored', labelpad=10)
    plt.title('Average States Explored by Algorithm', pad=15)

    plt.xticks(rotation=45, ha='right')
    plt.grid(False)
    plt.tight_layout()

    if save_to_file:
        path = os.path.join(REPORTS_DIR, "avg_states_explored.png")
        plt.savefig(path)
    plt.show()


def plot_avg_compute_time(avg_runs: list[dict], save_to_file: bool = False) -> None:
    """
    Visualize average compute time.
    """
    algorithms = [run['algorithm'] for run in avg_runs]
    avg_compute_time = [run['avg_compute_time'] for run in avg_runs]
    avg_compute_time = [t * 1000 for t in avg_compute_time]  # Convert to ms

    plt.figure(figsize=(10, 6))
    bars = plt.bar(algorithms, avg_compute_time, color="tab:orange")

    for bar, avg_time in zip(bars, avg_compute_time):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() * 1.05,
            f'{avg_time:.2f}',
            ha='center', va='bottom'
        )

    plt.yscale('log')
    plt.ylim(top=max(avg_compute_time) * 2)
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:.2f}'))  # Add commas to y axis
    plt.ylabel('Average Compute Time (ms)', labelpad=10)
    plt.title('Average Compute Time by Algorithm (Milliseconds)', pad=15)

    plt.xticks(rotation=45, ha='right')
    plt.grid(False)
    plt.tight_layout()

    if save_to_file:
        path = os.path.join(REPORTS_DIR, "avg_compute_time.png")
        plt.savefig(path)
    plt.show()
