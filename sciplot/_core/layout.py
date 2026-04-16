"""
布局管理 - 子图布局与保存
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec
import numpy as np

from sciplot._core.style import VENUES


PAPER_LAYOUTS: Dict[str, Dict[str, Tuple[float, float]]] = {
    "thesis": {
        "1x1": (6.1, 4.3),
        "1x2": (6.1, 3.0),
        "2x1": (6.1, 3.0),
        "2x2": (6.1, 5.0),
        "1x3": (6.1, 2.2),
        "3x1": (6.1, 2.2),
    },
    "ieee": {
        "1x1": (3.5, 3.0),
        "1x2": (3.5, 1.6),
        "2x1": (7.16, 1.6),
        "2x2": (3.5, 2.8),
        "1x3": (3.5, 1.2),
        "3x1": (7.16, 1.2),
    },
    "nature": {
        "1x1": (7.0, 5.0),
        "1x2": (3.5, 2.8),
        "2x1": (7.0, 2.8),
        "2x2": (3.5, 2.8),
        "1x3": (3.5, 2.0),
        "3x1": (7.0, 2.0),
    },
    "aps": {
        "1x1": (3.4, 2.8),
        "1x2": (3.4, 1.5),
        "2x1": (7.0, 1.5),
        "2x2": (3.4, 2.6),
    },
    "springer": {
        "1x1": (6.0, 4.5),
        "1x2": (6.0, 2.5),
        "2x2": (6.0, 4.2),
    },
}


def new_figure(
    venue: str = "nature",
    figsize: Optional[Tuple[float, float]] = None,
    **kwargs: Any,
) -> Tuple[Figure, Axes]:
    """
    创建新图形，自动套用 venue 尺寸

    参数:
        venue  : 期刊预设
        figsize: 自定义 (宽, 高) 英寸
        **kwargs: 传递给 plt.subplots()

    返回:
        (Figure, Axes)
    """
    if venue not in VENUES:
        raise ValueError(f"未知 venue '{venue}'，可用选项: {list(VENUES.keys())}")
    _, default_figsize, _ = VENUES[venue]
    size = figsize if figsize is not None else default_figsize
    return plt.subplots(figsize=size, **kwargs)


def save(
    fig: Figure,
    name: str,
    dpi: int = 1200,
    formats: Tuple[str, ...] = ("pdf", "png"),
    bbox_inches: str = "tight",
    dir: Optional[str] = None,
    **kwargs: Any,
) -> List[Path]:
    """
    保存图形

    参数:
        fig        : 图形对象
        name       : 文件名（不含扩展名）
        dpi        : 位图分辨率
        formats    : 输出格式
        bbox_inches: 边距裁剪
        dir        : 保存目录

    返回:
        已保存文件的路径列表
    """
    VECTOR_FORMATS = {"pdf", "svg", "eps"}

    save_dir = Path(dir) if dir else Path.cwd()
    save_dir.mkdir(parents=True, exist_ok=True)

    saved_paths: List[Path] = []
    for fmt in formats:
        path = save_dir / f"{name}.{fmt}"
        extra = {} if fmt in VECTOR_FORMATS else {"dpi": dpi}
        fig.savefig(path, bbox_inches=bbox_inches, format=fmt, **extra, **kwargs)
        saved_paths.append(path)
    return saved_paths


def create_subplots(
    nrows: int = 1,
    ncols: int = 1,
    venue: str = "nature",
    layout: Optional[str] = None,
    sharex: bool = False,
    sharey: bool = False,
    **kwargs: Any,
) -> Tuple[Figure, Union[Axes, np.ndarray]]:
    """
    创建规则网格子图布局

    参数:
        nrows   : 行数
        ncols   : 列数
        venue   : 期刊预设
        layout  : 论文布局字符串，如 "1x2"
        sharex  : 是否共享 X 轴
        sharey  : 是否共享 Y 轴
    """
    from sciplot._core.style import setup_style
    setup_style(venue)

    layout_key = f"{nrows}x{ncols}"
    if layout and venue in PAPER_LAYOUTS:
        figsize = PAPER_LAYOUTS.get(venue, {}).get(layout)
    else:
        _, figsize, _ = VENUES[venue]
        figsize = (figsize[0] * ncols * 0.8, figsize[1] * nrows * 0.8)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize,
                             sharex=sharex, sharey=sharey, **kwargs)
    ax_iter = axes.flat if isinstance(axes, np.ndarray) else [axes]
    for ax in ax_iter:
        ax.tick_params(direction="in")
    return fig, axes


def paper_subplots(
    nrows: int = 1,
    ncols: int = 1,
    venue: str = "thesis",
    **kwargs: Any,
) -> Tuple[Figure, Union[Axes, np.ndarray]]:
    """
    创建符合论文规范的子图布局

    参数:
        nrows   : 行数
        ncols   : 列数
        venue   : 论文类型
    """
    from sciplot._core.style import setup_style

    layout_key = f"{nrows}x{ncols}"
    figsize = (6.1, 4.3)

    if venue in PAPER_LAYOUTS:
        figsize = PAPER_LAYOUTS[venue].get(layout_key)
        if figsize is None:
            _, default_figsize, _ = VENUES[venue]
            figsize = (default_figsize[0] * ncols * 0.8, default_figsize[1] * nrows * 0.8)

    setup_style(venue)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, **kwargs)
    ax_iter = axes.flat if isinstance(axes, np.ndarray) else [axes]
    for ax in ax_iter:
        ax.tick_params(direction="in")
    return fig, axes


def create_gridspec(
    nrows: int = 1,
    ncols: int = 1,
    venue: str = "nature",
    **kwargs: Any,
) -> Tuple[Figure, GridSpec]:
    """
    创建 GridSpec 复杂不规则布局
    """
    from sciplot._core.style import setup_style
    setup_style(venue)
    _, figsize, _ = VENUES[venue]
    fig = plt.figure(figsize=figsize)
    gs = GridSpec(nrows, ncols, figure=fig, **kwargs)
    return fig, gs


def create_twinx(ax: Axes) -> Axes:
    """创建共享 X 轴的副 Y 轴"""
    ax2 = ax.twinx()
    ax2.tick_params(direction="in")
    return ax2


def list_paper_layouts(venue: Optional[str] = None) -> Dict[str, Dict[str, Tuple[float, float]]]:
    """
    列出论文子图布局尺寸配置
    """
    if venue:
        return {venue: PAPER_LAYOUTS.get(venue, {})}
    return PAPER_LAYOUTS
