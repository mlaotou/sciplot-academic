# SciPlot Academic v1.7.5 → v1.8.0 优化方案

## 一、紧急：必须修复的致命 Bug（会导致模块无法导入）

---

### Bug 1：`list_rmb_palettes` ImportError

**现象：** `import sciplot` 会直接报 ImportError。

`__init__.py` 第 58 行：
```python
from sciplot._core.palette import (
    ...
    list_rmb_palettes,   # ← 这个函数已经从 palette.py 中删除了！
    ...
)
```

但当前 `palette.py` 里完全没有 `list_rmb_palettes` 的定义，
人民币配色 `RMB_PALETTES` 字典本身也被删掉了。

**根因：** Kimi/Codex 在重构配色体系时把人民币系列整体移除了，
但 `__init__.py` 的导出列表没有同步更新。

**修复（两选一，推荐 B）：**

选项 A（临时打补丁，不推荐）：在 `__init__.py` 把 `list_rmb_palettes` 从导入里删掉。

选项 B（正确做法）：把人民币配色**加回来**。这本来就是你的特色配色，
不应该被删掉。在 `palette.py` 加回 `RMB_PALETTES` 并注册到 `RESIDENT_PALETTES`：

```python
# palette.py 新增（紧跟 SUNSET_PALETTE 之后）
RMB_PALETTES: Dict[str, List[str]] = {
    "100yuan": ["#780018", "#AA0033", "#DD0022", "#CC0044", "#FA8095"],
    "50yuan":  ["#25362B", "#276E3D", "#56B76A", "#3C4061", "#8E8E99"],
    "20yuan":  ["#532F1A", "#6B4E25", "#7F5643", "#796A5D", "#BE9A62"],
    "10yuan":  ["#242F4D", "#465A66", "#6382AA", "#828E99", "#7F606D"],
    "5yuan":   ["#413A4C", "#63576F", "#56B76A", "#6F8DB1", "#B3A479"],
    "1yuan":   ["#3C3F27", "#5A5745", "#9DA780", "#937539", "#C5AB71"],
}

RESIDENT_PALETTES: Dict[str, List[str]] = {
    **PASTEL_PALETTE,
    **OCEAN_PALETTE,
    **FOREST_PALETTE,
    **SUNSET_PALETTE,
    **RMB_PALETTES,   # ← 重新加入
}

def list_rmb_palettes() -> List[str]:
    """列出人民币配色方案名称"""
    return list(RMB_PALETTES.keys())
```

---

### Bug 2：`EARTH_PALETTE` 孤立，`apply_palette("earth")` 会报错

**现象：** 用户调用 `sp.setup_style(palette="earth")` 会得到：
```
ValueError: 未知配色方案 'earth'
```

`EARTH_PALETTE` 在 `palette.py` 里有定义，`list_earth_subsets()` 函数也有，
但 `EARTH_PALETTE` **没有被合并进 `RESIDENT_PALETTES`**。
所以 earth 系列颜色完全无法被 `apply_palette` 识别。

**修复：** 在组合 `RESIDENT_PALETTES` 时加入 `**EARTH_PALETTE`（同 Bug 1 的修复一起做）。

---

### Bug 3：可选依赖在顶层强制导入

**现象：** 没有安装 networkx 的用户 `import sciplot` 直接崩：
```
ImportError: No module named 'networkx'
```

`__init__.py` 里直接写了：
```python
from sciplot._ext.network import (
    plot_network,
    plot_network_from_matrix,
    plot_network_communities,
)
from sciplot._ext.venn import (
    plot_venn2,
    plot_venn3,
)
```

scipy 也被加进了 `pyproject.toml` 的 `dependencies`（core 依赖），
但它实际只被 `statistical.py` 和 `hierarchical.py` 用，属于重量级可选库。

**修复方案：** 改成懒导入 + 友好错误提示。

```python
# __init__.py 改成懒加载方式
def __getattr__(name: str):
    _LAZY_EXT = {
        "plot_network":            ("sciplot._ext.network",      "networkx"),
        "plot_network_from_matrix":("sciplot._ext.network",      "networkx"),
        "plot_network_communities":("sciplot._ext.network",       "networkx"),
        "plot_venn2":              ("sciplot._ext.venn",          "matplotlib-venn"),
        "plot_venn3":              ("sciplot._ext.venn",          "matplotlib-venn"),
        "plot_dendrogram":         ("sciplot._ext.hierarchical",  "scipy"),
        "plot_clustermap":         ("sciplot._ext.hierarchical",  "scipy"),
    }
    if name in _LAZY_EXT:
        module_path, dep_name = _LAZY_EXT[name]
        try:
            import importlib
            mod = importlib.import_module(module_path)
            return getattr(mod, name)
        except ImportError:
            raise ImportError(
                f"sp.{name}() 需要安装 {dep_name}。\n"
                f"请运行: pip install {dep_name}"
            ) from None
    raise AttributeError(f"module 'sciplot' has no attribute {name!r}")
```

同时在 `pyproject.toml` 把 scipy 从 `dependencies` 移到 `[project.optional-dependencies]`：
```toml
[project.optional-dependencies]
statistical = ["scipy>=1.7.0"]
ml = ["scikit-learn>=1.0.0"]
network = ["networkx>=2.6.0"]
venn = ["matplotlib-venn>=0.11.0"]
all = ["scipy>=1.7.0", "scikit-learn>=1.0.0", "networkx>=2.6.0", "matplotlib-venn>=0.11.0"]
```

---

### Bug 4：`plot_multi` 默认 `palette=None` 时智能子集失效

**现象：** 用户调用 `sp.plot_multi(x, [y1, y2])` 期望自动选 pastel-2，
但实际上不会触发自动子集，会用完整的 pastel（6色）。

```python
# basic.py 当前代码
def plot_multi(..., palette: Optional[str] = None, ...):
    n = len(y_list)
    effective_palette = palette          # ← None
    if n <= 4 and palette in ("pastel", "earth", "ocean"):  # ← None not in (...)，永远 False
        effective_palette = f"{palette}-{n}"
```

**修复：** 把 None 视为 DEFAULT_PALETTE 来处理，并扩展支持所有系列：

```python
from sciplot._core.palette import DEFAULT_PALETTE, RESIDENT_PALETTES

_AUTO_SUBSET_BASES = {"pastel", "ocean", "forest", "sunset", "earth"}

def plot_multi(..., palette: Optional[str] = None, ...):
    n = len(y_list)
    effective_palette = palette or DEFAULT_PALETTE

    # 智能子集：对支持子集的配色，自动选合适数量
    base_name = effective_palette  # 如 "pastel"、"ocean-3" 的 base 是 "ocean"
    for base in _AUTO_SUBSET_BASES:
        if effective_palette == base and f"{base}-{n}" in RESIDENT_PALETTES:
            effective_palette = f"{base}-{n}"
            break

    return plot_multi_line(
        x, y_list, ..., palette=effective_palette, ...
    )
```

---

### Bug 5：`aliases.py` 返回类型注解错误

所有 alias 函数的返回类型标注是 `Tuple[Figure, Axes]`，
但实际返回的是 `PlotResult`（因为底层函数已经返回 PlotResult）。

```python
# 当前 aliases.py（错的）
def line(...) -> Tuple[Figure, Axes]:
    return plot_line(...)   # ← plot_line 返回 PlotResult

# 应该是
def line(...) -> PlotResult:
    return plot_line(...)
```

IDE 自动补全和类型检查工具（mypy/pyright）会给出错误提示，影响使用体验。

---

## 二、架构层：值得系统性解决的设计问题

---

### Issue 1：`PlotResult` 与 `FigureWrapper` 是两套并行体系

**现状：**
- 普通绘图函数（`plot_line` 等）返回 `PlotResult`
- `FluentAPI` 的 `PlotChain.plot()` 返回 `FigureWrapper`
- 两者都支持链式调用，但 API 不一样，功能也不完全对等

**影响：**
- 用户切换用法时要学两套接口
- `FigureWrapper` 上的 `.xlabel()` 和 `PlotResult` 上的 `.xlabel()` 行为一致，
  但是独立维护，未来改一个要改两个，容易出 bug

**建议：** 让 `FigureWrapper` 继承或组合 `PlotResult`，
统一链式调用层。重构方向：

```python
# fluent.py
class FigureWrapper(PlotResult):
    """FigureWrapper 就是带 chain context 的 PlotResult"""
    
    def __init__(self, fig, ax, chain: PlotChain):
        super().__init__(fig, ax)
        self._chain = chain
    
    # 只需新增 PlotResult 里没有的方法（如切换回 chain 的操作）
    # 其他 .xlabel/.ylabel/.save 等全继承自 PlotResult
```

---

### Issue 2：`plot_combo` 返回裸 tuple，破坏统一性

```python
# distribution.py
def plot_combo(...) -> Tuple[Figure, Axes, Optional[Axes]]:
    ...
    return fig, ax_bar, ax_line   # ← 三元组，无法被 PlotResult 包装
```

这是唯一一个返回三元组的公开函数。建议创建一个专用的返回类型：

```python
# result.py 新增
class ComboPlotResult(PlotResult):
    """组合图结果，包含主轴和可选副轴"""
    
    def __init__(self, fig, ax_bar, ax_line=None):
        super().__init__(fig, ax_bar)
        self.ax_line = ax_line       # 副 Y 轴（可能为 None）
        self.ax_bar = ax_bar         # 主轴（bar 那侧）
    
    def __iter__(self):
        yield self._fig
        yield self._ax
        yield self.ax_line           # 三元解包兼容
```

用法变成：
```python
result = sp.plot_combo(...)
fig, ax_bar, ax_line = result   # 三元解包仍然有效
result.ax_bar.set_ylabel("...")  # 属性访问
result.save("combo")            # 链式保存
```

---

### Issue 3：`plot_clustermap` 的 figsize 是硬编码 (10, 10)

```python
# hierarchical.py
def plot_clustermap(...):
    fig = plt.figure(figsize=(10, 10))   # ← 硬编码
```

应该尊重 venue 的默认尺寸：
```python
_, base_figsize, _ = VENUES.get(effective_venue or "nature", VENUES["nature"])
heatmap_scale = max(base_figsize)
fig = plt.figure(figsize=(heatmap_scale, heatmap_scale))
```

---

### Issue 4：`plot_network` 使用已废弃的 matplotlib API

```python
# network.py
cmap = plt.cm.get_cmap("viridis")   # matplotlib 3.7+ 废弃，3.9 移除
```

应该改为：
```python
try:
    cmap = plt.colormaps["viridis"]   # matplotlib >= 3.5
except AttributeError:
    cmap = plt.cm.get_cmap("viridis") # fallback
```

---

### Issue 5：`radar` 数值标注位置在极坐标下偏移错误

```python
# polar.py
ax.annotate(
    f"{value:.2f}",
    xy=(angle, value),
    xytext=(angle, value + 0.08),   # ← 在极坐标下 +0.08 是径向偏移
    ...
)
```

极坐标里 `value + 0.08` 是往外偏移 0.08 个单位，对于 0-1 范围的数据基本不可见，
对于 0-100 的数据又会偏移太多。应该改成相对偏移：

```python
y_max = max(max(v) for v in values_list)
offset = y_max * 0.08   # 相对于数据范围的 8%

ax.annotate(
    f"{value:.2f}",
    xy=(angle, value),
    xytext=(angle, value + offset),
    ...
)
```

---

## 三、功能扩展：小而美的新增

---

### 新图表 1：`plot_lollipop`（棒棒糖图）

比柱状图更清晰的单维度排名展示，在 CS/统计论文里用来展示特征重要性、
模型得分等，比 `plot_horizontal_bar` 信息密度更高。

```python
# distribution.py 新增
def plot_lollipop(
    categories: List[str],
    values: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    sort: bool = True,
    marker_size: float = 8,
    stem_width: float = 2.0,
    baseline: float = 0.0,
    venue: Optional[str] = None,
    palette: Optional[str] = None,
    **kwargs,
) -> PlotResult:
    """
    绘制棒棒糖图（比柱状图更清晰的类别对比）
    
    示例:
        >>> features = ["模型A", "模型B", "模型C", "模型D"]
        >>> scores   = [88.5, 85.2, 90.1, 83.7]
        >>> fig, ax = sp.plot_lollipop(features, scores, ylabel="F1 Score (%)", sort=True)
        >>> sp.save(fig, "comparison")
    """
```

实现要点：
- 用 `ax.hlines(baseline, ...)` 画茎（水平基线）
- 用 `ax.vlines(x, baseline, values)` 画竖线
- 用 `ax.scatter(x, values, ...)` 画圆头
- 排序时同步对 categories 和 values 排序

---

### 新图表 2：`plot_slope`（斜率图）

展示两个时间点（或条件）之间的变化，比折线图在两点对比时更清晰。
常见于 before/after 对比、A/B test 结果展示。

```python
# timeseries.py 或 basic.py 新增
def plot_slope(
    labels: List[str],           # 各实体的标签（如 ["方法A", "方法B", "方法C"]）
    before: List[float],         # 左侧值
    after: List[float],          # 右侧值
    left_label: str = "Before",  # 左轴标签
    right_label: str = "After",  # 右轴标签
    show_diff: bool = True,      # 是否在右侧标注变化量
    venue: Optional[str] = None,
    palette: Optional[str] = None,
) -> PlotResult:
    """
    绘制斜率图（两点变化对比）
    
    示例:
        >>> methods = ["ResNet", "ViT", "本文"]
        >>> acc_before = [82.3, 85.7, 88.1]
        >>> acc_after  = [84.1, 87.2, 91.5]
        >>> fig, ax = sp.plot_slope(methods, acc_before, acc_after,
        ...     left_label="微调前", right_label="微调后", show_diff=True)
        >>> sp.save(fig, "finetuning_effect")
    """
```

---

### 新图表 3：`plot_density`（核密度估计）

比直方图更平滑地展示数据分布，统计/机器学习论文里常见。
基于 scipy.stats.gaussian_kde，已经是 core dep 了（可以直接用）。

```python
# distribution.py 或 statistical.py 新增
def plot_density(
    data: np.ndarray,
    xlabel: str = "",
    ylabel: str = "Density",
    title: str = "",
    bw_method: Optional[float] = None,  # KDE 带宽
    fill: bool = True,
    alpha: float = 0.3,
    venue: Optional[str] = None,
    palette: Optional[str] = None,
) -> PlotResult:
    """
    绘制核密度估计曲线（KDE，比直方图更平滑）
    
    示例:
        >>> data = np.random.normal(0, 1, 500)
        >>> fig, ax = sp.plot_density(data, xlabel="残差", fill=True)
        >>> sp.save(fig, "residual_distribution")
    """

# 顺带做多组对比版本
def plot_multi_density(
    data_list: List[np.ndarray],
    labels: Optional[List[str]] = None,
    ...
) -> PlotResult:
    """多组 KDE 对比图"""
```

---

### 新图表 4：`plot_scatter_matrix`（散点矩阵/配对图）

多特征两两关系展示，数据探索阶段必备，生物信息/统计论文高频。

```python
# multivariate.py 新增
def plot_scatter_matrix(
    data: np.ndarray,
    columns: Optional[List[str]] = None,
    color_by: Optional[np.ndarray] = None,
    diag: str = "hist",          # "hist" | "kde" | "none"
    alpha: float = 0.5,
    s: float = 10,
    venue: Optional[str] = None,
    palette: Optional[str] = None,
) -> PlotResult:
    """
    绘制散点矩阵（配对图）
    
    参数:
        diag: 对角线展示方式
              "hist" → 直方图（默认）
              "kde"  → 核密度曲线
              "none" → 空白
    
    示例:
        >>> data = np.random.randn(100, 4)
        >>> fig, axes = sp.plot_scatter_matrix(data,
        ...     columns=["特征A", "特征B", "特征C", "特征D"])
        >>> sp.save(fig, "pairplot")
    """
```

---

### 配色新增：发散型配色（为热力图/相关矩阵专用）

```python
# palette.py 新增
DIVERGING_PALETTES: Dict[str, List[str]] = {
    # 经典红蓝发散（相关矩阵最常用）
    "rdbu":    ["#8B1C2D", "#C44B5E", "#E8A0AA", "#F5F5F5", "#A0C8E0", "#4B7BA8", "#1C3D6B"],
    # 冷暖发散（科研常见）
    "coolwarm": ["#3A5FCC", "#7A9EF0", "#C8D8F8", "#F5F5F5", "#F8C8C8", "#F07A7A", "#CC3A3A"],
}
```

这些用于 `plot_heatmap` 的 `cmap` 参数时，应该能被 `sp.get_palette("rdbu")` 
返回颜色列表，但核心使用方式是：
```python
fig, ax = sp.plot_heatmap(corr_matrix, cmap="rdbu")
```

所以需要把它们注册为 matplotlib colormap：

```python
def _register_diverging_cmaps():
    """把发散型配色注册为 matplotlib colormap"""
    from matplotlib.colors import LinearSegmentedColormap
    for name, colors in DIVERGING_PALETTES.items():
        if name not in plt.colormaps:
            cmap = LinearSegmentedColormap.from_list(f"sp.{name}", colors)
            plt.colormaps.register(cmap)
```

---

## 四、代码质量：不大但值得做的改进

---

### 4.1 `config.py` 的 `tomllib` 导入降级问题

```python
# 当前代码
try:
    import tomllib          # Python 3.11+ 内置
except ImportError:
    import tomli as tomllib # 需要额外安装
```

问题：用户用 Python 3.8-3.10 时，如果没装 `tomli`，config 模块会崩。
但 `tomli` 并没有在 `pyproject.toml` 的 dependencies 里声明。

**修复：** 要么加进 dependencies，要么在 `load_config` 里 catch ImportError：
```python
def load_config(...):
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            warnings.warn(
                "配置文件功能需要 Python 3.11+ 或安装 tomli: pip install tomli",
                UserWarning,
            )
            return False
    ...
```

---

### 4.2 `smart.py` 中 `auto_rotate_labels` 的时机问题

```python
# 当前代码
labels = ax.get_xticklabels()
tick_labels = [t.get_text() for t in labels]  # ← 渲染前 text 可能为空
```

matplotlib 在调用 `fig.draw()` 或 `plt.show()` 前，
tick label 的文本有时是空字符串（特别是数值轴）。

**修复：** 先 `fig.canvas.draw()` 强制渲染一次再读：

```python
def auto_rotate_labels(ax, axis="x", ...):
    try:
        ax.figure.canvas.draw()  # 强制更新 tick 位置和文本
    except Exception:
        pass  # headless 环境可能失败，直接跳过
    
    if axis == "x":
        labels = ax.get_xticklabels()
        tick_labels = [t.get_text() for t in labels]
        ...
```

---

### 4.3 `plot_radar` 的 `show_labels=True` 在多组数据时会混乱

当 `values_list` 有多组数据时，每组数据的数值都会被标注，
导致同一个角度有多个重叠的数值标签。

**修复：** `show_labels` 默认改为 `False`，或只标注第一组数据：

```python
# 改成只在有需要时才标注（且只标注最后一个系列）
if show_labels and len(values_list) == 1:
    for angle, value in zip(angles[:-1], values_list[0]):
        ...
elif show_labels:
    # 多组时忽略数值标签，只显示图例
    pass
```

---

### 4.4 `plot_parallel` 中连续值的 colorbar 位置

当 `color_by` 是连续数值时，`fig.colorbar(sm, ax=ax, ...)` 会压缩
主图宽度。对于 nature/ieee 的精确版心控制来说，这会导致实际输出宽度
与预期不符。

**建议：** 给 `plot_parallel` 的连续着色模式增加一个 `show_colorbar` 参数，
默认 `True`，让用户可以关闭：
```python
def plot_parallel(
    ...,
    show_colorbar: bool = True,  # 新增
    ...
):
```

---

### 4.5 `pyproject.toml` 版本号与 `__init__.py` 不一致

```toml
# pyproject.toml
version = "1.7.5"
```
```python
# __init__.py
__version__ = "1.7.4"   # ← 落后一个版本
```

建议用 `importlib.metadata` 动态读取，避免双维护：
```python
# __init__.py
from importlib.metadata import version as _get_version
try:
    __version__ = _get_version("sciplot-academic")
except Exception:
    __version__ = "1.7.5"  # fallback
```

---

## 五、优先级总表

| 优先级 | 类型 | 内容 | 影响范围 | 工作量 |
|--------|------|------|----------|--------|
| 🔴 P0 | Bug | `list_rmb_palettes` ImportError | 所有用户无法 import | 5 min |
| 🔴 P0 | Bug | `EARTH_PALETTE` 不在 RESIDENT_PALETTES | earth 系列完全失效 | 5 min |
| 🔴 P0 | Bug | 可选依赖顶层导入 | 未装 networkx/venn 的用户崩溃 | 30 min |
| 🔴 P0 | Bug | `plot_multi` 默认 None palette 不触发智能子集 | 核心功能异常 | 10 min |
| 🟠 P1 | Bug | `aliases.py` 返回类型注解错误 | IDE/类型检查误报 | 15 min |
| 🟠 P1 | 架构 | `FigureWrapper` 继承 `PlotResult` | 统一 API，减少双维护 | 2h |
| 🟠 P1 | 架构 | `ComboPlotResult` 三元返回 | 语义清晰 | 1h |
| 🟠 P1 | Bug | `plot_clustermap` figsize 硬编码 | 尺寸不匹配 venue | 10 min |
| 🟠 P1 | Bug | `plot_network` 废弃 API | matplotlib 3.9 会报错 | 10 min |
| 🟠 P1 | Bug | `plot_radar` 数值标注偏移 | 多组数据时混乱 | 10 min |
| 🟡 P2 | 功能 | 加回人民币配色（作为特色） | 用户预期 | 20 min |
| 🟡 P2 | 功能 | 发散型配色 rdbu/coolwarm | 热力图必备 | 30 min |
| 🟡 P2 | 功能 | `plot_lollipop` 棒棒糖图 | 高频学术图表 | 1h |
| 🟡 P2 | 功能 | `plot_density` / `plot_multi_density` | 统计论文必备 | 1h |
| 🟡 P2 | 功能 | `plot_slope` 斜率图 | before/after 对比 | 1h |
| 🟡 P2 | 质量 | `tomllib` ImportError 处理 | Python <3.11 | 15 min |
| 🟡 P2 | 质量 | `auto_rotate_labels` 渲染时机 | 标签检测失效 | 20 min |
| 🟢 P3 | 功能 | `plot_scatter_matrix` 配对图 | 数据探索 | 2h |
| 🟢 P3 | 质量 | `__version__` 动态读取 | 双维护问题 | 5 min |
| 🟢 P3 | 质量 | `plot_parallel` colorbar 参数 | 精确版心控制 | 10 min |

---

## 六、v1.8.0 版本定义建议

**原则：先堵漏洞，再增功能。**

### 必须进 v1.8.0 的（P0+P1）
1. 修复所有 5 个 Bug（ImportError 类的在发版前必须跑一遍 `python -c "import sciplot"`）
2. 人民币配色加回来
3. `FigureWrapper` 合并进 `PlotResult`（或至少统一接口）
4. scipy 从 core deps 移出
5. 废弃 API 替换

### 可以进 v1.8.0 的（如果时间够）
1. `plot_lollipop`
2. `plot_density`
3. 发散型配色

### 留到 v1.9.0 的
1. `plot_slope`
2. `plot_scatter_matrix`
3. `plot_waterfall`（适合财务/工程领域论文）

---

## 七、一个被忽视的长期机会：`sp.inspect()` 诊断函数

科研用户最常见的环境问题：字体缺失导致中文方块字、scienceplots 安装位置不对、
依赖版本冲突。

建议新增一个 `sp.inspect()` 诊断工具：

```python
def inspect() -> None:
    """
    检查 SciPlot 运行环境，输出诊断信息
    
    示例:
        >>> sp.inspect()
        
        SciPlot Academic v1.8.0 环境诊断
        ══════════════════════════════════
        ✓ matplotlib    3.8.2
        ✓ numpy         1.26.0
        ✓ scienceplots  2.1.0
        ✓ scipy         1.11.0  (statistical plots)
        ✗ networkx      未安装   (network plots: pip install networkx)
        ✗ matplotlib-venn 未安装 (venn plots: pip install matplotlib-venn)
        
        字体检查:
        ✓ SimSun        (中文宋体，thesis/中文模式)
        ✗ Times New Roman (英文模式，建议安装)
        
        已注册配色: pastel, ocean, forest, sunset, 100yuan, ...
        当前默认: venue=nature, palette=pastel, lang=zh
    """
```

这个功能对新用户的 onboarding 价值极大，而且实现只需要约 60 行代码。

