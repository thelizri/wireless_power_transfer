import matplotlib.pyplot as plt
import numpy as np


def generate_burn_down_chart(work_remaining):
    """
    Generates a burn down chart.

    Parameters:
    - days: List of days in the sprint.
    - work_remaining: List of work remaining for each day.

    The length of `days` and `work_remaining` must be the same.
    """
    ideal_burndown = np.array(
        [80, 64, 48, 32, 16, 0]
    )  # Ideal burndown for a 5-day sprint

    plt.plot(
        work_remaining,
        marker="o",
        linestyle="-",
        color="b",
    )
    plt.plot(
        ideal_burndown,
        color="g",
        linestyle="-",
    )
    plt.legend(["Work Remaining", "Ideal Burndown"])
    plt.title("Burn Down Chart")  # Chart title
    plt.xlabel("Day")  # X-axis label
    plt.ylabel("Story Points")  # Y-axis label
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)  # Enable grid
    plt.show()  # Display the chart


work_remaining = np.array(
    [80, 70, 60, 30, 20, 0]
)  # Example work remaining for each day

generate_burn_down_chart(work_remaining)
