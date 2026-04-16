"""
SciPlot 图表模块
"""

from sciplot._plots.basic import (
    plot_line,
    plot_multi,
    plot_multi_line,
    plot_scatter,
)
from sciplot._plots.distribution import (
    plot_bar,
    plot_box,
    plot_violin,
    plot_histogram,
)
from sciplot._plots.advanced import (
    plot_errorbar,
    plot_confidence,
    plot_heatmap,
)

__all__ = [
    "plot_line",
    "plot_multi",
    "plot_multi_line",
    "plot_scatter",
    "plot_bar",
    "plot_box",
    "plot_violin",
    "plot_histogram",
    "plot_errorbar",
    "plot_confidence",
    "plot_heatmap",
]
