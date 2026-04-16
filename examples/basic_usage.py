"""
Basic usage examples for SciPlot.

This file demonstrates the fundamental features of the SciPlot library.
"""

import numpy as np
from sciplot import (
    setup_style,
    new_figure,
    save,
    plot_line,
    plot_multi_line,
    plot_scatter,
    plot_bar,
)

# Generate sample data
np.random.seed(42)
x = np.linspace(0, 10, 100)
y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
y2 = np.cos(x) + np.random.normal(0, 0.1, 100)
y3 = np.sin(x) * np.cos(x) + np.random.normal(0, 0.1, 100)


def example_1_simple_line():
    """Example 1: Simple line plot."""
    print("Example 1: Simple line plot")

    fig, ax = plot_line(
        x,
        y1,
        xlabel="Time (s)",
        ylabel="Amplitude",
        title="Simple Sine Wave",
        label="Signal",
        venue="ieee",
        palette="100yuan",
        linestyle="-",
        marker="",
    )

    save(fig, "outputs/example_01_simple_line")
    print("  Saved: outputs/example_01_simple_line.pdf\n")


def example_2_multi_line():
    """Example 2: Multi-line plot with different palettes."""
    print("Example 2: Multi-line plot")

    # Test different palettes
    palettes = ["100yuan", "50yuan", "20yuan", "10yuan", "5yuan", "1yuan"]

    for palette in palettes:
        fig, ax = plot_multi_line(
            x,
            [y1, y2, y3],
            labels=["sin(x)", "cos(x)", "sin(x)·cos(x)"],
            xlabel="x (radians)",
            ylabel="y",
            title=f"Trigonometric Functions - {palette}",
            venue="ieee",
            palette=palette,
            use_linestyles=True,
        )

        save(fig, f"outputs/example_02_multi_{palette}")
        print(f"  Saved: outputs/example_02_multi_{palette}.pdf")

    print()


def example_3_scatter():
    """Example 3: Scatter plot."""
    print("Example 3: Scatter plot")

    # Generate clustered data
    n_points = 200
    x_scatter = np.concatenate(
        [
            np.random.normal(2, 0.5, n_points),
            np.random.normal(5, 0.8, n_points),
            np.random.normal(8, 0.6, n_points),
        ]
    )
    y_scatter = np.concatenate(
        [
            np.random.normal(3, 0.5, n_points),
            np.random.normal(6, 0.8, n_points),
            np.random.normal(4, 0.6, n_points),
        ]
    )

    fig, ax = plot_scatter(
        x_scatter,
        y_scatter,
        xlabel="Feature 1",
        ylabel="Feature 2",
        title="Clustered Data",
        s=30,
        alpha=0.5,
        venue="nature",
        palette="50yuan",
        edgecolors="white",
        linewidth=0.5,
    )

    save(fig, "outputs/example_03_scatter")
    print("  Saved: outputs/example_03_scatter.pdf\n")


def example_4_bar_chart():
    """Example 4: Bar chart."""
    print("Example 4: Bar chart")

    categories = ["Model A", "Model B", "Model C", "Model D", "Model E"]
    values = np.array([85, 92, 78, 95, 88])

    fig, ax = plot_bar(
        categories,
        values,
        xlabel="Model",
        ylabel="Accuracy (%)",
        title="Model Comparison",
        venue="ieee",
        palette="100yuan",
        color="#780018",
        edgecolor="black",
        linewidth=1,
    )

    # Add value labels on bars
    for i, v in enumerate(values):
        ax.text(i, v + 1, str(v), ha="center", va="bottom", fontsize=9)

    save(fig, "outputs/example_04_bar")
    print("  Saved: outputs/example_04_bar.pdf\n")


def example_5_venues():
    """Example 5: Different venues."""
    print("Example 5: Different venues")

    venues = ["ieee", "nature", "aps", "springer", "thesis", "presentation"]

    for venue in venues:
        fig, ax = plot_line(
            x,
            y1,
            xlabel="Time (s)",
            ylabel="Amplitude",
            title=f"Venue: {venue}",
            venue=venue,
            palette="100yuan",
        )

        save(fig, f"outputs/example_05_venue_{venue}")
        print(f"  Saved: outputs/example_05_venue_{venue}.pdf")

    print()


def example_6_chinese_labels():
    """Example 6: Chinese labels."""
    print("Example 6: Chinese labels")

    setup_style("thesis", "100yuan", lang="zh-cn")
    fig, ax = new_figure("thesis")

    ax.plot(x, y1, label="信号1")
    ax.plot(x, y2, label="信号2")

    ax.set_xlabel("时间 (秒)")
    ax.set_ylabel("幅度")
    ax.set_title("正弦波与余弦波")
    ax.legend()
    ax.tick_params(direction="in")

    save(fig, "outputs/example_06_chinese")
    print("  Saved: outputs/example_06_chinese.pdf\n")


if __name__ == "__main__":
    import os

    # Create outputs directory
    os.makedirs("outputs", exist_ok=True)

    print("=" * 60)
    print("SciPlot Basic Usage Examples")
    print("=" * 60)
    print()

    example_1_simple_line()
    example_2_multi_line()
    example_3_scatter()
    example_4_bar_chart()
    example_5_venues()
    example_6_chinese_labels()

    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
