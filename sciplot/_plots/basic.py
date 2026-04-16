"""
基础图表 - 折线图、散点图
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sciplot._core.style import setup_style
from sciplot._core.palette import DEFAULT_PALETTE
from sciplot._core.layout import new_figure


LINE_STYLES: List[str] = ["-", "--", "-.", ":"]
MARKERS: List[str] = ["o", "s", "^", "D", "v", "<", ">", "p", "*", "h"]


def plot_line(
    x: np.ndarray,
    y: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    label: str = "",
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制单条折线图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    ax.plot(x, y, label=label, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if label:
        ax.legend()
    ax.tick_params(direction="in")
    return fig, ax


plot = plot_line


def plot_multi(
    x: Union[np.ndarray, List[np.ndarray]],
    y_list: List[np.ndarray],
    labels: Optional[List[str]] = None,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制多条折线图，自动智能选择配色子集"""
    n_lines = len(y_list)
    if n_lines <= 4 and palette in ("pastel", "earth", "ocean"):
        palette = f"{palette}-{n_lines}"

    return plot_multi_line(
        x, y_list, labels=labels,
        xlabel=xlabel, ylabel=ylabel, title=title,
        venue=venue, palette=palette,
        use_linestyles=False, **kwargs
    )


def plot_multi_line(
    x: Union[np.ndarray, List[np.ndarray]],
    y_list: List[np.ndarray],
    labels: Optional[List[str]] = None,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    use_linestyles: bool = False,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制多线折线图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    if labels is None:
        labels = [f"Series {i + 1}" for i in range(len(y_list))]
    for i, (y, lbl) in enumerate(zip(y_list, labels)):
        xi = x if isinstance(x, np.ndarray) else x[i]
        ls = LINE_STYLES[i % len(LINE_STYLES)] if use_linestyles else "-"
        ax.plot(xi, y, label=lbl, linestyle=ls, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend()
    ax.tick_params(direction="in")
    return fig, ax


def plot_scatter(
    x: np.ndarray,
    y: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    s: float = 20,
    alpha: float = 0.7,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制散点图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    ax.scatter(x, y, s=s, alpha=alpha, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax
