"""
SciPlot 扩展模块
包含机器学习可视化、3D 可视化等高级功能
"""

__all__ = []

def __getattr__(name):
    """延迟导入扩展模块"""
    if name == "ml":
        try:
            from sciplot._ext import ml
            return ml
        except ImportError:
            raise AttributeError(f"扩展模块 'ml' 需要额外依赖")
    if name == "plot3d":
        try:
            from sciplot._ext import plot3d
            return plot3d
        except ImportError:
            raise AttributeError(f"扩展模块 'plot3d' 需要额外依赖")
    raise AttributeError(f"模块 'sciplot._ext' 没有属性 '{name}'")
