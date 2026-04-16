"""
高级图表 - 误差条、置信区间、热力图
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from sciplot._core.style import setup_style
from sciplot._core.palette import DEFAULT_PALETTE
from sciplot._core.layout import new_figure


def plot_errorbar(
    x: np.ndarray,
    y: np.ndarray,
    yerr: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    fmt: str = "o",
    capsize: float = 4,
    markersize: float = 5,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """绘制误差条图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    ax.errorbar(x, y, yerr=yerr, fmt=fmt, capsize=capsize,
                markersize=markersize, **kwargs)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax


def plot_confidence(
    x: np.ndarray,
    y_mean: np.ndarray,
    y_std: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    label_mean: str = "Mean",
    label_std: str = "±1σ",
    alpha: float = 0.25,
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
) -> Tuple[Figure, Axes]:
    """绘制带置信区间的折线图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    (line,) = ax.plot(x, y_mean, label=label_mean)
    color = line.get_color()
    ax.fill_between(x, y_mean - y_std, y_mean + y_std,
                    alpha=alpha, color=color, label=label_std)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend()
    ax.tick_params(direction="in")
    return fig, ax


def plot_heatmap(
    data: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    cmap: str = "Blues",
    show_values: bool = False,
    fmt: str = ".2f",
    venue: str = "nature",
    palette: str = DEFAULT_PALETTE,
) -> Tuple[Figure, Axes]:
    """绘制热力图"""
    setup_style(venue, palette)
    fig, ax = new_figure(venue)
    im = ax.imshow(data, cmap=cmap, aspect="auto")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if show_values:
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                ax.text(j, i, format(data[i, j], fmt),
                        ha="center", va="center", fontsize=9)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.tick_params(direction="in")
    return fig, ax
