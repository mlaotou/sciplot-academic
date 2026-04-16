"""
Advanced usage examples for SciPlot.

This file demonstrates advanced features like subplots, GridSpec,
confidence intervals, error bars, heatmaps, and more.
"""

import numpy as np

from sciplot import (
    setup_style,
    new_figure,
    save,
    create_subplots,
    create_gridspec,
    create_twinx,
    plot_errorbar,
    plot_confidence,
    plot_heatmap,
    get_palette,
)

# Generate sample data
np.random.seed(42)


def example_1_subplots():
    """Example 1: Multiple subplots."""
    print("Example 1: Multiple subplots (2x2)")

    x = np.linspace(0, 10, 100)

    fig, axes = create_subplots(2, 2, venue="ieee", sharex=True)

    # Panel A: Sine
    axes[0, 0].plot(x, np.sin(x), label="sin(x)")
    axes[0, 0].set_title("(a) Sine Function")
    axes[0, 0].set_ylabel("Amplitude")
    axes[0, 0].legend()

    # Panel B: Cosine
    axes[0, 1].plot(x, np.cos(x), label="cos(x)", color="#AA0033")
    axes[0, 1].set_title("(b) Cosine Function")
    axes[0, 1].legend()

    # Panel C: Tangent (clipped)
    y_tan = np.tan(x)
    y_tan = np.clip(y_tan, -5, 5)
    axes[1, 0].plot(x, y_tan, label="tan(x)", color="#276E3D")
    axes[1, 0].set_title("(c) Tangent Function")
    axes[1, 0].set_xlabel("x (radians)")
    axes[1, 0].set_ylabel("Amplitude")
    axes[1, 0].legend()

    # Panel D: Exponential
    axes[1, 1].plot(x, np.exp(-x / 3), label="exp(-x/3)", color="#532F1A")
    axes[1, 1].set_title("(d) Exponential Decay")
    axes[1, 1].set_xlabel("x (radians)")
    axes[1, 1].legend()

    save(fig, "outputs/example_adv_01_subplots")
    print("  Saved: outputs/example_adv_01_subplots.pdf\n")


def example_2_gridspec():
    """Example 2: Complex GridSpec layout."""
    print("Example 2: GridSpec layout")

    setup_style("nature", "100yuan")
    fig, gs = create_gridspec(2, 3, venue="nature")

    x = np.linspace(0, 10, 100)

    # Top row: full width
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(x, np.sin(x), label="sin(x)")
    ax1.plot(x, np.cos(x), label="cos(x)")
    ax1.set_title("Trigonometric Functions")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.legend()
    ax1.tick_params(direction="in")

    # Bottom row: three panels
    colors = get_palette("50yuan")

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x, np.sin(2 * x), color=colors[0])
    ax2.set_title("sin(2x)")
    ax2.tick_params(direction="in")

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(x, np.cos(2 * x), color=colors[1])
    ax3.set_title("cos(2x)")
    ax3.tick_params(direction="in")

    ax4 = fig.add_subplot(gs[1, 2])
    ax4.plot(x, np.sin(x) * np.cos(x), color=colors[2])
    ax4.set_title("sin(x)·cos(x)")
    ax4.tick_params(direction="in")

    save(fig, "outputs/example_adv_02_gridspec")
    print("  Saved: outputs/example_adv_02_gridspec.pdf\n")


def example_3_twinx():
    """Example 3: Twin Y-axis plot."""
    print("Example 3: Twin Y-axis")

    setup_style("ieee", "100yuan")
    fig, ax1 = new_figure("ieee")

    x = np.linspace(0, 24, 100)
    temperature = 20 + 10 * np.sin(2 * np.pi * x / 24) + np.random.normal(0, 1, 100)
    pressure = 1013 + 20 * np.cos(2 * np.pi * x / 24) + np.random.normal(0, 2, 100)

    # Primary axis: Temperature
    color1 = "#780018"
    ax1.plot(x, temperature, color=color1, linewidth=2, label="Temperature")
    ax1.set_xlabel("Time (hours)")
    ax1.set_ylabel("Temperature (°C)", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1, direction="in")

    # Secondary axis: Pressure
    ax2 = create_twinx(ax1)
    color2 = "#276E3D"
    ax2.plot(x, pressure, color=color2, linewidth=2, linestyle="--", label="Pressure")
    ax2.set_ylabel("Pressure (hPa)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2, direction="in")

    ax1.set_title("Daily Temperature and Pressure Variation")

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    save(fig, "outputs/example_adv_03_twinx")
    print("  Saved: outputs/example_adv_03_twinx.pdf\n")


def example_4_errorbar():
    """Example 4: Error bar plot."""
    print("Example 4: Error bar plot")

    x = np.arange(1, 11)
    y = np.array([2.5, 3.8, 4.2, 5.1, 6.3, 5.8, 7.2, 8.1, 7.5, 8.8])
    yerr = np.array([0.3, 0.4, 0.35, 0.5, 0.45, 0.4, 0.55, 0.5, 0.45, 0.6])

    fig, ax = plot_errorbar(
        x,
        y,
        yerr,
        xlabel="Sample Number",
        ylabel="Measurement",
        title="Experimental Results with Error Bars",
        fmt="o",
        capsize=5,
        capthick=2,
        markersize=8,
        venue="ieee",
        palette="100yuan",
        color="#780018",
        ecolor="#AA0033",
        elinewidth=2,
        markeredgecolor="white",
        markeredgewidth=1,
    )

    save(fig, "outputs/example_adv_04_errorbar")
    print("  Saved: outputs/example_adv_04_errorbar.pdf\n")


def example_5_confidence():
    """Example 5: Confidence interval plot."""
    print("Example 5: Confidence interval")

    x = np.linspace(0, 10, 100)
    y_mean = np.sin(x) + 0.1 * x
    y_std = 0.2 + 0.1 * np.sin(x / 2) ** 2

    fig, ax = plot_confidence(
        x,
        y_mean,
        y_std,
        xlabel="x",
        ylabel="f(x)",
        title="Function with Confidence Interval",
        label_mean="Mean",
        label_std="±1 std",
        alpha=0.3,
        venue="nature",
        palette="50yuan",
    )

    save(fig, "outputs/example_adv_05_confidence")
    print("  Saved: outputs/example_adv_05_confidence.pdf\n")


def example_6_heatmap():
    """Example 6: Heatmap."""
    print("Example 6: Heatmap")

    # Generate correlation matrix
    np.random.seed(42)
    data = np.random.randn(100, 5)
    corr_matrix = np.corrcoef(data.T)

    fig, ax = plot_heatmap(
        corr_matrix,
        title="Feature Correlation Matrix",
        cmap="RdBu_r",
        show_values=True,
        fmt=".2f",
        venue="nature",
        palette="100yuan",
    )

    # Add labels
    labels = ["Feature A", "Feature B", "Feature C", "Feature D", "Feature E"]
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    save(fig, "outputs/example_adv_06_heatmap")
    print("  Saved: outputs/example_adv_06_heatmap.pdf\n")


def example_7_histogram():
    """Example 7: Histogram with multiple distributions."""
    print("Example 7: Histogram")

    setup_style("ieee", "100yuan")
    fig, ax = new_figure("ieee")

    # Generate data
    data1 = np.random.normal(0, 1, 1000)
    data2 = np.random.normal(2, 1.5, 1000)
    data3 = np.random.normal(-1, 0.5, 1000)

    colors = get_palette("100yuan")

    ax.hist(
        data1,
        bins=30,
        alpha=0.6,
        label="Distribution 1",
        color=colors[0],
        edgecolor="white",
        density=True,
    )
    ax.hist(
        data2,
        bins=30,
        alpha=0.6,
        label="Distribution 2",
        color=colors[1],
        edgecolor="white",
        density=True,
    )
    ax.hist(
        data3,
        bins=30,
        alpha=0.6,
        label="Distribution 3",
        color=colors[2],
        edgecolor="white",
        density=True,
    )

    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.set_title("Multiple Distribution Comparison")
    ax.legend()
    ax.tick_params(direction="in")

    save(fig, "outputs/example_adv_07_histogram")
    print("  Saved: outputs/example_adv_07_histogram.pdf\n")


def example_8_confusion_matrix():
    """Example 8: Confusion matrix."""
    print("Example 8: Confusion matrix")

    # Simulate confusion matrix
    classes = ["Class A", "Class B", "Class C", "Class D"]
    cm = np.array(
        [
            [85, 5, 8, 2],
            [3, 92, 3, 2],
            [6, 4, 88, 2],
            [2, 3, 5, 90],
        ]
    )

    fig, ax = plot_heatmap(
        cm,
        title="Confusion Matrix",
        cmap="Blues",
        show_values=True,
        fmt="d",
        venue="ieee",
        palette="10yuan",
    )

    ax.set_xticks(range(len(classes)))
    ax.set_yticks(range(len(classes)))
    ax.set_xticklabels(classes)
    ax.set_yticklabels(classes)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    save(fig, "outputs/example_adv_08_confusion")
    print("  Saved: outputs/example_adv_08_confusion.pdf\n")


if __name__ == "__main__":
    import os

    # Create outputs directory
    os.makedirs("outputs", exist_ok=True)

    print("=" * 60)
    print("SciPlot Advanced Usage Examples")
    print("=" * 60)
    print()

    example_1_subplots()
    example_2_gridspec()
    example_3_twinx()
    example_4_errorbar()
    example_5_confidence()
    example_6_heatmap()
    example_7_histogram()
    example_8_confusion_matrix()

    print("=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)
