"""
SciPlot 项目初始化脚本
在任何工作目录运行此脚本，快速搭建 sciplot 绘图骨架

使用方法:
    1. 复制此文件到项目根目录
    2. 运行: python project_init.py
    3. 自动生成 plotting.py 配置文件

或者让 AI 直接执行:
    exec(open("project_init.py").read())
"""

import os
import sys
from pathlib import Path

# ============================================================
# 配置模板
# ============================================================

PLOTTING_PY_TEMPLATE = '''"""
{project_name} - 绘图配置模块
基于 SciPlot 的统一定制配置

此文件由 project_init.py 自动生成
修改此文件可自定义项目级绘图风格
"""

import sys
from pathlib import Path

# ============================================================
# 自动查找并导入 sciplot
# ============================================================

def _find_sciplot():
    """在常见位置查找 sciplot"""
    try:
        import sciplot
        return sciplot
    except ImportError:
        pass

    possible_paths = [
        Path(__file__).parent,
        Path.cwd(),
        Path(__file__).parent.parent,
    ]

    for path in possible_paths:
        if path.exists() and (path / "sciplot" / "__init__.py").exists():
            sys.path.insert(0, str(path.parent))
            try:
                import sciplot
                return sciplot
            except ImportError:
                if str(path.parent) in sys.path:
                    sys.path.remove(str(path.parent))
                continue

    raise ImportError(
        "无法找到 sciplot。请确保:\n"
        "1. 已运行: uv pip install -e /path/to/sciplot\n"
        "2. 或将 sciplot 目录复制到本项目"
    )

# 导入 sciplot
sp = _find_sciplot()

# 重新导出所有常用函数和常量
from sciplot import (
    # 核心函数
    plot, plot_multi, save,
    plot_line, plot_multi_line, plot_scatter, plot_bar,
    plot_box, plot_violin, plot_errorbar, plot_confidence,
    plot_heatmap, plot_histogram,
    create_subplots, create_gridspec, create_twinx,
    setup_style, new_figure,
    # 工具函数
    get_palette, list_palettes, list_resident_palettes,
    list_pastel_subsets, list_earth_subsets, list_ocean_subsets,
    # 常量
    RESIDENT_PALETTES, PASTEL_PALETTE, EARTH_PALETTE, OCEAN_PALETTE,
    RMB_PALETTES, TOL_PALETTES,
    VENUES, LANGUAGES, LINE_STYLES, MARKERS,
    DEFAULT_PALETTE,
    # 元信息
    __version__, HAS_SCIENCEPLOTS,
)

# ============================================================
# 项目级默认配置（可根据需要修改）
# ============================================================

DEFAULT_VENUE = "nature"           # 默认期刊样式
DEFAULT_PALETTE = "pastel"         # 默认配色
DEFAULT_LANG = "zh"                # 默认中文

# 项目专用配色（可选）
PROJECT_COLORS = {{
    # 添加项目专用颜色
    # "primary": "#264653",
    # "secondary": "#2a9d8f",
}}

# ============================================================
# 便捷函数（项目级预设）
# ============================================================

def fig(**kwargs):
    """创建新图（使用项目默认配置）"""
    return new_figure(venue=kwargs.get("venue", DEFAULT_VENUE))


def multi(x, y_list, **kwargs):
    """绘制多线图（使用项目默认配置）"""
    return plot_multi(
        x, y_list,
        venue=kwargs.pop("venue", DEFAULT_VENUE),
        palette=kwargs.pop("palette", DEFAULT_PALETTE),
        **kwargs
    )


def line(x, y, **kwargs):
    """绘制单线图（使用项目默认配置）"""
    return plot_line(
        x, y,
        venue=kwargs.pop("venue", DEFAULT_VENUE),
        palette=kwargs.pop("palette", DEFAULT_PALETTE),
        **kwargs
    )


# ============================================================
# 版本信息
# ============================================================
__version__ = "1.0.0"
__sci_plot_version__ = getattr(sp, "__version__", "unknown")
'''


INIT_PY_TEMPLATE = '''"""
{project_name} - 绘图模块

使用方式:
    from plotting import plot, plot_multi, save, sp
    # 或
    import plotting as pl
"""

from .plotting import *
'''


EXAMPLE_PY_TEMPLATE = '''"""
SciPlot 使用示例 - {project_name}
"""

import numpy as np

# 导入项目绘图模块
from plotting import plot, plot_multi, save, sp

# 或使用简化别名
# from plotting import line, multi, fig


def example_single_line():
    """单线图示例"""
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plot(x, y, xlabel="时间 (s)", ylabel="电压 (V)", title="正弦波")
    save(fig, "example_single")


def example_multi_line():
    """多线图示例"""
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(x)

    # 3条线自动使用 pastel-3
    fig, ax = plot_multi(
        x, [y1, y2, y3],
        labels=["正弦", "余弦", "混合"],
        xlabel="时间 (s)",
        ylabel="幅值",
        title="三角函数对比"
    )
    save(fig, "example_multi")


def example_earth_palette():
    """使用 earth 配色示例"""
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    fig, ax = plot_multi(
        x, [y1, y2],
        labels=["实验组", "对照组"],
        xlabel="迭代次数",
        ylabel="准确率 (%)",
        palette="earth"  # 自动使用 earth-2
    )
    save(fig, "example_earth")


def example_ocean_palette():
    """使用 ocean 配色示例"""
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * 0.5

    fig, ax = plot_multi(
        x, [y1, y2, y3],
        labels=["方法A", "方法B", "方法C"],
        xlabel="样本数",
        ylabel="性能指标",
        palette="ocean"  # 自动使用 ocean-3
    )
    save(fig, "example_ocean")


def example_box_plot():
    """箱线图示例"""
    from plotting import plot_box, save

    # 生成三组数据
    np.random.seed(42)
    data_a = np.random.normal(100, 10, 200)
    data_b = np.random.normal(105, 15, 200)
    data_c = np.random.normal(95, 8, 200)

    fig, ax = plot_box(
        [data_a, data_b, data_c],
        labels=["方法A", "方法B", "方法C"],
        xlabel="算法",
        ylabel="准确率 (%)",
        title="三种方法性能对比"
    )
    save(fig, "example_box")


def example_violin_plot():
    """小提琴图示例"""
    from plotting import plot_violin, save

    # 生成两组数据
    np.random.seed(42)
    data_x = np.random.normal(0, 1, 1000)
    data_y = np.random.normal(0.5, 1.5, 1000)

    fig, ax = plot_violin(
        [data_x, data_y],
        labels=["实验组", "对照组"],
        xlabel="分组",
        ylabel="测量值",
        title="数据分布对比",
        showmedians=True
    )
    save(fig, "example_violin")


if __name__ == "__main__":
    print("运行 SciPlot 示例...")
    example_single_line()
    example_multi_line()
    example_earth_palette()
    example_ocean_palette()
    example_box_plot()
    example_violin_plot()
    print("示例完成！请查看生成的图片。")
'''


def init_project(project_path: str = None, project_name: str = None):
    """
    初始化项目绘图配置

    参数:
        project_path: 项目路径，默认为当前目录
        project_name: 项目名称，默认为目录名
    """
    # 确定项目路径
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    # 确定项目名称
    if project_name is None:
        project_name = project_path.name or "my_project"

    print(f"=" * 50)
    print(f"SciPlot 项目初始化")
    print(f"=" * 50)
    print(f"项目路径: {project_path.absolute()}")
    print(f"项目名称: {project_name}")
    print()

    # 创建 plotting.py
    plotting_file = project_path / "plotting.py"
    plotting_content = PLOTTING_PY_TEMPLATE.format(project_name=project_name)

    with open(plotting_file, "w", encoding="utf-8") as f:
        f.write(plotting_content)

    print(f"[✓] 创建: {plotting_file}")

    # 创建示例文件
    example_file = project_path / "plotting_example.py"
    example_content = EXAMPLE_PY_TEMPLATE.format(project_name=project_name)

    with open(example_file, "w", encoding="utf-8") as f:
        f.write(example_content)

    print(f"[✓] 创建: {example_file}")

    # 创建说明文件
    readme_file = project_path / "SCIPLOT_USAGE.md"
    readme_content = f'''# SciPlot 使用指南

## 快速开始

### 1. 基础绘图

```python
from plotting import plot, plot_multi, save
import numpy as np

# 单线图
x = np.linspace(0, 10, 100)
fig, ax = plot(x, np.sin(x), xlabel="时间", ylabel="电压")
save(fig, "结果图")

# 多线图（自动配色）
fig, ax = plot_multi(x, [y1, y2, y3], labels=["A", "B", "C"])
save(fig, "对比图")
```

### 2. 配色方案

三大常驻配色系（都有1-4色子集）：
- `pastel` (默认): 柔和粉彩
- `earth`: 大地色系
- `ocean`: 海洋蓝绿

```python
# 使用 earth 配色
fig, ax = plot_multi(x, [y1, y2], palette="earth")

# 使用 ocean 配色
fig, ax = plot_multi(x, [y1, y2, y3], palette="ocean")
```

### 3. 项目级预设

修改 `plotting.py` 中的 `DEFAULT_VENUE`, `DEFAULT_PALETTE` 等变量，
可统一改变整个项目的绘图风格。

### 4. 查看所有配色

```python
from plotting import list_palettes, list_resident_palettes

print(list_resident_palettes())  # 三大配色系
print(list_palettes())           # 所有配色
```

## 文件说明

- `plotting.py`: 项目绘图配置（可自定义）
- `plotting_example.py`: 使用示例
- `figures/`: 生成的图片保存目录

## 依赖安装

确保已安装 sciplot:
```bash
uv pip install -e d:/ZPan/PythonPackage/sciplot
```
'''

    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"[✓] 创建: {readme_file}")

    print()
    print("=" * 50)
    print("初始化完成！")
    print("=" * 50)
    print()
    print("下一步:")
    print("  1. 确保已安装 sciplot:")
    print("     uv pip install -e d:/ZPan/PythonPackage/sciplot")
    print()
    print("  2. 运行示例:")
    print("     python plotting_example.py")
    print()
    print("  3. 在你的代码中使用:")
    print("     from plotting import plot, plot_multi, save")
    print()


# 如果直接运行此脚本
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SciPlot 项目初始化")
    parser.add_argument("--path", "-p", help="项目路径", default=None)
    parser.add_argument("--name", "-n", help="项目名称", default=None)

    args = parser.parse_args()

    init_project(args.path, args.name)
