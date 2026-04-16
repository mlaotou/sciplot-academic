# SciPlot Academic — 科研绘图 Skill

---
name: sciplot
description: >
  科研绘图技能（sciplot-academic 包版 v1.7.1）。
  
  **必须使用本技能的场景**：
  - 用户需要绘制学术图表、论文插图、数据可视化
  - 用户提到 matplotlib、seaborn、plotly 等绘图库
  - 用户需要 Nature/IEEE/APS/Springer 等期刊格式的图表
  - 用户需要中文优化的科研图表（中文字体、中文标签）
  - 用户提到毕业设计图片、竞赛图表、论文配图
  - 用户需要箱线图、小提琴图、热力图、散点图、柱状图、折线图等
  - 用户需要多子图布局、显著性标注、配色方案
  - 用户提到 "画图"、"可视化"、"图表"、"figure"、"plot"
  
  **本技能提供**：
  - 默认中文 + Nature 期刊样式 + pastel 配色
  - 支持 IEEE/APS/Springer/Thesis 学位论文等期刊格式
  - 提供折线、散点、柱状、分组柱状、堆叠柱状、水平柱状、面积图、
    箱线、小提琴、热力图、阶梯图、误差条、置信区间、组合图、多子图、
    显著性标注等全类型图表
  - 语法糖功能：Fluent Interface 链式调用、Context Manager 上下文管理器、
    简洁函数别名
  - 语言自适应：中文模式自动禁用 LaTeX（避免 U+2212 警告），
    英文模式自动启用 LaTeX（数学公式更美观）
  
  **使用方式**：直接 `import sciplot as sp`，无需复制任何文件到项目目录。
  所有图表代码必须生成为独立可运行的 Python 脚本。
---

## 快速决策

**用户需要科研图表？→ 使用本技能**

无论用户提到的是：
- "帮我画个图"
- "论文需要插图"
- "matplotlib 怎么用"
- "这个数据显示一下"
- "Nature 格式的图"
- "中文图表"

都使用 `import sciplot as sp` 解决。

---

## 30 秒上手

```python
import sciplot as sp
import numpy as np

x = np.linspace(0, 10, 200)

# 方式 1: 传统 API
fig, ax = sp.plot(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
sp.save(fig, "结果图")

# 方式 2: 链式调用（语法糖）
fig = sp.style("nature").palette("pastel").plot(x, np.sin(x)).save("结果图")

# 方式 3: 简洁别名
fig, ax = sp.line(x, np.sin(x), xlabel="时间 (s)", ylabel="电压 (V)")
sp.save(fig, "结果图")
```

---

## 核心工作流

### Step 1: 确定场景

| 用户场景 | Venue | 格式 | DPI | 语言 |
|---------|-------|------|-----|------|
| Word 中文论文 | `thesis` | PNG | 1200 | zh |
| IEEE 英文投稿 | `ieee` | PDF | — | en |
| Nature 英文投稿 | `nature` | PDF | — | en |
| 学位论文 | `thesis` | PNG/PDF | 1200 | zh |

### Step 2: 选择 API 风格

**风格 A: 传统 API（推荐用于复杂图表）**
```python
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, ax = sp.plot(x, y, xlabel="X", ylabel="Y")
sp.save(fig, "output", formats=("png",), dpi=1200)
```

**风格 B: 链式调用（推荐用于快速绘图）**
```python
fig = (sp.style("ieee")
         .palette("earth")
         .plot(x, y1, label="A")
         .plot(x, y2, label="B")
         .legend()
         .save("output"))
```

**风格 C: 简洁别名（推荐用于简单图表）**
```python
fig, ax = sp.line(x, y)
fig, ax = sp.scatter(x, y)
fig, ax = sp.bar(categories, values)
```

### Step 3: 生成独立脚本

**必须创建独立可运行的 Python 脚本**，不要只给代码片段。

```python
"""
科研绘图脚本
依赖: pip install sciplot-academic
运行: python plot_result.py
"""
import numpy as np
import sciplot as sp

# 数据准备
x = np.linspace(0, 10, 200)
y1, y2 = np.sin(x), np.cos(x)

# 绘图
sp.setup_style("thesis", "pastel-2", lang="zh")
fig, ax = sp.plot(x, y1, xlabel="时间 (s)", ylabel="幅度")
sp.save(fig, "结果", formats=("png",), dpi=1200)

print("✓ 已保存")
```

---

## 关键特性详解

### 语言与 LaTeX 自动适配

```python
# 中文模式：自动禁用 LaTeX，中文显示正常，负号使用 ASCII
sp.setup_style("thesis", lang="zh")

# 英文模式：自动启用 LaTeX，数学公式更美观
sp.setup_style("ieee", lang="en")
```

### 智能配色选择

```python
# 自动根据数据量选择配色子集
sp.plot_multi(x, [y1, y2, y3])        # 自动使用 pastel-3
sp.plot_multi(x, [y1, y2, y3, y4])    # 自动使用 pastel-4
```

### 上下文管理器

```python
# 临时切换样式，不影响全局
with sp.style_context("ieee", palette="earth"):
    fig, ax = sp.plot(x, y)
    sp.save(fig, "ieee_style")

# 恢复默认样式
fig, ax = sp.plot(x, y)  # 使用 nature + pastel
```

---

## 图表类型速查

### 基础图表
- `sp.plot(x, y)` / `sp.line(x, y)` - 折线图
- `sp.scatter(x, y)` - 散点图
- `sp.plot_step(x, y)` / `sp.step(x, y)` - 阶梯图
- `sp.plot_area(x, y)` / `sp.area(x, y)` - 面积图
- `sp.plot_multi(x, [y1, y2])` - 多线图

### 柱状图
- `sp.plot_bar(cats, vals)` / `sp.bar(cats, vals)` - 单组柱状图
- `sp.plot_grouped_bar(groups, data)` - 分组柱状图（论文最常用）
- `sp.plot_stacked_bar(cats, data)` - 堆叠柱状图
- `sp.plot_horizontal_bar(cats, vals)` / `sp.hbar(cats, vals)` - 水平柱状图

### 分布图表
- `sp.plot_box(data)` / `sp.box(data)` - 箱线图
- `sp.plot_violin(data)` / `sp.violin(data)` - 小提琴图
- `sp.plot_histogram(data)` / `sp.hist(data)` - 直方图
- `sp.plot_heatmap(data)` / `sp.heatmap(data)` - 热力图

### 误差与置信
- `sp.plot_errorbar(x, y, yerr)` / `sp.errorbar(x, y, yerr)` - 误差条
- `sp.plot_confidence(x, mean, std)` - 置信区间

### 组合与标注
- `sp.plot_combo(x, bar_data, line_data)` - 组合图（柱状+折线）
- `sp.annotate_significance(ax, x1, x2, y, p_value)` - 显著性标注

---

## 布局系统

### 期刊尺寸

| venue | 尺寸（英寸） | 适用场景 |
|-------|-------------|----------|
| `nature` | 7.0 × 5.0 | Nature/Science 双栏全图 |
| `ieee` | 3.5 × 3.0 | IEEE 单栏 |
| `aps` | 3.4 × 2.8 | APS Physical Review |
| `springer` | 6.0 × 4.5 | Springer 期刊 |
| `thesis` | 6.1 × 4.3 | 学位论文（A4 版心） |

### 子图布局

```python
# 论文子图（推荐）
fig, axes = sp.paper_subplots(1, 2, venue="thesis")
axes[0].plot(x, y1)
axes[1].plot(x, y2)
sp.add_panel_labels(axes)  # 自动添加 (a) (b)
sp.save(fig, "subplots", formats=("png",), dpi=1200)
```

---

## 配色方案

### 三大常驻色系（推荐）
- `pastel` - 柔和粉彩（默认）
- `earth` - 大地色系
- `ocean` - 海洋蓝绿

### 使用方式
```python
sp.setup_style(palette="pastel-3")   # 使用前3色
sp.setup_style(palette="earth-2")    # 使用前2色
```

### 人民币系列
- `100yuan` (红) / `50yuan` (绿) / `20yuan` (棕)
- `10yuan` (蓝) / `5yuan` (紫) / `1yuan` (橄榄)

---

## 扩展功能

### 机器学习可视化
```python
from sciplot._ext.ml import plot_pca, plot_confusion_matrix

fig, ax = plot_pca(data, labels=labels)
fig, ax = plot_confusion_matrix(y_true, y_pred, labels=["A", "B", "C"])
```

### 3D 可视化
```python
from sciplot._ext.plot3d import plot_surface, plot_contour

fig, ax = plot_surface(X, Y, Z)
fig, ax = plot_contour(X, Y, Z, levels=15)
```

---

## 完整文档索引

详细文档请查阅 references/ 目录：

- [quickstart.md](./references/quickstart.md) - 快速上手与安装
- [syntax-sugar.md](./references/syntax-sugar.md) - 语法糖功能详解
- [core-functions.md](./references/core-functions.md) - 核心函数参考
- [charts.md](./references/charts.md) - 图表类型完整列表
- [color-schemes.md](./references/color-schemes.md) - 配色方案系统
- [layouts.md](./references/layouts.md) - 布局与多子图
- [extensions.md](./references/extensions.md) - ML 与 3D 扩展
- [best-practices.md](./references/best-practices.md) - 最佳实践与场景速查

---

## 黄金法则

1. **Word 用 PNG 1200 DPI，LaTeX 用 PDF**
2. **多子图总宽锁定**：用 `paper_subplots()` 或手动 `figsize=(6.1, h)`
3. **中文用 `lang="zh"`，英文用 `lang="en"`**
4. **≥4 条线用 `use_linestyles=True`**（色盲友好）
5. **必须生成独立可运行的 Python 脚本**

---

## 版本信息

- 包名：`sciplot-academic`（PyPI）
- 版本：**1.7.1**
- GitHub：https://github.com/rippleshe/sciplot-academic
