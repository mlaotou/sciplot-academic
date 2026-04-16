"""
SciPlot 核心模块
"""

from sciplot._core.registry import (
    PlotterMetadata,
    PLOTTER_REGISTRY,
    register_plotter,
    get_plotter,
    list_plotters,
)
from sciplot._core.style import setup_style, reset_style
from sciplot._core.palette import (
    set_custom_palette,
    get_palette,
)
from sciplot._core.layout import (
    new_figure,
    create_subplots,
    paper_subplots,
    create_gridspec,
    create_twinx,
    save,
)

__all__ = [
    # 注册机制
    "PlotterMetadata",
    "PLOTTER_REGISTRY",
    "register_plotter",
    "get_plotter",
    "list_plotters",
    # 样式
    "setup_style",
    "reset_style",
    # 配色
    "set_custom_palette",
    "get_palette",
    # 布局
    "new_figure",
    "create_subplots",
    "paper_subplots",
    "create_gridspec",
    "create_twinx",
    "save",
]
