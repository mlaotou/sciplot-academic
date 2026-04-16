"""
SciPlot — 科研绘图库 (Scientific Plotting Library)

基于 Matplotlib + SciencePlots 的期刊级科研绘图封装库，专为中文科研场景优化。

安装:
    pip install sciplot-academic
    uv pip install sciplot-academic

快速上手:
    >>> import sciplot as sp
    >>> import numpy as np
    >>> x = np.linspace(0, 10, 200)
    >>> fig, ax = sp.plot(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
    >>> sp.save(fig, "结果图")

================================================================================
功能特性
================================================================================

期刊样式：
    nature (默认) | ieee | aps | springer | thesis | presentation

三大常驻配色系（每种都有 1-4 色子集）：
    pastel (默认): 柔和粉彩  pastel-1/2/3/4
    earth        : 大地色系  earth-1/2/3/4
    ocean        : 海洋蓝绿  ocean-1/2/3/4

其他配色：
    rainbow-N (N=1-23) | bright | vibrant | muted | light | high-vis
    100yuan | 50yuan | 20yuan | 10yuan | 5yuan | 1yuan

图表类型：
    plot / plot_multi / plot_scatter / plot_bar / plot_box / plot_violin
    plot_errorbar / plot_confidence / plot_heatmap / plot_histogram

================================================================================
作者: SciPlot Team
版本: 1.5.0
================================================================================
"""

__version__ = "1.5.0"
__author__ = "SciPlot Team"

import warnings

try:
    import scienceplots  # noqa: F401
    HAS_SCIENCEPLOTS = True
except ImportError:
    warnings.warn(
        "scienceplots 未安装，请运行: pip install scienceplots",
        ImportWarning,
        stacklevel=2,
    )
    HAS_SCIENCEPLOTS = False


from sciplot._core.style import (
    setup_style,
    reset_style,
    get_venue_info,
    list_venues,
    list_languages,
    VENUES,
    LANGUAGES,
)
from sciplot._core.palette import (
    set_custom_palette,
    get_palette,
    list_palettes,
    list_all_palettes,
    list_resident_palettes,
    list_pastel_subsets,
    list_earth_subsets,
    list_ocean_subsets,
    list_rmb_palettes,
    list_tol_palettes,
    DEFAULT_PALETTE,
    RMB_PALETTES,
    RESIDENT_PALETTES,
    PASTEL_PALETTE,
    EARTH_PALETTE,
    OCEAN_PALETTE,
    TOL_PALETTES,
    ALL_PALETTES,
)
from sciplot._core.layout import (
    new_figure,
    create_subplots,
    paper_subplots,
    create_gridspec,
    create_twinx,
    save,
    list_paper_layouts,
    PAPER_LAYOUTS,
)
from sciplot._plots.basic import (
    plot_line,
    plot,
    plot_multi,
    plot_multi_line,
    plot_scatter,
    LINE_STYLES,
    MARKERS,
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
    "__version__",
    # 核心
    "setup_style", "reset_style", "new_figure", "save",
    # 图表
    "plot", "plot_line", "plot_multi", "plot_multi_line",
    "plot_scatter", "plot_bar", "plot_box", "plot_violin", "plot_histogram",
    "plot_errorbar", "plot_confidence", "plot_heatmap",
    # 布局
    "create_subplots", "paper_subplots", "create_gridspec", "create_twinx",
    # 工具
    "get_palette", "list_palettes", "list_all_palettes",
    "list_resident_palettes", "list_pastel_subsets", "list_earth_subsets", "list_ocean_subsets",
    "list_rmb_palettes", "list_tol_palettes",
    "list_venues", "list_languages", "list_paper_layouts",
    "get_venue_info", "set_custom_palette",
    # 常量
    "RMB_PALETTES", "RESIDENT_PALETTES", "PASTEL_PALETTE", "EARTH_PALETTE", "OCEAN_PALETTE",
    "TOL_PALETTES", "VENUES", "PAPER_LAYOUTS", "LANGUAGES",
    "LINE_STYLES", "MARKERS", "DEFAULT_PALETTE", "ALL_PALETTES",
    # 状态
    "HAS_SCIENCEPLOTS",
]
