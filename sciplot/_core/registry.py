"""
图表注册中心 - 支持可扩展的图表类型
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from matplotlib.figure import Figure
    from matplotlib.axes import Axes


@dataclass
class PlotterMetadata:
    """图表元数据"""
    name: str
    category: str
    supported_venues: List[str] = field(default_factory=lambda: ["nature", "ieee", "thesis"])
    default_params: Dict[str, Any] = field(default_factory=dict)
    description: str = ""


PLOTTER_REGISTRY: Dict[str, PlotterMetadata] = {}


def register_plotter(
    name: str,
    category: str = "basic",
    supported_venues: Optional[List[str]] = None,
    description: str = "",
    **default_params: Any,
) -> Callable:
    """
    装饰器：注册新的图表类型

    参数:
        name: 图表名称，用于调用如 plot_xxx()
        category: 分类，可选 basic/distribution/ml/3d
        supported_venues: 支持的 venue 列表
        description: 图表描述
        **default_params: 默认参数

    示例:
        @register_plotter("pca", category="ml", description="PCA 可视化")
        def plot_pca(data, **kwargs):
            ...
    """
    def decorator(func: Callable) -> Callable:
        PLOTTER_REGISTRY[name] = PlotterMetadata(
            name=name,
            category=category,
            supported_venues=supported_venues or ["nature", "ieee", "thesis"],
            default_params=default_params,
            description=description,
        )
        return func
    return decorator


def get_plotter(name: str) -> PlotterMetadata:
    """获取图表元数据"""
    if name not in PLOTTER_REGISTRY:
        available = list(PLOTTER_REGISTRY.keys())
        raise ValueError(
            f"未找到图表 '{name}'。可用图表: {available}"
        )
    return PLOTTER_REGISTRY[name]


def list_plotters(category: Optional[str] = None) -> Dict[str, PlotterMetadata]:
    """
    列出已注册的图表类型

    参数:
        category: 可选，按分类过滤

    返回:
        图表名称 -> 元数据 的字典
    """
    if category:
        return {k: v for k, v in PLOTTER_REGISTRY.items() if v.category == category}
    return dict(PLOTTER_REGISTRY)


def create_plot_func(name: str) -> Callable:
    """
    动态创建图表函数的工厂函数
    用于用户自定义扩展图表
    """
    metadata = get_plotter(name)

    def plot_func(*args, **kwargs):
        from sciplot import setup_style, new_figure

        venue = kwargs.pop("venue", "nature")
        palette = kwargs.pop("palette", "pastel")

        setup_style(venue, palette)
        fig, ax = new_figure(venue)
        return fig, ax

    return plot_func
