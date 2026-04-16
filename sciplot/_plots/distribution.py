"""
分布图表 - 柱状图、箱线图、小提琴图、直方图
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sciplot._core.style import setup_style
from sciplot._core.palette import DEFAULT_PALETTE
from sciplot._core.layout import new_figure


def plot_bar(
    categories: List[str],
    values: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    width: float = 0.6,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制柱状图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = [c["color"] for c in prop_cycle]
    bar_colors = [colors[i % len(colors)] for i in range(len(categories))]
    ax.bar(categories, values, width=width, color=bar_colors, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax


def plot_box(
    data: Union[np.ndarray, List[np.ndarray]],
    labels: Optional[List[str]] = None,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    showfliers: bool = True,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制箱线图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = [c["color"] for c in prop_cycle]
    bp = ax.boxplot(data, labels=labels, showfliers=showfliers, patch_artist=True, **kwargs)
    for i, patch in enumerate(bp["boxes"]):
        patch.set_facecolor(colors[i % len(colors)])
        patch.set_alpha(0.7)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax


def plot_violin(
    data: Union[np.ndarray, List[np.ndarray]],
    labels: Optional[List[str]] = None,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    showmeans: bool = False,
    showmedians: bool = True,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制小提琴图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    parts = ax.violinplot(data, showmeans=showmeans, showmedians=showmedians, **kwargs)
    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = [c["color"] for c in prop_cycle]
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i % len(colors)])
        pc.set_alpha(0.7)
    if labels:
        ax.set_xticks(range(1, len(labels) + 1))
        ax.set_xticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax


def plot_histogram(
    data: np.ndarray,
    bins: int = 30,
    xlabel: str = "",
    ylabel: str = "Frequency",
    title: str = "",
    density: bool = False,
    alpha: float = 0.7,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制直方图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    ax.hist(data, bins=bins, density=density, alpha=alpha, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax
