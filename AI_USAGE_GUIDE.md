# SciPlot AI 使用指南

## 核心原则（记住这三点）

1. **默认中文图** - 自动识别中文字符，优化字体
2. **默认 Nature 样式** - 单栏、高分辨率、无网格线
3. **默认 pastel 配色** - 柔和粉彩，1-4色自动用子集

---

## 方案一：全局安装（推荐）

### 一次性安装

```bash
# 在 sciplot 目录执行
cd d:\ZPan\PythonPackage\sciplot
uv pip install -e .
```

安装后，**任何项目**都可以直接导入：

```python
import sciplot as sp
```

### 为项目初始化 sciplot 骨架

当用户说"在这个项目使用 sciplot"时，执行：

```python
# 复制 project_init.py 到项目根目录，然后运行
exec(open("project_init.py").read())
init_project()
```

这会生成：
- `plotting.py` - 项目级绘图配置（自动查找 sciplot）
- `plotting_example.py` - 使用示例
- `SCIPLOT_USAGE.md` - 使用说明

之后用户代码中使用：

```python
from plotting import plot, plot_multi, save

# 或查看示例运行
# python plotting_example.py
```

---

## 方案二：复制文件（备用）

如果无法全局安装，将 `sciplot.py` 复制到项目目录：

```python
import shutil
import sys

# 复制 sciplot.py 到当前项目
src = r"d:\ZPan\PythonPackage\sciplot\sciplot.py"
dst = "sciplot.py"
shutil.copy(src, dst)
print(f"已复制 sciplot.py 到当前目录")
```

然后直接导入：

```python
import sciplot as sp
```

---

## 最常用的 3 个函数

| 函数 | 用途 | 示例 |
|------|------|------|
| `plot()` | 画单条线 | `plot(x, y, xlabel="时间", ylabel="电压")` |
| `plot_multi()` | 画多条线 | `plot_multi(x, [y1, y2], labels=["A", "B"])` |
| `save()` | 保存图片 | `save(fig, "结果图")` 生成 PDF + PNG |

---

## 三大常驻配色系（都有1-4色子集）

| 配色 | 风格 | 1-4条线自动子集 |
|------|------|-----------------|
| `pastel` | 柔和粉彩（默认） | pastel-1/2/3/4 |
| `earth` | 大地色系 | earth-1/2/3/4 |
| `ocean` | 海洋蓝绿 | ocean-1/2/3/4 |

```python
# 2条线自动用 pastel-2
plot_multi(x, [y1, y2])

# 3条线自动用 earth-3
plot_multi(x, [y1, y2, y3], palette="earth")

# 4条线自动用 ocean-4
plot_multi(x, [y1, y2, y3, y4], palette="ocean")
```

---

## 完整 API 速查

### 图表类型

```python
plot(x, y)                    # 单线图
plot_multi(x, [y1, y2])       # 多线图
plot_scatter(x, y)            # 散点图
plot_bar(categories, values)  # 柱状图
plot_box(data)                # 箱线图
plot_violin(data)             # 小提琴图
plot_errorbar(x, y, yerr)     # 误差条图
plot_confidence(x, mean, std) # 置信区间图
plot_heatmap(data)            # 热力图
plot_histogram(data)          # 直方图
```

### 布局

```python
create_subplots(2, 2)         # 2x2 子图
create_gridspec(2, 2)         # 不规则布局
create_twinx(ax)              # 双 Y 轴
```

### 工具

```python
setup_style(venue="nature", palette="pastel", lang="zh")
new_figure(venue="nature")
save(fig, "文件名", dpi=300)

# 查看配色
list_palettes()               # 所有配色
list_resident_palettes()      # 三大配色系
get_palette("pastel")         # 获取颜色列表
```

---

## 典型使用场景

### 场景1：用户说"画个对比图"

```python
from plotting import plot_multi, save
import numpy as np

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plot_multi(
    x, [y1, y2],
    labels=["方法A", "方法B"],
    xlabel="时间 (s)",
    ylabel="幅值",
    title="两种方法对比"
)
save(fig, "方法对比")
```

### 场景2：用户说"用大地色系"

```python
fig, ax = plot_multi(
    x, [y1, y2, y3],
    labels=["实验组", "对照组", "基准组"],
    palette="earth"  # 自动用 earth-3
)
```

### 场景3：用户说"画中文图"

```python
# 默认就是中文，直接用中文标签
fig, ax = plot(x, y, xlabel="迭代次数", ylabel="准确率 (%)")
```

---

## 给 AI 的指令模板

当用户要求使用 sciplot 时，按以下步骤：

1. **检查是否已安装**
   ```python
   import importlib.util
   spec = importlib.util.find_spec("sciplot")
   if spec is None:
       print("sciplot 未安装，请先运行: uv pip install -e d:/ZPan/PythonPackage/sciplot")
   ```

2. **为项目初始化骨架**
   ```python
   # 复制 project_init.py 并运行
   import shutil
   shutil.copy(r"d:\ZPan\PythonPackage\sciplot\project_init.py", "project_init.py")
   exec(open("project_init.py").read())
   init_project()
   ```

3. **使用 plotting 模块绘图**
   ```python
   from plotting import plot, plot_multi, save
   # ... 绘图代码 ...
   ```

---

## 常见问题

**Q: 用户项目里没有 sciplot 怎么办？**
A: 运行 `project_init.py` 生成 `plotting.py`，它会自动查找 sciplot。

**Q: 如何切换配色？**
A: 在 `plot_multi()` 中使用 `palette` 参数：
   - `palette="pastel"` (默认)
   - `palette="earth"` (大地色)
   - `palette="ocean"` (海洋蓝绿)

**Q: 如何切换期刊样式？**
A: 使用 `venue` 参数：
   - `venue="nature"` (默认)
   - `venue="ieee"` (IEEE双栏)
   - `venue="thesis"` (学位论文)

**Q: 如何保存高清图？**
A: `save(fig, "文件名", dpi=600)` 默认保存 PDF + PNG

---

## 能力边界（重要）

**SciPlot 不支持的图表类型**：

| 图表类型 | 替代方案 |
|---------|---------|
| 决策树 | `sklearn.tree.plot_tree` |
| 神经网络结构图 | `PlotNeuralNet` / `NN-SVG` |
| 流程图/拓扑图 | `graphviz` / `Mermaid` |
| 网络关系图 | `networkx` |
| 地理/地图 | `cartopy` / `folium` |
| 3D 图 | `matplotlib 3D` / `plotly` |
| 雷达图/桑基图/树状图 | `matplotlib` / `plotly` |

**判断准则**：当用户提到以下关键词时，**不要调用 SciPlot**：
```
决策树, 神经网络结构, 流程图, 地图, 3D, 雷达图, 桑基图, 甘特图...
```

---

## 版本信息

- SciPlot: 1.4.0
- 三大配色系: pastel, earth, ocean
- 默认: Nature样式 + pastel配色 + 中文
